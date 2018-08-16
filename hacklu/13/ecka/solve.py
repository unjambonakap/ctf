#!/usr/bin/env python3

import Crypto.Cipher.AES as AES
import base64
import socket
import re
import binascii


def toBin(num, nBytes):
    res=b''
    for i in range(nBytes):
        res+=bytes([num&0xff])
        num=num>>8
    return res

def readLine(s):
    res=b''
    while True:
        c=s.recv(1)
        res+=c
        if c==b'\n':
            return res


s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(('ctf.fluxfingers.net', 1330))

x=readLine(s)
x=readLine(s)
s.send(x)
P=readLine(s)
key=readLine(s)
s.send(P)
cipher=readLine(s)
cipher=cipher.rstrip()


cipher=base64.b64decode(cipher)
cipher=cipher[0:16]

key=re.search('\(([0-9]+) :', key.decode('ascii')).group(1)
tmp=("%064x" % int(key))
print(binascii.unhexlify(tmp))
print(key)
key=int(key)
key=toBin(key, 32)
key=key[::-1]

print(key)
aes=AES.new(key, mode=AES.MODE_ECB)

print(aes.decrypt(cipher))
