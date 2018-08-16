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
#include <random>


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
typedef pair<int,int> pii;
typedef vector<int> vi;
typedef vector<string> vs;

template<class T> void checkmin(T &a, T b){if (b<a)a=b;}
template<class T> void checkmax(T &a, T b){if (b>a)a=b;}
template<class T> void out(T t[], int n){REP(i, n)cout<<t[i]<<" "; cout<<endl;}
template<class T> void out(vector<T> t, int n=-1){for (int i=0; i<(n==-1?t.size():n); ++i) cout<<t[i]<<" "; cout<<endl;}
inline int count_bit(int n){return (n==0)?0:1+count_bit(n&(n-1));}
inline int low_bit(int n){return (n^n-1)&n;}
inline int ctz(int n){return (n==0?-1:ctz(n>>1)+1);}
int toInt(string s){int a; istringstream(s)>>a; return a;}
string toStr(int a){ostringstream os; os<<a; return os.str();}

typedef  unsigned int u32;
typedef  int         s32;
typedef signed char  s8 ;
typedef unsigned char u8 ;
typedef  signed short s16;
typedef  unsigned short u16;
typedef  unsigned long long  u64;
typedef  signed long long s64;

static unsigned long x=123456789, y=362436069, z=521288629;
std::mt19937_64 prng;

unsigned long xorshf96(void) {          //period 2^96-1
    unsigned long t;
    x ^= x << 16;
    x ^= x >> 5;
    x ^= x << 1;

    t = x;
    x = y;
    y = z;
    z = t ^ x ^ y;

    return z;
}



inline u8 rot3(u8 x){return (x<<3)|(x>>5);}
inline u8 gBox(u8 a, u8 b, u8 mode){return rot3(a+b+mode);}
inline u32 fBox(u32 _plain){
    u8 *plain=(u8*)&_plain;
    u8 t0,y1,y0,y2,y3;

    t0=plain[2]^plain[3];
    y1=gBox(plain[0]^plain[1], t0, 1);
    y0 = gBox(plain[0], y1, 0);
    y2 = gBox(t0, y1, 0);
    y3 = gBox(plain[3], y2, 1);

    return (((y0<<8)|y1)<<8|y2)<<8|y3;
}

u64 encrypt(u64 plain, u32 *subkeys){
    u32 pleft=plain&0xffffffff;
    u32 pright=plain>>32;

    u32 left,right, R2L, R2R, R3L, R3R, R4L, R4R;
    left=pleft^subkeys[4];
    right=pright^subkeys[5];

    R2L=left^right;
    R2R=left^fBox(R2L^subkeys[0]);

    R3L=R2R;
    R3R = R2L^fBox(R2R^subkeys[1]);

    R4L = R3R;
    R4R = R3L^fBox(R3R^subkeys[2]);

    u32 cipherLeft = R4L^fBox(R4R^subkeys[3]);
    u32 cipherRight = cipherLeft^R4R;

    return ((u64)cipherRight<<32)|cipherLeft;

}


void genKeys(u32 *subkeys){
    u64 *tb=(u64*)subkeys;
    REP(i,3) tb[i]=prng();
}

void test(){

    if (0){
        u32 subkeys[64];
        u64 plain;
        memset(subkeys,'a',4);
        memset(subkeys+1,'b',4);
        memset(subkeys+2,'x',4);
        memset(subkeys+3,'d',4);
        memset(subkeys+4,'e',4);
        memset(subkeys+5,'f',4);
        memset(&plain, 'z', 8);

        u64 res=encrypt(plain, subkeys);
        printf(">>> %Lx\n",res);
    }else{
        u32 subkeys[6];
        genKeys(subkeys);

        int nb=6;
        int cnt[1<<nb][1<<nb];
        memset(cnt,0,sizeof(cnt));
        int nrep=400000;

        REP(rr,nrep){
            if (rr%1000==0) printf(">> %d\n",rr);
            u32 tmp=prng();
            u32 res=fBox(tmp);

            REP(i,1<<nb){
                REP(j,1<<nb){
                    int vi=0, vj=0;
                    REP(k, nb){
                        if (i>>k&1) vi^=tmp>>k&1;
                        if (j>>k&1) vj^=res>>k&1;
                    }
                    cnt[i][j]+=vi==vj;
                }
            }
        }


        vector<double> vals;
        REP(i,1<<nb) REP(j,1<<nb) if (i||j){
            double v=1.*(cnt[i][j]-nrep/2)/(nrep/2);
            vals.pb(abs(v));
        }
        sort(ALL(vals));
        reverse(ALL(vals));
        REP(i,10) printf("%lf\n", vals[i]);
        puts("");


    }

    exit(0);
}


void test0(){

    int nb=4;
    int tb[1<<nb][1<<nb][1<<nb];
    memset(tb,0,sizeof(tb));
    printf("LA\n");
    REP(i,256) REP(j,256){
        int res=(i+j)%256;
        REP(x,1<<nb) REP(y,1<<nb) REP(z,1<<nb){
            int v=0;
            REP(k,nb){
                if (x>>k&1) v^=i>>k&1;
                if (y>>k&1) v^=j>>k&1;
                if (z>>k&1) v^=res>>k&1;
            }
            if (v==0) ++tb[x][y][z];
        }
    }

    int tot=256*256/2;
    REP(i,1<<nb){
        REP(j,1<<nb) REP(k,1<<nb){
            int v=tb[i][j][k]-tot;
            if (fabs(v)>=tot/2)
                printf("%d %d %d> > %d\n",i,j,k,v);

        }
    }
    exit(0);


}

int main(){

    int nstep=1000;
    int nstep2=1000;
    u32 subkeys[6];
    prng.seed(0);

    test0();
    test();


    u64 *sk64=(u64*)subkeys;
    int stat[4][64][64];
    memset(stat, 0, sizeof(stat));

    REP(i,nstep){
        genKeys(subkeys);
        REP(j,nstep2){
            u64 in=prng();
            u64 res=encrypt(in,subkeys);
            u64 res2=encrypt(in^1, subkeys);
            printf("%Lx\n", res^res2);
            REP(b1,3) REP(b2,64) REP(a,64){
                int c1=in>>a&1;
                int c2=subkeys[b1]>>b2&1;
                if (c1==c2) ++stat[b1][b2][a];
            }
        }
        break;
    }
    return 0;

    int mid=nstep*nstep2/2;
    vector<pair<double,int> > tb;
    REP(b1,3) REP(b2,64) REP(a,64){
        int cnt=stat[b1][b2][a]-mid;
        double val=1.*cnt/mid;
        tb.pb(MP(fabs(val), b1*64*64+b2*64+a));
    }

    sort(ALL(tb));
    reverse(ALL(tb));
    REP(i,64)
        printf(">>> %d >> %lf\n", tb[i].ND, tb[i].ST);
    REP(i,tb.size()) if (tb[i].ST>0.10)
        printf(">>> %d >> %lf\n", tb[i].ND, tb[i].ST);


    return 0;
}

