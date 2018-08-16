#!/usr/bin/env python


from chdrft.tube.connection import Connection
from chdrft.tube.process import Process
from chdrft.utils.misc import PatternMatcher
from chdrft.utils.binary import X86Machine
import time
import re
import struct
import binascii
import hashlib
import subprocess as sp
import os
import sys
from opa.crypto import Sha256, Sha1


class Server:

    def __init__(self, conn, oracle):
        self.conn = conn
        self.oracle = oracle

    def do_send(self, msg):
        self.conn.send(msg)
        self.conn.send('\n')

    def play(self, bet):
        self.conn.recv_until(PatternMatcher.frombytes(b'Play Video Poker'))
        self.do_send('3')

        self.conn.recv_until(PatternMatcher.frombytes(b'Bet:\n'))

        self.do_send(str(bet))

        res = self.conn.recv_until(
            PatternMatcher.frombytes(b'Please supply your')).decode()
        m = re.search('Our Secret_hash is ([0-9a-f]+)\n', res)
        assert m

        host_hash = binascii.a2b_hex(m.group(1))

        guessed_len = 0xe6  # prob 0.36?
        secret_len = 0xf4

        secret = b'a'*0x100

        deck = get_default_deck()
        self.conn.send(deck)

        res = self.conn.recv_until(
            PatternMatcher.frombytes(b'Supply your secret')).decode()

        self.conn.send(secret)

        #print('deck >> ', deck)

        res = self.conn.recv_until(
            PatternMatcher.fromre(b'Which cards would')).decode()
        hand = re.search('Your starting hand is (\w+)\n', res).group(1)

        #print('hand is >> ', hand)
        return_hand = self.get_return_cards(hand)
        #print('return cards >> ', return_hand)
        send_hand = ''.join([str(x) for x in return_hand])
        #print('sending >> ', send_hand)
        self.do_send(send_hand)

        res = self.conn.recv_until(
            PatternMatcher.fromre(b'The seed for our shuffle is [0-9a-f]+\n')).decode()
        sol_hash = re.search('shuffle is ([0-9a-f]+)\n', res).group(1)
        final_hand = re.search('Your ending hand is (\w+)\n', res).group(1)

        correct_seed = struct.unpack('<I', binascii.a2b_hex(sol_hash)[:4])[0]

        # print(binascii.b2a_hex(final_hash).decode())

    def get_return_cards(self, hand):
        cards = hand2cards(hand)

        self.oracle.send(' '.join([str(x) for x in cards]))
        self.oracle.send('\n')

        res = self.oracle.recv_until(PatternMatcher.frombytes(b'END\n'))
        res = res.decode()[:-4].rstrip()
        if len(res) == 0:
            return []
        return [int(x) for x in res.split(' ')]

    def get_balance(self):
        self.do_send('2')

        match = b'Your currnet balance is (\w+) gitsCoins'
        res = self.conn.recv_until(PatternMatcher.fromre(match))
        m = int(re.search(match, res).group(1))
        if m>999999:
            print(res)
            sys.exit(0)
        return m

    def solve(self):
        step = 0
        start = 1000
        now = start
        while True:
            step += 1
            if step == 1000:
                break
            self.play(now//20)
            now = self.get_balance()

            avg = (now-start)/step
            print('Current balance >> {}, step={}, avg={}', now, step, avg)


def hand2cards(x):
    x = x.replace('0', '')
    return [get_card_num(x[2*i:2*i+2]) for i in range(len(x)//2)]


def get_card_num(x):
    o1 = 'shdc'
    o2 = 'A234567891JQK'
    return o1.index(x[1])*13+o2.index(x[0])


def get_hash_builder(base_hash, base_len):
    #base_len in bytes
    x = Sha256()
    pad = (56-(base_len+1)) % 64
    suffix = [0x80]
    suffix += [0]*pad
    suffix = bytes(suffix)
    suffix += struct.pack('>Q', base_len*8)
    x.set_context(base_hash, base_len+len(suffix))

    suffix = b''
    return x, suffix


def get_default_deck():
    s = ''
    for i in range(10):
        s += chr(ord('0')+i)
    for i in range(26):
        s += chr(ord('a')+i)
    for i in range(0x10):
        s += chr(ord('A')+i)
    return s


def test_suf():

    x = Sha256()
    s1 = b'a'*0x100
    x.update(s1)

    val = x.get()
    y, suf = get_hash_builder(val, len(s1))

    tmp = b'b'*0x100
    y.update(tmp)
    print(y.get_context())
    v1 = y.get()

    print(binascii.b2a_hex(suf))
    x = Sha256()
    x.update(s1)
    x.update(suf)
    x.update(tmp)
    print(x.get_context())
    v2 = x.get()

    print(binascii.b2a_hex(v1))
    print(binascii.b2a_hex(v2))


def run():
    with Connection('localhost', 17171) as conn:
        with Process('./build/gitzino/distribute/gitzino_solve query', shell=True) as oracle:
            x = Server(conn, oracle)
            x.solve()


def xor(a, b):
    return [i ^ j for i, j in zip(a, b)]


def get_num(x):
    v = 0
    for i in x:
        v = 52*v+i
    return v


def test1():
    for i in range(100):
        x = Sha256()
        s = os.urandom(0xe6)

        x.update(s)
        h1 = x.get()

        x = Sha256()
        s += b'\x00'*(0x100-len(s))
        x.update(s)
        h2 = x.get_context()[0]
        print(binascii.b2a_hex(h1))
        print(binascii.b2a_hex(h2))
        print(binascii.b2a_hex(bytes(xor(h1, h2))))
        print()


def main():
    if 0:
        test1()
        return
    if 0:
        test_suf()
        return

    if 0:
        print(get_num([8, 9, 10, 11, 12]))
        return

    sp.check_call('waf -vv --out=build configure build', shell=True)

    with open('/tmp/test', 'wb') as f:
        tmp = os.urandom(4)
        tmp += b'a'*0x100
        tmp += b'\x00'*0x1
        tmp += b'Z'*0xe5
        tmp += b'\x80'
        tmp += b'5'*26
        f.write(tmp)

    #x = X86Machine(False)
    #res=x.get_disassembly('push 0x08049e58;ret')
    # print(binascii.hexlify(res))
    # return
    if 0:
        run()
    else:
        with Process('./gitzino/gitzino_nofork_nopriv', want_stdout=None) as unused:
            time.sleep(0.1)
            run()

main()
