#pragma once

#include <opa/crypto/aes.h>
#include <opa/math/common/Field.h>
#include <opa/math/common/GF_pBN.h>
#include <opa/math/common/GF_q.h>
#include <opa/math/common/Poly.h>
#include <opa/math/common/PolyRing.h>
#include <opa/math/common/Utils.h>
#include <opa/math/common/Types.h>
#include <opa/math/common/bignum.h>
#include <opa/stolen/StringRef.h>
#include <opa/utils/misc.h>
#include <opa/utils/string.h>
#include <opa_common.h>
#include <opa/math/common/base/range_coverage.h>
#include <opa/math/common/RealField.h>
#include <opa/math/common/Matrix.h>

using opa::math::common::RangeCoverage;
using bg = opa::math::common::bignum;
template <class T> using Field = opa::math::common::Field<T>;
using opa::math::common::GF_pBN;
using opa::math::common::rng64;
using opa::stolen::StringRef;
using opa::utils::get_bin_str;
typedef std::array<u64, 2> Gf128_t2;

namespace std {
template <class T, std::size_t N>
std::ostream &operator<<(std::ostream &os, const std::array<T, N> &a) {
  REP (i, N)
    os << a[i] << ",";
  return os;
}
}

OPA_NAMESPACE(matasano)

typedef opa::math::common::Poly<u32> Gf128_t;

class ECCurve;

class ECPoint {
public:
  ECPoint() {}
  ECPoint operator+(const ECPoint &b) const;
  ECPoint fast_scalar_mul(bg k) const;
  ECPoint inv() const;

  bool is_zero() const { return x == 0 && y == 1; }
  bool is_inv(const ECPoint &b) const { return b == inv(); }

  bool operator==(const ECPoint &b) const;
  bool cmp2(const ECPoint &b) const;

  bg x;
  bg y;
  const ECCurve *curve = nullptr;
};

class ECCurve {
public:
  ECCurve() {}
  void init(const bg &a, const bg &b, const bg &p) {
    this->a = a;
    this->b = b;
    this->p = p;
  }

  ECCurve(const bg &a, const bg &b, const bg &p) { init(a, b, p); }

  ECPoint import(const ECPoint &pt) const {
    ECPoint res = make_point();
    res.x = pt.x;
    res.y = pt.y;
    return res;
  }

  bool check_on(const ECPoint &pt) const;

  ECPoint make_point() const {
    ECPoint pt;
    pt.curve = this;
    return pt;
  }

  ECPoint make_point(const bg &x, const bg &y) const {
    ECPoint pt = make_point();
    pt.x = x;
    pt.y = y;
    return pt;
  }
  ECPoint make_x(const bg &x) const;

  ECPoint make_zero() const {
    ECPoint pt = make_point();
    pt.x = 0;
    pt.y = 1;
    return pt;
  }

  ECPoint gen_rand() const;

  bg a, b;
  bg p;
};

class MontgomeryCurve;
class MontgomeryPoint {
public:
  bg u;
  const MontgomeryCurve *curve;
  MontgomeryPoint fast_mul(const bg &k) const;
  MontgomeryPoint fast_scalar_mul(const bg &k) const { return fast_mul(k); }
  bool is_zero() const { return u == 0; }

  bool operator==(const MontgomeryPoint &p) const { return u == p.u; }
};

class MontgomeryCurve {
public:
  MontgomeryCurve();

  MontgomeryPoint make_point(const bg &u) const {
    auto res = make_point();
    res.u = u;
    return res;
  }

  MontgomeryPoint make_point() const {
    MontgomeryPoint res;
    res.curve = this;
    return res;
  }

  MontgomeryPoint make_zero() const { return make_point(0); }

  MontgomeryPoint gen_rand() const;
  MontgomeryPoint gen_rand_twist() const;
  bool is_twist(const MontgomeryPoint &pt) const;

  ECPoint to_weierstrass(const MontgomeryPoint &pt) const;
  MontgomeryPoint to_montgomery(const ECPoint &pt) const;
  bg compute_v(const MontgomeryPoint &pt) const;

  bg ladder(const bg &u, bg k) const;

  bg A, B, p;
};

template <typename Curve, typename Point> class ECDHBase {
public:
  ECDHBase(const Curve *curve, const Point &g, const bg &order_g) {
    this->curve = curve;
    this->g = g;
    this->order_g = order_g;
  }

  bg gen_priv_key() { return order_g.rand(); }

  const Curve *curve;
  Point g;
  bg order_g;
};

template <typename Curve, typename Point> class ECDH_ClientBase {
public:
  ECDH_ClientBase(const ECDHBase<Curve, Point> *ecdh, const bg &priv_key) {
    this->ecdh = ecdh;
    this->priv_key = priv_key;
    this->pub_key = ecdh->g.fast_scalar_mul(priv_key);
  }

  Point compute_secret(const Point &other_pubkey) const {
    return other_pubkey.fast_scalar_mul(priv_key);
  }

  const ECDHBase<Curve, Point> *ecdh;
  bg priv_key;
  Point pub_key;
};

template <typename Curve, typename Point> class OracleBase {
public:
  OracleBase(const ECDH_ClientBase<Curve, Point> *client) {
    this->client = client;
  }
  std::string query(const Point &pub_key) const {
    return raw_query(client->compute_secret(pub_key));
  }

  std::string raw_query(const Point &point) const {
    return do_hmac_simple("Je suis un jambon", point);
  }
  const ECDH_ClientBase<Curve, Point> *client;
};
std::string do_hmac_simple(StringRef str, StringRef k);
std::string do_hmac_simple(StringRef str, const bg &k);
std::string do_hmac_simple(StringRef str, const ECPoint &k);
std::string do_hmac_simple(StringRef str, const MontgomeryPoint &k);

bg sqrt_tonelli(bg a, const bg &p);

struct ECDSA_Params {
  ECPoint g;
  bg order_g;
};

class ECDSA {
public:
  typedef std::pair<bg, bg> ECDSA_Sign;
  static ECDSA_Sign sign(StringRef msg, const bg &priv_key,
                         const ECDSA_Params &params);
  static ECDSA_Sign sign_biased(StringRef msg, const bg &priv_key,
                                const ECDSA_Params &params,
                                int zeroed_low_bits);

  static bool verify(const ECDSA_Sign &s, StringRef msg, const ECPoint &pub_key,
                     const ECDSA_Params &params);

  static bg compute_hash(StringRef msg);
};

extern MontgomeryCurve mont_c1;
extern ECCurve weierstrass_c1;
extern ECPoint ecc1_g;
extern MontgomeryPoint mont_c1_g;
extern bg ecc1_a;
extern bg ecc1_b;
extern bg ecc1_p;
extern bg ecc1_order_g;
extern bg ecc1_order;
extern Gf128_t gcm_poly;
extern opa::math::common::GF_q<u32> gf128;

template <bool Left> class MulMatrixF2 {
public:
  MulMatrixF2() {}
  void init(int N, int M) {
    this->N = N;
    this->M = M;
    N2 = (N + 63) / 64;
    M2 = (M + 63) / 64;
    if (!Left)
      tb.resize(N2 * M);
    else
      tb.resize(M2 * N);
    memset(&tb[0], 0, sizeof(tb[0]) * tb.size());
  }

  void init_from_gf128_t2(const Gf128_t2 &v) {
    init(128, 1);
    REP (i, N)
      set(i, 0, v[i / 64] >> (i & 0x3f) & 1);
  }

  inline int get_id(int a, int b) const {
    if (Left)
      return a * M2 + (b >> 6);
    else
      return b * N2 + (a >> 6);
  }
  inline int get_bitpos(int a, int b) const {
    if (Left)
      return (b & 0x3f);
    else
      return (a & 0x3f);
  }

  inline u64 get_mask(int a, int b) const { return 1ull << get_bitpos(a, b); }

  inline int get(int a, int b) const {
    // OPA_CHECK0(a>=0 && a<N && b>=0 && b<M);
    return tb[get_id(a, b)] >> get_bitpos(a, b) & 1;
  }

  inline void set(int a, int b, int v) {
    int e = get_id(a, b);
    u64 r = tb[e];
    r = (r & ~get_mask(a, b)) | ((u64)v << get_bitpos(a, b));
    tb[e] = r;
  }

  inline void toggle(int a, int b) {
    int e = get_id(a, b);
    u64 r = tb[e];
    r ^= (u64)1 << get_bitpos(a, b);
    tb[e] = r;
  }

  template <class X> void set_row(int i, const std::vector<X> &data) {
    REP (j, data.size())
      set(i, j, data[j]);
  }

  template <class X> void set_col(int i, const std::vector<X> &data) {
    REP (j, data.size())
      set(j, i, data[j]);
  }

  template <bool V> MulMatrixF2<V> copy() const {
    MulMatrixF2<V> res;
    res.init(N, M);
    REP (i, N)
      REP (j, M)
        res.set(i, j, get(i, j));
    return res;
  }

  int reduce(int lastc) {
    int pos = 0;
    if (lastc == -1)
      lastc = M;

    for (int i = 0; i < N;) {
      if (pos == lastc)
        return i;

      int pivot = -1;
      FOR (j, i, N)
        if (get(j, pos) == 1) {
          pivot = j;
          break;
        }

      if (pivot != -1) {
        int idc = pos >> 6;
        FOR (c, idc, M2) { std::swap(tb[pivot * M2 + c], tb[i * M2 + c]); }
        REP (j, N)
          if (j != i && get(j, pos)) {
            FOR (c, idc, M2)
              tb[j * M2 + c] ^= tb[i * M2 + c];
          }
        ++i;
      }
      ++pos;
    }
    return -1;
  }

  template <class X>
  MulMatrixF2<Left> extract_rows(const std::vector<X> &rows) const {
    MulMatrixF2<Left> res;
    res.init(rows.size(), M);
    REP (i, rows.size())
      REP (j, M2)
        res.tb[res.get_id(i, j * 64)] = tb[get_id(rows[i], j * 64)];
    return res;
  }

  // eval only on 128x128 mat
  inline void eval(const Gf128_t2 &in, Gf128_t2 &o) const {
    static_assert(Left == false, "Need left false");
    // OPA_CHECK0(in.size() == 2);

    REP (k, 2) {
      u64 cur = 0;
      REP (i, M) {
        // if (GETB(in, i)) cur ^= tb[get_id(k * 64, i)];
        cur ^= tb[get_id(k * 64, i)] & -GETB(in, i);
      }
      o[k] = cur;
    }
  }

  void set_num_rows(int nrows) {
    static_assert(Left == true, "need true");
    OPA_CHECK0(nrows <= N);
    N = nrows;
    tb.resize(N * M2);
  }

  template <bool V> MulMatrixF2<V> eval_all(const MulMatrixF2<V> &v) const {
    OPA_CHECK0(v.M == 1 && v.N == M);
    MulMatrixF2<V> res;
    res.init(N, 1);
    REP (i, N) {
      int a = 0;
      REP (j, M)
        a ^= v.get(j, 0) & get(i, j);
      res.set(i, 0, a);
    }
    return res;
  }

  void disp() const {
    REP (i, N) {
      REP (j, M)
        printf("%d", get(i, j));
      puts("");
    }
  }

  void sadd(const MulMatrixF2<Left> &a) {
    OPA_CHECK0(a.N == N && a.M == M);
    REP (i, tb.size())
      tb[i] ^= a.tb[i];
  }

  MulMatrixF2<Left> transpose() const {
    MulMatrixF2<Left> res;
    res.init(M, N);
    REP (i, N)
      REP (j, M)
        res.set(j, i, get(i, j));
    return res;
  }

  MulMatrixF2<false> get_kernel_basis() {
    int lastr = reduce(-1);
    std::vector<std::vector<int> > res;

    if (lastr == -1)
      lastr = N;

    int j = 0;
    std::vector<int> fixed_vars;
    REP (i, lastr + 1) {
      while (j < M && (i == lastr || !get(i, j))) {
        std::vector<int> cur;
        REP (k, i)
          if (get(k, j))
            cur.pb(fixed_vars[k]);
        cur.pb(j);
        res.pb(cur);
        ++j;
      }
      fixed_vars.pb(j);
      ++j;
    }

    MulMatrixF2<false> m;
    m.init(M, res.size());

    REP (i, res.size()) {
      for (auto x : res[i])
        m.set(x, i, 1);
    }
    return m;
  }

  std::vector<int> get_col(int a) const {
    std::vector<int> res;
    REP (i, N)
      res.pb(get(i, a));
    return res;
  }

  std::vector<u64> tb;
  int N2, M2;
  int N, M;
};

template <typename TArray>
std::vector<int> bits_to_vec(const TArray &tb, int n) {
  std::vector<int> res;
  REP (i, n) { res.pb(GETB(tb, i)); }
  return res;
}

inline void add_gf128_t2(Gf128_t2 &i1, const Gf128_t2 &i2) {
  i1[0] ^= i2[0];
  i1[1] ^= i2[1];
}

inline std::string to_bytes_gf128_t2(const Gf128_t2 &a) {
  return std::string((const char *)&a[0], 16);
}

inline Gf128_t to_gf128_t(const Gf128_t2 &a) {
  return gf128.import_base(bg::fromrbytes(to_bytes_gf128_t2(a)));
}

inline Gf128_t2 to_gf128_t2(StringRef s) {
  OPA_CHECK0(s.size() == 16);
  Gf128_t2 res;
  res[0] = *(u64 *)(s.data());
  res[1] = *(u64 *)(s.data() + 8);
  return res;
}

inline Gf128_t to_gf128_t(StringRef s) { return to_gf128_t(to_gf128_t2(s)); }

inline Gf128_t2 to_gf128_t2(const Gf128_t &a) {
  return to_gf128_t2(gf128.to_base(a).getrbytes(16));
}

const int maxb = 1 << 16;
extern u8 cnt_bit[maxb];

inline int get_cnt_bit64(u64 a) {
  return cnt_bit[a & 0xffff] ^ cnt_bit[a >> 16 & 0xffff] ^
         cnt_bit[a >> 32 & 0xffff] ^ cnt_bit[a >> 48 & 0xffff];
}

inline MulMatrixF2<true> mul(const MulMatrixF2<true> &a,
                             const MulMatrixF2<false> &b) {
  MulMatrixF2<true> res;
  OPA_CHECK0(a.M == b.N);

  res.init(a.N, b.M);
  const int N2 = (a.M + 63) / 64;
  REP (i, a.N)
    REP (j, b.M) {
      int x = 0;
      REP (k, N2) {
        x ^=
          get_cnt_bit64(a.tb[a.get_id(i, k * 64)] & b.tb[b.get_id(k * 64, j)]);
      }
      res.set(i, j, x);
    }
  return res;
}

template <bool V1, bool V2>
inline MulMatrixF2<true> mul_slow(const MulMatrixF2<V1> &a,
                                  const MulMatrixF2<V2> &b) {
  MulMatrixF2<true> res;
  OPA_CHECK0(a.M == b.N);

  res.init(a.N, b.M);
  REP (i, a.N)
    REP (j, b.M) {
      int x = 0;
      REP (k, a.M)
        x ^= a.get(i, k) & b.get(k, j);
      res.set(i, j, x);
    }
  return res;
}

template <bool L1, bool L2>
inline MulMatrixF2<true> add(const MulMatrixF2<L1> &a,
                             const MulMatrixF2<L2> &b) {
  MulMatrixF2<true> res;
  res = a.template copy<true>();
  res.sadd(b);
  return res;
}

class AesGcm {
public:
  AesGcm() {}
  AesGcm(StringRef key) { init(key); }
  void init(StringRef key);
  void prepare(StringRef AD, StringRef cipher, StringRef nonce);
  void prepare_from_data(StringRef data, StringRef nonce);
  bool prepare_from_data_check_padding(StringRef data, StringRef nonce);

  // not using key
  std::vector<Gf128_t2> get_poly() const;
  std::vector<Gf128_t2> get_poly2(StringRef data) const;
  std::string get_tag() const;
  std::string get_data() const;
  Gf128_t2 get_s() const;
  Gf128_t2 get_h() const;
  static const int blk_size = 16;
  static const int nonce_size = 12;

  const std::string &get_nonce() const { return nonce; }

private:
  std::string AD;
  std::string cipher;
  std::string nonce;

  std::string key;
  opa::crypto::Aes m_aes;
  MulMatrixF2<false> h_mul;
};

inline void and_gf128_t2(Gf128_t2 &a, const Gf128_t2 &b) {
  a[0] &= b[0];
  a[1] &= b[1];
}

inline void shiftr_gf128_t2(Gf128_t2 &a) {
  a[0] >>= 1;
  a[0] |= a[1] << 63;
  a[1] >>= 1;
}

inline void shiftl_gf128_t2(Gf128_t2 &a) {
  a[1] <<= 1;
  a[1] |= a[0] >> 63;
  a[0] <<= 1;
}

class Gf128_Fast : public opa::math::common::Field<Gf128_t2> {
public:
  std::vector<Gf128_t2> mul_cache;
  bg m_order;
  bg m_inv_pw;

  Gf128_Fast() {
    Field<Gf128_t2>::init(bg(2).pow(128), 2);
    mul_cache.pb({ 0, 0 });
    REP (i, 2 * 128) { mul_cache.pb(to_gf128_t2(gf128.pr().x().powm(i))); }
    m_order = bg(2).pow(128) - 1;
    m_inv_pw = m_order - 1;
  }

  virtual Gf128_t2 inv(const Gf128_t2 &a) const {
    auto tmp = this->faste(a, m_inv_pw);
    OPA_CHECK0(this->mul(tmp, a) == getE());
    return tmp;
  }

  virtual Gf128_t2 mul(const Gf128_t2 &a, const Gf128_t2 &b) const {
    // return to_gf128_t2(to_gf128_t(a)*to_gf128_t(b));
    Gf128_t2 res = { 0, 0 };
    u64 f1 = a[0], f2 = a[1];
    int hb = 0;
    REP (i, 128)
      if (GETB(b, i))
        hb = i;

    int ha = 0;
    REP (i, 128)
      if (GETB(a, i))
        ha = i;

    Gf128_t2 rb = { 0, 0 };
    REP (i, hb + 1)
      if (GETB(b, i))
        BIT_BLOCK(rb, hb - i) |= BIT_B(rb, hb - i);

    {
      Gf128_t2 tmp = rb;
      REP (i, hb + 1) {
        Gf128_t2 tmp2 = tmp;
        and_gf128_t2(tmp2, a);
        int x = get_cnt_bit64(tmp2[0]) ^ get_cnt_bit64(tmp2[1]);
        add_gf128_t2(res, mul_cache[x * (1 + hb - i)]);

        shiftr_gf128_t2(tmp);
      }
    }

    {
      Gf128_t2 tmp = rb;
      shiftl_gf128_t2(tmp);

      REP (i, ha) {
        Gf128_t2 tmp2 = tmp;
        and_gf128_t2(tmp2, a);
        int x = get_cnt_bit64(tmp2[0]) ^ get_cnt_bit64(tmp2[1]);
        add_gf128_t2(res, mul_cache[x * (2 + hb + i)]);

        shiftl_gf128_t2(tmp);
      }
    }

    return res;
  }
  virtual Gf128_t2 add(const Gf128_t2 &a, const Gf128_t2 &b) const {
    Gf128_t2 res = a;
    add_gf128_t2(res, b);
    return res;
  }

  virtual Gf128_t2 neg(const Gf128_t2 &a) const { return a; }

  virtual bool isZ(const Gf128_t2 &a) const { return a == this->getZ(); }
  virtual bool isE(const Gf128_t2 &a) const { return a == this->getE(); }
  virtual Gf128_t2 import(const Gf128_t2 &a) const { return a; }

  virtual Gf128_t2 getZ() const { return Gf128_t2({ 0, 0 }); }
  virtual Gf128_t2 getE() const { return Gf128_t2({ 1, 0 }); }
  virtual Gf128_t2 getRandRaw() const { return { rng64(), rng64() }; }
};

void gram_schmidt(opa::math::common::Matrix<opa::math::common::Float> &a);

opa::math::common::Matrix<opa::math::common::Float>
LLL(const opa::math::common::Matrix<opa::math::common::Float> &e);

OPA_NAMESPACE_END(matasano)
