#include "msp430/insloader.h"
#include "msp430/emu.h"
#include <opa/utils/string.h>

using namespace std;

namespace opa {
namespace emu {
namespace msp430 {

#define READ_REG(x) (cpu->reg(x).read())
#define WRITE_REG(x, v) (cpu->reg(x).write(v))

#define WRITE_MEM(x, v) (memory->write(x, v))
#define READ_MEM(x) (memory->read(x))

void Ins::init(EmuMsp430 *emu) {
    m_emu = emu;
    cpu = &m_emu->cpu;
    memory = &m_emu->memory;

    REP(i, 2) m_ops[i].init(emu, this);

#define INS_DECL(name, fmt, code, op1, op2)                                    \
    handle_ins_decl(INS_ENUM_NAME(name), #name, fmt, code,                     \
                    &Ins::INS_HANDLER_NAME(name), INS_OP_MODE(op1),            \
                    INS_OP_MODE(op2));
#include <opa/emu/msp430/ins_vals.h>
#undef INS_DECL
}

void Ins::do_jump() {
    u16 val = m_ops[0].get();
    m_emu->cpu.set_pc(val);
}

#define INS_PROTO(name) void Ins::INS_HANDLER_NAME(name)()
#define INS_JMP_PROTO(name, cond, flags_var)                                   \
    INS_PROTO(name) {                                                          \
        FlagHandler &flags_var = m_emu->cpu.flags;                             \
        if (cond)                                                              \
            do_jump();                                                         \
    }

#define INS_SINGLEOP_PROTO(name, O)                                            \
    INS_PROTO(name) {                                                          \
        if (m_bytemode)                                                        \
            m_ops[0].set(cpu->op_##O##b(m_ops[0].get()));                      \
        else                                                                   \
            m_ops[0].set(cpu->op_##O(m_ops[0].get()));                         \
    }

#define INS_DOUBLEOP_PROTO(name, O)                                            \
    INS_PROTO(name) {                                                          \
        u16 res;                                                               \
        if (m_bytemode)                                                        \
            res = cpu->op_##O##b(m_ops[0].get(), m_ops[1].get());              \
        else                                                                   \
            res = cpu->op_##O(m_ops[0].get(), m_ops[1].get());                 \
        m_ops[1].set(res);                                                     \
    }

#define INS_DOUBLEOP_PROTO_NOSET(name, O)                                      \
    INS_PROTO(name) {                                                          \
        if (m_bytemode)                                                        \
            cpu->op_##O##b(m_ops[0].get(), m_ops[1].get());                    \
        else                                                                   \
            cpu->op_##O(m_ops[0].get(), m_ops[1].get());                       \
    }

INS_SINGLEOP_PROTO(RRC, rrc)
INS_SINGLEOP_PROTO(RRA, rra)

INS_PROTO(SWPB) {
    u16 tmp = m_ops[0].get();
    m_ops[0].set(tmp >> 8 | tmp << 8);
}

INS_PROTO(SXT) { m_ops[0].set(cpu->op_sxt(m_ops[0].get())); }

INS_PROTO(PUSH) {
    u16 sp = READ_REG(REG_SP) - 2;
    WRITE_REG(REG_SP, sp);
    u16 w = m_ops[0].get();
    if (m_bytemode)
        w |= READ_MEM(sp) & 0xff00;
    WRITE_MEM(sp, w);
}

INS_PROTO(CALL) {
    u16 sp = READ_REG(REG_SP) - 2;
    WRITE_REG(REG_SP, sp);
    u16 w = READ_REG(REG_PC);
    WRITE_MEM(sp, w);
    WRITE_REG(REG_PC, m_ops[0].get());
}

INS_PROTO(RETI) { assert(0); }

INS_JMP_PROTO(JEQ, x.z(), x)
INS_JMP_PROTO(JNE, !x.z(), x)
INS_JMP_PROTO(JC, x.c(), x)
INS_JMP_PROTO(JNC, !x.c(), x)
INS_JMP_PROTO(JN, x.n(), x)
INS_JMP_PROTO(JGE, (x.n() ^ x.v()) == 0, x)
INS_JMP_PROTO(JL, (x.n() ^ x.v()) == 1, x)
//INS_JMP_PROTO(JGE, (x.n() ^ x.v()) == 0, x)
//INS_JMP_PROTO(JL, (x.n() ^ x.v()) == 1, x)
INS_JMP_PROTO(JMP, 1, x)

INS_PROTO(MOV) { m_ops[1].set(m_ops[0].get()); }

INS_DOUBLEOP_PROTO(ADD, add)
INS_DOUBLEOP_PROTO(ADDC, addc)
INS_DOUBLEOP_PROTO(SUB, sub)
INS_DOUBLEOP_PROTO(SUBC, subc)
INS_DOUBLEOP_PROTO(DADD, dadd)
INS_DOUBLEOP_PROTO(BIC, bic)
INS_DOUBLEOP_PROTO(BIS, bis)
INS_DOUBLEOP_PROTO(XOR, xor)
INS_DOUBLEOP_PROTO(AND, and)

INS_DOUBLEOP_PROTO_NOSET(CMP, cmp)
INS_DOUBLEOP_PROTO_NOSET(BIT, bit)

void Ins::handle_ins_decl(InsType type, const std::string &name,
                          InsFormat format, u16 code, InsHandler handler,
                          OpMode op1, OpMode op2) {
    if (format == Format_SingleOp)
        m_single_op_mapping[code] = type;
    else if (format == Format_DoubleOp)
        m_double_op_mapping[code] = type;
    else
        m_jmp_op_mapping[code] = type;

    InsDesc desc = {};
    desc.op_mode[0] = op1;
    desc.op_mode[1] = op2;
    desc.type = type;
    desc.format = format;
    desc.name = name;
    desc.handler = handler;
    m_ins_mapping[type] = desc;
}

Ins::InsType Ins::get_ins_type(u16 w) {
    u16 tmp = w >> 12;

    if (tmp == 1) {
        u16 x = w & 0xf80;
        if (!m_single_op_mapping.count(x))
            return Ins_Invalid;
        return m_single_op_mapping[x];

    } else if (tmp == 2 || tmp == 3) {
        u16 x = w >> 8 & 0xfc;
        if (!m_jmp_op_mapping.count(x))
            return Ins_Invalid;
        return m_jmp_op_mapping[x];

    } else {
        u16 x = w >> 12;
        if (!m_double_op_mapping.count(x))
            return Ins_Invalid;
        return m_double_op_mapping[x];
    }
}

u16 Ins::get_next() {
    u16 pc = READ_REG(REG_PC);
    u16 val;
    if (pc == 0x0010)
        val = 0x4130;
    else
        val = READ_MEM(pc);

    m_len_op += 2;
    WRITE_REG(REG_PC, pc + 2);
    return val;
}

void Ins::load_op(Operand &op, OpMode type, u8 mode, u8 code) {
    op.type = Op_Invalid;

    //printf("on type=%d, mode=%x\n", type, mode);
    if (type == OpMode_None)
        return;

    if (type == OpMode_Src && (code == 2 || code == 3)) {
        if (code == 2) {
            if (mode == 0)
                op.build_reg(REG_SR);
            else if (mode == 1)
                op.build_regptr(REG_CG, get_next());
            else
                op.build_const(mode == 2 ? 4 : 8);
        } else
            op.build_const((mode + 1 & 3) - 1);
    } else {
        if (mode == 0)
            op.build_reg((RegEnum)code);
        else if (mode == 1)
            op.build_regptr((RegEnum)code, get_next());
        else {
            assert(type == OpMode_Src);

            if (mode == 2)
                op.build_regptr((RegEnum)code, 0);
            else if (mode == 3)
                op.build_regptrinc((RegEnum)code);
            else
                assert(0);
        }
    }
    op.set_bytemode(m_bytemode);
    op.load(type == OpMode_Dest);
}

void Ins::load() {
    m_orig_pc = READ_REG(REG_PC);
    m_len_op = 0;
    u16 b1 = get_next();
    m_raw = b1;

    Operand &op0 = m_ops[0];
    Operand &op1 = m_ops[1];

    m_type = get_ins_type(b1);
    if (m_type == Ins_Invalid) {
        OPA_ASSERT(0, "Failed to load ins, unknown.\nIns %04x:\n%s", b1,
                   m_emu->small_dump().c_str());
        return;
    }

    InsDesc &desc = m_ins_mapping[m_type];

    if (desc.format == Format_SingleOp) {
        m_nops = 1;
        m_bytemode = b1 >> 6 & 1;
        load_op(m_ops[0], desc.op_mode[0], b1 >> 4 & 0x3, b1 & 0xf);

    } else if (desc.format == Format_DoubleOp) {
        m_bytemode = b1 >> 6 & 1;
        m_nops = 2;
        load_op(m_ops[0], desc.op_mode[0], b1 >> 4 & 0x3, b1 >> 8 & 0xf);
        load_op(m_ops[1], desc.op_mode[1], b1 >> 7 & 0x1, b1 & 0xf);

    } else {
        u16 v = b1 & 0x3ff;
        if (v & 0x200)
            v = v - 1024;
        m_nops = 1;
        m_ops[0].build_regoff(REG_PC, v * 2);
        m_ops[0].load(false);
    }
}

void Ins::execute() {
    InsDesc &desc = m_ins_mapping[m_type];
    (this->*(desc.handler))();
}

string Ins::str() {
    string s;
    InsDesc &desc = m_ins_mapping[m_type];
    s += desc.name;
    if (m_bytemode)
        s += ".b";
    if (m_nops >= 1)
        s += " " + m_ops[0].str();
    if (m_nops == 2)
        s += ", " + m_ops[1].str();

    return s;
}

string Ins::oneliner_dump() {
    string res;
    res += utils::stdsprintf("pc=%04x %s", m_orig_pc, str().c_str());
    return res;
}

string Ins::dump() {
    string res;
    InsDesc &desc = m_ins_mapping[m_type];

    res += "====== Ins =====\n";
    u16 now_pc = READ_REG(REG_PC);
    res += utils::stdsprintf("old_pc=%x, pc=%x\n", m_orig_pc, now_pc);
    res +=
        utils::stdsprintf("PC data: %s, instype=%x, nops=%d\n",
                          utils::b2h(m_emu->peek(m_orig_pc, m_len_op)).c_str(),
                          desc.type, m_nops);
    res += utils::stdsprintf("Raw=%04x PC=%04x Mnemonic=%s\n", m_raw, m_orig_pc,
                             str().c_str());
    return res;
}
}
}
}
