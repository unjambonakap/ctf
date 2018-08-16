#include <opa_common.h>
#include <opa/math/common/Utils.h>

using namespace std;
using namespace opa::math::common;

const int tb[] = {
    0x63, 0x7C, 0x77, 0x7B, 0xF2, 0x6B, 0x6F, 0xC5, 0x30, 0x01, 0x67, 0x2B,
    0xFE, 0xD7, 0xAB, 0x76, 0xCA, 0x82, 0xC9, 0x7D, 0xFA, 0x59, 0x47, 0xF0,
    0xAD, 0xD4, 0xA2, 0xAF, 0x9C, 0xA4, 0x72, 0xC0, 0xB7, 0xFD, 0x93, 0x26,
    0x36, 0x3F, 0xF7, 0xCC, 0x34, 0xA5, 0xE5, 0xF1, 0x71, 0xD8, 0x31, 0x15,
    0x04, 0xC7, 0x23, 0xC3, 0x18, 0x96, 0x05, 0x9A, 0x07, 0x12, 0x80, 0xE2,
    0xEB, 0x27, 0xB2, 0x75, 0x09, 0x83, 0x2C, 0x1A, 0x1B, 0x6E, 0x5A, 0xA0,
    0x52, 0x3B, 0xD6, 0xB3, 0x29, 0xE3, 0x2F, 0x84, 0x53, 0xD1, 0x00, 0xED,
    0x20, 0xFC, 0xB1, 0x5B, 0x6A, 0xCB, 0xBE, 0x39, 0x4A, 0x4C, 0x58, 0xCF,
    0xD0, 0xEF, 0xAA, 0xFB, 0x43, 0x4D, 0x33, 0x85, 0x45, 0xF9, 0x02, 0x7F,
    0x50, 0x3C, 0x9F, 0xA8, 0x51, 0xA3, 0x40, 0x8F, 0x92, 0x9D, 0x38, 0xF5,
    0xBC, 0xB6, 0xDA, 0x21, 0x10, 0xFF, 0xF3, 0xD2, 0xCD, 0x0C, 0x13, 0xEC,
    0x5F, 0x97, 0x44, 0x17, 0xC4, 0xA7, 0x7E, 0x3D, 0x64, 0x5D, 0x19, 0x73,
    0x60, 0x81, 0x4F, 0xDC, 0x22, 0x2A, 0x90, 0x88, 0x46, 0xEE, 0xB8, 0x14,
    0xDE, 0x5E, 0x0B, 0xDB, 0xE0, 0x32, 0x3A, 0x0A, 0x49, 0x06, 0x24, 0x5C,
    0xC2, 0xD3, 0xAC, 0x62, 0x91, 0x95, 0xE4, 0x79, 0xE7, 0xC8, 0x37, 0x6D,
    0x8D, 0xD5, 0x4E, 0xA9, 0x6C, 0x56, 0xF4, 0xEA, 0x65, 0x7A, 0xAE, 0x08,
    0xBA, 0x78, 0x25, 0x2E, 0x1C, 0xA6, 0xB4, 0xC6, 0xE8, 0xDD, 0x74, 0x1F,
    0x4B, 0xBD, 0x8B, 0x8A, 0x70, 0x3E, 0xB5, 0x66, 0x48, 0x03, 0xF6, 0x0E,
    0x61, 0x35, 0x57, 0xB9, 0x86, 0xC1, 0x1D, 0x9E, 0xE1, 0xF8, 0x98, 0x11,
    0x69, 0xD9, 0x8E, 0x94, 0x9B, 0x1E, 0x87, 0xE9, 0xCE, 0x55, 0x28, 0xDF,
    0x8C, 0xA1, 0x89, 0x0D, 0xBF, 0xE6, 0x42, 0x68, 0x41, 0x99, 0x2D, 0x0F,
    0xB0, 0x54, 0xBB, 0x16
};

const int stb[] = {
    0x52, 0x09, 0x6A, 0xD5, 0x30, 0x36, 0xA5, 0x38, 0xBF, 0x40, 0xA3, 0x9E,
    0x81, 0xF3, 0xD7, 0xFB, 0x7C, 0xE3, 0x39, 0x82, 0x9B, 0x2F, 0xFF, 0x87,
    0x34, 0x8E, 0x43, 0x44, 0xC4, 0xDE, 0xE9, 0xCB, 0x54, 0x7B, 0x94, 0x32,
    0xA6, 0xC2, 0x23, 0x3D, 0xEE, 0x4C, 0x95, 0x0B, 0x42, 0xFA, 0xC3, 0x4E,
    0x08, 0x2E, 0xA1, 0x66, 0x28, 0xD9, 0x24, 0xB2, 0x76, 0x5B, 0xA2, 0x49,
    0x6D, 0x8B, 0xD1, 0x25, 0x72, 0xF8, 0xF6, 0x64, 0x86, 0x68, 0x98, 0x16,
    0xD4, 0xA4, 0x5C, 0xCC, 0x5D, 0x65, 0xB6, 0x92, 0x6C, 0x70, 0x48, 0x50,
    0xFD, 0xED, 0xB9, 0xDA, 0x5E, 0x15, 0x46, 0x57, 0xA7, 0x8D, 0x9D, 0x84,
    0x90, 0xD8, 0xAB, 0x00, 0x8C, 0xBC, 0xD3, 0x0A, 0xF7, 0xE4, 0x58, 0x05,
    0xB8, 0xB3, 0x45, 0x06, 0xD0, 0x2C, 0x1E, 0x8F, 0xCA, 0x3F, 0x0F, 0x02,
    0xC1, 0xAF, 0xBD, 0x03, 0x01, 0x13, 0x8A, 0x6B, 0x3A, 0x91, 0x11, 0x41,
    0x4F, 0x67, 0xDC, 0xEA, 0x97, 0xF2, 0xCF, 0xCE, 0xF0, 0xB4, 0xE6, 0x73,
    0x96, 0xAC, 0x74, 0x22, 0xE7, 0xAD, 0x35, 0x85, 0xE2, 0xF9, 0x37, 0xE8,
    0x1C, 0x75, 0xDF, 0x6E, 0x47, 0xF1, 0x1A, 0x71, 0x1D, 0x29, 0xC5, 0x89,
    0x6F, 0xB7, 0x62, 0x0E, 0xAA, 0x18, 0xBE, 0x1B, 0xFC, 0x56, 0x3E, 0x4B,
    0xC6, 0xD2, 0x79, 0x20, 0x9A, 0xDB, 0xC0, 0xFE, 0x78, 0xCD, 0x5A, 0xF4,
    0x1F, 0xDD, 0xA8, 0x33, 0x88, 0x07, 0xC7, 0x31, 0xB1, 0x12, 0x10, 0x59,
    0x27, 0x80, 0xEC, 0x5F, 0x60, 0x51, 0x7F, 0xA9, 0x19, 0xB5, 0x4A, 0x0D,
    0x2D, 0xE5, 0x7A, 0x9F, 0x93, 0xC9, 0x9C, 0xEF, 0xA0, 0xE0, 0x3B, 0x4D,
    0xAE, 0x2A, 0xF5, 0xB0, 0xC8, 0xEB, 0xBB, 0x3C, 0x83, 0x53, 0x99, 0x61,
    0x17, 0x2B, 0x04, 0x7E, 0xBA, 0x77, 0xD6, 0x26, 0xE1, 0x69, 0x14, 0x63,
    0x55, 0x21, 0x0C, 0x7D
};

const int perm[] = { 51, 43, 42, 47, 19, 49, 10, 23, 18, 11, 1,  60, 24,
                     31, 40, 54, 12, 56, 38, 59, 52, 6,  50, 13, 53, 34,
                     27, 17, 2,  3,  29, 26, 21, 30, 62, 20, 45, 16, 39,
                     28, 48, 35, 15, 22, 63, 58, 32, 57, 25, 33, 14, 36,
                     44, 37, 0,  8,  41, 5,  7,  9,  55, 46, 4,  61 };

const int iperm[] = { 54, 10, 28, 29, 62, 57, 21, 58, 55, 59, 6,  9,  16,
                      23, 50, 42, 37, 27, 8,  4,  35, 32, 43, 7,  12, 48,
                      31, 26, 39, 30, 33, 13, 46, 49, 25, 41, 51, 53, 18,
                      38, 14, 56, 2,  1,  52, 36, 61, 3,  40, 5,  22, 0,
                      20, 24, 15, 60, 17, 47, 45, 19, 11, 63, 34, 44 };

const u64 MOD = 18446744073709551615ULL;
const OPA_BG BMOD = OPA_BG::fromu64(MOD);
const int NB = 64;
const int NB2 = 8;

union state {
    u64 a;
    u8 b[NB2];
};

state k1, k2, k3;

state do_perm(state s) {
    state res;
    res.a = 0;
    REP(i, NB) res.a |= (s.a >> i & 1) << perm[i];
    return res;
}

state do_iperm(state s) {
    state res;
    res.a = 0;
    REP(i, NB) res.a |= (s.a >> i & 1) << iperm[i];
    return res;
}

state do_sub(state s) {
    REP(i, NB2) s.b[i] = tb[s.b[i]];
    return s;
}

state do_isub(state s) {
    REP(i, NB2) s.b[i] = stb[s.b[i]];
    return s;
}

u64 do_add(u64 a, u64 b) {
    OPA_BG ba = OPA_BG::fromu64(a);
    OPA_BG bb = OPA_BG::fromu64(b);
    return ((ba + bb) % BMOD).getu64();
}

u64 do_sub(u64 a, u64 b) {
    OPA_BG ba = OPA_BG::fromu64(a);
    OPA_BG bb = OPA_BG::fromu64(b);
    return ((BMOD + ba - bb) % BMOD).getu64();
}

inline state do_round(const state &a, const state &key) {
    state res;
    res = a;
    REP(i, NB2) res.b[i] = res.b[i] ^ key.b[i];
    res = do_sub(res);
    res = do_perm(res);
    return res;
}

inline state do_iround(const state &a, const state &key) {
    state res;
    res = a;
    res = do_iperm(res);
    res = do_isub(res);
    REP(i, NB2) res.b[i] = res.b[i] ^ key.b[i];
    return res;
}

state encrypt(state s) {
    s = do_round(s, k1);
    s = do_round(s, k2);
    u64 tmp = s.a;
    s.a = do_add(s.a, k3.a);
    return s;
}

state decrypt(state s) {
    u64 tmp = s.a;
    s.a = do_sub(s.a, k3.a);
    s = do_iround(s, k2);
    s = do_iround(s, k1);
    return s;
}

inline u64 scalar_bitprod(u64 a, u64 b) { return count_bit(a & b) & 1; }
u32 sb_diff[256][256] = { 0 };

void test() {
    REP(bit, 8) {
        u32 tb[256] = { 0 };
        REP(m, 256) {
            u32 cnt = 0;
            REP(a, 256) REP(b, 256) REP(p, 2) {
                if (scalar_bitprod(a - b - p & 255, m) == ((a ^ b) >> bit & 1))
                    ++tb[m];
            }
        }
        REP(m, 256) tb[m] -= 256 * 256;
        int bestp = 0;
        REP(m, 256) if (tb[m] > tb[bestp]) bestp = m;
        printf("%d >> %d\n", bestp, tb[bestp]);
    }

    {
        priority_queue<pair<int, pii> > q;
        REP(din, 256) FOR(dout, 1, 256) {
            REP(in, 256) sb_diff[din][dout] +=
                ((tb[in] ^ tb[in ^ din]) & dout) == dout;
            sb_diff[din][dout] -= 128;
            q.push(MP(abs(sb_diff[din][dout]), MP(din, dout)));
        }

        int target = iperm[4] % 8;
        printf("target=%d\n", iperm[2]);
        REP(din, 8)
        printf("%02x >> %d\n", 1 << din, sb_diff[1 << din][1 << target]);
        REP(i, 0) {
            auto x = q.top();
            q.pop();
            cout << x << endl;
        }
        for (u32 x = 10; x; x = x - 1 & 10) {
            printf("HAVE %d\n", x);
        }
    }
}

state k1_res;
state k2_res;
state k3_res;
int has_k1[8] = { 0 };
int has_k2[8] = { 0 };
int has_k3[8] = { 0 };

void test2(int bit) {
    int nx = 1 << 11;
    int sub_bit = bit;
    int sb_bit = iperm[sub_bit];

    int r2_bit = -1;
    {
        int tmp = 1 << sb_bit % 8;
        REP(i, 8) if (!has_k1[iperm[i + (sb_bit & ~0x7)] / 8] &&
                      (r2_bit == -1 ||
                       fabs(sb_diff[1 << i][tmp]) >
                           fabs(sb_diff[1 << r2_bit][tmp]))) r2_bit = i;
        if (r2_bit == -1 || fabs(sb_diff[1 << r2_bit][tmp]) < 8)
            return;
    }
    int sgn = sb_diff[1 << r2_bit][1 << sb_bit % 8] < 0 ? -1 : 1;
    r2_bit += sb_bit & ~0x7;

    int entry_bit = iperm[r2_bit];
    u64 sub_mask = 0x3ull << (sub_bit - 1);
    u8 diff = 1 << (entry_bit % 8);
    int key = entry_bit / 8;
    int shift = 8 * key;
    printf("K1_%d>> %d\n", key, k1.b[key]);
    priority_queue<pii> tb;
    REP(k1_x, 256) {

        int cnt = -nx / 2;
        int cnt2 = -nx / 2;
        // k1.b[key] = k1_x;

        REP(_inx, nx) {
            u8 x1 = rng();
            u8 x2 = x1 ^ diff;

            state i1, i2;
            i1.a = rng64();
            i2.a = i1.a;
            i1.b[key] = stb[x1] ^ k1_x;
            i2.b[key] = stb[x2] ^ k1_x;

            state d1, d2;

            if (0) {
                u64 diff2 = 1ull << r2_bit;
                state s1 = i1;
                state s2 = i2;
                REP(i, NB2) s1.b[i] ^= k1.b[i];
                s1 = do_sub(s1);
                assert(s1.b[key] == x1);
                s1 = do_perm(s1);

                REP(i, NB2) s2.b[i] ^= k1.b[i];
                s2 = do_sub(s2);
                assert(s2.b[key] == x2);
                s2 = do_perm(s2);

                assert(((s1.a ^ s2.a) & diff2) == diff2);
            }
            d1 = encrypt(i1);
            d2 = encrypt(i2);

            u64 diff = do_sub(d1.a, d2.a);
            u8 res = scalar_bitprod(diff, sub_mask); // guess for x1^x2[1]
            cnt += res == 1;

            u64 tmp1 = do_sub(d1.a, k3.a) >> sub_bit & 1;
            u64 tmp2 = do_sub(d2.a, k3.a) >> sub_bit & 1;
            cnt2 += (tmp1 ^ tmp2) == res;
        }
        tb.push(MP(cnt * sgn, k1_x));
        // printf("%d>> %d %d\n", k1_x, cnt, cnt2);
    }

    auto best = tb.top();
    tb.pop();
    auto best2 = tb.top();
    tb.pop();

    printf("FOUND FOR  %d >> %d (score=%d, best2=%d\n", key, best.ND, best.ST,
           best2.ST);
    if (best.ST - best2.ST > 20) {
        k1_res.b[key] = best.ND;
        puts("Accepting");
        has_k1[key] = 1;
    } else
        puts("FAILED");
    puts("");
}

void solve2() {
    int nx = 1 << 10;
    FOR(target_bit, 1, 64) {
        priority_queue<pii> tb;

        u64 sub_mask = 0x3ull << (target_bit - 1);
        int sb_bit = iperm[target_bit];
        int key = sb_bit / 8;
        u8 diff = 1 << sb_bit % 8;
        if (has_k2[key])
            continue;
        printf("ON TARGET >> %d\n", target_bit);

        REP(k2_x, 256) {

            int cnt = 0;
            REP(_inx, nx) {
                u8 x1 = rng();
                u8 x2 = x1 ^ diff;

                state i1, i2;
                i1.a = rng64();
                i2.a = i1.a;
                i1.b[key] = stb[x1] ^ k2_x;
                i2.b[key] = stb[x2] ^ k2_x;

                i1 = do_iround(i1, k1_res);
                i2 = do_iround(i2, k1_res);

                state d1, d2;

                d1 = encrypt(i1); // call oracle
                d2 = encrypt(i2);

                u64 sub_diff = do_sub(d1.a, d2.a);
                u8 res = scalar_bitprod(sub_diff, sub_mask);
                cnt += res == 1;
            }
            tb.push(MP(cnt, k2_x));
        }

        auto best = tb.top();
        tb.pop();
        auto best2 = tb.top();
        tb.pop();

        printf("FOUND FOR  %d >> %d (ans=%d (score=%d, best2=%d\n", key,
               best.ND, k2.b[key], best.ST, best2.ST);
        if (best.ST - best2.ST > 20) {
            k2_res.b[key] = best.ND;
            puts("Accepting");
            has_k2[key] = 1;
        } else
            puts("FAILED");
        puts("");
    }
}

void solve3(){
    state test;
    test.a=rng64();

    state res=encrypt(test);//oracle

    test=do_round(test,k1_res);
    test=do_round(test,k2_res);

    k3_res.a=do_sub(res.a, test.a);
    cout<<hex<<k3_res.a<<endl;
    cout<<"SOL >>"<<k3.a<<endl;
    //working too
}

int main() {
    initMathCommon(0);
    k1.a = rng64();
    k2.a = rng64();
    k3.a = rng64();
    printf("K1 >> %016Lx\n", k1.a);
    printf("K2 >> %016Lx\n", k2.a);
    printf("K3 >> %016Lx\n", k3.a);

    test();
    if (0) {
        FOR(i, 1, 64)
        test2(i);
        // finding k1
        // k1 found successfully
    } else {
        k1_res = k1; // supposing it worked
    }

    if (0) {
        solve2(); // working
    } else {
        k2_res = k2;
    }

    solve3();
    return 0;
    REP(i, NB) {
        u64 mask = 0;
        REP(j, 10) {
            state test, res;
            test.a = rng64();
            state res_orig = encrypt(test);
            test.a ^= 1ull << i;
            res = encrypt(test);
            u64 diff = do_sub(res.a, res_orig.a);
            u64 diff2 = do_sub(res_orig.a, res.a);
            printf(">>DIFF = %Lx %Lx\n", diff, diff2);
            mask |= diff;

            test.a ^= 1ull << i;
        }
        printf(">>DIFF %d=%016Lx\n", i, mask);
    }

    return 0;
}
