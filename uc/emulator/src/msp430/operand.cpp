#include "msp430/operand.h"
#include "msp430/emu.h"
#include "msp430/ins.h"
#include <opa/utils/string.h>

using namespace std;

namespace opa {
namespace emu {
namespace msp430 {

#define READ_REG(x) (m_emu->cpu.reg(x).read())
#define WRITE_REG(x, v) (m_emu->cpu.reg(x).write(v))

#define WRITE_MEM(x, v, bytemode)                                              \
    (bytemode ? m_emu->memory.writeb(x, v) : m_emu->memory.write(x, v))
#define READ_MEM(x, bytemode)                                                  \
    (bytemode ? m_emu->memory.readb(x) : m_emu->memory.read(x))

void Operand::init(EmuMsp430 *emu, Ins *ins) {
    m_emu = emu;
    m_ins = ins;
}

u16 Operand::get() {
    if (type == Op_RegPtr && is_dest)
        return READ_MEM(src_val, bytemode);
    return src_val;
}

void Operand::set(u16 val) {
    switch (type) {
    case Op_Reg:
        WRITE_REG(op.regid, val);
        break;

    case Op_Memory:
        WRITE_MEM(op.mem, val, bytemode);
        break;
    case Op_RegPtr: {
        WRITE_MEM(src_val, val, bytemode);
        break;
    }
    case Op_RegOff:
        assert(0);
        WRITE_REG(op.reg.regid, val);
        break;

    default:
        assert(0);
    }
}

void Operand::load(bool is_dest) {
    this->is_dest = is_dest;

    if (type == Op_RegPtrInc) {
        u16 v = READ_REG(op.regid);
        src_val = READ_MEM(v, bytemode);
        u8 add = bytemode ? 1 : 2;
        if (op.regid == REG_PC)
            add = 2;
        WRITE_REG(op.regid, v + add);

    } else if (type == Op_RegOff) {
        src_val = READ_REG(op.reg.regid) + op.reg.off;

    } else if (type == Op_RegPtr) {
        src_val = op.reg.off;
        if (op.reg.regid != REG_CG && op.reg.regid != REG_SR)
            src_val += READ_REG(op.reg.regid);

        if (!is_dest)
            src_val = READ_MEM(src_val, bytemode);

    } else if (type == Op_Reg)
        src_val = READ_REG(op.regid);

    else if (type == Op_Memory)
        src_val = READ_MEM(op.mem, bytemode);

    else if (type == Op_Constant)
        src_val = op.C;

    else
        assert(0);
    //printf("result of load >> srcval=%x\n", src_val);
}

string Operand::str() {
    string res;

    if (type == Op_Reg)
        res = m_emu->cpu.reg(op.regid).str().c_str();
    else if (type == Op_Constant)
        res = utils::stdsprintf("#%04x", op.C);
    // else if (type == Op_Memory)
    //    res = utils::stdsprintf("#0x%04x", op.C);
    else if (type == Op_RegOff)
        res = utils::stdsprintf(
            "%s+#%04x", m_emu->cpu.reg(op.reg.regid).str().c_str(), op.reg.off);
    else if (type == Op_RegPtr)
        res = utils::stdsprintf("%04x(%s)", op.reg.off,
                                m_emu->cpu.reg(op.reg.regid).str().c_str());
    else if (type == Op_RegPtrInc)
        res = utils::stdsprintf("@(%s)+",
                                m_emu->cpu.reg(op.reg.regid).str().c_str());
    else {
        printf(">> type=%d\n", type);
        assert(0);
    }
    return res;
}
}
}
}
