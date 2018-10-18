#!/usr/bin/sage
from sage.all_cmdline import *
import json
n=256

from mat import mat_after as M
from mat import mat_test as M
from mat import mat_before as M
b = [1] *len(M)

conds = []
if 1:
  tgt = b'flag{'
  for i in range(len(tgt)):
    for j in range(8):
      conds.append(((31-i)*8+j, ord(tgt[i]) >> j & 1))
else:
  for i in range(32): conds.append((i*8+7, 0))
  pass

for condp, condv in conds:
  vx = [0]*n
  vx[condp] = 1
  M.append(vx)
  b.append(condv)

m = Matrix(GF(2), M)
v = vector(GF(2), b)
k1 = m.transpose().kernel()

ans = m.solve_right(v)


anslist = []
nk = len(k1)
print(nk)
for i in range(2**nk):
  vx = vector(GF(2), [0]*n)
  for j in range(nk):
    if i >> j & 1:
      vx = vx + k1[j]
  anslist.append([int(x) for x in ans+vx])







open('./ans.out', 'w').write(json.dumps(anslist))

