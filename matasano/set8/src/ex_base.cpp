#include "matasano/ex_base.h"
#include <openssl/hmac.h>
#include <opa/crypto/hash.h>
#include <opa/crypto/aes.h>
#include <opa/math/common/Types.h>
#include <opa/utils/string_builder.h>

using namespace opa::crypto;
using namespace opa::math::common;

using opa::utils::StringBuilder;

using namespace std;

OPA_NAMESPACE(matasano)

bg ecc1_a;
bg ecc1_b;
bg ecc1_p;
bg ecc1_order_g;
bg ecc1_order;
ECCurve weierstrass_c1;
ECPoint ecc1_g;
MontgomeryPoint mont_c1_g;
MontgomeryCurve mont_c1;
Poly<u32> gcm_poly;
GF_q<u32> gf128;

u8 cnt_bit[maxb];

void init_bitstuff() {
  cnt_bit[0] = 0;
  FOR (i, 1, maxb) { cnt_bit[i] = 1 ^ cnt_bit[i & i - 1]; }
}

OPA_REGISTER_INIT(init_bitstuff, init_bitstuff);

void init_base() {
  init_math_types();
  Float::g_params.precision = 200;

  ecc1_b = 11279326;
  ecc1_p = bg("233970423115425145524320034830162017933", 10);
  ecc1_a = bg(-95051).modplus(ecc1_p);
  ecc1_order_g = bg("29246302889428143187362802287225875743", 10);
  ecc1_order = bg("233970423115425145498902418297807005944", 10);

  weierstrass_c1.init(ecc1_a, ecc1_b, ecc1_p);
  mont_c1 = MontgomeryCurve();
  ecc1_g = weierstrass_c1.make_point(
    182, bg("85518893674295321206118380980485522083", 10));
  mont_c1_g = mont_c1.make_point(4);

  gcm_poly = PR_GF2.xpw(128) + PR_GF2.xpw(7) + PR_GF2.xpw(2) + PR_GF2.x() +
             PR_GF2.constant(1);
  gf128.init(&GF2, gcm_poly);
}
OPA_REGISTER_INIT(init_base, init_base);

ECPoint ECPoint::inv() const {
  auto res = *this;
  res.y = (res.y * -1).modplus(curve->p);

  return res;
}

ECPoint ECPoint::operator+(const ECPoint &b) const {
  ECPoint res = curve->make_point();
  const auto &p = curve->p;
  if (is_zero())
    return b;
  if (b.is_zero())
    return *this;

  if (is_inv(b))
    return curve->make_zero();
  bg m;
  if (*this == b)
    m = (bg(3) * x * x + curve->a) * (y * 2).inv(p);
  else
    m = (b.y - y) * (b.x - x).inv(p);
  res.x = (m * m - x - b.x).modplus(p);
  res.y = (m * (x - res.x) - y).modplus(p);
  return res;
}

bool ECPoint::operator==(const ECPoint &b) const {
  if (x != b.x)
    return false;
  return y == b.y;
}

bool ECPoint::cmp2(const ECPoint &b) const {
  if (x != b.x)
    return false;
  return y == b.y || y == curve->p - b.y;
}

ECPoint ECPoint::fast_scalar_mul(bg k) const {
  ECPoint res = curve->make_zero();
  ECPoint v = *this;

  for (; k > 0; k = k.rshift(1), v = v + v) {
    if (k.get_bit(0))
      res = res + v;
  }
  return res;
}
std::string do_hmac_simple(StringRef str, StringRef key) {
  unsigned int res_size;
  u8 *res_buf = HMAC(EVP_sha256(), (const u8 *)key.data(), key.size(),
                     (const u8 *)str.data(), str.size(), nullptr, &res_size);
  auto res = std::string((char *)res_buf, res_size);
  return res;
}

std::string do_hmac_simple(StringRef str, const bg &k) {
  return do_hmac_simple(str, StringRef(k.str()));
}

std::string do_hmac_simple(StringRef str, const MontgomeryPoint &k) {
  return do_hmac_simple(str, StringRef(k.u.str()));
}

std::string do_hmac_simple(StringRef str, const ECPoint &k) {
  return do_hmac_simple(str, StringRef(k.x.str() + "," + k.y.str()));
}

ECPoint ECCurve::gen_rand() const {
  ECPoint res = make_point();

  while (true) {
    res.x = p.rand();
    bg tmp = (res.x.pow(3) + res.x * a + b).modplus(p);
    res.y = sqrt_tonelli(tmp, p);
    if (res.y != -1)
      return res;
  }
}

bool ECCurve::check_on(const ECPoint &pt) const {
  bg r1 = pt.y * pt.y;
  bg r2 = pt.x.pow(3) + pt.x * a + b;
  r1 = r1.modplus(p);
  r2 = r2.modplus(p);
  return r1 == r2;
}

ECPoint ECCurve::make_x(const bg &x) const {
  bg r2 = x.pow(3) + x * a + b;
  r2 = r2.modplus(p);
  return make_point(x, sqrt_tonelli(r2, p));
}

bg sqrt_tonelli(bg a, const bg &p) {
  int s = 0;
  if (a.legendre(p) != 1)
    return -1;
  {
    bg cur = p - 1;
    for (; cur.get_bit(s) == 0; ++s)
      ;
  }

  bg q = (p - 1).rshift(s);
  if (s == 1)
    return a.powm((q + 1) / 2, p);

  bg z;

  while (true) {
    z = p.rand();
    if (z.legendre(p) == -1)
      break;
  }

  bg c = z.powm(q, p);
  bg res = a.powm((q + 1) / 2, p);
  bg t = a.powm(q, p);
  int m = s;
  while (t != 1) {
    // invariant res^2=t*a
    bg tmp = t;
    int s2 = 0;
    for (; tmp != 1; ++s2, tmp = tmp * tmp % p)
      ;
    OPA_CHECK0(s2 < m);
    bg b = c.powm(bg(2).pow(m - s2 - 1), p); // b order 2^(s2+1)
    res = res * b % p;
    c = b.powm(2, p); // c order 2^s2
    t = t * c % p;    // t order <= s2-1
    m = s2;
  }
  return res;
}

MontgomeryPoint MontgomeryPoint::fast_mul(const bg &k) const {
  return curve->make_point(curve->ladder(u, k));
}

MontgomeryCurve::MontgomeryCurve() {
  p = ecc1_p;
  B = 1;
  A = 534;
}

bg MontgomeryCurve::ladder(const bg &u, bg k) const {
  bg u2 = 1, w2 = 0;
  bg u3 = u, w3 = 1;

  REPV (pos, k.get_size(2)) {
    int b = k.get_bit(pos);
    if (b)
      swap(u2, u3);
    if (b)
      swap(w2, w3);
    bg ut = (u2 * u3 - w2 * w3).powm(2, p);
    bg wt = (u * (u2 * w3 - w2 * u3).pow(2)).modplus(p);
    u3 = ut;
    w3 = wt;

    ut = (u2 * u2 - w2 * w2).powm(2, p);
    wt = bg(4) * u2 * w2 * (u2 * u2 + A * u2 * w2 + w2 * w2) % p;
    u2 = ut;
    w2 = wt;

    if (b)
      swap(u2, u3);
    if (b)
      swap(w2, w3);
  }
  return u2 * w2.powm(p - 2, p) % p;
}

ECPoint MontgomeryCurve::to_weierstrass(const MontgomeryPoint &pt) const {
  return weierstrass_c1.make_point((pt.u + 178) % p, compute_v(pt));
}

MontgomeryPoint MontgomeryCurve::to_montgomery(const ECPoint &pt) const {
  return make_point((pt.x - 178).modplus(p));
}

bg MontgomeryCurve::compute_v(const MontgomeryPoint &pt) const {
  bg v2 = pt.u.pow(3) + A * pt.u.pow(2) + pt.u;
  v2 = v2 * B.inv(p) % p;
  bg v = sqrt_tonelli(v2, p);
  return v;
}

MontgomeryPoint MontgomeryCurve::gen_rand() const {
  while (true) {
    auto res = make_point((p - 2).rand() + 2);
    if (!is_twist(res))
      return res;
  }
}

MontgomeryPoint MontgomeryCurve::gen_rand_twist() const {
  while (true) {
    auto res = make_point((p - 2).rand() + 2);
    if (is_twist(res))
      return res;
  }
}

bool MontgomeryCurve::is_twist(const MontgomeryPoint &pt) const {
  return compute_v(pt) == -1;
}

bg ECDSA::compute_hash(StringRef msg) {
  return bg(Sha256().update((const u8 *)msg.data(), msg.size()).get_hex(), 16);
}

ECDSA::ECDSA_Sign ECDSA::sign(StringRef msg, const bg &priv_key,
                              const ECDSA_Params &params) {
  bg k = (ecc1_order_g - 2).rand() + 2;
  bg r = params.g.fast_scalar_mul(k).x;
  bg h = compute_hash(msg);
  bg ik = k.inv(ecc1_order_g);
  bg res = (priv_key * r + h) * ik % ecc1_order_g;
  return MP(res, r);
}

ECDSA::ECDSA_Sign ECDSA::sign_biased(StringRef msg, const bg &priv_key,
                                     const ECDSA_Params &params,
                                     int zeroed_low_bits) {
  bg k = (ecc1_order_g - 2).rand() + 2;
  {
    bg mask = bg(2).pow(zeroed_low_bits) - 1;
    k = k ^ (mask & k);
  }

  bg r = params.g.fast_scalar_mul(k).x;
  bg h = compute_hash(msg);
  bg ik = k.inv(ecc1_order_g);
  bg res = (priv_key * r + h) * ik % ecc1_order_g;
  return MP(res, r);
}

bool ECDSA::verify(const ECDSA::ECDSA_Sign &s, StringRef msg,
                   const ECPoint &pub_key, const ECDSA_Params &params) {
  bg h = compute_hash(msg);

  if (0) {
    ECPoint r2 = weierstrass_c1.make_x(s.ND);

    ECPoint tmp = r2.fast_scalar_mul(s.ST);
    ECPoint check = pub_key.fast_scalar_mul(s.ND) + params.g.fast_scalar_mul(h);
    return tmp.x == check.x;
  } else {
    bg is = s.ST.inv(ecc1_order_g);
    bg u1 = is * s.ND % ecc1_order_g;
    bg u2 = is * h % ecc1_order_g;
    ECPoint pt = params.g.fast_scalar_mul(u2) + pub_key.fast_scalar_mul(u1);
    return pt.x == s.ND;
  }
}

void AesGcm::init(StringRef key) {
  this->key = key;
  OPA_CHECK0(key.size() == 16);
  m_aes.init(key, true);

  h_mul.init(128, 128);
  auto h = get_h();
  auto h2 = to_gf128_t(h);
  {
    std::vector<u32> tmp;
    REP (i, 128)
      tmp.pb(GETB(h, i));
    auto h3 = gf128.pr().import(tmp);
    OPA_CHECK0(h2 == h3);
  }

  Gf128_t cur = h2;
  REP (i, 128) {
    h_mul.set_col(i, cur.toVector(128));
    cur = cur * gf128.pr().x();
  }
}

void AesGcm::prepare(StringRef AD, StringRef cipher, StringRef nonce) {
  this->AD = AD;
  this->cipher = cipher;
  this->nonce = nonce;
}

void AesGcm::prepare_from_data(StringRef data, StringRef nonce) {
  u64 ad_size = *(u64 *)(data.data() + data.size() - 16) / 8;
  u64 cipher_size = *(u64 *)(data.data() + data.size() - 8) / 8;
  u64 pos = 0;
  AD = std::string(data.data() + pos, ad_size);
  pos += ad_size;
  pos = pos + 15 & ~15;
  cipher = std::string(data.data() + pos, cipher_size);
  this->nonce = nonce;
}

bool AesGcm::prepare_from_data_check_padding(StringRef data, StringRef nonce) {
  u64 ad_size = *(u64 *)(data.data() + data.size() - 16) / 8;
  u64 cipher_size = *(u64 *)(data.data() + data.size() - 8) / 8;
  int last_pos = data.size() - 16;
  u64 pos = 0;
  if (ad_size > last_pos) {
    OPA_CHECK0(false);
    return false;
  }
  AD = std::string(data.data() + pos, ad_size);
  pos += ad_size;

  int padsize;
  int npos = pos + 15 & ~15;
  padsize = npos - pos;

  if (npos + cipher_size > last_pos) {
    OPA_CHECK0(false);
    return false;
  }

  FOR (i, pos, npos)
    if (data[i] != 0) {
      OPA_DISP0(pos, npos, ad_size, cipher_size);
      OPA_CHECK0(false);
      return false;
    }

  cipher = std::string(data.data() + npos, cipher_size);
  npos += cipher_size;
  int npos2 = npos + 15 & ~15;
  if (npos2 != last_pos)
    return false;

  FOR (i, npos, npos2)
    if (data[i] != 0)
      return false;

  this->nonce = nonce;
  return true;
}

std::string AesGcm::get_data() const {
  return StringBuilder()
    .add(AD)
    .padmod(0, blk_size)
    .add(cipher)
    .padmod(0, blk_size)
    .add_num(AD.size() * 8, 8)
    .add_num(cipher.size() * 8, 8)
    .get();
}
std::vector<Gf128_t2> AesGcm::get_poly() const {

  std::string data = get_data();
  return get_poly2(data);
}

std::vector<Gf128_t2> AesGcm::get_poly2(StringRef data) const {

  std::vector<Gf128_t2> tb;
  REP (i, data.size() / blk_size) {
    auto tmp = StringRef(&data[i * blk_size], blk_size);
    tb.pb(to_gf128_t2(tmp));
  }
  return tb;
}

Gf128_t2 AesGcm::get_s() const {
  auto s_raw =
    m_aes.encrypt_raw(StringBuilder().add(nonce).add_num(1, 4).get());
  return to_gf128_t2(s_raw);
}

Gf128_t2 AesGcm::get_h() const {
  return to_gf128_t2(
    m_aes.encrypt_raw(StringBuilder().add_null(blk_size).get()));
}

std::string AesGcm::get_tag() const {
  OPA_CHECK0(nonce.size() == 12);

  auto s = get_s();
  auto poly = get_poly();
  Gf128_t2 g, tmp;
  g = { 0, 0 };

  // auto checkg = gf128.getZ();
  // auto checkh = to_gf128_t(get_h());

  for (auto &x : poly) {
    add_gf128_t2(g, x);

    h_mul.eval(g, tmp);
    g = tmp;
    // checkg = checkg + to_gf128_t(x);
    // checkg = checkh * checkg;
    // OPA_DISP0(g[0], g[1], checkg);
    // OPA_CHECK0(to_gf128_t(g) == checkg);
  }

  add_gf128_t2(s, g);
  return to_bytes_gf128_t2(s);
}

typedef Matrix<Float> Row;
void gram_schmidt(Matrix<Float> &a) {
  REP (i, a.n) {
    Row cur_row = a.get_mutable_row(i);
    REP (j, i) {
      Row other = a.get_row(j).clone();
      Float v = cur_row.dot(other) / other.dot(other);
      cur_row.ssub(other.scmul(v));
    }
  }
}

class LazyGramSchmidt {
public:
  void init(const Matrix<Float> *B) {
    this->B = B;
    invalid = 0;
    cur = B->clone();
  }

  void set_invalid(int nv) { invalid = min(nv, invalid); }

  void grahm_schmidt_row(int r) {
    cur.set_row(r, B->get_row(r));
    Matrix<Float> mod = cur.get_mutable_row(r);
    REP (j, r) {
      Row other = cur.get_row(j).clone();
      Float v = mod.dot(other) / other.dot(other);
      mod.ssub(other.scmul(v));
    }
  }

  Matrix<Float> get_row(int r) {
    while (invalid <= r) {
      grahm_schmidt_row(invalid);
      ++invalid;
    }
    return cur.get_mutable_row(r);
  }

  int invalid;
  Matrix<Float> cur;
  const Matrix<Float> *B = nullptr;
};
Float mu(const Matrix<Float> &a, const Matrix<Float> &b) {
  return a.dot(b) / b.dot(b);
}

Matrix<Float> LLL(const Matrix<Float> &e) {
  typedef Matrix<Float> M;
  Float delta = 0.99;
  M b = e.clone();
  LazyGramSchmidt q;
  q.init(&b);
  int n = e.n;
  int k = 1;
  while (k < n) {
    REPV (j, k) {
      Float mk = mu(b.get_row(k), q.get_row(j));
      if (mk.abs() > 0.5) {
        b.get_mutable_row(k).ssub(b.get_row(j).clone().scmul(mk.round()));
        q.set_invalid(k);
      }
    }

    Float mk2 = mu(b.get_row(k), q.get_row(k - 1));
    Float dk = q.get_row(k).dot(q.get_row(k));
    Float dk1 = q.get_row(k - 1).dot(q.get_row(k - 1));
    if (dk >= (delta - mk2 * mk2) * dk1)
      ++k;
    else {
      M tmpr = b.get_row(k).clone();
      b.set_row(k, b.get_row(k - 1));
      b.set_row(k - 1, tmpr);
      q.set_invalid(k - 1);
      k = max(k - 1, 1);
    }
  }

  return b;
}

/*
    function LLL(B, delta):
        B := copy(B)
        Q := gramschmidt(B)

        function mu(i, j):
            v := B[i]
            u := Q[j]
            return (v*u) / (u*u)

        n := len(B)
        k := 1

        while k < n:
            for j in reverse(range(k)):
                if abs(mu(k, j)) > 1/2:
                    B[k] := B[k] - round(mu(k, j))*B[j]
                    Q := gramschmidt(B)

            if (Q[k]*Q[k]) >= (delta - mu(k, k-1)^2) * (Q[k-1]*Q[k-1]):
                k := k + 1
            else:
                B[k], B[k-1] := B[k-1], B[k]
                Q := gramschmidt(B)
                k := max(k-1, 1)

        return B

        */
OPA_NAMESPACE_END(matasano)
