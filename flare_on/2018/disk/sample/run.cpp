#include <cassert>
#include <cstdio>
#include <cstdlib>
#include <fstream>
#include <iostream>
#include <map>
#include <opa_common.h>
#include <set>

const int NX = 0x10000 - 2038;
const int g_bufstart = 0x1208 / 2 - 2038;
const int g_bufend = 0x1248 / 2 - 2038;
const int g_buflen = g_bufend - g_bufstart;
DEFINE_string(infile, "", "");
DEFINE_int32(stop_at, -1, "");
DEFINE_bool(stop_at_output, false, "");
DEFINE_bool(log_mem, false, "");
DEFINE_string(query, "", "");
DEFINE_string(outfile, "", "");

typedef void *(*func_t)();
std::map<int, func_t> func_data;

std::map<int, std::set<int> > vals;
std::map<int, int> reads;
std::map<int, int> writes;
std::set<int> fixed_mem;
bool REAL = 0;
typedef std::array<u16, NX> mem_t;

u8 ror(u8 v) { return v = (v >> 1) | (v << 7); }

void sror(u8 &v) { v = ror(v); }

class Runner {
public:
  mem_t tb;
  u8 *buf;
  bool done;
  bool log_mem = false;
  int good = -1;
  int bad = -1;
  int goodcnt;
  int badcnt;
  std::vector<int> track;

  void reset(bool load = true) {
    buf = (u8 *)tb.data();
    log_mem = FLAGS_log_mem;
    if (load) {
      std::ifstream ifs(FLAGS_infile, std::ios::binary);
      assert(ifs.is_open());
      ifs.read((char *)tb.data(), NX * 2);
    }
    done = false;
    goodcnt = 0;
    badcnt = 0;
  }

  uint16_t T(uint16_t x) {
    OPA_CHECK0(x < tb.size());
    if (log_mem) {
      if (1) {
        vals[x].insert(tb[x]);

        // assert(vals[271].size() == 1);
      }
      // assert(x!=g_bufstart+2);
      ++reads[x];
    }
    return tb[x];
  }

  uint16_t &Ts(uint16_t x) {
    if (log_mem) {
      if (1) {
        vals[x].insert(tb[x]);
        // assert(vals[271].size() == 1);
      }
      // assert(x!=g_bufstart+1);
      ++writes[x];
    }

    return tb[x];
  }

  void run(const std::string pwd, int stop_at = -1) {
    REP (i, pwd.size()){
      tb[g_bufstart + i] = (u8)pwd[i];
    }

    while (!done) {
      if (T(6) == 1) {
        if (FLAGS_stop_at_output) {
          break;
        }
        printf("OUTPUT CHAR %d %c\n", T(4), T(4));

        Ts(6) = 0;
        Ts(4) = 0;
      }
      s16 op = T(0);

      if (op == good) goodcnt++;
      if (op == bad) {
        badcnt++;
      }

      s16 pos = T(op);
      if (pos >= g_bufstart && pos < g_bufend) {
        int id = pos - g_bufstart;
        if (stop_at == id) break;

        // printf("READ CHAR %d %d\n", id, tb[pos]);
      }

      if (pos <= -2) break;
      if (pos < 0) {
        Ts(0) += 1;
        continue;
      }

      s16 r1 = T(pos);
      s16 r2 = T(1);
      s16 diff = r1 - r2;
      if (op == 8253) {
        // printf("UFUUU %d %d >> %d\n", r1, r2, diff);
        track.push_back(diff);
      }
      Ts(1) = diff;

      if (pos == 2)
        Ts(3) = diff;
      else
        Ts(pos) = diff;

      if (r1 < r2) Ts(0) += 1;
      Ts(0) += 1;
    }
  }
};

template <class T> std::vector<int> diff_mem(const T &t1, const T &t2) {
  std::vector<int> res;
  REP (i, t1.size())
    if (t1[i] != t2[i]) res.push_back(i);
  return res;
}
template <class T> void diff_mem_print(const T &t1, const T &t2) {
  for (auto &diffp : diff_mem(t1, t2)) {
    printf("%d >> %04x  %04x (%d >> %d %d)\n", diffp, t1[diffp], t2[diffp],
           diffp, t1[diffp], t2[diffp]);
  }
}

mem_t get1(const std::string &pwd, int stop_at = -1) {
  Runner runner;
  runner.reset();
  runner.run(pwd, stop_at);
  return runner.tb;
}
int main(int argc, char **argv) {
  opa::init::opa_init(argc, argv);

  std::vector<char> clist;
  REP (i, 128) {
    if (!isprint(i) || i < 32) continue;
    OPA_DISP0(char(i), clist.size());
    clist.pb(i);
  }

  std::string pwd(30, '0');
  pwd[0] = '@';
  if (FLAGS_query.size() > 0) {
    mem_t res = get1(FLAGS_query);
    if (FLAGS_outfile.size()) {
      std::ofstream ofs(FLAGS_outfile, std::ios::binary);
      ofs.write((char *)res.data(), res.size() * 2);
    }

    return 0;
  }

  if (0) {
    std::vector<mem_t> mems;
    if (0) {
      for (auto &c : clist) {
        pwd[3] = c;
        mems.push_back(get1(pwd));
      }
    } else {
      FOR (i, 1, 30)
        pwd[i] = 'a';
      mems.push_back(get1(pwd));
      FOR (i, 1, 30)
        pwd[i] = 'b';
      mems.push_back(get1(pwd));
    }

    REP (i, mems.size() - 1) {
      printf("=== diff %d %d\n", 0, i);
      diff_mem_print(mems[0], mems[i + 1]);
    }
  } else if (0) {

    if (1) {
      int nx = 30;
      int base = 2681 * 2;

      REP (r, 8) {
        REP (c1, 256) {
          pwd[1] = c1;
          Runner runner;
          runner.reset();
          REP (i, nx)
            REP (j, r)
              sror(runner.buf[base + i]);
          runner.good = 8782;
          runner.bad = 8773;
          runner.run(pwd, 2);
          OPA_DISP0(c1, runner.goodcnt, runner.badcnt, runner.tb[2922],
                    runner.track);
          if (runner.track.back() == 0) {
            OPA_DISP("OK FOR ", c1, r);
          }
        }
      }

      return 0;
    }

    REP (c1, 256) {
      FOR (c2, 0, 256) {
        REP (c3, 256) {
          pwd[1] = c1;
          pwd[2] = c2;
          pwd[3] = c3;
          Runner runner;
          runner.reset();
          runner.run(pwd, 4);
          // OPA_CHECK(runner.tb[2922] == 0, c1, c2, c3);
          if (runner.track.back() == 0) {
            OPA_DISP("OK FOR ", pwd, c1, c2, c3);
          }
        }
      }
    }
  } else {

    // clang-format off
    std::vector<std::vector<int> > cnds = {
      {0x40,'a',0x4e,0x6,},
      //{0x40,'a',},
      //{0x40,'a'},

    //(0x40,0,0x4e,0x6,0x43,0x6,0x52,0x2,0x22,0x10,0x14,0x7,0x31,0xd7,0x52,0xd2,0x6,0xe7,0x4,0x14,0x43,0x10,0x7,0xd1,0x4d,0x13),a=0x4c,b=0
    };
    REP(i, cnds.size()){
      //cnds[i][2] = 0xce;
      //cnds[i][3] = 0x7;
      //cnds[i][1] += 0x80;
    }
    // clang-format on

    std::set<int> tmp;
    puts("START");
    printf("KAPPA %d\n", cnds[0].size());
    printf("KAPPA %d\n", cnds.size());
    while (cnds[0].size() < 30) {
      std::vector<std::vector<int> > ncnds;
      printf("START PROCESS %d\n", cnds[0].size());

      int id = 0;
      int x = 0;
      for (auto &cx : cnds) {

        ++id;
        REP (i, cx.size())
          pwd[i] = cx[i];

        if (0) {
          Runner runner;
          runner.reset();
          runner.good = 8782;
          runner.bad = 8773;
          runner.run(pwd, 4);
          printf("FUUU %d %d %d\n", runner.tb[2922], runner.goodcnt,
                 runner.badcnt);
        }

        int n = cx.size();
        mem_t curmem = get1(pwd, cx.size());

        OPA_DISP("ON CND", id, cnds.size(), x, tmp.size());
        REP (a, 256) {
          REP (b, 256) {
            pwd[n + 0] = a;
            pwd[n + 1] = b;

            Runner runner;
            runner.reset(false);
            runner.tb = curmem;
            runner.good = 8782;
            runner.bad = 8773;
            runner.run(pwd, n + 2);
            // OPA_CHECK(runner.tb[2922] == 0, c1, c2, c3);
            if ((s16)runner.tb[2922] == -6) OPA_DISP("GOT ", pwd, cx, a, b, runner.tb[2922]);
            if (runner.track.size() == 1 && runner.track.back() == 0) {
              OPA_DISP("OK FOR ", pwd, cx, a, b, runner.tb[2922]);
              ncnds.push_back(cx);
              ncnds.back().pb(a);
              ncnds.back().pb(b);
              REP (i, ncnds.back().size() / 2)
                printf("%c", ncnds.back()[i * 2]);
              puts("");
            }
          }
        }
      }

      cnds = ncnds;
      OPA_CHECK0(cnds.size() > 0);
      // cnds.resize(1);
    }
    puts("DONE");

    for (auto &cnd : cnds) {
      printf("HAVE CND >> ");
      REP (i, cnd.size())
        printf("%02d", cnd[i]);
      puts("");
    }
  }

  /*
     === diff 0 65
     273 >> 0020  0062 (273 >> 32 98)
     2880 >> 0042  2142 (2880 >> 66 8514)
     5721 >> 0000  2100 (5721 >> 0 8448)
     7926 >> 0063  2163 (7926 >> 99 8547)
     8029 >> 0062  2162 (8029 >> 98 8546)
     8768 >> 0d53  2e53 (8768 >> 3411 11859)


     */
  return 0;
}
