#include <opa/algo/base.h>
#include <opa_common.h>

using namespace std;
DEFINE_string(infile, "", "");
DEFINE_int32(bstart, 5, "");
DEFINE_int32(stop_blk, -1, "");
DEFINE_string(query, "", "");
DEFINE_int32(stop_at, -1, "");
DEFINE_bool(simplequery, false, "");
DEFINE_bool(disp, false, "");
DEFINE_bool(logfirstaccess, false, "");
DEFINE_int32(stop_access, -1, "");
DEFINE_string(outfile, "", "");

constexpr int NX = 0x10000;
std::vector<u16> x;
const int g_bufstart = 0x1208 / 2;
const int g_bufend = 0x1248 / 2;
const int g_buflen = g_bufend - g_bufstart;
std::vector<u16> ix(NX);

u16 g_m1 = 0x2dad;

std::vector<int> diff_mem(const std::vector<u16> &t1,
                          const std::vector<u16> &t2) {
  std::vector<int> res;
  REP (i, t1.size())
    if (t1[i] != t2[i]) res.push_back(i);
  return res;
}
void diff_mem_print(const std::vector<u16> &t1, const std::vector<u16> &t2) {
  for (auto &diffp : diff_mem(t1, t2)) {
    printf("%02x >> %04x  %04x\n", diffp, t1[diffp], t2[diffp]);
  }
}

void diff_exec_print(const std::vector<u16> &t1, const std::vector<u16> &t2) {
  REP (i, t1.size()) {
    if (t1[i] != t2[i]) {
      OPA_DISP("Exec split at ", i);
      break;
    }
  }
  REP (i, t1.size()) {
    if (t1[t1.size() - 1 - i] != t2[t2.size() - 1 - i]) {
      OPA_DISP("Reverse Exec split at ", i);
      break;
    }
  }
}

bool poly(u16 *x, u16 a, u16 b, u16 c) {
  x[b] -= x[a];
  return c && (s16)x[b] <= 0;
}

std::pair<u16, bool> step(u16 *x, u16 b) {
  if (poly(x, x[b], x[b + 1], x[b + 2])) {
    if (x[b + 2] == 0xffff) return { 0, false };
    b = x[b + 2];
  } else
    b += 3;
  return { b, true };
}

struct OutData {
  std::vector<u16> x;
  std::vector<u16> bseq;
  std::set<int> taint;
  int ob;
};

struct Ctrl {
  std::set<int> stopaccess;
  std::set<int> taint;
  std::set<int> dbg;
};

void disp_op(int b) {
  if (!FLAGS_disp) return;
  s16 r = x[x[b + 1]] - x[x[b]];
  printf("DO OP %04x ( %04x %04x %04x): %04x - %04x RES >> %04x\n", b, x[b],
         x[b + 1], x[b + 2], x[x[b + 1]], x[x[b + 0]], (u16)r);
  if (x[b + 2]) {
    if (r <= 0)
      printf("TAKE BRANCH TO %04x\n", x[b + 2]);
    else
      printf("NO BRANCH\n");
  }
}

void doit(const Ctrl &ctrl, OutData &od) {
  u16 b = FLAGS_bstart;
  int cnt = 0;
  std::set<int> taint = ctrl.taint;
  std::set<int> pwd_taint;
  typedef std::vector<int> cycle_t;

  std::map<cycle_t, std::vector<int> > cycle_counts;
  std::vector<int> next(NX, -1);
  std::map<int, pii> conds;
  std::map<int, std::set<int> > writes;
  std::map<int, std::set<pii> > reads;
  std::map<int, int> count_pos;
  std::map<int, std::set<int> > par;
  std::map<int, std::set<int> > next_blk;
  std::set<pii> edges;
  std::map<int, int> blk_next_jump;
  

  REP (i, g_buflen)
    pwd_taint.insert(g_bufstart + i);
  int last_branch = -1;

  while (1) {
    if (b + 3 > g_m1) {
      OPA_CHECK0(false);
    }
    cnt += 1;
    bool done = false;
    REP (f, 2) {
      if (pwd_taint.count(x[b + f])) {
        int pos = x[b + f] - g_bufstart;
        printf("FIRST ACCESS %d %d %d\n", pos, cnt, last_branch);
        if (FLAGS_stop_access == pos) {
          done = true;
        }
        pwd_taint.erase(x[b + f]);
      }
    }
    if (done) break;

    if (ctrl.stopaccess.count(x[b]) || ctrl.stopaccess.count(x[b + 1])) {
      OPA_DISP("Stopping because hit", x[b], od.bseq.size());
      break;
    }

    count_pos[b] += 1;
    od.bseq.push_back(b);
    // if (ctrl.dbg.count(x[b+1])){
    //  disp_op(b);
    //}

    if (x[b] == x[b + 1]) {
      // zero out
      taint.erase(x[b]);
    }
    if (taint.count(x[b]) || taint.count(x[b + 1])) {
      taint.insert(x[b + 1]);
      if (FLAGS_disp && x[b + 2]) printf("TAINTED JUMP\n");
      disp_op(b);
      // printf("DO CMP %04x %04x %04x %04x %x\n", x[b], x[b + 1], x[x[b]],
      //       x[x[b + 1]], cnt);
    }
    reads[b + 0].emplace(x[b + 0], b);
    reads[b + 1].emplace(x[b + 1], b);
    reads[b + 2].emplace(x[b + 2], b);

    if (x[b] != x[b + 1]) {
      u16 va = x[b];
      u16 vb = x[b + 1];

      if (va != vb) {
        writes[vb].insert(x[vb] - x[va]);
        reads[va].emplace(x[va], b);
        reads[vb].emplace(x[vb], b);
      }
    }

    auto sx = step(x.data(), b);
    bool is_branch = x[b + 2];

    if (!sx.second) {
      OPA_DISP("BREAK bEcUse ", b, x[b + 2]);
      break;
    }

    int ob = b;
    b = sx.first;

    edges.emplace(ob, b);
    if (is_branch) {
      blk_next_jump[last_branch] = ob;
      next_blk[last_branch].insert(b);
      par[b].insert(last_branch);
      if (b != ob + 3)
        conds[ob].second += 1;
      else
        conds[ob].first++;
      if (next[b] != -1) {
        cycle_t cur_cycle;
        int aa = b;
        while (aa != last_branch) {
          cur_cycle.pb(aa);
          int na = next[aa];
          next[aa] = -1;
          aa = na;
        }
        cur_cycle.pb(last_branch);
        cycle_counts[cur_cycle].push_back(cnt);
      } else {
        next[last_branch] = b;
      }

      last_branch = b;
    }

    if (FLAGS_stop_blk == b) break;
    if (x[4]) {
      printf("OUTPUTTING %03d %c %d %d\n", x[2] & 0xff, x[2] & 0xff, cnt,
             last_branch);
      OPA_DISP0(od.bseq.size());
      x[4] = 0;
      x[2] = 0;
      if (!FLAGS_simplequery) break;
    }
  }

  OPA_DISP0(cycle_counts.size());
  for (auto &e : cycle_counts) {
    if (e.second.size() < 50) continue;
    OPA_DISP0(e.first.size(), e.second.size());
    for (auto &p : e.first) printf("%d ", p);
    puts("");
  }

  OPA_DISP0(conds.size());

  for (auto &e : conds) {
    printf("Branch %d: %d %d ", e.first, e.second.first, e.second.second);
    if (e.second.first > 20 && e.second.second > 20) {
      printf(" SPLIT BRANCH");
    }
    if (std::max(e.second.first, e.second.second) > 0x1000)
      printf("LARGE POINT");
    else
      printf("SMALL");
    puts("");
  }

  for (auto &e : par) {
    printf("PAR %d >> ", e.first);
    for (auto &k : e.second) printf("%d ", k);
    puts("");
  }

  for (auto &e : next_blk) {
    printf("NXT %d >> ", e.first);
    for (auto &k : e.second) printf("%d ", k);
    puts("");
  }

  OPA_DISP0(reads.size());
  for (auto &e : reads) {
    if (e.second.size() == 1) continue;
    printf("READS %d %d ", e.first, e.second.size());
    if (e.second.size() <= 2) {
      for (auto &f : e.second) {
        printf(">> (%d %d)", f.first, f.second);
      }
    }
    puts("");
  }

  puts("BLK NExt JUMP");
  for (auto &e : blk_next_jump) {
    printf("%d >> %d\n", e.first, e.second);
  }

  puts("COUNT POS");
  for (auto &e : count_pos) {
    printf("%d >> %d\n", e.first, e.second);
  }
  OPA_DISP0(edges);
  od.taint = taint;
  od.ob = b;
  REP (i, NX)
    od.x = x;
}

OutData compute(const std::string &pwd, int stop_at = -1) {
  x = ix;
  OutData od;
  Ctrl ctrl;
  REP (i, pwd.size()) {
    x[g_bufstart + i] = pwd[i];
    ctrl.taint.insert(g_bufstart + i);
  }
  ctrl.stopaccess.insert(0x5c4d / 2);
  ctrl.dbg.insert(0x133d);

  if (stop_at >= 0) ctrl.stopaccess.insert(g_bufstart + stop_at);

  doit(ctrl, od);

  return od;
}

int main(int argc, char **argv) {
  opa::init::opa_init(argc, argv);
  OPA_CHECK0(FLAGS_infile.size() > 0);

  std::vector<std::vector<int> > seqs;
  std::vector<char> clist;

  std::ifstream ifs(FLAGS_infile, std::ios::binary);
  ifs.read((char *)ix.data(), NX * 2);

  std::string buf0(g_buflen, 'a');
  REP (i, 128) {
    if (!isprint(i) || i < 32) continue;
    OPA_DISP0(char(i), clist.size());
    clist.pb(i);
  }
  if (FLAGS_simplequery) {
    OutData od1 = compute(FLAGS_query, FLAGS_stop_at);
    if (FLAGS_outfile.size()) {
      std::ofstream ofs(FLAGS_outfile, std::ios::binary);
      ofs.write((char *)ix.data(), NX * 2);
    }

    return 0;
  }
  REP (i, FLAGS_query.size()) {
    if (i < g_buflen) buf0[i] = FLAGS_query[i];
  }

  FOR (pwdpos, FLAGS_query.size(), g_buflen) {
    printf("======== ON %d\n", pwdpos);
    std::vector<OutData> tmp;
    // clist = {'a', '0'};

    clist = { 0x20, 0x40, 0x41, 0x42, 0x44, 0x48 };
    for (auto &c : clist) {
      buf0[pwdpos] = c;
      OutData od1 = compute(buf0, pwdpos + 1);
      tmp.push_back(od1);
    }
    REP (i, clist.size() - 1) {
      printf("diff %x %x\n", clist[0], clist[i]);
      diff_mem_print(tmp[0].x, tmp[i + 1].x);
    }
    REP (i, clist.size()) {
      REP (j, i) {
        OPA_DISP("On exec ", i, j);
        diff_exec_print(tmp[i].bseq, tmp[j].bseq);
      }
    }
    break;

    opa::algo::UnionJoin uj(tmp.size());

    REP (i, tmp.size()) {
      REP (j, i) {
        if (tmp[i].bseq == tmp[j].bseq) uj.merge(i, j);
      }
    }
    for (auto &group : uj.get_groups()) {
      OPA_DISP0(group);
    }
    break;

    // break;
    // puts("----------------");
    // OutData od2 = compute(buf0);
    // diff_mem_print(od1.x, od2.x);
  }

  // return 0;

  /*
  REP (i, seqs.size())
    printf("%d : %c %d\n", i, clist[i], seqs[i].size());

  REP (a, seqs.size()) {
    REP (b, a) {
      int n = std::min(seqs[a].size(), seqs[b].size());
      bool diff = false;
      REP (j, n) {
        if (seqs[b][j] != seqs[a][j]) {
          diff = true;
          printf("%d %d diff at %d // %d xx %x %x\n", a, b, j, n, seqs[a][j],
                 seqs[b][j]);
          break;
        }
      }
      if (!diff) printf("NO DIFF %d %d\n", a, b);
    }
  }

  printf("%d\n", tainted_all.size());
  for (auto &x : tainted_all) {
    printf("%x\n", x);
  }

  puts("========= bvals");
  printf("%d\n", bvals.size());
  for (auto &x : bvals) {
    printf("%x\n", x);
  }

  puts("========= intersections");
  for (auto &x : bvals) {
    if (tainted_all.count(x)) printf("%x\n", x);
  }
  */

  return 0;
}
