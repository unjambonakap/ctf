#include <opa_common.h>
#include <opa/utils/string.h>

#include <opa/math/common/bignum.h>
#include <opa/math/common/Utils.h>

using namespace std;
using namespace opa::utils;
using namespace opa::math::common;

vector<u32> pl;
int target_size = 512;
int M = 2;
int test = 0;

bignum tb[2];
vector<u32> _factors[2];
vector<u32> used;

const int buflen = 2048;
char buf[buflen + 1];
vector<u32> active;
int POS;

bool isGenerator(const bignum &g, const bignum &N, const bignum &order,
                 const BGFactors &factors) {
    for (auto x : factors)
        if (g.powm(order / x.ST, N) == 1)
            return false;
    return true;
}

bool readBignum(bignum &x) {

    if (!fgets(buf, buflen - 1, stdin)) {
        fprintf(stderr, "no more stfuf to read\n");
        fflush(stderr);
        sleep(1);
        return false;
    }
        printf("PARSSING >> %s\n", buf);
    x = bignum(buf, 16);
    return true;
}

int go(int pos, bignum cur) {

    if (cur.get_size() > target_size) {
        if (testPrime(cur + 1)) {
            tb[POS] = cur;
            _factors[POS] = active;
            return 1;
        }
        return 0;
    }
    if (pos == pl.size())
        return 0;

    if (pl[pos] == 2 || !used[pos]) {
        used[pos] = 1;
        active.pb(pl[pos]);
        if (go(pos + 1, cur * pl[pos]))
            return 1;
        used[pos] = 0;
        active.pop_back();
    }
    return go(pos + 1, cur);
}

int main() {
    M = 2;
    // if (test) target_size=64;
    initMathCommon();
    bignum x = 1;
    u32 cur = 1e3;
    pl.pb(2);
    REP(i, 1e4) {
        cur = nextPrimeSmall(cur + 1);
        if (cur == 0)
            break;
        pl.pb(cur);
    }

    used = vector<u32>(pl.size() + 10, 0);
    REP(i, M) {
        active.clear();
        POS = i;
        cur = 1;
        assert(go(0, cur) > 0);
    }

    bignum p = tb[0] + 1;
    bignum q = tb[1] + 1;

    bignum N = p * q;
    bignum y("abcdef", 16);
    N.disp();

    if (!test) {
        assert(readBignum(N));
        fprintf(stderr, "JAMBON >> %s\n", N.getstr().c_str());
    }

    N.disp();
    bignum order = (p - 1) * (q - 1);

    map<u32, int> cnt;
    BGFactors factors = factor_large(order);
    bignum g;
    sort(ALL(factors));
    bignum N1 = N - 1;
    bignum ig;

    while (1) {
        bignum res = 0;
        if (!test) {
            assert(readBignum(y));
            assert(readBignum(g));

            assert(g<N);

        } else {
            y = N.rand();
            while (1) {
                g = N.rand();
                break;
                if (isGenerator(g, N, order, factors))
                    break;
            }
        }

        int pos = 0;
        ig = g.inv(N);
        if (ig < 0)
            goto fail;
        assert(ig * g % N == 1);

        for (auto x : factors) {
            if (0 && x.first == 2)
                continue;
            fprintf(stderr, "on %d/%d\n", pos++, factors.size());
            bignum px = order;
            bignum pxmul = 1;
            bignum curpx = 0;
            bignum cur = y;

            REP(j, x.ND) {
                assert(px % x.ST == 0);
                px = px / x.ST;
                bignum curmul = ig.faste(pxmul, N);
                bool fd = false;
                REP(k, x.ST.getu32()) {
                    if (cur.faste(px, N) == 1 && (x.ST != 2 || j + k)) {
                        fd = true;
                        break;
                    }
                    curpx += pxmul;
                    cur = cur * curmul % N;
                }
                if (!fd) {
                    puts("not found");
                    goto fail;
                }

                pxmul *= x.ST;
            }

            res += curpx * (px % pxmul).inv(pxmul) * px;
            res %= order;
        }

        {
            bignum check = g.faste(res, N);
            if (check != y)
                goto fail;
        }
        {
            printf("gcd >> ");
            res.gcd(order).disp();
            bignum eexp = res.inv(order);
            if (1 && eexp < 0)
                goto fail;
            assert(y.faste(eexp, N) == g);

            printf("E=");
            res.disp();
            printf("D=");
            eexp.disp();
            puts("SUCCESS");
        }
        goto end;

    fail:
        puts(">>FAILED");
    end:
        puts("EOF<<");
        fflush(stdout);
    }

    return 0;
}
