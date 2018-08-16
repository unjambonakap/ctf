// gcc -Wall -lz -o uncompress uncompress.c
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <string.h>
#include <zlib.h>

char in[4096], out[4096];
size_t outlen;

int main(int argc, char **argv) {
  int ret;
  memset(in,0,sizeof(in));
  read(0, in, sizeof(in));
  outlen = sizeof(out);
  ret = uncompress((unsigned char*)out, &outlen, (unsigned char*)in, sizeof(in));
  if (ret == Z_OK)
    write(1, out, outlen);
  return ret;
}
