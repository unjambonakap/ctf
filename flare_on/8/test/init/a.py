#!/usr/bin/env python


import sys
import binascii
from asq.initiators import query
import struct
from chdrft.utils.misc import Attributize

def extract():
    q=query(open('./orig', 'r').readlines())
    res=q.select(lambda x: x.strip()).select(lambda x: binascii.a2b_base64(x)).to_list()
    open('./dest.png', 'wb').write(b''.join(res))



def get_chunk(data, pos):
    length=struct.unpack('>I', data[pos:pos+4])[0]
    pos+=4
    code=data[pos:pos+4]
    pos+=4

    d=data[pos:pos+length]
    pos+=length
    pos+=4
    print('got header ', code, length)
    return Attributize(length=length, code=code, next_pos=pos)


def analyse():
    data=open('./dest.png', 'rb').read()
    pos=8
    while pos<len(data):
        print('on ', pos)
        chunk=get_chunk(data, pos)
        pos=chunk.next_pos





analyse()
