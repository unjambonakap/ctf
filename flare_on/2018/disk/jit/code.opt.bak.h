void hook_disp() {

  if (tb[4]) {
    printf("GOT CHAR >> %03d %c\n", tb[2] & 0xff, tb[2] & 0xff);
    tb[4] = 0;
    tb[2] = 0;
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
  tb[0] = 0;
  return nullptr;
  // NXT >>>  1935
}

void *func_1919() {
  tb[0] = 0;
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
  tb[0] = 0;
  // NXT >>>  1813
  return nullptr;
}

void *func_1807() {
  // tb[0] = 0;
  // tb[1819] -= tb[0];
  return nullptr;

  // NXT >>>  1813
  // NXT >>>  1816
}
void *func_1813() {
  // NXT >>>  1889
  return nullptr;
}

void *func_1816() {
  tb[0] = 0;
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
  tb[0] = 0;
  tb[0] = 0;
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
  tb[251] -= 2;
  tb[0] = 0;
  tb[0] = 0;
  exit(1);
  return nullptr;
}

void *func_593() {
  // ON END PATH

  tb[389] = tb[271];
  tb[0] = 0;
  tb[1266] = 0;
  tb[0] -= tb[389];
  tb[1266] -= tb[0];
  tb[1267] = tb[389];
  tb[1273] = tb[389];
  tb[0] = 0;
  tb[tb[1267]] -= tb[tb[1266]];
  tb[0] -= 347;
  tb[tb[1273]] -= tb[0];
  tb[0] = 0;
  tb[0] = 0;
  tb[251] -= 1;
  tb[1300] = 0;
  tb[0] -= tb[251];
  tb[1300] -= tb[0];
  tb[1311] = tb[tb[1300]];
  tb[0] = 0;
  tb[0] = 0;
  return (void *)get_func(tb[1311]);
  // NXT >>>  235
}


// ====== END FUNCTION ABOVE
// ====== END FUNCTION ABOVE
// ====== END FUNCTION ABOVE



void *func_742() {

  tb[251] -= 1;
  tb[389] = tb[271] + 6;

  if ((int16_t)tb[tb[389]] >= (int16_t)tb[421]) {
    tb[tb[389]] = tb[425];
    tb[389] = tb[271] + 4;
    tb[2] += tb[tb[389]];
    tb[4] += 1;
    hook_disp();
    tb[tb[389]] = tb[425];
  }

  // there was this
  //tb[389] = tb[271] + 5;
  //tb[1069] = tb[tb[389]] - tb[421];

  tb[389] = tb[271];

  //tb[529] = tb[385];
  //tb[529] -= 9655;

  tb[389] += tb[tb[389]];

  if ((int16_t)tb[tb[389]] <= -2)
    // END FUNC
    return (void *)func_593;
  else {

    tb[tb[251]] = tb[271];
    tb[251] += 1;
    tb[tb[251]] = 742;
    tb[251] += 1;

    tb[1331] = tb[271];
    tb[2033] = tb[1331];

    tb[2037] = tb[tb[271]];
    tb[2033] += tb[2037];
    tb[2031] = tb[tb[2033]];

    if ((int16_t)tb[2031] + 1 <= 0) {
      //  return (void *)func_1485;
      tb[2037] += 1;
      tb[tb[1331]] = tb[2037];
      tb[251] -= 1;
      return (void *)get_func(tb[tb[251]]); // probably func_742
    } else {
      //  return (void *)func_1481;
      tb[2033] = tb[1331];
      return (void *)func_1604;
    }
  }
}

void *func_1604() {
  tb[2033]++; // probably tb[1311]

  tb[1677] = tb[1331] + tb[2031];

  tb[2030] = tb[tb[1677]] - tb[tb[2033]];

  tb[2033] = tb[1331] + 1;
  tb[tb[1331] + 1] = tb[2030];
  tb[1819] = tb[2031] - 2;

  if ((int16_t)tb[1819] != 0) tb[2033] = tb[1331];
  tb[2033] += tb[2031];
  tb[tb[2033]] = tb[2030];
  tb[2037] = tb[tb[1331]];

  if (((int16_t)tb[2030]) < 0) {
    tb[2037]++;
  }

  tb[2037]++;
  tb[tb[1331]] = tb[2037];
  tb[251]--;
  return (void *)get_func(tb[tb[251]]);
}

func_t entry_func() { return func_1604; }
// ENTRY >>  1604
