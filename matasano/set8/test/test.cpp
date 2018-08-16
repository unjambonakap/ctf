#include <gtest/gtest.h>

#include <matasano/ex_base.h>
#include <opa/math/common/Utils.h>
#include <opa/math/common/Matrix.h>

using namespace opa::math::common;
using namespace std;
using namespace matasano;

void test_ecc_pt(const ECCurve &curve, ECPoint pt, const bg &order) {
  ECPoint res = pt.fast_scalar_mul(order);
  ASSERT_TRUE(res.is_zero());
}

/*
bg ecc1_gx = 182;
bg ecc1_gy("93674295321206118380980485522083", 10);
bg ecc1_order("233970423115425145498902418297807005944", 10);
bg ecc1_order_g("29246302889428143187362802287225875743", 10);

std::vector<std::pair<bg, bg>> weak_curve_params = {
    {210, bg("233970423115425145550826547352470124412", 10)},
    */

TEST(ECCCurve, TestFastScalarMul) {
  auto c1 = weierstrass_c1;

  ECPoint p1 = ecc1_g;
  ECPoint tmp = p1 + p1 + p1;
  ECPoint check = p1.fast_scalar_mul(3);
  ASSERT_TRUE(tmp == check);
}

TEST(ECCCurve, TestStayOnCurve) {
  auto c1 = weierstrass_c1;

  ECPoint p1 = ecc1_g;
  ECPoint check = p1 + p1;
  OPA_DISP0(check.x, check.y);
  ASSERT_TRUE(c1.check_on(p1));
  ASSERT_TRUE(c1.check_on(check));
}

TEST(ECCCurve, TestCurve1) {
  auto c1 = weierstrass_c1;

  test_ecc_pt(c1, ecc1_g, ecc1_order);
}

TEST(TonelliShanks, Test1) {
  bignum p = gen_prime(1 << 30);
  REP (i, 10) {
    bignum x;
    while (true) {
      x = p.rand();
      if (x.legendre(p) == 1)
        break;
    }
    bignum sq = sqrt_tonelli(x, p);
    ASSERT_EQ(sq * sq % p, x);
  }
}

TEST(TonelliShanks, TestLarge) {
  REP (prime_test, 10) {
    bignum p = gen_prime(bg(2).lshift(500));
    REP (i, 10) {
      bignum x;
      while (true) {
        x = p.rand();
        if (x.legendre(p) == 1)
          break;
      }
      bignum sq = sqrt_tonelli(x, p);
      ASSERT_EQ(sq * sq % p, x);
    }
  }
}

TEST(ECCCurve, TestMontgomery) {
  {
    auto res = mont_c1.to_weierstrass(mont_c1_g);
    OPA_DISP0(res.x, ecc1_p - res.y, ecc1_g.y);
    ASSERT_EQ(res, ecc1_g);
  }

  {
    REP (i, 10) {
      bg k = ecc1_order_g.rand();
      auto p1 = mont_c1_g.fast_mul(k);
      auto p2 = ecc1_g.fast_scalar_mul(k);
      auto tmp1 = mont_c1.to_weierstrass(p1);

      ASSERT_TRUE(tmp1.cmp2(p2));
      ASSERT_EQ(mont_c1.to_montgomery(p2), p1);
    }
  }
}

TEST(ECCCurve, TestTwistOrder) {
  {

    bg twist_order = ecc1_p * 2 + 2 - ecc1_order;
    REP (i, 10) {
      auto p = mont_c1.gen_rand_twist();
      auto p2 = p.fast_mul(twist_order);

      ASSERT_TRUE(p2.is_zero());
    }
  }
}
TEST(ECDSA, TestSign) {
  std::string msg = "kappa jambon 12";
  ECDSA_Params params{ ecc1_g, ecc1_order_g };

  ECDHBase<ECCurve, ECPoint> ecdh(&weierstrass_c1, ecc1_g, ecc1_order_g);
  auto bob = ECDH_ClientBase<ECCurve, ECPoint>(&ecdh, ecdh.gen_priv_key());

  auto s = ECDSA::sign(msg, bob.priv_key, params);
  ASSERT_TRUE(ECDSA::verify(s, msg, bob.pub_key, params));
}

TEST(GCM, TestTag) {
  AesGcm gcm(string(16, 'a'));
  gcm.prepare("THIS IS AD", "THIS IS CIPHER", "96bitnonce  ");
  gcm.get_tag();
}

TEST(Matrix, Mul) {
  REP (ntest, 100) {
    constexpr int N = 129;
    MulMatrixF2<true> al, ares;
    MulMatrixF2<false> ar;
    al.init(N, N);
    ar.init(N, N);
    Matrix<u32> bl, br, bres;
    bl.initialize(&GF2, N, N);
    br.initialize(&GF2, N, N);

    REP (i, N)
      REP (j, N) {
        int v1 = rng() % 2;
        int v2 = rng() % 2;
        al.set(i, j, v1);
        ar.set(i, j, v2);
        bl(i, j) = v1;
        br(i, j) = v2;
      }
    ares = mul(al, ar);
    bres = bl * br;

    // REP(i, N) REP(j, N) { OPA_DISP0(i,j,al.get(i,j), bl(i,j), ar.get(i,j),
    // ares.get(i,j), bres(i,j)); }
    REP (i, N)
      REP (j, N) { ASSERT_EQ(ares.get(i, j), bres(i, j)); }
  }
}

TEST(Gf128_t2, FastMul) {
  Gf128_Fast ff;
  REP (nt, 100) {
    Gf128_t e1 = gf128.getRandRaw();
    Gf128_t e2 = gf128.getRandRaw();
    auto res = e1 * e2;

    Gf128_t2 t1, t2;
    t1 = to_gf128_t2(e1);
    t2 = to_gf128_t2(e2);
    auto checkv = ff.mul(t1, t2);
    ASSERT_EQ(to_gf128_t2(res), checkv);
  }
}

TEST(LLL, GramSchmidt) {
  Matrix<Float> mat;
  RealF rf;
  mat = Matrix<Float>::rand(&rf, 3, 3);
  OPA_DISP0(mat);
  gram_schmidt(mat);
  OPA_DISP0(mat);
}

TEST(LLL, LLL) {
  Matrix<Float> mat;
  RealF rf;
  mat.initialize(&rf, 3, 3);
  mat(0, 0) = 100;
  mat(1, 0) = 350;
  mat(1, 1) = 40;
  mat(1, 2) = -300;
  mat(2, 2) = -250;
  OPA_DISP0(mat);
  auto res = LLL(mat);
  OPA_DISP0(res);
}

GTEST_API_ int main(int argc, char **argv) {
  puts("Running main() from gtest_main.cc\n");
  testing::InitGoogleTest(&argc, argv);
  opa::init::opa_init(argc, argv);
  return RUN_ALL_TESTS();
}
