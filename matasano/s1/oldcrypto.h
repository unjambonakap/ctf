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

struct bignum{
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
    void disp()const{getstr().disptext();}


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
};


struct mDH{
    mpz_t p,g,a,b,A,B,s;
    AES_KEY key1,rkey1,key2,rkey2;

    mDH(){ mpz_inits(p,g,a,b,A,B,s,NULL); }
    ~mDH(){ mpz_clears(p,g,a,b,A,B,s,NULL); }

    void gen_pg(){
        const char *nump="ffffffffffffffffc90fdaa22168c234c4c6628b80dc1cd129024e088a67cc74020bbea63b139b22514a08798e3404ddef9519b3cd3a431b302b0a6df25f14374fe1356d6d51c245e485b576625e7ec6f44c42e9a637ed6b0bff5cb6f406b7edee386bfb5a899fa5ae9f24117c4b1fe649286651ece45b3dc2007cb8a163bf0598da48361c55d39a69163fa8fd24cf5f83655d23dca3ad961c62f356208552bb9ed529077096966d670c354e4abc9804f1746c08ca237327ffffffffffffffff";
        mpz_set_ui(g,2);
        mpz_set_str(p,nump,16);
    }

    void set_pg(mpz_t ip, mpz_t ig){
        mpz_set(p,ip);
        mpz_set(g,ig);
    }

    void gen_A(mpz_t a, mpz_t A){
        mpz_urandomm(a,randstate,p);
        mpz_powm(A,g,a,p);
    }

    void setkey(mpz_t s, AES_KEY *key, AES_KEY *rkey){
        char *u=mpz_get_str(0,16,s);
        cout<<u<<endl;
        buffer x=buffer(u).hextobyte();
        x=sha1(x);
        x.n=16;
        puts("SET KEY");
        x.disphex();
        AES_set_encrypt_key(x.a,16*8,key);
        AES_set_decrypt_key(x.a,16*8,rkey);
        free(u);
    }

    buffer send_msg(const buffer &msg, AES_KEY *key){
        buffer iv=buffer::Rand(16);
        return aes_cbc_encrypt(msg,iv,key)+iv;
    }

    buffer recv_msg(const buffer &msg, AES_KEY *rkey){
        buffer iv=msg.a+msg.n-16;
        buffer x(msg.a,msg.n-16);
        return aes_cbc_decrypt(x,iv,rkey);
    }


    virtual buffer recv_msgA(const buffer &msg){assert(0);}
    virtual buffer recv_msgB(const buffer &msg){assert(0);}

    buffer recv_msg(const buffer &msg){return recv_msg(msg,&rkey1);}
    buffer send_msg(const buffer &msg){return send_msg(msg,&key1);}


};

struct mDH_bot1:public mDH{

    void gen_pgA(){
        gen_pg();
        mDH::gen_A(a,A);
    }


    void gen_A(){mDH::gen_A(a,A);}

    void recv_key(mpz_t ip, mpz_t ig, mpz_t iB){
        set_pg(ip,ig);

        gen_A();
        set_B(iB);
    }

    void set_B(mpz_t iB){
        mpz_set(B,iB);
        mpz_powm(s,B,a,p);
        setkey(s,&key1,&rkey1);
    }
};

struct mDH_atc1: public mDH{
    mpz_t ap,ag,aA,aB;
    mpz_t bp,bg,bA,bB;
    mDH_atc1(){ mpz_inits(ap,ag,aA,aB,bp,bg,bA,bB,NULL); }
    ~mDH_atc1(){ mpz_clears(ap,ag,aA,aB,bp,bg,bA,bB,NULL); }

    void recv_key1(mpz_t ip, mpz_t ig, mpz_t iA){
        mpz_set(p,ip);
        mpz_set(g,ig);
        mpz_set(aA,iA);

        gen_A(a,A);
        gen_A(b,B);

        mpz_powm(s,aA,b,p);
        setkey(s,&key1,&rkey1);
    }

    void recv_key2(mpz_t iB){
        mpz_set(bB,iB);
        mpz_powm(s,bB,a,p);
        setkey(s,&key2,&rkey2);
    }
    

    buffer recv_msgA(const buffer &msg){
        buffer u=recv_msg(msg,&rkey1);
        printf("FROM A=>B, reading: "); u.disptext();
        return send_msg(u,&key2);
    }
    buffer recv_msgB(const buffer &msg){
        buffer u=recv_msg(msg,&rkey2);
        printf("FROM B=>A, reading: "); u.disptext();
        return send_msg(u,&key1);
    }
};



struct mDH_atc2: public mDH{
    mpz_t ap,ag,aA,aB;
    mpz_t bp,bg,bA,bB;
    mDH_atc2(){ mpz_inits(ap,ag,aA,aB,bp,bg,bA,bB,NULL); }
    ~mDH_atc2(){ mpz_clears(ap,ag,aA,aB,bp,bg,bA,bB,NULL); }

    void recv_key1(mpz_t ip, mpz_t ig, mpz_t iA){
        mpz_set(p,ip);
        mpz_set(g,ig);

        mpz_set_ui(s,0);//using null key (p^whatev=0)
        setkey(s,&key1,&rkey1);
    }

    void recv_key2(mpz_t iB){
    }
    

    buffer recv_msgA(const buffer &msg){
        buffer u=recv_msg(msg,&rkey1);
        printf("FROM A=>B, reading: "); u.disptext();
        return msg;
    }
    buffer recv_msgB(const buffer &msg){
        buffer u=recv_msg(msg,&rkey1);
        printf("FROM B=>A, reading: "); u.disptext();
        return msg;//
    }
};


struct mDH_atc3: public mDH{
    mpz_t p,g,bA,aB;
    int mode;
    mDH_atc3(int i):mode(i){ mpz_inits(p,g,bA,aB,NULL); }
    ~mDH_atc3(){ mpz_clears(p,g,bA,aB,NULL); }

    void recv_key1(mpz_t ip, mpz_t ig){
        mpz_set(p,ip);
        mpz_set(g,ig);
        if (mode==0) mpz_set_ui(g,1);
        else if (mode==1) mpz_set(g,p);
        else if (mode==2) mpz_sub_ui(g,p,1);
    }

    void setA(mpz_t ia){

    }
    void setB(mpz_t ib){

    }

    void setup(){
        if (mode==0){
            /*
               g=1
               > B=1 >> Sa=B^a=1
               Sb=A^b >> set A=1
               */
            mpz_set_ui(bA,1);
            mpz_set_ui(aB,1);
            puts("SETTING ATC KEYS");
            setkey(g,&key1,&rkey1);
        }else if (mode==1){
            /*
               (unless a=0, not very likely :))
               g=0
               > B=0 >> Sa=B^a=0
               Sb=A^b >> set A=0
               */
            mpz_set_ui(bA,0);
            setkey(bA,&key1,&rkey1);
        }else{
            /*
               g=-1
               > B=1 or -1
               if B=1 > see mode=0
               if B=-1
                >> b odd
                sA=1 or -1, depending on a (unknown)
                sB=A^b. We could determine sA knowing if a is quadratic residue, but whatever
                let's just force the case sA=sB=1
               */
            mpz_set_ui(bA,1);
            mpz_set_ui(aB,1);

            setkey(bA,&key1,&rkey1);
        }
    }

    buffer recv_msgA(const buffer &msg){
        int fd=0;
        try{
            buffer u=recv_msg(msg,&rkey1);
            printf("FROM A=>B, reading: "); u.disptext();
            fd=1;
        }catch(...){printf("FUUU RERRor\n");}

        return msg;
    }
    buffer recv_msgB(const buffer &msg){
        return recv_msgA(msg);
    }
};



struct mDH_manager{

    void roundtrip(const buffer &msg, mDH &b1, mDH &b2, mDH &M){
        puts("");
        printf("sending %s\n",msg.a);

        buffer tmp=b1.send_msg(msg);
        tmp=M.recv_msgA(tmp);
        buffer res=b2.recv_msg(tmp);

        tmp=b2.send_msg(res);
        tmp=M.recv_msgB(tmp);
        res=b1.recv_msg(tmp);

        printf("after round trip: "); res.disptext();

        assert(res==msg);
    
    }


    void go1(){
        //standard mitm
        mDH_bot1 b1,b2;
        mDH_atc1 M;

        b1.gen_pgA();
        M.recv_key1(b1.p,b1.g,b1.A);
        b2.recv_key(M.p,M.g,M.A);
        M.recv_key2(b2.A);
        b1.set_B(M.B);


        roundtrip("abcdjfoe",b1,b2,M);
    }
    void go2(){
        //using p as B
        mDH_bot1 b1,b2;
        mDH_atc2 M;

        b1.gen_pgA();
        M.recv_key1(b1.p,b1.g,b1.A);
        b2.recv_key(M.p,M.g,M.p);
        M.recv_key2(b2.A);
        b1.set_B(M.p);


        roundtrip("GO2abcdjfoe",b1,b2,M);
    }

    void go3(){
        //using p as B
        REP(i,3){
            mDH_bot1 b1,b2;
            mDH_atc3 M(i);

            b1.gen_pg();
            M.recv_key1(b1.p,b1.g);
            b2.set_pg(M.p,M.g);

            printf("SET FOR B2\n");
            b1.gen_A();
            b2.gen_A();

            M.setA(b1.A);
            M.setB(b2.A);
            M.setup();

            b2.set_B(M.bA);
            b1.set_B(M.aB);

            roundtrip("GO3aIIIIIIbcdjfoe",b1,b2,M);
        }
    }
};
struct SRP_C{
    bignum N,g,k,A,B,a,x,u;
    buffer login,pass,salt;

    virtual void init(const buffer &_login, const buffer &_pass,const char *nump){

        login=_login;
        pass=_pass;
        N=buffer(nump); g=2; k=3;

        a=bignum::rand(N);
    }
    virtual void preproc(){
        A=g.powm(a,N);
    }


    virtual void recv1(const buffer &isalt, const bignum &iB){
        B=iB;
        salt=isalt;
    }

    virtual buffer dostuff(){
        buffer sA=A.getstr(16), sB=B.getstr(16);

        u=sha256(sA+sB).bytetohex();
        x=sha256(salt+pass).bytetohex();

        bignum S=((B-k*g.powm(x,N))%N).powm(a+u*x,N);


        buffer K=sha256(S.getstr(16).hextobyte());
        return hmac256(K,salt);
    }

};

struct SRP_S{
    bignum N,g,k,A,B,v,b;
    buffer login,pass,salt;

    virtual void init(const buffer &_login, const buffer &_pass, const char *nump){
        login=_login;
        pass=_pass;
        N=buffer(nump); g=2; k=3;

        b=bignum::rand(N);
    }
    virtual void preproc(){}

    virtual void recv1(const buffer &ilogin, const bignum &iA){
        A=iA; 
        salt=buffer::Rand(16);

        bignum x=sha256(salt+pass).bytetohex();
        v=g.powm(x,N);
        B=(k*v+g.powm(b,N))%N;
        //this step should be done after we know which email, doesnt matter tho
        v=g.powm(x,N);
    }


    virtual bool checkit(const buffer &res){
        buffer sA=A.getstr(16), sB=B.getstr(16);
        bignum u=sha256(sA+sB).bytetohex();
        bignum S=(A*(v.powm(u,N))).powm(b,N);

        S.getstr().disptext();

        buffer K=sha256(S.getstr(16).hextobyte());
        buffer expect=hmac256(K,salt);
        printf("expecting\t"); expect.disphex();
        printf("got \t\t"); res.disphex();
        return expect==res;
    }
};


struct SRP_C_zero :SRP_C{
    void preproc(){
        A=0;
    }

    buffer dostuff(){
        printf("DOING STUFF HERE\n");
        buffer K=sha256(buffer("0").hextobyte());
        return hmac256(K,salt);
    }

};



struct SRP_manager{
    void go1(SRP_C &c, SRP_S &s){
        const char *nump="ffffffffffffffffc90fdaa22168c234c4c6628b80dc1cd129024e088a67cc74020bbea63b139b22514a08798e3404ddef9519b3cd3a431b302b0a6df25f14374fe1356d6d51c245e485b576625e7ec6f44c42e9a637ed6b0bff5cb6f406b7edee386bfb5a899fa5ae9f24117c4b1fe649286651ece45b3dc2007cb8a163bf0598da48361c55d39a69163fa8fd24cf5f83655d23dca3ad961c62f356208552bb9ed529077096966d670c354e4abc9804f1746c08ca237327ffffffffffffffff";
        buffer login="guest", pass="admin";
        c.init(login,pass,nump);
        s.init(login,pass,nump);

        c.preproc();
        s.preproc();

        s.recv1(c.login,c.A);
        c.recv1(s.salt,s.B);

        buffer xx=c.dostuff();
        bool ok=s.checkit(xx);
        assert(ok);
        printf("DONE\n");

    }
};



struct SRP2_C{
    buffer login, pass, salt;
    bignum N,a,A,B,g,u,S,x;
    void init(const buffer &_login, const buffer &_pass,const char *nump){
        login=_login;
        pass=_pass;
        N=buffer(nump); g=2;
        a=bignum::rand(N);
    }
    void preproc(){
        A=g.powm(a,N);
    }


    void recv1(const buffer &isalt, const bignum &iB, const bignum &iu){
        B=iB;
        u=iu;
        salt=isalt;
    }


    buffer dostuff(){
        x=sha256(salt+pass).bytetohex();
        x.getstr().disptext();
        S=B.powm(a+u*x,N);
        S.getstr().disptext();
        return hmac256(sha256(S.getstr().hextobyte()),salt);
    }
};


struct SRP2_S{
    bignum N,g,A,B,v,b,u;
    buffer login,pass,salt;

    virtual void init(const buffer &_login, const buffer &_pass, const char *nump){
        login=_login;
        pass=_pass;
        N=buffer(nump); g=2;

        b=bignum::rand(N);
        B=g.powm(b,N);
    }
    virtual void preproc(){ u=bignum::rand(N-1); }


    virtual void recv1(const buffer &ilogin, const bignum &iA){
        A=iA; 
        salt=buffer::Rand(16);

        bignum x=sha256(salt+pass).bytetohex();
        v=g.powm(x,N);
    }


    virtual bool checkit(const buffer &res){
        bignum S=(A*v.powm(u,N)).powm(b,N);
        buffer K=sha256(S.getstr().hextobyte());
        buffer expect=hmac256(K,salt);
        printf("expecting\t"); expect.disphex();
        printf("got \t\t"); res.disphex();
        return expect==res;
    }
};


struct SRP2_fake:SRP2_S{
    vector<buffer> dict;

    SRP2_fake(){ dict=readfilebyline((uchar*)"/usr/share/dict/words");random_shuffle(ALL(dict)); }
    void init(const buffer &_login, const buffer &_pass, const char *nump){
        SRP2_S::init(_login,"",nump);//the pass is given, but wont use it :)
        b=1; B=g;
    }
    //it can take a lot of time, if we pick b=1 and u=1, it is quicker (A LOT)


    virtual void preproc(){ u=1;}


    virtual bool checkit(const buffer &res){
        //need to find x => v

        struct timeval st,nd;
        gettimeofday(&st,0);

        REP(i,dict.size()){
            if (i%100==0) printf("on %d/%d\n",i,dict.size());

            bignum x=sha256(salt+dict[i]).bytetohex();
            v=g.powm(x,N);
            bignum S=v*A%N;
            buffer K=sha256(S.getstr().hextobyte());
            buffer expect=hmac256(K,salt);

            if (expect==res){
                printf("PASSWORD IS %s\n",dict[i].a);
                gettimeofday(&nd,0);
                printf("TOOK %Ld seconds\n",nd.tv_sec-st.tv_sec);
                return true;

            }
        }
        return false;
    }
};


struct SRP2_manager{
    void go1(SRP2_C &c, SRP2_S &s){
        const char *nump="ffffffffffffffffc90fdaa22168c234c4c6628b80dc1cd129024e088a67cc74020bbea63b139b22514a08798e3404ddef9519b3cd3a431b302b0a6df25f14374fe1356d6d51c245e485b576625e7ec6f44c42e9a637ed6b0bff5cb6f406b7edee386bfb5a899fa5ae9f24117c4b1fe649286651ece45b3dc2007cb8a163bf0598da48361c55d39a69163fa8fd24cf5f83655d23dca3ad961c62f356208552bb9ed529077096966d670c354e4abc9804f1746c08ca237327ffffffffffffffff";
        buffer login="guest", pass="zygomaticofacial"; //something in /usr/share/dict/words
        c.init(login,pass,nump);
        s.init(login,pass,nump);

        c.preproc();
        s.preproc();

        s.recv1(c.login,c.A);
        c.recv1(s.salt,s.B,s.u);

        buffer xx=c.dostuff();
        bool ok=s.checkit(xx);
        assert(ok);
        printf("DONE\n");

    }
};



struct rsa{
    bignum n,p,q;
    bignum e,d;


    void gen(int ndigit=30){
        while(1){
            buffer x=buffer::Rand(ndigit);
            buffer y=buffer::Rand(ndigit);
            mpz_nextprime(p.a,bignum(x.bytetohex()).a);
            mpz_nextprime(q.a,bignum(y.bytetohex()).a);
            n=p*q;

            bignum et=(p-1)*(q-1);
            e=3;
            d=e.inv(et);
            if (d!=-1) break;
        }
    }

    bignum encrypt(const bignum &m)const{ return m.powm(e,n); }
    bignum decrypt(const bignum &m)const{ return m.powm(d,n); }
    bignum encryptstr(const buffer &a)const{ return bignum(a.bytetohex()).powm(e,n); }//size a > ~1/8 log 2 n will fail
    buffer decryptstr(const bignum &a)const{ return a.powm(d,n).getstr().hextobyte(); }
};

bignum crt(const vector<pair<bignum,bignum> > tb);


#endif


