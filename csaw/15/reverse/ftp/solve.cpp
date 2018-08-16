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

u32 ANS = 0x0d386d209;
char charset[] =
  "ABCDEFGHIJKLMNOPQRSTUVWXYZ";
int len;

char buf[10];

u32 do_hash(const char *buf, int n) {
  u32 res = 0x1505;
  REP(i, n) res = buf[i] + res * 33;
  return res;
}
//USER blankwall
//PASS JJUUQQZ
//flag{n0_c0ok1e_ju$t_a_f1ag_f0r_you}



bool check(char *buf, int n) {
  u32 res = do_hash(buf, n);
  return res == ANS;
}

int go(int pos) {
  buf[pos]='\n';
  if (check(buf, pos+1)) {
    buf[pos] = 0;
    printf("foudn sol >>  %s\n", buf);
    return 1;
  }

  if (pos == 7)
    return 0;
  REP(i, len) {
    buf[pos] = charset[i];
    if (go(pos + 1))
      return 1;
  }
  return 0;
}

int main() {
  printf("%x\n", do_hash("AAAAAA", 5));
  len = strlen(charset);
  go(0);
}
