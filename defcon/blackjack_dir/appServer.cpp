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
#include <signal.h>
#include <ucontext.h>

#include <sys/epoll.h>

#include <pthread.h>
#include <fcntl.h>
#include <sys/socket.h>
#include <sys/un.h>

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
typedef signed char s8;
typedef unsigned char u8;
typedef signed short s16;
typedef unsigned short u16;
typedef signed int s32;
typedef unsigned int u32;
typedef signed long long s64;
typedef unsigned long long u64;

template<class T> void checkmin(T &a, T b){if (b<a)a=b;}
template<class T> void checkmax(T &a, T b){if (b>a)a=b;}
template<class T> void out(T t[], int n){REP(i, n)cout<<t[i]<<" "; cout<<endl;}
template<class T> void out(vector<T> t, int n=-1){for (int i=0; i<(n==-1?t.size():n); ++i) cout<<t[i]<<" "; cout<<endl;}
inline int count_bit(int n){return (n==0)?0:1+count_bit(n&(n-1));}
inline int low_bit(int n){return (n^n-1)&n;}
inline int ctz(int n){return (n==0?-1:ctz(n>>1)+1);}
int toInt(string s){int a; istringstream(s)>>a; return a;}
string toStr(int a){ostringstream os; os<<a; return os.str();}

#include "random_export.h"
#include <Python.h>

const int maxSteps=1111;
const int bufsize=1111;
const int maxNumStates=1111;
const int oo=1e9;

const char *sockPath="blackjack_sock";


struct state{
    int buf[bufsize];
    int cash;
    int totalBets;
    u8 winnings[maxSteps];
} states[maxNumStates];

state tmpState;

set<int> *freeStates;
int totState=0;

int *h_cash=(int*)0x804c0f8;
int *h_totalBets=(int*)0x804c108;
int *h_winnings=(int*)0x804c120;

pthread_mutex_t mutex=PTHREAD_MUTEX_INITIALIZER;
pthread_cond_t cond=PTHREAD_COND_INITIALIZER;

volatile bool hasCommand;
volatile bool quitThread;
volatile bool doneCommand;
int localSock;


struct commandData{
    bool tip;
    int bet;
    int numHit;
    int win;
    int maxHit;
    int askTip;
    int stand;
} volatile cmd;

int curMoney;

#define LOCK(x) pthread_mutex_lock(&(x))
#define UNLOCK(x) pthread_mutex_unlock(&(x))

extern int doRound_entry(int fd) asm("doRound_entry");
extern int rand_getSize() asm("rand_getSize");
extern void rand_backup(void*) asm("rand_backup");
extern void rand_restore(void*) asm("rand_restore");

enum Response{
    RES_BET,
    RES_WON,
    RES_LOST,
    RES_DRAW,
    RES_TIP,
    RES_HS,
    RES_MONEY,
    RES_ELSE,
    RES_END,
    RES_NONE
};


inline bool isPrefix(const char *a, const char *b){
    return !strncmp(a,b,strlen(b));
}

Response getNext(){
    char c;

    char tmpBuf[222];
    int pos=0;
    struct epoll_event ev;

    int epollfd=epoll_create(1);
    ev.events=EPOLLIN;
    ev.data.fd=localSock;
    assert(epoll_ctl(epollfd, EPOLL_CTL_ADD, localSock, &ev)==0);
    Response res=RES_NONE;
    bool ok=true;

    while(1){
        int res=epoll_wait(epollfd, &ev, 1, 2);
        assert(res!=-1);
        if (res==0){
            ok=false;
            break;
        }
        int x=read(localSock, &c, 1);
        assert(x==1);
        tmpBuf[pos++]=c;
        if (c=='\n') break;
    }
    tmpBuf[pos]=0;

    if (pos>0) tmpBuf[pos-1]=0;
    //printf(">> RECV >> %s\n", tmpBuf);

    close(epollfd);


    if (isPrefix(tmpBuf, "How much would you like"))
        return RES_BET;

    if (isPrefix(tmpBuf, "You have")){
        sscanf(tmpBuf, "You have $%d", &curMoney);
        return RES_MONEY;
    }
    if (isPrefix(tmpBuf, "Hit or Stand"))
        return RES_HS;
    if (isPrefix(tmpBuf, "You lose"))
        return RES_LOST;
    if (isPrefix(tmpBuf, "It's a draw"))
        return RES_DRAW;
    if (isPrefix(tmpBuf, "You win"))
        return RES_WON;
    if (isPrefix(tmpBuf, "Would you like to tip"))
        return RES_TIP;
    if (isPrefix(tmpBuf, "Better luck"))
        return RES_END;
    if (!ok)
        return RES_NONE;

    return RES_ELSE;
}

Response getNextWait(){
}

void doSend(string s){
    s+="\n";
    write(localSock, s.c_str(), s.length());
}

void *commandThread(void *data){

    while(!quitThread){
        LOCK(mutex);
        while(!hasCommand && !quitThread) pthread_cond_wait(&cond, &mutex);
        hasCommand=false;
        UNLOCK(mutex);
        if (quitThread) break;

        localSock=socket(AF_UNIX, SOCK_STREAM, 0);
        assert(localSock!=-1);
        struct sockaddr_un peer;
        peer.sun_family=AF_UNIX;
        strcpy(peer.sun_path, sockPath);
        assert(connect(localSock, (struct sockaddr*)&peer, sizeof(peer.sun_family)+strlen(peer.sun_path))!=-1);




        cmd.askTip=0;
        cmd.stand=0;
        if (cmd.numHit==-1) cmd.numHit=oo;

        assert(getNext()==RES_MONEY);
        assert(getNext()==RES_BET);
        doSend(toStr(cmd.bet));
        assert(cmd.bet!=0);

        Response r;
        int wh=0;
        while(1){
            r=getNext();
            assert(r!=RES_NONE);

            if (r==RES_WON){ cmd.win=1; break; }
            if (r==RES_LOST){ cmd.win=-1; break; }
            if (r==RES_DRAW){ cmd.win=0; break; }
            if (r==RES_HS){
                if (wh<cmd.numHit){
                    doSend("H");
                    ++wh;
                }else{
                    cmd.stand=1;
                    doSend("S");
                }
                cmd.maxHit=wh;
            }
        }

        while(1){
            r=getNext();
            if (r==RES_NONE) 
                break;
            if (r==RES_TIP){
                doSend(cmd.tip?"y":"n");
                cmd.askTip=1;
            }
        }

        LOCK(mutex);
        doneCommand=true;
        pthread_cond_signal(&cond);
        close(localSock);
        UNLOCK(mutex);
    }

    return NULL;
}


static PyObject* py_doRound(PyObject *self, PyObject *args)
{
    int ok;
    int fd;
    const char *str;


    if (!PyArg_ParseTuple(args, "iii", &cmd.bet, &cmd.numHit, &cmd.tip))
        return Py_None;



    int s1, s2;
    struct sockaddr_un local;

    local.sun_family=AF_UNIX;
    strcpy(local.sun_path, sockPath);
    s1=socket(AF_UNIX, SOCK_STREAM, 0);
    assert(s1!=-1);
    unlink(local.sun_path);
    assert(bind(s1, (struct sockaddr*)&local, sizeof(local.sun_family)+strlen(local.sun_path))!=-1);
    assert(listen(s1, 1)!=-1);



    LOCK(mutex);
    doneCommand=false;
    hasCommand=true;
    pthread_cond_signal(&cond);
    UNLOCK(mutex);

    struct sockaddr_un remote;
    socklen_t len=sizeof(remote);;
    int remoteSock=accept(s1, (struct sockaddr*)&remote, &len);
    assert(remoteSock!=-1);
    close(s1);

    int res=doRound_entry(remoteSock);

    LOCK(mutex);
    while(!doneCommand) pthread_cond_wait(&cond, &mutex);
    UNLOCK(mutex);
    close(remoteSock);

    //printf("do roudn %d %d %d >> %d %d\n", cmd.bet, cmd.numHit, cmd.tip, cmd.win, cmd.maxHit);
    //printf(">> %d\n", *h_cash);

    return Py_BuildValue("iiii", cmd.win, cmd.maxHit, cmd.askTip, cmd.stand);
}


void backupState(state *s){
    rand_backup(s->buf);
    s->cash=*h_cash;;
    s->totalBets=*h_totalBets;
    memcpy(s->winnings, h_winnings, s->totalBets);
}

void restoreState(state *s){
    rand_restore(s->buf);
    *h_cash=s->cash;
    *h_totalBets=s->totalBets;
    memcpy(h_winnings, s->winnings, s->totalBets);
}

static PyObject* py_initState(PyObject *self, PyObject *args)
{
    const char *s;
    if (!PyArg_ParseTuple(args, "s", &s)) return Py_None;

    int val;
    memcpy(&val, s, 4);

    srand(val);
    return Py_None;
}


static PyObject* py_getState(PyObject *self, PyObject *args)
{
    if (!PyArg_ParseTuple(args, "")) return Py_None;
    backupState(&tmpState);

    return Py_BuildValue("iis#", tmpState.cash, tmpState.totalBets, tmpState.winnings, tmpState.totalBets);
}

static PyObject* py_backupState(PyObject *self, PyObject *args)
{
    assert(freeStates->size()>0);

    int avail=*freeStates->begin();
    freeStates->erase(avail);
    backupState(states+avail);

    return Py_BuildValue("i", avail);
}

static PyObject* py_restoreState(PyObject *self, PyObject *args)
{
    int ok;
    int stateNum;

    if (!PyArg_ParseTuple(args, "i", &stateNum))
        return Py_None;
    restoreState(states+stateNum);
    return Py_None;
}

static PyObject* py_releaseState(PyObject *self, PyObject *args)
{
    int ok;
    int stateNum;

    if (!PyArg_ParseTuple(args, "i", &stateNum))
        return Py_None;
    freeStates->insert(stateNum);
    return Py_None;
}


static PyMethodDef xxMethods[] = {
    {"initState", py_initState, METH_VARARGS, ""},
    {"backupState", py_backupState, METH_VARARGS, ""},
    {"restoreState", py_restoreState, METH_VARARGS, ""},
    {"getState", py_getState, METH_VARARGS, ""},
    {"releaseState", py_releaseState, METH_VARARGS, ""},
    {"doRound", py_doRound, METH_VARARGS, ""},
    {NULL, NULL, 0, NULL}
};

__attribute__((constructor)) void before(void) {
    assert(bufsize>=rand_getSize());
    freeStates=new set<int>();

    Py_Initialize();
    REP(i,maxNumStates)
        freeStates->insert(i);


    pthread_t th;
    hasCommand=false;
    quitThread=false;
    assert(pthread_create(&th, NULL, commandThread, 0)==0);

    Py_InitModule("xx", xxMethods);
    FILE *f=fopen("./sol.py", "r");
    PyRun_SimpleFile(f, "sol.py");

    LOCK(mutex);
    quitThread=true;
    pthread_cond_signal(&cond);
    UNLOCK(mutex);
    pthread_join(th, NULL);
    fclose(f);
    Py_Finalize();
    delete freeStates;
    exit(0);
}




