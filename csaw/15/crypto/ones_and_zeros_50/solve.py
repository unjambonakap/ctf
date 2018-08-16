#!/usr/bin/env python

import struct
import binascii
from chdrft.crypto.common import isalpha

def f1():
  x=open('./eps1.1_ones-and-zer0es_c4368e65e1883044f3917485ec928173.mpeg', 'r').read()
  print(x)
  print(len(x))
  s=''
  for i in range(len(x)//8):
    u=x[i*8:i*8+8]
    a=int(u,2)
    s+=chr(a)
  print(s)

def f2():
  x=open('./eps1.7_wh1ter0se_2b007cf0ba9881d954e85eb475d0d5e4.m4v', 'r').read()
  x='DURNJC'
  for i in range(26):
    s=''
    cl=''
    for j in x:
      if isalpha(j):
        cl+=j
        tmp=(ord(j)-ord('A')+i)%26
        tmp+=ord('A')
        s+=chr(tmp)
      else:
        s+=j
    print(s)



