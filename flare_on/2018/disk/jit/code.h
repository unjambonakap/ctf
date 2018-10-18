

void hook_disp(){

    if (tb[4]){
    printf("GOT CHAR >> %d %c\n", tb[2]&0xff, tb[2]&0xff);
    tb[4] = 0;
    tb[2] = 0;
    }
}




void* func_235();
void* func_590();
void* func_593();
void* func_742();
void* func_812();
void* func_815();
void* func_994();
void* func_1481();
void* func_1485();
void* func_1604();
void* func_1804();
void* func_1807();
void* func_1813();
void* func_1816();
void* func_1889();
void* func_1916();
void* func_1919();
void* func_1935();
void init(){
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
void* func_235(){
tb[251] -= 2;
tb[0] = 0;
tb[0] = 0;
exit(1); return nullptr;
}
void* func_590(){
tb[633] = tb[251];
tb[0] = 0;
tb[634] = 0;
tb[0] -= tb[251];
tb[634] -= tb[0];
tb[640] = tb[251];
tb[0] = 0;
tb[tb[634]] -= tb[tb[633]];
tb[0] -= tb[271];
tb[tb[640]] -= tb[0];
tb[251] += 1;
tb[0] = 0;
tb[661] = 742;
tb[0] = 0;
tb[714] = tb[251];
tb[0] = 0;
tb[715] = 0;
tb[0] -= tb[251];
tb[715] -= tb[0];
tb[721] = tb[251];
tb[0] = 0;
tb[tb[715]] -= tb[tb[714]];
tb[0] -= tb[661];
tb[tb[721]] -= tb[0];
tb[251] += 1;
tb[0] = 0;
tb[0] = 0;
tb[1315] = tb[251];
tb[0] = 0;
tb[0] = 0;
tb[0] = 0;
tb[1339] = -2;
tb[0] = 0;
tb[0] -= tb[1315];
tb[1339] -= tb[0];
tb[1376] = tb[1339];
tb[0] = 0;
tb[1331] = 0;
tb[0] -= tb[tb[1376]];
tb[1331] -= tb[0];
tb[2033] = tb[1331];
tb[0] = 0;
tb[1412] = 0;
tb[0] -= tb[2033];
tb[1412] -= tb[0];
tb[2037] = tb[tb[1412]];
tb[0] = 0;
tb[0] -= tb[2037];
tb[2033] -= tb[0];
tb[1445] = tb[2033];
tb[0] = 0;
tb[2031] = 0;
tb[0] -= tb[tb[1445]];
tb[2031] -= tb[0];
tb[1484] = tb[2031];
tb[0] = 0;
tb[1484] -= -1;
tb[0] -= tb[1484];
tb[0] = 0;
tb[1484] -= tb[0];

  if ((int16_t)tb[1484] <= 0) return (void*)func_1485;
  else return (void*)func_1481;
  
// NXT >>>  1481
// NXT >>>  1485
}
void* func_593(){
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
return (void*)get_func(tb[1311]);
// NXT >>>  235
}
void* func_742(){
tb[251] -= 1;
tb[389] = tb[271];
tb[0] = 0;
tb[0] -= 6;
tb[389] -= tb[0];
tb[785] = tb[389];
tb[0] = 0;
tb[417] = 0;
tb[0] -= tb[tb[785]];
tb[417] -= tb[0];
tb[824] = tb[417];
tb[0] = 0;
tb[824] -= tb[421];
tb[0] -= tb[824];

  if ((int16_t)tb[0] <= 0) return (void*)func_815;
  else return (void*)func_812;
  
// NXT >>>  812
// NXT >>>  815
}
void* func_812(){
tb[0] = 0;
tb[0] = 0;
return (void*)func_994;
// NXT >>>  994
}
void* func_815(){
tb[0] = 0;
tb[824] -= tb[0];
tb[861] = 0;
tb[0] -= tb[389];
tb[861] -= tb[0];
tb[862] = tb[389];
tb[868] = tb[389];
tb[0] = 0;
tb[tb[862]] -= tb[tb[861]];
tb[0] -= tb[425];
tb[tb[868]] -= tb[0];
tb[389] = tb[271];
tb[0] = 0;
tb[0] -= 4;
tb[389] -= tb[0];
tb[909] = tb[389];
tb[417] = tb[tb[909]];
tb[0] = 0;
tb[0] -= tb[417];
tb[2] -= tb[0];
tb[0] = 0;
tb[0] -= 1;
tb[4] -= tb[0];
hook_disp();
tb[0] = 0;
tb[982] = tb[389];
tb[0] = 0;
tb[983] = 0;
tb[0] -= tb[389];
tb[983] -= tb[0];
tb[989] = tb[389];
tb[0] = 0;
tb[tb[983]] -= tb[tb[982]];
tb[0] -= tb[425];
tb[tb[989]] -= tb[0];
tb[0] = 0;
return (void*)func_994;
// NXT >>>  994
}
void* func_994(){
tb[389] = 0;
tb[0] -= tb[271];
tb[389] -= tb[0];
tb[0] = 0;
tb[0] -= 5;
tb[389] -= tb[0];
tb[1030] = tb[389];
tb[0] = 0;
tb[417] = 0;
tb[0] -= tb[tb[1030]];
tb[417] -= tb[0];
tb[1069] = tb[417];
tb[0] = 0;
tb[1069] -= tb[421];
tb[0] -= tb[1069];
tb[0] = 0;
tb[0] = 0;
tb[389] = tb[271];
tb[0] = 0;
tb[493] = 0;
tb[0] -= tb[389];
tb[493] -= tb[0];
tb[385] = tb[tb[493]];
tb[529] = tb[385];
tb[0] = 0;
tb[529] -= 9655;
tb[0] -= tb[529];
tb[0] = 0;
tb[0] -= tb[385];
tb[389] -= tb[0];
tb[554] = tb[389];
tb[0] = 0;
tb[393] = 0;
tb[0] -= tb[tb[554]];
tb[393] -= tb[0];
tb[596] = tb[393];
tb[0] = 0;
tb[596] -= -2;
tb[0] -= tb[596];
tb[0] = 0;
tb[596] -= tb[0];

  if ((int16_t)tb[596] <= 0) return (void*)func_593;
  else return (void*)func_590;
  
// NXT >>>  590
// NXT >>>  593
}
void* func_1481(){
tb[2033] = tb[1331];
tb[0] = 0;
return (void*)func_1604;
// NXT >>>  1604
}
void* func_1485(){
tb[2033] = 0;
tb[0] -= tb[1331];
tb[2033] -= tb[0];
tb[0] = 0;
tb[0] = 0;
tb[0] -= 1;
tb[2037] -= tb[0];
tb[1546] = tb[2033];
tb[0] = 0;
tb[1547] = 0;
tb[0] -= tb[2033];
tb[1547] -= tb[0];
tb[1553] = tb[2033];
tb[0] = 0;
tb[tb[1547]] -= tb[tb[1546]];
tb[0] -= tb[2037];
tb[tb[1553]] -= tb[0];
tb[0] = 0;
tb[0] = 0;
tb[251] -= 1;
tb[1580] = 0;
tb[0] -= tb[251];
tb[1580] -= tb[0];
tb[1591] = tb[tb[1580]];
tb[0] = 0;
tb[0] = 0;
return (void*)get_func(tb[1591]);
// NXT >>>  742
}
void* func_1604(){
tb[0] = 0;
tb[0] -= 1;
tb[2033] -= tb[0];
tb[1632] = tb[2033];
tb[0] = 0;
tb[2030] = 0;
tb[0] -= tb[tb[1632]];
tb[2030] -= tb[0];
tb[2033] = tb[1331];
tb[0] = 0;
tb[0] -= tb[2031];
tb[2033] -= tb[0];
tb[1677] = tb[2033];
tb[0] = 0;
tb[2032] = 0;
tb[0] -= tb[tb[1677]];
tb[2032] -= tb[0];
tb[2036] = tb[2032];
tb[0] = 0;
tb[2036] -= tb[2030];
tb[2030] = 0;
tb[0] -= tb[2036];
tb[2030] -= tb[0];
tb[2033] = tb[1331];
tb[0] = 0;
tb[0] = 0;
tb[0] -= 1;
tb[2033] -= tb[0];
tb[1774] = tb[2033];
tb[0] = 0;
tb[1775] = 0;
tb[0] -= tb[2033];
tb[1775] -= tb[0];
tb[1781] = tb[2033];
tb[0] = 0;
tb[tb[1775]] -= tb[tb[1774]];
tb[0] -= tb[2030];
tb[tb[1781]] -= tb[0];
tb[1819] = tb[2031];
tb[0] = 0;
tb[1819] -= 2;
tb[0] -= tb[1819];

  if ((int16_t)tb[0] <= 0) return (void*)func_1807;
  else return (void*)func_1804;
  
// NXT >>>  1804
// NXT >>>  1807
}
void* func_1804(){
tb[0] = 0;
return (void*)func_1813;
// NXT >>>  1813
}
void* func_1807(){
tb[0] = 0;
tb[1819] -= tb[0];

  if ((int16_t)tb[1819] <= 0) return (void*)func_1816;
  else return (void*)func_1813;
  
// NXT >>>  1813
// NXT >>>  1816
}
void* func_1813(){
tb[2033] = tb[1331];
tb[0] = 0;
tb[0] -= tb[2031];
tb[2033] -= tb[0];
tb[1877] = tb[2033];
tb[0] = 0;
tb[1878] = 0;
tb[0] -= tb[2033];
tb[1878] -= tb[0];
tb[1884] = tb[2033];
tb[0] = 0;
tb[tb[1878]] -= tb[tb[1877]];
tb[0] -= tb[2030];
tb[tb[1884]] -= tb[0];
tb[0] = 0;
return (void*)func_1889;
// NXT >>>  1889
}
void* func_1816(){
tb[0] = 0;
return (void*)func_1889;
// NXT >>>  1889
}
void* func_1889(){
tb[1904] = 0;
tb[0] -= tb[1331];
tb[1904] -= tb[0];
tb[2037] = tb[tb[1904]];
tb[0] = 0;
tb[0] -= tb[2030];

  if ((int16_t)tb[0] <= 0) return (void*)func_1919;
  else return (void*)func_1916;
  
// NXT >>>  1916
// NXT >>>  1919
}
void* func_1916(){
tb[2037] += 1;
tb[0] = 0;
return (void*)func_1935;
// NXT >>>  1935
}
void* func_1919(){
tb[0] = 0;
return (void*)func_1935;
// NXT >>>  1935
}
void* func_1935(){
tb[0] = 0;
tb[0] -= 1;
tb[2037] -= tb[0];
tb[1984] = tb[1331];
tb[0] = 0;
tb[1985] = 0;
tb[0] -= tb[1331];
tb[1985] -= tb[0];
tb[1991] = tb[1331];
tb[0] = 0;
tb[tb[1985]] -= tb[tb[1984]];
tb[0] -= tb[2037];
tb[tb[1991]] -= tb[0];
tb[0] = 0;
tb[0] = 0;
tb[251] -= 1;
tb[2018] = 0;
tb[0] -= tb[251];
tb[2018] -= tb[0];
tb[2029] = tb[tb[2018]];
tb[0] = 0;
tb[0] = 0;
return (void*)get_func(tb[2029]);
// NXT >>>  742
}

func_t entry_func(){
return func_1604;
}
// ENTRY >>  1604
