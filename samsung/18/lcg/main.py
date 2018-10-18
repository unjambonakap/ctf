#!/usr/bin/env python

from chdrft.cmds import CmdsList
from chdrft.main import app
from chdrft.utils.cmdify import ActionHandler
from chdrft.utils.misc import Attributize
import chdrft.utils.misc as cmisc
import glog
from chdrft.utils.cmdify import call_sage
from chdrft.opa_sage.utils import lll, make_sparse
from chdrft.tube.process import Process
from chdrft.tube.connection import Connection
import gmpy2

global flags, cache
flags = None
cache = None


def args(parser):
  clist = CmdsList().add(test)
  ActionHandler.Prepare(parser, clist.lst)

def gcd_list(lst):
  res = 0
  for i in lst:
    res = gmpy2.gcd(res, i)
  return res

def test(ctx):
  print('on test')
  px = Process(['/usr/bin/python3', './lcg.py'])
  #px = Connection('lcg.eatpwnnosleep.com', 12345)
  with px as conn:
    lst = []

    nx = 10
    for i in range(nx):
      conn.send('123\n')
      res = int(conn.recv_until('\n').strip())
      lst.append(res)
    print(lst)
    return


    mguess = 0


    tb = []
    for i in range(nx-3):
      s0 = lst[i]
      s1 = lst[i+1]
      s2 = lst[i+2]
      r = lst[i+3]

      d = r-s2
      tb.append((s0, s1, s2, d))

    hist = []
    for i in range(3):
      hist.append(tb)
      ntb = []
      for j in range(len(tb)):
        for k in range(j):
          u = []

          x = tb[j][0]
          y = tb[k][0]
          for ii in range(1, len(tb[j])):
            u.append(tb[j][ii] * y - tb[k][ii] * x)
          ntb.append(u)
      tb = ntb
    mguess = gcd_list([x for x, in tb])

    x0, y0, z0, m0 = 6181369669767163407,5407744839835496434,8744744311366254845,10714829862921516198

    if 1:
      coeffs = []
      for e in reversed(hist):
        lx = []
        for x in e:
          d = x[-1]
          for i in range(1, len(x)-1):
            d -= x[i] * coeffs[i-1]
          d %= mguess
          print()
          print(x)
          print('aaaa', (d-x[0] * x0)%mguess)

          g, u, v = gmpy2.gcdext(x[0] % mguess, mguess)
          #if g!=1:continue
          print(d,g, d%g, mguess, x0)
          print((x0*d-g)%mguess)
          print((y0*d-g)%mguess)
          print(((x0-y0)*d-g)%mguess)
          assert d% g == 0
          lx.append(d // g * u% mguess)
          print((d-lx[-1] * x[0]) % mguess)
          print(gcd_list(lx), (x0 % lx[-1]) % mguess, lx[-1])
        assert len(lx) > 0
        coeffs.insert(0, gcd_list(lx))
    return


    m, tsf = make_sparse()
    TGT = 2**128
    M = 2**64

    nv = nx-2
    for i in range(nv):
      m[0][i] = lst[i+2]*M
      m[1][i] = -lst[i+1]*M
      m[2][i] = -lst[i+0]*M
      m[3][i] = -M
      m[4+i][i] = mguess*M
      m[4+i][4+nv+i] = 1
    m[0][nv] = M
    m[1][nv+1] = 1
    m[2][nv+2] = 1
    m[3][nv+3] = 1
    m = tsf(m)
    res = call_sage(lll, m)
    for i in res:
      if i[nv] != 0:
        u = i[nv] // M
        x = i[nv+1] // u
        y = i[nv+2] // u
        z = i[nv+3] // u

    s0, s1 = lst[-2:]
    for i in range(nx, 32):
      ns = (s0 * y + s1 * x + z) % mguess
      s0, s1 = s1, ns
      conn.send(f'{s1}\n')

    conn.interactive()

    #SCTF{LCG_is_too_simple_to_be_a_good_CSPRNG}






def main():
  ctx = Attributize()
  ActionHandler.Run(ctx)


app()
