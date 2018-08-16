#include <opa_common.h>
#include <random>
#include <thread>

const int M = 52;
int cnt[M][M];

int main() {
    const u64 maxn = 1ll << 20;
    for (u64 i = 0; i < maxn; ++i) {
        std::mt19937 prng;
        prng.seed(i);
        vi tb;
        REP(j, M) {
            int v = prng() % (M - j);
            ++cnt[j][v];
            tb.pb(v);
        }
    }
    REP(i,M) out(cnt[i],M);

    return 0;
}
