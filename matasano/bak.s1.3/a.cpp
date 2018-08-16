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

const int maxs=111111;
const double oo=1e9;
const char *m64="ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/";

double freq[]={12.02,9.10,8.12,7.68,7.31,6.95,6.28,6.02,5.92,4.32,3.98,2.88,2.71,2.61,2.30,2.11,2.09,2.03,1.82,1.49,1.11,0.69,0.17,0.11,0.10,0.07,0};
int sfreq[27];
int rm64[128];
char buf[maxs];
int pos;


int cmp1(int a, int b){return freq[a]>freq[b];}
double sq(double a){return a*a;}

void disphex(char *a, int n){REP(i,n) printf("%02x",a[i]); puts("");}
char *getb(int n){ assert(pos+n<maxs);int u=pos; pos+=n+1; return buf+u; }

int b64e(char *a, int n, char *&b){
    int sz=(n+2)*4/3+2;
    b=getb(sz+n+10);

    memcpy(b+sz,a,n);
    a=b+sz;
    REP(i,3) a[n+i]=0;

    int pad=(3-n%3)%3, m=0;
    for (int i=0; i<n+pad; i+=3){
        int x=a[i]<<16|a[i+1]<<8|a[i+2];
        REP(j,4) b[m+3-j]=m64[x&0x3f], x>>=6;
        m+=4;
    }
    REP(i,pad) b[m++]='=';
    b[m]=0;
    return m;
}

int b64d(char *a, int n, char *&b){
    int pad=0;
    for (;a[n-pad-1]=='='; ++pad);
    int sz=(n+3)*3/4-pad;
    b=getb(sz);

    memset(b,0,sz);

    int m=0;
    assert(n%4==0);
    for (int i=0; i<n;){
        int x=0;
        REP(j,4) x=x<<6|rm64[a[i++]];
        REP(j,3) b[m+2-j]=x&0xff, x>>=8;
        m+=3;
    }
    m-=pad;
    return m;
}

int hextobyte(char *a, char *&b){
    int n=strlen(a);
    assert(!(n&1));
    b=getb(n/2);
    REP(i,n/2) sscanf(a+2*i,"%2x",b+i);
    return n/2;
}
int bytetohex(char *a, int n, char *&b){
    b=getb(2*n);
    REP(i,n) sprintf(b+2*i,"%02x",a[i]);
    return n*2;
}

double computescore(char *x, int n){
    map<int,int> mp;
    int nx=n;
    REP(i,n) if (isalpha(x[i])) ++mp[x[i]|32], --nx;

    int nsp=0;
    REP(i,n) if (isprint(x[i]) && isspace(x[i])) ++nsp, --nx;

    double sc=0;
    sc+=sq(100.*nsp/n-freq[sfreq[0]]);
    FE(it,mp) sc+=sq(freq[it->ST-'a']-100.*it->ND/n);
    sc+=sq(100.*nx/n);

    return sc;
}

double computedistribscore(char *x, int n){
    map<char,int> mp;
    REP(i,n) ++mp[x[i]];
    vector<double> tb;
    FE(it,mp) tb.pb(100.*it->ND/n);
    double sc=0;
    sc+=sq(freq[sfreq[0]]-tb[0]);
    while(tb.size()<27) tb.pb(0);
    sort(ALL(tb));
    reverse(ALL(tb));
    FOR(i,1,tb.size()) sc+=sq(freq[sfreq[min(i,26)]]-tb[i]);
    return sc;


}

double solvexor(char *x, int n, double best2=oo){
    char *y,*z;
    y=getb(n);
    vector<pair<double,int> > tb;
    REP(i,256){
        REP(j,n) y[j]=x[j]^i;
        tb.pb(MP(computescore(y,n),i));
    }

    int top=1;
    sort(ALL(tb));

    REP(i,top){
        if (tb[i].ST>=best2) continue;
        best2=tb[i].ST;
        puts("");
        puts("====");
        int k=tb[i].ND;
        printf("key %x, score %lf\n",k,tb[i].ST);
        printf("<START>");
        REP(j,n) if (isprint(x[j]^k)) printf("%c",x[j]^k); puts("<END>");
        printf("<START>");
        REP(j,n) if (isprint(x[j]^k)) printf("%d",isspace(x[j]^k)); puts("<END>");
    }
    return best2;
}

vector<char> singlexorcnd(char *x, int n, int ncnd){
    vector<pair<double,char> > tb;
    char *y=getb(n);
    REP(i,256){
        REP(j,n) y[j]=x[j]^i;
        tb.pb(MP(computescore(y,n),i));
    }
    sort(ALL(tb));

    vector<char> res;
    REP(i,ncnd) res.pb(tb[i].ND);
    return res;
}

void blockxorenc(char *a, int n, char *k, int m, char *b){ REP(i,n) b[i]=a[i]^k[i%m]; }

int solveblockxor(char *x, int n, char *&key, int quiet=1, int ncnd=1){
    int trynk=30;
    char *y=getb(n);

    vector<pair<double,int> > tb;
    FOR(ks,1,trynk+1){
        double sc=0;
        REP(i,ks){
            int m=0;
            for (int j=i; j<n; j+=ks) y[m++]=x[j];
            sc+=computedistribscore(y,m);//just comparing char distribution against english language
        }
        tb.pb(MP(sc/ks,ks));
    }
    sort(ALL(tb));

    key=getb(trynk);
    int ks=0;

    REPV(_i,min(trynk,ncnd)){
        ks=tb[_i].ND;
        if (!quiet) printf("%d-TH CANDIDATE:\n",_i+1);
        REP(i,ks){
            int m=0; 
            for (int j=i; j<n; j+=ks) y[m++]=x[j];
            key[i]=singlexorcnd(y,m,1)[0];
        }
        key[ks]=0;
        if (!quiet){
            char *res=getb(n);
            blockxorenc(x,n,key,ks,res);
            printf("FOR KEY %s, have:\n",key);
            printf("==START==\n");
            REP(i,n) printf("%c",isspace(res[i])||isprint(res[i])?res[i]:'?');
            puts("");
            printf("==END==\n");
        }
    }
    return ks;

}

void go1(){
    char *bufa="49276d206b696c6c696e6720796f757220627261696e206c696b65206120706f69736f6e6f7573206d757368726f6f6d";
    char *bufb="SSdtIGtpbGxpbmcgeW91ciBicmFpbiBsaWtlIGEgcG9pc29ub3VzIG11c2hyb29t";

    char *x,*y,*z;
    int n,m;

    n=hextobyte(bufa,x);
    n=b64e(x,n,y);
    assert(!memcmp(bufb,y,n));

    n=b64d(bufb,strlen(bufb),z);
    n=bytetohex(z,n,y);
    assert(!memcmp(bufa,y,n));


}

void go2(){
    char *a="1c0111001f010100061a024b53535009181c";
    char *b="686974207468652062756c6c277320657965";
    char *res="746865206b696420646f6e277420706c6179";

    char *x, *y, *z; 
    int n;
    n=hextobyte(a,x);
    hextobyte(b,y);

    z=getb(n);
    REP(i,n) z[i]=x[i]^y[i];
    n=bytetohex(z,n,x);

    assert(!memcmp(res,x,n));
}

void go3(){
    char *a="1b37373331363f78151b7f2b783431333d78397828372d363c78373e783a393b3736";
    char *x;

    int n=hextobyte(a,x);
    solvexor(x,n);
}

void go4(){
    char a[66];
    char *x;
    FILE *f=fopen("ex4.txt","r");
    double best=oo;
    while(fscanf(f," %s",a)>0){
        int n=hextobyte(a,x);
        best=solvexor(x,n,best);
    }
}

void go5(){
    char *res="0b3637272a2b2e63622c2e69692a23693a2a3c6324202d623d63343c2a26226324272765272a282b2f20430a652e2c652a3124333a653e2b2027630c692b20283165286326302e27282f";
    char *plain="Burning 'em, if you ain't quick and nimble\nI go crazy when I hear a cymbal";
    char *key="ICE";
    char *x,*y,*z;
    int n=strlen(plain);

    x=getb(n);
    blockxorenc(plain,n,key,3,x);
    disphex(x,n);

    int m=hextobyte(res,y);

    assert(n==m);
    assert(!memcmp(x,y,n));
}


void go6(){
    char a[maxs];
    int n=0;
    FILE *f=fopen("ex6.txt","r");
    while(fscanf(f," %s",a+n)>0) n+=strlen(a+n);
    char *x,*y,*z;

    n=b64d(a,n,x);
    int ks=solveblockxor(x,n,y);

    z=getb(n);
    blockxorenc(x,n,y,ks,z);
    printf("RESULT FOR KEY <%s>:\n",y);
    cout<<z<<endl;
    //char *keyres="Terminator X: Bring the noise";
    //assert(ks==strlen(keyres));
    //assert(!memcmp(keyres,y,ks));
}
void go7(){

    /*

BASH:

a=`echo "YELLOW SUBMARINE" | xxd -ps`
openssl enc -aes-128-ecb -d -a -K $a -nosalt < ex7.txt

==== OUTPUT >> ~same lyrics as previous exo
       */
    printf("SEE SOURCE CODE go7() for bash commands, result is lyrics from previous exercise\n");
}

void go8(){
    char buf[maxs];
    FILE *f=fopen("ex8.txt","r");
    int step=0;
    while(fscanf(f," %s",buf)>0){
        ++step;
        int n=strlen(buf);
        set<string> uu;
        int cnt=0;
        for (int i=0; i<n; i+=32){
            ++cnt;
            string a;
            REP(j,32) a+=buf[i+j];
            uu.insert(a);
        }
        if (uu.size()!=cnt){
            printf("%d-th step has duplicate 16bytes\n",step);
            printf("it is cipher: %s\n",buf);
        }

    }
    /*
       133-th cipher
       d880619740a8a19b7840a8a31c810a3d08649af70dc06f4fd5d2d69c744cd283e2dd052f6b641dbf9d11b0348542bb5708649af70dc06f4fd5d2d69c744cd2839475c9dfdbc1d46597949d9c7e82bf5a08649af70dc06f4fd5d2d69c744cd28397a93eab8d6aecd566489154789a6b0308649af70dc06f4fd5d2d69c744cd283d403180c98c8f6db1f2a3f9c4040deb0ab51b29933f2c123c58386b06fba186ad880619740a8a19b7840a8a31c810a3d08649af70dc06f4fd5d2d69c744cd283e2dd052f6b641dbf9d11b0348542bb5708649af70dc06f4fd5d2d69c744cd2839475c9dfdbc1d46597949d9c7e82bf5a08649af70dc06f4fd5d2d69c744cd28397a93eab8d6aecd566489154789a6b0308649af70dc06f4fd5d2d69c744cd283d403180c98c8f6db1f2a3f9c4040deb0ab51b29933f2c123c58386b06fba186a
       */
}

void go(int i){
    puts("");
    puts("");
    puts("");
    puts("");
    printf("RESULT EXO %d\n",i+1);
    if (i==0) go1();
    if (i==1) go2();
    if (i==2) go3();
    if (i==3) go4();
    if (i==4) go5();
    if (i==5) go6();
    if (i==6) go7();
    if (i==7) go8();
}

int main(int argc, char **argv){
    REP(i,27) sfreq[i]=i;
    sort(sfreq,sfreq+27,cmp1);

    REP(i,64) rm64[m64[i]]=i;

    assert(argc>=2);
    int x; sscanf(argv[1]," %d",&x);
    int nc=8;

    if (x==-1) REP(i,nc) go(i);
    else{
        assert(x>=0 && x<nc);
        go(x);
    }

    return 0;
}

