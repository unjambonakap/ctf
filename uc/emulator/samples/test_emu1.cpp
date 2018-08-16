
#include <fstream>
#include <opa_common.h>
#include <opa/emu/msp430/emu.h>
#include <opa/utils/string.h>

using namespace std;
using namespace opa::emu::msp430;
using namespace opa::utils;

int main(int argc, char **argv) {
    srand(0);
    --argc, ++argv;

    int mode = atoi(argv[0]);
    --argc, ++argv;

    assert(argc > 0);
    ifstream file(argv[0]);
    --argc, ++argv;

    file.seekg(0, ios::end);
    int size = file.tellg();
    file.seekg(0, ios::beg);
    string buf(size + 1, 0);
    file.read((char *)buf.c_str(), size);
    file.close();

    std::string s;
    if (argc > 0) {
        s = argv[0];
        --argc, ++argv;
        fprintf(stderr, "FUU %s\n", s.c_str());
        s = h2b(s);
    } else {
        REP(i, 1) s += "a";
    }

    string trace;
    if (argc > 0) {
        trace = argv[0];
        --argc, ++argv;
    }

    EmuMsp430 emu(trace);
    emu.load(buf);
    std::string cur_out;

    if (mode == 0) {

        while (true) {
            emu.run();
            assert(emu.get_status() == EmuMsp430::Status_Interrupted);
            if (emu.intType == Int_Putc)
                cur_out += emu.get_stdout();

            if (cur_out == "What's the passwor") {
                ofstream of("dump1.core");
                string tmp = emu.serialize();
                of.write(tmp.c_str(), tmp.size());
                of.close();
                break;
            }
        }

    } else {

        while (true) {
            emu.run();
            assert(emu.get_status() == EmuMsp430::Status_Interrupted);
            if (emu.intType == Int_Putc)
                cur_out += emu.get_stdout();
            else
                break;
        }

        printf(">> GOT >> %s\n", emu.get_stdout().c_str());
        emu.set_stdin(s);
        emu.run();
        printf(">> GOT >> %s\n", emu.get_stdout().c_str());
        printf("SOLVED> > %d\n", emu.is_solved());

        puts("DONE HERE");
    }

    return 0;
}
