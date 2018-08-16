#!/usr/bin/env python

from chdrft.cmds import CmdsList
from chdrft.main import app
from chdrft.utils.cmdify import ActionHandler
from chdrft.utils.misc import Attributize
import chdrft.utils.misc as cmisc
import glog
import not_des

global flags, cache
flags = None
cache = None


def args(parser):
  clist = CmdsList().add(test).add(test2)
  ActionHandler.Prepare(parser, clist.lst)

def doit(inp, key):
  inp=bytes(inp)
  key=bytes(key)
  a = not_des.DESEncrypt(inp, key)
  res=  not_des.Xor(a, inp)
  print('fuuu', a, res, inp)
  return res

def rdoit(inp, key):
  inp=bytes(inp)
  key=bytes(key)
  return not_des.Xor(not_des.DESDecrypt(inp, key), inp) 

def test(ctx):
  key = bytearray(b'a'*not_des.KEY_SIZE)
  inp = bytearray(b'a'*not_des.BLOCK_SIZE)
  tot = key+inp

  key[0]^=1
  tot += key + inp

  kx = b'a'*not_des.KEY_SIZE
  tmp = not_des.DESDecrypt(b'\x00'*not_des.BLOCK_SIZE, kx)
  print(doit(tmp, kx))
  print(not_des.DESEncrypt(tmp, kx))

  tot += kx + tmp
  open('./output.dat', 'wb').write(tot)


def test2(ctx):
  k0 = bytes(b'\x00'*not_des.KEY_SIZE)
  k1 = bytes(b'\xff'*not_des.KEY_SIZE)
  import struct

  for i in range(2**40):
    inp = struct.pack('<Q', i)
    outp = not_des.DESEncrypt(inp, k0)
    if bytes(outp) == inp:
      print('FOUND ', inp)
      break

def main():
  ctx = Attributize()
  ActionHandler.Run(ctx)


app()
