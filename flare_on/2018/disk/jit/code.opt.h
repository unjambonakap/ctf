void hook_disp() {

  if (T(4)) {
    if (REAL) {
      printf("GOT CHAR >> %03d %c\n", T(2) & 0xff, T(2) & 0xff);
    }
    Ts(4) = 0;
    Ts(2) = 0;
  }
}

void *func_235();

void *func_590();

void *func_593();

void *func_742();

void *func_812();

void *func_815();

void *func_994();

void *func_1481();

void *func_1485();

void *func_1604();

void *func_1804();

void *func_1807();

void *func_1813();

void *func_1816();

void *func_1889();

void *func_1916();

void *func_1919();

void *func_1935();
void init() {
  func_data[235] = func_235;
  func_data[590] = func_590;
  func_data[593] = func_593;
  func_data[742] = func_742;
  func_data[812] = func_812;
  func_data[815] = func_815;
  func_data[994] = func_994;
  func_data[1481] = func_1481;
  func_data[1485] = func_1485;
  func_data[1604] = func_1604;
  func_data[1804] = func_1804;
  func_data[1807] = func_1807;
  func_data[1813] = func_1813;
  func_data[1816] = func_1816;
  func_data[1889] = func_1889;
  func_data[1916] = func_1916;
  func_data[1919] = func_1919;
  func_data[1935] = func_1935;
}

void *func_1916() {
  Ts(0) = 0;
  return nullptr;
  // NXT >>>  1935
}

void *func_1919() {
  Ts(0) = 0;
  return nullptr;
  // NXT >>>  1935
}

void *func_1935() {
  if (0) {
  }
  return nullptr;
  // NXT >>>  742
}

void *func_1481() {

  assert(0);
  return nullptr;
  // NXT >>>  1604
}

void *func_1485() {

  if (0) {
  } else {
  }
  return nullptr;
}
void *func_1804() {
  Ts(0) = 0;
  // NXT >>>  1813
  return nullptr;
}

void *func_1807() {
  // T(0) = 0;
  // T(1819) -= T(0);
  return nullptr;

  // NXT >>>  1813
  // NXT >>>  1816
}
void *func_1813() {
  // NXT >>>  1889
  return nullptr;
}

void *func_1816() {
  Ts(0) = 0;
  return (void *)func_1889;
  // NXT >>>  1889
}

void *func_1889() {
  if (0) {
  }

  return nullptr;

  // NXT >>>  1916
  // NXT >>>  1919
}

void *func_590() {
  if (0) {
  } else {

    // NXT >>>  1481
    // NXT >>>  1485
  }
  // NXT >>>  1481
  // NXT >>>  1485
  return nullptr;
}

void *func_812() {
  Ts(0) = 0;
  Ts(0) = 0;
  return (void *)func_994;
  // NXT >>>  994
}

void *func_815() {

  if (0) {
  } else {
    return (void *)func_994;
  }
  return nullptr;
}

void *func_994() {

  if (0) {
  } else {
  }
  return nullptr;

  // NXT >>>  590
  // NXT >>>  593
}

// =============== UP HERE OBSOLETE
// =============== UP HERE OBSOLETE
// =============== UP HERE OBSOLETE
// =============== UP HERE OBSOLETE
// =============== UP HERE OBSOLETE

void *func_235() {
  Ts(0) = 0;
  Ts(0) = 0;
  return nullptr;
}

void *func_593() {
  // ON END PATH

  Ts(389) = T(271);
  Ts(0) = 0;
  Ts(1266) = 0;
  Ts(0) -= T(389);
  Ts(1266) -= T(0);
  Ts(1267) = T(389);
  Ts(1273) = T(389);
  Ts(0) = 0;
  Ts(T(1267)) -= T(T(1266));
  Ts(0) -= 347;
  Ts(T(1273)) -= T(0);
  return (void *)func_235;
  // NXT >>>  235
}

// ====== END FUNCTION ABOVE
// ====== END FUNCTION ABOVE
// ====== END FUNCTION ABOVE

void *func_742() {

  if ((int16_t)T(2044) >= (int16_t)1) {
    Ts(2044) = 0;
    Ts(2) += T(2042);
    Ts(4) += 1;
    hook_disp();
    Ts(2042) = 0;
  }

  // there was this
  // T(389) = T(271) + 5;
  // T(1069) = T(T(389)) - T(421);

  // T(529) = T(385);
  // T(529) -= 9655;
  Ts(2031) = T(2038 + T(2038));
  /*
2038: init at 3317
2040: 0 -> easy invert result, 0 not overriden
2039: result of last diff
2041: result of last diff with arg2 == 2
store diff at 2039 at other

     */

  if ((int16_t)T(2031) <= -2)
    // END FUNC
    return (void *)func_593;
  else {

    // 2038 -> store current operation id
    // 2031:-> action id

    if ((int16_t)T(2031) >= 0) {
      //  return (void *)func_1481;

      int ia = 2038 + T(2031);
      int va = T(ia);
      int ib = 2039;
      int vb = T(ib);
      uint16_t r1 = va; // sometimes password here
      uint16_t r2 = vb;
      int curop = T(2038);
      // compare two things

      Ts(ib) = r1 - r2;

      if ((int16_t)T(2031) != 2) {
        Ts(ia) = r1 - r2;
      } else {
        Ts(2041) = r1 - r2;
      }

      if (REAL){
      printf("COMPARE %d %d %d %d RES >> %d >> OP %d, fixed=%d\n", ia-2038, ib-2038, (int16_t)r1,
             (int16_t)r2, int16_t(r1 - r2), curop, fixed_mem.count(ia));
      }

      if ((int16_t)r1 < (int16_t)r2) {
        Ts(2038)++;
      }
    } else {
      if (REAL)
      printf("NOP %d\n", T(2038));

    }
    Ts(2038)++;
  }
  return (void *)func_742; // probably func_742
}

void *func_1604() {
  Ts(2033)++; // probably T(1311)

  uint16_t r1 = T(2038 + T(2031)); // sometimes password here
  uint16_t r2 = T(T(2033));
  printf("INIT OP %d %d xx check %d\n", T(2031), T(2038), T(2038 + T(2038)));

  Ts(2033) = 2038 + 1;
  Ts(2038 + 1) = r1 - r2;

  if ((int16_t)T(2031) != 2) Ts(2033) = 2038;
  Ts(2033) += T(2031);
  Ts(T(2033)) = r1 - r2;
  printf("INIT OP %d %d TO %d\n", r1, r2, Ts(2033));

  if ((int16_t)r1 < (int16_t)r2) {
    Ts(2038)++;
  }

  Ts(2038)++;
  return (void *)func_742;
}

func_t entry_func() { return func_1604; }
// ENTRY >>  1604
