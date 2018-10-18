#!/usr/bin/env python

from chdrft.cmds import CmdsList
from chdrft.main import app
from chdrft.utils.cmdify import ActionHandler
from chdrft.utils.misc import Attributize
import chdrft.utils.misc as cmisc
import glog
from chdrft.tube.connection import Connection
import json

global flags, cache
flags = None
cache = None


def args(parser):
  clist = CmdsList().add(test)
  ActionHandler.Prepare(parser, clist.lst)


def test(ctx):
  if 0:
    for i in range(200):
      with Connection('arcade.fluxfingers.net', 1822) as conn:
        order = 79182553273022138539034276599687

        print('ADDINg ', i)
        data = dict(x=542342417109300762922401936535663978, y=726821508217691654812343977365180386, c=0xdead+order*i, d=0xbeef, groupID='jambon')
        print(data)
        conn.send_padded(json.dumps(data)+'\n', 8192)


  with Connection('arcade.fluxfingers.net', 1822) as conn:
    ndata = dict(x=167579391684973268008976899398162142, y=112257816371615265563133215310271332, c=0xdeaf, d=0xbeff, groupID='jambon')
    conn.send_padded(json.dumps(ndata)+'\n', 8192)
    conn.interactive()


def main():
  ctx = Attributize()
  ActionHandler.Run(ctx)


app()
