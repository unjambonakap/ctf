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
#include <fstream>
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
  REP (i, n)
    cout << t[i] << " ";
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
const u64 blk_size = 512;
extern "C" void init_rc5(char *ctx);
extern "C" void decrypt_rc5(char *ctx, u8 *buf);

int main() {
  vector<pair<u64, u64> > blocks;
  blocks.pb(MP(blk_size * 1 + 64, blk_size * 2 - 64));
  blocks.pb(MP(blk_size * 2097155, blk_size * 02046-64));
  //blocks.pb(MP(blk_size * 0x0003147776, blk_size * 1));

  int len = 0;
  for (auto &a : blocks)
    len += a.ND;

  u8 *buf = new u8[len];
  FILE *f = fopen("./img", "rb");
  u64 buf_pos = 0;

  for (auto &a : blocks) {
    fseeko(f, a.ST, SEEK_SET);
    fread(buf + buf_pos, 1, a.ND, f);
    buf_pos += a.ND;
  }

  char ctx[1000];
  init_rc5(ctx);

  for (int i = 0; i < len; i += 0x10) {
    decrypt_rc5(ctx, buf + i);
  }
  struct fileentry {
    u32 size;
    u8 drand[0x10];
    u8 dhash[0x10];
    char content[0];
  };

  vector<fileentry *> entries;
  int pos = 0;
  int fileid=0;
  while (true) {
    if (pos >= len)
      break;
    fileentry *cur=(fileentry *)(buf + pos);
    entries.pb(cur);
    pos += cur->size+0x24;
    printf("got entry >> %x, %x %x\n", cur->size, pos, len);
    if (pos<=len){
      char fname[100];
      sprintf(fname, "./files/res_%02d.out", fileid);
      std::ofstream ofs(fname, std::ofstream::binary);
      ofs.write((const char*)cur->drand, 0x10);
      ofs.write((const char*)cur->dhash, 0x10);
      ofs.write((const char*)cur->content, cur->size);
    }
    ++fileid;
  }

  return 0;
}
