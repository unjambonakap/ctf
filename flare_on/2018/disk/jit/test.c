#include <stdint.h>
#include <stdio.h>

void func(uint16_t *tb) {

branch_1475:
  tb[0] -= tb[0];
  tb[1484] -= tb[0];

  if (tb[1484] <= 0)
    goto branch_1485;
  else
    goto branch_1481;

branch_1485:
  puts("1");
  return;
branch_1481:
  puts("2");
}

