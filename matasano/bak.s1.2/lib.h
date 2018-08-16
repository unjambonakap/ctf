#ifndef LIB_H
#define LIB_H

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

#include<openssl/aes.h>

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
typedef vector<pair<string,string> > cookie;

const int maxs=1e8;
const double oo=1e9;

const double freq[]={12.02,9.10,8.12,7.68,7.31,6.95,6.28,6.02,5.92,4.32,3.98,2.88,2.71,2.61,2.30,2.11,2.09,2.03,1.82,1.49,1.11,0.69,0.17,0.11,0.10,0.07,0};
struct Utils{

    const char *m64;
    int sfreq[27];
    int rm64[128];

    char buf[maxs];
    int pos;
    struct cmp1{
        bool operator()(int a, int b){return freq[a]<freq[b];}
    };

    Utils(){
        pos=0;
        m64="ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/";
        REP(i,27) sfreq[i]=i;
        sort(sfreq,sfreq+27,cmp1());
        REP(i,64) rm64[m64[i]]=i;

        initkey();

    }

    double sq(double a){return a*a;}

    void fillrand(char *a, int n){ REP(i,n) a[i]=rand()&0xff; }
    void disphex(char *a, int n){REP(i,n) printf("%02x",(unsigned char)a[i]); puts("");}
    void disptext(char *a, int n){REP(i,n) printf("%c", isprint(a[i])||isspace(a[i])?a[i]:'?');puts("");}

    char *copy(char *a, int n){char *x=getb(n); memcpy(x,a,n); return x;}

    char *getb(int n){ assert(pos+n<maxs);int u=pos; pos+=n+1; return buf+u; }

    char *readfile(char *fname){
        char *a=getb(11111);
        int n=0;
        FILE *f=fopen(fname,"r");
        while(fscanf(f," %s",a+n)>0) n+=strlen(a+n);
        assert(n<11111);
        return a;
    }

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
        int sz=(n+3)*3/4-pad+100;
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

    int rpkcs7(char *s, int n){
        int x=s[n-1];
        for (int i=n-1; i>=n-x; --i) if (s[i]!=x) throw "PADDING ERROR";
        return n-x;
    }

    int pkcs7(char *a, int n, int bs, char *&b){
        assert(bs<256);
        int u=bs-n%bs;
        b=getb(n+u);
        memcpy(b,a,n);
        REP(i,u) b[n+i]=u;
        return n+u;
    }

    int aes_ecb_encrypt(char *a, char *&out, int n, AES_KEY *key){
        int bs=16;
        char *b;
        n=pkcs7(a,n,bs,b);
        out=getb(n);
        REP(i,n/bs) AES_ecb_encrypt(b+i*bs,out+i*bs,key,AES_ENCRYPT);
        return n;
    }

    int aes_cbc_encrypt(char *a, char *&out, int n, AES_KEY *key, char *iv){
        int bs=16;
        char *b;
        n=pkcs7(a,n,bs,b);
        out=getb(n);
        AES_cbc_encrypt(b,out,n,key,iv,AES_ENCRYPT);
        return n;
    }

    int aes_ecb_decrypt(char *a, char *&out, int n, AES_KEY *key){
        int bs=16;
        out=getb(n);
        REP(i,n/bs) AES_ecb_encrypt(a+i*bs,out+i*bs,key,AES_DECRYPT);
        return rpkcs7(out,n);
    }

    int aes_cbc_decrypt(char *a, char *&out, int n, AES_KEY *key, char *iv){
        int bs=16;
        out=getb(n);
        AES_cbc_encrypt(a,out,n,key,iv,AES_DECRYPT);
        return rpkcs7(out,n);
    }

    int cbcxordec(char *a, int n, char *iv, int bs, char *key, int nk, char *&b){
        assert(n%bs==0);
        b=getb(n);
        AES_KEY key2;
        AES_set_decrypt_key(key,nk*8,&key2);
        char *x=getb(bs);
        REP(i,n/bs){
            AES_decrypt(a+i*bs,b+i*bs,&key2);
            blockxorenc(b+i*bs,bs,iv,bs,b+i*bs);
            iv=a+i*bs;
        }
        return n;
    }




    int oracle1(char *a, int n, char *&res, int &used){
        int n1=rand()%6+5;
        int n2=rand()%6+5;
        char *b=getb(n+n1+n2);
        memcpy(b,a+n1,n);
        fillrand(b,n1);
        fillrand(b+n+n1,n2);
        n=pkcs7(b,n1+n2+n,16,a);

        char *kk=getb(16);
        fillrand(kk,16);
        AES_KEY key;
        AES_set_encrypt_key(kk,16*8,&key);

        used=rand()/(RAND_MAX/2)&1;
        if (used){
            char *iv=getb(16);
            fillrand(iv,16);
            n=aes_cbc_encrypt(b,res,n,&key,iv);
        }else{
            n=aes_ecb_encrypt(b,res,n,&key);
        }
        return n;
    }

    AES_KEY KEYA, RKEYA;
    char *prefix;
    int nprefix;
    char IVA[16];
    char tmpiv[16];
    void initkey(){
        char kk[16];
        fillrand(kk,16);
        fillrand(IVA,16);

        nprefix=rand()%32+5;
        printf("APPENDING %d\n",nprefix);
        prefix=getb(nprefix);
        fillrand(prefix,nprefix);
        
        AES_set_encrypt_key(kk,16*8,&KEYA);
        AES_set_decrypt_key(kk,16*8,&RKEYA);
    }

    int oracle2(char *a, int n, char *&res){
        char *ustr="Um9sbGluJyBpbiBteSA1LjAKV2l0aCBteSByYWctdG9wIGRvd24gc28gbXkgaGFpciBjYW4gYmxvdwpUaGUgZ2lybGllcyBvbiBzdGFuZGJ5IHdhdmluZyBqdXN0IHRvIHNheSBoaQpEaWQgeW91IHN0b3A/IE5vLCBJIGp1c3QgZHJvdmUgYnkK";
        char *x;
        int m=b64d(ustr,strlen(ustr),x);

        char *b=getb(n+m);
        memcpy(b,a,n); memcpy(b+n,x,m);
        n+=m;
        return aes_ecb_encrypt(b,res,n,&KEYA);
    }

    int oracle2a(char *a, int n, char *&res){
        char *ustr="Um9sbGluJyBpbiBteSA1LjAKV2l0aCBteSByYWctdG9wIGRvd24gc28gbXkgaGFpciBjYW4gYmxvdwpUaGUgZ2lybGllcyBvbiBzdGFuZGJ5IHdhdmluZyBqdXN0IHRvIHNheSBoaQpEaWQgeW91IHN0b3A/IE5vLCBJIGp1c3QgZHJvdmUgYnkK";
        char *x;
        int m=b64d(ustr,strlen(ustr),x);

        char *b=getb(n+m+nprefix);
        memcpy(b,prefix,nprefix);
        memcpy(b+nprefix,a,n); memcpy(b+n+nprefix,x,m);
        n+=m+nprefix;
        int tmp=aes_ecb_encrypt(b,res,n,&KEYA);
        return tmp;
    }



    int decodecookie(char *s, cookie &res){
        int n=strlen(s);

        res.clear();
        for (int i=0; i<n;){
            int j,k;
            for (j=i; j<n && s[j]!='&'; ++j);
            int pos=-1;
            for (k=i; k<j; ++k) if (s[k]=='='){
                if (pos!=-1) return -1;
                pos=k;
            }
            if (pos==-1) return -1;
            res.pb(MP(string(s+i,k-i),string(s+k+1,j-k-1)));
        }
        return 0;
    }


    int profile_for(const string &email, char *&cc, char *&cipher){
        string s;
        REP(i,email.size()) if (email[i]!='&'&&email[i]!='=') s+=email[i];
        string u;
        u+="email="+s+"&uid=10&role=user";

        int n=u.size();
        cc=copy(u.c_str(),n);
        return aes_ecb_encrypt(cc,cipher,n,&KEYA);
    }

    int decrypt_profile(char *a, int n, char *&res){
        return aes_ecb_decrypt(a,res,n,&RKEYA);
    }
    void dispcookie(cookie &a){
        FE(it,a) printf("'%s': '%s' \n",it->ST.c_str(),it->ND.c_str());
    }


    int enc3(char *a, int n, char *&res){

        char *st="comment1=cooking%20MCs;userdata=";
        char *nd=";comment2=%20like%20a%20pound%20of%20bacon";
        char *colon="%3B", *equal="%3D";
        int na=strlen(st), nb=strlen(nd);
        int c=0;
        REP(i,n) c+=a[i]==';'||a[i]=='=';
        char *x=getb(n+na+nb+2*c);
        memcpy(x,st,na);
        int nx=na;
        REP(i,n){
            if (a[i]==';') memcpy(x+nx,colon,3), nx+=3;
            else if (a[i]=='=') memcpy(x+nx,equal,3), nx+=3;
            else x[nx++]=a[i];
        }
        memcpy(x+nx,nd,nb);
        nx+=nb;
        memcpy(tmpiv,IVA,16);
        return aes_cbc_encrypt(x,res,nx,&KEYA,tmpiv);
    }

    int checkit(char *a, int n){
        char *res;
        char *pattern=";admin=true;";
        memcpy(tmpiv,IVA,16);
        n=aes_cbc_decrypt(a,res,n,&RKEYA,tmpiv);
        disptext(res,n);
        int nx=strlen(pattern);
        return strstr(res,pattern)!=0;
    }




};

#endif
