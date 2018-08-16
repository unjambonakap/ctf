#include"crypto.h"


gmp_randstate_t randstate;

void initcrypto(){
    gmp_randinit_default(randstate);
}
bignum crt(const vector<pair<bignum,bignum> > tb){
    bignum n=1;
    bignum res=0;
    FE(it,tb) n=n*it->ND;
    FE(it,tb){
        bignum x=n/it->ND;
        res=res+x*it->ST*(x%it->ND).inv(it->ND);
                }
    return res%n;
}


buffer bad_getpkcs1hash(const buffer &a){
    int l;
    int i=2;
    if (a[0]!=0) goto fail;
    if (a[1]!=1) goto fail;
    for (;i<a.n && a[i]==0xff; ++i);
    if (i+5>=a.n || a[i]!=0) goto fail;
    ++i;

    memcpy(&l,a.a+i,4);
    //instead of using asn1, just have the length of hash on 4 bytes (little endian)
    assert(i+4+l<=a.n);//would be equal for correct impl
    return buffer(a.a+i+4,l);

fail:
    throw "bad pkcs1";
}


