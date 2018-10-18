#include <opa/crypto/la/algo.h>
#include <opa/crypto/la/blocks.h>
#include <opa/crypto/la/relation_driver.h>
#include <opa/crypto/stream/plan.h>
#include <opa/crypto/stream/solver.h>
#include <opa/crypto/stream/target.h>
#include <opa/math/common/Matrix.h>
#include <opa/math/common/algebra/basis.h>
#include <opa/math/common/fast_gf2.h>
#include <opa/math/common/stats.h>
#include <opa/threading/runner.h>
#include <opa/utils/csv.h>
#include <opa/utils/misc.h>
#include <opa_common.h>

using namespace std;
using namespace opa::crypto::stream;
using namespace opa::crypto::la;
using namespace opa::crypto;
using namespace opa::math::common;
using namespace opa::utils;

// clang-format off
std::vector<vi> tb = {{0, 64, 96, 128, 192, 255}, {0, 64, 96, 128, 192}, {0, 64, 96, 128}, {0, 64, 96, 192}, {0, 64, 128, 192, 255}, {0, 64, 192, 255}, {0, 64, 192}, {0, 64, 255}, {0, 96, 128, 192}, {0, 96, 128, 255}, {0, 96, 128}, {0, 96, 192}, {0, 128, 192, 255}, {0, 128, 192}, {0, 128, 255}, {0, 128}, {0, 192}, {0, 255}, {0}, {64, 96, 128, 192, 255}, {64, 96, 128, 192}, {64, 96, 192}, {64, 96, 255}, {64, 128}, {64, 192, 255}, {64, 192}, {64, 255}, {64}, {96, 128, 192, 255}, {96, 128, 255}, {96, 128}, {96, 192, 255}, {96, 192}, {96, 255}, {96}, {128, 192, 255}};
// clang-format on
const int n = 256;
const int M = 1001;
std::vector<int> expected;

std::vector<u32> used = { 0, 64, 96, 128, 192, 255 };

class TargetBlock : public CipherBlock {
public:
  mutable std::map<int, int> ids;

  virtual void init() {
    for (auto &x : tb)
      for (auto &a : x) {
        if (!ids.count(a)) ids[a] = ids.size();
      }
    int deg = ids.size();
    CipherBlock::init(Params()
                        .call(CallInfo(deg, 0, true))
                        .input_size(ids.size())
                        .output_size(1)
                        .fast_eval(true)
                        .rel_driver(new SimpleRelDriver(0.1, 100)));
    desc() = opa::utils::SPrintf("TargetBlock()");
  }

  virtual void do_evaluate(const BitVec &iv, const BitVec &kv,
                           BitVec &ov) const {
    OPA_CHECK0(false);
  }

  virtual void do_get_relations(Relations &rels) const {
    return get_relations_dumb(rels);
  }
  virtual void do_get_relations_diff(Relations &rels) const {
    OPA_CHECK0(false);
  }

  virtual void do_get_pre_fail(const Basis &out, Basis &res) const override {
    OPA_CHECK0(false);
  }

  virtual void setup_jit(const JitBuilder &builder) const override {
    OPA_CHECK0(false);
  }

  virtual u64 fast_eval1(u64 a) const override {
    int v = 0;
    for (auto &x : tb) {
      int term = 1;
      for (auto &pos : x) term &= (a >> ids[pos]) & 1;
      v ^= term;
    }
    return v;
  }
};

TargetBlock blk;

int eval1(const Poly<u32> &poly) {
  int v = 0;
  for (auto &e : blk.ids) v |= poly.get_safe(e.first) << e.second;
  return blk.fast_eval1(v);
}

void test1() {
  auto lfsr = LFSR<u32>();

  puts("test1");
  // x^256 + x^10 + x^5 + x^2 + 1
  std::vector<int> pwlist = { 0, 2, 5, 10, 256 };
  auto poly = PR_GF2.getZ();
  for (auto &pw : pwlist) poly = poly + PR_GF2.xpw(pw);
  OPA_DISP0(poly);

  OPA_DISP0(PR_GF2.factor(poly));

  auto rels = blk.get_relations();
  if (0) {
    std::string ol(64, 0);
    Poly<u32> base = PR_GF2.getE();
    lfsr.init(&GF2, base, poly);
    std::vector<u32> lst;
    REP (i, 512) {

      int x;
      int v;
      if (0) {
        x = eval1(lfsr.get_state());
        x = lfsr.get_state().get_safe(0);
        v = lfsr.get_next_non_galois_gps_style();
      } else {
        std::vector<u32> nstate(256);
        v = base.get_safe(0);
        auto nbase = base;
        if (v) nbase = nbase + poly;
        REP (i, 255)
          nstate[i] = nbase.get_safe(i + 1);
        base = PR_GF2.import(nstate);
      }
      ol[i / 8] |= v << (i % 8);
    }
    std::reverse(ALL(ol));
    // 4840000000000000000000000000000000000001484000014840000000000001000000000000000000000000000000000000000100000001
    // 00 00 00 00 00 00 00 01
    std::string want =
      "484000000000000148400001484000000000000000000000000000000000000100000000"
      "00000001000000010000000000000000000000000000000000000001";

    std::string want_bin = opa::utils::h2b(want);

    std::vector<u32> seq;
    REPV (i, want_bin.size()) {
      REP (j, 8)
        seq.push_back(want_bin[i] >> j & 1);
    }

    if (0) {
      std::string target =
        "31018c85020813093200c6ae4822e400261853722f054a1e0805600340086050803808"
        "10640342825506829c0209a041340101b54f1848425aa208035d40510068044597575a"
        "02b115a9002436958884d110a2515022240aec060e0a0200c4296081062829a0032825"
        "0210001533404b206301482800234000501d0104";
      std::string target_bin = opa::utils::h2b(target);
      std::reverse(ALL(target_bin));
      std::vector<u32> nseq;
      for (auto &c : target_bin) {
        REP (i, 8)
          nseq.push_back(c >> i & 1);
      }

      auto nlfsr = LFSR<u32>();
      OPA_CHECK0(nlfsr.init_from_seq(&GF2, nseq));
      OPA_DISP0(nlfsr.size(), nseq.size());
      REP (i, 200)
        OPA_DISP0(i, nlfsr.get_next_non_galois_gps_style(), seq[i]);
      OPA_DISP0(nlfsr.get_poly());
      return;
    }

    // 00000000000000000000000148400001484000000000000100000000000000000000000000000000000000000000000000000001000000010000000000000001
    std::string have = opa::utils::b2h(ol);
    REPV (i, 64)
      printf("%02x %c%c %c%c\n", 63 - i, want[2 * i], want[2 * i + 1],
             have[2 * i], have[2 * i + 1]);
    OPA_DISP0(want);
    OPA_DISP0(have);
    return;
    std::reverse(ALL(lst));

    auto nlfsr = LFSR<u32>();
    nlfsr.init_from_seq(&GF2, lst);
    OPA_DISP0(nlfsr.get_poly());
    return;
  }

  OPA_DISP0(rels);
  REP (i, 1 << blk.ids.size()) { OPA_DISP0(i, blk.fast_eval1(i)); }

  std::vector<std::vector<std::vector<vi> > > terms(M);
  REP (i, M) {
    REP (j, tb.size()) {
      terms[i].emplace_back();
      terms[i][j].resize(tb[j].size());
    }
  }

  std::vector<std::vector<BitVec> > decomp(M);
  REP (i, M) { decomp[i].resize(used.size(), BitVec(n)); }

  OPA_DISP0(blk.ids);

  REP (p, n) {
    lfsr.init(&GF2, PR_GF2.xpw(p), poly);
    REP (i, M) {
      auto vals = lfsr.get_state();
      lfsr.get_next_non_galois2();
      REP (j, used.size())
        decomp[i][j].set(p, vals.get_safe(used[j]));

      // lfsr.get_next();
    }
  }

  std::vector<BitVec> eqs;
  REP (i, M) {
    if (!(expected[i] & 1)) continue;
    BitVec cur(n);
    REP (j, used.size())
      cur.sxorz(decomp[i][j]);
    eqs.push_back(cur);
  }
  //FILE *fx = fopen
  OPA_DISP0(eqs.size());
  REP (i, eqs.size()) {
    printf("[");
    REP (j, n)
      printf("%d,", eqs[i].get(j));
    printf("],\n");
  }
  // MulMatrixF2<true> mat;
  // mat.init(M,n);
  // REP(i,M){
  //  REP(j,n) mat.set(i,j, eqs[i].get(j));
  //}

  return;

  std::set<std::vector<int> > entries;
  REP (i, M) {
    for (auto &b : terms[i]) {
      for (auto &c : b) {
        std::sort(ALL(c));
        OPA_CHECK0(c.size() > 0);
        entries.insert(c);
      }
    }
    OPA_DISP0(i, entries.size());
  }
  puts("FINAL");
  OPA_DISP0(entries.size());
}

void solve_real() {
  std::string want =
    "484000000000000148400001484000000000000000000000000000000000000100000000"
    "00000001000000010000000000000000000000000000000000000001";

  std::string want_bin = opa::utils::h2b(want);
  std::reverse(ALL(want_bin));

  std::vector<u32> seq;
  REP (i, want_bin.size()) {
    REP (j, 8)
      seq.push_back(want_bin[i] >> j & 1);
  }

  auto lfsr = LFSR<u32>();

  puts("test1");
  // x^256 + x^10 + x^5 + x^2 + 1
  // std::vector<int> pwlist = {0, 160, 192, 256};
  std::vector<int> pwlist = { 0, 2, 5, 10, 256 };
  auto poly = PR_GF2.getZ();
  for (auto &pw : pwlist) poly = poly + PR_GF2.xpw(pw);
  OPA_DISP0(poly);

  std::vector<u32> output;
  lfsr.init(&GF2, PR_GF2.xpw(0), poly);
  REP (i, n) { output.pb(lfsr.get_next_v2()); }

  auto poly2 = PR_GF2.getZ();
  for (auto &pw : pwlist) poly2 = poly2 + PR_GF2.xpw(256 - pw);

  std::vector<u32> output2;
  lfsr.init(&GF2, PR_GF2.xpw(0), poly);
  REP (i, 2 * n) {
    output2.pb(lfsr.get_next_v2());
    OPA_DISP0(lfsr.get_state());
  }
  REP (i, output2.size()) { printf("%d %d %d\n", i, output2[i], seq[i]); }
  return;

  PolyModField<u32> pmf;
  pmf.init(&GF2, poly);
  auto o1 = pmf.import(output);
  auto o2 = pmf.import(output2);
  auto o3 = pmf.div(o2, o1);

  std::vector<u32> output3;
  lfsr.init(&GF2, PR_GF2.import(o3), poly);
  REP (i, n) { output3.pb(lfsr.get_next_non_galois()); }
  OPA_DISP0(pmf.mul(o1, o3) - o2);
  REP (i, n) {
    printf("%d %d %d %d\n", output[i], output3[i], output2[i], seq[i]);
  }
}
void checkit() {
  std::vector<u32> ans = {
    0, 1, 0, 1, 0, 1, 1, 0, 0, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1,
    1, 0, 0, 1, 1, 0, 0, 1, 0, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 0, 1, 0, 1, 1,
    0, 1, 0, 0, 1, 1, 1, 1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 0,
    0, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 0, 0, 1, 1, 1, 0, 1, 1, 0, 0, 1, 1, 0,
    1, 0, 1, 0, 0, 1, 1, 0, 1, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 1, 1, 1, 0, 0,
    1, 1, 0, 0, 1, 1, 0, 1, 0, 0, 1, 0, 1, 0, 1, 1, 0, 0, 1, 1, 1, 1, 0, 1,
    0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1, 1, 0, 0, 1, 0, 1, 0, 0, 0, 1,
    1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 0, 0, 1, 1, 1, 0, 1, 1, 0,
    0, 0, 1, 1, 1, 1, 0, 1, 0, 0, 0, 1, 1, 0, 0, 0, 1, 0, 1, 1, 1, 0, 0, 1,
    1, 1, 1, 1, 0, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 1, 0, 1, 0, 0, 0,
    1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 1, 0, 1, 0, 0
  };
  REP (i, 64)
    printf("%d %d\n", i, (int)blk.fast_eval1(i));
  puts("");

  std::vector<int> pwlist = { 0, 2, 5, 10, 256 };
  auto poly = PR_GF2.getZ();
  for (auto &pw : pwlist) poly = poly + PR_GF2.xpw(pw);

  auto lfsr = LFSR<u32>();
  lfsr.init(&GF2, PR_GF2.import(ans), poly);
  lfsr.init(&GF2, PR_GF2.xpw(0), poly);

  std::vector<u32> seq;
  REP (i, M) {
    int g = 1;
    REP (j, used.size())
      g ^= lfsr.get_state().get_safe(used[j]);
    int x = eval1(lfsr.get_state());
    int v = lfsr.get_next_non_galois2();
    seq.push_back(v);
    if (v) {
      printf("%d %d %d %d %d\n", v, x, expected[i], x * g, i);
    }
  }
  auto nlfsr = LFSR<u32>();
  OPA_CHECK0(nlfsr.init_from_seq(&GF2, seq));
  OPA_DISP0(nlfsr.get_poly());
}

void gen() {
  std::vector<int> pwlist = { 0, 2, 5, 10, 256 };
  auto poly = PR_GF2.getZ();
  std::string key = "flag{abcdef jambon kapa lala";
  key.resize(32, 'x');
  key[31] = '}';
  OPA_DISP0(key);
  std::vector<u32> keyb;
  REP (i, key.size() * 8) { keyb.push_back(key[i >> 3] >> (i & 7) & 1); }
  for (auto &pw : pwlist) poly = poly + PR_GF2.xpw(pw);

  auto lfsr = LFSR<u32>();
  lfsr.init(&GF2, PR_GF2.import(keyb), poly);
  std::vector<u32> res;
  REP (i, M) {
    res.pb(eval1(lfsr.get_state()));
    lfsr.get_next_non_galois2();
  }
  std::string ress((M + 7) / 8, 0);
  REP (i, M) { ress[i / 8] |= res[i] << (i & 7); }
  OPA_DISP0(opa::utils::b2h(ress));
  OPA_DISP0(key);
}

int main(int argc, char **argv) {
  opa::init::opa_init(argc, argv);
  blk.init();
  if (1) {
    opa::threading::Runner::EasySetup();
  }

  std::string res_bin;

  if (0) {
    std::string res_hex = "0131018c85020813093200c6ae4822e400261853722f054a1e08"
                          "0560034008605080380810"
                          "640342825506829c0209a041340101b54f1848425aa208035d40"
                          "510068044597575a02b115"
                          "a9002436958884d110a2515022240aec060e0a0200c429608106"
                          "2829a00328250210001533"
                          "404b206301482800234000501d0104";
    res_bin = opa::utils::h2b(res_hex);
    std::reverse(ALL(res_bin));
  } else {
    res_bin = opa::utils::h2b("64210040030344204d5248602a2018430000402803002218c415c112b20151870800ad01d0321a51042200038421086423c022082aa820880a30098281119380a920e6427680b805410e012001420514090080840067680000474b28be21c93a6d35b801023248881891228e4183511e1004205030830002525900394200");
  }
  int cnt = 0;

  REP (i, M) {
    expected.push_back(res_bin[i >> 3] >> (i & 7) & 1);
    cnt += expected.back();
  }
  OPA_DISP0(cnt);

  int typ = 1;
  if (typ == 0) {
    checkit();
  } else if (typ == 1) {
    test1();
  } else if (typ == 2) {
    gen();
  } else {
    solve_real();
  }

  return 0;
}
