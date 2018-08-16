#include "msp430/reg.h"

namespace opa {
namespace emu {
namespace msp430 {

u16 Reg::read(bool dbg) {
    if (m_id == REG_CG)
        return 0;
    return m_val;
}

void Reg::write(u16 v, bool dbg) { m_val = v; }

void Reg::init(RegEnum id, const std::string &desc) {
    m_val = 0;
    m_id = id;
    m_desc = desc;
}

std::string Reg::str() const { return m_desc; }
}
}
}
