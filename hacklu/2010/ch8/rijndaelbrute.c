#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <unistd.h>
#include "rijndael.h"

#define ALPHA "\x00qwertasdfgzxcvb"
#define KEYLEN 16

unsigned char cipher[] = {
0x40, 0x40, 0xa9, 0x8a, 0xd1, 0xae, 0x25, 0xdf, 0x8b, 0xe9,
0x7d, 0xf6, 0x5f, 0x90, 0xa9, 0x80, 0x97, 0xf3, 0x95, 0x80,
0xe4, 0x11, 0x65, 0x55, 0x0a, 0xdc, 0xf8, 0x29, 0x41, 0x7b,
0x00, 0x2c, 0x0f, 0x81, 0xb3, 0xb1, 0xbc, 0xdc, 0x83, 0x91,
0x1e, 0x06, 0x52, 0xd8, 0xa9, 0x28, 0x04, 0x35, 0x41, 0x6a,
0x33, 0x2f, 0x7a, 0x3f, 0x8b, 0x34, 0x91, 0x24, 0x9b, 0x3b,
0x66, 0x96, 0x25, 0x0c, 0x4c, 0x24, 0x36, 0xe6, 0x62, 0x1d,
0x0c, 0xf2, 0x38, 0x2b, 0x2d, 0x7e, 0x24, 0x8f, 0x08, 0x76,
0x92, 0xd0, 0x6a, 0xeb, 0x23, 0x29, 0x1b, 0x47, 0x96, 0x24,
0x45, 0xcd, 0x76, 0x47, 0x99, 0xdf, 0x49, 0x7c, 0xf2, 0xc3,
0xcc, 0x02, 0xd1, 0xbe, 0xb7, 0xe1, 0xae, 0xed, 0xe6, 0x82,
0x37, 0x30, 0xc3, 0xd2, 0x92, 0x08, 0x0f, 0xde, 0xa5, 0x21,
0xd9, 0x8b, 0xf8, 0xde, 0x60, 0x7c, 0x0e, 0x29};

void brute(int thread, int threads_num, int offset) {
    unsigned long rijndael_buffer[RKLENGTH(KEYLEN*8)];
    unsigned char key[KEYLEN+1] = "wcwteseawx";
    unsigned int pos[KEYLEN];
    unsigned char plain[KEYLEN+1];
    int i;
    
    int nrounds = NROUNDS(KEYLEN*8);
    
    unsigned char *keyb = key + strlen((char*)key);
    
    for (i = 0; i < KEYLEN; i++)
        pos[i] = 0;

    while (1) {

        rijndaelSetupDecrypt(rijndael_buffer, key, KEYLEN*8);
        rijndaelDecrypt(rijndael_buffer, nrounds, cipher, plain);
        
        //plain starts with 674e
        if (plain[0] == '6' && plain[1] == '7' &&
            plain[2] == '4' && plain[3] == 'e') {
            
            printf("Key: %s\n", key);

            printf("Text: ");
            for (i = 0; i < sizeof(cipher)/KEYLEN; i++) {
                rijndaelDecrypt(rijndael_buffer, nrounds, cipher, plain);
                plain[KEYLEN] = 0;
                printf("%s", plain);
            }
            printf("\n");
            
        }
        
        int add = 1, nesting = 0;
        while (add) {
        
            if (nesting == 0)
                pos[nesting] += threads_num;
            else
                pos[nesting]++;

            if (pos[nesting] < sizeof(ALPHA)-1) {
                add = 0;
            } else {
                pos[nesting] = 1;
                if (nesting == 0) {
                    pos[nesting] += offset;
                }
            }
            
            keyb[nesting] = ALPHA[pos[nesting]];
            nesting++;
            
            if (add && keyb+nesting >= key+KEYLEN) {
                return;
            }
        }
        
    }
}

int main(int argc, char * argv[]) {

    if (argc != 2) {
        printf("Usage: %s <number_of_threads>\n", argv[0]);
        return 1;
    }
    int nfork = atoi(argv[1]);
    
    int offset = 0;
    int nf = nfork;
    while (nf) {
        if (fork())
            nf -= 1;
        else break;
        offset++;
    }

    if (nf == 0) {
        int status, i;
        for (i = 0; i < nfork; i++)
            wait(&status);
        printf("Bruteforce ended\n");
        return 0;
    }
    
    brute(nf, nfork, offset);
    
    return 0;
    
}
