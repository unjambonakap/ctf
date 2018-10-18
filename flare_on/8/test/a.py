#!/usr/bin/env python

import matplotlib.pyplot as plt
import math
from PIL import Image
import sys
import binascii
from asq.initiators import query
import struct
from chdrft.utils.misc import Attributize, DictWithDefault
import zlib
import numpy as np
import itertools


def extract():
    q = query(open('./orig', 'r').readlines())
    res = q.select(lambda x: x.strip()).select(
        lambda x: binascii.a2b_base64(x)).to_list()
    open('./dest.png', 'wb').write(b''.join(res))


def do_plot(a, **kw):
    y, binEdges = np.histogram(a, bins=range(max(a) + 1))
    plt.plot(binEdges[:-1], y, '.', **kw)


def get_chunk(data, pos):
    length = struct.unpack('>I', data[pos:pos + 4])[0]
    pos += 4
    code = data[pos:pos + 4]
    pos += 4

    start_pos = pos
    d = data[pos:pos + length]
    pos += length
    end_pos = pos

    chk = data[pos:pos + 4]
    pos += 4
    print('got header ', code, length)
    return Attributize(length=length,
                       code=code,
                       start_pos=start_pos,
                       end_pos=end_pos,
                       next_pos=pos,
                       chk=chk)


def analyse():
    data = open('./dest.png', 'rb').read()
    pos = 8
    tb = []
    while pos < len(data):
        print('on ', pos)
        chunk = get_chunk(data, pos)
        tb.append(chunk)
        pos = chunk.next_pos

    d = b''
    for j in range(1, len(tb)):
        c = tb[j]
        tmp = data[c.start_pos:c.end_pos]
        if c.code == b'IDAT':
            d += tmp

    dx = zlib.decompressobj()
    u = dx.decompress(d)
    w = 600
    h = 480

    pitch = w * 3 + 1
    b = []
    for i in range(h):
        b.append(int(u[pitch * i]))
    print(b)

    x = Image.open('./dest.png')
    y = Image.open('./r1.png')
    w, h = x.width, x.height
    z = Image.new('RGB', (w, h))

    lsta = [[] for i in range(3)]
    lstb = [[] for i in range(3)]
    all = []
    for i in range(w):
        for j in range(h):
            pos = (i, j)
            a = x.getpixel(pos)
            b = y.getpixel(pos)
            res = [0] * 3
            for k in range(3):
                lsta[k].append(a[k])
                lstb[k].append(b[k])
                all.append(a[k])
                res[k] = int(math.fabs(a[k] - b[k]))

            lim = 150
            if res[0] > lim and res[1] > lim and res[2] > lim:
                res = [255, 0, 0]
            else:
                res = a
            z.putpixel(pos, tuple(res))
    #z.save('./diff2.png')
    lsta = np.array(lsta)
    lstb = np.array(lstb)
    sa = np.sum(lsta, axis=0)
    sb = np.sum(lstb, axis=0)


    modlog = 1
    group = 8 // modlog
    mod = 2 ** modlog
    for AA in itertools.chain([sa, all], lsta):
        tb = []
        for i in range(len(AA) // group):
            x = AA[i * group:i * group + group]
            assert len(x) == group
            x = [a % mod for a in x]
            v = 0
            for k in range(group):
                v += x[k] * mod ** k
            tb.append(v)


        do_plot(tb)
    plt.show()

    return

    do_plot(sa, label='A')
    do_plot(sb, label='B')
    plt.legend()
    plt.show()
    #return
    for k in range(3):
        do_plot(lsta[k], label='A')
        do_plot(lstb[k], label='B')
        plt.legend()
        plt.show()


analyse()
