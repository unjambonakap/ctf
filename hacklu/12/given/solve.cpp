#include <opa_common.h>
#include <opa/utils/string.h>
#define OPENSSL_DISABLE_OLD_DES_SUPPORT
#include <openssl/des.h>
#include <opa/crypto/cracker_job.h>

using namespace std;
using namespace opa::utils;
using namespace opa::crypto;
using namespace opa::threading;

string challenge;
string response;
string init_plain;
string k[3];
#define VERIFIER1_KEY KEY1
#define VERIFIER2_KEY KEY2
#define CRACKER_KEY1 KEY3
#define CRACKER_KEY2 KEY4

typedef std::function<bool(const std::string &, const std::string &)>
  VerifierFunc;
OPA_CLASS_STORE_REGISTER_BY_KEY_MAKE(
  VerifierFunc([](const string &a, const string &b) { return a == b; }),
  VERIFIER1_KEY, VerifierFunc);

OPA_CLASS_STORE_REGISTER_BY_KEY_MAKE(VerifierFunc([](const string &a,
                                                     const string &b) {
  return a.substr(6, 2) == b.substr(0, 2);
}),
                                     VERIFIER2_KEY, VerifierFunc);

class DesEncryptor {
public:
  void set_key(const std::string &key) {
    DES_set_key((const_DES_cblock *)key.c_str(), &m_ks);
  }

  void encrypt(const std::string &buf, std::string &res) {
    OPA_ASSERT0(buf.size() == 8);
    DES_ecb_encrypt((const_DES_cblock *)buf.c_str(), (DES_cblock *)res.c_str(),
                    &m_ks, DES_ENCRYPT);
  }

private:
  DES_cblock m_block;
  DES_key_schedule m_ks;
};

typedef opa::utils::Storable<VerifierFunc> StorableVerifier;
/// TGEN: m_expected, m_plain
class CrackerFunc : public cracker::CrackerChecker {
public:
  void init(const std::string &expected, const std::string &plain) {
    m_expected = expected;
    m_plain = plain;
  }

  virtual bool operator()(const std::string &str) const override {
    std::string m_tmp(DES_KEY_SZ, 0);
    m_encryptor.set_key(str);
    m_encryptor.encrypt(m_plain, m_tmp);
    return verifier->get()(m_tmp, m_expected);
  }

  OPA_TGEN_IMPL(m_expected, m_plain, verifier);

  std::shared_ptr<StorableVerifier> verifier;

private:
  std::string m_expected;
  std::string m_plain;
  mutable DesEncryptor m_encryptor;
};
OPA_CLASS_STORE_REGISTER_BY_KEY(CrackerFunc, CRACKER_KEY1);

/// TGEN: m_expected, m_plain
class CrackerFunc2 : public cracker::CrackerChecker {
public:
  void init(const std::string &expected) { m_expected = expected; }

  virtual bool operator()(const std::string &str) const override {
    std::string t1(DES_KEY_SZ, 0);

    m_encryptor.set_key(str);
    m_encryptor.encrypt(init_plain, t1);
    m_encryptor.set_key(t1);
    m_encryptor.encrypt(challenge, t1);
    return m_expected == t1;
  }

  OPA_TGEN_IMPL(m_expected);

private:
  std::string m_expected;
  mutable DesEncryptor m_encryptor;
};
OPA_CLASS_STORE_REGISTER_BY_KEY(CrackerFunc2, CRACKER_KEY2);

void stage1(Dispatcher *dispatcher) {
  cracker::Cracker *cx =
    Runner::GetJob<cracker::Cracker>(cracker::Cracker::JobName);
  {
    cracker::Params params;
    cracker::Pattern pattern;
    CrackerFunc *func = OPACS_GET(CRACKER_KEY1, CrackerFunc);
    params.checker.reset(func);
    func->init(k[2], challenge);
    func->verifier.reset(OPACS_GET(VERIFIER1_KEY, StorableVerifier));

    pattern.charset = cracker::CHARSET_ALL;
    pattern.init.resize(8, 0);
    pattern.mp = { 0, 1 };
    params.patterns.pb(pattern);
    cx->init(params);
    dispatcher->process_job(*cx);
  }

  vector<string> tb2;
  if (0) {
    vector<string> tb;
    for (auto &x : cx->res_list()) {
      for (auto &y : x.tb) {
        cracker::Cracker *cx2 =
          Runner::GetJob<cracker::Cracker>(cracker::Cracker::JobName);

        cracker::Params params;
        cracker::Pattern pattern;

        CrackerFunc *func = OPACS_GET(CRACKER_KEY1, CrackerFunc);
        params.checker.reset(func);
        OPA_DISP("curs str >> ", b2h(y), init_plain, y.size(),
                 init_plain.size());
        func->init(y, init_plain);
        func->verifier.reset(OPACS_GET(VERIFIER2_KEY, StorableVerifier));

        pattern.charset = cracker::CHARSET_UPPER;
        pattern.init.resize(8, 0);
        pattern.mp = { 0, 1, 2, 3, 4, 5 };
        params.patterns.pb(pattern);
        cx2->init(params);
        dispatcher->process_job(*cx2);

        for (auto &a : cx2->res_list()) {
          for (auto &b : a.tb) {
            tb.pb(b);
          }
        }
      }
    }
    puts("GO step 2");
    printf(">> HAVE %d\n", tb.size());

    vector<pair<string, string> > tb2;
    int id = 0;
    for (auto &x : tb) {
      cracker::Cracker *cx3 =
        Runner::GetJob<cracker::Cracker>(cracker::Cracker::JobName);

      DesEncryptor enc;
      enc.set_key(x);
      string res;
      res.resize(8);
      enc.encrypt(init_plain, res);

      cracker::Params params;
      cracker::Pattern pattern;

      CrackerFunc *func = OPACS_GET(CRACKER_KEY1, CrackerFunc);
      params.checker.reset(func);
      func->init(k[1], challenge);
      func->verifier.reset(OPACS_GET(VERIFIER1_KEY, StorableVerifier));

      pattern.charset = cracker::CHARSET_ALL;
      pattern.init = "00" + res.substr(0, 6);
      pattern.mp = { 0, 1 };
      params.patterns.pb(pattern);
      cx3->init(params);
      dispatcher->process_job(*cx3);

      for (auto &a : cx3->res_list()) {
        for (auto &b : a.tb) {
          tb2.pb(MP(x, b));
          OPA_DISP("CND >> ", x);
        }
      }
    }
  }

  {
    vector<string> tb3;
    tb2.pb("");

    {

      vector<string> &dest = tb2;
      FILE *f = fopen("/usr/share/cracklib/cracklib-small", "r");
      while (true) {
        char buf[255];
        if (!fgets(buf, 100, f))
          break;
        buf[strlen(buf) - 1] = 0;
        dest.pb(buf);
        if (dest.back().size() < 2)
          dest.pop_back();
        for (auto &x : dest.back())
          if (islower(x))
            x = x ^ 32;
      }
    }

    REP(start, 1) {
      for (auto &x : tb2) {
        // OPA_DISP("processing ", x);
        cracker::Cracker *cx4 =
          Runner::GetJob<cracker::Cracker>(cracker::Cracker::JobName);

        cracker::Params params;
        cracker::Pattern pattern;

        CrackerFunc2 *func = OPACS_GET(CRACKER_KEY2, CrackerFunc2);
        params.checker.reset(func);
        func->init(k[0]);

        pattern.charset = cracker::CHARSET_UPPER;
        pattern.init = x;
        pattern.init = string(start, '0') + pattern.init;
        while (pattern.init.size() < 8)
          pattern.mp.pb(pattern.init.size()), pattern.init += "0";
        REP(i, start) pattern.mp.pb(i);
        pattern.init.resize(8);

        if (pattern.mp.size()!=2) continue;

        params.patterns.pb(pattern);
        cx4->init(params);
        dispatcher->process_job(*cx4);

        for (auto &a : cx4->res_list()) {
          for (auto &b : a.tb) {
            OPA_DISP("MAYBE >> ", b);
          }
        }
      }
    }

    vector<string> tb4;
    for (auto &x : tb3) {
      cracker::Cracker *cx4 =
        Runner::GetJob<cracker::Cracker>(cracker::Cracker::JobName);

      cracker::Params params;
      cracker::Pattern pattern;

      DesEncryptor enc;
      enc.set_key(x.substr(0, 8));
      string res;
      res.resize(8);
      enc.encrypt(init_plain, res);

      DesEncryptor enc2;
      enc2.set_key(res);
      enc2.encrypt(challenge, res);
      if (res == k[0])
        tb4.pb(x);
    }

    for (auto &x : tb4) {
      OPA_DISP("Have ans: ", x);
    }
  }
}

void go() {

  opa::threading::Runner runner;
  runner.run_both();

  stage1(runner.dispatcher());

  exit(0);
}

int main(int argc, char **argv) {
  opa::init::opa_init(argc, argv);
  init_plain = "Trololol";
  challenge = h2b("dead234a1f13beef");

  response = h2b("78165eccbf53cdb11085e8e5e3626ba9bdefd5e9de62ce91");
  REP(i, 3) k[i] = response.substr(8 * i, 8);
  go();

  response = h2b("41787c9f6ffde56919ca3cd8d8944590a9fff68468e2bcb6");
  REP(i, 3) k[i] = response.substr(8 * i, 8);

  challenge = "abcdefgh";
  {
    DesEncryptor x;
    string tmp(8, 0);
    REP(i, 6) tmp[i] = 'A';
    std::string res;
    x.set_key(tmp);
    res.resize(8);
    x.encrypt(init_plain, res);
    printf(">> %d\n", tmp.size());
    OPA_DISP("got res", b2h(res));
  }
  response = h2b("5f46bc50a72feeb37c427514d615f86183344145700d8154");
  REP(i, 3) k[i] = response.substr(8 * i, 8);
  go();

  if (1) {
    DesEncryptor x;
    string key = h2b("9a35000000000000");
    x.set_key(key);
    string res(8, 0);
    x.encrypt(challenge, res);
    cout << b2h(res) << endl;
  }

  return 0;
}
