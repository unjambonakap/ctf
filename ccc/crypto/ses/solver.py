
# coding: utf-8

# In[8]:


n = 128
nb = 16


# In[263]:


k_word_id = n
k_rcon_id = k_word_id + 4 * 8
k_const_id = k_rcon_id+8
nextp = 4*8+8+1


# In[337]:


sbox = (
    'c61963bc974832ed64bbc11e35ea904f99463ce3c8176db23be49e416ab5cf10'
    '78a7dd0229f68c53da057fa08b542ef127f8825d76a9d30c855a20ffd40b71ae'
    'a17e04dbf02f558a03dca679528df728fe215b84af700ad55c83f9260dd2a877'
    '1fc0ba654e91eb34bd6218c7ec334996409fe53a11ceb46be23d4798b36c16c9'
    '08d7ad725986fc23aa750fd0fb245e815788f22d06d9a37cf52a508fa47b01de'
    'b66913cce738429d14cbb16e459ae03fe9364c93b8671dc24b94ee311ac5bf60'
    '6fb0ca153ee19b44cd1268b79c4339e630ef954a61bec41b924d37e8c31c66b9'
    'd10e74ab805f25fa73acd60922fd87588e512bf4df007aa52cf389567da2d807'
).decode('hex')
sbox = bytearray(sbox)


def sbox_tsf(s):
  res = s * 0
  for i in range(8):
    for j in range(8):
      if (sbox[1 << i]^^sbox[0]) >> j & 1:
        res[j, :] += s[i, :]
    res[i, -1] += sbox[0] >> i & 1
  return res


# In[338]:



def mul(a, b):
  p = 0
  while b:
    if b & 1:
      p ^^= a
    a <<= 1
    if a & 0x100:
      a ^^= 0x1b
    b >>= 1
  return p & 0xff


def mul_mat(x):
  res = matrix(GF(2), 8, 8)
  for i in range(8):
    y = mul(1<<i, x)
    for j in range(8):
      res[j,i] = y>>j&1
  return res


# In[387]:


def sub_round(dx):
  m, k = dx
  nm = m * 0
  for blk in range(n // 8):
    nm[blk*8:blk*8+8,:] = sbox_tsf(m[blk*8:blk*8+8,:])
  return nm, k


def shift_round(dx):
  m, k = dx
  nm = copy(m)
  for i in range(1, 4):
    for j in range(4):
      blk = i + 4 * j
      oblk = (i + (4 * j + 4 * i)) % 16
      for kk in range(8):
        nm[blk * 8 + kk, :] = m[oblk * 8 + kk, :]
  return nm, k

def mix_round(dx):
  m, k = dx
  nm = m * 0
  
  m2 = mul_mat(2)
  m3 = mul_mat(3)
  
  for col in range(0, 16, 4):
    for kk in range(4):
      bx = [(3,2), (0,3), (1,0), (2,1)]
      ba = (0,1,2,3)
      bb = (1,2,3,0)
      for i in range(8):
        nm[(col+kk)*8+i,:] +=  m[(col+bx[kk][0])*8+i,:] + m[(col+bx[kk][1])*8+i,:] 
        for j in range(8):
          if m2[i,j]: nm[(col+kk)*8+i,:] += m[(col+ba[kk])*8+j,:]
          if m3[i,j]: nm[(col+kk)*8+i,:] += m[(col+bb[kk])*8+j,:]
          
  return nm, k


# In[437]:


def add_round(dx):
  m, k = dx
  nm = m
  print(m, nm, k)
  for i in range(n):
    nm[i, n:] += k[i, :]
  return nm, k


def expand_round(dx):
  m, k = dx
  nk = k * 0
  nk[-1,-1] = 1
  word = matrix(GF(2), 4 * 8, n + nextp)
  wid = (1, 2, 3, 0)
  for i in range(4):
    for j in range(8):
      pos = wid[i] * 8 + j
      word[i * 8 + j, :] = k[k_word_id + pos, :]
  for i in range(4):
    word[i * 8:i * 8 + 8, :] = sbox_tsf(word[i * 8:i * 8 + 8, :])
  for j in range(8):
    word[0 * 8 + j, :] += k[k_rcon_id + j, :]
  nk[k_rcon_id:k_rcon_id + 8, k_rcon_id:k_rcon_id +
     8] = mul_mat(2) * k[k_rcon_id:k_rcon_id + 8, k_rcon_id:k_rcon_id + 8]

  for i in range(4):
    for j in range(4):
      for kk in range(8):
        word[j * 8 + kk, :] += k[(i * 4 + j) * 8 + kk, :]
        nk[(i * 4 + j) * 8 + kk, :] = word[j * 8 + kk, :]
  for i in range(4):
    for j in range(8):
      nk[k_word_id + i * 8 + j, :] = word[i * 8 + j, :]
  return m, nk


# In[508]:


def add_and_expand(dx):
  return expand_round(add_round(dx))

nextp = 4*8+8+1
def block_build():
  f_n = 4*8+8+1+2*n
  m0 = matrix(GF(2), n, 2*n+nextp)
  for i in range(n): m0[i,i] = 1
  k0 = matrix.identity(GF(2), n + nextp)
    
  
  dx=  m0, k0
  
  if 0:
    dx=  add_and_expand(dx)
    dx=  sub_round(dx)
    dx=  shift_round(dx)
    dx=  mix_round(dx)
    dx=  add_and_expand(dx)
    
    dx=  add_and_expand(dx)
    dx=  sub_round(dx)
    dx=  shift_round(dx)
    dx=  mix_round(dx)
    dx=  add_and_expand(dx)
    
    dx=  sub_round(dx)
    dx=  shift_round(dx)
    dx=  mix_round(dx)
    dx=  add_and_expand(dx)
    return dx
  
  dx=  add_and_expand(dx)
  dx=  sub_round(dx)
  dx=  shift_round(dx)
  dx=  mix_round(dx)
  
  m0, k0 = dx
  
  M = matrix(GF(2), f_n)
  M[:n,:] = m0
  M[n:,n:] = k0
  
  dx=  add_and_expand(dx)
  dx=  sub_round(dx)
  dx=  shift_round(dx)
  dx=  mix_round(dx)
  
  nr = 31337
  M = M ** (nr-1)
  m1 = M[:n,:]
  k1= M[n:,n:]
  dx1 = m1, k1
  
 # for i in range(n):
 #   if k1[i] != dx[1][i]:
 #     print(k1[i])
 #     print(dx[1][i])
 #     print(k1[i] - dx[1][i])
 #   assert k1[i] == dx[1][i], i
 #   if m1[i] != dx[0][i]:
 #     print(m1[i])
 #     print(dx[0][i])
 #     print(m1[i] - dx[0][i])
 #   assert m1[i] == dx[0][i], i

  dx = dx1
  dx=  add_and_expand(dx)
  dx=  sub_round(dx)
  dx=  shift_round(dx)
  dx=  add_and_expand(dx)
  return dx

def get_vecs():
  m,k = block_build()
  evalm  = matrix(GF(2), 2*n+nextp, 2*n+1)
  for i in range(n):
    evalm[i,i] = 1
    evalm[i+n,i+n] = 1
  for wid in range(4*8):
    kid = wid + n + 12 * 8
    evalm[2*n+wid, kid] = 1
    
  recon0 = 0x8d
  for j in range(8):
    evalm[2*n+4*8+j,-1] = recon0 >> j & 1
  evalm[-1,-1] = 1
  return m * evalm, m
  


# In[756]:


res, res0 = get_vecs()


# In[792]:


cipher = bytearray(open('./flag.enc', 'rb').read())
#cipher = bytearray(open('./flag2.enc', 'rb').read())
rels = []
print(res.dimensions())
nblocks = len(cipher) // 16
N = n + nblocks * 16 * 8
a0 = vector(GF(2), N)
for i in range(len(cipher)):
  blk = i // 16
  for j in range(8):
    v = cipher[i] >> j & 1
    a=  copy(a0)
    iid = (i % 16)*8+j
    
    a[nblocks*n:] = vector(res[iid,n:2*n])
    a[blk*n:blk*n+n] = vector(res[iid,:n])
    
    b = (v ^^ int(res[iid,-1]))
    rels.append((a,b))
  


# In[793]:


known = []
for i in range(7): known.append((i, 0))
#for i, v in enumerate(bytearray('a'*7)):
for i, v in enumerate(bytearray('34C3_')):
  known.append((i+8, v))
for i, v in known:
  for j in range(8):
    a = copy(a0)
    vv = v >> j & 1
    a[i*8+j] = 1
    rels.append((a, vv))
   


# In[794]:



bitrel = []
for i in range(8, len(cipher)-31):
 bitrel.append((i*8+7, 0))
#bitrel.append((7*8+6, 0))
#bitrel.append((7*8+5, 1))

for pos, v in bitrel:
 a = copy(a0)
 a[pos] = 1
 rels.append((a, v))


# In[795]:


mrels = matrix(GF(2), len(rels), len(a))
bv = vector(GF(2), len(rels))
for i, (a, b) in  enumerate(rels):
  mrels[i,:] = a
  bv[i] = b
  
  

  


# In[796]:


kern = mrels.right_kernel().matrix()
print(kern.dimensions())


# In[797]:


img = kern[:,:-n].image()
bb=  img.basis_matrix()
print(bb.dimensions())


# In[798]:


ans = mrels.solve_right(bv)[:-n]
print(len(ans))
txt = []
for i in range(0, len(ans), 8):
  txt.append(vec_to_n(ans[i:i+8]))
print(txt)
  
with open('./sol.base', 'wb') as f:
  f.write(bytearray(txt))
with open('./sol.kern', 'wb') as f:
  import struct
  f.write(struct.pack('<II', *bb.dimensions()))
  for i in range(bb.dimensions()[0]):
    for j in range(bb.dimensions()[1]):
      f.write(str(kern[i,j]))


# In[753]:


print(bb.dimensions())


# In[782]:


import array
plain = array.array('B')
plain.fromstring( open('./plain2.enc', 'rb').read())
print(plain)
print(nblocks, len(plain) // 16)


# In[783]:


kx = bytearray('a'*16)
ansv = copy(a0)
print(n)
for i, b in enumerate(plain):
  ansv[i*8:i*8+8] = to_vec(b, 8)
kvec = copy(a0)
for i, b in enumerate(kx):
  kvec[nblocks*n+i*8: nblocks*n+i*8+8] = to_vec(b, 8)
ansv += kvec
  
for a ,b in rels:
  xa = a.dot_product(ansv)
  if xa!=b:
    print(xa, b, a)
  assert xa == b


# In[510]:


inx = [0] * 16
keyx = [0] * 16
evalv = vector(GF(2), 2*n+1)
for i in range(n): evalv[i] = inx[i//8] >> i & 1
for i in range(n): evalv[n+i] = keyx[i//8] >> i & 1
evalv[-1] = 1

evalv0 = vector(GF(2), 2*n+nextp)
for i in range(n): evalv0[i] = inx[i//8] >> i & 1
for i in range(n): evalv0[n+i] = keyx[i//8] >> i & 1
for i in range(4*8): evalv0[n+n+i] = keyx[12+i//8] >> i & 1
for i in range(8): evalv0[n+n+4*8+i] = 0x8d >> i & 1
evalv0[-1] =1

ans0 = res0 * evalv0
tb0 = [0] * 16
for i in range(n):
  tb0[i//8] |= int(ans0[i]) << (i%8)
  
ans = res * evalv
tb = [0] * 16
for i in range(n):
  tb[i//8] |= int(ans[i]) << (i%8)
print(tb)
print(tb0)
  
  


# In[384]:


tmp, kk = None, matrix.identity(GF(2), n+nextp)
tmp, kk = expand_round((tmp, kk))
tmp, kk = expand_round((tmp, kk))
evalv = vector(GF(2), n+nextp)
for i in range(n): evalv[i] = keyx[i//8] >> i & 1
for i in range(4*8): evalv[n+i] = keyx[12+i//8] >> i & 1
for i in range(8): evalv[n+4*8+i] = 0x8d >>i & 1
evalv[-1] = 1

ans = kk * evalv
tb = [0] * 16
word = [0] * 4
for i in range(n):
  tb[i//8] |= int(ans[i]) << (i%8)
for i in range(4*8):
  word[i//8] |= int(ans[n+i]) << (i%8)
rcon = 0 
for i in range(8):
  rcon |= int(ans[n+4*8+i]) << (i%8)
print(tb, word, rcon)

  
  
def to_vec(v, nn):
  res = vector(GF(2), nn)
  for i in range(nn): res[i] = v >> i & 1
  return res


def vec_to_n(x):
  res = 0
  for i in range(len(x)):
    res |= int(x[i]) << i
  return res

tm = matrix(GF(2), 8, 9)
for i in range(8): tm[i,i] = 1
tm = sbox_tsf(tm)
aa= tm * to_vec(0x100 | 93, 9)
print(sbox[93], vec_to_n(aa))
print(tm)
  


# In[385]:


print(mul_mat(2))

