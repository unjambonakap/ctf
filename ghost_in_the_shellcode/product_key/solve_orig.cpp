#include <vector>
#include <list>
#include <map>
#include <set>
#include <deque>
#include <queue>
#include <stack>
#include <algorithm>
#include <numeric>
#include <utility>
#include <sstream>
#include <iostream>
#include <cstdlib>
#include <string>
#include <cstring>
#include <cstdio>
#include <cmath>
#include <cstdlib>
#include <ctime>
#include <cassert>
#include <climits>
#include <unistd.h>
//#include <ext/hash_map>
#include <time.h>
#include <thread>
#include <mutex>

using namespace std;
using namespace __gnu_cxx;

#define REP(i, n) for (int i = 0; i < int(n); ++i)
#define REPV(i, n) for (int i = (n)-1; (int)i >= 0; --i)
#define FOR(i, a, b) for (int i = (int)(a); i < (int)(b); ++i)

#define FE(i, t)                                                               \
    for (__typeof((t).begin()) i = (t).begin(); i != (t).end(); ++i)
#define FEV(i, t)                                                              \
    for (__typeof((t).rbegin()) i = (t).rbegin(); i != (t).rend(); ++i)

#define two(x) (1LL << (x))
#define ALL(a) (a).begin(), (a).end()

#define pb push_back
#define ST first
#define ND second
#define MP(x, y) make_pair(x, y)

typedef long long ll;
typedef unsigned long long ull;
typedef unsigned int uint;
typedef pair<int, int> pii;
typedef vector<int> vi;
typedef vector<string> vs;
typedef signed char s8;
typedef unsigned char u8;
typedef signed short s16;
typedef unsigned short u16;
typedef signed int s32;
typedef unsigned int u32;
typedef signed long long s64;
typedef unsigned long long u64;

template <class T> void checkmin(T &a, T b) {
    if (b < a)
        a = b;
}
template <class T> void checkmax(T &a, T b) {
    if (b > a)
        a = b;
}
template <class T> void out(T t[], int n) {
    cout << hex;
    REP(i, n) cout << t[i] << " ";
    cout << endl;
}
template <class T> void out(vector<T> t, int n = -1) {
    cout << hex;
    for (int i = 0; i < (n == -1 ? t.size() : n); ++i)
        cout << t[i] << " ";
    cout << endl;
}
inline int count_bit(int n) {
    return (n == 0) ? 0 : 1 + count_bit(n & (n - 1));
}
inline int low_bit(int n) { return (n ^ n - 1) & n; }
inline int ctz(int n) { return (n == 0 ? -1 : ctz(n >> 1) + 1); }
int toInt(string s) {
    int a;
    istringstream(s) >> a;
    return a;
}
string toStr(int a) {
    ostringstream os;
    os << a;
    return os.str();
}

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
int rol(int val, int shift) {
    return (val << shift & mask) | val >> NB - shift;
}

int cnd[M][N][M];

char imap[128];

thread_local int bits[M][NB];
int bitspace = 8;
int check_mask = 1 | 1 << bitspace | 1 << 2 * bitspace;

const int ncheck = 7;
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
        REP(j, N) if (ivals[pos][j] != -1) have[cur_check][pos][j & cur_mask] =
            1;

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

struct state {
    void save(int round, int pos, int cx) {
        m_round = round;
        m_pos = pos;
        m_cx = cx;
        memcpy(m_bits, bits, sizeof(bits));
    }

    void restore() { memcpy(bits, m_bits, sizeof(bits)); }
    int m_bits[M][NB];
    int m_round;
    int m_pos;
    int m_cx;
};

#define LOCK() gLock.lock()
#define UNLOCK() gLock.unlock()
mutex gLock;
queue<state> states;
thread_local int SAVE_ROUND;
const int maxn = 1e5;

void go(int round, int pos, int cx) {
    int cur = 0;
    if (pos == M) {
        if (cx & check_mask)
            return;

        if (round == SAVE_ROUND) {
            state cur;
            cur.save(round, pos, cx);
            LOCK();
            while (states.size() == maxn) {
                UNLOCK();
                usleep(1e6);
                LOCK();
            }
            states.push(cur);
            UNLOCK();
            return;
        }

        if (1 && round == 11) {
            int vals[M];
            REP(i, M) vals[i] = getCur(i);
            int tmp = eval_round(vals, 0) >> 12 & 0xff;
            if (tmp != 1)
                return;
        }

        if (!do_check(round + 1))
            return;

        if (round == 13) {
            static int sol = 0;
            int vals[M];
            REP(i, M) vals[i] = getCur(i);
            int res[M];
            REP(i, M) res[i] = eval_round(vals, i);
            if (res[2])
                return;
            if (res[3])
                return;
            printf("here %x\n", res[0]>>12);
            if (res[4])
                return;

            puts("check 0");
            if ((res[0] >> 12 & 0xff) == 1) {
                printf(">> found sol\n");
                out(vals, M);
                vi tmp = reverse_last(vals);
                out(tmp);
                printf(">> %d\n", tmp.size());
                string sol = get_str(tmp.data());
                printf("vals >> "), out(vals, M);
                printf("res >> "), out(res, M);
                printf("str>> %s\n", sol.c_str());
                assert(0);
            }

            // REP(i, M) { out(bits[i], NB); }
            ++sol;
            return;
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

        go(round, pos + 1, nc);

        memcpy(bits[pos], old, sizeof(old));
    fail:

        ;
    }
}

bool done = false;
void worker() {
    SAVE_ROUND = -1;
    while (true) {
        LOCK();
        if (states.size() == 0) {
            UNLOCK();
            if (done)
                break;
            sleep(1);
            continue;
        }
        state now = states.front();
        states.pop();
        UNLOCK();

        now.restore();
        go(now.m_round, now.m_pos, now.m_cx);
    }
}

int main() {
    REP(i, validChars.size()) imap[validChars[i]] = i;
    memset(ivals, -1, sizeof(ivals));
    memset(check_point, -1, sizeof(check_point));

    REP(i, NB) {
        int tmp = -1;
        REP(j, M) tmp &= getMask(i, j);
        if (~tmp >> 12 & 0xff)
            printf("ok at %d\n", i);
    }

    REP(j, M) REP(i, N)
        ivals[j][rol(i ^ A[j], shiftA[j]) - rol(i ^ B[j], shiftB[j]) & mask] =
            i;
    int cnt = 0;
    // make_check(12);
    make_check(14);

    // int data[]={ 0, 0, 0, 0, 0 };
    // int data[] = { 0x21003, 0xd0905, 0xce6d2, 0x27603, 0xd4068 };
    //int data[]={0x21003, 0xd0905, 0xce6d2, 0x27603, 0xd4068};
    //vi tmp = reverse_last(data);

    //printf(">> %s\n", get_str(tmp.data()).c_str());
    //return 0;

    memset(bits, -1, sizeof(bits));
    SAVE_ROUND = 0;

    int nthread = 4;
    vector<thread> threads(4);
    REP(i, nthread) { threads[i] = thread(worker); }

    go(0, 0, 0);
    printf("got >> %d\n", states.size());
    done = true;
    REP(i, nthread)
    threads[i].join();

    return 0;
}
