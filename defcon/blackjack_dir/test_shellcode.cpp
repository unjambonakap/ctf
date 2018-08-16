#include <cstdio>
#include <cstdlib>
#include <assert.h>
#include <unistd.h>


const int len=1111;
char buf[len];
typedef void (*fptr)();

int main(){
    FILE *f=fopen("./res_shellcode", "rb");
    fread(buf, 1, len, f);
    fclose(f);
    fptr x;
    x=(fptr)buf;
    x();
    assert(0);


    return 0;
}
