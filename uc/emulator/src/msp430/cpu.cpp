#include "msp430/cpu.h"
#include <opa/utils/string.h>
#include "msp430/emu.h"

using namespace std;

namespace opa {
namespace emu {
namespace msp430 {
bool FlagHandler::has_flag(SR_Flags flag) { return (m_sr->read() & flag) != 0; }
const u16 RESERVED_MASK = 0xffff << 9;

void FlagHandler::set_flag(SR_Flags flag, bool v) {
    u16 cur = m_sr->read() & ~RESERVED_MASK;
    if (v)
        cur |= flag;
    else
        cur &= ~flag;

    m_sr->write(cur);
}

string FlagHandler::dump() {
    string res;
    res += c() ? "C" : " ";
    res += n() ? "N" : " ";
    res += v() ? "V" : " ";
    res += z() ? "Z" : " ";
    return res;
}

u16 FlagHandler::save() { return m_sr->read() & FLAG_ALL; }

void FlagHandler::restore(u16 v) {
    u16 x = m_sr->read() & ~FLAG_ALL;
    m_sr->write(x | v);
}

void FlagHandler::update(u32 res) {
    set_c(res >> 16 != 0);
    res &= 0xffff;
    set_z(res == 0);
    set_n(res >> 15);
}

void FlagHandler::updateb(u16 res) {
    set_c(res >> 8 != 0);
    res &= 0xff;
    set_z(res == 0);
    set_n(res >> 7);
}

void FlagHandler::update2(u16 res) {
    set_v(0);
    update(res);
    set_c(!z());
}
void FlagHandler::update2b(u8 res) {
    set_v(0);
    updateb(res);
    set_c(!z());
}

void Cpu::init() {
#define MSP430_REG(name, str) m_regs[REG_NAME(name)].init(REG_NAME(name), #str);
#include "msp430/reg_vals.h"
#undef MSP430_REG

    flags.init(&reg_sr());
}

string Cpu::dump_cpu() {
    string res;
    for (int i = 0; i < REG_ENUM_MAX; ++i) {
        res += utils::stdsprintf("%s=%04x", m_regs[i].str().c_str(),
                                 m_regs[i].read(true));
        if (i % 4 == 3)
            res += "\n";
        else
            res += " ";
    }
    res += "Flags: " + flags.dump();
    return res;
}

std::string Cpu::oneliner_dump() {

    string res;
    for (int i = 0; i < REG_ENUM_MAX; ++i) {
        res += utils::stdsprintf("%s=%04x", m_regs[i].str().c_str(),
                                 m_regs[i].read(true));
        res += " ";
    }
    res += flags.dump();
    return res;
}

#define sgn(x) (x >> 15 & 1 ? -1 : 1)
#define sgnb(x) (x >> 7 & 1 ? -1 : 1)

u16 Cpu::op_add(u16 a, u16 b, bool c) {
    u32 x = (u32)a + b + c;
    // flags.set_v(sgn(a + c) == sgn(b) && sgn(b) != sgn(x));
    flags.update(x);
    return x;
}

u8 Cpu::op_addb(u8 a, u8 b, bool c) {
    u16 x = (u16)a + b + c;
    // flags.set_v(sgnb(a + c) == sgnb(b) && sgnb(b) != sgnb(x));
    flags.updateb(x);
    return x;
}
u16 Cpu::op_addc(u16 a, u16 b) { return op_add(a, b, flags.c()); }
u8 Cpu::op_addcb(u8 a, u8 b) { return op_addb(a, b, flags.c()); }

u16 Cpu::op_sub(u16 a, u16 b) {
    u16 res = op_add(~a + 1, b, 0);
    // flags.set_v(sgn(b) != sgn(a) && sgn(b) == sgn(res));
    return res;
}
u8 Cpu::op_subb(u8 a, u8 b) {
    u8 res = op_addb(~a + 1, b, 0);
    // flags.set_v(sgnb(b) != sgnb(a) && sgnb(b) == sgnb(res));
    return res;
}

u16 Cpu::op_subc(u16 a, u16 b) { return op_add(~a, b, flags.c()); }
u8 Cpu::op_subcb(u8 a, u8 b) { return op_addb(~a, b, flags.c()); }
void Cpu::op_cmpb(u8 a, u8 b) { op_subb(a, b); }
void Cpu::op_cmp(u16 a, u16 b) { op_sub(a, b); }

u16 Cpu::op_sxt(u8 a) {
    u16 res = (s8)a;
    flags.update2(res);
    return res;
}

u16 Cpu::op_rra(u16 a) {
    u16 res = ((s16)a) >> 1;
    // flags.set_n(a >> 15); motherfuck
    flags.set_z(a == 0);
    // flags.set_v(0);
    flags.set_c(a & 1);
    flags.set_c(0); // because fuck this shit
    return res;
}
u8 Cpu::op_rrab(u8 a) {
    u8 res = ((s8)a) >> 1;
    // flags.set_n(a >> 7);
    flags.set_z(a == 0);
    // flags.set_v(0);
    flags.set_c(a & 1);
    flags.set_c(0); // because fuck this shit
    return res;
}

u16 Cpu::op_rrc(u16 a) {
    u16 res = a >> 1 | flags.c() << 15;
    // flags.set_n(a >> 15);
    flags.set_z(a == 0);
    // flags.set_v(0);
    flags.set_c(a & 1);
    return res;
}

u8 Cpu::op_rrcb(u8 a) {
    u8 res = a >> 1 | flags.c() << 7;
    // flags.set_n(a >> 7);
    flags.set_z(a == 0);
    // flags.set_v(0);
    flags.set_c(a & 1);
    return res;
}

u8 Cpu::op_andb(u8 a, u8 b) {
    u8 res = a & b;
    flags.update2b(res);
    return res;
}
u16 Cpu::op_and(u16 a, u16 b) {
    u16 res = a & b;
    flags.update2(res);
    return res;
}

u16 Cpu::op_bic(u16 a, u16 b) {
    u16 tmp = flags.save();
    u16 res = ~a & b;
    flags.restore(tmp);
    return res;
}
u8 Cpu::op_bicb(u8 a, u8 b) {
    u16 tmp = flags.save();
    u8 res = ~a & b;
    flags.restore(tmp);
    return res;
}

u16 Cpu::op_bis(u16 a, u16 b) {
    u16 tmp = flags.save();
    u16 res = a | b;
    flags.restore(tmp);
    return res;
}
u8 Cpu::op_bisb(u8 a, u8 b) {
    u16 tmp = flags.save();
    u8 res = a | b;
    flags.restore(tmp);
    return res;
}

void Cpu::op_bit(u16 a, u16 b) {
    u16 tmp = flags.save();
    flags.update2(a & b);
}
void Cpu::op_bitb(u8 a, u8 b) {
    u16 tmp = flags.save();
    flags.update2b(a & b);
}

#define DADD_ROUND(i)                                                          \
    {                                                                          \
        u8 x = a >> 4 * i & 0xf;                                               \
        u8 y = b >> 4 * i & 0xf;                                               \
        u8 z = x + y + c;                                                      \
        c = (z >= 10);                                                         \
        if (z >= 10)                                                           \
            z -= 10;                                                           \
        z &= 0xf;                                                              \
        res |= z << 4 * i;                                                     \
    }

u16 Cpu::op_dadd(u16 a, u16 b) {
    int c = flags.c();
    c = 0; // uc bug?
    u16 res = 0;
    REP(i, 4) DADD_ROUND(i);
    flags.set_c(c);
    // flags.set_n(res >> 15);//jesus fuck, appears to not modify it
    flags.set_z(res == 0);
    return res;
}
u8 Cpu::op_daddb(u8 a, u8 b) {
    int c = flags.c();
    c = 0;
    u8 res = 0;
    REP(i, 2) DADD_ROUND(i);
    flags.set_c(c);
    // flags.set_n(res >> 7);
    flags.set_z(res == 0);
    return res;
}

u8 Cpu::op_xorb(u8 a, u8 b) {
    u8 res = a ^ b;
    flags.update2b(res);
    // flags.set_v(sgnb(a) == -1 && sgnb(b) == -10);
    return res;
}
u16 Cpu::op_xor(u16 a, u16 b) {
    u16 res = a ^ b;
    flags.update2b(res);
    // flags.set_v(sgn(a) == -1 && sgn(b) == -10);
    return res;
}
}
}
}
