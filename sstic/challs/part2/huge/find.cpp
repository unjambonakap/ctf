// Compile with g++ -g -masm=intel -o a.out find.cpp

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

#define FOR (i, a, b) for (int i = (int)(a); i < (int)(b); ++i)

#define FE                                                                     \
  (i, t) for (__typeof((t).begin()) i = (t).begin(); i != (t).end(); ++i)
#define FEV                                                                    \
  (i, t) for (__typeof((t).rbegin()) i = (t).rbegin(); i != (t).rend(); ++i)

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

int main() {
  for (u64 i = 0; i < 1ull << 32; ++i) {
    u64 a = 0x1e716dcb + (i << 32);
    u64 b = 0x6365623134333ffe;
    u64 res;

    // ok at 3174346476
//a=0xbd34aeec1e716dcbull;
//b=0x6365623134333ffeull;
    __asm__ volatile("mov rax, %2\n"
                     "pushq rax\n"
                     "mov rax, %1\n"
                     "pushq rax\n"
                     "wait\n"
                     "fnclex\n"
                     "fld tbyte ptr [rsp]\n"
                     "fld st(0)\n"
                     "fcos\n"
                     "fcompp\n"
                     "wait\n"
                     "fnstsw ax\n"
                     "and rax, 0xffdf\n"
                     "mov %0, rax\n"
                     "popq rax\n"
                     "popq rax\n"
                     : "=r"(res)
                     : "r"(a), "r"(b)
                     : "%rax");

    if (res == 0x4000) {
      printf("ok at %Lu\n", i);
      break;
    }
  }
  return 0;
}

/*
const char *checker =
  "\x9b\xdb\xe2\xdb\x6c\x24\x18\xd9\xc0\xd9\xff\xde\xd9\x9b\xdf\xe0\xc3";
typedef void (*f)();

int main() {
  for (u64 i = 0; i < 1ull << 32; ++i) {
    u64 a = 0x1e716dcb + (i << 32);
    u64 res;
    __asm__ volatile("mov rax, %1\n"
                     "mov rbx, %2\n"
                     "call rbx\n"
                     "mov %0, rax\n"
                     "popq rax\n"
                     : "=r"(res)
                     : "m"(a), "m"(checker)
                     : "rax", "rbx");

    if ((res&0xffff) == 0x4000) {
      printf("ok at %Lu\n", i);
    }
  }
  return 0;
}
*/
