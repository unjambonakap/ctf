
# coding: utf-8

# In[77]:


import hashlib

target =  bytearray(b'E\x8b\x9f\xa25\x86zo\xae\n+\xc5\xb5\x14ebd(\xe6\xd2\xfam\xe98i\xa3\x8aVzG\x87u')
cur = bytearray(b'8\xad\xc5\xfek\x13\x9b\xda\xa8\x04hS\x9b\xe7\xd8\x86o*\x1e\x90\xceo\xb7?r\xd3\x8cR\x07\xf9\xf4]')




# In[78]:


cnds = []
for i in range(300):
  fname='fake%03d'%i
  tmp = hashlib.sha256(fname.encode('ASCII') + '\x00')
  print(fname, tmp.hexdigest())
  cnds.append((fname, bytearray(tmp.digest())))


# In[79]:


def to_vec(x):
  n = len(x)*8
  res  =vector(GF(2), n)
  for i in range(n):
    res[i] = x[i//8]>>(i&7)&1
  return res
    
m = matrix(GF(2), 256, len(cnds))
for i, v in enumerate(cnds):
  m[:,i] = to_vec(v[1])

b = to_vec(target) + to_vec(cur)
x = m.solve_right(b)


print(len(x))


# In[80]:


import os
dest = './tmp/signed_data/'
for i in range(len(cnds)):
  if x[i]: 
    with open(dest+cnds[i][0], 'wb') as f:
      pass

