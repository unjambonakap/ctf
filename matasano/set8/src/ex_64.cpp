#include "matasano/ex_64.h"
#include <opa/math/common/GF_p.h>
#include <opa/math/common/GF_q.h>
#include <opa/math/common/Matrix.h>
#include <opa/math/common/Poly.h>
#include <opa/math/common/PolyRing.h>
#include <opa/math/common/base/range_coverage.h>
#include <opa/math/common/base/value.h>
#include <opa/math/common/rng.h>
#include <opa/utils/string_builder.h>
#include <opa/utils/string.h>

using namespace opa::math::common;
using namespace opa::crypto;
using namespace std;
using namespace opa::utils;

OPA_NAMESPACE(matasano)

namespace {
const int maxb = 1 << 16;
u8 cnt_bit[maxb];

inline int get_cnt_bit64(u64 a) {
  return cnt_bit[a & 0xffff] ^ cnt_bit[a >> 16 & 0xffff] ^
         cnt_bit[a >> 32 & 0xffff] ^ cnt_bit[a >> 48 & 0xffff];
}

void init_bitstuff() {
  cnt_bit[0] = 0;
  FOR(i, 1, maxb) { cnt_bit[i] = 1 ^ cnt_bit[i & i - 1]; }
}

OPA_REGISTER_INIT(init_bitstuff, init_bitstuff);
}

/*
   want sum(di*h^i)=0
   di=0 if i!=2^k
   Mi -> vector repr of di
   Ai -> vector repr of fi(x) = x^2^i
   -> sum(Mi*Ai)*h=B*h=0
   Mij -> sum(Mj*dij)

   B=sum_i,j((Mj*dij)*Ai)
   B=sum_k(Ck), k in {0,127}*{1,log2(n)}
   B -> M_b,128
   b -> num of bits kept from tag

   can represent Ck as a single row, concat of all others

   d0=0
   find B with max number of null rows

   oracle tells if message passed auth
   zeroed out k rows in B
   b-k rows non zero
   if yes, B*h = 0 -> new linear rels for h

   these rels help us improve forgery?
   only send requests where at least one non zero row in B
   if only one non zero row sent and wrong answer, it is a valid new rel for
   h

*/

class GcmOracle {
 public:
  struct Params {
    AesGcm target;
    RangeCoverage output_bits;
  };

  void init(const Params &params) {
    m_params = params;
    nonce = m_params.target.get_nonce();
  }

  bool query(StringRef data, StringRef tag) {
    // OPA_DISP0(b2h(shorten_tag(tag)), b2h(get_shortened_tag(data)));
    return get_shortened_tag(data) == shorten_tag(tag);
  }

  std::string get_shortened_tag(StringRef data) {
    m_params.target.prepare_from_data(data, nonce);
    std::string full_tag = m_params.target.get_tag();
    return shorten_tag(full_tag);
  }

  std::string shorten_tag(StringRef tag) {
    return Value::FromBytes(m_params.output_bits, tag).to_bytes();
  }

  Params m_params;
  std::string nonce;

 private:
};

class BSGS {
 public:
  void init(int size) {
    size_low = sqrt(size);

    {
      Gf128_t cur = gf128.getE();
      Gf128_t small_step = gf128.pr().x();
      REP(i, size_low) {
        low.pb(cur);
        cur = cur * small_step;
      }
    }

    {
      Gf128_t cur = gf128.getE();
      Gf128_t large_step = gf128.pr().x().powm(size_low);
      REP(i, size / size_low + 1) {
        high.pb(cur);
        cur = cur * large_step;
      }
    }
  }

  Gf128_t get(int x) { return low[x % size_low] * high[x / size_low]; }

  std::vector<Gf128_t> low, high;
  int size_low;
};

class Solver {
 public:
  struct Params {
    std::string data;
    GcmOracle oracle;
    RangeCoverage output_bits;
    std::string tag;
  };

  void init(const Params &params) {
    m_params = params;
    int nblocks = m_params.data.size() * 8 / 128;
    logv = log2_high_bit(nblocks);
    OPA_CHECK0(logv >= 0);
    // skipping h^2^0 val
    puts("Start init solver");

    std::vector<MulMatrixF2<true>> d_mat(n);
    MulMatrixF2<false> pw_mat;
    pw_mat.init(n, n);

    BSGS bsgs;
    bsgs.init((1 << (logv - 1)) * n);
    puts("bsgs done");
    obits = params.output_bits.to_vec();
    REP(i, n) {
      Gf128_t cur = gf128.pr().x().powm(i);
      d_mat[i].init(n, n);
      REP(j, n) {
        d_mat[i].set_col(j, cur.toVector(n));
        cur = cur * gf128.pr().x();
      }
    }
    OPA_DISP0(logv);
    int nmat = (logv - 1) * n;
    mats.resize(nmat);

    change_id.clear();

    FOR(i, 1, logv) {
      int pw_val = 1 << i;
      change_id.pb(nblocks - pw_val);
      REP(j, n) {
        Gf128_t cur_pw = bsgs.get(j * pw_val);
        pw_mat.set_col(j, cur_pw.toVector(n));
      }

      if (0) {
        REP(k, 100) {
          auto u = gf128.getRand();

          Gf128_t2 res;
          pw_mat.eval(to_gf128_t2(u), res);
          OPA_CHECK0(u.powm(pw_val) == to_gf128_t(res));
        }

        exit(0);
      }

      REP(k, n) {
        // OPA_DISP("on ", i, logv, k);

        auto tmp = mul(d_mat[k], pw_mat);
        mats[(i - 1) * n + k] = tmp.extract_rows(obits);
      }
    }
    puts("done init");
  }

  void do_test() {
    auto &target = m_params.oracle.m_params.target;
    auto oh = target.get_h();
    Gf128_t h = to_gf128_t(oh);
    REP(i, mats.size()) {
      int pw = 1 << (1 + i / 128);
      auto hpw = h.powm(pw);

      std::string buf = m_params.data;
      u64 *tb = (u64 *)&buf[0];
      int pos = change_id[i / 128] * 128 + (i & 127);
      tb[pos / 64] ^= 1ull << (pos & 0x3f);
      target.prepare_from_data(buf, m_params.oracle.nonce);
      auto tag = target.get_tag();

      Gf128_t2 res;
      auto tmpm = mats[i].copy<false>();
      tmpm.eval(target.get_h(), res);
      auto tmpv = hpw * gf128.pr().xpw(i & 127);

      REP(j, 128) {
        int x1 = GETB(tag, j);
        int x2 = GETB(m_params.tag, j);
        int change = GETB(res, j);
        // OPA_DISP0(pos, i, j, x1, x2, change, res[0], res[1]);
        OPA_CHECK0(change == tmpv.get_safe(j));
        OPA_CHECK0(x1 == x2 ^ change);
      }
    }
  }

  void go() {
    if (0) {
      puts("GO TEST");
      do_test();
      puts("DoNe TEST");
    }
    /*
another way to reduce the number of columns: ignore h_i for some i.
If h_i != 0, oracle would say yes with low probability.
If h_i = 0, then ignoring it does not change success prob
*/

    MulMatrixF2<true> rels;
    rels.init(0, 0);

    MulMatrixF2<false> kernel_basis;
    kernel_basis.init(n, n);
    REP(i, n) kernel_basis.set(i, i, 1);

    vector<MulMatrixF2<true>> cur_mats(mats.size());

    while (true) {
      // too lazy to do obits.size() choose logv-1, random will do
      vector<int> perm;
      REP(i, obits.size()) perm.pb(i);
      REP(i, mats.size()) {
        cur_mats[i] = mul(mats[i], kernel_basis);
        //  cur_mats[i] = mats[i];
      }
      int input_dim = cur_mats[0].M;

      random_shuffle(ALL(perm));
      // want mats.size() > kernel_basis.M*take + 1
      // take = floor((mats.size()-1)/kernel_basis.M
      int take = (mats.size() - 1) / input_dim;
      take = min(take, int(perm.size() - 1));
      OPA_DISP0(take);

      int lastc = take * input_dim + 63 & ~63;
      MulMatrixF2<true> m;
      m.init(mats.size(), lastc + mats.size());
      memset(&m.tb[0], 0, sizeof(u64) * m.tb.size());
      OPA_DISP0(perm);
      REP(j, mats.size()) {
        REP(i, take) {
          REP(k, input_dim) m.set(j, i * input_dim + k,
                                  cur_mats[j].get(perm[i], k));
        }
        m.set(j, lastc + j, 1);
      }

      if (0) m.disp();

      OPA_DISP0(m.N, m.M);
      int lastr = m.reduce(lastc);
      int rem = m.N - lastr;
      OPA_DISP0(rem, lastr, m.N);
      OPA_CHECK0(lastr != -1);
      rem = min(rem, 30);

      Gf128_t cur = gf128.getZ();
      OPA_DISP0(rem, input_dim);

      FOR(mask_, 1, 1 << rem) {
        if (mask_ % 100 == 0) OPA_DISP0(mask_);
        int mask = rng() % (1 << rem);

        std::string buf = m_params.data;
        u64 *tb = (u64 *)&buf[0];

        auto m1 = MulMatrixF2<true>();
        const bool test_m1 = (mask_ % 1000 == 0) && 0;
        if (test_m1) {
          m1.init(obits.size(), 128);
        }

        REP(j, rem) {
          if (!(mask >> j & 1)) continue;
          if (test_m1) {
            FOR(k, lastc, m.M) {
              if (m.get(lastr + j, k)) {
                m1 = add(m1, mats[k - lastc]);
              }
            }
          }

          for (int p = lastc, pos = 0; p < m.M; p += 64, ++pos)
            tb[2 * change_id[pos / 2] + (pos & 1)] ^=
                m.tb[m.get_id(lastr + j, p)];
        }
        // OPA_CHECK0(buf != m_params.data);

        if (test_m1) {
          mul(m1, kernel_basis).disp();
        }
        bool ans = false;
        ans = m_params.oracle.query(buf, m_params.tag);
        if (ans) {

          if (test_m1) {
            m1.disp();
            REP(i, obits.size()) {
              printf("%d >> %d: ", i, perm[i]);
              REP(j, 128) printf("%d", m1.get(perm[i], j));
              puts("");
            }
            out(perm);

            out(tb + change_id.back() - 10, 10);
          }

          // contains changed bits
          MulMatrixF2<true> set_bits;
          set_bits.init(1, mats.size());

          REP(j, rem) {
            if (mask >> j & 1) {
              REP(p, mats.size())
              if (m.get(lastr + j, lastc + p)) set_bits.toggle(0, p);
            }
          }

          MulMatrixF2<true> new_rel;
          {
            new_rel.init(obits.size(), n);
            REP(i, mats.size()) {
              if (!set_bits.get(0, i)) continue;
              auto tmp = mats[i].extract_rows(perm);
              new_rel.sadd(tmp);
            }

            if (0) {
              auto checkm = new_rel.copy<false>();
              auto checkv = m_params.oracle.m_params.target.get_h();

              MulMatrixF2<true> checkvm;
              checkvm.init_from_gf128_t2(checkv);
              auto resv2 = new_rel.eval_all(checkvm);

              Gf128_t2 resv;
              checkm.eval(checkv, resv);

              resv2.disp();
              OPA_DISP0(resv[0], resv[1]);
              REP(i, obits.size()) {
                OPA_DISP0(GETB(resv, i), resv2.get(i, 0));
                OPA_CHECK0(GETB(resv, i) == resv2.get(i, 0));
              }

              // REP(i, take) { OPA_CHECK0(resv2.get(perm[i], 0) == 0); }

              REP(i, obits.size()) {
                OPA_CHECK0(GETB(resv, i) == 0);
                OPA_CHECK0(resv2.get(i, 0) == 0);
              }
            }

            MulMatrixF2<true> old_rels = rels;
            rels.init(old_rels.N + obits.size(), n);
            OPA_DISP0(old_rels.N, old_rels.M, n);
            REP(i, old_rels.N) REP(j, n) rels.set(i, j, old_rels.get(i, j));

            REP(i, obits.size()) {
              REP(j, n) rels.set(old_rels.N + i, j, new_rel.get(i, j));
            }
          }

          {
            kernel_basis = rels.get_kernel_basis();
            int nrows = rels.M - kernel_basis.M;
            rels.set_num_rows(nrows);
            rels.disp();
            OPA_DISP0("CUR bASIS >> ", kernel_basis.N, kernel_basis.M);
            if (kernel_basis.M == 1) {
              puts("WE ARE DONE");
              found_h = kernel_basis.get_col(0);
              return;
            }

            /*
            auto res = mul(tmp, kernel_basis);
            kernel_basis.disp();
            puts("");
            res.disp();
            res is null mat
            */

            if (0) {
              auto checkv = m_params.oracle.m_params.target.get_h();
              MulMatrixF2<true> checkvm;
              checkvm.init_from_gf128_t2(checkv);
              auto resv = rels.eval_all(checkvm);
              REP(i, resv.N) OPA_CHECK0(resv.get(i, 0) == 0);
            }

            OPA_DISP0(mask_);
            puts("GOT ONE");
            break;
          }
        }
      }
    }
  }
  std::vector<int> found_h;

 private:
  const int n = 128;
  std::vector<int> obits;
  std::vector<int> change_id;
  int logv;
  Params m_params;
  std::vector<MulMatrixF2<true>> mats;
};

void ex_64() {
  AesGcm target(StringBuilder()
                    .add("Je suis un jambon")
                    .pad('a', AesGcm::blk_size)
                    .get());
  target.prepare("", Rng2::get()->bytes((1 << 17) * 16 + 32),
                 Rng2::get()->bytes(12));

  RangeCoverage output_bits = RangeCoverage().add_interval(0, 32);

  GcmOracle oracle;
  oracle.init({target, output_bits});
  std::string data = target.get_data();
  std::string tag = target.get_tag();

  Solver solver;
  solver.init({data, oracle, output_bits, tag});
  //OPA_CHECK0(oracle.query(data, tag));
  solver.go();

  auto ans_h = bits_to_vec(target.get_h(), 128);

  OPA_DISP0(solver.found_h, ans_h);
  OPA_CHECK0(solver.found_h == ans_h);
}

OPA_NAMESPACE_END(matasano)
