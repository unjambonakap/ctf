#include "matasano/ex_60.h"

using namespace std;
using namespace opa::math::common;

OPA_NAMESPACE(matasano)

typedef ECDHBase<MontgomeryCurve, MontgomeryPoint> ECDH;
typedef OracleBase<MontgomeryCurve, MontgomeryPoint> Oracle;
typedef ECDH_ClientBase<MontgomeryCurve, MontgomeryPoint> ECDH_Client;

bg pwn_oracle(const Oracle &oracle, const bg &twist_order, bg &bound) {
  struct FactorData {
    int pw;
    int cur_pw;
    s64 base_factor;
    bg cur_factor;
    bool operator<(const FactorData &x) const {
      return cur_factor > x.cur_factor;
    }
  };
  priority_queue<FactorData> q;

  bg rem;
  auto fx = factor_small(twist_order, rem);
  OPA_DISP0(fx);
  for (auto &e : fx) {
    if (e.first >= 1e8)
      continue;
    if (e.first == 2) {
      // x ^ order /2 == 1 or -1, but can't distinguish.
      // So can't generate bad
      if (e.second >= 2)
        q.push({ 1, 1, 4, bg(4) });
    } else {
      // will only handle single power this time :(
      q.push({ 1, 1, e.first, bg(e.first) });
    }
  }

  vector<pair<bignum, bignum> > tb;
  while (!q.empty()) {
    FactorData cur_data = q.top();
    q.pop();

    puts("");
    OPA_DISP0(cur_data.cur_factor, cur_data.cur_pw);
    MontgomeryPoint bad;
    while (true) {
      bad = mont_c1.gen_rand_twist();
      bad = bad.fast_mul(twist_order / cur_data.cur_factor);
      if (!bad.is_zero())
        break;
    }

    std::string oracle_res = oracle.query(bad);
    bg step_pw = cur_data.cur_factor / cur_data.base_factor;
    MontgomeryPoint stepv = bad.fast_mul(step_pw);

    MontgomeryPoint cur = stepv.fast_mul(0);
    bg cur_pw = 0;
    OPA_DISP("on factor ", cur_data.cur_factor, step_pw, cur_pw, cur.u, bad.u);

    {
      bg target = oracle.client->priv_key;
      OPA_DISP("pkey", target % cur_data.cur_factor);
      MontgomeryPoint tmp = bad.fast_mul(target);
      MontgomeryPoint tmp2 = bad.fast_mul(target % cur_data.cur_factor);
      OPA_CHECK0(tmp == tmp2);
    }

    bool found = false;
    REP (i, cur_data.base_factor) {
      if (oracle.raw_query(cur) == oracle_res) {
        OPA_DISP("GOT AT ", i);
        found = true;
        break;
      }

      cur_pw += step_pw;
      // would have to go back to weierstrass
      cur = stepv.fast_mul(cur_pw);
    }

    OPA_DISP0(oracle.client->priv_key % cur_data.cur_factor, cur_pw);
    bg paired_pw = cur_data.cur_factor - cur_pw;

    // special case where order / 2 and 0 are merged if order is even
    // Just skip it as it is a pain to handle
    if (cur_pw == 0 && cur_data.cur_factor % 2 == 0)
      continue;
    // OPA_CHECK0(oracle.client->priv_key % cur_data.cur_factor == cur_pw ||
    //           oracle.client->priv_key % cur_data.cur_factor == paired_pw);
    // OPA_CHECK0(found);

    tb.pb(MP(cur_data.base_factor, cur_pw));

    ++cur_data.cur_pw;
    cur_data.cur_factor *= cur_data.base_factor;
    if (cur_data.cur_pw < cur_data.pw)
      q.push(cur_data);
  }

  vector<int> sgn_query;
  CRT crt1;
  REP (i, tb.size()) {
    auto &x = tb[i];
    if (x.ND != 0)
      sgn_query.pb(i);
    else {
      crt1.add(x.ST, 1, x.ND);
    }
  }
  auto v1 = crt1.solve();
  auto v2 = crt1.get_bound();
  if (!sgn_query.size()) {
    bound = v2;
    return v1;
  }

  vector<bignum> vals;
  vals.pb(tb[sgn_query[0]].ND);

  REP (k, sgn_query.size() - 1) {
    auto a = tb[sgn_query[k]];
    auto b = tb[sgn_query[k + 1]];

    auto testv = crt_coprime({ { vals[k], a.ST }, { b.ND, b.ST } });

    bg order_want = a.ST * b.ST;
    MontgomeryPoint bad;
    while (true) {
      bad = mont_c1.gen_rand_twist();
      bad = bad.fast_mul(twist_order / order_want);
      if (!bad.is_zero())
        break;
    }
    auto pt = bad.fast_mul(testv);
    if (oracle.query(bad) == oracle.raw_query(pt))
      vals.pb(b.ND);
    else {
      vals.pb(-b.ND);
    }
    OPA_DISP0(vals.back());
  }

  CRT x;
  x.add(v2, 1, v1);
  REP (i, sgn_query.size())
    x.add(tb[sgn_query[i]].ST, 1, vals[i]);
  auto res = x.solve();
  bound = x.get_bound();
  // result is res or -res
  return res;
}

class KangarooSolver {
  typedef ECPoint KangarooPoint;

public:
  std::vector<KangarooPoint> cache;

  inline void do_step(const KangarooPoint &g, bg &x, KangarooPoint &y, int k) {
    int f = 1 + (y.x.getu32_unsafe() & (1 << k) - 1);
    x += f;
    // could have used weierstrass representation, but whatever
    y = y + cache[f];
  }

  std::pair<bg, KangarooPoint> kangaroooo_one(const KangarooPoint &g,
                                              const bg &b, int k, int nstep) {
    bg init_pw = b;
    // init_pw = bg("13c4736c4c755a1b9620496916bf116e", 16);
    OPA_DISP0(init_pw, nstep);
    KangarooPoint start = g.fast_scalar_mul(init_pw);

    bg rx = init_pw;
    KangarooPoint ry = start;

    REP (i, nstep) {
      if (i % 10000 == 1)
        OPA_DISP0(ry.x, rx, i * 100 / nstep);
      do_step(g, rx, ry, k);
    }
    return MP(rx, ry);
  }

  bg kangaroooo_solve(const KangarooPoint &g, const KangarooPoint &_y,
                      const bg &a, const bg &b) {

    u32 nstep = (b - a).sqrt().getu32() * 8;
    int k = log2_high_bit(nstep);
    cache.clear();
    int sz = (1 << k) + 1;
    cache.resize(sz);
    OPA_DISP("CACHE of size ", sz);
    cache[0] = g.curve->make_zero();
    REP (i, sz - 1) {
      if (i % 1000 == 0)
        OPA_DISP0(i, sz);
      cache[i + 1] = g + cache[i];
    }

    bg xt;
    KangarooPoint yt;
    std::tie(xt, yt) = kangaroooo_one(g, b, k, nstep);
    int nid = 0;
    REP (j, 3) {
      bg to = xt;
      bg x = (b - a).sqrt().rand();
      KangarooPoint y = _y;
      y = y + g.fast_scalar_mul(x);

      ++nid;
      OPA_DISP("On step ", nid, xt, nstep);

      while (true) {
        if (x + a > to)
          break;
        do_step(g, x, y, k);
        if (y.cmp2(yt)) {
          return xt - x;
        }
      }
    }
    return -1;
  }
};

void ex_60() {
  {
    auto p1 =
      mont_c1.make_point(bg("76600469441198017145391791613091732004", 10));
    auto p2 = mont_c1.to_weierstrass(p1);
    OPA_DISP0(p1.u, p2.x, p2.y);
    OPA_CHECK0(p2.y == -1);
  }

  ECDH ecdh1(&mont_c1, mont_c1_g, ecc1_order_g);

  ECDH_Client bob(&ecdh1, ecdh1.gen_priv_key());
  ECDH_Client alice(&ecdh1, ecdh1.gen_priv_key());

  {
    MontgomeryPoint secret1 = bob.compute_secret(alice.pub_key);
    MontgomeryPoint secret2 = alice.compute_secret(bob.pub_key);
    OPA_DISP0(secret1.u, secret2.u);
    OPA_DISP0(alice.priv_key, bob.priv_key);
    OPA_CHECK0(secret1 == secret2);
  }

  {
    Oracle oracle(&bob);
    bg twist_order = ecc1_p * 2 + 2 - ecc1_order;
    OPA_DISP("Twist order >> ", twist_order);
    bg bound;
    bg cnd;

    if (0) {
      cnd = pwn_oracle(oracle, twist_order, bound);
    } else {
      // cnd=3d360a219eed82407ea871,bound=7b26bc5d78d246ffdf0c74,ecc1_order_g=1600a20f8c2c8e00a3f1911303382d1f,
      cnd = bg("3d360a219eed82407ea871"), bound = bg("7b26bc5d78d246ffdf0c74");
    }
    OPA_DISP0(cnd, bound, ecc1_order_g);

    while (true) {
      for (int sgn = -1; sgn <= 1; sgn += 2) {
        bg v = (cnd * sgn).modplus(ecc1_order_g);
        // v+bound*k
        bg ibound = bound.inv(ecc1_order_g);
        bg lb = v * ibound % ecc1_order_g;
        bg ub = lb + ecc1_order_g / bound;

        ECPoint g2 = ecc1_g.fast_scalar_mul(bound);
        //OPA_DISP0(ecc1_order_g / bound, lb, ub);
        //OPA_DISP0(v, bob.priv_key % bound);
        //OPA_DISP0(bob.priv_key * ibound % ecc1_order_g);
        //OPA_DISP0(bound * ibound % ecc1_order_g, ecc1_order_g);
        //OPA_DISP0(g2.fast_scalar_mul(bound).x);
        //OPA_DISP0(ecc1_g.fast_scalar_mul(bound * ibound).x);
        //OPA_DISP0(ecc1_g.fast_scalar_mul(v + bound * (bob.priv_key / bound)).x);
        //OPA_DISP0(mont_c1.to_weierstrass(bob.pub_key).x,
        //          ecc1_g.fast_scalar_mul(bob.priv_key).x,
        //          g2.fast_scalar_mul(bob.priv_key / bound + v * ibound).x);
        bg tmp;
        KangarooSolver solver;
        tmp = solver.kangaroooo_solve(g2, mont_c1.to_weierstrass(bob.pub_key),
                                      lb, ub);
        if (tmp == -1)
          continue;
        tmp = tmp - lb;

        bg res = (v + bound * tmp) % ecc1_order_g;
        OPA_DISP("GOT KAPPA ", res, bob.priv_key, ecc1_order_g - res, tmp);
        OPA_CHECK0(res == bob.priv_key);
        return;
      }
    }
  }
}

OPA_NAMESPACE_END(matasano)
