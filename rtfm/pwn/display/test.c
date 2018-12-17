#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>


int main() {
  char *tmp2 = (char *)malloc(0x100);
  char *tmp3 = (char *)malloc(0x100);
  char *tmp = (char *)malloc(0x100);
  char *tmp1 = (char *)malloc(0x100);
  printf("AAAT %p\n", tmp);
  printf("AAAT %p\n", tmp1);
  printf("AAAT %p\n", tmp2);
  printf("AAAT %p\n", tmp3);
  memset(tmp, 'a', 0x100);
  memset(tmp1, 'a', 0x100);
  memset(tmp2, 'a', 0x100);
  memset(tmp3, 'a', 0x100);
  free(tmp2);
  free(tmp1);

  for (int j=-5; j<5; ++j) printf("%d\t%016Lx\n", j, *(((uint64_t*)tmp)+j));
  free(tmp);
  puts("");
  for (int j=-5; j<5; ++j) printf("%d\t%016Lx\n", j, *(((uint64_t*)tmp)+j));
  puts("");
  return 0;
}
