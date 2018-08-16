#!/usr/bin/env python
from gmpy2 import mpz, gcd, next_prime, invert, isqrt
import random
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5
from Crypto.Cipher import PKCS1_OAEP
import base64
from Crypto import Random
import sys


n0 = mpz(
    17088099071005160077519535201251561512827343312119898927636879052601867044714726370386690019037410713114320026517402376841417405031151513348071692422844111539444422581984359115079190646208324178506319406900715874915900634363805971709855749306898889145210604580281672508427585998760093545394796048750722655959)
n1 = mpz(
    17088099071005160077519535201251561512827343312119898927636879052601867044714726370386690019037410713114320026517402376841417405031151513348071692422843595984982748293316974068618115911067742584379552735602316711058821390310015568237776017595377114965964917241868369393081542210506249720365990388566061488767)
n2 = mpz(
    17088099071005160077519535201251561512827343312119898927636879052601867044714726370386690019037410713114320026517402376841417405031151513348071692422843432549712853189869867645149366559627418953279461425319827343120906512593400627639486709587239380005123784026423814996927322189025803939737718582864288985553)

nbits=40
p = random.randint(1 << nbits, 1 << nbits+1)
q = random.randint(1 << nbits, 1 << nbits+1)

P=[]
Q=[]
for i in range(0, 3):
    p = next_prime(p)
    q = next_prime(q)
    P.append(p)
    Q.append(q)

#n0=P[0]*Q[2]
#n1=P[1]*Q[1]
#n2=P[2]*Q[0]


d0 = n0 - n2
d1 = n1 - n0


def solve2(p0, q2):
    print('found p0', p0)
    print('found q0', q2)
    ub=1000
    for i in range(1,ub):
        if gcd(n1,p0+i)!=1:
            p1=p0+i
            q1=n1//p1
            break
    else:
        return None
    for i in range(1,ub):
        if gcd(n2,p1+i)!=1:
            p2=p1+i
            q0=n2//p2
            break

    return p0,q2,p1,q1,p2,q0

def solve():
    ub = 1000
    for i0 in range(1, ub):
        for i1 in range(1, ub):
            for i2 in range(1,ub):
                d = d0 * i0 + (d1-i2*i0) * i1
                tmp = gcd(d, n0)
                if tmp != 1:
                    p0=tmp
                    q2=n0//p0

    else:
        assert False


q2=mpz(4165938907260954640804986514555496835723686162893011508104816859692320046868363019435944953520658898678455053432699809898947934756189120526030787871227863)
p0=mpz(4101860217206195486319508931988944464741665503169699281154625914180099350459859416508157842908810493659777848990372055112637980426665995893689191266676993)
#p0, q2, p1, q1, p2, q0 = solve()
assert p0 * q2 == n0

p0, q2, p1, q1, p2, q0 = solve2(p0,q2)
assert p0 * q2 == n0
assert p1 * q1 == n1
assert p2 * q0 == n2
print(p0,q2)
print(p1,q1)
print(p2,q0)
P=[]*3
Q=[]*3
P=[p0,p1,p2]
Q=[q0,q1,q2]


a=p1-p0
b=q1-q0

p=p0
q=q0
diff=a*b*p0*q0
diff-=(a*a*p0*p0+b*b*q0*q0)
print('>>>GOT ')
print(diff)
tmp=p0*q0+(a*p0+b*q0)//2
n2=p0*q0*p1*q1
print(tmp-isqrt(n2))
X=p0*q0*a*b-(p0*b+a*q0)**2//4
V=p*q+(p*b+a*q)//2
print(X//V)
print('laa', isqrt(n2)-isqrt(V-X))
sys.exit(0)

m0='DjXmcsw0QXBRBiUOx2Uu4kS/gFvIYyf6MSJLWlwy8i7WjVB8vOtUb90GTFSuHDX6iawvUg/XVjU7DVAi9EhMGSS2LyvgMH4nD4gjlVlC2PkxkNDILuUq//5DMoTUyootReoke1jXDnmHg1y0KglkIylL2dufsHc74cAKnciNU9U='
m1='DkYN4JwQU+EstIvIs662BISkzXxqqfb62DrJFV5efVuXtkLSQrzHgLczgC1blF8e29x46Jz2yjqb1eb2IJX59yuDBHiQ13ckId+E732Bpu00ee9UqYtSNNnQFIo8LIBWFxIUK3+XjNynDD9ArcF5OkLvk8o8AU1DcAdusQtsURo='
m2='CuMo9lJNex64Wh63DORfMPkcwX7inwNd3QEi/OKb2vbh69v4iF46/4tCz8ZF7FEKfNxmXuyPREdS7YPqNGi9hQT21CmeiXe/AbDCITrhYVMWJi4A6wjZjkdslHklnmJFnULRkSLVCYAgVQAbPGO3CmQ+3y9QSAhZM5qi8NQnoOo='
m=[m0,m1,m2]
N=[]
D=[]
privKey=[]
pubKey=[]
res=''
for i in range(0, 3):
    N.append(P[i] * Q[2 - i])
    D.append(long(invert(long(65537), (P[i] - 1) * (Q[2 - i] - 1))))
    privKey.append(RSA.construct((long(N[i]), long(65537), long(D[i]), long(P[i]), long(Q[2 - i]))))
    pubKey.append(RSA.construct((long(N[i]), long(65537))))
    key = PKCS1_v1_5.new(privKey[i])
    res+=key.decrypt(base64.b64decode(m[i]), '')
print(res)




#hi all the flag is ASIS{a0c8f997d5cdd699d336b0f2f12af326}
