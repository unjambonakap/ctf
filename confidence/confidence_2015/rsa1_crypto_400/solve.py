#!/usr/bin/env python

from chdrft.utils.misc import path_from_script
import chdrft.opa_sage.utils as sage_utils
import subprocess as sp


def get_flag(ia):
    return int(open(path_from_script(__file__, './resources/out/flag%d' %
                                     ia)).read())


def get_key():
    with open(path_from_script(__file__, './resources/out/n1')) as f:
        return int(f.read()), 3


def solve(ia, ib):
    n, e = get_key()

    va = get_flag(ia)
    vb = get_flag(ib)
    print(n, e, va, vb)
    res = sage_utils.call_argparsified(['sage', '-python'],
                                       sage_utils.coppersmith, n, e, va, vb)

    res=int(res)
    print('GOT RESULT >> ',res.to_bytes((res.bit_length()+7)//8, byteorder='big'))
    #b"Drgns{She's_playin'_dumb_all_the_timeJust_to_keep_it_funTo_get_you_on_like_ahh!Be_careful_amigoShe_talkin'_and_walkin}K\xbc\x91\x11"


def go():
    solve(0, 1)


if __name__ == '__main__':
    go()
