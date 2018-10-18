
# coding: utf-8

# In[1]:


import sys
import angr
import logging
logging.getLogger('angr').setLevel('WARNING')


# In[25]:





# In[2]:


#proj = angr.Project('./a.out')
proj = angr.Project('./algo.opt.out')
test_func = proj.loader.find_symbol('test')
print(proj.entry)


# In[3]:


def solve(n):
  s = proj.factory.blank_state(addr=test_func.rebased_addr)
  q = s.memory.load(0x1000, n+1)
  for i in range(8):
    s.se.add(q[i] == 0)
  print(q)

  # call the authenticate function with *username being 0x1000 and *password being 0x2000
  #c = proj.surveyors.Caller(test_func.rebased_addr, (0x1000,0x2000), start=s)
  print(hex(test_func.rebased_addr))
  c = proj.surveyors.Caller(test_func.rebased_addr, (0x1000, n), start=s)

  res  = tuple(c.map_se('eval_upto', q, 2, solution=1, cast_to=str))
  print(res)


# In[ ]:


solve(33)


# In[123]:




