#!/usr/bin/env python

a=0x10000
v=0
b=1
for i in range(0x20):

    nv=(b>>4)*v+a
    v=nv%2**32
    a*=2
    a%=2**32
    b+=1
    print(hex(v), hex(a), i)
