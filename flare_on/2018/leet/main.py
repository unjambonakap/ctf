#!/usr/bin/env python

from chdrft.cmds import CmdsList
from chdrft.main import app
from chdrft.utils.cmdify import ActionHandler
from chdrft.utils.misc import Attributize
import chdrft.utils.misc as cmisc
import glog
import json
import base64

global flags, cache
flags = None
cache = None


def args(parser):
  clist = CmdsList().add(test)
  ActionHandler.Prepare(parser, clist.lst)


def test(ctx):
  data = json.load(open('./dump.json', 'r'))
  for seg in data:
    seg = Attributize(seg)
    with open(f'segs/seg_{seg.mem_seg}_{hex(seg.addr)}.bin', 'wb') as f:
      f.write(base64.b64decode(seg.content))



def main():
  ctx = Attributize()
  ActionHandler.Run(ctx)


app()
