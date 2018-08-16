#include <opa_common.h>
#include <opa/threading/runner.h>
#include <opa/threading/dispatcher.h>
#include <protobuf/product_key_msg.pb.h>
#include <opa/math/common/Utils.h>

using namespace opa::threading;
using namespace std;

string validChars = "12346789ABCDEFGHIJKLMNPQRTUVWXYZ";

int A[] = { 271135, 185705, 872007, 1022754, 413042 };
int B[] = { 821273, 66000, 7662, 386178, 611981 };
int C[] = { 770098, 621577, 992113, 830442, 243815 };
int D[] = { 376235, 84434, 1019539, 784643, 594329 };
int E[] = { 284649, 885640, 213732, 236091, 132494 };
int F[] = { 615228, 967387, 708052, 69554, 150828 };
int G[] = { 318496, 486875, 327057, 320030, 560587 };

const int *TB[] = { C, D, E, F, G };
int shiftA[] = { 5, 7, 11, 13, 17 };
int shiftB[] = { 3, 6, 9, 12, 15 };
int shiftC[] = { 16, 11, 8, 4, 2 };

const int NB = 20;
const int N = 1 << NB;
const int mask = N - 1;
const int M = 5;
const int ncheck = 7;
int rol(int val, int shift) {
    return (val << shift & mask) | val >> NB - shift;
}

class ProductKey {
  public:
    char imap[128];

    int bits[M][NB];
    int bitspace = 8;
    int check_mask = 1 | 1 << bitspace | 1 << 2 * bitspace;
    std::string sol;

    int cur_check = 0;
    int check_point[NB];
    int have[ncheck][M][N];
    int ivals[M][N];

    int getlast(int x) {
        int sum = 0;
        REP(i, 4) sum += x & 0x1f, x >>= 5;
        return sum % 32;
    }

    string get_single(int x) {
        vector<int> tb(5);
        REP(i, 4) tb[3 - i] = x >> 5 * i & 0x1f;
        tb[4] = getlast(x);
        std::string res;
        REP(i, 5) res += validChars[tb[i]];
        return res;
    }

    inline int getShift(int target, int pos) {
        // array3[i]=sum(F(a2[i+k], TB[k][i], shiftC[k])
        // i=target, i+k=pos =>  k=pos-target
        return shiftC[(M + pos - target) % M];
    }

    inline int getConst(int target, int pos) {
        return TB[(M + pos - target) % M][target];
    }

    inline int getBitPos(int round, int shiftVal) {
        return (NB + round - shiftVal) % NB;
    }

    inline int getCur(int pos) {
        int v = 0;
        REP(j, NB) v |= max(0, bits[pos][j]) << j;
        return v;
    }

    int eval_round(int *in, int round) {
        int res = 0;
        REP(j, M) res += rol(in[j] ^ getConst(round, j), getShift(round, j));
        res &= mask;
        return res;
    }

    inline int getMask(int round, int pos) {
        int cur_mask = 0;
        FOR(target, 2, M) REP(j, round) cur_mask |=
            1 << getBitPos(j, getShift(target, pos));
        return cur_mask;
    }

    void make_check(int round) {
        assert(cur_check < ncheck);
        check_point[round] = cur_check;
        printf("making check %d %d\n", round, cur_check);
        REP(pos, M) {
            int cur_mask = getMask(round, pos);
            REP(j, N) if (ivals[pos][j] !=
                          -1) have[cur_check][pos][j & cur_mask] = 1;

            int cnt = 0;
            int tot = 0;
            REP(j, N) if (!(j & ~cur_mask)) {
                ++tot;
                if (!have[cur_check][pos][j])
                    ++cnt;
            }
            printf("mask=%x, pos %d, missing %d/%d\n", cur_mask, pos, cnt, tot);
        }
        puts("\n");
        ++cur_check;
    }

    inline bool do_check(int round) {
        int id = check_point[round];
        if (id == -1)
            return true;
        REP(pos, M)
        if (!have[id][pos][getCur(pos)])
            return false;
        return true;
    }

    std::string get_str(int *in) {
        std::string res;
        REP(i, M) res += (i == 0 ? "" : "-") + get_single(in[i]);
        return res;
    }

    vector<int> reverse_last(int *tb) {
        vi res;
        REP(i, M) {
            assert(ivals[i][tb[i]] != -1);
            res.pb(ivals[i][tb[i]]);
        }
        return res;
    }

    int SAVE_ROUND;
    const int maxn = 1e5;

    bool go(int round, int pos, int cx) {
        int cur = 0;
        if (pos == M) {
            if (cx & check_mask)
                return false;

            if (round == SAVE_ROUND) {
                product_key::Data data;
                data.set_round(round);
                data.set_pos(pos);
                data.set_cx(cx);
                data.set_bits(bits, sizeof(bits));
                bool more;
                cb(data, more);
                return !more;
            }

            if (1 && round == 11) {
                int vals[M];
                REP(i, M) vals[i] = getCur(i);
                int tmp = eval_round(vals, 0) >> 12 & 0xff;
                if (tmp != 1)
                    return false;
            }

            if (!do_check(round + 1))
                return false;

            if (round == 13) {
                static int nsol = 0;
                int vals[M];
                REP(i, M) vals[i] = getCur(i);
                int res[M];
                REP(i, M) res[i] = eval_round(vals, i);
                if (res[2])
                    return false;
                if (res[3])
                    return false;
                printf("here %x\n", res[0] >> 12);
                if (res[4])
                    return false;

                puts("check 0");
                if ((res[0] >> 12 & 0xff) == 1) {
                    printf(">> found sol\n");
                    out(vals, M);
                    vi tmp = reverse_last(vals);
                    out(tmp);
                    printf(">> %d\n", tmp.size());
                    sol = get_str(tmp.data());
                    printf("vals >> "), out(vals, M);
                    printf("res >> "), out(res, M);
                    printf("str>> %s\n", sol.c_str());
                    puts("HAS FOUND SOLUTION");
                    fflush(stdout);
                    return true;
                }

                // REP(i, M) { out(bits[i], NB); }
                //++nsol;
                return false;
            }

            return go(round + 1, 0, cx >> 1);
        }

        int old[NB];
        memcpy(old, bits[pos], sizeof(old));

        REP(i, 8) {
            int nc = cx;
            REP(j, 3) {
                int bit = i >> j & 1;
                nc += bit << (j * bitspace);
                int shift = getShift(2 + j, pos);
                int bitpos = getBitPos(round, shift);
                int C = getConst(2 + j, pos) >> bitpos & 1;
                bit ^= C;
                int c = old[bitpos];

                if (c != -1 && c != bit)
                    goto fail;
                bits[pos][bitpos] = bit;
            }

            if (go(round, pos + 1, nc))
                return true;

            memcpy(bits[pos], old, sizeof(old));
        fail:

            ;
        }
        return false;
    }

    void init(int save_round) {
        printf("INIT KAPPA %d\n", save_round);
        SAVE_ROUND = save_round;
        REP(i, validChars.size()) imap[validChars[i]] = i;
        memset(ivals, -1, sizeof(ivals));
        memset(check_point, -1, sizeof(check_point));

        REP(i, NB) {
            int tmp = -1;
            REP(j, M) tmp &= getMask(i, j);
            if (~tmp >> 12 & 0xff)
                printf("ok at %d\n", i);
        }

        REP(j, M) REP(i, N) ivals
            [j][rol(i ^ A[j], shiftA[j]) - rol(i ^ B[j], shiftB[j]) & mask] = i;
        make_check(14);
        memset(bits, -1, sizeof(bits));
    }

    std::function<u32(product_key::Data &work, bool &out_more)> cb;
};

class ProductKeyJob
    : public opa::threading::FindOneJob<product_key::Init, product_key::Data,
                                        product_key::Res> {
  public:
    OPA_DECL_CLONE(Job, ProductKeyJob)

    static void Register() {
        opa::threading::Runner::Register_job(
            JOB_NAME, []() { return new ProductKeyJob(); });
        OPA_REGISTER_TJOB(ProductKeyJob)
    }
    static const std::string JOB_NAME;

    shared_ptr<ProductKey> x;
    ProductKeyJob() { x = make_shared<ProductKey>(); }
    std::string sol;
    bool found;

    virtual void tworker_initialize(const product_key::Init &init) {
        puts("WORKER INITIALIZE");
        x->init(-1);
    }

    virtual void tserver_initialize(product_key::Init &out_init) {
        puts("SERVER INIT");
        found = false;
        x->init(1);
    }

    virtual void worker_finalize() {}

    virtual void tworker_do_work(const product_key::Data &data,
                                 product_key::Res &out_res) {
        OPA_ASSERT0(data.bits().size() == sizeof(x->bits));
        memcpy(x->bits, data.bits().data(), sizeof(x->bits));
        puts("GO DO WORK");
        fflush(stdout);
        bool res = x->go(data.round(), data.pos(), data.cx());
        out_res.set_found(res);
        if (res)
            out_res.set_res(x->sol);
    }
    // dispatcher part
    virtual void server_finalize() {}
    virtual void tserver_get_work(const std::function<opa::threading::DataId(
        const product_key::Data &data, bool &out_more)> &cb) {
        x->cb = cb;
        puts("LAAA");
        x->go(0, 0, 0);
        puts("END GET WORK");
    }

    virtual bool tserver_handle_res(const product_key::Res &res) {
        if (!res.found())
            return false;
        found = true;
        sol = res.res();
        puts("GOT ONE HERE MOFO");
        return true;
    }

  private:
};

const std::string ProductKeyJob::JOB_NAME = "PKEY_JOB";

void run_server(Dispatcher *dispatcher) {

    int cnt = 0;
    // make_check(12);

    // int data[]={ 0, 0, 0, 0, 0 };
    // int data[] = { 0x21003, 0xd0905, 0xce6d2, 0x27603, 0xd4068 };
    // int data[]={0x21003, 0xd0905, 0xce6d2, 0x27603, 0xd4068};
    // vi tmp = reverse_last(data);

    // printf(">> %s\n", get_str(tmp.data()).c_str());
    // return 0;

    ProductKeyJob job;
    dispatcher->process_job(job, Runner::GetJobId(ProductKeyJob::JOB_NAME));
    assert(job.found);
    printf("Solutoin >>> %s\n", job.sol.c_str());
    fflush(stdout);
}

void init() { opa::math::common::initMathCommon(0); }

int main(int argc, char **argv) {
    init();
    Runner runner;

    ProductKeyJob::Register();
    Runner::Build();
    Dispatcher *dispatcher;

    runner.run(argc, (char **)argv, run_server);
}
