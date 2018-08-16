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
    rsa A; A.gen();
    buffer aa="abcd";
    bignum a=bignum::frombytestr(aa);
    bignum b=bignum(2).powm(A.e,A.n);
    bignum res=A.decrypt(A.encrypt(a)*b%A.n)*bignum(2).inv(A.n)%A.n;
    buffer ans=res.getstr2();
    assert(ans==aa);
}


void go2(){
    rsa A;
    A.gen(1024/8);
    buffer msg="hi mom";

    buffer obuf(85);//it fits shortly, alittle bit more tmp>n otherwise next cubic root changes more than first 85 bytes :)
    

    buffer h=sha256(msg);
    buffer tmp=buffer((uchar*)"\xff\x00\x01\xff\x00",5)+buffer((uchar*)&h.n,4)+h;
    printf("want :\n");
    tmp.disphex();
    bignum x=bignum::frombytestr(tmp+obuf);
    bignum xx;
    mpz_root(xx.a,x.a,3);
    mpz_add_ui(x.a,xx.a,1);
    

    buffer fake=A.decryptsig(x);
    assert(fake==sha256(msg));
    printf("signature verified\n");
}

void go3(){
    dsa A;
    buffer msg="foawjef;a";
    assert(A.check(msg,A.sign(msg)));
    printf("success\n");

    bignum k;
    pair<bignum,bignum> pp=A.sign2(msg,k);
    bignum x=A.getx(msg,k,pp.ST,pp.ND);
    assert(x==A.x);
    printf("success retrieving x with k\n");



    buffer str="For those that envy a MC it can be hazardous to your health\nSo be friendly, a matter of life and death, just like a etch-a-sketch\n";//geez
    buffer h1=sha1(str);
    dsa B;
    B.y=buffer("84ad4719d044495496a3201c8ff484feb45b962e7302e56a392aee4abab3e4bdebf2955b4736012f21a08084056b19bcd7fee56048e004e44984e2f411788efdc837a0d2e5abb7b555039fd243ac01f0fb2ed1dec568280ce678e931868d23eb095fde9d3779191b8c0299d6e07bbb283e6633451e535c45513b2d33c99ea17");

    bignum r(buffer("548099063082341131477253921760299949438196259240"),10);
    bignum s(buffer("857042759984254168557880549501802188789837994940"),10);
    REP(i,(1<<16)+1){
        if (i%100==0) printf("on %d\n",i);
        bignum x=B.getx(str,bignum(i),r,s);
        B.x=x;
        pair<bignum,bignum> tmp=B.sign3(str,bignum(i));
        if (r==tmp.ST&&s==tmp.ND){
            printf("key is ,got it on attempt %d \n",i);
            x.disp();
            puts("SHA1:");
            sha1(x.getstr()).disphex();
            break;
        }

    }
    /*

       OUTPUT>>>
       
       on 16000
       on 16100
       on 16200
       on 16300
       on 16400
       on 16500
       key is ,got it on attempt 16575
       15fb2873d16b3e129ff76d0918fd7ada54659e49
SHA1:
0954edd5e0afe5542a4adf012611a91912a3ec16


       */

}

struct data{
    bignum r,s,m;
    buffer msg;
};

void go4(){
    dsa A;
    A.y=buffer("2d026f4bf30195ede3a088da85e398ef869611d0f68f0713d51c9c1a3a26c95105d915e2d8cdf26d056b86b8a7b85519b1c23cc3ecdc6062650462e3063bd179c2a6581519f674a61f1d89a1fff27171ebc1b93d4dc57bceb7ae2430f98a6a4d83d8279ee65d71c1203d2c96d65ebbf7cce9d32971c3de5084cce04a2e147821");

    vector<buffer> sl=readfilebyline((uchar*)"ex44.txt");;
    vector<data> tb(sl.size()/4);


    for (int i=0; i<tb.size(); ++i){
        tb[i].msg=sl[i*4].a+5;
        tb[i].s=bignum(sl[i*4+1].a+3,10);//WHYYYYYYY Would you use base10 for god sake
        tb[i].r=bignum(sl[i*4+2].a+3,10);
        tb[i].m=bignum(sl[i*4+3].a+3);
        puts("");

        cout<<tb[i].msg.a<<"XX"<<endl;
        sha1(tb[i].msg).disphex();
        tb[i].m.disp();
    }


    map<bignum,int> seen;
    int fd=0;
    puts("====");
    puts("====");
    REP(i,tb.size()){
        assert(A.check(tb[i].msg,MP(tb[i].r,tb[i].s)));

        if (seen.count(tb[i].r)){
            int ii=seen[tb[i].r];
            data &d1=tb[i], &d2=tb[ii];
            bignum k=(d1.m-d2.m)*(d1.s-d2.s).inv(A.q)%A.q;
            bignum x=A.getx(d1.msg,k,d1.r,d1.s);
            A.x=x;
            
            puts("");

            pair<bignum,bignum> pp=A.sign3(d1.msg,k);
            pair<bignum,bignum> pp2=A.sign3(d2.msg,k);
            if (pp.ST!=d1.r || pp.ND!=d1.s || pp2.ST!=d2.r || pp2.ND!=d2.s){

                printf("got a collision on r, weird\n");
                printf("could not find k\n");
            }else{
                printf("for %d %d\n",i,ii);
                printf("KEY IS "); x.disp();
                printf("sha1: "); sha1(x.getstr()).disphex();
                fd=1;

            }

        }
        seen[tb[i].r]=i;
    }
    assert(fd);


    /*
       output>>>

       Yeah me shoes a an tear up an' now me toes is a show a XX
       bc7ec371d951977cba10381da08fe934dea80314
       bc7ec371d951977cba10381da08fe934dea80314

       Where me a born in are de one Toronto, so XX
       d6340bfcda59b6b75b59ca634813d572de800e8f
       d6340bfcda59b6b75b59ca634813d572de800e8f
       ====
       ====

       got a collision on r, weird
       could not find k

       for 9 1
       KEY IS f1b733db159c66bce071d21e044a48b0e4c1665a
sha1: ca8f6f7c66fa362d40760d135b763eb8527d3d52

for 10 2
KEY IS f1b733db159c66bce071d21e044a48b0e4c1665a
sha1: ca8f6f7c66fa362d40760d135b763eb8527d3d52


       */


}
void go5(){
    dsa A;
    A.setg(0);
    pair<bg,bg> p=A.sign("test");
    printf("signing 'test' >>>(r,s)=\n");
    p.ST.disp();
    p.ND.disp();


    printf("checking test and test2 for this (r,s)\n");
    cout<<A.check("test",p)<<endl;
    cout<<A.check("test2",p)<<endl;

    //both verifies


    A.setg(A.p+1);
    pair<bg,bg> master;
    bg z=1203813;
    int step=0;
    while(1){
        z=(z+1)%A.q;
        master.ST=A.y.powm(z,A.p)%A.q;
        if (z==0 || master.ST==0) continue;
        master.ND=master.ST*z.inv(A.q)%A.q;
        break;
    }

    printf("master sig:\n");
    master.ST.disp();
    master.ND.disp();

    assert(A.check("test",master));
    assert(A.check("test2",master));
    printf("both test and test2 verifie against that sig\n");
}



void go6(){
    rsa A; A.gen(128);
    bignum cipher=A.encrypt(buffer("VGhhdCdzIHdoeSBJIGZvdW5kIHlvdSBkb24ndCBwbGF5IGFyb3VuZCB3aXRoIHRoZSBGdW5reSBDb2xkIE1lZGluYQ").fromb64().bytetohex());

    bignum a=0, b=1;
    bignum x=A.encrypt(2);
    bignum y=cipher;
    bignum res;

    while(1){
        bg lb,ub;
        lb=(A.n*a+b-1)/b;
        ub=A.n*(a+1)/b;
        if (lb==ub){res=lb; break;}

        lb.getstr2().disptext();
        y=y*x%A.n;
        a=a*2;
        b=b*2;
        if (A.oracle(y)) a=a+1;
    }
    res.getstr2().disptext();
    res.disp();

    assert(A.encrypt(res)==cipher);
    printf("success biatch\n");


    /*
       .....

       That's why I found you don't play around with the Funky Cold Medin`??
       That's why I found you don't play around with the Funky Cold Medin`??
       That's why I found you don't play around with the Funky Cold Medin`??
       That's why I found you don't play around with the Funky Cold Medin`??
       That's why I found you don't play around with the Funky Cold Medin`??
       That's why I found you don't play around with the Funky Cold Medin`??
       That's why I found you don't play around with the Funky Cold Medina??
       That's why I found you don't play around with the Funky Cold Medina??
       That's why I found you don't play around with the Funky Cold Medina??
       54686174277320776879204920666f756e6420796f7520646f6e277420706c61792061726f756e642077697468207468652046756e6b7920436f6c64204d6564696e610000
       success biatch

       */
}


typedef pair<bg,bg> pgg;

struct finalsolver{
    rsa A;
    bignum B,n,s;
    bignum M;
    struct stats_t{
        int r1,r2,s1,s2;
        int u1,u2;
        vi lst;
    } stats;

    finalsolver(int sz){ A.gen(sz); }
    bignum enc(const buffer &msg){return A.encrypt(M=A.pad(msg));}
    vector<pgg> update(const vector<pgg> &tb){
        vector<pgg> res;
        REP(i,tb.size()){
            bignum a=tb[i].ST, b=tb[i].ND;
            bignum r=(a*s-B*3+n)/n, ub=(b*s-B*2)/n;
            for (; r<=ub; r=r+1){
                a=max(a,(B*2+r*n+s-1)/s);
                bignum nb=(B*3-1+r*n)/s;

                if (nb>b) nb=b, r=ub;
                res.pb(MP(a,nb)), ++stats.u2;
            }
        }
        return res;
    }

    buffer solve(const bignum &x){
        n=A.n;
        int k=(mpz_sizeinbase(n.a,2))/8;
        B=bignum(2).powm(8*(k-2),n);
        s=n/(B*3);
        n.disp();
        B.disp();

        A.n.disp();
        int step=0;
        for (;!A.oracle2(x*A.encrypt(s)%n); s=s+1);

        s.disp();
        vector<pgg> tb, tb2;
        tb.pb(MP(B*2,B*3-1));
        tb=update(tb);

        memset(&stats,0,6*4);

        while(1){
            puts("\n\n");
            if (tb.size()>1) stats.lst.pb(tb.size());
            printf("HAVE SIZE >>>> %d\n",tb.size());
            //REP(i,tb.size()) tb[i].ST.disp(),tb[i].ND.disp(), puts("==");

            if (tb.size()==1){
                ++stats.s1;
                bignum a=tb[0].ST, b=tb[0].ND;
                if (a==b) break;
                a.disp();
                b.disp();

                bignum r=((b*s-B*2)*2)/n;
                for (;; r=r+1){
                    bignum lb=(B*2+r*n)/b, ub=(B*3+r*n+a-1)/a;
                    for (; lb<ub; lb=lb+1, ++stats.r1) if (A.oracle2(x*A.encrypt(lb)%n)){ s=lb; goto done; }
                }
done:;
            }else for (++stats.r2, s=s+1; !A.oracle2(x*A.encrypt(s)%n); s=s+1, ++stats.s2);

            tb=update(tb);

        }

        printf("======STATS\n");
        printf("%d %d xx  %d %d xx %d %d\n",stats.r1,stats.r2,stats.s1,stats.s2,stats.u1,stats.u2);
        REP(i,stats.lst.size()) printf("%d ",stats.lst[i]); puts("");
        bignum res=tb[0].ST;
        return A.unpad(A.repad(res));
    }





};

void go7(){

    int sz=32;
    finalsolver xx(sz);
    buffer msg="dadada";

    buffer res=xx.solve(xx.enc(msg));
    assert(res==msg);
    printf("RESULT MOFO>>>\n");
    res.disptext();
}

void go8(){
    int sz=128;
    finalsolver xx(sz);
    buffer msg=buffer::Rand(sz-11);

    buffer res=xx.solve(xx.enc(msg));
    assert(res==msg);
    printf("RESULT MOFO>>>\n");
    res.disptext();

    //took 2 min, ~130k oracle call (mostly on step 2b)

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
    buffer b("44706139643629284570616d64");
    b.hextobyte().disptext();
    return 0;

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
