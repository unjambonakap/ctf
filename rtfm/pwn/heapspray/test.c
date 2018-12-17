#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>

typedef uint64_t u64;

int main() {
  int sz = 0x10;
  for (int i =0 ; i< 100; ++i){
    u64 *x = (u64*)&sz;
    printf("%016Lx\n", x[i]);
  }
  return;
  srand(0);
  (u64 ***)malloc(0x1000);

  u64 ***tb0 = (u64 ***)malloc(sz);
  u64 ***tb1 = (u64 ***)malloc(sz);
  u64 ***tb2 = (u64 ***)malloc(sz);
  u64 ***tb3 = (u64 ***)malloc(sz);

  u64 ***tgt = tb1;
  int range = 5;
  free(tgt);
  for (int i = -range; i < range; ++i) printf("%p %d\n", tgt[i], i);

  if (0) {
    puts("===");
    tgt = (u64 ***)tgt[3];
    for (int i = -range; i < range; ++i) printf("%p %d\n", tgt[i], i);
  }
  for (int i=0; i<1000; ++i){


  }

  scanf("%d", &sz);
  return 0;
}
