#include "matasano/ex_61.h"
#include <opa/crypto/padding.h>
#include <opa/utils/string.h>

using namespace opa::crypto;
using namespace std;
using namespace opa::math::common;

OPA_NAMESPACE(matasano)

typedef ECDHBase<ECCurve, ECPoint> ECDH;
typedef ECDH_ClientBase<ECCurve, ECPoint> ECDH_Client;

namespace {

void part1() {

  ECDHBase<ECCurve, ECPoint> ecdh(&weierstrass_c1, ecc1_g, ecc1_order_g);
  auto bob = ECDH_ClientBase<ECCurve, ECPoint>(&ecdh, ecdh.gen_priv_key());

  std::string msg = "tortank jambon";
  ECDSA_Params orig_params{ecc1_g, ecc1_order_g};
  auto s = ECDSA::sign(msg, bob.priv_key, orig_params);

  OPA_CHECK0(ECDSA::verify(s, msg, bob.pub_key, orig_params));

  // now forging key with params for same message
  //  s = (r*d+h)*ik
  //  verify: (is*h)*g+(is*r)*Q _x==R
  // h*g+r*Q _x == s*R
  // g+ih*r*Q== ih*s*R
  // Q -> rand point, g fix to verify equation

  ECDSA_Params forged_params{ecc1_g, ecc1_order_g};
  ECPoint forged_key = ecc1_g.fast_scalar_mul((ecc1_order_g - 2).rand() + 2);
  ECPoint R = weierstrass_c1.make_x(s.ND);
  auto h = ECDSA::compute_hash(msg);
  auto ih = h.inv(ecc1_order_g);

  auto tmp = R.fast_scalar_mul(s.ST * ih);
  auto tmp2 = forged_key.fast_scalar_mul(ih * s.ND);
  auto forged_g = tmp + tmp2.inv();
  forged_params.g = forged_g;
  OPA_DISP0(forged_g.x, forged_key.x, ecc1_g.x, bob.pub_key.x);

  OPA_CHECK0(ECDSA::verify(s, msg, forged_key, forged_params));
  puts("attributed signature of message successfully");
}

class SmoothPrimeOrderFinder {
 public:
  SmoothPrimeOrderFinder(const bg &lb) {
    prime_list = opa::math::common::pl;
    prime_list.resize(1000);
    prime_list.erase(prime_list.begin());
    this->lb = lb;
  }

  bg get_one() {
    std::random_shuffle(ALL(prime_list));
    OPA_CHECK0(rec(0, 2));
    return res;
  }

  bool rec(int pos, const bg &cur) {
    if (pos == prime_list.size()) return false;
    if (cur > lb * 3 / 2) return false;

    bg ncur = cur * prime_list[pos];
    if (ncur > lb) {
      if (testPrime(ncur + 1)) {
        res = ncur;
        return true;
      }
    }
    if (rec(pos + 1, ncur)) return true;
    if (rec(pos + 1, cur)) return true;
    return false;
  }

  bg lb;
  std::vector<u32> prime_list;
  bg res;
};

void forge_rsa(const bg &a, const bg &b, bg &e, bg &n) {

  // find (e',n' >= n) st a^e'=b (n')
  // smooth order -> p-1 and q-1 smooth
  // equation must have solution -> ensured if s is generator

  int sz = max(b.get_size(2), a.get_size(2)) + 30;
  OPA_DISP("GOGIN FOR size ", sz);

  SmoothPrimeOrderFinder finder(bg(1).lshift(sz / 2));
  while (true) {
    bg p2, q2;
    p2 = finder.get_one();
    while (true) {
      q2 = finder.get_one();
      if (q2.gcd(p2) == 2) break;
    }
    p2 += 1;
    q2 += 1;
    bg rem;
    auto f1 = factor_small(p2 - 1, rem);
    OPA_CHECK0(rem == 1);
    auto f2 = factor_small(q2 - 1, rem);
    OPA_CHECK0(rem == 1);
    OPA_DISP0("try ", p2, q2);

    bg n2 = p2 * q2;
    bg order2 = (p2 - 1) * (q2 - 1);
    std::set<u32> factors;
    for (auto &x : f1) factors.insert(x.ST);
    for (auto &x : f2) factors.insert(x.ST);
    bg cnd;
    factors.erase(2);

    // pseudo gen, wont be ^order/2 will be 1 as 2 | p-1, q-1
    // more factors gcd(p-1,q-1), less chance we have of m having s base log
    bool is_gen = true;
    for (auto &x : factors) {
      if (a.powm(order2 / x, n2) == 1) {
        is_gen = false;
        break;
      }
    }
    if (!is_gen) continue;
    OPA_DISP("should be ok for ", p2, q2, a);

    CRT crt;
    for (auto &x : factors) {
      OPA_DISP("ON facxtor", x);

      bg cur = 1;
      bg step = a.powm(order2 / x, n2);
      bg target = b.powm(order2 / x, n2);
      int pw = -1;
      REP(i, x) {
        if (target == cur) {
          pw = i;
          break;
        }
        cur = cur * step % n2;
      }
      OPA_CHECK0(pw != -1);
      crt.add(x, 1, pw);
    }

    bg pw = crt.solve();
    bool fd = false;
    REP(i, 4) {
      if (a.powm(pw, n2) == b) {
        fd = true;
        break;
      }
      pw += order2 / 4;
    }
    if (!fd) continue;
    e = pw;
    n = n2;
    break;
  }
}

void part2() {

  {
    bg p = gen_prime(bg(1).lshift(512));
    bg q = gen_prime(bg(1).lshift(530));
    bg n = p * q;
    bg e = 65537;
    bg phi = (p - 1) * (q - 1);
    bg d = e.inv(phi);

    std::string msg = "caracole";
    auto padded_msg = pkcs1(msg, 40);

    bg s = bg::frombytes(padded_msg).powm(e, n);
    bg m = s.powm(d, n);
    OPA_DISP0(opa::utils::b2h(m.getbytes()), opa::utils::b2h(padded_msg));
    auto res = rpkcs1(m.getbytes());
    OPA_CHECK0(res.ND);
    OPA_CHECK0(msg == res.ST);

    bg e2, n2;
    forge_rsa(s, m, e2, n2);
    OPA_CHECK0(s.powm(e2, n2) == m);
  }

  {
    bg e2, n2;
    std::string ss(1024 / 8, 'a');
    ss += "je suis un jambon";
    bg enc = bg::frombytes(ss);
    bg m = bg::frombytes("not much more ideas for random snip");
    forge_rsa(enc, m, e2, n2);
    OPA_CHECK0(enc.powm(e2, n2) == m);
    OPA_DISP(enc.getbytes(), enc.powm(e2, n2).getbytes(), e2, n2);
  }
}
}

void ex_61() {
  part1();
  part2();
}

OPA_NAMESPACE_END(matasano)
