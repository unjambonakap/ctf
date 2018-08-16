#include<boost/random/mersenne_twister.hpp>
#include"crypto.h"
#include"helper.h"
#include<stdarg.h>

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


void go1(){
    const char *nump="ffffffffffffffffc90fdaa22168c234c4c6628b80dc1cd129024e088a67cc74020bbea63b139b22514a08798e3404ddef9519b3cd3a431b302b0a6df25f14374fe1356d6d51c245e485b576625e7ec6f44c42e9a637ed6b0bff5cb6f406b7edee386bfb5a899fa5ae9f24117c4b1fe649286651ece45b3dc2007cb8a163bf0598da48361c55d39a69163fa8fd24cf5f83655d23dca3ad961c62f356208552bb9ed529077096966d670c354e4abc9804f1746c08ca237327ffffffffffffffff";
    mpz_t p,g,a,b,A,B,s1,s2;
    mpz_inits(p,g,a,b,A,B,s1,s2,NULL);

    mpz_set_ui(g,2);
    mpz_set_str(p,nump,16);

    mpz_urandomm(a,randstate,p);
    mpz_urandomm(b,randstate,p);

    mpz_powm(A,g,a,p);
    mpz_powm(B,g,b,p);

    mpz_powm(s1,A,b,p);
    mpz_powm(s2,B,a,p);

    cout<<mpz_get_str(0,16,s1)<<endl;
    cout<<mpz_get_str(0,16,s2)<<endl;
    //leak, iknow

    assert(mpz_cmp(s1,s2)==0);
    mpz_clears(p,g,a,b,A,B,s1,s2,NULL);
}





void go2(){
    mDH_manager A;
    puts("FUU");
    A.go1();
    A.go2();
}

void go3(){
    mDH_manager A;
    puts("FUU");
    A.go3();
}

void go4(){
    SRP_manager A;
    SRP_C a;
    SRP_S b;
    A.go1(a,b);
}
void go5(){
    SRP_manager A;
    //send zero => s=0 => hmac(0,salt)
    SRP_C_zero a;
    SRP_S b;
    A.go1(a,b);
}
void go6(){
    SRP2_manager A;
    SRP2_C a,c;
    SRP2_S b;
    A.go1(a,b); //just checking protocol works

    //trying every word, compute x on fake server => S => hmac(...), compare to the one computed by client til it is the same.
    //choose value of B,u... to speed up computations 
    //it can take a lot of time, if we pick b=1 and u=1, it is quicker (A LOT)

    printf("gogo 2\n");
    SRP2_fake d;
    A.go1(c,d);

    /*
       using /usr/share/dict/words
       output>>>
       ...
       on 276600/479829
       on 276700/479829
       on 276800/479829
       on 276900/479829
       PASSWORD IS zygomaticofacial
       TOOK 194 seconds
       DONE
       */

}
void go7(){
    rsa test;
    test.gen();

    test.decrypt(test.encrypt(buffer("42"))).getstr().disptext();


}
void go8(){
    rsa a;
    buffer plain="zygomaticofacial";
    vector<pair<bignum,bignum> > tb;
    REP(i,3){
        rsa a; a.gen();
        tb.pb(MP(a.encryptstr(plain),a.n));
    }
    bignum res=crt(tb);
    bignum sol;
    mpz_root(sol.a,res.a,3);

    buffer ans=sol.getstr().hextobyte();
    printf("obtain "); ans.disptext();
    assert(ans==plain);

}

void go(int i){
    srand(0);
    puts("");
    puts("");
    puts("");
    puts("");
    printf("RESULT EXO %d\n",i);
    if (i==1) go1();
    if (i==2) go2();
    if (i==3) go3();
    if (i==4) go4();
    if (i==5) go5();
    if (i==6) go6();
    if (i==7) go7();
    if (i==8) go8();
}

int main(int argc, char **argv){
    assert(argc>=2);
    inithelper();
    initcrypto();
    int x; sscanf(argv[1]," %d",&x);
    int nc=8;

    if (x==-1) REP(i,nc) go(i);
    else{
        assert(x>=1 && x<=nc);
        go(x);
    }

    return 0;
}
