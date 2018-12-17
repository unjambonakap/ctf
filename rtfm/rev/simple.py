#!/usr/bin/env python

from chdrft.cmds import CmdsList
from chdrft.main import app
from chdrft.utils.cmdify import ActionHandler
from chdrft.utils.misc import Attributize
import chdrft.utils.misc as cmisc
import glog

global flags, cache
flags = None
cache = None


def args(parser):
  clist = CmdsList().add(test)
  ActionHandler.Prepare(parser, clist.lst)


def test(ctx):
  print('on test')
  import binascii
  data = binascii.unhexlify('8478828074859993816969847A70847A7A8065799E')
  for b in range(128):
    res = [b]
    for i in range(1, len(data)):
      px = (data[i-1] - (res[-1]-0x58)) % 256
      res.append(px)
    print(bytes(res))


def main():
  ctx = Attributize()
  ActionHandler.Run(ctx)


app()
