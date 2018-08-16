#!/usr/bin/env python

from chdrft.tube.connection import Connection
from chdrft.tube.process import Process
from chdrft.crypto.hash import HashType, length_extension, hash_factory
from chdrft.utils.misc import path_from_script, PatternMatcher
import subprocess as sp
import binascii
import time
import struct
import hashlib

server_exe = 'python2 '+path_from_script(__file__, './knockers.py')

authorized_port = 80
server_port = 8008
token = ''
want_port = 7175
secret_len = 16


def get_cmd(*args):
    return ' '.join([server_exe]+list(args))


def knock(token):
    token = binascii.b2a_hex(token).decode()
    sp.check_call(get_cmd('knock', 'localhost', token), shell=True)

def test():
    key=b'jambon'
    extra=b'KAPPA'
    x=hash_factory(HashType.SHA512)
    x.update(key)
    mac=x.get()


    suf, forged_mac=length_extension(HashType.SHA512, mac, len(key), extra)
    print(binascii.b2a_hex(forged_mac))

    x.reset()
    x.update(key+suf)
    print(binascii.b2a_hex(x.get()))






def main():
    if 0:
        test()
        return

    sp.check_call(get_cmd('setup', '80'), shell=True)
    global token
    token = sp.check_output(
        get_cmd('newtoken', str(authorized_port)),
        shell=True)

    print(token)
    token = binascii.a2b_hex(token.rstrip())

    with Process(get_cmd('serve'), shell=True) as x:
        time.sleep(0.5)

        mac = token[0:64]
        msg = token[64:]

        extra = struct.pack('!H', want_port)
        print(len(token))
        suffix, valid_token = length_extension(
            HashType.SHA512, mac, secret_len+len(msg), extra)
        print(valid_token, msg, suffix)
        knock(valid_token+msg+suffix)

        pattern = PatternMatcher.fromre(b'(allowing host [^\n]*\n|bad message)')
        while True:
            res = x.recv_until(pattern, timeout=1)
            if not res:
                break
            print(res)


main()
