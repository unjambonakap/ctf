#include <opa_common.h>
#include <random>
#include <opa/utils/string.h>

u32 do_round(const u16 *tb, int n) {
    u16 a = 0;
    u16 b = 0;

    REP(i, n) {
        a += tb[i];
        b ^= tb[i];
        u16 c = b;
        b = a >> 8 | a << 8;
        a = c;
    }
    return (u32)a << 16 | b;
    //ae8da34764af
}

int main() {
    u32 sol = 0xfeb19298;
    std::mt19937 prng;

    int n = 3;
    u16 tb[n];
    u64 cnt=0;
    while (1) {
        ++cnt;
        if (cnt%int(1e8)==0) printf("on %Lu\n", cnt);
        REP(i, n) tb[i] = prng();
        u32 res = do_round(tb, n);
        if (res == sol) {
            printf(">> foudn solution %s\n",
                   opa::utils::b2h((const char *)tb).c_str());
        }
    }

    return 0;
}
