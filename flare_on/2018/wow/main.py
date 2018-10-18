#!/usr/bin/env python

from chdrft.cmds import CmdsList
from chdrft.main import app
from chdrft.utils.cmdify import ActionHandler
from chdrft.utils.misc import Attributize
import chdrft.utils.misc as cmisc
import glog
import struct
from chdrft.emu.binary import x86_mc

global flags, cache
flags = None
cache = None


def args(parser):
  clist = CmdsList().add(test).add(decode1).add(test1)
  ActionHandler.Prepare(parser, clist.lst)


def test(ctx):
  print('on test')


def decode1(ctx):
  magic = 0xdeedeeb
  data = open('./dump1.bin', 'rb').read()
  res = bytearray()
  for i in range(0, len(data), 4):
    content = data[i:i+4]
    tmp = struct.unpack('<I', content)[0] ^ magic
    res.extend(struct.pack('<I', tmp))
  with open('./dump1.dec.bin', 'wb') as f:
    f.write(res)

  # + jump at 0x580


def test1(ctx):
  tmp =[61] + [0]*4+[116,6,104] + [0]*4+[-61,-117,-52,102,-127,-28, -8, -1, 102, -125, -20, 32, -22] +  [0]*4 + [51,0]
  tmp = bytearray([x%256 for x in tmp])
  print(tmp)
  x86_mc.disp_ins(tmp)

def main():
  ctx = Attributize()
  ActionHandler.Run(ctx)


app()
