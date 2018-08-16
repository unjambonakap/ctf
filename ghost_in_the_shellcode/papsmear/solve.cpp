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
//#include <ext/hash_map>

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
    REP(i, n) cout << t[i] << " ";
    cout << endl;
}
template <class T> void out(vector<T> t, int n = -1) {
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

const int maxn = 1e6;

int gcd(int a, int b) {
    if (a < b)
        return gcd(b, a);
    return b ? a : gcd(b, a % b);
}

int isp[maxn];

int main() {
    memset(isp, 1, sizeof(isp));
    for (int i = 2; i < maxn; ++i)
        if (isp[i])
            for (ll j = 1ll * i * i; j < maxn; j += i)
                isp[j] = 0;

    FOR(i, 1e4, 1e5) if (isp[i]) FOR(j, 100, 1000) {
        REP(k, 9) if (!isp[i + k * j]) goto fail;
        printf("ok %d %d\n", i, j);
    fail:;
    }

    return 0;
}
