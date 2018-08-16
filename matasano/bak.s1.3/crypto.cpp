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


