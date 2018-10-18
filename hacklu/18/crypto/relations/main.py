#!/usr/bin/env python

from chdrft.cmds import CmdsList
from chdrft.main import app
from chdrft.utils.cmdify import ActionHandler
from chdrft.utils.misc import Attributize
import chdrft.utils.misc as cmisc
import glog
from chdrft.tube.connection import Connection
from contextlib import ExitStack
import re

global flags, cache
flags = None
cache = None
import base64


def args(parser):
  clist = CmdsList().add(test)
  ActionHandler.Prepare(parser, clist.lst)



class Solver(ExitStack):
  def __init__(self):
    super().__init__()
    self.conn = Connection('arcade.fluxfingers.net', 1821)

  def __enter__(self):
    super().__enter__()
    self.enter_context(self.conn)
    self.conn.recv_until('Possible Oracles')
    return self



  def get_ans(self):
    res= self.conn.recv_until('Possible Oracles').decode()
    m = re.search('Ciphertext is  (.+)', res)
    return base64.b64decode(m.group(1))

  def do_xor(self, a):
    self.conn.send(f'XOR\n{a:x}\n')
    return self.get_ans()

  def do_add(self, a):
    self.conn.send(f'ADD\n{a:x}\n')
    return self.get_ans()


def test(ctx):
  with Solver() as solver:
    v = 0

    for i in range(128):
      print('ON ', i)
      if solver.do_xor(1<<i) != solver.do_add(1<<i):
        v |= 1<<i

    print('GOT ', v)
    ov = v
    for typ in ('big', 'little'):
      for xv in (0, 2**127):

        key = bytearray((v^xv).to_bytes(16, typ))
        print('KEY >> ', key, base64.b64encode(key))
        solver.conn.send(f'DEC\n{base64.b64encode(key).decode()}\n')
    solver.conn.interactive()

#flag{r3l4t3d_k3y_der1iviNg_fuNct1on5_h4ve_to_be_a_l1mit3d_cla55}





def main():
  ctx = Attributize()
  ActionHandler.Run(ctx)


app()
