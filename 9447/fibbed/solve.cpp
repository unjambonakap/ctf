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
#define REPV(i, n) for (int i = (n) - 1; (int)i >= 0; --i)
#define FOR(i, a, b) for (int i = (int)(a); i < (int)(b); ++i)

#define FE(i, t) \
  for (__typeof((t).begin()) i = (t).begin(); i != (t).end(); ++i)
#define FEV(i, t) \
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

template <class T>
void checkmin(T &a, T b) {
  if (b < a) a = b;
}
template <class T>
void checkmax(T &a, T b) {
  if (b > a) a = b;
}
template <class T>
void out(T t[], int n) {
  REP(i, n) cout << t[i] << " ";
  cout << endl;
}
template <class T>
void out(vector<T> t, int n = -1) {
  for (int i = 0; i < (n == -1 ? t.size() : n); ++i) cout << t[i] << " ";
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

// prime=981725946171163877
// server=58449491987662952,704965025359609904
// client=453665378628814896,152333692332446539
// data=59719af4dbb78be07d0398711c0607916dd59bfa57b297cd220b9d2d7d217f278db6adca88c9802098ba704a18cce7dd0124f8ce492b39b64ced0843862ac2a6
ull prime;
const int n = 2;

struct M {
  M() {
    m[0][0] = 0;
    m[0][1] = 1;

    m[1][0] = m[1][1] = 1;
  }

  void ident() { REP(i, n) REP(j, n) m[i][j] = i == j; }

  M mul(const M &peer)const{
    REP(i,2) REP(j,2){

    }

  }

  ull m[n][n];
};

ull fastecomp(ull a, ull b, ull p) {
  while (p) {
    if (p&1
  }
}

ull find(ull a, ull b) { ull mx = prime; }

int main() {

  prime = 981725946171163877ll;
  ull s1 = 58449491987662952ll;
  ull s2 = 704965025359609904ll;
  ull c1, c2;
  c1 = 453665378628814896ll;
  c2 = 152333692332446539ll;
  return 0;
}
