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


using namespace std;
using namespace __gnu_cxx;



#define REP(i,n) for(int i = 0; i < int(n); ++i)

#define REPV(i, n) for (int i = (n) - 1; (int)i >= 0; --i)
#define FOR(i, a, b) for(int i = (int)(a); i <= (int)(b); ++i)
#define FORV(i, a, b) for(int i = (int)(a); i >= (int)(b); --i)

#define FE(i,t) for (typeof((t).begin())i=(t).begin();i!=(t).end();++i)
#define FEV(i,t) for (typeof((t).rbegin())i=(t).rbegin();i!=(t).rend();++i)

#define SZ(a) (int((a).size()))
#define two(x) (1 << (x))
#define twoll(x) (1LL << (x))
#define ALL(a) (a).begin(), (a).end()
#define CLR(a) (a).clear()


#define pb push_back
#define PF push_front
#define ST first
#define ND second
#define MP(x,y) make_pair(x, y)

typedef long long ll;
typedef unsigned long long ull;
typedef pair<int,int> pii;
typedef vector<int> vi;
typedef vector<string> vs;
typedef queue<int> qi;

template<class T> void checkmin(T &a, T b){if (b<a)a=b;}
template<class T> void checkmax(T &a, T b){if (b>a)a=b;}
template<class T> void out(T t[], int n){REP(i, n)cout<<t[i]<<" "; cout<<endl;}
template<class T> void out(vector<T> t, int n=-1){for (int i=0; i<(n==-1?t.size():n); ++i) cout<<t[i]<<" "; cout<<endl;}
inline int count_bit(int n){return (n == 0)?0:1+count_bit(n&(n-1));}
inline bool bit_set(int a, int b){return (a&two(b));}
inline int low_bit(int n){return (n^n-1)&n;}
inline int ctz(int n){return (n==0?-1:(n==1?0:ctz(n>>1)+1));}
int toInt(string s){int a; istringstream(s)>>a; return a;}
string toStr(int a){ostringstream os; os<<a; return os.str();}

const int sbox[]={ 
    0x63, 0x7c, 0x77, 0x7b, 0xf2, 0x6b, 0x6f, 0xc5, 0x30, 0x01, 0x67, 0x2b, 0xfe, 0xd7, 0xab, 0x76, 
    0xca, 0x82, 0xc9, 0x7d, 0xfa, 0x59, 0x47, 0xf0, 0xad, 0xd4, 0xa2, 0xaf, 0x9c, 0xa4, 0x72, 0xc0, 
    0xb7, 0xfd, 0x93, 0x26, 0x36, 0x3f, 0xf7, 0xcc, 0x34, 0xa5, 0xe5, 0xf1, 0x71, 0xd8, 0x31, 0x15, 
    0x04, 0xc7, 0x23, 0xc3, 0x18, 0x96, 0x05, 0x9a, 0x07, 0x12, 0x80, 0xe2, 0xeb, 0x27, 0xb2, 0x75, 
    0x09, 0x83, 0x2c, 0x1a, 0x1b, 0x6e, 0x5a, 0xa0, 0x52, 0x3b, 0xd6, 0xb3, 0x29, 0xe3, 0x2f, 0x84, 
    0x53, 0xd1, 0x00, 0xed, 0x20, 0xfc, 0xb1, 0x5b, 0x6a, 0xcb, 0xbe, 0x39, 0x4a, 0x4c, 0x58, 0xcf, 
    0xd0, 0xef, 0xaa, 0xfb, 0x43, 0x4d, 0x33, 0x85, 0x45, 0xf9, 0x02, 0x7f, 0x50, 0x3c, 0x9f, 0xa8, 
    0x51, 0xa3, 0x40, 0x8f, 0x92, 0x9d, 0x38, 0xf5, 0xbc, 0xb6, 0xda, 0x21, 0x10, 0xff, 0xf3, 0xd2, 
    0xcd, 0x0c, 0x13, 0xec, 0x5f, 0x97, 0x44, 0x17, 0xc4, 0xa7, 0x7e, 0x3d, 0x64, 0x5d, 0x19, 0x73, 
    0x60, 0x81, 0x4f, 0xdc, 0x22, 0x2a, 0x90, 0x88, 0x46, 0xee, 0xb8, 0x14, 0xde, 0x5e, 0x0b, 0xdb, 
    0xe0, 0x32, 0x3a, 0x0a, 0x49, 0x06, 0x24, 0x5c, 0xc2, 0xd3, 0xac, 0x62, 0x91, 0x95, 0xe4, 0x79, 
    0xe7, 0xc8, 0x37, 0x6d, 0x8d, 0xd5, 0x4e, 0xa9, 0x6c, 0x56, 0xf4, 0xea, 0x65, 0x7a, 0xae, 0x08, 
    0xba, 0x78, 0x25, 0x2e, 0x1c, 0xa6, 0xb4, 0xc6, 0xe8, 0xdd, 0x74, 0x1f, 0x4b, 0xbd, 0x8b, 0x8a, 
    0x70, 0x3e, 0xb5, 0x66, 0x48, 0x03, 0xf6, 0x0e, 0x61, 0x35, 0x57, 0xb9, 0x86, 0xc1, 0x1d, 0x9e, 
    0xe1, 0xf8, 0x98, 0x11, 0x69, 0xd9, 0x8e, 0x94, 0x9b, 0x1e, 0x87, 0xe9, 0xce, 0x55, 0x28, 0xdf, 
    0x8c, 0xa1, 0x89, 0x0d, 0xbf, 0xe6, 0x42, 0x68, 0x41, 0x99, 0x2d, 0x0f, 0xb0, 0x54, 0xbb, 0x16}; 


void add(double *a, int  *b, int m){
    REP(i, m) a[i]+=b[i];
}

int main(){
    int n, m;
    int aes_size=16;//aes 128 bits
    cin>>n;
    cin>>m;
    printf("start reading trace (%d x %d)\n", n, m);
    int plain[n][aes_size];
    int trace[n][m];
    REP(i, n) REP(j, m) cin>>trace[i][j];
    REP(i, n) REP(j, aes_size) cin>>hex>>plain[i][j];
    printf("end reading input file\n");

    int key[aes_size];


    //simpler version
//    REP(i, aes_size){//aes 128 bits key
//        printf("on key %d \n", i);
//        double bestval=-1.;
//        REP(j, 256){//all possible values for the i-th key
//            double suma[m], sumb[m];
//            memset(suma, 0, sizeof(suma));
//            memset(sumb, 0, sizeof(sumb));
//            int cnta, cntb;
//            cnta=cntb=0;
//            REP(k, n){
//                int res=sbox[j^plain[k][i]];
//                if (count_bit(res)>=4) add(suma, trace[k], m), ++cnta;
//                //if (res&1) add(suma, trace[k], m), ++cnta;
//                else add(sumb, trace[k], m), ++cntb;
//            }
//
//            //easy to implement simd instructions
//            if (cnta) REP(k, m) suma[k]/=cnta;
//            if (cntb) REP(k, m) sumb[k]/=cntb;
//            REP(k, m) suma[k]=fabs(suma[k]-sumb[k]);
//
//
//            double tmp=*max_element(suma, suma+m);
//            if (tmp>bestval) bestval=tmp, key[i]=j;
//        }
//        printf("%c => %x\n", key[i], key[i]);
//    }


    //newmann pearson correlation test

    double vara[m];
    double meana[m];
    memset(vara, 0, sizeof(vara));
    memset(meana, 0, sizeof(meana));
    REP(i, m){
        REP(j, n) meana[i]+=trace[j][i];
        meana[i]/=n;
    }
    REP(i, m){
        REP(j, n) vara[i]+=(trace[j][i]-meana[i])*(trace[j][i]-meana[i]);
        vara[i]=sqrt(vara[i]/n);
    }


    REP(i, aes_size){//aes 128 bits key
        printf("on key %d \n", i);
        double bestval=-1.;
        REP(j, 256){//all possible values for the i-th key
            double tb[n];
            double vartb, meantb;

            vartb=meantb=0.;
            REP(k, n){
                int res=sbox[j^plain[k][i]];
                tb[k]=(count_bit(res)>=4);
                meantb+=tb[k];
            }
            meantb/=n;
            REP(k, n) vartb+=(tb[k]-meantb)*(tb[k]-meantb);
            vartb=sqrt(vartb/n);

            double res[m];
            memset(res, 0, sizeof(res));

            REP(k, m){//look for correlation between tb and trace[*][k], pick 
                REP(l, n) res[k]+=(tb[l]-meantb)*(trace[l][k]-meana[k]);
                res[k]=abs(res[k])/(vara[k]*vartb);
            }


            double tmp=*max_element(res, res+m);
            if (tmp>bestval) bestval=tmp, key[i]=j;
        }
        printf("%c => %x\n", key[i], key[i]);
    }
}



