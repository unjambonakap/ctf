#!/usr/bin/env python

from chdrft.cmds import CmdsList
from chdrft.main import app
from chdrft.utils.cmdify import ActionHandler
from chdrft.utils.misc import Attributize
import chdrft.utils.misc as cmisc
import glog
import json

global flags, cache
flags = None
cache = None


def args(parser):
  clist = CmdsList().add(test).add(decode)
  ActionHandler.Prepare(parser, clist.lst)


def test(ctx):
  print('on test')

  data = 0x131018c85020813093200c6ae4822e400261853722f054a1e080560034008605080380810640342825506829c0209a041340101b54f1848425aa208035d40510068044597575a02b115a9002436958884d110a2515022240aec060e0a0200c4296081062829a00328250210001533404b206301482800234000501d0104
  bits = []
  for i in range(1001):
    bits.append(data>>i&1)
  print(bits)

  expr = '''x0*x64*x96*x128*x192*x255
x0*x64*x96*x128*x192
x0*x64*x96*x128
x0*x64*x96*x192
x0*x64*x128*x192*x255
x0*x64*x192*x255
x0*x64*x192
x0*x64*x255
x0*x96*x128*x192
x0*x96*x128*x255
x0*x96*x128
x0*x96*x192
x0*x128*x192*x255
x0*x128*x192
x0*x128*x255
x0*x128
x0*x192
x0*x255
x0
x64*x96*x128*x192*x255
x64*x96*x128*x192
x64*x96*x192
x64*x96*x255
x64*x128
x64*x192*x255
x64*x192
x64*x255
x64
x96*x128*x192*x255
x96*x128*x255
x96*x128
x96*x192*x255
x96*x192
x96*x255
x96
x128*x192*x255'''

  tb = []

  for e in expr.splitlines():
    lst = []
    for xv in e.split('*'):
      lst.append(int(xv[1:]))
    tb.append(lst)
  tb.sort()
  print('nterms >> ', len(tb))
  print()

  
  vals = []
  for pos, i in enumerate(tb):
    a = 0
    for p, j in enumerate((0, 64, 96, 128, 192, 255)):
      a += int(j in i) << p
    vals.append(a)
    print(a)

  mp = (0, 64, 96, 128, 192, 255)
  rmp = {k:i for i,k in enumerate(mp)}

  func = []
  for i in range(64):
    v =0
    for term in tb:
      u = 1
      for e in term:
        u &= i >> rmp[e] & 1
      v ^= u

    func.append(v)
  print(func)
  print(len(tb))



def decode(ctx):
  anslist = json.load(open('./ans.out', 'r'))
  for res in anslist:
    v = 0
    for i in range(256): v |= res[i]<<i
    print(v.to_bytes(32, 'little')[::-1])
    #flag{StR34m_C1Ph3R_Annih1lat3D!}


def main():
  ctx = Attributize()
  ActionHandler.Run(ctx)


app()
