#include "matasano/ex_62.h"
#include <opa/crypto/padding.h>

using namespace opa::utils;
using namespace opa::crypto;
using namespace opa::stolen;
using namespace std;
using namespace opa::math::common;

OPA_NAMESPACE(matasano)

/*
  function sign(m, d):
      k := random_scalar(1, q)
      r := (k * G).x
      s := (H(m) + d*r) * k^-1
      return (r, s)

k=a*2^l+b, b=0 b!=0?, a is small
s=(H+d*r)*a^-1*2^-l
s*a=(H+d*r)/2^l
d*r/s/2^l=a-H/2^l/s

a~= 0
d*(r/s/2^l) = -(...)
d*u=v
      */

void ex_62() {
  typedef ECDHBase<ECCurve, ECPoint> ECDH;
  typedef ECDH_ClientBase<ECCurve, ECPoint> ECDH_Client;

  ECDHBase<ECCurve, ECPoint> ecdh(&weierstrass_c1, ecc1_g, ecc1_order_g);
  auto bob = ECDH_ClientBase<ECCurve, ECPoint>(&ecdh, ecdh.gen_priv_key());
  bg order = ecc1_order_g;

  int bias_bits = 8;
  int nrel = 20;
  vector<pair<bg, bg> > rels;

  REP (i, nrel) {
    std::string msg = Rng::get()->bytes(10);
    ECDSA_Params orig_params{ ecc1_g, ecc1_order_g };
    auto s = ECDSA::sign_biased(msg, bob.priv_key, orig_params, bias_bits);

    bg tmp = (s.first * (1 << bias_bits)).inv(order);
    bg u = s.second * tmp % order;
    bg v = -ECDSA::compute_hash(msg) * tmp % order;
    rels.pb(MP(u, v));
  }

  RealF rf;
  Matrix<Float> mat;
  int n = nrel + 2;
  int m = nrel + 2;

  mat.initialize(&rf, n, m);
  REP (i, nrel) {
    mat(i, i).from_bg(order);
    mat(nrel, i).from_bg(rels[i].ST);
    mat(nrel + 1, i).from_bg(rels[i].ND);
  }
  mat(nrel + 1, nrel + 1) = Float::From_bg(order) / (1 << bias_bits);
  mat(nrel, nrel) = 1. / (1 << bias_bits);
  OPA_DISP0(mat);

  auto res = LLL(mat);
  bool fd = false;
  REP (i, n) {
    auto x = res(i, nrel + 1) * (1 << bias_bits);
    bg ans = bg::fromFloat(x);
    if (ans.abs() == order) {
      bg sol_g = bg::fromFloat(res(i, nrel) * (1 << bias_bits)).abs();
      OPA_DISP0(sol_g, bob.priv_key);
      OPA_CHECK0(sol_g == bob.priv_key);
      fd=true; break;
    }
    OPA_DISP0(ans, order);
  }
  OPA_CHECK0(fd == true);
}

OPA_NAMESPACE_END(matasano)
