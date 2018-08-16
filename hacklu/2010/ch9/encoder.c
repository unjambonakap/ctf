// gcc -Wall -o encoder encoder.c base128.c base32.c base64.c
// save file & compile in iodine-0.6.0-rc1/src/
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <string.h>
#include "encoding.h"
#include "base32.h"
#include "base64.h"
#include "base128.h"

static struct encoder *enc;
char in[4096], out[4096];
size_t outlen;

int main(int argc, char **argv) {
  if (argc < 3) {
    printf("Usage: %s <32|64|128> <e|d>\n", argv[0]);
    exit(1);
  }

  if (!strcmp(argv[1], "32")) enc = get_base32_encoder();
  else if (!strcmp(argv[1], "64")) enc = get_base64_encoder();
  else enc = get_base128_encoder();

  outlen = sizeof(out);
  fgets(in, sizeof(in), stdin);
  if (!strcmp(argv[2],"e"))
    enc->encode(out, &outlen, in, strlen(in));
  else
    enc->decode(out, &outlen, in, strlen(in));

  out[outlen] = 0;
  write(1, out, outlen);
  return 0;
}
