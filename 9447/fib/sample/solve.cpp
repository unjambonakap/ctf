#include <opa_common.h>
#include <opa/math/common/bignum.h>
#include <opa/math/common/Matrix.h>
#include <opa/math/common/GF_pBN.h>

using namespace std;
using namespace opa::math::common;

const u64 prime = 981725946171163877ll;
u64 s1 = 58449491987662952ll;
u64 s2 = 704965025359609904ll;
u64 c1 = 453665378628814896ll;
u64 c2 = 152333692332446539ll;
GF_pBN F(bignum::fromu64(prime));

struct DS {
  map<pair<u64, u64>, int> tb[16][16];
  unordered_set<u64> t1[16];
  unordered_set<u64> t2[16];
  bool check(u64 a, u64 b) {
    if (!t1[a & 15].count(a))
      return false;
    if (!t2[b & 15].count(b))
      return false;
    // if (!tb[a & 15][b & 15].count(MP(a, b)))
    //  return false;
    return true;
  }

  void add(u64 a, u64 b, int v) {
    t1[a & 15].insert(a);
    t2[b & 15].insert(b);
    // tb[a & 15][b & 15][MP(a, b)] = v;
  }
};
DS ds;

int find(u64 a, u64 b) {
  u64 id = 0;
  while (1) {
    ++id;
    u64 c = a + b;
    if (c >= prime)
      c -= prime;
    a = b;
    b = c;

    if (id % 10000000 == 0)
      printf("ON %Ld %Ld %Ld\n", id, a, b);
    if (int(id) != 0x5bd1d4b)
      continue;

    if (ds.check(a, b)) {
      OPA_DISP("FOUJND", id, a, b);
      return 0;
    }
  }
}

Matrix<bignum> get_mat() {
  Matrix<bignum> m(&F, 2, 2);
  m(0, 0) = 0;
  m(1, 0) = 1;
  m(0, 1) = 1;
  m(1, 1) = 1;
  return m;
}

void compute(u64 pos, u64 s1, u64 s2, u64 &a, u64 &b) {
  auto tmp = get_mat().faste(bignum::fromu64(pos));
  a = ((tmp(0, 0) * bignum::fromu64(s1) + tmp(0, 1) * bignum::fromu64(s2)) %
       bignum::fromu64(prime))
        .getu64();
  b = ((tmp(1, 0) * bignum::fromu64(s1) + tmp(1, 1) * bignum::fromu64(s2)) %
       bignum::fromu64(prime))
        .getu64();
}

int main(int argc, char **argv) {
  opa::init::opa_init(argc, argv);
  int nstep = 3e7;
  u64 pw = prime / nstep;

  OPA_DISP("FASTE ", pw);
  auto m = get_mat().faste(bignum::fromu64(pw));
  puts("DONE");
  auto tmp = m.identity();

  u64 v1, v2;
  {
    // ON 8680000000 558447188542942340 869904829766800237

    u64 pos;
    pos = 0x179e5c4 * pw - 0x205bd1d4b-1;
    compute(pos, 0, 1, v1, v2);

    OPA_DISP0(pos, v1, v2, s1, s2);
  }

  REP (i, nstep) {
    tmp = tmp * m;
    if (i % 10000 == 0)
      OPA_DISP0(i, nstep);
    u64 a, b;
    a = tmp(0, 0).getu64();
    b = tmp(1, 0).getu64();
    if (a == v1 && b == v2) {
      OPA_DISP0("FOUND ", i);
      return 0;
    }
    // ds.add(a, b, i);
  }
  return 0;

  {
    // s1 = tmp(0, 0).getu64();
    // s2 = tmp(1, 0).getu64();
    find(s1, s2);
  }

  return 0;
}
