#include <opa_common.h>
#include <opa/math/common/Utils.h>
#include <opa/math/common/rng.h>
#include <opa/math/common/Matrix.h>
#include <opa/math/common/GF_p.h>
#include <opa/math/common/algo.h>
#include <opa/utils/misc.h>
#include <opa/crypto/la/misc.h>
#include <opa/crypto/la/context.h>
#include <opa/crypto/la/graph.h>
#include <opa/crypto/la/feistel.h>
#include <opa/crypto/la/tester.h>
#include <opa/crypto/la/des.h>
#include <opa/threading/runner.h>
#include <opa/crypto/la/feistel_linear_driver.h>
#include <opa/crypto/la/feistel_diff_driver.h>

using namespace asmjit;
using namespace opa::crypto::la;

using namespace opa::math::common;
using namespace opa::utils;
using namespace std;

void test_rels() {
  // SboxBlock blk;
  // blk.init(SboxDesc::Rand(3, 2));
  AddBlock blk;
  blk.init(3);
  const auto &rels = blk.get_relations(true);
  OPA_DISP0(rels);
  exit(0);
}

void go() {
  // test_rels();

  // TODO: GraphRelStorer should take input from RelationDriver
  // TODO: In feistel, maybe allow more than one rel per step
  opa::threading::Runner runner;
  CipherContext *ctx = CipherContext::singleton.get();

  if (0) {
    runner.run_both();
    ctx->dispatcher = runner.dispatcher();
  }

  vector<u16> keys;
  keys.pb(0xabcd);
  keys.pb(0x1235);
  keys.pb(0x8422);
  keys.pb(0xeeff);
  keys.pb(0xdd22);
  keys.pb(0);

  if (0) {
    auto blk = ctx->instanciate<FealFBoxBlockN<16> >();
    blk->init();
    const auto &rels = blk->get_relations(true);
    OPA_DISP0(rels);

    Relation rel;
    rel.in = { 0xb, 0xf };
    rel.out = { 0x2 };
    blk->test_rel(100, rel.in, rel.out, true);
    // x=r.in=r.m_cover=(0,10,),,r.out=r.m_cover=(8,f,),,r.c=0,r.cost=r.m_prob=1,,,
    //  x=r.in=r.m_cover=(4,14,),,r.out=r.m_cover=(7,b,f,),,r.c=0,r.cost=r.m_prob=1,,,
    //  x=r.in=r.m_cover=(8,18,),,r.out=r.m_cover=(3,4,7,8,),,r.c=0,r.cost=r.m_prob=1,,,
    //  x=r.in=r.m_cover=(c,1c,),,r.out=r.m_cover=(3,4,),,r.c=0,r.cost=r.m_prob=1,,,

    return;
  }

  ctx->is_debug() = false;
  constexpr int BLK_SIZE = 16;
  typedef FealFBoxBlockN<BLK_SIZE> TARGET;
  SPTR(TARGET) blk = ctx->instanciate<TARGET>();
  blk->init();
  SPTR(FeistelBlock) blk2 = ctx->instanciate<FeistelBlock>();
  int nround = 4;
  blk2->init(FeistelBlock::Params(blk, nround, false /* mid_xor */));

  blk->driver()->to_simple()->thresh() = 1;
  blk2->driver()->to_simple()->thresh() = 1;
  blk2->build();

  for (auto &e : blk->get_input_relations().tb) {
    OPA_DISP("For rel ", e);
    blk->test_rel(100, e.in, e.out);
  }

  if (1) {

    const auto &diff_rels = blk->get_relations(true);
    OPA_DISP0(diff_rels);

    FeistelDiffSolver solver;
    solver.init(blk2.get());
    const FeistelSolver::RequiredData &required_data =
      solver.first_phase_find_rels();

    for (auto &per_round : required_data.data_per_round) {
      puts("PER ROUND ");

      for (auto &rel : per_round.rels) {
        u64 diff = (rel.l + rel.r.shift(BLK_SIZE)).to<u64>();
        OPA_DISP0(diff);
        OPA_DISP("test rel >> ", solver.test_r2(100, rel, true));
      }
    }
    RequiredDiffs diffs = solver.required_data_to_diffs(required_data);
    CipherData cipher_data;
    BitVec kv = BitVec::rand(blk2->key_size());
    diffs.gen_cipher_data(kv, blk2.get(), &cipher_data);
    FeistelSolverResult result;
    ctx->target_key = kv;
    OPA_DISP0(cipher_data.x_diff.size());
    puts("START SEcond phASE, wnat");
    OPA_DISP0(ctx->target_key);

    solver.second_phase_entry(cipher_data, &result);
    OPA_DISP0(opa::utils::Join("\n", result.keys));
    OPA_CHECK0(result.keys.size() > 0);
    OPA_DISP0(kv, kv.to<u64>());

    BitVec found_key = result.keys[0];
    OPA_DISP0("FOUND KEY KAPPA ", found_key, kv==found_key);
    OPA_CHECK0(blk2->verify_data(cipher_data, found_key));

    return;
  }

  if (1) {
    BitVec kv = BitVec::rand(blk2->key_size());
    // kv.copy(BitVec(blk2->blk_size()*2), blk2->blk_size());
    int ndata = 200;
    // OPA_DISP0(blk->fast_eval2(0, 0x277e));
    // OPA_DISP0(blk->fast_eval2(0, 0x27f6));
    // return;
    // ur[i]=a.round=c,a.vbase=dbc2,a.vkey=277e,a.cost=1,,
    //  i=1,cur[i]=a.round=c,a.vbase=5bc2,a.vkey=27f6,a.cost=1,,
    ctx->target_key = kv;

    CipherData data = blk2->gen_rand(ndata, kv);
    OPA_DISP0(data.x[0].first.n, data.x[0].second.n);
    CipherData test_data;
    blk2->undo_last_round(data, kv.extract(0, blk2->blk_size()), &test_data);
    for (auto &e : test_data.x) {
      OPA_DISP0(e.first, e.second, e.first.xorz(e.second));
    }
    OPA_DISP0(kv, kv.to<u64>());

    FeistelLinearSolver solver;
    solver.init(blk2.get());
    FeistelSolverResult res = solver.solve(data);
    OPA_DISP0(opa::utils::Join("\n", res.keys));
    OPA_CHECK0(res.keys.size() > 0);
    OPA_DISP0(kv, kv.to<u64>());

    BitVec found_key = res.keys[0];
    OPA_CHECK0(blk2->verify_data(data, found_key));
    OPA_DISP("Verification succeeded", data.x.size(), data.x_diff.size());

    return;
  }

  if (0) {
    const auto &rels = blk->get_relations(true);
    OPA_DISP0(rels);
    return;
    // blk->test_rel(1e4, { 0x14, 0x3f }, { 0xa, 0x12, 0x1c });
  }

  if (1) {
    Relation rel;
    rel.in = { 0, 0x10 };
    rel.out = { 0x8, 0xf };
    blk->test_rel(1000, rel.in, rel.out, true);
    // x=r.in=r.m_cover=(0,10,),,r.out=r.m_cover=(8,f,),,r.c=0,r.cost=r.m_prob=1,,,
    //  x=r.in=r.m_cover=(4,14,),,r.out=r.m_cover=(7,b,f,),,r.c=0,r.cost=r.m_prob=1,,,
    //  x=r.in=r.m_cover=(8,18,),,r.out=r.m_cover=(3,4,7,8,),,r.c=0,r.cost=r.m_prob=1,,,
    //  x=r.in=r.m_cover=(c,1c,),,r.out=r.m_cover=(3,4,),,r.c=0,r.cost=r.m_prob=1,,,

    return;
  }

  blk->verify();
  int nr = 1e6;
  Value kv = Value::Rand(blk2->key_size());
  u64 target_key = kv.get(blk->key_size() * (nround - 1)).to<u64>();
  OPA_DISP("WANT KEY >> ", target_key);
  ctx->target_key = target_key;
  // 13498fbbac,-> 4
  // f70db07d9e27, -> 5
  // 9e270afd8f09, 6

  // FeistelDiffSolver solver;
  // solver.init(blk2.get(), true);
  // RequiredData required_data = solver.first_phase_find_rels();
  // RequiredDiffs required_diffs =
  // solver.required_data_to_diffs(required_data);

  // CipherData data;
  // solver.second_phase_find_keys(data);
}

int main(int argc, char **argv) {
  opa::init::opa_init(argc, argv);
  srand(0);
  go();

  return 0;
}
