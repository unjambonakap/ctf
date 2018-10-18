
# coding: utf-8

# In[9]:


lst = [831859191720139449, 9851589274461583502, 7428013382608299119, 6195444962520996076, 9270419801499270943, 8012680837977611190, 5829434570022631083, 860371710421504904, 7594472904013868669, 333314036240824486
      ]
n = len(lst)


# In[21]:


print(n)
m = matrix(ZZ , n-2, 3)
for i in range(n-2):
  m[i,0] = lst[i]
  m[i,1] = lst[i+1]
  m[i,2] = 1
  
b = vector(lst[2:])
  
H,U = m.hermite_form(transformation=True)
r = U * b
mod = gcd(r[3:])


nm = matrix(Integers(mod), m)
print(nm.solve_right(b))

