#!/usr/bin/python


import hashlib
import socket
import re
import sys
import base64
import itertools
import binascii
import array
import os
import time
import subprocess as sp

DEBUG=True

def rot3(x):
    return ((x<<3)|(x>>5))&0xff


def gBox(a,b,mode):
    return rot3((a+b+mode)%256)
def fBox(plain):
    t0 = (plain[2] ^ plain[3])
    y1 = gBox(plain[0] ^ plain[1], t0, 1)
    y0 = gBox(plain[0], y1, 0)
    y2 = gBox(t0, y1, 0)
    y3 = gBox(plain[3], y2, 1)

    return [y3, y2, y1, y0]

def encrypt(plain,subkeys):
    pleft = plain[0:4]
    pright = plain[4:]
    def list_xor(l1,l2):
        return map(lambda x: x[0]^x[1], zip(l1,l2))
    left = list_xor(pleft, subkeys[4])
    right = list_xor(pright, subkeys[5])

    R2L = list_xor(left, right)
    R2R = list_xor(left, fBox(list_xor(R2L, subkeys[0])))

    R3L = R2R;
    R3R = list_xor(R2L, fBox(list_xor(R2R, subkeys[1])))

    R4L = R3R;
    R4R = list_xor(R3L, fBox(list_xor(R3R, subkeys[2])))

    cipherLeft = list_xor(R4L, fBox(list_xor(R4R, subkeys[3])))
    cipherRight = list_xor(cipherLeft, R4R)
    if DEBUG:
        print "PL",pleft
        print "PR",pright
        print "L", left
        print "R", right
        print "R2R",R2R
        print "R2L",R2L
        print "R3R",R3R
        print "R3L",R3L
        print "R4R",R4R
        print "R4L",R4L
        print "CL",cipherLeft
        print "CR",cipherRight
    return cipherLeft+cipherRight

def decrypt(plain,subkeys):
    cipherLeft = plain[0:4]
    cipherRight = plain[4:]

    def list_xor(l1,l2):
        return map(lambda x: x[0]^x[1], zip(l1,l2))
    R4R = list_xor(cipherLeft,cipherRight)
    R4L = list_xor(cipherLeft, fBox(list_xor(R4R, subkeys[3])))


    R3R = R4L
    R3L = list_xor(R4R , fBox(list_xor(R3R, subkeys[2])))

    R2R = R3L
    R2L = list_xor(R3R, fBox(list_xor(R2R, subkeys[1])))

    left = list_xor(R2R, fBox(list_xor(R2L, subkeys[0])))
    right = list_xor(left, R2L)

    pleft = list_xor(left, subkeys[4])
    pright = list_xor(right, subkeys[5])
    if DEBUG:
        print "PL",pleft
        print "PR",pright
        print "L", left
        print "R", right
        print "R2R",R2R
        print "R2L",R2L
        print "R3R",R3R
        print "R3L",R3L
        print "R4R",R4R
        print "R4L",R4L
        print "CL",cipherLeft
        print "CR",cipherRight
    return pleft+pright

def genKeys():
    subkeys=[]
    for x in xrange(6):
        subkeys.append(array.array("B",os.urandom(4)))
    return subkeys



def getArray(letter, num):
    return array.array("B", [ord(letter)]*num)




def solve1(s):

    b=bytearray()
    dst=21
    for i in range(dst):
        b.append('a')

    sx=[]
    cs=range(256)

    for i in itertools.product(cs,cs,[0,1,2]):
        tmp=bytearray(b)
        tmp[17]=i[0]
        tmp[18]=i[1]
        tmp[19]=i[2]
        sx.append(tmp)

    print "STARTING"
    x=s.recv(1024)
    m=re.search('starting with (\S*)', x)
    if m is None:
        print "BAD RECV:", x
        sys.exit(1)

    prefix=m.group(1)
    fd=None
    cnt=0
    for i in sx:
        cnt+=1
        tmp=i
        tmp[0:16]=prefix
        res=hashlib.sha1(tmp).digest()

        if ord(res[-1])==0xff and ord(res[-2])==0xff:
            fd=tmp
            break



    s.send(fd)

def solve2(s):
    time.sleep(1)
    x=s.recv(1024)
    m=re.search('Please decrypt: (\S*)', x)
    if m is None:
        print "BAD RECV:", x
        sys.exit(1)
    cipher=m.group(1)



    c1=cipher[0:16]
    c2=cipher[16:]
    c1=binascii.hexlify(binascii.unhexlify(c1)[::-1])
    c2=binascii.hexlify(binascii.unhexlify(c2)[::-1])
    data=c1+' '+c2+'\n'
    num=100
    data+='%d\n'%num
    for i in range(num):
        x=os.urandom(8)
        s.send(x)
        x=binascii.hexlify(x)
        y=s.recv(1024)
        y=y.rstrip()

        y=binascii.hexlify(binascii.unhexlify(y)[::-1])
        x=binascii.hexlify(binascii.unhexlify(x)[::-1])
        data+='%s %s\n'%(x,y)
    f=open('/tmp/test.in', 'w')
    f.write(data)
    f.close()

    print "starting script"
    px=sp.Popen(['./a.out'], shell=True, stdin=sp.PIPE, stdout=sp.PIPE)
    res=px.communicate(data)[0]
    print "waiting"
    r=px.wait()


    if r==0:
        x=re.search('RESULT >> (\S+) (\S+)', res)
        p1=x.group(1)
        p2=x.group(2)
        p1=binascii.unhexlify(p1)
        p2=binascii.unhexlify(p2)
        print 'Answer: <%s%s>'%(p1,p2)
    else:
        print 'FAIL'






"03773da4a222f42d98a053db618fda2b"


PORT=8888
HOST='localhost'
#HOST='54.85.93.193'

s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST,PORT))

solve1(s)
solve2(s)






