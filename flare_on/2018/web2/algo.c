#include <assert.h>
#include <math.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include "algo.h"
#define ORIG_LEN 65536 * 2
u8 buf[ORIG_LEN + ORIG_LEN];

#define i32_store(a, offset, b) (*(u32 *)(&buf[offset]) = (b))
#define i32_store8(a, offset, b) (*(u8 *)(&buf[offset]) = (u8)(b))

#define i32_load(a, offset) (*(u32 *)(&buf[offset]))
#define i32_load8_u(a, offset) (*(u8 *)(&buf[offset]))

static void f1(void);
static u32 f2(u32, u32, u32, u32);
static u32 f3(u32, u32, u32, u32);
static u32 f4(u32, u32, u32, u32);
static u32 f5(u32, u32, u32, u32);
static u32 f6(u32, u32, u32, u32);
static u32 f7(u32, u32, u32, u32);
static u32 f8(u32, u32, u32, u32);
static u32 f_dispatch(u32 k, u32 a, u32 b, u32 c, u32 d) {
  if (k == 1) return f2(a, b, c, d);
  if (k == 2) return f3(a, b, c, d);
  if (k == 3) return f4(a, b, c, d);
  if (k == 4) return f5(a, b, c, d);
  if (k == 5) return f6(a, b, c, d);
  if (k == 6) return f7(a, b, c, d);
  if (k == 7) return f8(a, b, c, d);
  return f8(a, b, c, d);
}
static u32 f9(u32, u32, u32, u32, u32);
static u32 Match(u32, u32, u32, u32);
static u32 writev_c(u32, u32, u32);
u32 __attribute__ ((noinline))  test_wrap(u32 *input, u32 *inputlen);

void __attribute__ ((noinline))  test_end(int res);


static u32 g0;

#define FUNC_PROLOGUE
#define FUNC_EPILOGUE

static u32 f2(u32 p0, u32 p1, u32 p2, u32 p3) {
  u32 l0 = 0, l1 = 0, l2 = 0, l3 = 0, l4 = 0, l5 = 0, l6 = 0, l7 = 0, l8 = 0,
      l9 = 0, l10 = 0, l11 = 0, l12 = 0, l13 = 0, l14 = 0, l15 = 0, l16 = 0,
      l17 = 0, l18 = 0, l19 = 0, l20 = 0, l21 = 0, l22 = 0, l23 = 0, l24 = 0,
      l25 = 0, l26 = 0, l27 = 0, l28 = 0, l29 = 0, l30 = 0, l31 = 0;
  FUNC_PROLOGUE;
  u32 i0, i1;
  i0 = g0;
  l0 = i0;
  i0 = 32u;
  l1 = i0;
  i0 = l0;
  i1 = l1;
  i0 -= i1;
  l2 = i0;
  i0 = 2u;
  l3 = i0;
  i0 = l2;
  i1 = p0;
  i32_store((&memory), (u32)(i0 + 20), i1);
  i0 = l2;
  i1 = p1;
  i32_store((&memory), (u32)(i0 + 16), i1);
  i0 = l2;
  i1 = p2;
  i32_store((&memory), (u32)(i0 + 12), i1);
  i0 = l2;
  i1 = p3;
  i32_store((&memory), (u32)(i0 + 8), i1);
  i0 = l2;
  i0 = i32_load((&memory), (u32)(i0 + 16));
  l4 = i0;
  i0 = l3;
  l5 = i0;
  i0 = l4;
  l6 = i0;
  i0 = l5;
  i1 = l6;
  i0 = i0 > i1;
  l7 = i0;
  i0 = l7;
  l8 = i0;
  i0 = l8;
  i0 = !(i0);
  if (i0) {
    goto B1;
  }
  i0 = 105u;
  l9 = i0;
  i0 = l2;
  i1 = l9;
  i32_store((&memory), (u32)(i0 + 24), i1);
  goto B0;
B1:;
  i0 = 0u;
  l10 = i0;
  i0 = l2;
  i0 = i32_load((&memory), (u32)(i0 + 20));
  l11 = i0;
  i0 = l11;
  i0 = i32_load8_u((&memory), (u32)(i0));
  l12 = i0;
  i0 = l2;
  i1 = l12;
  i32_store8((&memory), (u32)(i0 + 31), i1);
  i0 = l2;
  i0 = i32_load8_u((&memory), (u32)(i0 + 31));
  l13 = i0;
  i0 = 255u;
  l14 = i0;
  i0 = l13;
  i1 = l14;
  i0 &= i1;
  l15 = i0;
  i0 = 15u;
  l16 = i0;
  i0 = l15;
  i1 = l16;
  i0 &= i1;
  l17 = i0;
  i0 = 255u;
  l18 = i0;
  i0 = l17;
  i1 = l18;
  i0 &= i1;
  l19 = i0;
  i0 = l10;
  l20 = i0;
  i0 = l19;
  l21 = i0;
  i0 = l20;
  i1 = l21;
  i0 = i0 != i1;
  l22 = i0;
  i0 = l22;
  l23 = i0;
  i0 = l23;
  i0 = !(i0);
  if (i0) {
    goto B2;
  }
  i0 = 112u;
  l24 = i0;
  i0 = l2;
  i1 = l24;
  i32_store((&memory), (u32)(i0 + 24), i1);
  goto B0;
B2:;
  i0 = 0u;
  l25 = i0;
  i0 = 2u;
  l26 = i0;
  i0 = l2;
  i0 = i32_load((&memory), (u32)(i0 + 20));
  l27 = i0;
  i0 = l27;
  i0 = i32_load8_u((&memory), (u32)(i0 + 1));
  l28 = i0;
  i0 = l2;
  i0 = i32_load((&memory), (u32)(i0 + 12));
  l29 = i0;
  i0 = l29;
  i1 = l28;
  i32_store8((&memory), (u32)(i0), i1);
  i0 = l2;
  i0 = i32_load((&memory), (u32)(i0 + 8));
  l30 = i0;
  i0 = l30;
  i1 = l26;
  i32_store((&memory), (u32)(i0), i1);
  i0 = l2;
  i1 = l25;
  i32_store((&memory), (u32)(i0 + 24), i1);
B0:;
  i0 = l2;
  i0 = i32_load((&memory), (u32)(i0 + 24));
  l31 = i0;
  i0 = l31;
  goto Bfunc;
Bfunc:;
  FUNC_EPILOGUE;
  return i0;
}

static u32 f3(u32 p0, u32 p1, u32 p2, u32 p3) {
  u32 l0 = 0, l1 = 0, l2 = 0, l3 = 0, l4 = 0, l5 = 0, l6 = 0, l7 = 0, l8 = 0,
      l9 = 0, l10 = 0, l11 = 0, l12 = 0, l13 = 0, l14 = 0, l15 = 0, l16 = 0,
      l17 = 0, l18 = 0, l19 = 0, l20 = 0, l21 = 0, l22 = 0, l23 = 0, l24 = 0,
      l25 = 0, l26 = 0, l27 = 0, l28 = 0, l29 = 0, l30 = 0, l31 = 0, l32 = 0,
      l33 = 0, l34 = 0, l35 = 0;
  FUNC_PROLOGUE;
  u32 i0, i1;
  i0 = g0;
  l0 = i0;
  i0 = 32u;
  l1 = i0;
  i0 = l0;
  i1 = l1;
  i0 -= i1;
  l2 = i0;
  i0 = 2u;
  l3 = i0;
  i0 = l2;
  i1 = p0;
  i32_store((&memory), (u32)(i0 + 20), i1);
  i0 = l2;
  i1 = p1;
  i32_store((&memory), (u32)(i0 + 16), i1);
  i0 = l2;
  i1 = p2;
  i32_store((&memory), (u32)(i0 + 12), i1);
  i0 = l2;
  i1 = p3;
  i32_store((&memory), (u32)(i0 + 8), i1);
  i0 = l2;
  i0 = i32_load((&memory), (u32)(i0 + 16));
  l4 = i0;
  i0 = l3;
  l5 = i0;
  i0 = l4;
  l6 = i0;
  i0 = l5;
  i1 = l6;
  i0 = i0 > i1;
  l7 = i0;
  i0 = l7;
  l8 = i0;
  i0 = l8;
  i0 = !(i0);
  if (i0) {
    goto B1;
  }
  i0 = 105u;
  l9 = i0;
  i0 = l2;
  i1 = l9;
  i32_store((&memory), (u32)(i0 + 24), i1);
  goto B0;
B1:;
  i0 = 1u;
  l10 = i0;
  i0 = l2;
  i0 = i32_load((&memory), (u32)(i0 + 20));
  l11 = i0;
  i0 = l11;
  i0 = i32_load8_u((&memory), (u32)(i0));
  l12 = i0;
  i0 = l2;
  i1 = l12;
  i32_store8((&memory), (u32)(i0 + 31), i1);
  i0 = l2;
  i0 = i32_load8_u((&memory), (u32)(i0 + 31));
  l13 = i0;
  i0 = 255u;
  l14 = i0;
  i0 = l13;
  i1 = l14;
  i0 &= i1;
  l15 = i0;
  i0 = 15u;
  l16 = i0;
  i0 = l15;
  i1 = l16;
  i0 &= i1;
  l17 = i0;
  i0 = 255u;
  l18 = i0;
  i0 = l17;
  i1 = l18;
  i0 &= i1;
  l19 = i0;
  i0 = l10;
  l20 = i0;
  i0 = l19;
  l21 = i0;
  i0 = l20;
  i1 = l21;
  i0 = i0 != i1;
  l22 = i0;
  i0 = l22;
  l23 = i0;
  i0 = l23;
  i0 = !(i0);
  if (i0) {
    goto B2;
  }
  i0 = 112u;
  l24 = i0;
  i0 = l2;
  i1 = l24;
  i32_store((&memory), (u32)(i0 + 24), i1);
  goto B0;
B2:;
  i0 = 0u;
  l25 = i0;
  i0 = 2u;
  l26 = i0;
  i0 = l2;
  i0 = i32_load((&memory), (u32)(i0 + 20));
  l27 = i0;
  i0 = l27;
  i0 = i32_load8_u((&memory), (u32)(i0 + 1));
  l28 = i0;
  i0 = 255u;
  l29 = i0;
  i0 = l28;
  i1 = l29;
  i0 &= i1;
  l30 = i0;
  i0 = 4294967295u;
  l31 = i0;
  i0 = l30;
  i1 = l31;
  i0 ^= i1;
  l32 = i0;
  i0 = l2;
  i0 = i32_load((&memory), (u32)(i0 + 12));
  l33 = i0;
  i0 = l33;
  i1 = l32;
  i32_store8((&memory), (u32)(i0), i1);
  i0 = l2;
  i0 = i32_load((&memory), (u32)(i0 + 8));
  l34 = i0;
  i0 = l34;
  i1 = l26;
  i32_store((&memory), (u32)(i0), i1);
  i0 = l2;
  i1 = l25;
  i32_store((&memory), (u32)(i0 + 24), i1);
B0:;
  i0 = l2;
  i0 = i32_load((&memory), (u32)(i0 + 24));
  l35 = i0;
  i0 = l35;
  goto Bfunc;
Bfunc:;
  FUNC_EPILOGUE;
  return i0;
}

static u32 f4(u32 p0, u32 p1, u32 p2, u32 p3) {
  u32 l0 = 0, l1 = 0, l2 = 0, l3 = 0, l4 = 0, l5 = 0, l6 = 0, l7 = 0, l8 = 0,
      l9 = 0, l10 = 0, l11 = 0, l12 = 0, l13 = 0, l14 = 0, l15 = 0, l16 = 0,
      l17 = 0, l18 = 0, l19 = 0, l20 = 0, l21 = 0, l22 = 0, l23 = 0, l24 = 0,
      l25 = 0, l26 = 0, l27 = 0, l28 = 0, l29 = 0, l30 = 0, l31 = 0, l32 = 0,
      l33 = 0, l34 = 0, l35 = 0, l36 = 0, l37 = 0, l38 = 0;
  FUNC_PROLOGUE;
  u32 i0, i1;
  i0 = g0;
  l0 = i0;
  i0 = 32u;
  l1 = i0;
  i0 = l0;
  i1 = l1;
  i0 -= i1;
  l2 = i0;
  i0 = 3u;
  l3 = i0;
  i0 = l2;
  i1 = p0;
  i32_store((&memory), (u32)(i0 + 20), i1);
  i0 = l2;
  i1 = p1;
  i32_store((&memory), (u32)(i0 + 16), i1);
  i0 = l2;
  i1 = p2;
  i32_store((&memory), (u32)(i0 + 12), i1);
  i0 = l2;
  i1 = p3;
  i32_store((&memory), (u32)(i0 + 8), i1);
  i0 = l2;
  i0 = i32_load((&memory), (u32)(i0 + 16));
  l4 = i0;
  i0 = l3;
  l5 = i0;
  i0 = l4;
  l6 = i0;
  i0 = l5;
  i1 = l6;
  i0 = i0 > i1;
  l7 = i0;
  i0 = l7;
  l8 = i0;
  i0 = l8;
  i0 = !(i0);
  if (i0) {
    goto B1;
  }
  i0 = 105u;
  l9 = i0;
  i0 = l2;
  i1 = l9;
  i32_store((&memory), (u32)(i0 + 24), i1);
  goto B0;
B1:;
  i0 = 2u;
  l10 = i0;
  i0 = l2;
  i0 = i32_load((&memory), (u32)(i0 + 20));
  l11 = i0;
  i0 = l11;
  i0 = i32_load8_u((&memory), (u32)(i0));
  l12 = i0;
  i0 = l2;
  i1 = l12;
  i32_store8((&memory), (u32)(i0 + 31), i1);
  i0 = l2;
  i0 = i32_load8_u((&memory), (u32)(i0 + 31));
  l13 = i0;
  i0 = 255u;
  l14 = i0;
  i0 = l13;
  i1 = l14;
  i0 &= i1;
  l15 = i0;
  i0 = 15u;
  l16 = i0;
  i0 = l15;
  i1 = l16;
  i0 &= i1;
  l17 = i0;
  i0 = 255u;
  l18 = i0;
  i0 = l17;
  i1 = l18;
  i0 &= i1;
  l19 = i0;
  i0 = l10;
  l20 = i0;
  i0 = l19;
  l21 = i0;
  i0 = l20;
  i1 = l21;
  i0 = i0 != i1;
  l22 = i0;
  i0 = l22;
  l23 = i0;
  i0 = l23;
  i0 = !(i0);
  if (i0) {
    goto B2;
  }
  i0 = 112u;
  l24 = i0;
  i0 = l2;
  i1 = l24;
  i32_store((&memory), (u32)(i0 + 24), i1);
  goto B0;
B2:;
  i0 = 0u;
  l25 = i0;
  i0 = 3u;
  l26 = i0;
  i0 = l2;
  i0 = i32_load((&memory), (u32)(i0 + 20));
  l27 = i0;
  i0 = l27;
  i0 = i32_load8_u((&memory), (u32)(i0 + 1));
  l28 = i0;
  i0 = 255u;
  l29 = i0;
  i0 = l28;
  i1 = l29;
  i0 &= i1;
  l30 = i0;
  i0 = l2;
  i0 = i32_load((&memory), (u32)(i0 + 20));
  l31 = i0;
  i0 = l31;
  i0 = i32_load8_u((&memory), (u32)(i0 + 2));
  l32 = i0;
  i0 = 255u;
  l33 = i0;
  i0 = l32;
  i1 = l33;
  i0 &= i1;
  l34 = i0;
  i0 = l30;
  i1 = l34;
  i0 ^= i1;
  l35 = i0;
  i0 = l2;
  i0 = i32_load((&memory), (u32)(i0 + 12));
  l36 = i0;
  i0 = l36;
  i1 = l35;
  i32_store8((&memory), (u32)(i0), i1);
  i0 = l2;
  i0 = i32_load((&memory), (u32)(i0 + 8));
  l37 = i0;
  i0 = l37;
  i1 = l26;
  i32_store((&memory), (u32)(i0), i1);
  i0 = l2;
  i1 = l25;
  i32_store((&memory), (u32)(i0 + 24), i1);
B0:;
  i0 = l2;
  i0 = i32_load((&memory), (u32)(i0 + 24));
  l38 = i0;
  i0 = l38;
  goto Bfunc;
Bfunc:;
  FUNC_EPILOGUE;
  return i0;
}

static u32 f5(u32 p0, u32 p1, u32 p2, u32 p3) {
  u32 l0 = 0, l1 = 0, l2 = 0, l3 = 0, l4 = 0, l5 = 0, l6 = 0, l7 = 0, l8 = 0,
      l9 = 0, l10 = 0, l11 = 0, l12 = 0, l13 = 0, l14 = 0, l15 = 0, l16 = 0,
      l17 = 0, l18 = 0, l19 = 0, l20 = 0, l21 = 0, l22 = 0, l23 = 0, l24 = 0,
      l25 = 0, l26 = 0, l27 = 0, l28 = 0, l29 = 0, l30 = 0, l31 = 0, l32 = 0,
      l33 = 0, l34 = 0, l35 = 0, l36 = 0, l37 = 0, l38 = 0;
  FUNC_PROLOGUE;
  u32 i0, i1;
  i0 = g0;
  l0 = i0;
  i0 = 32u;
  l1 = i0;
  i0 = l0;
  i1 = l1;
  i0 -= i1;
  l2 = i0;
  i0 = 3u;
  l3 = i0;
  i0 = l2;
  i1 = p0;
  i32_store((&memory), (u32)(i0 + 20), i1);
  i0 = l2;
  i1 = p1;
  i32_store((&memory), (u32)(i0 + 16), i1);
  i0 = l2;
  i1 = p2;
  i32_store((&memory), (u32)(i0 + 12), i1);
  i0 = l2;
  i1 = p3;
  i32_store((&memory), (u32)(i0 + 8), i1);
  i0 = l2;
  i0 = i32_load((&memory), (u32)(i0 + 16));
  l4 = i0;
  i0 = l3;
  l5 = i0;
  i0 = l4;
  l6 = i0;
  i0 = l5;
  i1 = l6;
  i0 = i0 > i1;
  l7 = i0;
  i0 = l7;
  l8 = i0;
  i0 = l8;
  i0 = !(i0);
  if (i0) {
    goto B1;
  }
  i0 = 105u;
  l9 = i0;
  i0 = l2;
  i1 = l9;
  i32_store((&memory), (u32)(i0 + 24), i1);
  goto B0;
B1:;
  i0 = 3u;
  l10 = i0;
  i0 = l2;
  i0 = i32_load((&memory), (u32)(i0 + 20));
  l11 = i0;
  i0 = l11;
  i0 = i32_load8_u((&memory), (u32)(i0));
  l12 = i0;
  i0 = l2;
  i1 = l12;
  i32_store8((&memory), (u32)(i0 + 31), i1);
  i0 = l2;
  i0 = i32_load8_u((&memory), (u32)(i0 + 31));
  l13 = i0;
  i0 = 255u;
  l14 = i0;
  i0 = l13;
  i1 = l14;
  i0 &= i1;
  l15 = i0;
  i0 = 15u;
  l16 = i0;
  i0 = l15;
  i1 = l16;
  i0 &= i1;
  l17 = i0;
  i0 = 255u;
  l18 = i0;
  i0 = l17;
  i1 = l18;
  i0 &= i1;
  l19 = i0;
  i0 = l10;
  l20 = i0;
  i0 = l19;
  l21 = i0;
  i0 = l20;
  i1 = l21;
  i0 = i0 != i1;
  l22 = i0;
  i0 = l22;
  l23 = i0;
  i0 = l23;
  i0 = !(i0);
  if (i0) {
    goto B2;
  }
  i0 = 112u;
  l24 = i0;
  i0 = l2;
  i1 = l24;
  i32_store((&memory), (u32)(i0 + 24), i1);
  goto B0;
B2:;
  i0 = 0u;
  l25 = i0;
  i0 = 3u;
  l26 = i0;
  i0 = l2;
  i0 = i32_load((&memory), (u32)(i0 + 20));
  l27 = i0;
  i0 = l27;
  i0 = i32_load8_u((&memory), (u32)(i0 + 1));
  l28 = i0;
  i0 = 255u;
  l29 = i0;
  i0 = l28;
  i1 = l29;
  i0 &= i1;
  l30 = i0;
  i0 = l2;
  i0 = i32_load((&memory), (u32)(i0 + 20));
  l31 = i0;
  i0 = l31;
  i0 = i32_load8_u((&memory), (u32)(i0 + 2));
  l32 = i0;
  i0 = 255u;
  l33 = i0;
  i0 = l32;
  i1 = l33;
  i0 &= i1;
  l34 = i0;
  i0 = l30;
  i1 = l34;
  i0 &= i1;
  l35 = i0;
  i0 = l2;
  i0 = i32_load((&memory), (u32)(i0 + 12));
  l36 = i0;
  i0 = l36;
  i1 = l35;
  i32_store8((&memory), (u32)(i0), i1);
  i0 = l2;
  i0 = i32_load((&memory), (u32)(i0 + 8));
  l37 = i0;
  i0 = l37;
  i1 = l26;
  i32_store((&memory), (u32)(i0), i1);
  i0 = l2;
  i1 = l25;
  i32_store((&memory), (u32)(i0 + 24), i1);
B0:;
  i0 = l2;
  i0 = i32_load((&memory), (u32)(i0 + 24));
  l38 = i0;
  i0 = l38;
  goto Bfunc;
Bfunc:;
  FUNC_EPILOGUE;
  return i0;
}

static u32 f6(u32 p0, u32 p1, u32 p2, u32 p3) {
  u32 l0 = 0, l1 = 0, l2 = 0, l3 = 0, l4 = 0, l5 = 0, l6 = 0, l7 = 0, l8 = 0,
      l9 = 0, l10 = 0, l11 = 0, l12 = 0, l13 = 0, l14 = 0, l15 = 0, l16 = 0,
      l17 = 0, l18 = 0, l19 = 0, l20 = 0, l21 = 0, l22 = 0, l23 = 0, l24 = 0,
      l25 = 0, l26 = 0, l27 = 0, l28 = 0, l29 = 0, l30 = 0, l31 = 0, l32 = 0,
      l33 = 0, l34 = 0, l35 = 0, l36 = 0, l37 = 0, l38 = 0;
  FUNC_PROLOGUE;
  u32 i0, i1;
  i0 = g0;
  l0 = i0;
  i0 = 32u;
  l1 = i0;
  i0 = l0;
  i1 = l1;
  i0 -= i1;
  l2 = i0;
  i0 = 3u;
  l3 = i0;
  i0 = l2;
  i1 = p0;
  i32_store((&memory), (u32)(i0 + 20), i1);
  i0 = l2;
  i1 = p1;
  i32_store((&memory), (u32)(i0 + 16), i1);
  i0 = l2;
  i1 = p2;
  i32_store((&memory), (u32)(i0 + 12), i1);
  i0 = l2;
  i1 = p3;
  i32_store((&memory), (u32)(i0 + 8), i1);
  i0 = l2;
  i0 = i32_load((&memory), (u32)(i0 + 16));
  l4 = i0;
  i0 = l3;
  l5 = i0;
  i0 = l4;
  l6 = i0;
  i0 = l5;
  i1 = l6;
  i0 = i0 > i1;
  l7 = i0;
  i0 = l7;
  l8 = i0;
  i0 = l8;
  i0 = !(i0);
  if (i0) {
    goto B1;
  }
  i0 = 105u;
  l9 = i0;
  i0 = l2;
  i1 = l9;
  i32_store((&memory), (u32)(i0 + 24), i1);
  goto B0;
B1:;
  i0 = 4u;
  l10 = i0;
  i0 = l2;
  i0 = i32_load((&memory), (u32)(i0 + 20));
  l11 = i0;
  i0 = l11;
  i0 = i32_load8_u((&memory), (u32)(i0));
  l12 = i0;
  i0 = l2;
  i1 = l12;
  i32_store8((&memory), (u32)(i0 + 31), i1);
  i0 = l2;
  i0 = i32_load8_u((&memory), (u32)(i0 + 31));
  l13 = i0;
  i0 = 255u;
  l14 = i0;
  i0 = l13;
  i1 = l14;
  i0 &= i1;
  l15 = i0;
  i0 = 15u;
  l16 = i0;
  i0 = l15;
  i1 = l16;
  i0 &= i1;
  l17 = i0;
  i0 = 255u;
  l18 = i0;
  i0 = l17;
  i1 = l18;
  i0 &= i1;
  l19 = i0;
  i0 = l10;
  l20 = i0;
  i0 = l19;
  l21 = i0;
  i0 = l20;
  i1 = l21;
  i0 = i0 != i1;
  l22 = i0;
  i0 = l22;
  l23 = i0;
  i0 = l23;
  i0 = !(i0);
  if (i0) {
    goto B2;
  }
  i0 = 112u;
  l24 = i0;
  i0 = l2;
  i1 = l24;
  i32_store((&memory), (u32)(i0 + 24), i1);
  goto B0;
B2:;
  i0 = 0u;
  l25 = i0;
  i0 = 3u;
  l26 = i0;
  i0 = l2;
  i0 = i32_load((&memory), (u32)(i0 + 20));
  l27 = i0;
  i0 = l27;
  i0 = i32_load8_u((&memory), (u32)(i0 + 1));
  l28 = i0;
  i0 = 255u;
  l29 = i0;
  i0 = l28;
  i1 = l29;
  i0 &= i1;
  l30 = i0;
  i0 = l2;
  i0 = i32_load((&memory), (u32)(i0 + 20));
  l31 = i0;
  i0 = l31;
  i0 = i32_load8_u((&memory), (u32)(i0 + 2));
  l32 = i0;
  i0 = 255u;
  l33 = i0;
  i0 = l32;
  i1 = l33;
  i0 &= i1;
  l34 = i0;
  i0 = l30;
  i1 = l34;
  i0 |= i1;
  l35 = i0;
  i0 = l2;
  i0 = i32_load((&memory), (u32)(i0 + 12));
  l36 = i0;
  i0 = l36;
  i1 = l35;
  i32_store8((&memory), (u32)(i0), i1);
  i0 = l2;
  i0 = i32_load((&memory), (u32)(i0 + 8));
  l37 = i0;
  i0 = l37;
  i1 = l26;
  i32_store((&memory), (u32)(i0), i1);
  i0 = l2;
  i1 = l25;
  i32_store((&memory), (u32)(i0 + 24), i1);
B0:;
  i0 = l2;
  i0 = i32_load((&memory), (u32)(i0 + 24));
  l38 = i0;
  i0 = l38;
  goto Bfunc;
Bfunc:;
  FUNC_EPILOGUE;
  return i0;
}

static u32 f7(u32 p0, u32 p1, u32 p2, u32 p3) {
  u32 l0 = 0, l1 = 0, l2 = 0, l3 = 0, l4 = 0, l5 = 0, l6 = 0, l7 = 0, l8 = 0,
      l9 = 0, l10 = 0, l11 = 0, l12 = 0, l13 = 0, l14 = 0, l15 = 0, l16 = 0,
      l17 = 0, l18 = 0, l19 = 0, l20 = 0, l21 = 0, l22 = 0, l23 = 0, l24 = 0,
      l25 = 0, l26 = 0, l27 = 0, l28 = 0, l29 = 0, l30 = 0, l31 = 0, l32 = 0,
      l33 = 0, l34 = 0, l35 = 0, l36 = 0, l37 = 0, l38 = 0;
  FUNC_PROLOGUE;
  u32 i0, i1;
  i0 = g0;
  l0 = i0;
  i0 = 32u;
  l1 = i0;
  i0 = l0;
  i1 = l1;
  i0 -= i1;
  l2 = i0;
  i0 = 3u;
  l3 = i0;
  i0 = l2;
  i1 = p0;
  i32_store((&memory), (u32)(i0 + 20), i1);
  i0 = l2;
  i1 = p1;
  i32_store((&memory), (u32)(i0 + 16), i1);
  i0 = l2;
  i1 = p2;
  i32_store((&memory), (u32)(i0 + 12), i1);
  i0 = l2;
  i1 = p3;
  i32_store((&memory), (u32)(i0 + 8), i1);
  i0 = l2;
  i0 = i32_load((&memory), (u32)(i0 + 16));
  l4 = i0;
  i0 = l3;
  l5 = i0;
  i0 = l4;
  l6 = i0;
  i0 = l5;
  i1 = l6;
  i0 = i0 > i1;
  l7 = i0;
  i0 = l7;
  l8 = i0;
  i0 = l8;
  i0 = !(i0);
  if (i0) {
    goto B1;
  }
  i0 = 105u;
  l9 = i0;
  i0 = l2;
  i1 = l9;
  i32_store((&memory), (u32)(i0 + 24), i1);
  goto B0;
B1:;
  i0 = 5u;
  l10 = i0;
  i0 = l2;
  i0 = i32_load((&memory), (u32)(i0 + 20));
  l11 = i0;
  i0 = l11;
  i0 = i32_load8_u((&memory), (u32)(i0));
  l12 = i0;
  i0 = l2;
  i1 = l12;
  i32_store8((&memory), (u32)(i0 + 31), i1);
  i0 = l2;
  i0 = i32_load8_u((&memory), (u32)(i0 + 31));
  l13 = i0;
  i0 = 255u;
  l14 = i0;
  i0 = l13;
  i1 = l14;
  i0 &= i1;
  l15 = i0;
  i0 = 15u;
  l16 = i0;
  i0 = l15;
  i1 = l16;
  i0 &= i1;
  l17 = i0;
  i0 = 255u;
  l18 = i0;
  i0 = l17;
  i1 = l18;
  i0 &= i1;
  l19 = i0;
  i0 = l10;
  l20 = i0;
  i0 = l19;
  l21 = i0;
  i0 = l20;
  i1 = l21;
  i0 = i0 != i1;
  l22 = i0;
  i0 = l22;
  l23 = i0;
  i0 = l23;
  i0 = !(i0);
  if (i0) {
    goto B2;
  }
  i0 = 112u;
  l24 = i0;
  i0 = l2;
  i1 = l24;
  i32_store((&memory), (u32)(i0 + 24), i1);
  goto B0;
B2:;
  i0 = 0u;
  l25 = i0;
  i0 = 3u;
  l26 = i0;
  i0 = l2;
  i0 = i32_load((&memory), (u32)(i0 + 20));
  l27 = i0;
  i0 = l27;
  i0 = i32_load8_u((&memory), (u32)(i0 + 1));
  l28 = i0;
  i0 = 255u;
  l29 = i0;
  i0 = l28;
  i1 = l29;
  i0 &= i1;
  l30 = i0;
  i0 = l2;
  i0 = i32_load((&memory), (u32)(i0 + 20));
  l31 = i0;
  i0 = l31;
  i0 = i32_load8_u((&memory), (u32)(i0 + 2));
  l32 = i0;
  i0 = 255u;
  l33 = i0;
  i0 = l32;
  i1 = l33;
  i0 &= i1;
  l34 = i0;
  i0 = l30;
  i1 = l34;
  i0 += i1;
  l35 = i0;
  i0 = l2;
  i0 = i32_load((&memory), (u32)(i0 + 12));
  l36 = i0;
  i0 = l36;
  i1 = l35;
  i32_store8((&memory), (u32)(i0), i1);
  i0 = l2;
  i0 = i32_load((&memory), (u32)(i0 + 8));
  l37 = i0;
  i0 = l37;
  i1 = l26;
  i32_store((&memory), (u32)(i0), i1);
  i0 = l2;
  i1 = l25;
  i32_store((&memory), (u32)(i0 + 24), i1);
B0:;
  i0 = l2;
  i0 = i32_load((&memory), (u32)(i0 + 24));
  l38 = i0;
  i0 = l38;
  goto Bfunc;
Bfunc:;
  FUNC_EPILOGUE;
  return i0;
}

static u32 f8(u32 p0, u32 p1, u32 p2, u32 p3) {
  u32 l0 = 0, l1 = 0, l2 = 0, l3 = 0, l4 = 0, l5 = 0, l6 = 0, l7 = 0, l8 = 0,
      l9 = 0, l10 = 0, l11 = 0, l12 = 0, l13 = 0, l14 = 0, l15 = 0, l16 = 0,
      l17 = 0, l18 = 0, l19 = 0, l20 = 0, l21 = 0, l22 = 0, l23 = 0, l24 = 0,
      l25 = 0, l26 = 0, l27 = 0, l28 = 0, l29 = 0, l30 = 0, l31 = 0, l32 = 0,
      l33 = 0, l34 = 0, l35 = 0, l36 = 0, l37 = 0, l38 = 0, l39 = 0, l40 = 0;
  FUNC_PROLOGUE;
  u32 i0, i1;
  i0 = g0;
  l0 = i0;
  i0 = 32u;
  l1 = i0;
  i0 = l0;
  i1 = l1;
  i0 -= i1;
  l2 = i0;
  i0 = 3u;
  l3 = i0;
  i0 = l2;
  i1 = p0;
  i32_store((&memory), (u32)(i0 + 20), i1);
  i0 = l2;
  i1 = p1;
  i32_store((&memory), (u32)(i0 + 16), i1);
  i0 = l2;
  i1 = p2;
  i32_store((&memory), (u32)(i0 + 12), i1);
  i0 = l2;
  i1 = p3;
  i32_store((&memory), (u32)(i0 + 8), i1);
  i0 = l2;
  i0 = i32_load((&memory), (u32)(i0 + 16));
  l4 = i0;
  i0 = l3;
  l5 = i0;
  i0 = l4;
  l6 = i0;
  i0 = l5;
  i1 = l6;
  i0 = i0 > i1;
  l7 = i0;
  i0 = l7;
  l8 = i0;
  i0 = l8;
  i0 = !(i0);
  if (i0) {
    goto B1;
  }
  i0 = 105u;
  l9 = i0;
  i0 = l2;
  i1 = l9;
  i32_store((&memory), (u32)(i0 + 24), i1);
  goto B0;
B1:;
  i0 = 6u;
  l10 = i0;
  i0 = l2;
  i0 = i32_load((&memory), (u32)(i0 + 20));
  l11 = i0;
  i0 = l11;
  i0 = i32_load8_u((&memory), (u32)(i0));
  l12 = i0;
  i0 = l2;
  i1 = l12;
  i32_store8((&memory), (u32)(i0 + 31), i1);
  i0 = l2;
  i0 = i32_load8_u((&memory), (u32)(i0 + 31));
  l13 = i0;
  i0 = 255u;
  l14 = i0;
  i0 = l13;
  i1 = l14;
  i0 &= i1;
  l15 = i0;
  i0 = 15u;
  l16 = i0;
  i0 = l15;
  i1 = l16;
  i0 &= i1;
  l17 = i0;
  i0 = 255u;
  l18 = i0;
  i0 = l17;
  i1 = l18;
  i0 &= i1;
  l19 = i0;
  i0 = l10;
  l20 = i0;
  i0 = l19;
  l21 = i0;
  i0 = l20;
  i1 = l21;
  i0 = i0 != i1;
  l22 = i0;
  i0 = l22;
  l23 = i0;
  i0 = l23;
  i0 = !(i0);
  if (i0) {
    goto B2;
  }
  i0 = 112u;
  l24 = i0;
  i0 = l2;
  i1 = l24;
  i32_store((&memory), (u32)(i0 + 24), i1);
  goto B0;
B2:;
  i0 = 0u;
  l25 = i0;
  i0 = 3u;
  l26 = i0;
  i0 = l2;
  i0 = i32_load((&memory), (u32)(i0 + 20));
  l27 = i0;
  i0 = l27;
  i0 = i32_load8_u((&memory), (u32)(i0 + 2));
  l28 = i0;
  i0 = 255u;
  l29 = i0;
  i0 = l28;
  i1 = l29;
  i0 &= i1;
  l30 = i0;
  i0 = l2;
  i0 = i32_load((&memory), (u32)(i0 + 20));
  l31 = i0;
  i0 = l31;
  i0 = i32_load8_u((&memory), (u32)(i0 + 1));
  l32 = i0;
  i0 = 255u;
  l33 = i0;
  i0 = l32;
  i1 = l33;
  i0 &= i1;
  l34 = i0;
  i0 = l30;
  i1 = l34;
  i0 -= i1;
  l35 = i0;
  i0 = 255u;
  l36 = i0;
  i0 = l35;
  i1 = l36;
  i0 &= i1;
  l37 = i0;
  i0 = l2;
  i0 = i32_load((&memory), (u32)(i0 + 12));
  l38 = i0;
  i0 = l38;
  i1 = l37;
  i32_store8((&memory), (u32)(i0), i1);
  i0 = l2;
  i0 = i32_load((&memory), (u32)(i0 + 8));
  l39 = i0;
  i0 = l39;
  i1 = l26;
  i32_store((&memory), (u32)(i0), i1);
  i0 = l2;
  i1 = l25;
  i32_store((&memory), (u32)(i0 + 24), i1);
B0:;
  i0 = l2;
  i0 = i32_load((&memory), (u32)(i0 + 24));
  l40 = i0;
  i0 = l40;
  goto Bfunc;
Bfunc:;
  FUNC_EPILOGUE;
  return i0;
}

static u32 f9(u32 p0, u32 p1, u32 p2, u32 p3, u32 p4) {
  u32 l0 = 0, l1 = 0, l2 = 0, l3 = 0, l4 = 0, l5 = 0, l6 = 0, l7 = 0, l8 = 0,
      l9 = 0, l10 = 0, l11 = 0, l12 = 0, l13 = 0, l14 = 0, l15 = 0, l16 = 0,
      l17 = 0, l18 = 0, l19 = 0, l20 = 0, l21 = 0, l22 = 0, l23 = 0, l24 = 0,
      l25 = 0, l26 = 0, l27 = 0, l28 = 0, l29 = 0, l30 = 0, l31 = 0, l32 = 0,
      l33 = 0, l34 = 0, l35 = 0, l36 = 0, l37 = 0, l38 = 0, l39 = 0, l40 = 0,
      l41 = 0, l42 = 0, l43 = 0, l44 = 0, l45 = 0, l46 = 0, l47 = 0, l48 = 0,
      l49 = 0, l50 = 0, l51 = 0, l52 = 0, l53 = 0, l54 = 0, l55 = 0, l56 = 0,
      l57 = 0, l58 = 0, l59 = 0, l60 = 0, l61 = 0, l62 = 0, l63 = 0, l64 = 0,
      l65 = 0, l66 = 0, l67 = 0, l68 = 0, l69 = 0, l70 = 0, l71 = 0, l72 = 0,
      l73 = 0, l74 = 0, l75 = 0, l76 = 0, l77 = 0, l78 = 0, l79 = 0, l80 = 0,
      l81 = 0, l82 = 0, l83 = 0, l84 = 0, l85 = 0, l86 = 0, l87 = 0, l88 = 0,
      l89 = 0, l90 = 0, l91 = 0, l92 = 0, l93 = 0, l94 = 0, l95 = 0, l96 = 0,
      l97 = 0, l98 = 0, l99 = 0, l100 = 0, l101 = 0, l102 = 0, l103 = 0,
      l104 = 0, l105 = 0, l106 = 0, l107 = 0, l108 = 0, l109 = 0, l110 = 0,
      l111 = 0, l112 = 0, l113 = 0;
  FUNC_PROLOGUE;
  u32 i0, i1, i2, i3, i4;
  i0 = g0;
  l0 = i0;
  i0 = 64u;
  l1 = i0;
  i0 = l0;
  i1 = l1;
  i0 -= i1;
  l2 = i0;
  i0 = l2;
  g0 = i0;
  i0 = 0u;
  l3 = i0;
  i0 = l2;
  i1 = p0;
  i32_store((&memory), (u32)(i0 + 52), i1);
  i0 = l2;
  i1 = p1;
  i32_store((&memory), (u32)(i0 + 48), i1);
  i0 = l2;
  i1 = p2;
  i32_store((&memory), (u32)(i0 + 44), i1);
  i0 = l2;
  i1 = p3;
  i32_store((&memory), (u32)(i0 + 40), i1);
  i0 = l2;
  i1 = p4;
  i32_store((&memory), (u32)(i0 + 36), i1);
  i0 = l2;
  i1 = l3;
  i32_store((&memory), (u32)(i0 + 32), i1);
  i0 = l2;
  i0 = i32_load((&memory), (u32)(i0 + 52));
  l4 = i0;
  i0 = l2;
  i1 = l4;
  i32_store((&memory), (u32)(i0 + 28), i1);
  i0 = l2;
  i1 = l3;
  i32_store((&memory), (u32)(i0 + 24), i1);
L1:
  i0 = 0u;
  l5 = i0;
  i0 = l2;
  i0 = i32_load((&memory), (u32)(i0 + 28));
  l6 = i0;
  i0 = l2;
  i0 = i32_load((&memory), (u32)(i0 + 52));
  l7 = i0;
  i0 = l2;
  i0 = i32_load((&memory), (u32)(i0 + 48));
  l8 = i0;
  i0 = l7;
  i1 = l8;
  i0 += i1;
  l9 = i0;
  i0 = l6;
  l10 = i0;
  i0 = l9;
  l11 = i0;
  i0 = l10;
  i1 = l11;
  i0 = i0 < i1;
  l12 = i0;
  i0 = l12;
  l13 = i0;
  i0 = l5;
  l14 = i0;
  i0 = l13;
  i0 = !(i0);
  if (i0) {
    goto B2;
  }
  i0 = l2;
  i0 = i32_load((&memory), (u32)(i0 + 24));
  l15 = i0;
  i0 = l2;
  i0 = i32_load((&memory), (u32)(i0 + 40));
  l16 = i0;
  i0 = l15;
  l17 = i0;
  i0 = l16;
  l18 = i0;
  i0 = l17;
  i1 = l18;
  i0 = i0 < i1;
  l19 = i0;
  i0 = l19;
  l14 = i0;
B2:;
  i0 = l14;
  l20 = i0;
  i0 = 1u;
  l21 = i0;
  i0 = l20;
  i1 = l21;
  i0 &= i1;
  l22 = i0;
  i0 = l22;
  i0 = !(i0);
  if (i0) {
    goto B3;
  }
  i0 = 7u;
  l23 = i0;
  i0 = l2;
  i0 = i32_load((&memory), (u32)(i0 + 28));
  l24 = i0;
  i0 = l24;
  i0 = i32_load8_u((&memory), (u32)(i0));
  l25 = i0;
  i0 = l2;
  i1 = l25;
  i32_store8((&memory), (u32)(i0 + 63), i1);
  i0 = l2;
  i0 = i32_load8_u((&memory), (u32)(i0 + 63));
  l26 = i0;
  i0 = 255u;
  l27 = i0;
  i0 = l26;
  i1 = l27;
  i0 &= i1;
  l28 = i0;
  i0 = 15u;
  l29 = i0;
  i0 = l28;
  i1 = l29;
  i0 &= i1;
  l30 = i0;
  i0 = l2;
  i1 = l30;
  i32_store8((&memory), (u32)(i0 + 23), i1);
  i0 = l2;
  i0 = i32_load8_u((&memory), (u32)(i0 + 23));
  l31 = i0;
  i0 = 255u;
  l32 = i0;
  i0 = l31;
  i1 = l32;
  i0 &= i1;
  l33 = i0;
  i0 = l23;
  l34 = i0;
  i0 = l33;
  l35 = i0;
  i0 = l34;
  i1 = l35;
  i0 = (u32)((s32)i0 <= (s32)i1);
  l36 = i0;
  i0 = l36;
  l37 = i0;
  i0 = l37;
  i0 = !(i0);
  if (i0) {
    goto B4;
  }
  i0 = 112u;
  l38 = i0;
  i0 = l2;
  i1 = l38;
  i32_store((&memory), (u32)(i0 + 56), i1);
  goto B0;
B4:;
  i0 = 0u;
  l39 = i0;
  i0 = 15u;
  l40 = i0;
  i0 = l2;
  i1 = l40;
  i0 += i1;
  l41 = i0;
  i0 = l41;
  l42 = i0;
  i0 = 8u;
  l43 = i0;
  i0 = l2;
  i1 = l43;
  i0 += i1;
  l44 = i0;
  i0 = l44;
  l45 = i0;
  i0 = 0u;
  l46 = i0;
  i0 = 1024u;
  l47 = i0;
  i0 = l2;
  i0 = i32_load8_u((&memory), (u32)(i0 + 23));
  l48 = i0;
  i0 = 255u;
  l49 = i0;
  i0 = l48;
  i1 = l49;
  i0 &= i1;
  l50 = i0;
  i0 = 2u;
  l51 = i0;
  i0 = l50;
  i1 = l51;
  i0 <<= (i1 & 31);
  l52 = i0;
  i0 = l47;
  i1 = l52;
  i0 += i1;
  l53 = i0;
  i0 = l53;
  i0 = i32_load((&memory), (u32)(i0));
  l54 = i0;
  i0 = l2;
  i1 = l54;
  i32_store((&memory), (u32)(i0 + 16), i1);
  i0 = l2;
  i1 = l46;
  i32_store8((&memory), (u32)(i0 + 15), i1);
  i0 = l2;
  i1 = l39;
  i32_store((&memory), (u32)(i0 + 8), i1);
  i0 = l2;
  i0 = i32_load((&memory), (u32)(i0 + 16));
  l55 = i0;
  i0 = l2;
  i0 = i32_load((&memory), (u32)(i0 + 28));
  l56 = i0;
  i0 = l2;
  i0 = i32_load((&memory), (u32)(i0 + 48));
  l57 = i0;
  i0 = l2;
  i0 = i32_load((&memory), (u32)(i0 + 28));
  l58 = i0;
  i0 = l2;
  i0 = i32_load((&memory), (u32)(i0 + 52));
  l59 = i0;
  i0 = l58;
  i1 = l59;
  i0 -= i1;
  l60 = i0;
  i0 = l57;
  i1 = l60;
  i0 -= i1;
  l61 = i0;
  i0 = l56;
  i1 = l61;
  i2 = l42;
  i3 = l45;
  i4 = l55;
  i0 = f_dispatch(i4, i0, i1, i2, i3);
  l62 = i0;
  i0 = l39;
  l63 = i0;
  i0 = l62;
  l64 = i0;
  i0 = l63;
  i1 = l64;
  i0 = i0 != i1;
  l65 = i0;
  i0 = l65;
  l66 = i0;
  i0 = l66;
  i0 = !(i0);
  if (i0) {
    goto B5;
  }
  goto B3;
B5:;
  i0 = l2;
  i0 = i32_load8_u((&memory), (u32)(i0 + 15));
  l67 = i0;
  i0 = 255u;
  l68 = i0;
  i0 = l67;
  i1 = l68;
  i0 &= i1;
  l69 = i0;
  i0 = l2;
  i0 = i32_load((&memory), (u32)(i0 + 44));
  l70 = i0;
  i0 = l2;
  i0 = i32_load((&memory), (u32)(i0 + 24));
  l71 = i0;
  i0 = l70;
  i1 = l71;
  i0 += i1;
  l72 = i0;
  i0 = l72;
  i0 = i32_load8_u((&memory), (u32)(i0));
  l73 = i0;
  i0 = 24u;
  l74 = i0;
  i0 = l73;
  i1 = l74;
  i0 <<= (i1 & 31);
  l75 = i0;
  i0 = l75;
  i1 = l74;
  i0 = (u32)((s32)i0 >> (i1 & 31));
  l76 = i0;
  i0 = l69;
  l77 = i0;
  i0 = l76;
  l78 = i0;
  i0 = l77;
  i1 = l78;
  i0 = i0 == i1;
  l79 = i0;
  i0 = l79;
  l80 = i0;
  i0 = l80;
  i0 = !(i0);
  if (i0) {
    goto B6;
  }
  i0 = l2;
  i0 = i32_load((&memory), (u32)(i0 + 32));
  l81 = i0;
  i0 = 1u;
  l82 = i0;
  i0 = l81;
  i1 = l82;
  i0 += i1;
  l83 = i0;
  i0 = l2;
  i1 = l83;
  i32_store((&memory), (u32)(i0 + 32), i1);
B6:;
  i0 = l2;
  i0 = i32_load((&memory), (u32)(i0 + 8));
  l84 = i0;
  i0 = l2;
  i0 = i32_load((&memory), (u32)(i0 + 28));
  l85 = i0;
  i0 = l85;
  i1 = l84;
  i0 += i1;
  l86 = i0;
  i0 = l2;
  i1 = l86;
  i32_store((&memory), (u32)(i0 + 28), i1);
  i0 = l2;
  i0 = i32_load((&memory), (u32)(i0 + 24));
  l87 = i0;
  i0 = 1u;
  l88 = i0;
  i0 = l87;
  i1 = l88;
  i0 += i1;
  l89 = i0;
  i0 = l2;
  i1 = l89;
  i32_store((&memory), (u32)(i0 + 24), i1);
  goto L1;
B3:;
  i0 = l2;
  i0 = i32_load((&memory), (u32)(i0 + 28));
  l90 = i0;
  i0 = l2;
  i0 = i32_load((&memory), (u32)(i0 + 52));
  l91 = i0;
  i0 = l2;
  i0 = i32_load((&memory), (u32)(i0 + 48));
  l92 = i0;
  i0 = l91;
  i1 = l92;
  i0 += i1;
  l93 = i0;
  i0 = l90;
  l94 = i0;
  i0 = l93;
  l95 = i0;
  i0 = l94;
  i1 = l95;
  i0 = i0 != i1;
  l96 = i0;
  i0 = l96;
  l97 = i0;
  i0 = l97;
  i0 = !(i0);
  if (i0) {
    goto B8;
  }
  i0 = 0u;
  l98 = i0;
  i0 = l2;
  i0 = i32_load((&memory), (u32)(i0 + 36));
  l99 = i0;
  i0 = l99;
  i1 = l98;
  i32_store8((&memory), (u32)(i0), i1);
  goto B7;
B8:;
  i0 = l2;
  i0 = i32_load((&memory), (u32)(i0 + 32));
  l100 = i0;
  i0 = l2;
  i0 = i32_load((&memory), (u32)(i0 + 40));
  l101 = i0;
  i0 = l100;
  l102 = i0;
  i0 = l101;
  l103 = i0;
  i0 = l102;
  i1 = l103;
  i0 = i0 != i1;
  l104 = i0;
  i0 = l104;
  l105 = i0;
  i0 = l105;
  i0 = !(i0);
  if (i0) {
    goto B10;
  }
  i0 = 0u;
  l106 = i0;
  i0 = l2;
  i0 = i32_load((&memory), (u32)(i0 + 36));
  l107 = i0;
  i0 = l107;
  i1 = l106;
  i32_store8((&memory), (u32)(i0), i1);
  goto B9;
B10:;
  i0 = 1u;
  l108 = i0;
  i0 = l2;
  i0 = i32_load((&memory), (u32)(i0 + 36));
  l109 = i0;
  i0 = l109;
  i1 = l108;
  i32_store8((&memory), (u32)(i0), i1);
B9:;
B7:;
  i0 = 0u;
  l110 = i0;
  i0 = l2;
  i1 = l110;
  i32_store((&memory), (u32)(i0 + 56), i1);
B0:;
  i0 = l2;
  i0 = i32_load((&memory), (u32)(i0 + 56));
  l111 = i0;
  i0 = 64u;
  l112 = i0;
  i0 = l2;
  i1 = l112;
  i0 += i1;
  l113 = i0;
  i0 = l113;
  g0 = i0;
  i0 = l111;
  goto Bfunc;
Bfunc:;
  FUNC_EPILOGUE;
  return i0;
}

static u32 Match(u32 p0, u32 p1, u32 p2, u32 p3) {
  u32 l0 = 0, l1 = 0, l2 = 0, l3 = 0, l4 = 0, l5 = 0, l6 = 0, l7 = 0, l8 = 0,
      l9 = 0, l10 = 0, l11 = 0, l12 = 0, l13 = 0, l14 = 0, l15 = 0, l16 = 0,
      l17 = 0, l18 = 0, l19 = 0, l20 = 0, l21 = 0, l22 = 0, l23 = 0;
  FUNC_PROLOGUE;
  u32 i0, i1, i2, i3, i4;
  i0 = g0;
  l0 = i0;
  i0 = 32u;
  l1 = i0;
  i0 = l0;
  i1 = l1;
  i0 -= i1;
  l2 = i0;
  i0 = l2;
  g0 = i0;
  i0 = 0u;
  l3 = i0;
  i0 = 11u;
  l4 = i0;
  i0 = l2;
  i1 = l4;
  i0 += i1;
  l5 = i0;
  i0 = l5;
  l6 = i0;
  i0 = 0u;
  l7 = i0;
  i0 = l2;
  i1 = p0;
  i32_store((&memory), (u32)(i0 + 24), i1);
  i0 = l2;
  i1 = p1;
  i32_store((&memory), (u32)(i0 + 20), i1);
  i0 = l2;
  i1 = p2;
  i32_store((&memory), (u32)(i0 + 16), i1);
  i0 = l2;
  i1 = p3;
  i32_store((&memory), (u32)(i0 + 12), i1);
  i0 = l2;
  i1 = l7;
  i32_store8((&memory), (u32)(i0 + 11), i1);
  i0 = l2;
  i0 = i32_load((&memory), (u32)(i0 + 24));
  l8 = i0;
  i0 = l2;
  i0 = i32_load((&memory), (u32)(i0 + 20));
  l9 = i0;
  i0 = l2;
  i0 = i32_load((&memory), (u32)(i0 + 16));
  l10 = i0;
  i0 = l2;
  i0 = i32_load((&memory), (u32)(i0 + 12));
  l11 = i0;
  i0 = l8;
  i1 = l9;
  i2 = l10;
  i3 = l11;
  i4 = l6;
  i0 = f9(i0, i1, i2, i3, i4);
  l12 = i0;
  i0 = l3;
  l13 = i0;
  i0 = l12;
  l14 = i0;
  i0 = l13;
  i1 = l14;
  i0 = i0 != i1;
  l15 = i0;
  i0 = l15;
  l16 = i0;
  i0 = l16;
  i0 = !(i0);
  if (i0) {
    goto B1;
  }
  i0 = 0u;
  l17 = i0;
  i0 = l2;
  i1 = l17;
  i32_store((&memory), (u32)(i0 + 28), i1);
  goto B0;
B1:;
  i0 = l2;
  i0 = i32_load8_u((&memory), (u32)(i0 + 11));
  l18 = i0;
  i0 = 1u;
  l19 = i0;
  i0 = l18;
  i1 = l19;
  i0 &= i1;
  l20 = i0;
  i0 = l2;
  i1 = l20;
  i32_store((&memory), (u32)(i0 + 28), i1);
B0:;
  i0 = l2;
  i0 = i32_load((&memory), (u32)(i0 + 28));
  l21 = i0;
  i0 = 32u;
  l22 = i0;
  i0 = l2;
  i1 = l22;
  i0 += i1;
  l23 = i0;
  i0 = l23;
  g0 = i0;
  i0 = l21;
  goto Bfunc;
Bfunc:;
  FUNC_EPILOGUE;
  return i0;
}

/*
static u32 writev_c(u32 p0, u32 p1, u32 p2) {
  u32 l0 = 0, l1 = 0, l2 = 0, l3 = 0, l4 = 0, l5 = 0, l6 = 0, l7 = 0, l8 = 0,
      l9 = 0, l10 = 0, l11 = 0, l12 = 0, l13 = 0, l14 = 0, l15 = 0, l16 = 0,
      l17 = 0, l18 = 0, l19 = 0, l20 = 0, l21 = 0, l22 = 0, l23 = 0, l24 = 0,
      l25 = 0, l26 = 0, l27 = 0, l28 = 0, l29 = 0, l30 = 0, l31 = 0, l32 = 0,
      l33 = 0, l34 = 0, l35 = 0, l36 = 0, l37 = 0, l38 = 0, l39 = 0, l40 = 0,
      l41 = 0, l42 = 0, l43 = 0, l44 = 0, l45 = 0, l46 = 0, l47 = 0, l48 = 0,
      l49 = 0, l50 = 0;
  FUNC_PROLOGUE;
  u32 i0, i1;
  i0 = g0;
  l0 = i0;
  i0 = 32u;
  l1 = i0;
  i0 = l0;
  i1 = l1;
  i0 -= i1;
  l2 = i0;
  i0 = l2;
  g0 = i0;
  i0 = 0u;
  l3 = i0;
  i0 = l2;
  i1 = p0;
  i32_store((&memory), (u32)(i0 + 28), i1);
  i0 = l2;
  i1 = p1;
  i32_store((&memory), (u32)(i0 + 24), i1);
  i0 = l2;
  i1 = p2;
  i32_store((&memory), (u32)(i0 + 20), i1);
  i0 = l2;
  i1 = l3;
  i32_store((&memory), (u32)(i0 + 16), i1);
  i0 = l2;
  i1 = l3;
  i32_store((&memory), (u32)(i0 + 12), i1);
L1:
  i0 = l2;
  i0 = i32_load((&memory), (u32)(i0 + 12));
  l4 = i0;
  i0 = l2;
  i0 = i32_load((&memory), (u32)(i0 + 20));
  l5 = i0;
  i0 = l4;
  l6 = i0;
  i0 = l5;
  l7 = i0;
  i0 = l6;
  i1 = l7;
  i0 = (u32)((s32)i0 < (s32)i1);
  l8 = i0;
  i0 = l8;
  l9 = i0;
  i0 = l9;
  i0 = !(i0);
  if (i0) {
    goto B0;
  }
  i0 = 0u;
  l10 = i0;
  i0 = l2;
  i1 = l10;
  i32_store((&memory), (u32)(i0 + 8), i1);
L3:
  i0 = l2;
  i0 = i32_load((&memory), (u32)(i0 + 8));
  l11 = i0;
  i0 = l2;
  i0 = i32_load((&memory), (u32)(i0 + 24));
  l12 = i0;
  i0 = l2;
  i0 = i32_load((&memory), (u32)(i0 + 12));
  l13 = i0;
  i0 = 3u;
  l14 = i0;
  i0 = l13;
  i1 = l14;
  i0 <<= (i1 & 31);
  l15 = i0;
  i0 = l12;
  i1 = l15;
  i0 += i1;
  l16 = i0;
  i0 = l16;
  i0 = i32_load((&memory), (u32)(i0 + 4));
  l17 = i0;
  i0 = l11;
  l18 = i0;
  i0 = l17;
  l19 = i0;
  i0 = l18;
  i1 = l19;
  i0 = i0 < i1;
  l20 = i0;
  i0 = l20;
  l21 = i0;
  i0 = l21;
  i0 = !(i0);
  if (i0) {
    goto B2;
  }
  i0 = l2;
  i0 = i32_load((&memory), (u32)(i0 + 24));
  l22 = i0;
  i0 = l2;
  i0 = i32_load((&memory), (u32)(i0 + 12));
  l23 = i0;
  i0 = 3u;
  l24 = i0;
  i0 = l23;
  i1 = l24;
  i0 <<= (i1 & 31);
  l25 = i0;
  i0 = l22;
  i1 = l25;
  i0 += i1;
  l26 = i0;
  i0 = l26;
  i0 = i32_load((&memory), (u32)(i0));
  l27 = i0;
  i0 = l2;
  i0 = i32_load((&memory), (u32)(i0 + 8));
  l28 = i0;
  i0 = l27;
  i1 = l28;
  i0 += i1;
  l29 = i0;
  i0 = l29;
  i0 = i32_load8_u((&memory), (u32)(i0));
  l30 = i0;
  i0 = 24u;
  l31 = i0;
  i0 = l30;
  i1 = l31;
  i0 <<= (i1 & 31);
  l32 = i0;
  i0 = l32;
  i1 = l31;
  i0 = (u32)((s32)i0 >> (i1 & 31));
  l33 = i0;
  i0 = l33;
  putchar(i0);
  i0 = l2;
  i0 = i32_load((&memory), (u32)(i0 + 8));
  l34 = i0;
  i0 = 1u;
  l35 = i0;
  i0 = l34;
  i1 = l35;
  i0 += i1;
  l36 = i0;
  i0 = l2;
  i1 = l36;
  i32_store((&memory), (u32)(i0 + 8), i1);
  goto L3;
B2:;
  i0 = l2;
  i0 = i32_load((&memory), (u32)(i0 + 24));
  l37 = i0;
  i0 = l2;
  i0 = i32_load((&memory), (u32)(i0 + 12));
  l38 = i0;
  i0 = 3u;
  l39 = i0;
  i0 = l38;
  i1 = l39;
  i0 <<= (i1 & 31);
  l40 = i0;
  i0 = l37;
  i1 = l40;
  i0 += i1;
  l41 = i0;
  i0 = l41;
  i0 = i32_load((&memory), (u32)(i0 + 4));
  l42 = i0;
  i0 = l2;
  i0 = i32_load((&memory), (u32)(i0 + 16));
  l43 = i0;
  i0 = l43;
  i1 = l42;
  i0 += i1;
  l44 = i0;
  i0 = l2;
  i1 = l44;
  i32_store((&memory), (u32)(i0 + 16), i1);
  i0 = l2;
  i0 = i32_load((&memory), (u32)(i0 + 12));
  l45 = i0;
  i0 = 1u;
  l46 = i0;
  i0 = l45;
  i1 = l46;
  i0 += i1;
  l47 = i0;
  i0 = l2;
  i1 = l47;
  i32_store((&memory), (u32)(i0 + 12), i1);
  goto L1;
B0:;
  i0 = l2;
  i0 = i32_load((&memory), (u32)(i0 + 16));
  l48 = i0;
  i0 = 32u;
  l49 = i0;
  i0 = l2;
  i1 = l49;
  i0 += i1;
  l50 = i0;
  i0 = l50;
  g0 = i0;
  i0 = l48;
  goto Bfunc;
Bfunc:;
  FUNC_EPILOGUE;
  return i0;
}
*/

u8 pb[] = { 0xE4, 0x47, 0x30, 0x10, 0x61, 0x24, 0x52, 0x21, 0x86, 0x40, 0xAD,
            0xC1, 0xA0, 0xB4, 0x50, 0x22, 0xD0, 0x75, 0x32, 0x48, 0x24, 0x86,
            0xE3, 0x48, 0xA1, 0x85, 0x36, 0x6D, 0xCC, 0x33, 0x7B, 0x6E, 0x93,
            0x7F, 0x73, 0x61, 0xA0, 0xF6, 0x86, 0xEA, 0x55, 0x48, 0x2A, 0xB3,
            0xFF, 0x6F, 0x91, 0x90, 0xA1, 0x93, 0x70, 0x7A, 0x06, 0x2A, 0x6A,
            0x66, 0x64, 0xCA, 0x94, 0x20, 0x4C, 0x10, 0x61, 0x53, 0x77, 0x72,
            0x42, 0xE9, 0x8C, 0x30, 0x2D, 0xF3, 0x6F, 0x6F, 0xB1, 0x91, 0x65,
            0x24, 0x0A, 0x14, 0x21, 0x42, 0xA3, 0xEF, 0x6F, 0x55, 0x97, 0xD6 };

//void success() { puts("ok"); }
//void failure() { puts("bad"); }
//
//u32 test2(u32 *input) {
//  char *sneaky = "SOSNEAKY";
//
//  return strcmp((const char *)input, sneaky) == 0;
//}
//char *sneaky = "SOSNEAKY";
//
//int authenticate(char *username) {
//  // if (username[0] == 'a') return 1;
//  char *sneaky = "SO";
//  if (strcmp(username, sneaky) == 0) return 1;
//  return 0;
//}

static const u8 data_segment_data_0[] = {
  0x01, 0x00, 0x00, 0x00, 0x02, 0x00, 0x00, 0x00, 0x03, 0x00,
  0x00, 0x00, 0x04, 0x00, 0x00, 0x00, 0x05, 0x00, 0x00, 0x00,
  0x06, 0x00, 0x00, 0x00, 0x07, 0x00, 0x00, 0x00,
};

#define memcpya(a, b, c) {for (int i=0; i<(c); ++i) ((char*)a)[i] = ((char*)b)[i];}
#define memseta(a, b, c) {for (int i=0; i<(c); ++i) ((char*)a)[i] = (b);}

u32 test(u32 *input, u32 inputlen) {

  g0 = 66592u;
  ((char *)input)[inputlen] = 0;
  memcpya(&(buf[1024u]), data_segment_data_0, 28);

  int p1 = ORIG_LEN;
  memcpya(buf + p1, input, inputlen);
  int p2 = p1 + (inputlen + 64) & ~63;
  int pblen = sizeof(pb);
  memcpya(buf + p2, pb, pblen);
  memseta(buf + p2+pblen, 0, 3*pblen);

  if (Match((u32)p2, pblen, (u32)p1, inputlen) == 1) {
    //success();
    return 1;
  } else {
    //failure();
    return 0;
  }
}

//void _start(){
//
//  test(0, 0);
//}

//u32 __attribute__ ((noinline))  test_wrap(u32 *input, u32 *inputlen){
//  return test(input, *inputlen);
//}
//
//void __attribute__ ((noinline))  test_end(int res){
//  asm("");
//  printf("FUU %d\n", res);
//
//}
//
//u32 g_buf[100];
//u32 g_len;
//
void go(){
  char bb[1000];
  int n;
  FILE *f = fopen("./data.in", "rb");
  fread(&n, 4, 1, f);
  fread(bb, n, 1, f);
  fclose(f);
  //while(1){
  //  int res = test_wrap(g_buf, &g_len);
  //  test_end(res);
  //}

}

int main() {
  go();
  return 0;
}
