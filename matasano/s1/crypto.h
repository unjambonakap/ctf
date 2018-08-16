#ifndef CRYPTO_H
#define CRYPTO_H 
#include <vector>
#include <list>
#include <map>
#include <set>
#include <deque>
#include <queue>
#include <stack>
#include <algorithm>
#include <numeric>
#include <utility>
#include <sstream>
#include <iostream>
#include <cstdlib>
#include <string>
#include <cstring>
#include <cstdio>
#include <cmath>
#include <cstdlib>
#include <ctime>
#include <cassert>
#include <climits>
//#include <ext/hash_map>
#include<ctime>
#include<unistd.h>
#include<endian.h>
#include<sys/time.h>

#include<openssl/aes.h>
#include<openssl/sha.h>
#include<openssl/md4.h>
#include<openssl/hmac.h>

#include<gmp.h>
#include"helper.h"

using namespace std;
using namespace __gnu_cxx;



#define REP(i,n) for(int i = 0; i < int(n); ++i)
#define REPV(i, n) for (int i = (n) - 1; (int)i >= 0; --i)
#define FOR(i, a, b) for(int i = (int)(a); i < (int)(b); ++i)

#define FE(i,t) for (__typeof((t).begin())i=(t).begin();i!=(t).end();++i)
#define FEV(i,t) for (__typeof((t).rbegin())i=(t).rbegin();i!=(t).rend();++i)

#define two(x) (1LL << (x))
#define ALL(a) (a).begin(), (a).end()


#define pb push_back
#define ST first
#define ND second
#define MP(x,y) make_pair(x, y)

typedef long long ll;
typedef unsigned long long ull;
typedef unsigned int uint;
typedef unsigned char uchar;
typedef pair<int,int> pii;
typedef vector<int> vi;
typedef vector<string> vs;
typedef vector<pair<string,string> > cookie;

extern gmp_randstate_t randstate;
void initcrypto();

typedef struct bignum{
    mpz_t a;
    ~bignum(){ mpz_clear(a); }
    bignum(const bignum &b){ mpz_init(a); mpz_set(a,b.a); }
    bignum(){mpz_init(a);}
    bignum(const buffer &b, int base=16){ mpz_init(a); mpz_set_str(a,(char*)b.a,base); }
    bignum(int u){ mpz_init(a); mpz_set_si(a,u); }
    buffer getstr(int base=16)const{
        char *x=mpz_get_str(0,base,a);
        buffer b(x);
        free(x);
        return b;
    }

    buffer getstr2()const{ return getstr().hextobyte(); }

    void disp()const{getstr().disptext();}

    static bignum frombytestr(const buffer &b){ return bignum(b.bytetohex()); }

    static bignum rand(const bignum &b){
        bignum res;
        mpz_urandomm(res.a,randstate,b.a);
        return res;
    }



    bignum &operator=(const bignum &b){ mpz_set(a,b.a); return *this; }
    bignum operator+(const bignum &b)const{
        bignum res;
        mpz_add(res.a,a,b.a);
        return res;
    }
    bignum operator-(const bignum &b)const{
        bignum res;
        mpz_sub(res.a,a,b.a);
        return res;
    }
    bignum operator*(const bignum &b)const{
        bignum res;
        mpz_mul(res.a,a,b.a);
        return res;
    }
    bignum operator/(const bignum &b)const{
        bignum res;
        mpz_fdiv_q(res.a,a,b.a);
        return res;
    }
    bignum ceil(const bignum &b)const{
        bignum res;
        mpz_fdiv_q(res.a,a,b.a);
        return res;
    }
    bignum operator%(const bignum &b)const{
        bignum res;
        mpz_mod(res.a,a,b.a);
        return res;
    }
    bignum powm(const bignum &b, const bignum &mod)const{
        bignum res;
        mpz_powm(res.a,a,b.a,mod.a);
        return res;
    }


    bool operator<(const bignum &b)const{return mpz_cmp(a,b.a)<0;}
    bool operator>(const bignum &b)const{return mpz_cmp(a,b.a)>0;}
    bool operator<=(const bignum &b)const{return mpz_cmp(a,b.a)<=0;}
    bool operator>=(const bignum &b)const{return mpz_cmp(a,b.a)>=0;}
    bool operator==(const bignum &b)const{ return mpz_cmp(a,b.a)==0; }
    bool operator!=(const bignum &b)const{return mpz_cmp(a,b.a)!=0;}

    bignum inv(const bignum &n)const{
        bignum u,v,d;
        bignum::egcd(n,*this,u,v,d);
        if (d!=1) return -1;
        return v;
    }

    static void egcd(const bignum &a, const bignum &b, bignum &u, bignum &v, bignum &d){
        if (a<b) egcd(b,a,v,u,d);
        _egcd(a,b,1,0,0,1,u,v,d);
    }


    static void _egcd(const bignum &a, const bignum &b, const bignum &ua, const bignum &va, const bignum &ub, const bignum &vb, bignum &u, bignum &v, bignum &d){
        if (b==0){u=ua; v=va; d=a; return;}
        bignum tmp=a/b;
        _egcd(b,a%b,ub,vb,ua-tmp*ub,va-tmp*vb,u,v,d);
    }
}bg;


buffer bad_getpkcs1hash(const buffer &a);


struct rsa{
    bignum n,p,q;
    bignum e,d;
    int sz;



    void gen(int ndigit=30){
        sz=ndigit*8;
        ndigit/=2;
        while(1){
            buffer x=buffer::Rand(ndigit);
            buffer y=buffer::Rand(ndigit);
            mpz_nextprime(p.a,bignum(x.bytetohex()).a);
            mpz_nextprime(q.a,bignum(y.bytetohex()).a);
            n=p*q;
            if (mpz_sizeinbase(n.a,2)!=sz) continue;

            bignum et=(p-1)*(q-1);
            e=3;
            d=e.inv(et);
            if (d!=-1) break;
        }
    }

    bignum encrypt(const bignum &m)const{
        assert(m<n);
        return m.powm(e,n); 
    }
    bignum decrypt(const bignum &m)const{
        assert(m<n);
        return m.powm(d,n); 
    }
    bignum encryptstr(const buffer &a)const{ 
        //size a > ~1/8 log 2 n will fail
        bignum b=bignum(buffer("ff")+a.bytetohex());
        return encrypt(b); 
    }
    buffer decryptstr(const bignum &a)const{
        buffer tmp=decrypt(a).getstr().bytetohex();
        return buffer(tmp.a+1,tmp.n-1);//chomp first ff
    }

    buffer decryptpad(const bignum &m)const{
        return repad(decrypt(m));
    }

    bignum encryptpad(const buffer &a)const{
        return encrypt(pad(a));
    }

    buffer repad(const bignum &x)const{
        int u=mpz_sizeinbase(x.a,16);
        buffer y=x.getstr2();

        buffer res(sz/8);
        memcpy(res.a+res.n-y.n,y.a,y.n);
        return res;
    }

    bignum pad(const buffer &a)const{
        assert(a.n+11<=sz/8);
        buffer enc(sz/8);
        enc[1]=2;
        int u=2;
        REP(i,sz/8-3-a.n) enc[u++]=0xff;
        enc[u++]=0;
        memcpy(enc.a+u,a.a,a.n);
        return bignum::frombytestr(enc);
    }


    buffer unpad(const buffer &a)const{
        int i=2;
        for (; i<a.n && a[i]==0xff; ++i);
        return buffer(a.a+i+1);
    }

    int oracle(const bignum &a){ return mpz_odd_p(decrypt(a).a); }

    int oracle2(const bignum &a){
        buffer x=decryptpad(a);
        return x[0]==0 && x[1]==2;
    }


    buffer decryptsig(const bignum &a){
        buffer b=encrypt(a).getstr().hextobyte();
        buffer c=buffer(b.a+1,b.n-1);
        return bad_getpkcs1hash(c);
    }
};

bignum crt(const vector<pair<bignum,bignum> > tb);


struct dsa{
    bignum p,q,g;
    bignum x,y;
    int safe;

    dsa(){
        safe=1;
        p=buffer("800000000000000089e1855218a0e7dac38136ffafa72eda7859f2171e25e65eac698c1702578b07dc2a1076da241c76c62d374d8389ea5aeffd3226a0530cc565f3bf6b50929139ebeac04f48c3c84afb796d61e5a4f9a8fda812ab59494232c7d2b4deb50aa18ee9e132bfa85ac4374d7f9091abc3d015efc871a584471bb1");
        q =buffer( "f4f47f05794b256174bba6e9b396a7707e563c5b");
        g = buffer("5958c9d3898b224b12672c0b98e06c60df923cb8bc999d119458fef538b8fa4046c8db53039db620c094c9fa077ef389b5322a559946a71903f990f1f7e0e025e2d7f7cf494aff1a0470f5b64c36b625a097f1651fe775323556fe00b3608c887892878480e99041be601a62166ca6894bdd41a7054ec89f756ba9fc95302291");
        x=bignum::rand(q-1)+1;
        y=g.powm(x,p);
    }

    void setg(const bignum &ng){
        g=ng;
        y=g.powm(x,p);
        safe=0;
    }

    pair<bignum,bignum> sign(const buffer &m){
        while(1){
            bignum k=bignum::rand(q-1)+1;
            bignum r,s;
            r=g.powm(k,p)%q;
            if (safe && r==0) continue;
            s=k.inv(q)*(bignum::frombytestr(sha1(m))+x*r)%q;
            if (safe && s==0) continue;
            return MP(r,s);
        }
    }

    pair<bignum,bignum> sign2(const buffer &m, bignum &k){
        while(1){
            k=bignum::rand(q-1)+1;
            bignum r,s;
            r=g.powm(k,p)%q;
            if (safe && r==0) continue;
            s=k.inv(q)*(bignum::frombytestr(sha1(m))+x*r)%q;
            if (safe && s==0) continue;
            return MP(r,s);
        }
    }
    pair<bignum,bignum> sign3(const buffer &m, const bignum &k){
        bignum r,s;
        r=g.powm(k,p)%q;
        s=k.inv(q)*(bignum::frombytestr(sha1(m))+x*r)%q;
        return MP(r,s);
    }

    bool check(const buffer &m, const pair<bignum,bignum> &u){
        const bignum &r=u.ST, &s=u.ND;
        if (safe){
            if (r<0 || r>=q) return false;
            if (s<0 || s>=q) return false;
        }
        bignum w=s.inv(q);
        bignum u1,u2;
        u1=bignum::frombytestr(sha1(m))*w%q;
        u2=r*w%q;
        bignum v=g.powm(u1,p)*y.powm(u2,p)%p%q;
        return v==r;
    }


    bignum getx(const buffer &m, const bignum &k, const bignum &r, const bignum &s){
        return (s*k-bignum::frombytestr(sha1(m)))*r.inv(q)%q;
    }
};



#endif


