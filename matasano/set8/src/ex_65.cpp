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

const int LOG_BLOCKS = 4;
namespace {
const int maxb = 1 << 16;
u8 cnt_bit[maxb];

inline int get_cnt_bit64(u64 a) {
  return cnt_bit[a & 0xffff] ^ cnt_bit[a >> 16 & 0xffff] ^
         cnt_bit[a >> 32 & 0xffff] ^ cnt_bit[a >> 48 & 0xffff];
}

void init_bitstuff() {
  cnt_bit[0] = 0;
  FOR (i, 1, maxb) { cnt_bit[i] = 1 ^ cnt_bit[i & i - 1]; }
}

OPA_REGISTER_INIT(init_bitstuff, init_bitstuff);

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
    bool padding_ok =
      m_params.target.prepare_from_data_check_padding(data, nonce);
    if (!padding_ok) {
      OPA_CHECK0(false);
      return "sure, you fool";
    }

    if (data.size() / 16 > (1 << (LOG_BLOCKS + 1))) {
      OPA_CHECK0(false);
      return "arbitrary size limit, because I like it.";
    }
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
      REP (i, size_low) {
        low.pb(cur);
        cur = cur * small_step;
      }
    }

    {
      Gf128_t cur = gf128.getE();
      Gf128_t large_step = gf128.pr().x().powm(size_low);
      REP (i, size / size_low + 1) {
        high.pb(cur);
        cur = cur * large_step;
      }
    }
  }

  Gf128_t get(int x) { return low[x % size_low] * high[x / size_low]; }

  std::vector<Gf128_t> low, high;
  int size_low;
};

vector<int> get_sol(const MulMatrixF2<true> &m, const MulMatrixF2<true> &vec) {
  vector<int> sol;
  // want: m'*X =vec
  MulMatrixF2<true> m2;
  m2.init(m.M, m.N);
}

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

    logv = LOG_BLOCKS + 1;
    nblocks = (1 << logv);
    // skipping h^2^0 val
    puts("Start init solver");
    OPA_DISP0(nblocks);

    std::vector<MulMatrixF2<true> > d_mat(n);
    MulMatrixF2<false> pw_mat;
    pw_mat.init(n, n);

    BSGS bsgs;
    bsgs.init((1 << (logv - 1)) * n);
    puts("bsgs done");
    obits = params.output_bits.to_vec();
    REP (i, n) {
      Gf128_t cur = gf128.pr().x().powm(i);
      d_mat[i].init(n, n);
      REP (j, n) {
        d_mat[i].set_col(j, cur.toVector(n));
        cur = cur * gf128.pr().x();
      }
    }

    OPA_DISP0(logv);
    int nmat = (logv - 1) * n;
    mats.resize(nmat);

    change_id.clear();

    REP (i, logv) {
      int pw_val = 1 << i;
      if (i > 0)
        change_id.pb(nblocks - pw_val);
      REP (j, n) {
        Gf128_t cur_pw = bsgs.get(j * pw_val);
        pw_mat.set_col(j, cur_pw.toVector(n));
      }

      REP (k, n) {
        // OPA_DISP("on ", i, logv, k);

        auto tmp = mul(d_mat[k], pw_mat).extract_rows(obits);
        if (i == 0) {
          size_block_mats.pb(tmp);
        } else {
          mats[(i - 1) * n + k] = tmp;
        }
      }
    }
    puts("done init");
    int target_size = nblocks * AesGcm::blk_size;
    forge_data = StringBuilder()
                   .pad(0, target_size - m_params.data.size())
                   .add(m_params.data)
                   .get();
  }

  void go() {

    MulMatrixF2<true> rels;
    rels.init(0, 0);

    MulMatrixF2<false> kernel_basis;
    kernel_basis.init(n, n);
    REP (i, n)
      kernel_basis.set(i, i, 1);

    vector<MulMatrixF2<true> > cur_mats(mats.size());
    vector<MulMatrixF2<true> > cur_size_mats(size_block_mats.size());

    int maxs = nblocks - 1; // 1 for size block

    while (true) {

      vector<int> perm;
      REP (i, obits.size())
        perm.pb(i);
      REP (i, size_block_mats.size())
        cur_size_mats[i] = mul(size_block_mats[i], kernel_basis);

      REP (i, mats.size()) {
        cur_mats[i] = mul(mats[i], kernel_basis);
        //  cur_mats[i] = mats[i];
      }
      int input_dim = cur_mats[0].M;

      random_shuffle(ALL(perm));
      // want mats.size() >= kernel_basis.M*take
      // take = mats.size()/kernel_basis.M
      int take = (mats.size()) / input_dim;
      take = min(take, int(perm.size() - 1));
      OPA_DISP0(take);

      int lastc = take * input_dim + 63 & ~63;
      MulMatrixF2<true> m;
      m.init(mats.size(), lastc + mats.size());
      memset(&m.tb[0], 0, sizeof(u64) * m.tb.size());
      REP (j, mats.size()) {
        REP (i, take) {
          REP (k, input_dim)
            m.set(j, i * input_dim + k, cur_mats[j].get(perm[i], k));
        }
        m.set(j, lastc + j, 1);
      }

      int lastr = m.reduce(lastc);
      OPA_DISP0(m.N, m.M, lastr);
      // have m.N>=m.M
      if (lastr == -1)
        lastr = m.N;
      int rem = m.N - lastr;
      rem = min(rem, 30);

      // only byte boundary
      for (int ad_size = 0; ad_size < maxs * 128; ad_size += 8) {

        if (ad_size & 127) {
          int tmp = nblocks - ad_size / 128 - 1 + 1; // block id where we finish

          // tmp is a power of 2 -> we don't want that as the padding is checked
          // to be 0
          if ((tmp & tmp - 1) == 0)
            continue;
        }

        int cipher_size = maxs * 128 - (ad_size + 127 & ~127);
        Gf128_t2 new_block_size = { (u64)ad_size, (u64)cipher_size };
        Gf128_t2 diff_block = new_block_size;
        const Gf128_t2 old_block_size =
          to_gf128_t2(StringRef(&m_params.data[m_params.data.size() - 16], 16));
        add_gf128_t2(diff_block, old_block_size);

        // const_vec is the vector we are trying to achieve with a rows of m
        MulMatrixF2<true> const_vec;
        MulMatrixF2<true> cur_vec;
        const_vec.init(lastc, 1);
        cur_vec.init(lastc, 1);

        REP (j, n) {
          if (GETB(diff_block, j)) {
            REP (i, take) {
              REP (k, input_dim)
                cur_vec.set(i * input_dim + k, 0,
                            cur_size_mats[j].get(perm[i], k));
            }
            const_vec = add(const_vec, cur_vec);
          }
        }
        std::vector<int> sol;

        {
          vector<int> x(lastr);
          int col = 0;
          REP (i, lastr) {
            while (!m.get(i, col))
              ++col;
            x[i] = const_vec.get(col, 0);
          }

          bool ok = true;
          REP (i, lastc) {
            int v = 0;
            REP (j, lastr)
              v ^= x[j] & m.get(j, i);
            if (v != const_vec.get(i, 0)) {
              ok = false;
              break;
            }
          }
          if (!ok) {
            continue;
          }

          REP (i, x.size())
            if (x[i])
              sol.pb(i);
        }

        Gf128_t cur = gf128.getZ();

        FOR (mask_, 0, 1 << rem) {
          int mask = rng() % (1 << rem);

          std::string buf = forge_data;
          u64 *tb = (u64 *)&buf[0];

          vector<int> active_rows = sol;

          REP (j, rem) {
            if (!(mask >> j & 1))
              continue;
            active_rows.pb(lastr + j);
          }

          for (auto row : active_rows) {
            for (int p = lastc, pos = 0; p < m.M; p += 64, ++pos) {
              OPA_CHECK0(2 * change_id[pos / 2] * 8 < buf.size());
              tb[2 * change_id[pos / 2] + (pos & 1)] ^= m.tb[m.get_id(row, p)];
            }
          }

          if (0) {
            MulMatrixF2<true> mx;
            mx.init(1, lastc);
            for (auto row : active_rows) {
              REP (j, lastc)
                mx.set(0, j, mx.get(0, j) ^ m.get(row, j));
            }

            REP (j, lastc)
              mx.set(0, j, mx.get(0, j) ^ const_vec.get(j, 0));

            REP (j, lastc)
              OPA_CHECK(mx.get(0, j) == 0, j);
          }

          OPA_CHECK0(forge_data.size() == nblocks * 16);
          {
            u64 *tb = (u64 *)&buf[buf.size() - 16];
            tb[0] = new_block_size[0];
            tb[1] = new_block_size[1];
          }
          // OPA_CHECK0(buf != m_params.data);

          static int cnt = 0;
          ++cnt;
          if (cnt % 100 == 0)
            OPA_DISP0(cnt);

          bool ans = false;
          ans = m_params.oracle.query(buf, m_params.tag);

          if (ans) {
            cnt = 0;
            // contains changed bits
            MulMatrixF2<true> set_bits;
            set_bits.init(1, mats.size());

            for (auto row : active_rows) {
              REP (p, mats.size()) {
                if (m.get(row, lastc + p))
                  set_bits.toggle(0, p);
              }
            }

            MulMatrixF2<true> new_rel;
            {
              new_rel.init(obits.size(), n);
              REP (i, mats.size()) {
                if (!set_bits.get(0, i))
                  continue;
                auto tmp = mats[i].extract_rows(perm);
                new_rel.sadd(tmp);
              }
              REP (i, size_block_mats.size()) {
                if (!GETB(diff_block, i))
                  continue;
                new_rel.sadd(size_block_mats[i].extract_rows(perm));
              }

              if (0) {
                puts("NEW REL >> ");
                new_rel.disp();
              }

              if (0) {
                auto checkm = new_rel.copy<false>();
                auto checkv = m_params.oracle.m_params.target.get_h();

                MulMatrixF2<true> checkvm;
                checkvm.init_from_gf128_t2(checkv);
                auto resv2 = new_rel.eval_all(checkvm);

                Gf128_t2 resv;
                checkm.eval(checkv, resv);

                OPA_DISP0(resv[0], resv[1]);
                REP (i, obits.size()) {
                  OPA_CHECK0(GETB(resv, i) == resv2.get(i, 0));
                }

                // REP(i, take) { OPA_CHECK0(resv2.get(perm[i], 0) == 0); }

                if (1)
                  REP (i, take) {
                    OPA_CHECK0(GETB(resv, i) == 0);
                    OPA_CHECK0(resv2.get(i, 0) == 0);
                  }
              }

              MulMatrixF2<true> old_rels = rels;
              rels.init(old_rels.N + obits.size(), n);
              REP (i, old_rels.N)
                REP (j, n)
                  rels.set(i, j, old_rels.get(i, j));

              REP (i, obits.size()) {
                REP (j, n)
                  rels.set(old_rels.N + i, j, new_rel.get(i, j));
              }
            }

            {
              int last = kernel_basis.M;
              kernel_basis = rels.get_kernel_basis();
              int nrows = rels.M - kernel_basis.M;
              rels.set_num_rows(nrows);

              if (last == kernel_basis.M)
                goto next;

              if (0) {
                rels.disp();
                OPA_DISP0("CUR bASIS >> ", kernel_basis.N, rels.M);
              }
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
                REP (i, resv.N)
                  OPA_CHECK0(resv.get(i, 0) == 0);
              }

              OPA_DISP0(mask_);
              OPA_DISP0(rem, input_dim);
              goto next;
            }
          }
        }
      }
    next:;
    }
  }
  std::vector<int> found_h;

private:
  const int n = 128;
  std::vector<int> obits;
  std::vector<int> change_id;
  int logv;
  int nblocks;
  std::string forge_data;

  Params m_params;
  std::vector<MulMatrixF2<true> > mats;
  std::vector<MulMatrixF2<true> > size_block_mats;
  Gf128_Fast ff;
};
}

void ex_65() {
  AesGcm target(
    StringBuilder().add("Je suis un jambon").pad('a', AesGcm::blk_size).get());
  target.prepare("", Rng2::get()->bytes(16), Rng2::get()->bytes(12));
  target.prepare("", StringBuilder().pad('z', 16*5).get(), Rng2::get()->bytes(12));
  OPA_CHECK0(target.get_h().size() == 2);

  RangeCoverage output_bits = RangeCoverage().add_interval(0, LOG_BLOCKS * 2);

  GcmOracle oracle;
  oracle.init({ target, output_bits });
  std::string data = target.get_data();
  std::string tag = target.get_tag();

  Solver solver;
  solver.init({ data, oracle, output_bits, tag });
  // OPA_CHECK0(oracle.query(data, tag));
  solver.go();

  auto ans_h = bits_to_vec(target.get_h(), 128);

  OPA_DISP0(solver.found_h, ans_h);
  OPA_CHECK0(solver.found_h == ans_h);
}

OPA_NAMESPACE_END(matasano)
