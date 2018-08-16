#include <opa_common.h>

#include <opa/math/common/Utils.h>
#include <opa/utils/string.h>

using namespace std;
using namespace opa;
using namespace opa::math::common;
using namespace opa::utils;

std::vector<bignum> lst;

/* Period parameters -- These are all magic.  Don't change. */
#define N 624
#define M 397
#define MATRIX_A 0x9908b0dfUL   /* constant vector a */
#define UPPER_MASK 0x80000000UL /* most significant w-r bits */
#define LOWER_MASK 0x7fffffffUL /* least significant r bits */

typedef struct {
    unsigned long state[N];
    int index;
    u32 genrand_int32() {
        unsigned long y;
        static unsigned long mag01[2] = { 0x0UL, MATRIX_A };
        /* mag01[x] = x * MATRIX_A  for x=0,1 */
        unsigned long *mt;

        mt = self->state;
        if (self->index >= N) { /* generate N words at one time */
            int kk;

            for (kk = 0; kk < N - M; kk++) {
                y = (mt[kk] & UPPER_MASK) | (mt[kk + 1] & LOWER_MASK);
                mt[kk] = mt[kk + M] ^ (y >> 1) ^ mag01[y & 0x1UL];
            }
            for (; kk < N - 1; kk++) {
                y = (mt[kk] & UPPER_MASK) | (mt[kk + 1] & LOWER_MASK);
                mt[kk] = mt[kk + (M - N)] ^ (y >> 1) ^ mag01[y & 0x1UL];
            }
            y = (mt[N - 1] & UPPER_MASK) | (mt[0] & LOWER_MASK);
            mt[N - 1] = mt[M - 1] ^ (y >> 1) ^ mag01[y & 0x1UL];

            self->index = 0;
        }

        y = mt[self->index++];
        y ^= (y >> 11);
        y ^= (y << 7) & 0x9d2c5680UL;
        y ^= (y << 15) & 0xefc60000UL;
        y ^= (y >> 18);
        return y;
    }

    void init_by_array(unsigned long init_key[], unsigned long key_length) {
        unsigned int i, j,
            k; /* was signed in the original code. RDH 12/16/2002 */
        unsigned long *mt;

        mt = self->state;
        init_genrand(self, 19650218UL);
        i = 1;
        j = 0;
        k = (N > key_length ? N : key_length);
        for (; k; k--) {
            mt[i] = (mt[i] ^ ((mt[i - 1] ^ (mt[i - 1] >> 30)) * 1664525UL)) +
                    init_key[j] + j; /* non linear */
            mt[i] &= 0xffffffffUL;   /* for WORDSIZE > 32 machines */
            i++;
            j++;
            if (i >= N) {
                mt[0] = mt[N - 1];
                i = 1;
            }
            if (j >= key_length)
                j = 0;
        }
        for (k = N - 1; k; k--) {
            mt[i] = (mt[i] ^ ((mt[i - 1] ^ (mt[i - 1] >> 30)) * 1566083941UL)) -
                    i;             /* non linear */
            mt[i] &= 0xffffffffUL; /* for WORDSIZE > 32 machines */
            i++;
            if (i >= N) {
                mt[0] = mt[N - 1];
                i = 1;
            }
        }

        mt[0] = 0x80000000UL; /* MSB is 1; assuring non-zero initial array */
        Py_INCREF(Py_None);
        return Py_None;
    }
    std::string getrandbits(int k) {

        int bytes = ((k - 1) / 32 + 1) * 4;
        u8 *bytearray = (u8 *)malloc(bytes);

        /* Fill-out whole words, byte-by-byte to avoid endianness issues */
        for (int i = 0; i < bytes; i += 4, k -= 32) {
            u32 r = prng();
            if (k < 32)
                r >>= (32 - k);
            printf(">> got %x\n", r);
            bytearray[i + 0] = (unsigned char)r;
            bytearray[i + 1] = (unsigned char)(r >> 8);
            bytearray[i + 2] = (unsigned char)(r >> 16);
            bytearray[i + 3] = (unsigned char)(r >> 24);
        }

        /* little endian order to match bytearray assignment order */
        // result = _PyLong_FromByteArray(bytearray, bytes, 1, 0);
        string res = string((const char *)bytearray, bytes);
        free(bytearray);
        return res;
    }

} RandomObject;

void load() {

    FILE *f = fopen("./crypto1/pubkey_tsf.txt", "r");
    while (1) {
        char buf[128];
        int cnt = fscanf(f, "%s", buf);
        if (cnt != 1)
            break;
        lst.pb(bignum(buf));
    }
}

void test() {
    prng.seed(0);
    string res = getrandbits(10);
    REP(i, res.size()) printf("%x\n", res[i]);
    printf(">> %s\n", b2h(res).c_str());
}

int main() {
    test();
    load();
    for (s64 i = 0; i < 1ll << 32; ++i) {
        break;
    }

    return 0;
}
