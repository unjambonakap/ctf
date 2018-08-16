#include "matasano/ex_63.h"
#include <opa/utils/string_builder.h>

using namespace opa::utils;
using namespace opa::stolen;
using namespace std;
using namespace opa::math::common;

OPA_NAMESPACE(matasano)
/*
   code that I already had (except for the special case :) )
template <class T>
void PolyRing<T>::equalDegFactor(Poly<T> a, int deg,
                                 std::vector<Poly<T> > &res) const {
  bignum q = m_ring->getSize();

  if (a.deg() == deg) {
    res.push_back(a);
    return;
  }

  bignum pw;
  if (q.get_bit(0)) {
    pw = 1;
    for (int i = 0; i < deg; ++i)
      pw = pw * q;
    pw = (pw - 1) / 2;
  } else {
    pw = 0;
    for (bignum i = 1; i <= q; i.slshift(1), pw += 1)
      ;
    pw *= deg;
    pw -= 1;
  }

  // :(
  int special_case = deg == 1 && a.deg() == 2;


  while (1) {

    Poly<T> spe_root;
    Poly<T> a_special = a;

    if (special_case) {
      //create artificial third factor
      spe_root = import({ m_ring->getRandRaw(), m_ring->getE() });
      a_special = a * spe_root;
    }

    Poly<T> b = rand(a_special.deg() - 1);

    if (m_ring->getSize().get_bit(0)) {
      b = this->faste(b, pw, a);
      b = add(b, getE());
    } else {
      Poly<T> tmp = b;
      REP (i, pw.getu32() - 1) {
        tmp = this->mod(mul(tmp, tmp), a_special);
        b = add(b, tmp);
      }
    }

    b = this->gcd(a, b);
    if (b.deg() > 0 && b.deg() < a.deg()) {
      Poly<T> q = this->div(a, b);
      equalDegFactor(q, deg, res);
      equalDegFactor(b, deg, res);
      return;
    }
  }
}

template <class T>
std::vector<Poly<T> > PolyRing<T>::factor(Poly<T> a, int deg_lim) const {
  std::vector<Poly<T> > res;
  Poly<T> rem = x();
  if (deg_lim == -1)
    deg_lim = a.deg();
  deg_lim = std::min(deg_lim, a.deg() / 2);

  for (int i = 1; i <= deg_lim; ++i) {
    rem = this->faste(rem, m_ring->getSize(), a);

    Poly<T> tmp = add(rem, neg(x()));

    while (1) {
      tmp = this->gcd(a, tmp);

      if (tmp.deg() <= 0)
        break;

      equalDegFactor(tmp, i, res);
      a = this->div(a, tmp);
    }
  }

  if (a.deg() > 0)
    res.push_back(a);
  return res;
}

*/

vector<Gf128_t2> repeated_nonce_find_h(StringRef data1, StringRef tag1,
                                       StringRef data2, StringRef tag2) {
  AesGcm builder;
  builder.init(string(AesGcm::blk_size, 'a'));
  string dummy_nonce = string(AesGcm::nonce_size, 'Z');

  builder.prepare("", data1, dummy_nonce);
  std::string d1 = builder.get_data();
  builder.prepare("", data2, dummy_nonce);
  std::string d2 = builder.get_data();

  REP (i, d1.size())
    d1[i] ^= d2[i];

  vector<Gf128_t2> poly = builder.get_poly2(d1);
  Gf128_Fast ff;
  poly.pb(ff.add(to_gf128_t2(tag1), to_gf128_t2(tag2)));
  reverse(ALL(poly));

  PolyRing<Gf128_t2> pr_gf128;
  pr_gf128.init(&ff);
  auto imported_poly = pr_gf128.import(poly);
  auto factors = pr_gf128.factor(imported_poly, 1);
  OPA_DISP("factors >> ", factors.size());
  bool found = false;

  vector<Gf128_t2> res;
  for (auto &factor : factors) {
    if (factor.deg() == 1) {
      auto cnd = ff.mul(factor[0], ff.inv(factor[1]));
      res.pb(cnd);
    }
  }
  return res;
}

void ex_63() {

  AesGcm bob;
  bob.init(
    StringBuilder().add("JE SUIS UN JAMBON").pad(0, AesGcm::blk_size).get());
  std::string data1(100, 'a');
  std::string data2(100, 'b');
  std::string nonce =
    StringBuilder().add("REPEATRED NONCE").pad(0, AesGcm::nonce_size).get();

  bob.prepare("", data1, nonce);
  string tag1 = bob.get_tag();
  bob.prepare("", data2, nonce);
  string tag2 = bob.get_tag();
  auto res = repeated_nonce_find_h(data1, tag1, data2, tag2);
  bool fd = 0;
  for (auto &cnd : res) {
    if (cnd == bob.get_h()) {
      OPA_DISP0(cnd, bob.get_h());
      fd = 1;
      break;
    }
  }
  OPA_CHECK0(fd);
}

OPA_NAMESPACE_END(matasano)
