#include <cstdio>
#include <cstdlib>
#include <ctype.h>
#include <cstring>
#include <cassert>

extern "C" {
bool Java_com_flareon_flare_ValidateActivity_validate(void *buf);
}
char BUF[100];
int pos;

const char *func1(void *useless) {
  // printf("ON FUCN1 >> %p\n", useless);
  return BUF;
}

void func2(void *a, void *b, void *c) {
  // printf("RECV FUNC2 >> %p %p %p >> %s\n", a, b, c);
}

void func3(void *a, void *str) {
  char *tmp = (char *)str;
  int x = strlen(tmp);
  if (x != 2) {
    printf("SOL IS <<%s>>\n", BUF);
  }
}

int main(int argc, char **argv) {
  int len = 0x300;
  int offset1 = 0x2a4;
  int offset2 = 0x2a8;
  int offset3 = 0x29c;

  char obj[len];
  *(char **)(obj + offset1) = (char *)func1;
  *(char **)(obj + offset2) = (char *)func2;
  *(char **)(obj + offset3) = (char *)func3;
  void *tmp = obj;

  char msg[200];
  fgets(msg, 100, stdin);
  pos = strlen(msg);
  memcpy(BUF, msg, pos);
  BUF[pos]=0;
  printf("BONJOUR, trying <%s>\n", BUF);

  for (int i = 0; i < 256; ++i) {
    for (int j = 0; j < 256; ++j) {
      if (!isprint(i) || !isprint(j)) continue;
      BUF[pos] = i;
      BUF[pos + 1] = j;
      BUF[pos + 2] = 0;
      Java_com_flareon_flare_ValidateActivity_validate(&tmp);
    }
  }

  printf("DONE KAPPA, last try: <%s>\n", BUF);
  Java_com_flareon_flare_ValidateActivity_validate(&tmp);
  return 1;

  return 0;
}
