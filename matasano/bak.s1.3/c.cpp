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
    buffer iv;
    AES_KEY key, rkey;
    vector<buffer> tb;

    ex1(){
        genivkey(iv,&key,&rkey);
        vector<buffer> tmp=readfilebyline("ex17.in");
        FE(it,tmp) tb.pb(it->fromb64());
    }



    void enc(buffer &cipher, buffer &ivo, int i=-1)const{
        ivo.from(iv);
        if (i==-1) i=rand()%tb.size();
        cipher=aes_cbc_encrypt(tb[i],iv,&key);
    }

    int oracle(buffer &cipher){
        try{
            aes_cbc_decrypt(cipher,iv,&rkey);
        }catch(...){
            return 0;
        }
        return 1;
    }
};


struct ex3{
    buffer key;
    vector<buffer> tb;

    ex3(const char *fname){
        key=buffer::Rand(16);
        vector<buffer> tmp=readfilebyline(fname);
        ll nonce=1ll*rand()*rand();
        FE(it,tmp) tb.pb(ctr_go(it->fromb64(),key,nonce));
    }
};


struct ex8{
    int seed;
    PRNG prng;
    ex8(){ seed=rand()&0xffff; prng.seed(seed);}
    
    buffer encrypt(const buffer &a){
        int np=rand()%100;
        buffer b(a.n+np);
        b.fillrand(0,np);
        memcpy(b.a+np,a.a,a.n);
        return prng.encrypt(b);
    }
};

void go1(){
    int bs=16;
    ex1 A;
    REP(step,10){
        buffer cipher, iv;
        A.enc(cipher,iv,step);
        int n=cipher.n;
        buffer plain(n);

        REP(bi,n/bs){
            buffer x(2*bs);
            memcpy(x.a+bs,cipher.a+bs*bi,bs);

            REPV(i,bs){
                vi cnd;
                REP(v,256) if (x.a[i]=v, A.oracle(x)) cnd.pb(v);
                if (cnd.size()==2){
                    assert(i);
                    x.a[i-1]^=0xff;
                    x.a[i]=cnd[0];
                    if (!A.oracle(x)) swap(cnd[0],cnd[1]);
                    cnd.pop_back();
                }
                assert(cnd.size()==1);
                x.a[i]=cnd[0];
                plain.a[bi*bs+i]=x.a[i]^(bs-i);
                for (int j=i; j<bs; ++j) x.a[j]^=(bs-i)^(bs-i+1);
            }
        }

        char *prev=iv.a;
        REP(bi,n/bs){
            REP(j,bs) plain.a[bi*bs+j]^=prev[j];
            prev=cipher.a+bi*bs;
        }
        plain.rpkcs7();
        printf("RESULT>>>\n");
        plain.disptext();
    }
    /*

       RESULT EXO 1
       RESULT>>>
       000000Now that the party is jumping
       RESULT>>>
       000001With the bass kicked in and the Vega's are pumpin'
       RESULT>>>
       000002Quick to the point, to the point, no faking
       RESULT>>>
       000003Cooking MC's like a pound of bacon
       RESULT>>>
       000004Burning 'em, if you ain't quick and nimble
       RESULT>>>
       000005I go crazy when I hear a cymbal
       RESULT>>>
       000006And a high hat with a souped up tempo
       RESULT>>>
       000007I'm on a roll, it's time to go solo
       RESULT>>>
       000008ollin' in my five point oh
       RESULT>>>
       000009ith my rag-top down so my hair can blow
       */
}

void go2(){
    const uchar *AA="L77na/nrFsKvynd6HzOoG7GHTLXsTVu9qvY/2syLXzhPweyyMTJULu/6/kXX0KSvoOLSFQ==";
    const uchar *key="YELLOW SUBMARINE";

    buffer res=ctr_go(buffer(AA).fromb64(),buffer(key),0);
    res.disptext();


    /*
       RESULT EXO 2
       Yo, VIP Let's kick it Ice, Ice, baby Ice, Ice, baby
       */
}
void go3(){

    ex3 A("ex19.in");
    xorstream B;
    B.tb=A.tb;
    buffer stream=B.go();
    B.dispresult();

    /*
       could not make out the last word 
       STREAM >>>
00ab7f500c344188e66e52b2ec0a535be412baa8fc139950d7a46417346c1e09f04f4b5141200000TEXT RESULT
           0         10        20        30
01234567890123456789012345678901234567
0>>he, too, has been changed in his turKt<<<EOF
1>>i have passed with a nod of the head<<<EOF
2>>he might have won fame in the end,<<<EOF
3>>so daring and sweet his thought.<<<EOF
4>>or have lingered awhile and said<<<EOF
5>>this other his helper and friend<<<EOF
6>>i have met them at close of day<<<EOF
7>>so sensitive his nature seemed,<<<EOF
8>>what voice more sweet than hers<<<EOF
9>>but lived where motley is worn:<<<EOF
10>>from counter or desk among grey<<<EOF
11>>a drunken, vain-glorious lout.<<<EOF
12>>to some who are near my heart,<<<EOF
13>>he, too, has resigned his part<<<EOF
14>>yet I number him in the song;<<<EOF
15>>he had done most bitter wrong<<<EOF
16>>and thought before I had done<<<EOF
17>>all changed, changed utterly:<<<EOF
18>>being certain that they and I<<<EOF
19>>that woman's days were spent<<<EOF
20>>until her voice grew shrill.<<<EOF
21>>or polite meaningless words,<<<EOF
22>>this other man I had dreamed<<<EOF
23>>around the fire at the club,<<<EOF
24>>of a mocking tale or a gibe<<<EOF
25>>a terrible beauty is born.<<<EOF
26>>a terrible beauty is born.<<<EOF
27>>this man had kept a school<<<EOF
28>>and rode our winged horse.<<<EOF
29>>was coming into his force;<<<EOF
30>>eighteenth-century houses.<<<EOF
31>>polite meaningless words,<<<EOF
32>>when young and beautiful,<<<EOF
33>>coming with vivid faces<<<EOF
34>>her nights in argument<<<EOF
35>>in ignorant good will,<<<EOF
36>>to please a companion<<<EOF
37>>she rode to harriers?<<<EOF
38>>in the casual comedy;<<<EOF
39>>transformed utterly:<<<EOF
       */
}
void go4()
{
    ex3 A("ex20.in");
    xorstream B;
    B.tb=A.tb;
    B.go();
    B.dispresult();

    /*

STREAM >>>
20ab7f500c344188e66e52b2ec0a535be412baa8fc139950d7a46417346c1e09f04f4b5164788b47cba597e1d615a450a19b2cc4201d6a8b84a3071dTEXT RESULT
0         10        20        30        40        50        60        70        80        90        100       110
0123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567
0>>And count our money / Yo, well check this out, yo Eli<<<EOF
1>>And we outta here / Yo, what happened to peace? / Peace<<<EOF
2>>Soon the lyrical format is superior / Faces of death remain<<<EOF
3>>Turn down the bass down / And let the beat just keep on rockin'<<<EOF
4>>Yo, I hear what you're saying / So let's just pump the music up<<<EOF
5>>Search for a nine to five, if I strive / Then maybe I'll stay alive<<<EOF
6>>Flashbacks interfere, ya start to hear: / The R-A-K-I-M in your ear;<<<EOF
7>>Make sure the system's loud when I mention / Phrases that's fearsome<<<EOF
8>>Well, check this out, since Norby Walters is our agency, right? / True<<<EOF
9>>Terror in the styles, never error-files / Indeed I'm known-your exiled!<<<EOF
10>>Thinkin' of a master plan / 'Cuz ain't nuthin' but sweat inside my hand<<<EOF
11>>Fish, which is my favorite dish / But without no money it's still a wish<<<EOF
12>>Rakim, check this out, yo / You go to your girl house and I'll go to mine<<<EOF
13>>So now to test to see if I got pull / Hit the studio, 'cuz I'm paid in full<<<EOF
14>>Melodies-unmakable, pattern-unescapable / A horn if want the style I posses<<<EOF
15>>Then the beat is hysterical / That makes Eric go get a ax and chops the wack<<<EOF
16>>Musical madness MC ever made, see it's / Now an emergency, open-heart surgery<<<EOF
17>>'Cause my girl is definitely mad / 'Cause it took us too long to do this album<<<EOF
18>>A pen and a paper, a stereo, a tape of / Me and Eric B, and a nice big plate of<<<EOF
19>>Okay, so who we rollin' with then? We rollin' with Rush / Of Rushtown Management<<<EOF
20>>But now I learned to earn 'cuz I'm righteous / I feel great, so maybe I might just<<<EOF
21>>Lyrics of fury! A fearified freestyle! / The "R" is in the house-too much tension!<<<EOF
22>>Friday the thirteenth, walking down Elm Street / You come in my realm ya get beat!<<<EOF
23>>So I walk up the street whistlin' this / Feelin' out of place 'cuz, man, do I miss<<<EOF
24>>MC's decaying, cuz they never stayed / The scene of a crime every night at the show<<<EOF
25>>Music's the clue, when I come your warned / Apocalypse Now, when I'm done, ya gone!<<<EOF
26>>Death wish, so come on, step to this / Hysterical idea for a lyrical professionist!<<<EOF
27>>Check this out, since we talking over / This def beat right here that I put together<<<EOF
28>>This is off limits, so your visions are blurry / All ya see is the meters at a volume<<<EOF
29>>I'm rated "R"...this is a warning, ya better void / Poets are paranoid, DJ's D-stroyed<<<EOF
30>>Haven't you ever heard of a MC-murderer? / This is the death penalty,and I'm servin' a<<<EOF
31>>I need money, I used to be a stick-up kid / So I think of all the devious things I did<<<EOF
32>>Battle's tempting...whatever suits ya! / For words the sentence, there's no resemblance<<<EOF
33>>Open your mind, you will find every word'll be / Furier than ever, I remain the furture<<<EOF
34>>Cuz your about to see a disastrous sight / A performance never again performed on a mic:<<<EOF
35>>So I start my mission, leave my residence / Thinkin' how could I get some dead presidents<<<EOF
36>>Yo Rakim, what's up? / Yo, I'm doing the knowledge, E., man I'm trying to get paid in full<<<EOF
37>>Then nonchalantly tell you what it mean to me / Strictly business I'm quickly in this mood<<<EOF
38>>Cuz I came back to attack others in spite- / Strike like lightnin', It's quite frightenin'!<<<EOF
39>>You think you're ruffer, then suffer the consequences! / I'm never dying-terrifying results<<<EOF
40>>Kara Lewis is our agent, word up / Zakia and 4th and Broadway is our record company, indeed<<<EOF
41>>Novocain ease the pain it might save him / If not, Eric B.'s the judge, the crowd's the jury<<<EOF
42>>I bless the child, the earth, the gods and bomb the rest / For those that envy a MC it can be<<<EOF
43>>The fiend of a rhyme on the mic that you know / It's only one capable, breaks-the unbreakable<<<EOF
44>>Ya tremble like a alcoholic, muscles tighten up / What's that, lighten up! You see a sight but<<<EOF
45>>So I dig into my pocket, all my money is spent / So I dig deeper but still comin' up with lint<<<EOF
46>>Hazardous to your health so be friendly / A matter of life and death, just like a etch-a-sketch<<<EOF
47>>For those that oppose to be level or next to this / I ain't a devil and this ain't the Exorcist!<<<EOF
48>>'Cuz I don't like to dream about gettin' paid / So I dig into the books of the rhymes that I made<<<EOF
49>>If not, my soul'll release! / The scene is recreated, reincarnated, updated, I'm glad you made it<<<EOF
50>>Suddenly you feel like your in a horror flick / You grab your heart then wish for tomorrow quick!<<<EOF
51>>I wake ya with hundreds of thousands of volts / Mic-to-mouth resuscitation, rhythm with radiation<<<EOF
52>>But don't be afraid in the dark, in a park / Not a scream or a cry, or a bark, more like a spark;<<<EOF
53>>Worse than a nightmare, you don't have to sleep a wink / The pain's a migraine every time ya thin9<<<EOF
54>>And I don't care if the whole crowd's a witness! / I'm a tear you apart but I'm a spare you a hea w<<<EOF
55>>I wanna hear some of them def rhymes, you know what I'm sayin'? / And together, we can get paid i<#y+#G<<<EOF
56>>Shake 'till your clear, make it disappear, make the next / After the ceremony, let the rhyme restrjq~#N#B#<<<EOF
57>>Program into the speed of the rhyme, prepare to start / Rhythm's out of the radius, insane as ther`m?#B#R#<<<EOF
58>>I used to roll up, this is a hold up, ain't nuthin' funny / Stop smiling, be still, don't nuthin'rnp(###T#####2#a###<<<EOF
59>>You want to hear some sounds that not only pounds but please your eardrums; / I sit back and obse uz~#C#######2#m#####<<<EOF
0         10        20        30        40        50        60        70        80        90        100       110
0123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567

*/

}

void go5(){
    PRNG prng;
    boost::mt19937 prng2;
    REP(step,10){

        prng2.seed(step);
        prng.seed(step);
        REP(step2,100){
            uint u=prng.gen();
            uint v=prng2();
            printf("%d %d\n",u,v);
            assert(u==v);
        }
    }
}


void go6(){
    int t=time(0);
    PRNG prng;
    t+=rand()%1000;
    int ot=t;
    prng.seed(ot);
    printf("seeding with %d\n",ot);
    t+=rand()%1000;
    int res=prng.gen();
    

    for (;;--t){
        PRNG x; x.seed(t);
        if (x.gen()==res) break;
    }
    printf("initial seed >> %d\n",t);
    assert(t==ot);
}



void go7(){
    PRNG a,b;
    a.seed(rand());
    REP(i,624){
        uint v=a.gen();
        b.mt[i]=b.reverse(v);
        b.index=0;
    }
    REP(i,100) assert(a.gen()==b.gen());
    printf("success\n");
    //one way function (ie hash) the output. Since it is not reversible, can't retrieve prng inner state
}



void go8(){
    ex8 A;
    buffer a(16);
    memset(a.a,'a',16);
    buffer res=A.encrypt(a);
    int ans=-1;
    REP(i,1<<16){
        PRNG prng; prng.seed(i);
        buffer b=prng.encrypt(res);
        int fd=1;
        REP(j,16) if (b.a[b.n-1-j]!='a'){fd=0; break;}
        if (fd) ans=i;
    }
    printf("orig seed was %d, found %d\n",A.seed,ans);
    assert(ans!=-1);
    assert(A.seed==ans);


    /*
       for the second part, this is exactly the same to verify the token: iterate backward through timestamp, using it as seeds, generate the stream and compare it to your token
       */
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
