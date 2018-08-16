#!/usr/bin/env python

import gmpy2
import binascii
import re
import scapy.all as sc
import sys
import pprint

n1=1696206139052948924304948333474767
p1=38456719616722997
q1=44106885765559411

n2=3104649130901425335933838103517383
p2=49662237675630289
q2=62515288803124247
e1=0x10001
e2=e1
d1=gmpy2.invert(e1, (p1-1)*(q1-1))
d2=gmpy2.invert(e2, (p2-1)*(q2-1))
print(d2*e2%((p2-1)*(q2-1)))
print(d1*e1%((p1-1)*(q1-1)))


assert p1*q1==n1
assert p2*q2==n2
x='55305652494430674d544d3749455242564545675053417765444e694d4452694d6a5a684d47466b595752684d6d59324e7a4d794e6d4a694d474d315a445a4d4f794254535563675053417765444a6c4e5746694d6a526d4f57526a4d6a466b5a6a51774e6d45344e32526c4d47497a596a524d4f773d3d0a'

global res
res=[]
global h2
global it
h2={}
it=0


def do_one(x):
  a=binascii.a2b_base64(x.strip())
  print(a)
  m=re.search(b'SEQ = (.*); DATA = 0x(.+)L; SIG = 0x(.*)L;', a)
  assert m

  data=int(m.group(2),16)
  sig=int(m.group(3),16)
  seq=int(m.group(1))

  assert data<n2
  assert sig<n2

  plain=int(gmpy2.powmod(data,d2,n2))
  assert data==gmpy2.powmod(plain, e2, n2)
  sig2=gmpy2.powmod(data, e1, n1)
  sig3=gmpy2.powmod(sig, d1, n1)
  sig4=gmpy2.powmod(plain, e1, n1)
  assert sig!=sig4
  assert sig2!=sig
  assert sig3!=sig2
  assert sig3!=sig4

  print(plain, sig2, sig3, sig4)

  global res, h2, it
  it+=1
  res.append((seq,it,plain))
  if not sig in h2:
    h2[sig]=[]
  h2[sig].append([plain, seq, it])


reader=sc.rdpcap('./dump.pcap')
for a in reader:
  tmp=bytes(a.payload)[14:]
  b=sc.IP(tmp)[sc.TCP]
  if b.flags!=0x08:
    continue
  print()
  do_one(bytes(b.payload))

h={}
for a,*_ in res:
  h[a]=[]
for a,b,c in res:
  h[a].append(c)
print(h)
print(''.join([chr(a[-1]) for _,a in h.items()]))
res.sort()
print('LAA')
print(''.join([chr(a[2]) for a in res]))
pprint.pprint(h2)


