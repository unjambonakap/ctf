#!/usr/bin/env python

import not_des
k0 = bytes(b'\x00'*not_des.KEY_SIZE)
k1 = bytes(b'\xff'*not_des.KEY_SIZE)
import struct

for i in range(2**40):
  inp = struct.pack('<Q', i)
  outp = not_des.DESEncrypt(inp, k0)
  if i % 10000 == 0: print(i)
  if bytes(outp) == inp:
    print('FOUND ', inp)
    break
