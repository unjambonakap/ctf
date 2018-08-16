#include "matasano/ex_58.h"
#include "matasano/ex_57.h"

using namespace std;
using namespace opa::math::common;
DEFINE_int32(ex58_part, 0, "");

OPA_NAMESPACE(matasano)

namespace {

inline void do_step(const bg &p, const bg &g, bg &x, bg &y, int k) {
  int f = 1 + (y.getu32_unsafe() & (1 << k) - 1);
  x += f;
  y = y * g.powm(f, p) % p;
}

std::pair<bg, bg> kangaroooo_one(const bg &p, const bg &g, const bg &a,
                                 const bg &b, int k, int nstep) {
  bg init_pw = (b - a).rand();
  OPA_DISP0(init_pw, nstep);
  bg start = g.powm(init_pw, p);

  bg rx = init_pw;
  bg ry = start;

  REP (i, nstep)
    do_step(p, g, rx, ry, k);
  return MP(rx, ry);
}

bg kangaroooo_solve(const bg &p, const bg &g, const bg &_y, const bg &a,
                    const bg &b) {
  u32 nstep = (b - a).sqrt().getu32() * 2;
  int k = log2_high_bit(nstep) + 2;

  int nid = 0;
  while (true) {
    bg xt, yt;
    std::tie(xt, yt) = kangaroooo_one(p, g, a, b, k, nstep);
    bg to = xt;
    bg x = 0;
    bg y = _y;

    ++nid;
    OPA_DISP("On step ", nid, xt, nstep);

    while (true) {
      if (x > to)
        break;
      do_step(p, g, x, y, k);
      if (y == yt) {
        return xt + a - x;
      }
    }
  }
}

bg p("114703748749252756581166635072321614020866502584538962745349916768989992"
     "626415815191010747406423698482332942398515192123418443373471198998743914"
     "56329785623",
     10);

bg q("335062023296420808191071248367701059461", 10);
bg j("342335868508074046234750483813286862110711967013742304926158448659292374"
     "17097514638999377942356150481334217896204702",
     10);
bg g("622952335333961296978159266084741085889881358738459939978290179936063635"
     "566740258555167783009058567397963466103140082647486611657350811560630587"
     "013183357",
     10);
bignum y1("7760073848032689505395005705677365876654629189298052775"
          "75459760744661755"
          "8600394076764814236081991643094239886772481052254010323"
          "78016509395523642"
          "9914607119",
          10);
bignum y2("9388897478013399550694114614498790691034187453089355259"
          "6026140741329188438998332773974481442458832256117269120"
          "25846772975325932794909655215329941809013733",
          10);

void part1() {
  OPA_DISPL("PART 1", "kappa");

  {
    bg lb = 0;
    bg ub = (1 << 20) + 1;
    auto res = kangaroooo_solve(p, g, y1, lb, ub);
    OPA_DISP0(res);
    OPA_CHECK0(g.powm(res, p) == y1);
  }

  {
    bg lb = 0;
    bg ub = bignum::fromu64((1ll << 40) + 1);
    auto res = kangaroooo_solve(p, g, y2, lb, ub);
    OPA_DISP0(res, y2, g.powm(res, p));
    OPA_CHECK0(g.powm(res, p) == y2);
  }
}

void part2() {
  OPA_DISPL("PART 2", "kappa");

  ExtractModval x;
  x.init(p, g, q);
  bg modres;
  bg r = x.go_extract(modres);
  bg lb = 0;
  bg ub = q / modres + 1;
  bg pubkey = x.oracle.m_bob.get_pubkey();

  bg y = pubkey * g.powm(r, p).inv(p) % p;
  bg g2 = g.powm(modres, p);
  auto k = kangaroooo_solve(p, g2, y, lb, ub);

  bg res = k * modres + r;
  OPA_DISP0(res, x.oracle.m_bob.priv_key);
  OPA_CHECK0(res == x.oracle.m_bob.priv_key);
}
}

void ex_58() {
  if (FLAGS_ex58_part != 2)
    part1();
  if (FLAGS_ex58_part != 1)
    part2();
}

OPA_NAMESPACE_END(matasano)
