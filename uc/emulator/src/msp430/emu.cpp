#include "msp430/emu.h"
#include "msp430/ins.h"
#include <rapidjson/document.h>
#include <rapidjson/error/en.h>
#include <opa/utils/string.h>

#include <rapidjson/writer.h>
#include <rapidjson/stringbuffer.h>

using namespace std;

namespace opa {
namespace emu {
namespace msp430 {

const int INT_RAND = 0x20;
const int INT_PUTC = 0x00;
const int INT_GETC = 0x01;
const int INT_GETS = 0x02;
const int INT_OPEN = 0x7f;
const int INT_CHECK_AND_OPEN = 0x7e;
const int INT_CHECK_AND_FLAG = 0x7d;

class InsCuller {
  public:
    InsCuller(int n) { this->n = n; }

    bool add(u16 pc) {
        int has_skipped = 0;

        REP(i, seen.size()) {
            if (seen[i].ST == pc) {
                ++seen[i].ND;
                return false;
            }
            has_skipped |= seen[i].ND > 0;
        }

        if (has_skipped) {
            printf("=============skipped:");
            REP(i, seen.size()) if (seen[i].ND > 0)
                printf(" %04x: %d,", seen[i].ST, seen[i].ND);
            REP(i, seen.size()) seen[i].ND = 0;
            puts("");
            puts("");
        }

        if (seen.size() == n)
            seen.pop_front();
        seen.pb(MP(pc, 0));
        return true;
    }

    deque<pair<u16, int> > seen;
    int n;
};
InsCuller culler(10);

EmuMsp430::EmuMsp430(const string &trace) {
    cpu.init();

    // u16 res=cpu.op_dadd(0x61b3, 0xfc8e);
    // printf("%x %x\n", res, cpu.flags.save());
    // exit(1);
    m_trace = 0;
    if (trace.size())
        m_trace = fopen(trace.c_str(), "w");
    m_ins.init(this);
}

u16 EmuMsp430::peek(u16 addr) { return memory.read(addr, true); }

string EmuMsp430::peek(u16 addr, int len) {
    len = len + 1 & ~1;
    string res(len, 0);
    REP(i, len / 2) {
        u16 v = peek(addr + 2 * i);
        res[2 * i] = v & 0xff;
        res[2 * i + 1] = v >> 8;
    }
    return res;
}

void EmuMsp430::poke(u16 addr, u16 val) { memory.write(addr, val); }
void EmuMsp430::poke(u16 addr, const u16 *data, int n) {
    REP(i, n) {
        u16 v = data[i];
        poke(addr + 2 * i, v);
    }
}

void EmuMsp430::poke(u16 addr, const string &data, int n) {
    if (n == -1)
        n = data.size();
    assert(n % 2 == 0);
    poke(addr, (const u16 *)data.c_str(), n / 2);
}

u16 EmuMsp430::peek_reg(RegEnum reg) { return cpu.reg(reg).read(true); }

void EmuMsp430::poke_reg(RegEnum reg, u16 data) {
    cpu.reg(reg).write(data, true);
}

void EmuMsp430::step() { do_step(); }

int EmuMsp430::do_gets(u8 *dest, int n) {
    intType = Int_Gets;
    assert(n > 0);
    if (m_stdin.size() == 0)
        return 0;

    printf("INTERUPT GETS ASK FOR %d\n", n);
    n = min(n, (int)m_stdin.size());
    std::string nw;
    FOR(i, n, m_stdin.size())
    nw += m_stdin[i];
    printf(">>>GOT %d\n", m_stdin.size());
    memcpy(dest, m_stdin.c_str(), n);
    dest[n] = 0;
    m_stdin = nw;
    return n;
}

bool EmuMsp430::do_putc(u8 c) {
    intType = Int_Putc;
    if (m_stdout.size())
        return false;

    m_stdout += c;
    printf("DO PUTC >> %c\n", c);
    return true;
}

bool EmuMsp430::handle_interrupt() {
    printf("handling interrupt mofo\n");

    u16 int_num = cpu.get_sr() >> 8 ^ 0x80;
    u16 start_arg = cpu.get_sp() + 0x8;

    printf("recv int=%02x, arg=%04x\n", int_num, start_arg);
    switch (int_num) {
    case INT_CHECK_AND_OPEN:
        cpu.set_r15(0);
        break;
    case INT_CHECK_AND_FLAG: {
        u16 flag_addr = memory.read(start_arg + 4);
        memory.write(flag_addr, 0);
        break;
    }
    case INT_OPEN:
        m_status = Status_Off;
        m_solved = true;
        return false;
        break;
    case INT_RAND: {
        u16 v = rand();
        v = 0;
        printf("setting rand >> %02x\n", v);
        cpu.set_r15(v);
        break;
    }
    case INT_PUTC: {
        u8 c = memory.read(start_arg);
        if (!do_putc(c)) {
            m_status = Status_Interrupted;
            return false;
        }
        break;
    }
    case INT_GETC: {
        u8 res;
        if (!do_gets(&res, 1)) {
            m_status = Status_Interrupted;
            return false;
        }
        cpu.set_r15(res);
        break;
    }
    case INT_GETS: {
        int n;
        u16 addr, want;
        addr = memory.read(start_arg);
        want = memory.read(start_arg + 2);
        printf("INTERRUPT GETS, args=%04x, addr=%04x, want=%04x\n", start_arg,
               addr, want);

        u8 *buf = (u8 *)malloc(want + 1);
        n = do_gets(buf, want);
        if (!n) {
            m_status = Status_Interrupted;
            free(buf);
            return false;
        }
        REP(i, n + 1)
        memory.writeb(addr + i, buf[i]);
        printf("FUU GOT %d\n", n);
        free(buf);
        break;
    }

    default:
        OPA_ASSERT(0, "got unknown interrupt %02x\n", int_num);
    }
    return true;
}

void EmuMsp430::begin_ins_hook() {}

void EmuMsp430::end_ins_hook() {
    if (cpu.get_pc() == 0x10)
        m_status = Status_Interrupted;
}

bool EmuMsp430::do_step() {
    if (m_status == Status_Interrupted) {
        if (!handle_interrupt())
            return false;
        m_status = Status_Stopped;
    }
    if (m_status != Status_Stopped)
        return false;

    if (m_trace) {
        string dump = small_dump();
        fwrite(dump.c_str(), 1, dump.size(), m_trace);
        fflush(m_trace);
    }

    begin_ins_hook();

    if (m_status != Status_Stopped)
        return false;

    m_ins.load();
    m_ins.execute();

    if (m_ins.get_pc() == 0xe000) {
        string dump = cpu.oneliner_dump() + " " + m_ins.oneliner_dump();
        dump += " " + utils::b2h(peek(m_ins.get_pc(), 6));
        if (1 || culler.add(m_ins.get_pc()))
            printf("%s\n", dump.c_str());
    }

    if (m_trace) {
        string dump = m_ins.dump();
        dump += "\n";
        fwrite(dump.c_str(), 1, dump.size(), m_trace);
        fflush(m_trace);
    }

    end_ins_hook();

    if (cpu.get_sr() & FLAG_CPUOFF) {
        printf("Cpu turning off\n");
        m_status = Status_Off;
        return true;
    }
    // if (cpu.get_pc()==0x45e0)
    //    assert(0);
    return true;
}

void EmuMsp430::run() {
    while (true) {
        if (!do_step())
            return;
    }
}

void EmuMsp430::load(const string &snapshot) {
    rapidjson::Document d;

    d.Parse(snapshot.c_str());
    printf(">> %d %s\n", d.HasParseError(),
           rapidjson::GetParseError_En(d.GetParseError()));
    assert(!d.HasParseError());

    {
        rapidjson::Value &a = d["regs"];
        assert(a.IsArray());
        REP(i, a.Size()) {
            rapidjson::Value &b = a[i];
            assert(b.IsInt());
            poke_reg((RegEnum)i, b.GetInt());
        }
        assert(a.Size() == REG_ENUM_MAX);
    }

    if (d.HasMember("updatememory")) {
        rapidjson::Value &a = d["updatememory"];
        assert(a.IsString());
        string memdata = utils::h2b(a.GetString());

        int sz = 8;
        int n = memdata.size() / sizeof(u16);
        int stride = sz + 1;

        assert(n % stride == 0);

        const u16 *tb = (const u16 *)memdata.c_str();
        for (int i = 0; i < n; i += stride) {
            u16 addr = tb[i];
            addr = addr >> 8 | addr << 8;
            assert(addr % 2 == 0);
            poke(addr, tb + i + 1, sz);
        }
    }

    if (d.HasMember("wholememory")) {
        rapidjson::Value &a = d["wholememory"];
        assert(a.IsString());
        string memdata = utils::b64d(a.GetString());
        poke(0, memdata);
    }
    reset();
}

string EmuMsp430::serialize() {
    rapidjson::StringBuffer s;
    rapidjson::Writer<rapidjson::StringBuffer> w(s);
    w.StartObject();

    {
        w.String("regs");
        w.StartArray();
        REP(i, REG_ENUM_MAX)
        w.Uint(cpu.reg(i).read(true));
        w.EndArray();
    }

    {
        w.String("wholememory");
        string mem = peek(0, 1 << 16);
        mem = utils::b64e(mem);
        w.String(mem.c_str(), mem.size());
    }
    w.EndObject();
    return s.GetString();
}

std::string EmuMsp430::get_stdout() {
    string out = m_stdout;
    m_stdout.clear();
    return out;
}

void EmuMsp430::reset() {
    m_status = Status_Stopped;
    m_stdin.clear();
    m_stdout.clear();
    m_solved = false;
}

string EmuMsp430::small_dump() {
    string cpu_dump = cpu.dump_cpu();

    string atPc, atSp;
    for (int i = 0; i < 8; ++i)
        atPc += utils::dump_hex(peek(cpu.get_pc() + 2 * i)) + " ";

    for (int i = 0; i < 8; ++i)
        atSp += utils::dump_hex(peek(cpu.get_sp() + 2 * i)) + " ";

    string res =
        utils::stdsprintf("Cpu:\n%s\n@PC:%s\n@SP:%s\n", cpu_dump.c_str(),
                          atPc.c_str(), atSp.c_str());

    return res;
}
}
}
}
