
# coding: utf-8

# In[2]:


import struct
content = open('./mat.bin', 'rb').read()
n, m = struct.unpack('<QQ', content[:16])


# In[38]:


pos = 16
dmat = matrix(m, n)
for i in range(n):
  data.append([])
  for j in range(m):
    dmat[j,i] = struct.unpack('<Q', content[pos:pos+8])[0]
    pos += 8


# In[39]:


cipher_data = open('./flag.txt.enc', 'rb').read()[8:]
cipher_data = open('./abc.enc', 'rb').read()[8:]
cipher = []
for i in range(n):
  cipher.append(struct.unpack('<Q', cipher_data[i*8:i*8+8])[0])
cipher = vector(cipher)


# In[40]:


res = cipher * 0
for i in range(m): res += vector(dmat[i,:]) * 97
print((res-cipher) %(2**64) )


# In[69]:


M = matrix(m+n+1, n+m+n+1)

p1 = n
p2 = p1 + m
p3 = p2 + n

MX = 100
EXPECT = 2**40

M[:m,:n] = dmat
for i in range(m):
  M[i,p1+i] = EXPECT // 128

ri = m
for i in range(n):
  M[ri+i, i] = 2**64
  M[ri+i, p2+i] = EXPECT // m // 128
ri += n
  
M[-1, :n] = cipher
M[-1,-1] = EXPECT
print(M[:,-1])


# In[70]:


res = M.LLL()



# In[72]:


for i in res.rows():
  if not i.is_zero():
    for j in range(m):
      print(i[j+n] // M[j,j+n])
    break

