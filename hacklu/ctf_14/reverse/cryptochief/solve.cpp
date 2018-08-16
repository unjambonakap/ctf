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

#include "md5.h"

using namespace std;



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
typedef pair<int,int> pii;
typedef vector<int> vi;
typedef vector<string> vs;
typedef signed char s8;
typedef unsigned char u8;
typedef signed short s16;
typedef unsigned short u16;
typedef signed int s32;
typedef unsigned int u32;
typedef signed long long s64;
typedef unsigned long long u64;

template<class T> void checkmin(T &a, T b){if (b<a)a=b;}
template<class T> void checkmax(T &a, T b){if (b>a)a=b;}
template<class T> void out(T t[], int n){REP(i, n)cout<<t[i]<<" "; cout<<endl;}
template<class T> void out(vector<T> t, int n=-1){for (int i=0; i<(n==-1?t.size():n); ++i) cout<<t[i]<<" "; cout<<endl;}
inline int count_bit(int n){return (n==0)?0:1+count_bit(n&(n-1));}
inline int low_bit(int n){return (n^n-1)&n;}
inline int ctz(int n){return (n==0?-1:ctz(n>>1)+1);}
int toInt(string s){int a; istringstream(s)>>a; return a;}
string toStr(int a){ostringstream os; os<<a; return os.str();}

const int maxn=1e5;
char buf[maxn];
const int defaultSeed=0x1337cafe;

void disp(const string& a){
    REP(i, a.size()) printf("%02x ", (u8)a[i]);
    puts("");
}

string getMd5(const string& a){
    //MD5_CTX ctx;
    //MD5Init(&ctx);
    //MD5Update(&ctx, (const u8*)a.c_str(), a.size());
    //string res;
    //res.resize(16);
    //memcpy((char*)res.c_str(), ctx.digest, 16);
    //MD5Final(&ctx);
    //return res;
    return md5(a);
}

string unhexlify(const string &a){
    assert(a.size()%2==0);
    string res;
    res.resize(a.size()/2);
    for (int i=0; i<a.size(); i+=2){
        u32 tmp;
        sscanf(a.c_str()+i,"%02x", &tmp);
        res[i/2]=tmp;
    }
    return res;
}




u32 rol(u32 x, u32 v){
    return (x<<v)|(x>>(32-v));
}
u32 ror(u32 x, u32 v){
    return (x>>v)|(x<<(32-v));
}


void hash2(u32* h, int mks){
    int from=rand()%(mks/4);
    int to=rand()%(mks/4);
    u32& t1=h[from];
    u32& t2=h[to];

    t1=t1^t2;
    t2=t2^t1;
    t1^=t2;//5551

    u32 boobs=0xb000b135;
    u32 beef=0xdeadbeef;
    u32 ecc=0xecc83501;
    u32 cafe=0x1337cafe;
    u32 tmp=((~t1)|t2)+((~(t1|boobs))^rol(t2,0x10));
    u32 tmp2=((~t2^t1)^ecc)^((t2|boobs)&(t1|beef));
    t2=tmp-tmp2+t2;//5648

    tmp=((~(t1|beef))^rol(t2,0x8))^((~rol(t1,0x10))^rol(t2,0x8));
    tmp2=(ror(t1,0x8)|(t2^cafe))+(ror(t1,0x8)|t2);
    t1=tmp-tmp2+t1;

    tmp=((~t1^t2)^ecc)+(~t1|t2);
    tmp2=(~rol(t1,0x10))^rol(t2,0x8)^(ror(t2,0x8)|t1);
    t2=(tmp-tmp2)^t2;

    tmp=(~(t1|boobs)^rol(t2,0x10))+((t2|beef)&(t1|boobs));
    tmp2=((t1^cafe)|ror(t2,0x8))^(rol(t2,0x8)^~(t1|beef));
    t1=(tmp-tmp2)&t1;
}


string otp(const string& a, const string& b){
    string res;
    res.resize(a.size());
    REP(i,a.size())
        res[i]=a[i]^b[i];
    return res;
}
const int mks=8;

string hash(const string& a){
    u32 seed=((u8)a[0])<<8|((u8)a[a.size()-1])<<16|a.size();
    u8 hh[mks];
    srand(seed);

    REP(i,mks){
        hh[i]=0;
        REP(j,4){
            u32 x=rand();
            hh[i]|=x>>(24-j*8);
        }
    }
    REP(i0,a.size()){
        REP(iter,mks/4){
            //mks==8 >> x={0}

            u32 *tb=(u32*)hh;
            REP(x,mks/8){
                tb[x]=(~tb[x+1])|tb[x];
            }

            REP(n0, mks/4*0x17){
                hash2(tb, mks);
            }
        }
    }


    while(1){
        int fd=0;
        REP(i,mks)
            if (hh[i]==0)
                hh[i]=rand(), fd=1;
        if (!fd) break;
    }

    return string((const char*)hh, mks);
}


struct KG{
    KG(const string& input){
        a=::hash(input);
        id=1;
    }

    void calculate(){
        REP(i,mks){
            a[i]+=i%id;
            if (id&1)
                a[i]=~a[i];
        }
        a=::hash(a);
        ++id;
    }

    string getNBytes(int n){
        int no=n/mks+1;
        string res;
        REP(i,no){
            calculate();
            res+=a;
        }
        res.resize(n);
        return res;
    }

    string a;
    int id;
};


string readFile(const char* filename){
    FILE* f=fopen(filename, "rb");
    int len=fread(buf, 1, maxn, f);
    fclose(f);
    return string(buf, len);
}

string getOtp1Str(const string& pass, u32 n){
    KG kg(pass);
    string res=kg.getNBytes(n);
    return res;
}


string getOtp2Str(int n){
    string s=readFile("./otp2_str");
    while(s.size()<n)
        s+=s;
    s.resize(n);
    return s;
}


string getOtp3Str(int n, u32 seed){
    string res;
    res.resize(n);
    srand(seed);
    REP(i,n) res[i]=rand();
    return res;
}


string doit(const string& data, const string& pass, u32 seed, bool encrypt){
    vector<string> tb;
    int n=data.size();
    tb.pb(getOtp1Str(pass, n));
    tb.pb(getOtp2Str(n));
    tb.pb(getOtp3Str(n, seed));
    if (!encrypt) reverse(ALL(tb));

    string res=data;
    REP(i,tb.size())
        res=otp(res, tb[i]);
    return res;
}


void test1(){
    string in=readFile("./data/plain.txt");
    string key=readFile("./data/key.txt");
    string expected=readFile("./data/res1.txt");

    string ans=doit(in, key, defaultSeed, true);
    REP(i,ans.size()) printf("%d %d\n", ans[i], expected[i]);
    assert(ans==expected);
}

bool checkit(const string& pass, const string& cipher, const string& digest){
    string res=doit(cipher, pass, defaultSeed, false);
    string md5=getMd5(res);
    //disp(res);
    //printf("%02x %02x %02x %02x\n", (u8)md5[0], (u8)md5[1], (u8)md5[2], (u8)md5[3]);
    //printf("%02x %02x %02x %02x\n", (u8)digest[0], (u8)digest[1], (u8)digest[2], (u8)digest[3]);
    assert(md5.size()==32);
    assert(digest.size()==32);
    for (int i=0; i<32; ++i) if (md5[i]!=digest[i]) return 0;
    printf(">> %s<<\n", res.c_str());
    return 1;
}

void test2(){
    string res=readFile("./secret.krypto");
    string plainMd5="2aa0ce19d626a687517255f68e4e7640";
    disp(plainMd5);

    char charset[256];
    int nc=0;
    REP(i,256)
        charset[nc++]=i;

    FOR(n,2,101){
        string pass;
        pass.resize(n);
        printf("on %d\n", n);
        REP(i,nc) REP(j,nc){
            pass[0]=charset[i];
            pass[n-1]=charset[j];
            if (checkit(pass, res, plainMd5)){
                string ans=doit(res, pass, defaultSeed, false);
                disp(ans);
            }
        }

    }
}


int main(){
    if (0){
        test1();
    }else{
        test2();
    }

    return 0;
}

