#!/usr/bin/env python

from chdrft.main import app
from chdrft.emu.binary import x86_mc, patch_file


global flags, cache
flags = None
cache = None

def args(parser):
  pass

def main():
  #patch_file('./b3s23', 0x0000111d, b'\x00'*4)
  #patch_file('./b3s23', 0x0000900, b'\x10'*4)
  x86_mc.disp_ins(b'\x00')

  lst='add dl, 1; inc edx; xor eax, eax; nop; mov ecx, ebx; xor ebx, ebx; mov dl, 0xff; add al, 3; int 0x80; add al, 0'.split(';')

  tot=[]
  for x in lst:
    v=x86_mc.get_disassembly(x)
    s=[]
    for i in range(len(v)*8):
      s.append(v[i//8]>>(i&7)&1)
    print(x, s)
    tot.extend(s)
  print(len(tot))

#pusha [0, 0, 0, 0, 0, 1, 1, 0]
#xor eax, eax [1, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1]
#nop [0, 0, 0, 0, 1, 0, 0, 1]
#mov ecx, ebx [1, 0, 0, 1, 0, 0, 0, 1, 1, 0, 0, 1, 1, 0, 1, 1]
#xor ebx, ebx [1, 0, 0, 0, 1, 1, 0, 0, 1, 1, 0, 1, 1, 0, 1, 1]
#mov dl, 0xff [0, 1, 0, 0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1]
#add al, 3 [0, 0, 1, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0]
#int 0x80 [1, 0, 1, 1, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1]
#add al, 0 [0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
#xor dl, 0x80 [0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1]


  sol=['0 tub 0 0 0 0 block 0 0 0 0 0 0 0', #add al, 3
      'block 0 tub 0 0 block 0 0 block 0 block',#mov ecx, ebx 
      '0 0 0 tub 0',  #nop
      'block 0 0 0 block 0 0 block 0 block 0 block', #xor ebx, ebx
      '0 0 0 0 0 block 0', #pusha
      '0 tub 0 0 0 0 0 0 0 0 0 0 0 0', # add al, 0
      'tub, '
      'block 0 block 0 0 block 0 0 0 0 0 0 tub',
      ]



app()
