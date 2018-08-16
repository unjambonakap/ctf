#include<boost/random/mersenne_twister.hpp>
#include "helper.h"

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


struct ex1{

    buffer key;
    ll nonce;
    buffer plain;
    buffer cipher;
    ex1(){
        plain=readfile((uchar*)"ex25.txt");
        plain=plain.fromb64();
        key=buffer::Rand(16);
        nonce=1ll*rand()*rand();
        cipher=ctr_go(plain,key,nonce);
    }

    buffer edit(const buffer &a, int offset, const buffer &b){
        buffer x=ctr_go(a,key,nonce);
        assert(offset>=0 && x.n>=b.n+offset);
        memcpy(x.a+offset,b.a,b.n);
        return ctr_go(x,key,nonce);
    }
};

struct ex2{
    buffer key;
    ll nonce;
    ex2(){
        key=buffer::Rand(16);
        nonce=1ll*rand()*rand();
    }
    
    buffer enc(const buffer &a){

        const char *st="comment1=cooking%20MCs;userdata=";
        const char *nd=";comment2=%20like%20a%20pound%20of%20bacon";
        const char *colon="%3B", *equal="%3D";
        int na=strlen(st), nb=strlen(nd);
        int c=0;
        REP(i,a.n) c+=a[i]==';'||a[i]=='=';
        buffer x(a.n+na+nb+2*c);
        memcpy(x.a,st,na);
        int nx=na;
        REP(i,a.n){
            if (a[i]==';') memcpy(x.a+nx,colon,3), nx+=3;
            else if (a[i]=='=') memcpy(x.a+nx,equal,3), nx+=3;
            else x[nx++]=a[i];
        }
        memcpy(x.a+nx,nd,nb);
        return ctr_go(x,key,nonce);
    }

    int checkit(const buffer &a){
        const char *pattern=";admin=true;";
        buffer x=ctr_go(a,key,nonce);
        return strstr((char*)x.a,(char*)pattern)!=0;
    }
};


struct ex3{
    buffer iv, bkey;

    AES_KEY key, rkey;
    ex3(){
        bkey=buffer::Rand(16);
        AES_set_encrypt_key(bkey.a,16*8,&key);
        AES_set_decrypt_key(bkey.a,16*8,&rkey);
        iv=bkey;
    }
    
    buffer encrypt(const buffer &a){
        REP(i,a.n) if (!isprint(a[i])) throw "wronc enc";
        return aes_cbc_encrypt(a.a,iv,&key);
    }

    buffer decrypt(const buffer &a, bool &err){
        buffer b=aes_cbc_decrypt(a,iv,&rkey);
        err=false;
        REP(i,b.n) if (isprint(b[i])) err=true;
        return b;
    }
};



struct ex5{
    buffer key;
    ex5(){
        key=buffer::Rand(rand()%10+10);
        printf("USING KS %d\n",key.n);
    }

    buffer gethash(const buffer &a){ return sha1_prefix(key,a); }

    bool checkit(const buffer &a, const buffer &hash){
        buffer hash2=gethash(a);
        return hash==hash2;
    }

};

struct ex6{
    buffer key;
    ex6(){
        key=buffer::Rand(rand()%10+10);
        printf("USING KS %d\n",key.n);
    }

    buffer gethash(const buffer &a){ return md4_prefix(key,a); }

    bool checkit(const buffer &a, const buffer &hash){
        buffer hash2=gethash(a);
        return hash==hash2;
    }

};


void go1(){
    ex1 A;
    buffer cipher=A.cipher;
    buffer res=A.edit(cipher,0,cipher);
    assert(res==A.plain);
    printf("res and plain are equal\n");
}

void go2(){
    ex2 A;
    const char *want=";admin=true;";
    int nx=strlen(want);
    buffer tmp(256);
    memset(tmp.a,'a',tmp.n);
    buffer x=A.enc(tmp);
    REP(i,nx) x[128+i]^='a'^want[i];
    assert(A.checkit(x));
}

void go3(){
    ex3 A;
    buffer a(64);
    memset(a.a,'a',a.n);
    buffer b=A.encrypt(a);
    memset(b.a+16,0,16);
    memcpy(b.a+32,b.a,16);

    bool err;
    buffer x=A.decrypt(b,err);
    assert(err);
    buffer key(16);
    REP(i,16) key[i]=x[i]^x[i+32];

    assert(key==A.bkey);
    printf("got key\n");
    key.disphex();
}



void go4(){
    buffer res=sha1("abcd");
    res.disphex();
    res=sha1_prefix("abcd","efg");
    res.disphex();
}

void go5(){
    buffer res=sha1("aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa");
    buffer res2=sha1_raw(sha1_preproc("aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",0,0));
    assert(res==res2);

    ex5 A;

    buffer tmp="comment1=cooking%20MCs;userdata=foo;comment2=%20like%20a%20pound%20of%20bacon";
    buffer p1=A.gethash(tmp);


    int fd=0;
    REP(ks,30){
        buffer pre=sha1_preproc(tmp,ks,0);
        buffer post=";admin=true";

        buffer hash=sha1_raw(sha1_preproc(post,0,pre.n+ks),p1);
        buffer res=pre+post;
        if (A.checkit(res,hash)){
            printf("FOUND IT FOR LENGTH %d\n",ks);
            res.disphex();
            res.disptext();
            fd=1;
            break;
        }

    }
    assert(fd);
}


void go6(){
    const char *str="aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa";
    buffer res=md4(str);
    buffer res2=md4_raw(md4_preproc(str,0,0));
    res.disphex();
    res2.disphex();
    assert(res==res2);

    ex6 A;

    buffer tmp="comment1=cooking%20MCs;userdata=foo;comment2=%20like%20a%20pound%20of%20bacon";
    buffer p1=A.gethash(tmp);


    int fd=0;
    REP(ks,30){
        buffer pre=md4_preproc(tmp,ks,0);
        buffer post=";admin=true";

        buffer hash=md4_raw(md4_preproc(post,0,pre.n+ks),p1);
        buffer res=pre+post;
        if (A.checkit(res,hash)){
            printf("FOUND IT FOR LENGTH %d\n",ks);
            res.disphex();
            res.disptext();
            fd=1;
            break;
        }

    }
    assert(fd);
}


struct ex7{
    buffer key;
    buffer cmd;
    int sz, repeat;
    int keepbest, expand;

    ex7(int repeat, int expand, int keepbest):repeat(repeat),expand(expand),keepbest(keepbest){
        sz=40;
        key="jeez i need to learn python";
    }

    buffer checkit(const buffer &a){
        return hmac(a,key);
    }

    double go(const buffer &sig, int *retcode){
        memcpy(cmd.a+cmd.n-sz,sig.a,sz);
        struct timeval st,nd;
        gettimeofday(&st,0);
        *retcode=system((char*)cmd.a);
        gettimeofday(&nd,0);
        double span=(nd.tv_sec-st.tv_sec)*1e6+nd.tv_usec-st.tv_usec;
        return span;
    }

    double eval(const buffer &sig){
        vector<double> x;
        REP(step,repeat){
            int tmp;
            x.pb(go(sig,&tmp));
            if (!tmp) throw sig;
        }
        sort(ALL(x));
        int n=ceil(repeat*0.9);
        double s=0;
        REP(i,n) s+=x[i];
        sig.disptext();
        printf("%lf\n",s/n);
        return s/n;
    }



    buffer solve(const buffer &file){
        int n=(1<<4*expand)*(keepbest+1);

        buffer pool[n];
        REP(i,n) pool[i]=buffer(sz), memset(pool[i].a,'0',sz);

        cmd=buffer("./query.sh ")+file+buffer(" ")+pool[0];

        vi lst;
        REP(i,n) lst.pb(i);
        int u=lst.back(); lst.pop_back();

        vector<pair<double,int> > tb, ntb;
        tb.pb(MP(0.,u));
        int m=0;
        try{
            while(1){
                printf("HAVE SIZE %d\n",tb.size());
                if (m==sz) break;

                REP(i,tb.size()){
                    int P=1<<4*min(sz-m,expand);
                    REP(j,P){
                        assert(lst.size());
                        int u=lst.back(), x=j; lst.pop_back();

                        memcpy(pool[u].a,pool[tb[i].ND].a,m);
                        REP(k,expand) pool[u][m+k]=gethexchar(x&0xf), x>>=4;
                        ntb.pb(MP(-eval(pool[u]),u));
                    }
                    lst.pb(tb[i].ND);
                }
                cout<<lst.size()<<endl;


                tb.clear();
                sort(ALL(ntb));
                printf("FIXED %d >> PICKING \n",m+expand);
                REP(i,ntb.size()){
                    if (i<keepbest) tb.pb(ntb[i]), pool[ntb[i].ND].disptext();
                    else lst.pb(ntb[i].ND);
                }
                ntb.clear();
                m+=expand;
            }
            printf("could not find solution\n");
            return buffer(40);
        }catch(buffer b){
            return b;
        }
    }
};


void go7(){
    ex7 A(1,1,1);//works fine for 50ms
    buffer file="abc";
    buffer ans=A.checkit(file);
    buffer res=A.solve(file).hextobyte();
    ans.disphex();
    res.disphex();
    assert(ans==res);
}



void go8(){
    ex7 A(30,1,1);//works for 1ms for at least the first 4 char (didnt wait beyond that)
    buffer file="abc";
    buffer ans=A.checkit(file);
    buffer res=A.solve(file).hextobyte();
    ans.disphex();
    res.disphex();
    assert(ans==res);
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
    int x; sscanf(argv[1]," %d",&x);
    int nc=8;

    if (x==-1) REP(i,nc) go(i);
    else{
        assert(x>=1 && x<=nc);
        go(x);
    }

    return 0;
}
