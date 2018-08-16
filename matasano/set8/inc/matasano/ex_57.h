#pragma once
#include <matasano/ex_base.h>

OPA_NAMESPACE(matasano)


class DiffieHelmannClient {
 public:
  void init(const bg &p, const bg &g, const bg &priv_key) {
    this->p = p;
    this->g = g;
    this->priv_key = priv_key;
  }

  bg compute_secret(const bg &other_pubkey) const {
    return other_pubkey.powm(priv_key, p);
  }
  bg get_pubkey() const { return g.powm(priv_key, p); }

  bg priv_key;
  bg p;
  bg g;
};

class Ex57Oracle {
 public:
  void init(DiffieHelmannClient bob) { m_bob = bob; }
  std::string query(const bg &eve_pubkey, StringRef msg) const {
    bg shared_secret = m_bob.compute_secret(eve_pubkey);
    return do_hmac_simple(msg, shared_secret);
  }

  DiffieHelmannClient m_bob;
};


class ExtractModval {
 public:
  void init(const bg &p, const bg &g, const bg &q) {

    DiffieHelmannClient bob;
    bg bob_priv_key = q.rand();
    bob.init(p, g, bob_priv_key);

    bg bob_chall = bob.get_pubkey();
    Ex57Oracle oracle;
    oracle.init(bob);

    init(p, g, q, oracle);
  }

  void init(const bg &p, const bg &g, const bg &q, Ex57Oracle oracle) {
    this->p = p;
    this->g = g;
    this->q = q;
    this->oracle = oracle;
  }
  bg go_extract(bg &modres);

  bg p, g, q;
  Ex57Oracle oracle;
};

void ex_57();

OPA_NAMESPACE_END(matasano)
