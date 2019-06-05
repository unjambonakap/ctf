
#include <cstdint>
#include <cstdio>
#include <cstdlib>
#include <cstring>
#include <string>
extern "C" {
int64_t gogo(char *data);
void good() { puts("good"); }
void bad() { puts("bad"); }
}

uint64_t go(char *data, const char *key) {
  int pos_key = 0x10000;
  int pos_check = 0x10020;
  for (int i=0; i<8; ++i){
    data[pos_key+i] = key[i];
  }
  gogo(data);
  for (int i=0; i<8; ++i){
    if (data[pos_key+i] != data[pos_check+i]) return 0;
  }
  return true;
}

int main(int argc, char **argv) {
  FILE *f = fopen("./data.bin", "rb");
  int sz = 0x10040;
  char *data = (char*)malloc(sz);
  fread(data, 1, sz, f);
  uint64_t res = 0;
  res = go(data, argv[1]);
  if (res) {
    good();
  } else
    bad();

  free(data);
  return 0;
}
