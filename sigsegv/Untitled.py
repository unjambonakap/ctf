
# coding: utf-8

# In[13]:


import binascii
txt = 'ȃǹǷȃǵǷȆȋǜǑǣǤǕǗǑǓǕǣǤǠǑǣǣǙǖǑǓǙǜǕȍ'
tb = txt.encode('utf-8')
if 0:
  tb = txt.encode('utf-16')[2:]
  t1 = []
  t0 = []
  print(len(tb))
  print(tb)
  for i in range(0, len(tb), 4):
    t0.append(tb[i]+tb[i+1]<<8)
    t1.append(tb[i+2]+tb[i+3]<<8)
  print(tb)
  #tb= b'\u0203\u01f9\u01f7\u0203\u01f5\u01f7\u0206\u020b\u01dc\u01d1\u01e3\u01e4\u01d5\u01d7\u01d1\u01d3\u01d5\u01e3\u01e4\u01e0\u01d1\u01e3\u01e3\u01d9\u01d6\u01d1\u01d3\u01d9\u01dc\u01d5\u020d'
  
x='C883C7B9C7B7C883C7B5C7B7C886C88BC79CC791C7A3C7A4C795C797C791C793C795C7A3C7A4C7A0C791C7A3C7A3C799C796C791C793C799C79CC795C88D'
check = binascii.unhexlify(x)
print(check == tb)
print(tb)


# In[14]:


tb0=tb[0::2]
tb=tb[1::2]
print(tb)


# In[15]:


want = b'sigsegv{'
for j in range(len(want)):
  print(want[j]^tb[j], tb0[j])


# In[35]:


res = []
for i in range(len(tb)):
  x = tb[i]
  x ^= 208 + (tb0[i]-199) * 32
  print(hex(tb0[i]), hex(tb[i]), txt[i], chr(x))
  res.append(x)
      
    
print(bytes(res).decode())


# In[8]:


for i in range(256):
  res = []
  for j in range(len(tb)):
    res.append(i ^ tb[j])
  print(bytes(res))
  


# In[ ]:


import chdrft.utils.misc as cmisc
import chdrft.crypto.common as ccrypto
content = b'\x4f\x01\x13\x1e\x09\x59\x34\x09\x0b\x05\x26\x53\x31\x41\x5a\x18\x0e\x53\x1d\x15\x1c\x10\x11\x13\x5b\x06\x16\x69\x15\x29\x55\x1d\x55\x5d\x06\x1d\x0e\x1f\x0c\x14\x13\x5b\x06\x16\x69\x1e\x2a\x40\x5a\x1d\x18\x53\x19\x06\x00\x16\x02\x56\x0a\x1f\x16\x69\x07\x30\x14\x1b\x0a\x5d\x07\x1b\x08\x06\x13\x02\x56\x0b\x05\x06\x3b\x53\x33\x55\x16\x10\x19\x16\x1b\x47\x1f\x00\x47\x15\x13\x0b\x1f\x25\x16\x2b\x53\x1f\x45\x52\x1b\x1d\x0a\x1f\x5b'
print(content)


# In[29]:


solver = ccrypto.VigenereSolver(encdata)
for i in range(2, 30):
  print(i, np.mean(solver.get_n_guess_score(i)))


tlen = 17
key = []
for grpid in range(tlen):
  grp = solver.get_group(grpid, tlen)
  res = solver.solve_single_pad(grp)
  print('\n\n\n', grpid)

  tmp = cmisc.asq_query(res).where(lambda x: x[0].nbad == 0).to_list()
  cnds = []
  for sc, i in tmp:
    cnd = bytes(ccrypto.xor(grp, i))
    ix = ccrypto.get_incidence_freq(cnd)
    cnds.append((ix[ord('8')], i))
  key.append(max(cnds)[1])
print(bytes(key))
print(bytes(ccrypto.xorpad(encdata, key)).decode())

