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

#include <openssl/ec.h>
#include <openssl/ecdh.h>
#include <openssl/evp.h>

#include <sys/socket.h>
#include <sys/types.h>
#include <arpa/inet.h>
#include <netdb.h>

using namespace std;
using namespace __gnu_cxx;

#define REP(i, n) for (int i = 0; i < int(n); ++i)
#define REPV(i, n) for (int i = (n) - 1; (int)i >= 0; --i)
#define FOR(i, a, b) for (int i = (int)(a); i < (int)(b); ++i)

#define FE(i, t)                                                               \
    for (__typeof((t).begin()) i = (t).begin(); i != (t).end(); ++i)
#define FEV(i, t)                                                              \
    for (__typeof((t).rbegin()) i = (t).rbegin(); i != (t).rend(); ++i)

#define two(x) (1LL << (x))
#define ALL(a) (a).begin(), (a).end()

#define pb push_back
#define ST first
#define ND second
#define MP(x, y) make_pair(x, y)

typedef long long ll;
typedef unsigned long long ull;
typedef unsigned int uint;
typedef pair<int, int> pii;
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

template <class T> void checkmin(T &a, T b) {
    if (b < a)
        a = b;
}
template <class T> void checkmax(T &a, T b) {
    if (b > a)
        a = b;
}
template <class T> void out(T t[], int n) {
    REP(i, n) cout << t[i] << " ";
    cout << endl;
}
template <class T> void out(vector<T> t, int n = -1) {
    for (int i = 0; i < (n == -1 ? t.size() : n); ++i)
        cout << t[i] << " ";
    cout << endl;
}
inline int count_bit(int n) {
    return (n == 0) ? 0 : 1 + count_bit(n & (n - 1));
}
inline int low_bit(int n) { return (n ^ n - 1) & n; }
inline int ctz(int n) { return (n == 0 ? -1 : ctz(n >> 1) + 1); }
int toInt(string s) {
    int a;
    istringstream(s) >> a;
    return a;
}
string toStr(int a) {
    ostringstream os;
    os << a;
    return os.str();
}

EC_GROUP *group;


void init() {
    int sock = socket(AF_INET, SOCK_STREAM, 0);
    assert(sock != -1);

    struct sockaddr_in peer;
    struct hostent host;

    peer.port = htons(1330);
    peer.family = AF_INET;
    memcpy(&peer.sin_addr, host.h_addr_list[0], host.h_length);

    sock = connect(sock, &peer, sizeof(peer));
    assert(sock != -1);
    assert(dup(sock, stdin) != -1);
    assert(dup(sock, stdout) != -1);
}


EC_POINT* getPoint(){
    const int buflen=1024;
    char buf[buflen];
    int y;
    scanf("(%s : %d)", buf, &y);
    BN_dec2bn(&bn, buf);
    EC_POINT* point=EC_POINT_new(group);
    assert(point!=0);
    assert(EC_POINT_set_compressed_coordinates_GFp(group, point, bn, y, NULL)==1);

    BN_free(bn);
    return point;
}

void solve() {
    scanf("use P26r1");

    group=EC_GROUP_new_by_curve_name(NID_X9_62_prime256v1);
    assert(group!=NULL);

    EC_KEY* key1=EC_KEY_new_by_curve_name(NID_X9_62_prime256v1);
    assert(key1!=0);

    EC_POINT *p1;
    p1=getPoint();

}

int main() {
    solve();
    return 0;
}
