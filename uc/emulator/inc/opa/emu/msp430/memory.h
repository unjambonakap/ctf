#ifndef _H_OPS_EMU_MSP430_MEMORY
#define _H_OPS_EMU_MSP430_MEMORY

#include <opa_common.h>

namespace opa {
namespace emu {
namespace msp430 {
const int MEM_SIZE = 0x10000;

class Memory {
  public:
    u16 read(u16 addr, bool dbg = false);
    u8 readb(u16 addr, bool dbg = false);
    void write(u16 addr, u16 val, bool dbg = false);
    void writeb(u16 addr, u8 val, bool dbg = false);
    Memory();

  private:
    u16 m_data[MEM_SIZE / 2];
};
}
}
}

#endif
