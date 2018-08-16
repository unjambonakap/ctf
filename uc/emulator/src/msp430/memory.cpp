#include "msp430/memory.h"

#include <opa_common.h>

namespace opa {
namespace emu {
namespace msp430 {

Memory::Memory() { memset(m_data, 0, sizeof(m_data)); }

u16 Memory::read(u16 addr, bool dbg) {
    assert(dbg || addr % 2 == 0);
    return readb(addr, dbg) | readb(addr + 1, dbg) << 8;
}
u8 Memory::readb(u16 addr, bool dbg) { return ((u8 *)m_data)[addr]; }

void Memory::writeb(u16 addr, u8 val, bool dbg) { 
    if (addr>=0x43fe && addr<=0x4401){ printf("MODIF HERE, set @%x=%x\n", addr, val);}
    if ((addr&~1)==0xe952){ printf("WRITE HERE, set @%x=%x\n", addr, val);}
    ((u8 *)m_data)[addr] = val; 
}

void Memory::write(u16 addr, u16 val, bool dbg) {
    assert(dbg || addr % 2 == 0);
    writeb(addr, val, dbg);
    writeb(addr + 1, val >> 8, dbg);
}
}
}
}
