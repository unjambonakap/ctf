#include <cassert>
#include <cstdio>
#include <cstdlib>
#include <fstream>
#include <iostream>
#include <map>
#include <set>

const int NX = 0x10000;
uint16_t tb[NX];
const int g_bufstart = 0x1208 / 2;
const int g_bufend = 0x1248 / 2;
const int g_buflen = g_bufend - g_bufstart;

typedef void *(*func_t)();
std::map<int, func_t> func_data;

std::map<int, std::set<int> > vals;
std::map<int, int> reads;
std::map<int, int> writes;
std::set<int> fixed_mem;
bool REAL = 0;

uint16_t T(uint16_t x) {
  if (1) {
    vals[x].insert(tb[x]);

    // assert(vals[271].size() == 1);
  }
  if (x >= g_bufstart && x < g_bufend) printf("READ CHAR %d\n", x - g_bufstart);
  // assert(x!=g_bufstart+2);
  ++reads[x];

  return tb[x];
}

uint16_t &Ts(uint16_t x) {
  if (1) {
    vals[x].insert(tb[x]);
    // assert(vals[271].size() == 1);
  }
  // assert(x!=g_bufstart+1);
  ++writes[x];

  return tb[x];
}

func_t get_func(int x) {
  if (!func_data.count(x)) {
    printf("DO NOT HAVE FUNC %x\n", x);
    assert(0);
  }
  return func_data[x];
}

#if 0
#include "code.h"
#else
#include "code.opt.h"
#endif

void run() {
  vals.clear();
  writes.clear();
  reads.clear();
  std::ifstream ifs("../turing_data/real.start.serbx", std::ios::binary);
  ifs.read((char *)tb, NX * 2);
  printf("HAAAA %d\n", tb[2038+2007]);
  init();
  tb[g_bufstart] = '@';

  func_t cur = (func_t)entry_func();
  while (cur) {
    cur = (func_t)cur();
  }
  printf("HAAAA %d\n", tb[2038+2007]);
}

int main() {
  // const vals:
  // 271 -> 2038
  // 1331 -> 2038
  // 421 -> 1
  // 425 -> 0
  run();
  for (auto &val : vals)
    if (val.second.size() == 1) fixed_mem.insert(val.first);
  REAL = true;

  int maxv = 9654;
  int startv = 207;
  for (int i=startv; i<=maxv; ++i){
    if (tb[2038+i] == 0){
      //printf("BRANCH AT %d\n"

    }

  }



  run();

  for (auto &x : vals) {
    if (x.first != 2031) continue;
    printf("%d %d >> ", x.first, x.second.size());
    for (auto &v : x.second) printf(">> %d", v);

    puts("");
  }

  puts("DATA===");
  printf("%d\n", tb[2040]);

  return 0;
}
