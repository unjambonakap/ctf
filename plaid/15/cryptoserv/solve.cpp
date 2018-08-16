#include <opa_common.h>
#include <opa/utils/string.h>

using namespace std;
using namespace opa::utils;

const int nvm = 16;

u32 vm[nvm];

string skey = "ab8762794fef7f2d";
string soutput = "e26bc4786742a65584e430fc717f3842ad3d93729c5b832d12e5210a6faca"
                 "da4f1c21318909f2cc92ed326176b36afadfe3e755649692928f3d06b1ceb"
                 "0ffa09abf7502c373e04b39c5295238bb75c15a8891301bce7ca3a4589570"
                 "235ef451759de44203f06a6e40df2a87e55d6d2f8627153e169dd89a80f59"
                 "f9d766789f55d174aeb7bbffdec3f6c23a0efdd9452d68e9d4cd96090133a"
                 "820a8ee7eee0b6880a1a9af93756243cbb17d511308a03376d7ac0411f4b7"
                 "4bc8d0dd1bc963d80003413d19b6f1861aa2fcf82eaa18ebdd1053053e4ef"
                 "a5a6cbaf02e3f37deb46c";

string mkey1 = "230fc764";
string mkey2 = "5e1c7e02";
string mkey3 = "cae25e28";
string mkey4 = "9f425d29";
string smkey = mkey1 + mkey2 + mkey3 + mkey4;

const u32 *s_key;
const u32 *s_mkey;
const u32 *s_expected;
const u32 e = 0x9e3779b9;

void check(u32 p0, u32 p1, u32 r0, u32 r1) {
    u32 d = 0;
    u32 v0 = s_key[0];
    u32 v1 = s_key[1];
    v0 ^= p0;
    v1 ^= p1;

    REP(i, 0x40) {
        u32 v2, v3, va;
        v2 = v1 << 4;
        v3 = v1 >> 5;
        v2 ^= v3;
        v2 += v1;
        va = s_mkey[d & 0x3] + d;
        v2 ^= va;
        v0 += v2;
        d += e;
        v2 = v0 << 4;
        v3 = v0 >> 5;
        v2 ^= v3;
        v2 += v0;
        va = s_mkey[d >> 0xb & 0x3] + d;
        v2 ^= va;
        v1 += v2;
    }
    assert(v0 == r0);
    assert(v1 == r1);
}

void go(u32 v0, u32 v1) {
    u32 orig_v0 = v0;
    u32 orig_v1 = v1;

    u32 d = 0;
    vector<u32> dval;
    int nr = 0x40;
    REP(i, nr + 1) {
        dval.pb(d);
        d += e;
    }

    REPV(i, nr) {
        u32 va, vd, v2, v3;
        v2 = v0 << 4;
        v3 = v0 >> 5;
        v2 ^= v3;
        v2 += v0;

        vd = dval[i + 1];
        va = s_mkey[vd >> 0xb & 0x3] + vd;
        v2 ^= va;
        v1 -= v2;
        // first part

        v2 = v1 << 4;
        v3 = v1 >> 5;
        v2 ^= v3;
        v2 += v1;

        vd = dval[i];
        va = s_mkey[vd & 0x3] + vd;
        v2 ^= va;
        v0 -= v2;
    }
    v0 ^= s_key[0];
    v1 ^= s_key[1];

    u32 buf[3];
    buf[0] = v0;
    buf[1] = v1;
    buf[2] = 0;
    // printf(">> %s\n", (char*)buf);
    u8 *tmp = (u8 *)buf;
    printf("%s", tmp);
    check(v0,v1,orig_v0, orig_v1);
}

int main() {

    string output = opa::utils::h2b(soutput);
    string mkey = opa::utils::h2b(smkey);
    string key = opa::utils::h2b(skey);
    int nr = output.size() / 8;

    const u32 *pkey = (const u32 *)key.c_str();
    const u32 *pmkey = (const u32 *)mkey.c_str();
    const u32 *poutput = (const u32 *)output.c_str();

    REP(i, nr) {
        s_key = pkey;
        s_mkey = pmkey;
        s_expected = poutput + i * 2;
        go(s_expected[0], s_expected[1]);
        pkey = poutput + i * 2;
    }
    return 0;
}
