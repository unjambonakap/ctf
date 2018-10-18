
# coding: utf-8

# In[247]:


x = GF(2)['y'].gen()
poly = x ^ 256 + x ^ 10 + x ^ 5 + x ^ 2 + 1
poly.factor()
state = 0x48400000000000014840000148400000000000000000000000000000000000010000000000000001000000010000000000000000000000000000000000000001
EXPECTED = 0x48400000000000014840000148400000000000000000000000000000000000010000000000000001000000010000000000000000000000000000000000000001
EXPECTED =0x5c96048400000000000000000000000000000000000000000000000000000001104010000000000000000000000000000000000000000000000000000000000148400000000000000000000000000000000000000000000000000000000000010000000000000000000000000000000000000000000000000000000000000001
state_tb = []
for i in range(512):
  state_tb.append(state >> i & 1)

n = 256
mat = matrix(GF(2), n, n)
px = []
for i in range(n+1):
  px.append(poly[i])


# In[110]:


matrix(GF(2), [[1,1],[2,1]])
vector


# In[194]:


px = px[::-1]
if 1:
  for i in range(n):
    mat[n - 1, i] = px[i]
    if i != 0: mat[i - 1, i] = 1
else:
  for i in range(n):
    mat[i, 0] = px[i]
    if i != 0: mat[i - 1, i] = 1
      

      
mconds = matrix(GF(2), n,n)
for i in range(n):
  ac = mat ** i
  mconds[i,:] = vector(ac[:,0])
  mconds[i,:] = vector(ac[0,:])
  
b = vector(GF(2), state_tb[0:n])
ans = mconds.solve_right(b)
print(ans)


# In[192]:


m2 = matrix(GF(2), n, n)
for i in range(n):
  for j in range(n):
    m2[i, j] = state_tb[i+j]
b2 = vector(GF(2), state_tb[n:])
print(m2.solve_right(b2))
print(m2.kernel())


# In[87]:


pr.<x0,x1,x2,x3,x4,x5> = BooleanPolynomialRing()
xlist = [x0,x1,x2,x3,x4,x5, 1]


# In[94]:


f0=1+x0*x1*x2*x3*x4 + x0*x1*x2 + x0*x1*x3*x4*x5 + x0*x1*x4 + x0*x1*x5 + x0*x2*x3*x4*x5 + x0*x2*x3 + x0*x2*x4 + x0*x4*x5 + x0 + x1*x2*x3*x4*x5 + x1*x2*x4 + x1*x2*x5 + x1*x3*x4 + x1*x3*x5 + x1 + x2*x3*x4 + x2 + x3*x4*x5
f = nf
lst = []
for i in range(1, 128):
  g = 0
  for j in range(7):
    if i>>j&1: g += xlist[j]
  lst.append(((g*f).degree(), i))
print(min(lst))
    


# In[121]:


nf =   x0*x1*x2*x3*x4*x5 + x0*x1*x2*x3*x4 + x0*x1*x2*x3 + x0*x1*x2*x4 + x0*x1*x3*x4*x5 + x0*x1*x4*x5 + x0*x1*x4 + x0*x1*x5 + x0*x2*x3*x4 + x0*x2*x3*x5 + x0*x2*x3 + x0*x2*x4 + x0*x3*x4*x5 + x0*x3*x4 + x0*x3*x5 + x0*x3 + x0*x4 + x0*x5 + x0 + x1*x2*x3*x4*x5 + x1*x2*x3*x4 + x1*x2*x4 + x1*x2*x5 + x1*x3 + x1*x4*x5 + x1*x4 + x1*x5 + x1 + x2*x3*x4*x5 + x2*x3*x5 + x2*x3 + x2*x4*x5 + x2*x4 + x2*x5 + x2 + x3*x4*x5 + 1


# In[119]:


from sage.crypto.boolean_function import BooleanFunction

tb = [0, 1, 1, 0, 1, 0, 0, 0, 0, 1, 1, 0, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 0, 0, 1, 1, 1, 0, 1, 1, 1, 1, 0, 1, 0, 0, 1, 0, 0, 1, 1, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 1, 1, 0, 1, 1, 0, 1, 1]
tb = [0, 1, 1, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 1, 0, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 1, 1, 0]

tb = [a^1 for a in tb]
func = BooleanFunction(tb)


# In[122]:


f2 = BooleanFunction(nf)
for a, b in zip(func.truth_table(), f2.truth_table()):
  print(a,b)


# In[125]:


print(func.algebraic_normal_form())
print(func.absolute_autocorrelation())
print(func.nonlinearity())
print(f2.annihilator(3))
print(func.autocorrelation())
func.truth_table()


# In[108]:


import mat


# In[255]:


class LFSR:
  def __init__(self, coeffs, n=None, state=1, version=0):
    poly = 0
    if n is None: n = coeffs[-1]
    for j in coeffs:
      poly |= 1 << j
    rpoly = 0
    for j in coeffs:
      rpoly |= 1 << (n-j)
    self.coeffs = coeffs
    self.poly = (poly, rpoly)[version%2]
    self.n = n
    self.state = state
    self.mask = (1 << n) - 1
    self.next = (self.next1, self.next2, self.next3, self.next4)[version // 2]

  def next2(self):
    b = self.state >> (self.n - 1)
    self.state = self.state << 1
    assert b == 0 or b == 1
    if b:
      self.state ^^= self.poly^^1 
    return b

  def next1(self):
    b = self.state & 1
    if b & 1:
      self.state ^^= self.poly ^^ 1
    self.state = self.state >> 1
    return b
  
  def next3(self):
    b = self.state & 1
    tmp = self.state & self.poly
    self.state = self.state >> 1
    cnt = 0
    for j in range(self.n):
      cnt ^^= tmp >> j & 1
    self.state |= cnt << self.n-1
    self.state &= self.mask
    return b
  
  def next4(self):
    vx = 0
    for i in (256, 96, 64):
    #for i in (1, 161, 193):
      vx ^^= self.state >> (256-i) & 1
    self.state = self.state << 1
    bx = self.state >> self.n & 1
    if bx:
      self.state ^^= self.poly
    return vx
    return bx
    
  
  def get_seq(self, state, n):
    self.state = state
    res = 0
    for i in range(n):
      res |= self.next() << i
    return res


# In[256]:


coeffs = [0, 2, 5, 10, 256]
nx = 1024
for version in range(8):
  a = LFSR(coeffs, 256, 1, version=version)
  print('TRY')
  print 'G',hex(a.get_seq(1, nx))
  print 'A',hex(a.get_seq(1<<255, nx))
print 'R', hex(EXPECTED)
print 'done'


# In[261]:



a = LFSR(coeffs, 256, 1, version=2*2)
for i in range(1024):
  v = a.next()
  assert v == (EXPECTED >> i & 1)
  if v: print i, v


# In[207]:


for i in range(512):
  if (EXPECTED >> i & 1): print(i)

