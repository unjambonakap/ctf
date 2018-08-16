#!/usr/bin/env python

from chdrft.main import app
from chdrft.utils.cmdify import call_sage
from chdrft.utils.misc import Attributize
from chdrft.opa_sage.utils import lll
import json
import numpy as np

global flags, cache
flags = None
cache = None

def args(parser):
  pass

def rot(a, v):
  return mul(a[v:], -1)+a[:v]

def mul(a, c):
  return list([x*c for x in a])

def main():
  data=Attributize(json.load(open('/tmp/params', 'r')))
  n=len(data.a)
  print(n)
  q=data.q
  target=q
  mx=5
  sc=target//mx
  a=mul(data.a, sc)
  r=mul(data.pub, sc)

  m=[]
  n1=n
  n2=n+1
  nn=n1+n2

  v0=r
  v0x=[0]*n2
  v0x[n]=target
  m.append(v0+v0x)

  for i in range(n):
    cur_v=rot(a, n-i)
    t1=[0]*n2
    t1[i]=target//mx
    m.append(cur_v+t1)

    tmod=[0]*nn
    tmod[i]=target*sc
    m.append(tmod)
  res = call_sage(lll, m)

  res=np.array(res[0])/sc
  res=res[n1:-1]
  tmp=np.array(data.enc)-op(res,np.array(data.pk))
  tmp%=q
  tb=[]
  for i in range(n):
    d1=min(tmp[i],q-tmp[i])
    if d1<10:
      tb.append(0)
    else:
      tb.append(1)

  print(tb)
  print(data.secret)


  #tmp=np.array(data.pub)
  #if 1:
  #  for i in range(n):
  #    tmp-=np.array(rot(data.a, n-i))*data.sk[i]
  #else:
  #  tmp-=op(np.array(data.a), np.array(data.sk))

  #tmp%=q
  #print(tmp)

def op(a, b):
  c = np.fft.ifft(np.fft.fft(a, a.size * 2) * np.fft.fft(b, b.size * 2)).real
  return (c[0:a.size] - c[a.size:]).astype(np.int)
app()
