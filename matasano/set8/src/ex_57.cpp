#include "matasano/ex_57.h"

using namespace std;
using namespace opa::math::common;

OPA_NAMESPACE(matasano)

bg ExtractModval::go_extract(bg &modres) {

  bg j = (p - 1) / q;
  OPA_DISP0(j * q - p);

  OPA_CHECK0(g.powm(q, p) == bg(1));

  bg dummy;
  auto factors = factor_small(j, dummy);
  OPA_DISPL("factors >> ", factors, dummy);

  priority_queue<pair<s64, pair<s64, int>>> tb;

  for (auto x : factors) {
    tb.push(MP(-x.first, MP(x.first, x.second)));
  }
  std::string msg = "JE SUIS UN JAMbon";

  bg cur = 1;
  map<s64, s64> remainders;
  while (cur < q) {
    auto next = tb.top();
    next.first = -next.first;
    if (next.first > 1e6) {
      break;
    }
    tb.pop();
    bignum e;

    while (1) {
      e = bg::fromu64(rng());
      if (e.powm((p - 1) / next.first, p) != 1) break;
    }

    bg v = 1;
    int prev_pw = next.first / next.second.first;
    int prev = remainders[prev_pw];
    remainders.erase(prev_pw);

    v = v * e.powm((p - 1) / next.first * prev, p) % p;
    int step = prev_pw;
    int result = 0;
    bool found = false;

    bg fake_pubkey = e.powm((p - 1) / next.first, p);
    bg stepv = e.powm((p - 1) / next.second.first, p);

    std::string res = oracle.query(fake_pubkey, msg);
    REP(i, next.second.first) {
      if (do_hmac_simple(msg, v) == res) {
        found = true;
        break;
      }
      v = v * stepv % p;
      result += step;
    }
    OPA_CHECK0(found);

    remainders[next.first] = prev + result;
    if (--next.second.second)
      tb.push(MP(-next.first * next.second.first, next.second));
    cur *= next.second.first;
  }

  vector<pair<bg, bg>> rems;
  for (auto entry : remainders) rems.pb(MP(entry.second, entry.first));
  for (auto entry : remainders) {
    auto v = oracle.m_bob.priv_key % entry.first;
    OPA_DISP0(entry.first, v, entry.second);
  }

  bg ans = crt_coprime(rems);
  modres = 1;
  for (auto entry : rems) {
    modres *= entry.second;
  }

  return ans;
}

void ex_57() {
  bg q("236234353446506858198510045061214171961", 10);
  bg p(
      "719977399739191103060999931777394127432276433342869892173633964392834645"
      "370008535880297390048559291047548008972614070810247495742990353136958996"
      "9318716771",
      10);
  bg g(
      "456535639709574065543685450348382683213610614163956348773243819534369043"
      "760611782831804241823818489621235232911860810008318753503340201059951264"
      "1674644143",
      10);

  ExtractModval x;
  x.init(p, g, q);
  bg modres;
  bg found = x.go_extract(modres);
  OPA_CHECK0(q <= modres);

  OPA_CHECK0(found == x.oracle.m_bob.priv_key);
  OPA_DISPL("Succeeding finding key", found, x.oracle.m_bob.priv_key,
            found % q);
}

OPA_NAMESPACE_END(matasano)
