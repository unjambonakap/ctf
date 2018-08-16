#ifndef _H_OPS_EMU_MSP430_OPERAND
#define _H_OPS_EMU_MSP430_OPERAND

#include <opa_common.h>
#include <opa/emu/msp430/cpu.h>

namespace opa {
namespace emu {
namespace msp430 {

class EmuMsp430;
class Ins;
enum OpType {
    Op_Constant,
    Op_Memory,
    Op_Reg,
    Op_RegOff,
    Op_RegPtr,
    Op_RegPtrInc,
    Op_Invalid,
};

class Operand {
  public:
    void init(EmuMsp430 *emu, Ins *ins);

    void build_const(u16 C) {
        type = Op_Constant;
        op.C = C;
    }
    void build_mem(u16 mem) {
        assert(0);
        type = Op_Memory;
        op.mem = mem;
    }

    void build_reg(RegEnum regid) {
        type = Op_Reg;
        op.regid = regid;
    }

    void build_regptr(RegEnum regid, u16 off) {
        type = Op_RegPtr;
        op.reg.regid = regid;
        op.reg.off = off;
    }

    void build_regoff(RegEnum regid, u16 off) {
        type = Op_RegOff;
        op.reg.regid = regid;
        op.reg.off = off;
    }

    void build_regptrinc(RegEnum regid) {
        type = Op_RegPtrInc;
        op.regid = regid;
    }

    void load(bool is_dest);
    void set_bytemode(bool bytemode) { this->bytemode = bytemode; }

    u16 get();
    void set(u16 val);

    std::string str();



    OpType type;
    EmuMsp430 *m_emu;
    Ins *m_ins;
    bool bytemode;
    bool is_dest;
    u16 src_val;

    union {
        u16 C;
        u16 mem;
        RegEnum regid;
        struct {
            RegEnum regid;
            u16 off;
        } reg;
    } op;
};
}
}
}
#endif
