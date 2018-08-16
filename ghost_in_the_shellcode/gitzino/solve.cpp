#include <opa_common.h>
#include <unistd.h>
#include "gitzino.h"

#include <opa/crypto/hash.h>
#include <opa/utils/string.h>
#include <sys/mman.h>

__BEGIN_DECLS
void entry_initRand(u32 val);
u32 entry_genRand();
u32 entry_test1(void *ptr);
__END_DECLS

using namespace opa::utils;
using namespace opa::crypto;
using namespace std;

const int nentry = 0.6e9;
const int maxn = 3.81e8;
const int nc = 5;

int *data;

static inline void get_perm(u32 seed, u32 *tb) {
    entry_initRand(seed);
    REP(i, n) tb[i] = i;
    REPV(i, n) {
        u32 res = entry_genRand() % (i + 1);
        swap(tb[i], tb[res]);
    }
}
void build_db() {
    u32 tb[n];

    {
        map<u64, int> cnt;
        int nstep = 1e6;
        REP(i, nstep) {
            entry_initRand(-i);
            u64 v = 0;
            REP(j, 10) v = v << 6 | entry_genRand() % (52 - j);
            cnt[v] += 1;
        }
        int mx = 0;
        FE(it, cnt) mx = max(mx, it->ND);
        printf("max >> %d\n", mx);
        return;
    }

    REP(i, nentry) {
        if (i % int(1e6) == 0)
            printf("on %d\n", i);
        get_perm(i, tb);
        u32 key = get_perm_key(tb);
        data[key] = i;
    }
    return;

    FILE *f = fopen(db_file, "wb");
    fwrite(data, 4, maxn, f);
    fclose(f);
}

void load_db() {
    FILE *f = fopen(db_file, "rb");
    fread(data, 4, maxn, f);
    fclose(f);
}

void test_len() {

    u32 target = 0x8048e73;
    u32 page_size = sysconf(_SC_PAGESIZE);
    int res = mprotect((void *)(target & ~(page_size - 1)), page_size,
                       PROT_EXEC | PROT_WRITE);
    u8 *ptr = (u8 *)target;
    ptr[0] = 0xc3;
    FILE *f = fopen("/dev/urandom", "rb");
    char buf[0x110] = { 0 };

    int seen[257] = { 0 };
    puts("GOGO");
    REP(i, 100000) {
        fread(buf, 1, 0x100, f);
        // memset(buf, 'a', 0x100);
        memset(buf + 0xe6, 0, 0x1a);
        u32 x = entry_test1(buf);
        ++seen[x];
    }
    REP(i, 257) printf("%d >> %d\n", i, seen[i]);
    puts("END");
    // Pmax = Px(256) ~= 0.36
    fclose(f);
}

int eval_cost(vi cards) {
    set<int> colors;
    vi vals;
    REP(i, nc) colors.insert(cards[i] / 13);
    REP(i, nc) vals.pb(cards[i] % 13);
    sort(ALL(vals));

    map<int, int> cntvals;
    REP(i, vals.size()) cntvals[vals[i]] += 1;

    bool straight = true;
    REP(i, nc - 1) if (vals[i] + 1 != vals[i + 1]) {
        straight = false;
        break;
    }

    bool straight2 = true;
    FOR(i, 1, nc) if ((vals[i] + 1) % 13 != vals[(i + 1) % nc]) {
        straight2 = false;
        break;
    }
    straight = straight || straight2;

    vi repeat;
    FE(it, cntvals) if (it->ND > 1) repeat.pb(it->ND);
    sort(ALL(repeat));

    if (colors.size() == 1) {
        if (straight)
            return vals[nc - 1] == 12 ? 800 : 50;
        return 6;
    }

    if (repeat.size() && repeat[0] == 4)
        return 25;
    if (repeat.size() == 2 && repeat[0] == 2 && repeat[1] == 3)
        return 9;

    if (straight)
        return 4;
    if (repeat.size() && repeat[0] == 3)
        return 3;
    if (repeat.size() == 2)
        return 2;
    if (*--vals.end() >= 10)
        return 1;
    return 0;
}

void mode_queries() {

    char buf[128];
    u32 tb[n];
    load_db();
    fprintf(stderr, "Loaded db\n");

    while (1) {
        if (fgets(buf, 127, stdin) <= 0)
            break;

        u32 key;
        int pos = 0;
        u32 cards[5];
        REP(i, 5) {
            int tmp = 0;
            sscanf(buf + pos, "%d%n", cards + i, &tmp);
            pos += tmp;
        }
        key = get_perm_key(cards);

        fprintf(stderr, "get key >> %x >> data=%d\n", key, data[key]);
        REP(i, 5) fprintf(stderr, "%d ", cards[i]);
        fprintf(stderr, "\n");

        int seed = data[key];
        if (seed != -1) {
            get_perm(seed, tb);

            vi cards;
            REP(i, nc) cards.pb(key % n), key /= n;
            reverse(ALL(cards));
            REP(i, nc) fprintf(stderr, ">> %x", cards[i]);
            fprintf(stderr, "\n");
            REP(i, nc) fprintf(stderr, ">> %x", tb[i]);
            fprintf(stderr, "\n");

            pii best = MP(-2, 0);
            vi best_cards;
            REP(i, 1 << nc) {
                vi now = cards;
                REP(j, nc) if (i >> j & 1) now[j] = tb[nc + j];
                int cost = eval_cost(now);
                if (cost > best.first)
                    best = MP(cost, i), best_cards = now;
            }

            fprintf(stderr, "best cost >> %d\n", best.ST);
            printf("cost=%d,seed=%d", best.ST, seed);

            printf(",expected=");
            REP(i, nc) printf("%d,", best_cards[i]);

            printf("return=");
            REP(i, nc) if (best.ND >> i & 1) printf("%d,", i);
        }

        puts("END");

        fflush(stdout);
    }
}

INIT_FUNC_ATTR void go() {
    printf("GOGOOG KAPPA\n");

    int datalen = sizeof(data[0]) * maxn;
    data = (int *)malloc(datalen);
    assert(data != 0);
    memset(data, -1, datalen);

    int mode = 2;
    if (mode == 0)
        test_len();
    else if (mode == 1)
        build_db();
    else if (mode == 2)
        mode_queries();
    exit(0);
}
