#/usr/bin/env python

import idc
import idautils

for x in open('./funcs.list', 'r').readlines():
  x = x.strip()
  if not x: continue
  a, b= [int(a, 16) for a in x.split(':')]
  addr = a * 16 + b
  idc.MakeFunction(addr)
