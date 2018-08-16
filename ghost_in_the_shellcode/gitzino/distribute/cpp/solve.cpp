#include <opa_common.h>
#include <mutex>
#include <opa/math/common/Utils.h>
#include <opa/utils/string.h>
#include <unordered_map>

using namespace std;
using namespace opa::utils;
using namespace opa::math::common;

const int npass = 4;
const int nthreads = 4;
const u64 max_seed = 1ll << 32;
const u32 key_chunk_size = 1 << 10;
const int ncards = 52;
const int nhand = 5;
const u32 chunk_size = 1 << 15;
const int max_handforcost = 1 << 30;
const int max_key = int(381e6 + chunk_size * npass) &
                    ~(chunk_size * npass - 1); // include additional chunk_size
const int buffer_size = chunk_size * 1024;     // multiple requried
const std::string file_format = "data/chunk_%08u.out";
const char *cost_filename = "data/cost";

const int tot_chunks = max_key / chunk_size;

const int chunks_per_pass = tot_chunks / npass; // exact div required

vi default_perm;

u32 LOW_KEY;
u32 HIGH_KEY;

u32 RETURN_MASK[1 << nhand];
u32 IRETURN_MASK[1 << nhand];

enum class CostEnum : u8 {
    Nothing,
    Jacks,
    TwoPairs,
    Three,
    Straight,
    Flush,
    House,
    Four,
    StraightFlush,
    RoyalFlush,
};
int costMap[256];

void initMasks() {
    int tmp = 6;
    u32 elemMask = (1 << tmp) - 1;
    REP(k, 1 << nhand) {
        u32 cur = 0;
        REP(j, nhand) if (k >> j & 1) cur |= elemMask << (j * tmp);
        RETURN_MASK[k] = cur;
        IRETURN_MASK[k] = (1 << tmp * nhand) - 1 ^ cur;
    }
}

std::string getChunkFilename(int chunkid) {
    return stdsprintf(file_format.c_str(), chunkid);
}

struct Elem {
    u32 low;
    u32 high;
    Elem() {}
    Elem(u32 low, u32 high) {
        this->low = low;
        this->high = high;
    }
    bool operator<(const Elem &e) const { return low < e.low; }
};

bool isCurrentPass(const Elem &e) {
    return e.low >= LOW_KEY && e.low < HIGH_KEY;
}

int getChunkId(const Elem &e) { return (e.low - LOW_KEY) / chunk_size; }

u32 getHandWithIperm(const u32 *tb, const u32 *iperm) {
    u32 res = 0;
    REP(i, nhand) res = res * ncards + iperm[tb[i]];
    return res;
}

u32 getHand(const u32 *tb) {
    u32 res = 0;
    REP(i, nhand) res = res * ncards + tb[i];
    return res;
}

void extractHand(u32 hand, u32 *tb) {
    REPV(i, nhand) tb[i] = hand % ncards, hand /= ncards;
}

void extractHandForCost(u32 hand, u32 *tb) {
    REPV(i, nhand) tb[i] = hand & 0x3f, hand >>= 6;
}

u32 getHandForCost(u32 *tb) {
    u32 res = 0;
    REP(i, nhand) res = res << 6 | tb[i];
    return res;
}

u32 getHandForCost(u32 hand, const u32 *perm) {
    u32 tb[nhand];
    extractHand(hand, tb);
    REP(i, nhand) tb[i] = perm[tb[i]];
    return getHandForCost(tb);
}

u32 getHandForCost(u32 hand) {
    u32 tb[nhand];
    extractHand(hand, tb);
    return getHandForCost(tb);
}

u32 getNewHand(u32 low, u32 high, int mod) {
    return (low & IRETURN_MASK[mod]) | (high & RETURN_MASK[mod]);
}

CostEnum getCostNoCache(u32 handForCost) {
    u32 tb[nhand];
    extractHandForCost(handForCost, tb);

    set<int> colors;
    vi vals;
    vi repeats;
    REP(i, nhand) colors.insert(tb[i] / 13);
    REP(i, nhand) vals.pb(tb[i] % 13);
    sort(ALL(vals));

    map<int, int> cntvals;
    REP(i, vals.size()) cntvals[vals[i]] += 1;

    bool straight = true;
    REP(i, ncards - 1) if (vals[i] + 1 != vals[i + 1]) {
        straight = false;
        break;
    }

    bool straight2 = true;
    FOR(i, 1, ncards) if ((vals[i] + 1) % 13 != vals[(i + 1) % ncards]) {
        straight2 = false;
        break;
    }
    straight = straight || straight2;

    vi repeat;
    s32 has = -1;
    FE(it, cntvals) if (it->ND > 1) repeat.pb(it->ND), has = it->ST;
    sort(ALL(repeat));

    if (colors.size() == 1) {
        if (straight)
            return vals[0] == 0 && vals[ncards - 1] == 12
                       ? CostEnum::RoyalFlush
                       : CostEnum::StraightFlush;
        return CostEnum::Flush;
    }

    if (repeat.size() && repeat[0] == 4)
        return CostEnum::Four;
    if (repeat.size() == 2 && repeat[0] == 2 && repeat[1] == 3)
        return CostEnum::House;

    if (straight)
        return CostEnum::Straight;
    if (repeat.size() && repeat[0] == 3)
        return CostEnum::Three;
    if (repeat.size() == 2)
        return CostEnum::TwoPairs;
    if (repeats.size() == 1 && (has == 0 || has >= 10))
        return CostEnum::Jacks;
    return CostEnum::Nothing;
}

void getPerm(mt19937 &rng, u32 *tb) {
    REP(i, ncards) tb[i] = i;
    REPV(i, ncards) {
        int x = (u32)rng() % (i + 1);
        swap(tb[i], tb[x]);
    }
}

struct Queue {
    void add(u32 v) { q.push(v); }

    bool get(u32 &res) {
        bool ret = false;
        lock.lock();
        if (q.size())
            ret = true, res = q.front(), q.pop();
        lock.unlock();
        return ret;
    }

    mutex lock;
    queue<int> q;
};

struct GlobalData;
struct Chunk {
    vector<Elem> raw_data;
    u32 *data;
    u32 *pos;
    u32 datapos;
    u32 chunk_base;
    Chunk() {
        data = 0;
        pos = 0;
    }

    void init(u32 base) {
        chunk_base = base;
        free(data);
        free(pos);
        data = 0;
        pos = 0;
    }
    int getn() { return pos[chunk_size]; }

    void transform() {
        sort(ALL(raw_data));
        int n = raw_data.size();
        data = (u32 *)malloc(sizeof(u32) * n);
        pos = (u32 *)malloc(sizeof(u32) * (chunk_size + 1));
        assert(data);
        assert(pos);
        datapos = 0;

        u32 last = chunk_base;
        for (int i = 0; i < n;) {
            FOR(j, last, raw_data[i].low + 1) pos[j - chunk_base] = datapos;
            last = raw_data[i].low + 1;

            int j = i;
            for (j = i; j < n && raw_data[i].low == raw_data[j].low; ++j)
                data[datapos++] = raw_data[j].high;
            i = j;
        }
        FOR(j, last, chunk_base + chunk_size + 1) pos[j - chunk_base] = datapos;
        raw_data.resize(0);
    }

    void dump(FILE *f) {
        fwrite(pos, 4, chunk_size + 1, f);
        fwrite(data, 4, pos[chunk_size], f);
    }

    void load(FILE *f) {
        pos = (u32 *)malloc(sizeof(u32) * (chunk_size + 1));
        fread(pos, 4, chunk_size + 1, f);
        int n = pos[chunk_size];

        data = (u32 *)malloc(sizeof(u32) * n);
        fread(data, 4, n, f);
    }

    void load() {
        std::string filename = getChunkFilename(chunk_base / chunk_size);
        FILE *f = fopen(filename.c_str(), "rb");
        load(f);
        fclose(f);
    }
    void unload() { init(0); }

    s64 getBestCost(const u32 *perm, GlobalData &data);
    pii getBestActionForHand(u32 hand, const u32 *perm, GlobalData &data);
};

class PermEval {
  public:
    u32 perm[ncards];
    mt19937 rng;

    pii cur_swap;
    s64 cur_cost;

    pii best_swap;
    s64 best_cost;
    mutex m_mutex;

    void init(mt19937 &rng) {
        this->rng = rng;
        REP(i, ncards) perm[i] = i;
        getPerm(rng, perm);
        best_swap = MP(0, 0);
        best_cost = INT_MIN; // dont want to compute first cost
        select_next();
    }

    void do_swap() { swap(perm[cur_swap.ST], perm[cur_swap.ND]); }

    void select_next() {
        printf("last cos %Ld, pemr=", cur_cost);
        out(perm, ncards);
        do_swap(); // reverse swap
        cur_swap = best_swap;
        do_swap(); // apply best swap
        printf("bset cost >>> %Ld\n", best_cost);
        out(perm, ncards);
        puts("=============");

        best_swap = MP(0, 0);
    }

    void gen_next() {
        printf("got new cost %Ld for perm: ", cur_cost);
        out(perm, ncards);
        do_swap(); // reverse
        if (cur_cost >= best_cost)
            best_cost = cur_cost, best_swap = cur_swap;

        cur_cost = 0;
        cur_swap.ST = rng() % ncards;
        cur_swap.ND = rng() % (ncards - 1);
        cur_swap.ND += cur_swap.ND >= cur_swap.ST;
        do_swap(); // apply
    }

    void updateCost(s64 add) {
        lock_guard<mutex> lk(m_mutex);
        cur_cost += add;
    }
};

struct GlobalData {
    GlobalData() {
        perms = 0;
        tmpCost = 0;
    }

    void init(int size) { chunks.resize(size); }

    void rebase(u32 base) {
        REP(i, chunks.size()) chunks[i].init(i * chunk_size + base);
    }

    void pushData(Elem *tb, int n) {

        lock.lock();
        REP(i, n) {
            if (!isCurrentPass(tb[i]))
                continue;
            int id = getChunkId(tb[i]);
            assert(id < chunks.size());
            chunks[id].raw_data.pb(tb[i]);
        }
        lock.unlock();
    }

    void pushCosts(const vector<pair<u32, CostEnum> > &tb) {
        costLock.lock();
        if (tmpCost == 0) {
            tmpCost = (u8 *)malloc(max_handforcost);
            memset(tmpCost, -1, max_handforcost);
        }
        REP(i, tb.size()) {
            assert(tb[i].ST < max_handforcost);
            assert(tmpCost[tb[i].ST] == 0xff);
            tmpCost[tb[i].ST] = (u8)tb[i].ND;
        }
        costLock.unlock();
    }

    void addGain(s64 gain) {
        lock.lock();
        totGain += gain;
        lock.unlock();
    }

    void dumpCost(FILE *f) {
        u32 batch_size = 1 << 25;
        u32 sz = max_handforcost;
        for (int i = 0; i < sz; i += batch_size) {
            int need = min(sz - i, batch_size);
            int written = fwrite(tmpCost + i, sizeof(tmpCost[0]), need, f);
            assert(written == need);
        }
    }

    void loadCost(FILE *f) {
        int sz = max_handforcost;

        tmpCost = (u8 *)malloc(max_handforcost);
        fprintf(stderr, "load %d\n", sz);

        int batch_size = 1 << 20;
        int info_period = sz / batch_size / 100;
        for (int i = 0; i < (sz + batch_size - 1) / batch_size; ++i) {
            if (i % info_period == 0)
                fprintf(stderr, "loadCost %d %%\n", i / info_period);
            int nx = min(batch_size, sz - i * batch_size);
            int read =
                fread(tmpCost + i * batch_size, sizeof(tmpCost[0]), nx, f);
            assert(read == nx);
        }
    }

    int getHandCost(u32 hand) { return costMap[tmpCost[hand]]; }

    u32 getBestAction(u32 hand, const u32 *perm) {
        int chunkid = hand / chunk_size;
        Chunk &chunk = chunks[hand / chunk_size];
        chunk.init(chunkid * chunk_size);
        chunk.load();

        pii res = chunk.getBestActionForHand(hand, perm, *this);
        chunk.unload();
        return res.ND;
    }

    void addn(u64 n) {
        lock_guard<mutex> lk(lock);
        totelem += n;
    }

    mutex costLock;
    int ncost;
    u8 *tmpCost;
    u64 totelem;

    s64 totGain;
    Queue q;
    mutex lock;
    vector<Chunk> chunks;
    vi activePerm;

    vector<PermEval> *perms;
    u32 low_range;
    u32 high_range;
};

pii Chunk::getBestActionForHand(u32 hand, const u32 *perm,
                                GlobalData &globalData) {
    u32 id = hand - chunk_base;
    assert(id < chunk_size);

    u32 lowHand;
    vector<u32> highHands;
    lowHand = getHandForCost(hand, perm);

    FOR(j, pos[id], pos[id + 1]) highHands.pb(getHandForCost(data[j], perm));

    pii curBest = MP(INT_MIN, 0);
    REP(k, 1 << nhand) {
        int curCost = 0;
        REP(j, highHands.size()) {
            u32 newHand = getNewHand(lowHand, highHands[j], k);
            // assert(getCostNoCache(newHand) ==
            // globalData.getHandCost(newHand));
            curCost += globalData.getHandCost(newHand) - 1;
        }
        curBest = max(curBest, MP(curCost, k));
    }
    return curBest;
}

s64 Chunk::getBestCost(const u32 *perm, GlobalData &globalData) {
    s64 totCost = 0;

    REP(i, chunk_size) {
        pii res = getBestActionForHand(chunk_base + i, perm, globalData);
        totCost += res.ST;
    }
    return totCost;
}

struct Worker {
    Worker() { buffer = new Elem[buffer_size]; }
    void init(GlobalData &data) { this->data = &data; }

    void set_perm(u32 seed, Elem *dest) {
        rng.seed(seed);
        getPerm(rng, tb);
        dest->low = getHand(tb);
        dest->high = getHand(tb + nhand);
    }

    void stage1() {
        u32 seed;
        int nstep = max_seed / key_chunk_size;
        cursize = 0;

        while (data->q.get(seed)) {
            if (cursize == buffer_size)
                data->pushData(buffer, cursize), cursize = 0;
            int want = 100;
            int info_period = nstep / want;
            int curstep = seed / key_chunk_size;
            if (curstep % info_period == 0)
                printf("stage1 %d %% %d\n", curstep / info_period, want);

            REP(i, key_chunk_size) set_perm(seed + (u32)i, buffer + cursize++);
        }

        data->pushData(buffer, cursize), cursize = 0;
    }

    void stage2() {
        u32 chunkid;
        while (data->q.get(chunkid)) {
            int info_period = chunks_per_pass / 100;

            int passChunkId = chunkid % chunks_per_pass;
            if (passChunkId % info_period == 0)
                printf("stage2 %d %%\n", passChunkId / info_period);

            Chunk &chunk = data->chunks[passChunkId];
            std::string filename = getChunkFilename(chunkid);
            chunk.transform();
            FILE *f = fopen(filename.c_str(), "wb");
            chunk.dump(f);
            fclose(f);
        }
    }

    void load_query() {
        u64 count = 0;
        u32 chunkid;
        u32 tot_len = data->high_range - data->low_range;
        int info_period = tot_len / 100;

        while (data->q.get(chunkid)) {
            u32 cur_pos = chunkid - data->low_range;
            if (cur_pos % info_period == 0)
                printf("load_query %d %%\n", cur_pos / info_period);

            Chunk &chunk = data->chunks[chunkid];
            chunk.init(chunkid * chunk_size);
            chunk.load();
            count += chunk.getn();
        }
        data->addn(count);
    }

    void unload_query() {
        u32 chunkid;
        u32 tot_len = data->high_range - data->low_range;
        int info_period = tot_len / 100;

        while (data->q.get(chunkid)) {
            u32 cur_pos = chunkid - data->low_range;
            if (cur_pos % info_period == 0)
                printf("unload_query %d %%\n", cur_pos / info_period);

            Chunk &chunk = data->chunks[chunkid];
            chunk.unload();
        }
    }

    void eval_cost() {
        u32 chunkid;
        u32 tot_len = data->high_range - data->low_range;
        int info_period = tot_len / 100;
        u64 cnt = 0;
        while (data->q.get(chunkid)) {
            u32 cur_pos = chunkid - data->low_range;
            if (cur_pos % info_period == 0)
                printf("eval_cost %d %%\n", cur_pos / info_period);

            Chunk &chunk = data->chunks[chunkid];
            cnt += chunk.pos[chunk_size];

            REP(j, data->perms->size()) {
                PermEval &cur = (*data->perms)[j];
                s64 gain = chunk.getBestCost(cur.perm, *data);
                cur.updateCost(gain);
            }
        }
        data->addn(cnt);
    }

    void init_cost() {

        u32 hand;
        const int maxCostBufSize = 1000;
        vector<pair<u32, CostEnum> > costBuffer;
        costBuffer.reserve(maxCostBufSize);

        int info_period = max_key / 100;
        while (data->q.get(hand)) {
            if (costBuffer.size() == maxCostBufSize)
                data->pushCosts(costBuffer), costBuffer.clear();
            if (hand % info_period == 0)
                printf("initCost >> %d %%\n", hand / info_period);

            u32 tb[nhand];
            extractHand(hand, tb);
            sort(tb, tb + nhand);

            bool ok = true;
            REP(i, nhand - 1) if (tb[i] == tb[i + 1]) {
                ok = false;
                break;
            }

            if (!ok)
                continue;

            u32 handForCost = getHandForCost(hand);
            CostEnum cost = getCostNoCache(handForCost);
            costBuffer.pb(MP(handForCost, cost));
        }
        data->pushCosts(costBuffer), costBuffer.clear();
    }

    void join() {
        th->join();
        delete th;
    }

    GlobalData *data;
    Elem *buffer;
    int cursize;

    thread *th;
    mt19937 rng;
    u32 tb[ncards];
};

class Manager {

  public:
    Manager() : workers(nthreads) { FE(it, workers) it->init(data); }

    void initPass(int passId) {
        LOW_KEY = passId * chunks_per_pass * chunk_size;
        HIGH_KEY = LOW_KEY + chunks_per_pass * chunk_size;
        data.rebase(LOW_KEY);
    }

    void init_cost() {
        int tot = 1;
        REP(i, nhand) tot *= ncards;
        REP(i, tot) data.q.add(i);

        FE(it, workers) it->th =
            new thread([](Worker *w) { w->init_cost(); }, &*it);
        join();

        FILE *costFile = fopen(cost_filename, "wb");
        data.dumpCost(costFile);
        fclose(costFile);
    }

    void init_compute() {
        data.init(chunks_per_pass);

        REP(passId, npass) {
            printf("on pass %d\n", passId);
            initPass(passId);

            puts("stage 1");
            REP(i, max_seed / key_chunk_size)
            data.q.add((u32)i * key_chunk_size);
            FE(it, workers) it->th =
                new thread([](Worker *w) { w->stage1(); }, &*it);
            join();

            puts("go stage 2");
            REP(i, chunks_per_pass) data.q.add(passId * chunks_per_pass + i);
            FE(it, workers) it->th =
                new thread([](Worker *w) { w->stage2(); }, &*it);
            join();
            puts("DONE");
        }
    }

    void load_cost() {
        FILE *costFile = fopen(cost_filename, "rb");
        data.loadCost(costFile);
        fclose(costFile);
        data.init(tot_chunks);
    }

    void load_query(u32 low_range, u32 high_range) {
        data.low_range = low_range;
        data.high_range = high_range;

        data.totelem = 0;
        FOR(i, low_range, high_range) data.q.add(i);
        FE(it, workers) it->th =
            new thread([](Worker *w) { w->load_query(); }, &*it);
        join();
    }

    void unload_query() {
        FOR(i, data.low_range, data.high_range) data.q.add(i);
        FE(it, workers) it->th =
            new thread([](Worker *w) { w->unload_query(); }, &*it);
        join();
    }

    void do_cost_eval() {
        FOR(i, data.low_range, data.high_range) data.q.add(i);
        FE(it, workers) it->th =
            new thread([](Worker *w) { w->eval_cost(); }, &*it);
        join();
    }

    void join() { FE(it, workers) it->join(); }

    GlobalData data;
    vector<Worker> workers;
};

const int nperms = 4;
const int nload = 2;
const int num_neighbor = 2;
const u32 load_range = (tot_chunks + nload - 1) / nload;

class Optimizer {
  public:
    vector<PermEval> perms;
    mt19937 rng;
    Manager *manager;

    Optimizer() : perms(nperms) {}

    void init(Manager *manager) {
        this->manager = manager;
        rng.seed(rand());
        REP(i, nperms) perms[i].init(rng);
        manager->data.perms = &perms;
    }

    void go(int nround) {
        REP(i, nround) {

            REP(j, num_neighbor) {
                REP(k, nperms) perms[k].gen_next();

                REP(k, 1) {
                    u32 low_range = load_range * k;
                    u32 high_range = min((u32)tot_chunks, load_range * (k + 1));
                    manager->load_query(low_range, high_range);
                    manager->do_cost_eval();
                    manager->unload_query();
                }
            }
            REP(k, nperms)
            perms[k].select_next();
        }
    }
};

int main(int argc, char **argv) {
    srand(time(0));
    costMap[(u8)CostEnum::Nothing] = 0;
    costMap[(u8)CostEnum::Jacks] = 1;
    costMap[(u8)CostEnum::TwoPairs] = 2;
    costMap[(u8)CostEnum::Three] = 3;
    costMap[(u8)CostEnum::Straight] = 4;
    costMap[(u8)CostEnum::Flush] = 6;
    costMap[(u8)CostEnum::House] = 9;
    costMap[(u8)CostEnum::Four] = 25;
    costMap[(u8)CostEnum::StraightFlush] = 50;
    costMap[(u8)CostEnum::RoyalFlush] = 800;

    initMasks();
    REP(i, ncards) default_perm.pb(i);

    Manager manager;
    std::string mode = "";
    if (argc >= 2)
        mode = argv[1];

    if (mode == "init") {
        manager.init_compute();

    } else if (mode == "cost") {
        manager.init_cost();

    } else if (mode == "optim") {
        manager.load_cost();
        Optimizer x;
        x.init(&manager);
        x.go(100);
    } else if (mode == "expected") {

        manager.load_cost();
        u32 perm[] = { 40, 34, 22, 17, 46, 12, 4,  16, 18, 38, 5,  30, 10,
                       25, 3,  14, 37, 50, 7,  47, 23, 32, 44, 0,  11, 20,
                       15, 41, 42, 35, 39, 33, 49, 36, 13, 27, 43, 6,  29,
                       51, 1,  28, 8,  31, 19, 26, 21, 2,  45, 48, 9,  24 };
        REP(i, ncards) perm[i] = i;
        vector<PermEval> vec(1);
        PermEval &x = vec[0];
        memcpy(x.perm, perm, sizeof(perm));
        manager.data.perms = &vec;
        int nsep = 100;

        u32 active_range = (tot_chunks + nsep - 1) / nsep;

        manager.data.totelem = 0;
        REP(k, nsep) {
            x.cur_cost = 0;
            u32 low_range = active_range * k;
            u32 high_range = min((u32)tot_chunks, active_range * (k + 1));
            manager.load_query(low_range, high_range);
            manager.do_cost_eval();
            manager.unload_query();
            double avg = 1. * x.cur_cost / manager.data.totelem;
            printf("at sep %d, avg=%lf, totelem=%ld\n", k, avg,
                   manager.data.totelem);
        }
        assert(manager.data.totelem == max_seed);
        printf("expected gain: %lf\n", 1. * x.cur_cost / max_seed);

    } else if (mode == "query") {
        manager.load_cost();

        vi perm = default_perm;
        u32 iperm[ncards];
        REP(i, ncards) iperm[perm[i]] = i;

        int buflen = 128;
        char buf[buflen];
        while (fgets(buf, buflen, stdin)) {
            u32 tb[nhand];
            int pos = 0;
            // fprintf(stderr, "recv >> %s\n", buf);
            REP(i, nhand) {
                int tmp;
                assert(sscanf(buf + pos, "%d%n", tb + i, &tmp) > 0);
                pos += tmp;
            }

            u32 hand = getHandWithIperm(tb, iperm);
            u32 action = manager.data.getBestAction(hand, (u32 *)perm.data());
            REP(i, nhand) if (action >> (nhand - 1 - i) & 1) printf("%d ", i);
            puts("END");
            fflush(stdout);
        }

    } else if (mode == "test") {
        manager.load_cost();

        int nstep = 30000;
        mt19937 rng;

        u32 perm[] = { 40, 34, 22, 17, 46, 12, 4,  16, 18, 38, 5,  30, 10,
                       25, 3,  14, 37, 50, 7,  47, 23, 32, 44, 0,  11, 20,
                       15, 41, 42, 35, 39, 33, 49, 36, 13, 27, 43, 6,  29,
                       51, 1,  28, 8,  31, 19, 26, 21, 2,  45, 48, 9,  24 };

        srand(2);
        REP(i, ncards) perm[i] = i;
        u32 iperm[ncards];
        REP(i, ncards) iperm[perm[i]] = i;

        s64 v = 0;
        int info_period = nstep / 100;
        REP(k, nstep) {

            if (k % info_period == 0)
                printf("test %d %%, v=%Ld, avg=%lf\n", k / info_period, v,
                       1. * v / (k + 1));

            u32 seed = (u32)rand() % max_seed;
            u32 tb[ncards];

            rng.seed(seed);
            getPerm(rng, tb);
            REP(i, ncards) tb[i] = perm[tb[i]];
            u32 hand = getHandWithIperm(tb, iperm);

            u32 action = manager.data.getBestAction(hand, perm);
            REP(k, nhand) if (action >> (nhand - 1 - k) & 1)
                swap(tb[k], tb[k + nhand]);

            u32 handForCost = getHandForCost(tb);
            assert(costMap[(u8)getCostNoCache(handForCost)] ==
                   manager.data.getHandCost(handForCost));

            int cost = manager.data.getHandCost(handForCost);
            if (0 && cost > 1) {
                REP(i, nhand) printf("(%d,%d) ", tb[i] % 13, tb[i] / 13);
                puts("");
            }
            v += cost - 1;
        }
        printf(">> got in total %Ld\n", v);

    } else {
        printf("unknown action %s\n", mode.c_str());
        return 1;
    }

    return 0;
}
