#ifndef _H_OPS_EMU_MSP430_REG
#define _H_OPS_EMU_MSP430_REG

#include <opa_common.h>

namespace opa {
namespace emu {
namespace msp430 {

#define MSP430_REG(name, str) REG_NAME(name),
enum RegEnum {
#include <opa/emu/msp430/reg_vals.h>
    REG_ENUM_MAX
};


class Reg {
  public:
    u16 read(bool dbg = false);
    void write(u16 v, bool dbg = false);

    void init(RegEnum id, const std::string &desc);
    std::string str() const;

  private:
    std::string m_desc;
    u16 m_val;
    RegEnum m_id;
};
}
}
}
#endif
