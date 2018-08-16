#ifndef _H_OPA_EMU_MSP430_EMU
#define _H_OPA_EMU_MSP430_EMU

#include <opa_common.h>
#include <opa/emu/msp430/memory.h>
#include <opa/emu/msp430/insloader.h>
#include <opa/emu/msp430/cpu.h>

namespace opa {
namespace emu {
namespace msp430 {

#undef MSP430_REG

enum IntType {
    Int_Putc,
    Int_Gets,
};

class EmuMsp430 {
  public:
    enum Status {
        Status_Stopped,
        Status_Interrupted,
        Status_Off,
    };

    std::string peek(u16 addr, int len);
    u16 peek(u16 addr);
    void poke(u16 addr, u16 val);
    void poke(u16 addr, const u16 *data, int n);
    void poke(u16 addr, const std::string &data, int n = -1);
    u16 peek_reg(RegEnum reg);
    void poke_reg(RegEnum reg, u16 data);

    void step();
    void run();
    std::string small_dump();

    std::string serialize();
    void load(const std::string &snapshot);

    std::string get_stdout();
    void set_stdin(const std::string &a) { m_stdin += a; }

    Status get_status() { return m_status; }
    EmuMsp430(const std::string &trace);
    Memory memory;
    Cpu cpu;
    bool is_solved() { return m_solved; }
    void reset();

    IntType intType;

  private:
    int do_gets(u8 *dest, int n);
    bool do_putc(u8 c);
    void begin_ins_hook();
    bool do_step();
    void end_ins_hook();
    bool handle_interrupt();
    Ins m_ins;
    std::string m_stdout;
    std::string m_stdin;
    bool m_solved;
    FILE *m_trace;

    Status m_status;
};
}
}
}
#endif
