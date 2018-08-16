
# coding: utf-8

# In[52]:


import json
basemat = json.load(open('./mat.data', 'r'))


# In[53]:


n=256
nx = len(basemat)

import itertools
import random

perm = list(range(nx))

while True:
  random.shuffle(perm)
  vecs = list([basemat[i] for i in perm])
  
  m = matrix(vecs[nx-n:])
  
  vals = []
  for i in range(nx-n+1):
    m[0,:] = vector(vecs[i])
    vals.append(m.determinant())
  d = gcd(vals)
  print(d)
  if d == 1: break

print(perm)


# In[54]:


curd = 0
curvec = vector(m[0,:] * 0)

data = dict()
data['base'] = perm[:nx-n+1]
data['mat_id'] = perm[nx-n+1:]
data['make_unimodular'] = []

for i, dx in enumerate(vals):
  nd, u, v = xgcd(curd, dx)
  curvec = curvec * u + vector(vecs[i]) * v
  curd = nd
  data['make_unimodular'].append((int(u), int(v)))


# In[55]:


nmat = copy(m)
nmat[0,:] = curvec
print(nmat.determinant())
imat = nmat.inverse()


# In[56]:


data['imat'] = list([list(map(int, x)) for x in imat.rows()])


# In[57]:


import json
json.dump(data, open('./tsf.data', 'w'))

