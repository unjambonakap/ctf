#!/usr/bin/env python


import binascii
import base64
from chdrft.tube.connection import Connection
from Crypto.Cipher import AES
from functools import reduce
import time

FIL = './commands/stat_signed.txt'


def rehash(command):
    key = open('./secret', 'r').read()
    aes = AES.new(key, AES.MODE_ECB)
    pad = "\x00" * (16 - (len(command) % 16))
    command += pad

    blocks = [command[x:x+16] for x in range(0, len(command), 16)]
    cts = [aes.encrypt(block) for block in blocks]

    command = command[:-len(pad)]

    print(cts)
    t = cts[0]
    for i in range(1, len(cts)):
        t = [x ^ y for x, y in zip(t, cts[i])]

    t = binascii.b2a_hex(bytes(t))
    return t


def test_sign(command):
    tmp = rehash(command)
    s = binascii.b2a_base64(command.encode())
    return tmp+b':'+s


def resign(fil, dest):
    tag, cmd = open(fil, 'r').read().rstrip().split(':')
    open(dest, 'wb').write(test_sign(binascii.a2b_base64(cmd).decode()))


def test1():
    cmd = "print 'bonjour'; kappa jmabon\n"
    data = test_sign(cmd)

    with Connection('localhost', 4324) as conn:
        conn.send(data)


def go():
    fil = FIL
    tag, cmd = open(fil, 'r').read().rstrip().split(':')
    cmd = binascii.a2b_base64(cmd)
    blocks = [cmd[x:x+16] for x in range(0, len(cmd), 16)]
    print(blocks)

    prefix = 'self.request.send(open("./secret", "r").read()+"\\n<<EOF")\n'
    prefix += '\n'*(16-len(prefix) % 16)
    prefix = prefix.encode()

    forged_cmd = prefix+prefix+cmd
    data = tag.encode()+b':'+binascii.b2a_base64(forged_cmd)

    with Connection('localhost', 4324) as conn:
        conn.send(data)
        time.sleep(1)
        print(conn.recv_until(lambda x: x.find(b"<<EOF")))


resign('./commands/stat.txt', FIL)
go()
