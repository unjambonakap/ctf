#!/usr/bin/env python

from chdrft.utils.misc import path_from_script
import chdrft.opa_sage.utils as sage_utils
import subprocess as sp
import gmpy2
import random
from chdrft.math.utils import div_mod, solve_quadratic_eq
import os
from chdrft.crypto.common import Mt19937
import sys
import math

base_dir = sys.argv[1]

#base_dir=path_from_script(__file__,'./')


def get_flag(ia):
    return int(open(os.path.join(base_dir, './out/flag%d' % ia)).read())


def get_key(key):
    with open(os.path.join(base_dir, './out/n%d' % key)) as f:
        return int(f.read()), 3


def check_prime(n):
    return gmpy2.is_prime(n)


def get_prime(n):
    while (not check_prime(n)) or (((n - 1) % 3) == 0):
        n += random.getrandbits(512)
    return n


def solve():
    n, e = get_key(1)

    nflags = 1024
    tb = []
    bad = -1
    for i in range(nflags):
        c = get_flag(i)
        m = gmpy2.iroot(c, e)[0]

        if m ** e % n == c:
            tb.append((m, c))
        else:
            bad = i

    tb = [x[0] for x in tb]
    print(nflags, bad)
    assert len(tb) == nflags - 1

    mt = Mt19937()

    cnd = []
    mt.reset(tb[:mt.N], True)
    random.setstate(mt.getstate())
    for i in range(mt.N, len(tb)):
        assert tb[i] == random.getrandbits(32)

    p0 = 0
    SHIFT = 320
    M = 2 ** SHIFT
    n, e = get_key(2)

    target_p = 3188187676260795965393885912632098092092277177926841147691470208151965030089842950300974043990137117739500760273623793766322015607677005000098664637168316257
    target_q = 1875108872692582482723835846987634639216683975594610214652027228798320162263319042334868729073502157497613319189296249826764958581795978574624701452494517079
    tmp = target_p >> SHIFT
    print(math.log(tmp) / math.log(2))
    target_p &= M - 1
    nmod = n % M

    print('bad at ', bad)
    cnt = 0
    found = False
    lst=[]
    while not found:
        cnt += 1
        p0 = p0 + random.getrandbits(512) & M - 1
        if target_p == p0:
            found = True
            print('OK GOT IT', cnt)

        i2m = int(gmpy2.invert(M, n))
        coeffs = [i2m * p0 % n, 1]
        xlim = 2 ** (540 - SHIFT)



        if cnt==151:
            p1=477803646718302850184754674941187089219848795391372938813636
            print(p0,p1)
            p=p0+p1*M
            assert n%p==0 and p!=1 and p!=n
            q=n//p
            d=gmpy2.invert(e, n-p-q+1)

            c=get_flag(bad)
            m=int(pow(c, d, n))

            plain=m.to_bytes((m.bit_length()+7)//8, byteorder='big')
            print('GOT RESULT >> ',plain)

#GOT RESULT >>  b'DrgnS{ThisFlagMustBeEnteredVerbally|W_Szczebrzeszynie_chrzaszcz_brzmi_w_trzcinie_I_Szczebrzeszyn_z_tego_slynie}'
            break



        lst.append([n, str(coeffs), xlim, 0.4])

        if cnt==1000:
            break
        #res = sage_utils.call_argparsified([
        #    'sage', '-python'
        #], sage_utils.coppersmith_small_root_entry, n, str(coeffs), xlim, 0.4)
        #print(res)
        #print(p0)
        #print(nmod)
        #q0 = div_mod(nmod, p0, M)
        #if q0 == None:
        #    continue
        #print(target_q & M - 1)
        #print(q0)
        #print(p0 * target_q % M)
        #print(nmod)
        #print('')

        #A = n >> (SHIFT * 2)
        #B = n >> SHIFT & M - 1
        #va = q0*M
        #vb = A*M*M+p0*q0-n
        #vc = p0*A
        #sols=solve_quadratic_eq(va,vb,vc)
        #print(sols)
        #continue

        #coeffs = [int(x) for x in [vc, vb, va]]
        #print(nmod)
        #print(str(coeffs))
    else:
        print('FAILURE')

    fx=open('/tmp/data.in', 'w')
    fx.write(str(lst))


def go():
    solve()


if __name__ == '__main__':
    go()
