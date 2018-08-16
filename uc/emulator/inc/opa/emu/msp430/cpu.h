#ifndef _H_OPS_EMU_MSP430_CPU
#define _H_OPS_EMU_MSP430_CPU

#include <opa_common.h>
#include <opa/emu/msp430/reg.h>

namespace opa {
namespace emu {
namespace msp430 {

enum SR_Flags {
    FLAG_C = 1 << 0,
    FLAG_Z = 1 << 1,
    FLAG_N = 1 << 2,
    FLAG_V = 1 << 8,
    FLAG_CPUOFF = 1 << 4,
    FLAG_ALL = FLAG_C | FLAG_Z | FLAG_N | FLAG_V | FLAG_CPUOFF,
};

enum Interrupt {
    Interrupt_Input,
    Interrupt_Unlock,
    Interrupt_Else,
};

class FlagHandler {
  public:
    FlagHandler() { m_sr = 0; }

    bool c() { return has_flag(FLAG_C); }
    bool n() { return has_flag(FLAG_N); }
    bool v() { return has_flag(FLAG_V); }
    bool z() { return has_flag(FLAG_Z); }

    void set_flag(SR_Flags flag, bool v);
    void set_c(bool v) { set_flag(FLAG_C, v); }
    void set_n(bool v) { set_flag(FLAG_N, v); }
    void set_v(bool v) { set_flag(FLAG_V, v); }
    void set_z(bool v) { set_flag(FLAG_Z, v); }

    bool has_flag(SR_Flags flag);
    void update(u32 res);
    void updateb(u16 res);
    void update2(u16 res);
    void update2b(u8 res);

    void init(Reg *sr) { m_sr = sr; }
    std::string dump();

    u16 save();
    void restore(u16 v);

  private:
    Reg *m_sr;
};

class Cpu {
  public:
    void init();
    std::string dump_cpu();
    std::string oneliner_dump();
    FlagHandler flags;

    u16 op_add(u16 a, u16 b, bool c = 0);
    u8 op_addb(u8 a, u8 b, bool c = 0);

    u16 op_addc(u16 a, u16 b);
    u8 op_addcb(u8 a, u8 b);

    u16 op_sub(u16 a, u16 b);
    u8 op_subb(u8 a, u8 b);

    u16 op_subc(u16 a, u16 b);
    u8 op_subcb(u8 a, u8 b);
    void op_cmpb(u8 a, u8 b);
    void op_cmp(u16 a, u16 b);

    u16 op_sxt(u8 a);
    u16 op_rra(u16 a);
    u8 op_rrab(u8 a);

    u16 op_rrc(u16 a);
    u8 op_rrcb(u8 a);
    u8 op_andb(u8 a, u8 b);
    u16 op_and(u16 a, u16 b);
    u8 op_xorb(u8 a, u8 b);
    u16 op_xor(u16 a, u16 b);

    u16 op_bis(u16 a, u16 b);
    u8 op_bisb(u8 a, u8 b);
    u16 op_bic(u16 a, u16 b);
    u8 op_bicb(u8 a, u8 b);
    void op_bit(u16 a, u16 b);
    void op_bitb(u8 a, u8 b);

    u16 op_dadd(u16 a, u16 b);
    u8 op_daddb(u8 a, u8 b);

    Reg &reg(RegEnum v) { return m_regs[v]; }
    Reg &reg(int v) { return m_regs[(RegEnum)v]; }
#define MSP430_REG(name, str)                                                  \
    u16 get_##str(bool debug = false) {                                        \
        return m_regs[REG_NAME(name)].read(debug);                             \
    }                                                                          \
    u16 set_##str(u16 v, bool debug = false) {                                 \
        m_regs[REG_NAME(name)].write(v, debug);                                \
    }                                                                          \
    Reg &reg_##str() { return m_regs[REG_NAME(name)]; }

#include <opa/emu/msp430/reg_vals.h>
#undef MSP430_REG

  private:
    Reg m_regs[REG_ENUM_MAX];
};
}
}
}
#endif
