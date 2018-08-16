#!/usr/bin/env python

import subprocess as sp
import binascii
import glob
from chdrft.utils.misc import chdrft_executor


def get_name(s):
    return binascii.hexlify(s).decode()


def get_file(s):
    return './tmp/res_{}.out'.format(s)


def get_trace(s):
    return './tmp/trace_{}.out'.format(s)


def do_run(s):
    name = get_name(s)
    print('name >> ', name)
    fmt = './build/emulator/test_emu1 ./data/hollywood {name} > {out}'
    cmd = fmt.format(name=name, out=get_file(name))

    sp.check_call(cmd, shell=True)


def check(i):
    a1=get_name(bytes([0]))
    a2=get_name(i)
    out_fil='./tmp/diff_{}.out'.format(a2)
    cmd = 'diff {} {} | sort | uniq | cut -c 142-148 > {}'.format(get_file(a1), get_file(a2), out_fil)
    print(cmd)
    sp.check_call(cmd, shell=True)

sp.check_call('waf -vv --out=build configure build ', shell=True)

if 0:
    for i in range(0x100):
        chdrft_executor.submit(do_run, bytes([i]))
    chdrft_executor.shutdown()
else:
    for i in range(0x100):
        chdrft_executor.submit(check, bytes([i]))
    chdrft_executor.shutdown()
