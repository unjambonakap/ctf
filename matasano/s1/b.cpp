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

#include "lib.h"

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


Utils A;

void go1(){
    char *a="YELLOW SUBMARINE";
    char *b;
    int nb;
    nb=A.pkcs7(a,strlen(a),20,b);
    A.disphex(b,nb);
}

void go2(){
    char *a=A.readfile("ex9.txt");
    int n=strlen(a);
    char *b;
    n=A.b64d(a,n,b);

    char *key="YELLOW SUBMARINE";
    int nk=strlen(key);
    int bs=16;
    char *iv=A.getb(bs);
    memset(iv,0,bs);

    char *x;
    int m=A.cbcxordec(b,n,iv,bs,key,nk,x);
    A.disptext(x,m);

}
void go3(){

    int sz=4*16;
    char *buf=A.getb(sz);
    memset(buf,'a',sz);
    REP(step,100){
        char *res;
        int ans;
        int n=A.oracle1(buf,sz,res,ans);
        int diff=0;
        REP(i,16) if (res[16+i]!=res[32+i]){diff=1; break;}
        assert(diff==ans);
    }
    puts("success");

}
void go4(){
    char buf[32], *res;
    char x[1111]={0}, *ans;
    ans=x+16;
    memset(buf,0,32);
    int sz=0;
    int prev=-1;
    int nans=-1;
    for (int i=0; nans==-1 || i<nans; ++i){
        REP(j,15) buf[j]=ans[i-15+j];
        //want block finishing at pos i
        int pad=15-i&0xf;
        REP(v,256){
            buf[15]=v;
            int n=A.oracle2(buf,16+pad,res);
            if (nans==-1 && !v){
                if (prev==-1) prev=n;
                else if (prev!=n) nans=n-16-pad;
            }
            int ok=1;
            REP(j,16) if (res[j]!=res[16+pad+i-15+j]){ok=0; break;}

            if (ok){
                ans[i]=v;
                goto done;
            }
        }
        printf("FAIL ON STEP %d\n",i);
        assert(0);
done:;
    }

    ans[nans]=0;

    puts("RESULT >>> ");
    cout<<ans<<endl;
}

void go5(){
    /*
       Principle
       we have:
       email=X&uid=10&role=user

       (16 char block)
       A=(email=str) >> #str=16-#(email=)=10
       B=(AAA&uid=10&role=)
       C=(admin&uid=10&rol)
       (e=user============)

       now depending on the implementation of the cookie parser
       possible to scramble last chunk so that we have at least one &, no = nor a 'e' as first letter (randomly, it should be obtained quite quickly)

       */
    char *cc;
    char *res1, *res2;
    int n1, n2;
    char *p1="0123456789AAA";
    char *p2="0123456789admin";
    n1=A.profile_for(string(p1),cc,res1);
    n2=A.profile_for(string(p2),cc,res2);

    char buf[64];
    memcpy(buf,res1,32);
    memcpy(buf+32,res2+16,32);

    n1=A.decrypt_profile(buf,64,cc);
    printf("DECRYPTED MESSAGE: \n");
    cout<<cc<<endl;
}


void go6(){
    /*
       same idea as ex4
       but we need to be able to
       (prefix+0000)
       (XX+unknown)
       we must have XX at a beginning of a block 

       do it with large sled of 0
cipher:
(rand)(rand)(cipher(0))...(cipher(0))(cipher(000+unk))(cipher(unk))

then add 0 till the number of cipher(0) increases
=> we'll now that we have a last one



       */
    const int maxp=16*10*2;

    char buf[32+maxp+32]={0}, *res;
    char x[1111]={0}, *ans;
    ans=x+16;
    int sz=0;
    int prev=-1;
    int nans=-1;

    int st, from;

    int cnt=-1;
    for (int i=0; i<20; ++i){
        assert(i<=17);
        buf[maxp+i]=1;//to avoid a 0 byte in unknown buffer as first byte
        int mid=maxp/2;//multiple of 16
        int m=maxp+i+1;
        int n=A.oracle2a(buf,m,res);
        int cnt2=0;
        int j;
        for (j=mid; j+16<=n; j+=16, ++cnt2) if (memcmp(res+mid,res+j,16)) break;
        
        if (cnt==-1) cnt=cnt2;
        else{
            assert(cnt==cnt2 || cnt+1==cnt2);
            st=maxp+i;
            from=j;
            if (cnt+1==cnt2) break;
        }
        buf[maxp+i]=0;
    }

    for (int i=0; nans==-1 || i<nans; ++i){
        REP(j,15) buf[st+j]=ans[i-15+j];
        //want block finishing at pos i
        int pad=15-i&0xf;
        REP(v,256){
            buf[st+15]=v;
            int n=A.oracle2a(buf,st+16+pad,res);
            n-=from;
            if (nans==-1 && !v){
                if (prev==-1) prev=n;
                else if (prev!=n) nans=n-16-pad;
            }
            int ok=1;
            res+=from;
            REP(j,16) if (res[j]!=res[16+pad+i-15+j]){ok=0; break;}

            if (ok){
                ans[i]=v;
                goto done;
            }
        }
        printf("FAIL ON STEP %d\n",i);
        assert(0);
done:;
    }

    ans[nans]=0;

    puts("RESULT >>> ");
    cout<<ans<<endl;
}



void go7(){
    char *s="ICE ICE BABY\x04\x04\x04\x04";
    char *s2="ICE ICE BABY\x05\x05\x05\x05";
    char *s3="ICE ICE BABY\x01\x02\x03\x04";
    char *tb[]={s,s2,s3};
    for (int i=0; i<3; ++i){
        char *x=tb[i];
        printf("STRIP PADDING OF :"); A.disphex(x,strlen(x));
        try{
            char *res;
            int n=A.rpkcs7(x,strlen(x));
            printf("SUCCESSFUL: >>"); A.disphex(x,n);
        }catch(...){
            printf("FAIL\n");
        }
    }


}
void go8(){
    //because it uses Ci-1 as the IV

    char *u=";admin=true;aaaa";
    int nx=222;
    char tmp[nx];
    memset(tmp,'a',nx);
    int pos=128;
    char xx[16];
    char *st="comment1=cooking%20MCs;userdata=";

    char *res;
    int n=A.enc3(tmp,nx,res);
    REP(i,16) res[pos+i]^=u[i]^'a';
    int ans=A.checkit(res,n);
    printf("%d\n",ans);


}

void go(int i){
    srand(0);
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
