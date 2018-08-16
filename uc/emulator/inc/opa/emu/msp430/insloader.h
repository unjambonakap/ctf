#ifndef _H_OPS_EMU_MSP430_INS
#define _H_OPS_EMU_MSP430_INS

#include <opa_common.h>
#include <opa/emu/msp430/operand.h>
#include <opa/emu/msp430/cpu.h>
#include <opa/emu/msp430/memory.h>
#define INS_HANDLER_NAME(x) x##_handler

namespace opa {
namespace emu {
namespace msp430 {

class EmuMsp430;

class Ins {
  public:
#define INS_DECL(name, fmt, code, op1, op2) INS_ENUM_NAME(name),
    enum InsType {
#include <opa/emu/msp430/ins_vals.h>
        Ins_Invalid,
    };
#undef INS_DECL

    typedef void (Ins::*InsHandler)();

    enum InsFormat {
        Format_SingleOp,
        Format_DoubleOp,
        Format_Jump,
    };

    enum OpMode {
        OpMode_None = -1,
        OpMode_Dest,
        OpMode_Src,
    };

    struct InsDesc {
        InsFormat format;
        InsType type;
        InsHandler handler;
        std::string name;
        OpMode op_mode[2]; // src=0, dst=1
    };

    void init(EmuMsp430 *emu);
    void load();
    void execute();
    std::string dump();
    std::string oneliner_dump();
    u16 get_pc() { return m_orig_pc; }

    u16 get_next();
    std::string str();

  private:
    EmuMsp430 *m_emu;
    Cpu *cpu;
    Memory *memory;

    InsType m_type;
    Operand m_ops[2];
    int m_nops;
    bool m_bytemode;
    u16 m_len_op;

    u16 m_raw;
    u16 m_orig_pc;

    void do_jump();
    InsType get_ins_type(u16 w);
    void load_op(Operand &op, OpMode type, u8 mode, u8 code);

    void handle_ins_decl(InsType type, const std::string &name,
                         InsFormat format, u16 code, InsHandler handler,
                         OpMode op1, OpMode op2);

#define INS_DECL(name, format, format_code, op1, op2)                          \
    void INS_HANDLER_NAME(name)();
#include <opa/emu/msp430/ins_vals.h>
#undef INS_DECL

    std::map<u16, InsType> m_single_op_mapping;
    std::map<u16, InsType> m_double_op_mapping;
    std::map<u16, InsType> m_jmp_op_mapping;
    std::map<InsType, InsDesc> m_ins_mapping;
};
}
}
}

#endif
