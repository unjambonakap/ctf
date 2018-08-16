#include "matasano/ex_59.h"

using namespace std;

OPA_NAMESPACE(matasano)
typedef ECDHBase<ECCurve, ECPoint> ECDH;
typedef OracleBase<ECCurve, ECPoint> Oracle;
typedef ECDH_ClientBase<ECCurve, ECPoint> ECDH_Client;

std::vector<std::pair<bg, bg> > weak_curve_params = {
  { 210, bg("233970423115425145550826547352470124412", 10) },
  { 504, bg("233970423115425145544350131142039591210", 10) },
  { 727, bg("233970423115425145545378039958152057148", 10) },
};

bg pwn_oracle(const Oracle &oracle) {
  struct FactorData {
    int pw;
    int cur_pw;
    int curve_id;
    s64 base_factor;
    bg cur_factor;
    bool operator<(const FactorData &x) const {
      return cur_factor > x.cur_factor;
    }
  };
  map<s64, FactorData> factors;

  REP (i, weak_curve_params.size()) {
    ECCurve c2(ecc1_a, weak_curve_params[i].first, ecc1_p);
    bg cur_order = weak_curve_params[i].second;
    bg rem;
    auto fx = factor_small(cur_order, rem);
    for (auto &f : fx) {
      if (factors.count(f.ST) && factors[f.ST].pw > f.ND)
        continue;
      factors[f.ST] = { f.ND, 1, i, f.ST, bg(f.ST) };
    }
  }
  priority_queue<FactorData> q;
  for (auto &x : factors) {
    OPA_DISP0(x.second.pw, x.second.base_factor);
    q.push(x.ND);
  }

  opa::math::common::CRT crt;
  while (true) {
    if (crt.get_bound() >= ecc1_order_g)
      break;
    puts("");
    FactorData cur_data = q.top();
    q.pop();
    ECCurve c2(ecc1_a, weak_curve_params[cur_data.curve_id].first, ecc1_p);
    bg cur_order = weak_curve_params[cur_data.curve_id].second;

    ECPoint bad;
    while (true) {
      bad = c2.gen_rand();
      OPA_CHECK0(c2.check_on(bad));
      bad = bad.fast_scalar_mul(cur_order / cur_data.cur_factor);
      if (!bad.is_zero())
        break;
    }

    std::string oracle_res = oracle.query(bad);
    bg step_pw = cur_data.cur_factor / cur_data.base_factor;
    ECPoint stepv = bad.fast_scalar_mul(step_pw);

    bg cur_pw = FindWithDefault(crt.mp(), bg(cur_data.base_factor)).second;
    ECPoint cur = stepv.fast_scalar_mul(cur_pw);
    OPA_DISP("on factor ", cur_data.cur_factor, step_pw, cur_pw, cur.x, bad.x);

    {
      bg target = oracle.client->priv_key;
      OPA_DISP("pkey", target % cur_data.cur_factor);
      ECPoint tmp = bad.fast_scalar_mul(target);
      ECPoint tmp2 = bad.fast_scalar_mul(target % cur_data.cur_factor);
      OPA_CHECK0(c2.check_on(tmp2));
      ECPoint tmp3 = bad.fast_scalar_mul(cur_data.cur_factor);
      OPA_DISP0(tmp3.is_zero(), tmp3.x, tmp3.y, bad.x, bad.y);
      OPA_DISP0(bad.x, (bad + bad).x, tmp2.x);
      OPA_CHECK0(tmp3.is_zero());
      OPA_CHECK0(tmp == tmp2);
    }

    bool found = false;
    REP (i, cur_data.base_factor) {
      if (oracle.raw_query(cur) == oracle_res) {
        found = true;
        break;
      }

      cur_pw += step_pw;
      cur = cur + stepv;
    }

    OPA_DISP0(oracle.client->priv_key % cur_data.cur_factor, cur_pw);
    OPA_CHECK0(oracle.client->priv_key % cur_data.cur_factor == cur_pw);
    OPA_CHECK0(found);

    crt.add(cur_data.base_factor, cur_data.cur_pw, cur_pw);

    ++cur_data.cur_pw;
    cur_data.cur_factor *= cur_data.base_factor;
    if (cur_data.cur_pw < cur_data.pw)
      q.push(cur_data);
  }
  return crt.solve();
}

void ex_59() {
  ECDH ecdh1(&weierstrass_c1, ecc1_g, ecc1_order_g);

  ECDH_Client bob(&ecdh1, ecdh1.gen_priv_key());
  ECDH_Client alice(&ecdh1, ecdh1.gen_priv_key());

  {
    ECPoint secret1 = bob.compute_secret(alice.pub_key);
    ECPoint secret2 = alice.compute_secret(bob.pub_key);
    OPA_DISP0(secret1.x, secret1.y, secret2.x, secret2.y);
    OPA_DISP0(alice.priv_key, bob.priv_key);
    OPA_CHECK0(secret1 == secret2);
  }

  {
    Oracle oracle(&bob);
    bg res = pwn_oracle(oracle);
    OPA_DISP0(res, oracle.client->priv_key);
    OPA_CHECK0(res == oracle.client->priv_key);
  }
}

OPA_NAMESPACE_END(matasano)
