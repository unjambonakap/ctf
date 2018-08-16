#ifndef HELPER_H
#define HELPER_H 
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


struct buffer{
    uchar *a; int n;

    ~buffer(){free(a);}
    buffer(int n=0):n(n){a=(uchar*)malloc(n+1);memset(a,0,n+1);}
    buffer(const uchar *b, int n):n(n){a=(uchar*)malloc(n+1); memcpy(a,b,n); a[n]=0;}
    buffer(const uchar *b){n=strlen((char*)b); a=(uchar*)malloc(n+1); memcpy(a,b,n); a[n]=0;}
    buffer(const char *b){n=strlen(b); a=(uchar*)malloc(n+1); memcpy(a,b,n); a[n]=0;}
    buffer(const buffer &b){n=b.n; a=(uchar*)malloc(n+1); memcpy(a,b.a,n); a[n]=0;}
    buffer operator=(const buffer &b){n=b.n; a=(uchar*)malloc(n+1); memcpy(a,b.a,n); a[n]=0; return *this;}
    bool operator==(const buffer &b)const{
        if (b.n!=n) return 0;
        return !memcmp(b.a,a,n);
    }

    uchar &operator[](int i){return a[i];}
    uchar operator[](int i)const{return a[i];}

    buffer operator+(const buffer &b)const{
        buffer x(n+b.n);
        memcpy(x.a,a,n);
        memcpy(x.a+n,b.a,b.n);
        return x;
    }

    void from(const buffer &b){free(a); n=b.n; a=(uchar*)malloc(n+1); memcpy(a,b.a,n);}
    buffer copy()const{ buffer x; x.from(*this); return x;}


    static buffer Rand(int n){
        buffer x(n);
        REP(i,n) x.a[i]=rand()&0xff;
        return x;
    }

    buffer tob64() const;

    buffer fromb64() const;
    void disphex(int m=-1)const{if (m==-1) m=n; ;REP(i,m) printf("%02x",(unsigned uchar)a[i]); puts("");}
    void disptext(int m=-1)const{if (m==-1) m=n; REP(i,m) printf("%c", isprint(a[i])||isspace(a[i])?a[i]:'?');puts("");}

    void fillrand(int u, int v){
        assert(u>=0 && v<n);
        FOR(i,u,v) a[i]=rand()&0xff;
    }

    buffer hextobyte()const{
        assert(!(n&1));
        buffer b(n/2);
        REP(i,n/2) sscanf((char*)a+2*i,"%2x",b.a+i);
        return b;
    }
    buffer bytetohex()const{
        buffer b(2*n);
        REP(i,n) sprintf((char*)b.a+2*i,"%02x",a[i]);
        return b;
    }
    void rpkcs7(int bs=16){
        int x=a[n-1];
        if (!x || x>bs) throw "PADDING ERROR";
        for (int i=n-1; i>=n-x; --i) if (a[i]!=x) throw "PADDING ERROR";
        n-=x;
    }

    buffer pkcs7(int bs=16) const{
        assert(bs<256);
        int u=bs-n%bs;
        buffer b(n+u);
        memcpy(b.a,a,n);
        REP(i,u) b.a[n+i]=u;
        return b;
    }

    double computescore()const;
};

const int maxc=222;
const int maxn=222;
struct xorstream{
    vector<buffer> tb;
    int n,mx;
    int perm[maxn];
    int iperm[maxn];
    int state[maxc];
    vector<pair<double,int> > lst[maxc];

    buffer go();
    void dispstate();
    void dispresult();
};

struct cmpbuffervector{
    const vector<buffer> &tb;
    cmpbuffervector(const vector<buffer> &tb):tb(tb){}
    bool operator()(int a, int b){return tb[a].n>tb[b].n;}
};


struct PRNG{
    uint mt[624];
    int index;

    PRNG(){index=0;}
    void seed(uint s){
        index=0;
        mt[0]=s;
        FOR(i,1,624) mt[i]=0x6c078965*(mt[i-1]^(mt[i-1]>>30))+i;
    }


    uint gen(){
        if (!index) gen_numbers();
        uint y=mt[index];
        int oy=y;
        y^=y>>11;
        y^=y<<7&0x9d2c5680;
        y^=y<<15&0xefc60000;
        y^=y>>18;
        index=(index+1)%624;
        assert(reverse(y)==oy);
        return y;
    }

    void gen_numbers(){
        REP(i,624){
            uint y=(mt[i]&0x80000000)
                +(mt[(i+1)%624]&0x7fffffff);
            mt[i]=mt[(i+397)%624]^y>>1;
            if (y&1) mt[i]^=0x9908b0df;
        }
    }

    uint revl(uint x, uint c, uint M){
        ll m2=(1u<<c)-1;
        uint y=x&~M;
        for (; m2&(uint)-1; m2<<=c) y|=(x^y<<c)&m2&M;
        return y;
    }
    uint revr(uint x, uint c, uint M){
        uint m2=(1u<<c)-1<<(32-c);
        uint y=x&~M;
        for (; m2; m2>>=c) y|=(x^y>>c)&m2&M;
        return y;
    }

    uint reverse(uint y){
        y=revr(y,18,-1);
        y=revl(y,15,0xefc60000);
        y=revl(y,7,0x9d2c5680);
        y=revr(y,11,-1);
        return y;
    }

    buffer encrypt(const buffer &a){
        buffer b(a);
        REP(i,b.n) b[i]^=gen()&0xff;
        return b;
    }
};
buffer break_xorstream(const vector<buffer> &tb);





void inithelper();
void genivkey(buffer &iv, AES_KEY *key, AES_KEY *rkey);

buffer readfile(uchar *fname);
vector<buffer> readfilebyline(uchar *fname);
buffer aes_ecb_encrypt(const buffer &in, AES_KEY *key, int bs=16);
buffer aes_cbc_encrypt(const buffer &in, const buffer &iv, AES_KEY *key, int bs=16);
buffer aes_ecb_decrypt(const buffer &in, AES_KEY *key, int bs=16);
buffer aes_cbc_decrypt(const buffer &in, const buffer &iv, AES_KEY *key, int bs=16);
buffer ctr_go(const buffer &in, const buffer &keys, ll nonce);

buffer sha1(const buffer &a);
buffer sha1_prefix(const buffer &key, const buffer &a);
buffer sha1_preproc(const buffer &a, int cursz, int sz);
buffer sha1_raw(const buffer &a, SHA_CTX *ctx);
buffer sha1_raw(const buffer &a, const buffer &prev=buffer());
void sha1_hashtoctx(const buffer &hash, SHA_CTX *ctx);
buffer sha1_ctxtohash(SHA_CTX *ctx);

buffer md4(const buffer &a);
buffer md4_prefix(const buffer &key, const buffer &a);
void md4_hashtoctx(const buffer &hash, MD4_CTX *ctx);
buffer md4_ctxtohash(MD4_CTX *ctx);
buffer md4_raw(const buffer &a, MD4_CTX *ctx);
buffer md4_raw(const buffer &a, const buffer &prev=buffer());
buffer md4_preproc(const buffer &a, int cursz, int sz);



buffer hmac(const buffer &a, const buffer &key);
char gethexchar(int x);

#endif

