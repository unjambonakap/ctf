#!/usr/bin/env python

from chdrft.cmds import CmdsList
from chdrft.main import app
from chdrft.utils.cmdify import ActionHandler
from chdrft.utils.misc import Attributize
import chdrft.utils.misc as cmisc
import glog
import numpy as np
from chdrft.emu.binary import arch_data, guess_arch
import chdrft.emu.kernel as kernel
from chdrft.emu.structures import StructBuilder, CodeStructExtractor, Structure, StructBackend, g_data, MemBufAccessor
from chdrft.emu.func_call import AsyncMachineCaller, FuncCallWrapperGen, FunctionCaller, AsyncFunctionCaller, SimpleBufGen
import unicorn as uc
from chdrft.emu.elf import ElfUtils
from chdrft.emu.trace import TraceEvent, WatchedMem, WatchedRegs, Display
import chdrft.emu.trace as trace
import traceback as tb
import numpy as np
import binascii
import struct
from chdrft.tube.fifo import ManagedBidirectionalFifo
from chdrft.tube.process import Process
import curses.ascii
import time
glog.setLevel(glog.INFO)
import itertools
import os
import ctypes
import ctypes.util
from chdrft.utils.swig import swig_unsafe
from collections import defaultdict
import pefile
import yaml
import chdrft.emu.structures as Structures
import subprocess as sp
from chdrft.tube.serial import Serial
from chdrft.dbg.gdbdebugger import GdbDebugger, launch_gdb
from concurrent.futures import wait
import tempfile
import re
import multiprocessing
import pprint
from collections import OrderedDict
import pickle
import z3
from chdrft.tube.connection import Connection, Server
import disk_code
import networkx as nx
import numpy as np
import pygraphviz
from networkx.drawing.nx_agraph import write_dot
import glob

charset = [i for i in range(128) if curses.ascii.isprint(i)]

global flags, cache
flags = None
cache = None
BASE_PASSWORD = 'jambonkapalala'

solve_pwd = bytes(( 0x40,0x1,0x4e,0x6,0x43,0x6,0x52,0x2,0x22,0x10,0x14,0x7,0x31,0xd7,0x52,0xd2,0x6,0xe7,0x4,0x14,0x43,0x10,0x7,0xd1,0xcd,0x14,0xcc,0x1,0x31,0x13))

def args(parser):
  clist = CmdsList().add(test).add(search).add(decode).add(gen_turing_data).add(analyse).add(
      analyse_z3
  ).add(trace).add(ser_bx).add(translate_code).add(blk_analysis).add(solve_l2).add(analyse_l2)
  clist.add(l2_analyse_loop1).add(l2_explore_end).add(l2_diff_exec).add(l2_full_graph).add(l2_analyse_patterns).add(l2_track_conds).add(l2_decode)
  clist.add(l2_run_multiple).add(maybe_final).add(l2_test).add(l2_diff_mems).add(l2_final)


  ActionHandler.Prepare(parser, clist.lst)
  parser.add_argument('--mem', default='./dump.state1.bin')
  parser.add_argument('--regs', default='./dump.state1.regs')
  parser.add_argument('--pickle_start', default='./turing_data/real.start')
  parser.add_argument('--infile')
  parser.add_argument('--bochs_state', action='store_true')
  parser.add_argument('--has-header', action='store_true')
  parser.add_argument('--mode1', action='store_true')
  parser.add_argument('--follow', action='store_true')
  parser.add_argument('--raw-password', action='store_true')
  parser.add_argument('--debug', action='store_true')
  parser.add_argument('--use_final', action='store_true')
  parser.add_argument('--analyse_loop', action='store_true')
  parser.add_argument('--shorten', action='store_true')
  parser.add_argument('--track_tainted', action='store_true')
  parser.add_argument('--taint_pwd', action='store_true')
  parser.add_argument('--gen-graph', action='store_true')
  parser.add_argument('--taint', nargs='*', type=cmisc.to_int, default=[])
  parser.add_argument('--stopb', nargs='*', type=cmisc.to_int, default=[])
  parser.add_argument('--infiles', nargs='*', type=str, default=[])

  parser.add_argument('--startb', type=int)
  parser.add_argument('--stop_access', type=cmisc.to_int, nargs='*', default=[])
  parser.add_argument('--passlist', type=str, nargs='*', default=[])
  parser.add_argument('--initpass')
  parser.add_argument('--qemu_log', action='store_true')
  parser.add_argument('--stop_at_output', action='store_true')
  parser.add_argument('--signed_load', action='store_true')
  parser.add_argument('--outfile')
  parser.add_argument('--analyse_to', type=int)
  parser.add_argument('--analyse_count', type=int, default=1)
  parser.add_argument('--codefile')
  parser.add_argument('--maxrounds', type=int, default=200)

  parser.add_argument('--transpile-req', type=cmisc.to_int, nargs='*', default=[])

def main():
  g_data.set_m32(True)
  ctx = Attributize()
  ActionHandler.Run(ctx)


def load_kern(ctx):
  code_low = 1
  code_high = 0
  stack_low = 1
  stack_high = 0
  log_file = '/tmp/info.out_{}'.format(ctx.runid)
  if flags.bochs_state:
    kern, elf = kernel.Kernel.LoadFrom(bochs_state=(ctx.mem, ctx.regs), arch=guess_arch('x86_16'))
  else:
    kern, elf = kernel.Kernel.LoadFrom(qemu_state=(ctx.mem, ctx.regs), arch=guess_arch('x86_16'))

  #kern.mu.hook_add(uc.UC_ERR_WRITE_PROT, kernel.safe_hook(kern.hook_bad_mem_access), None, 0, 2**32-1)
  kern.mu.hook_add(
      uc.UC_HOOK_MEM_WRITE_UNMAPPED | uc.UC_HOOK_MEM_FETCH_UNMAPPED,
      kernel.safe_hook(kern.hook_unmapped)
  )
  kern.mu.hook_add(uc.UC_HOOK_CODE, kernel.safe_hook(kern.hook_code), None, code_low, code_high)
  kern.mu.hook_add(
      uc.UC_HOOK_MEM_READ | uc.UC_HOOK_MEM_WRITE, kernel.safe_hook(kern.hook_mem_access), None, 1, 0
  )
  kern.tracer.ignore_unwatched = True
  #kern.tracer.watched.append(WatchedRegs('regs', regs, cmisc.to_list('rip rcx rdx rsp')))
  kern.tracer.watched.append(WatchedMem('all', kern.mem, 0, n=2**32, sz=1))

  return kern, elf


class KernelRunner:

  def __init__(self, kern):
    self.kern = kern

  def __call__(self, end_pc):
    pass


class UCSolver:

  def __init__(self, kern):
    self.kern = kern
    self.regs = kern.regs
    self.mem = kern.mem
    self.stack = kern.stack
    self.handler = self.handle()
    kern.mu.hook_add(uc.UC_HOOK_INTR, kernel.safe_hook(self.hook_intr0))
    kern.hook_intr_func = self.hook_intr
    self.output = bytearray()
    self.msgs = []
    self.bios_cnt = 0x1000
    self.kern.notify_hook_code = self.notify_hook_code
    self.img = open('./suspicious_floppy_v1.0.img', 'rb').read()

    self.dx = dict()

    self.keydata = bytearray(b'a\r')
    self.keypos = 0

  def hook_addr(self, addr, handler=None):
    if handler is None: handler = self
    self.kern.mu.hook_add(uc.UC_HOOK_CODE, kernel.safe_hook(handler), None, addr, addr + 1)

  def failure_hook(self, *args):
    print('ON FAILURE')
    self.kern.stop()

  def do_retf(self, n):
    nip, ncs = self.stack.popn(2)
    self.stack.popn(n)
    self.regs.ip = nip
    self.regs.cs = ncs

  def notify_hook_code(self, address):
    if address == 0x97c12:
      nread = self.regs.al
      buf = self.regs.es * 16 + self.regs.bx
      head = self.regs.dh
      cylinder = self.regs.ch
      assert self.regs.dl == 0
      self.regs.flags.cf = 0
      self.regs.ah = 0
      self.regs.al = nread
      sector = self.regs.cl - 1 + 18 * head + cylinder * 36
      self.msgs.append(f'Read sector {sector} {buf}')
      self.mem.write(buf, self.img[sector * 512:(sector + nread) * 512])
      self.do_retf(1)
    pass

  def check_enhanced_keystroke(self):
    self.regs.flags.zf = 0
    self.kern.change_eflags = self.regs.eflags
    self.regs.al = self.keydata[self.keypos]

  def get_enhanced_keystroke(self):
    self.regs.al = self.keydata[self.keypos]
    self.keypos += 1

  def charout(self, c):
    self.output.append(c)
    print('OUTPUT >> ', self.output)

  def hook_intr0(self, _1, intno, _2):
    self.regs.ip += 2
    #self.kern.kill_in =10
    pass

  def open_existing_file(self):
    addr = self.regs.ds * 16 + self.regs.dx
    fname = self.mem.get_str(addr).decode()
    print('MODE >> ', hex(self.regs.al), hex(addr), fname)

    assert fname.find('/') == -1, fname
    self.regs.flags.cf = 0
    handle = len(self.dx) + 3
    self.dx[handle] = open('DATA/' + fname, 'rb+')

    self.regs.ax = handle

  def close_file(self):
    self.regs.flags.cf = 0
    self.regs.ax = 0

  def get_dev_info(self):
    print(self.regs.bx)
    self.regs.flags.cf = 0
    self.regs.dx = 0x40

  def write_to_file(self):
    print('handle', self.regs.bx, self.regs.cx)
    addr = self.regs.ds * 16 + self.regs.dx
    handle = self.regs.bx
    content = self.mem.read(addr, self.regs.cx)
    print('WROTE >> ', content)
    self.regs.flags.cf = 0
    f = self.dx[handle]
    f.write(content)
    self.regs.ax = self.regs.cx

  def read_file(self):
    print('handle', self.regs.bx, self.regs.cx)
    addr = self.regs.ds * 16 + self.regs.dx
    handle = self.regs.bx
    f = self.dx[handle]
    n = self.regs.cx
    res = f.read(n)
    self.mem.write(addr, res)
    self.regs.flags.cf = 0
    self.regs.ax = len(res)
    self.msgs.append(f'Read {handle} {n}')

  def lseek(self):
    orig = self.regs.al
    handle = self.regs.bx
    pos = ctypes.c_int32(self.regs.cx << 16 | self.regs.dx).value
    f = self.dx[handle]
    f.seek(pos, orig)
    npos = f.tell()
    self.regs.ax = npos >> 16
    self.regs.dx = npos & 0xffff

  def hook_intr(self, intno, addr):
    print(self.output)
    print('\n'.join(self.msgs))
    self.msgs.append(
        f'HAS INT {intno:x} {self.regs.ah:x} {self.regs.al:x} {self.regs.ip:x} {addr:x}'
    )
    print(f'=================ON INTER {intno:x} {self.regs.ah:x}, {self.regs.al:x}')
    self.kern.stack.push(self.regs.eflags)
    self.kern.stack.push(self.regs.cs)
    self.kern.stack.push(addr - self.regs.cs * 16)
    intpos = 4 * intno
    to_ip = self.mem.read_u16(intpos)
    to_cs = self.mem.read_u16(intpos + 2)
    self.regs.cs = to_cs
    self.regs.ip = to_ip
    print(f'{intpos:x} {to_cs:x} {to_ip:x}')

    ah = self.regs.ah
    ax = self.regs.ax
    if 0:
      pass
    elif (intno, ah) == (0x16, 0x11):
      self.check_enhanced_keystroke()
    elif (intno, ah) == (0x16, 0x10):
      self.get_enhanced_keystroke()
    elif (intno, ah) == (0x21, 0x3e):
      self.close_file()
    elif (intno, ah) == (0x21, 0x3d):
      self.open_existing_file()
    elif (intno, ah) == (0x21, 0x44):
      self.get_dev_info()

    elif (intno, ah) == (0x21, 0x40):
      self.write_to_file()
    elif (intno, ah) == (0x21, 0x42):
      self.lseek()

    elif (intno, ah) == (0x21, 0x3f):
      self.read_file()
    elif (intno, ah) == (0x10, 0xe):
      self.charout(self.regs.al)

    elif (intno, ax) == (0x2f, 0x168f):
      print('req close intr')
    elif (intno, ah) == (0x2a, 0x84):
      print('keyboard loop intr')
    elif (intno, ah) == (0x2a, 0x82):
      print('network useless')
    elif (intno, ah) == (0x2f, 0x11):
      print('network useless 2')
    elif (intno, ah) == (0x1a, 0x0):
      print('get time', self.bios_cnt)
      self.mem.write_u8(0x470, 0)
      self.mem.write_u32(0x46c, self.bios_cnt)
      self.bios_cnt += 1
    elif (intno, ah) == (0x13, 0x2):
      # read sector
      print('READ SECTXOR')

    else:
      assert 0
    #self.kern.kill_in = 10

  def __call__(self, *args, **kwargs):
    next(self.handler)

  def handle(self):
    self.kern.stop()
    yield


def event_handle(e, fevent, fop):
  glog.info('Got event %s', e)
  if isinstance(e, trace.TraceEvent):
    fevent.write(str(e) + '\n\n')

  elif isinstance(e, trace.VmOp):
    fevent.write(e.gets(regs=True) + '\n\n\n')
    fop.write(str(e) + '\n\n\n')
    fop.flush()
    fevent.flush()


def trace_event_handler(e):
  if isinstance(e, TraceEvent):
    print(str(e) + '\n\n')


def test(ctx):
  kern, elf = load_kern(ctx)
  kern.tracer.diff_mode = False
  event_log = open('/tmp/evens_{}.out'.format(ctx.runid), 'w')
  vmop_log = open('/tmp/vmop_{}.out'.format(ctx.runid), 'w')
  kern.tracer.cb = lambda x: event_handle(x, event_log, vmop_log)

  solver = UCSolver(kern)
  kern.ignore_mem_access = False

  try:
    #kern.set_real_mode()
    print(kern.regs.cs)
    print(kern.regs.ip)
    kern.regs.ip += kern.regs.cs * 16
    kern.start()
    #print('RESTARTING')
    #kern.set_real_mode()
    #kern.start(count=3)
  except uc.UcError as e:
    print('%s' % e)
    tb.print_exc()

  #print(kern.mem.read(output_addr, 20))
  return


def search(ctx):
  if 0:
    dx = open('./suspicious_floppy_v1.0.img', 'rb').read()
    if 1:
      pattern = b'aaaaaaaa'
    else:
      pattern = bytes(
          [
              0xe5, 0x20, 0x20, 0x20, 0x20, 0x20, 0x20, 0x20, 0x20, 0x20, 0x20, 0x10, 0x00, 0x00,
              0x00, 0x00, 0x00, 0x00, 0x99, 0x32, 0x00, 0x00, 0xf8, 0x66, 0x88, 0x32, 0x57, 0x04,
              0x00, 0x02, 0x00, 0x00, 0xe5, 0x55, 0x54, 0x4f, 0x45, 0x58, 0x45, 0x43, 0x42, 0x41,
              0x54, 0x20, 0x00, 0xa4, 0xf0, 0x6c, 0x87, 0x2a, 0x87, 0x2a, 0x00, 0x00, 0x00, 0x88,
              0xc8, 0x28, 0xe6, 0x00, 0xe5, 0x04, 0x00, 0x00, 0xe5, 0x4f, 0x4e, 0x46, 0x49, 0x47,
              0x20, 0x20, 0x53, 0x59, 0x53, 0x20, 0x00, 0x37, 0xf1, 0x6c, 0x87, 0x2a, 0x89, 0x2a,
              0x00, 0x00, 0x00, 0x88, 0xc8, 0x28, 0xe9, 0x00, 0x4f, 0x03, 0x00, 0x00, 0xe5, 0x45,
              0x54, 0x52
          ]
      )

  else:
    dx = open('./dump.state4.mem', 'rb').read()
    pattern = open('./alldata/img/infohelp.exe', 'rb').read()[:100]
    pattern = b'aaaaaaaa'

  print(hex(dx.find(pattern)))
  print(hex(dx.rfind(pattern)))


def poly(x, a0, a1, a2):
  x[a1] = (x[a1] - x[a0]) & 0xffff
  return a2 and x[a1] == 0


def make_secret(x, m1, m2):
  b = m2
  rnd = 0
  while True:
    rnd += 1
    if b + 3 > m1: break

    if poly(x, x[b], x[b + 1], x[b + 2]):
      if x[b + 2] == 0xffff:
        break
      b = x[b + 2]
    else:
      b += 3

    #if rnd == 3:
    #  break
    if rnd % 100000 == 0:
      print(rnd)
    if x[4]:
      print('OUTPUT ', x[2] & 0xff)
      x[2] = 0
      x[4] = 0


def decode(ctx):
  if 0:
    addr = 0x97c0 * 16 + 0x0223
    buf = open('./dump.test.mem', 'rb').read()[addr:]
    buf = buf[:0x20000]
  else:
    buf = open('./dump.turing.mem', 'rb').read()

  x = []
  for i in range(0, len(buf), 2):
    x.append(struct.unpack('<H', buf[i:i + 2])[0])

  make_secret(x, 0x2dad, 5)


def gen1(pwd):
  try:
    cmd = 'qemu-system-x86_64 -L . -hda fat:hda-contents -bios bios.bin  -nographic -serial pty -monitor stdio -S'
    proc = sp.Popen(cmd, shell=True, stdin=sp.PIPE, stdout=sp.PIPE, stderr=sp.PIPE)
    data = b''
    pts = None
    while True:
      data += proc.stderr.read(1)
      m = re.search(b'(/dev/pts/[0-9]+)\s', data)
      if m:
        pts = m.group(1).decode()
        break
    print(data)
    print(pts)
    proc.stdin.write(b'c\n')
    proc.stdin.flush()

    with Serial(pts) as conn:
      data = b''
      while True:
        data += conn.recv(1)
        if data.find(b'Shell>') != -1:
          break
      print('START HERE')
      conn.send(b'fs0:\r\n')
      time.sleep(0.5)

      conn.send(('%s\r\n' % filename).encode())

      data = b''
      while True:
        data += conn.recv(1)
        if data.find(b'DONE_KAPPA') != -1:
          break

      print('res >>', data)
      res = get_ok_pos(data)
  except Exception:
    print('exception >> ', e)
    traceback.print_exc()
    pass
  proc.stdin.write(b'q\n')
  proc.stdin.flush()
  proc.kill()
  return res


def gdb_get_content(data):
  conn_port, outfile, use_raw_password = data
  print('GDB STUF')
  with Connection('localhost', conn_port) as conn_sync:

    x = GdbDebugger()
    print(x.do_execute('target remote localhost:1234'))
    print('Connected')

    addr = 0x97c0 * 16 + 0x5dd9
    data_addr = 0x97c0 * 16 + 0x223
    send_pass_addr= 0x1e00-5
    buf_addr2= 0x1dfb
    overwrite_pass = (send_pass_addr, buf_addr2, 0x1e7b)
    end_pass_copy_addr = 0xffff*16+0x58eb

    print(x.do_execute(f'x /10w {hex(data_addr)}'))
    x.do_execute(f'b *{hex(end_pass_copy_addr)}')
    want_pass = conn_sync.recv_fixed_size(0x30)
    print('WATED PASS ', want_pass, hex(end_pass_copy_addr))
    conn_sync.send('1')

    x.do_execute('c')
    x.do_execute('delete')


    if not use_raw_password:
      print('ON ', end_pass_copy_addr)
      print('ORIG PWD >> ', x.mem.read(send_pass_addr, 0x30))
      print('ORIG PWD2 >> ', x.mem.read(buf_addr2, 0x30))
      m = x.mem.read(0, 0x100000)
      pattern = BASE_PASSWORD.encode()

      for match in re.finditer(pattern, m):
        pos = match.start()
        print('FOUDN PASS AT ', hex(pos))
        x.mem.write(pos, want_pass)



    x.do_execute(f'b *{hex(addr)}')
    x.do_execute('c')

    print(x.do_execute(f'x /10b {hex(data_addr)}+0d4616'))
    for i, c in enumerate(want_pass):
      if c >= 0x80:
        x.mem.write_u8(data_addr+4616+2*i+1, 0xff)
    print('KAPPA')
    import sys
    print('Buf in data', x.mem.read(data_addr+4616, 0x30))

    sys.stdout.flush()
    data = x.mem.read(data_addr, 0x10)
    print('read some', data)
    data = x.mem.read(data_addr, 0x20000)
    with open(outfile, 'wb') as f:
      f.write(data)
    print('NOW, lets try to finish')
    x.do_execute('delete')
    print('should be done')
    conn_sync.send('1')
    #x.do_execute('c')



def do_run_gdb(port):

  def runner():
    print('luanching gdb')
    launch_gdb('main', 'gdb_get_content', args=[port])

  res = cmisc.chdrft_executor.submit(runner)
  return res


def gen1(pwd):
  time.sleep(1)
  print()
  print()
  print()
  print()
  print()
  print('NOW RUNING ', pwd)
  conn_port = 11111
  res = None

  proc = None
  outfile = tempfile.mktemp()
  task = do_run_gdb((conn_port, outfile, flags.raw_password))
  try:

    cmd = 'qemu-system-i386 -no-kvm -monitor stdio -fda ./suspicious_floppy_v1.0.img -m 32M -smp 1 -nographic -serial pty -S'
    proc = sp.Popen(cmd, shell=True, stdin=sp.PIPE, stdout=sp.PIPE, stderr=sp.PIPE)
    data = b''
    pts = None
    while True:
      data += proc.stderr.read(1)
      m = re.search(b'(/dev/pts/[0-9]+)\s', data)
      if m:
        pts = m.group(1).decode()
        break

    print(data)
    print(pts)

    with Serial(pts) as conn, Server(conn_port) as conn_sync:
      proc.stdin.write(b'c\n')
      proc.stdin.flush()

      data = b''
      time.sleep(0.1)
      #conn.recv_until('Enter the password')
      proc.stdin.write(b'stop\n')
      proc.stdin.write(b'gdbserver\n')
      proc.stdin.write(b'cont\n')
      proc.stdin.flush()

      padded_pwd = bytearray(b'a'*0x30)
      padded_pwd[:len(pwd)] = pwd
      conn_sync.send(padded_pwd)
      conn_sync.recv_fixed_size(1)
      conn.trash()
      if flags.raw_password:
        conn.send(f'{pwd.decode()}' + '\r\n')
      else:
        conn.send(BASE_PASSWORD + '\r\n')
      conn.flush()
      print('SENT password')
      print(conn.recv_fixed_size(30))

      if flags.qemu_log:
        while True:
          print(conn.recv(1))
      conn_sync.recv_fixed_size(1)
      res = open(outfile, 'rb').read()
      wait([task])
      print(conn.flush())
      proc.stdin.write(b'q\n')
      proc.stdin.flush()

  except Exception as e:
    print('exception >> ', e)
    tb.print_exc()
    assert 0

  finally:
    time.sleep(0.1)
    proc.terminate()
    print('KILLING')
    time.sleep(0.1)
    proc.kill()
  return res


def gen_turing_data(ctx):
  for small in charset:
    data = gen1(('@'+chr(small)).encode())
    open(f'./turing_data/test_{small}.out', 'wb').write(data)

  for large in ['a' * 512, 'b' * 512, 'a' * 1024]:
    data = gen1(large)
    open(f'./turing_data/test_large_{large[:10]}_{len(large)}.out', 'wb').write(data)


m1 = 0x2dad
intervals = []


def check_in(x):
  for a0, b0 in intervals:
    if x + 1 >= a0 + 1 and x < b0: return 1
  return 0


def poly(x, a0, a1, a2):
  x[a1] = (x[a1] - x[a0]) & 0xffff
  # branch if x[a1] <= 0
  return a2 and (x[a1] == 0 or (x[a1] >> 15 & 1))


def do_step(b, x):
  if poly(x, x[b], x[b + 1], x[b + 2]):
    if x[b + 2] == 0xffff:
      print('END')
      return None
    b = x[b + 2]
  else:
    b += 3
  return b


def prove(f, conds=[]):
  s = z3.Solver()
  for cond in conds:
    s.add(cond)
  s.add(z3.Not(f))
  return s.check() == z3.unsat


def prove_either(f, conds):
  return prove(f, conds) or prove(z3.Not(f), conds)


def get_data():

  import pickle
  b, x = pickle.load(open('./turing_data/state.start', 'rb'))
  xorig = list(x)
  seen = set()
  import queue
  q = queue.Queue()

  def add(a):
    if a in seen: return
    q.put(a)
    seen.add(a)

  add(b)
  writepos = set()
  jumppos = set()

  while not q.empty():
    b = q.get()
    if b >= 0x2dad: break
    x0, x1, x2 = x[b:b + 3]
    y0, y1, y2 = xorig[b:b + 3]
    assert x0 == y0
    assert x1 == y1
    assert x2 == y2

    writepos.add(x1)
    add(b + 3)
    if x2 != 0:
      add(x[x2])
      jumppos.add(b + 2)

  return Attributize(writepos=disk_code.readsnotconst, jumppos=jumppos)


def bv(val):
  return z3.BitVecVal(val, 16)


class Solver:

  def __init__(self):
    self.rundata = get_data()

  def jit_block(self, node, x, v={}, names={}, conds=[], base_conds=None):
    bvsort = z3.BitVecSort(16)
    ix = list(x)
    x = list(x)
    v = z3.Array('v', bvsort, bvsort)
    names = dict(names)
    conds = list(conds)

    reads = {}
    for i in range(NX):
      ii = bv(i)
      if i in names:
        var = z3.BitVec(names[i], 16)
        conds.append(z3.And(var >= z3.BitVecVal(32, 16), var < z3.BitVecVal(128, 16)))
        vv = var
      elif i in self.rundata.writepos:
        name = 'var_%04x' % i
        vv = z3.BitVec(name, 16)
      else:
        vv = z3.BitVecVal(x[i], 16)
      v = z3.Store(v, ii, vv)


    names.update(base_conds)
    print(len(reads))

    print('Starting')

    cntops = 0
    writes = []
    for b in node.chain:
      bz = bv(b)
      cntops += 1
      a0 = v[bz + bv(0)]
      a1 = v[bz + bv(1)]
      a2 = v[bz + bv(2)]

      v0 = v[a0]
      v1 = v[a1]
      v = z3.simplify(z3.Store(v, a1, v1 - v0))

      a0 = z3.simplify(a0)
      a1 = z3.simplify(a1)
      a2 = z3.simplify(a2)
      cnd = v[a1] <= bv(0)
      writes.append(a1)

    print('GOGO ', cntops, node.chain[0])
    print('reads')
    pprint.pprint(reads)
    print('writes')
    for a in writes:
      a = z3.simplify(a)
      print(a, z3.simplify(v[a]))

  def jit_block0(self, node, x, v={}, names={}, conds=[], base_conds={}):
    ix = list(x)
    x = list(x)
    v = OrderedDict(v)
    names = dict(names)
    conds = list(conds)

    reads = {}

    def get_var(a):
      if a in v: return v[a]
      if a not in names:
        names[a] = 'var_%04x' % a
        if a in self.rundata.writepos:
          v[a] = z3.BitVec(names[a], 16)
        else:
          v[a] = z3.BitVecVal(x[a], 16)
        reads[a] = v[a], x[a]
        return v[a]
      else:
        v[a] = z3.BitVec(names[a], 16)
        conds.append(z3.And(v[a] >= z3.BitVecVal(32, 16), v[a] < z3.BitVecVal(128, 16)))
        reads[a] = v[a], x[a]
        return v[a]

    names.update(base_conds)
    print(len(reads))

    cntops = 0
    seenblk = defaultdict(lambda: 0)
    for b in node.chain:
      a0, a1, a2 = x[b:b + 3]

      v0 = get_var(a0)
      v1 = get_var(a1)
      v[a1] = v1 - v0

      cnd = v[a1] <= z3.BitVecVal(0, 16)

    print('reads')
    pprint.pprint(reads)
    print('writes')
    skeys = list(v.keys())
    skeys.sort()

    for k in skeys:
      #if not k in self.rundata.writepos: continue
      a = z3.simplify(v[k])
      if k in reads and prove(a == reads[k][0]): continue

      print(hex(k), a, z3.is_const(a), ix[k], x[k], k in self.rundata.writepos)
    klist = set(v.keys())
    klist.update(reads.keys())

    mp = {k: iid for iid, k in enumerate(klist)}
    fixed = set()

    mat = []
    N = len(mp)
    for i in range(N):
      mat.append([0] * N)

    def norm_term(a):
      a = a.strip()
      if a.startswith('var_'):
        return f'tb[{int(a[4:], 16)}]'
      return str(ctypes.c_int16(int(a)).value)


    funccode = []
    for k, iid in mp.items():
      if k in v: u = v[k]
      else: u = v[k]
      u = z3.simplify(u)
      if k in reads and prove(a == reads[k][0]):
        fixed.add(k)

      u = str(u)


      def tsf_expr(u):
        tx = []
        for term in u.split('+'):
          tx.append('*'.join([norm_term(e) for e in term.split('*')]))
        return '+'.join(tx)

      code = f'ntb[{k}] = ' + tsf_expr(u)
      funccode.append(code)

      print(k, hex(k), 'k >> >', u)

    print('FUN CCODE >> ', node.chain[0])
    print('\n'.join(funccode))

  def analyse_block0(self, b, x, v={}, names={}, conds=[], base_conds={}, depth=0, nconds=[]):
    if depth == 2: return
    depth += 1

    print('===============')
    print('===============')
    print('===============')
    print('===============')
    print('===============')
    print('===============')
    print('===============')
    print('===============')
    print('===============')
    conds.extend(nconds)
    branch0, branch1, v, conds, x = self.jit_block0(
        b, x, names=names, v=v, base_conds=base_conds, conds=conds
    )
    if flags.analyse_loop: return
    if branch0[0] is not None:
      self.analyse_block0(
          branch0[0], x, v=v, conds=conds, names=names, nconds=(branch0[1],), depth=depth
      )
    if branch1[0] is not None:
      self.analyse_block0(
          branch1[0], x, v=v, conds=conds, names=names, nconds=(branch1[1],), depth=depth
      )


def trace_turing(b, x):
  print('START ', b)
  rnd = 0

  tainted = set(flags.taint)
  if flags.taint_pwd:
    for i in range(pwd_start, pwd_end):
      tainted.add(i)

  stop_access = set([pwd_start + i for i in flags.stop_access])

  while True:
    rnd += 1
    if b + 3 > m1: break

    if rnd == flags.maxrounds:
      print('STOP max rounds')
      break

    if flags.shorten and b in disk_code.code_shorten:
      func = disk_code.code_shorten[b]
      cx = 0
      while True:
        nb = func(x)
        cx += 1
        if nb != b:
          print('LALALA', cx, nb)
          b = nb
          break
      continue

    else:
      va = x[b + 0]
      vb = x[b + 1]
      if flags.debug:
        print(b, 'args', va, vb, x[b+2], 'vals', x[va], x[vb], 'res', x[vb]-x[va])
      if flags.track_tainted:
        if va == vb and va in tainted:
          tainted.remove(va)
        if va in tainted or vb in tainted:
          tainted.add(vb)
      if va in stop_access or vb in stop_access:
        print('BREAKING ON ACCESSS ', va, vb, rnd)
        break

      if check_in(va) or check_in(vb):
        print('ACCESS AAAAgot on ', rnd, va-pwd_start, vb-pwd_start)
      a2 = x[b + 2]
      oldb = b
      b = do_step(b, x)

    if a2:
      print('CHECK ', oldb, b, rnd, a2, x[vb], vb)

    if b in flags.stopb: break
    if x[4]:
      print('OUTPUT ', x[2] & 0xff)
      break


  if flags.track_tainted:
    for e in tainted:
      print(hex(e), hex(x[e]))
  return b, x


def trace(ctx):
  b, x = pickle.load(open(ctx.pickle_start, 'rb'))
  set_init_pass(x)
  b, x = trace_turing(b, x)
  if flags.outfile:
    pickle.dump((b, x), open(flags.outfile, 'wb'))


def set_init_pass(x):
  if flags.initpass:
    for i, c in enumerate(flags.initpass.encode()):
      x[pwd_start + i] = c


def analyse_z3(ctx):
  fromstart = 0
  if fromstart:
    b, x = pickle.load(open('./turing_data/state.start', 'rb'))
  else:
    b, x = pickle.load(open(ctx.pickle_start, 'rb'))

  m1 = 0x2dad
  found = False
  blk = b
  b0 = b
  x0 = list(x)
  rnd = 0
  set_init_pass(x)

  names_pwd = dict()
  for i in range(pwd_start, pwd_end):
    names_pwd[i] = 'pass_%02x' % (i - pwd_start)

  ops = []
  if not fromstart:
    solver = Solver()

    #analyse_block(b, x, base_conds=names_pwd)
    if flags.mode1:
      if flags.startb:
        b = flags.startb
      for n in get_nodes()[0]:
        solver.jit_block(n, x, base_conds=names_pwd)
    else:
      solver.analyse_block0(b, x, base_conds=names_pwd)

  else:
    while True:
      rnd += 1
      if b + 3 > m1: break
      va = x[b + 0]
      vb = x[b + 1]
      ops.append((va, vb, x[b + 2]))
      if check_in(va) or check_in(vb):
        found = True

      b = do_step(b, x)
      if x[b + 2] != 0:
        if found:
          pickle.dump((b0, x0), open('./turing_data/real.char2.start', 'wb'))
          return

        ops = []
        blk = b
        b0 = b
        x0 = list(x)



NX = 0x10000
pwd_start, pwd_end = 0x1208 // 2, 0x1248 // 2
pwd_len = pwd_end - pwd_start
intervals.append((pwd_start, pwd_end))

d = get_data()

def ser_bx(ctx):
  assert ctx.outfile
  b, x = pickle.load(open(ctx.pickle_start, 'rb'))
  ser = bytearray(struct.pack('<65536H', *x))
  open(ctx.outfile, 'wb').write(ser)
  print('B>> >', b)


def analyse(ctx):
  b, x = pickle.load(open(ctx.pickle_start, 'rb'))
  realbranches = []
  fakebranches = []
  varbranches = []
  for branch in disk_code.branches:
    a0, a1, a2 = x[branch:branch+3]
    ii = disk_code.iblk_desc[branch]
    print(branch, ii, a0, a1, a2)
    if branch+2 in d.writepos:
      varbranches.append(ii)
      print('VARBRACH ', branch+2)

    elif branch in d.writepos or branch+1 in d.writepos or a0 != a1:
      realbranches.append(ii)
    else:
      fakebranches.append((branch, a2))

  print(realbranches)
  print(varbranches)
  print(fakebranches)

  return
  print(d.writepos.intersection(d.jumppos))
  a = 1608
  while True:
    if x[a+2]:
      print('JMP >> ', a, x[a+2])
      break
    else:
      a += 3


class ExecutionNode:
  def __init__(self, chain):
    self.chain = chain
    self.node_name = f'{chain[0]} - {chain[-1]}'
    self.nxt = []
    self.varbranch = 0


def get_nodes(edges, noforce=0):
  d = get_data()

  g = nx.DiGraph()
  g.add_edges_from(edges)
  nodes_cl = defaultdict(lambda: 0)
  START_NODE = 1
  END_NODE = 2
  varbranches = []

  for node in g:
    if g.in_degree(node) !=1 or node == 1604: nodes_cl[node] |= START_NODE
    is_end = 0
    if noforce==0 and node + 2 in d.writepos:
      is_end = 1
      varbranches.append(node)

    if is_end or g.out_degree(node) != 1:
      nodes_cl[node] |= END_NODE
      for nxt in g.neighbors(node):
        nodes_cl[nxt] |= START_NODE


  groupnodes = {}

  bignodes= []
  for node in g:
    if not (nodes_cl[node] & START_NODE): continue
    p = node
    lst =[]
    while True:
      if p!=node and (nodes_cl[p] & START_NODE): break

      lst.append(p)
      if (nodes_cl[p] & END_NODE): break
      assert g.out_degree(p) == 1
      p = next(g.neighbors(p))

    cur = ExecutionNode(lst)
    bignodes.append(cur)
    for e in lst: 
      assert e not in groupnodes
      if p in varbranches: cur.varbranch = 1
      groupnodes[e] = cur


  bigedges = []
  for n in bignodes:
    for nxt in g.neighbors(n.chain[-1]):
      nn = groupnodes[nxt]
      bigedges.append((n.node_name, nn.node_name))
      n.nxt.append(nn)

  bg = nx.DiGraph()
  bg.add_edges_from(bigedges)
  write_dot(bg, f"{flags.runid}_biggraph.dot")
  write_dot(g, f"{flags.runid}_graph.dot")
  return bignodes, varbranches
def translate_code(ctx):
  bignodes, varbranches = get_nodes(disk_code.edges)

  b, x = pickle.load(open(ctx.pickle_start, 'rb'))
  startpoints = defaultdict(lambda: 0)

  with open(flags.codefile, 'w') as codefile:
    print('''

void hook_disp(){

    if (tb[4]){
    printf("GOT CHAR >> %d %c\\n", tb[2]&0xff, tb[2]&0xff);
    tb[4] = 0;
    tb[2] = 0;
    }
}



''', file=codefile)
    for n in  bignodes:
      print(f'void* func_{n.chain[0]}();', file=codefile)

    print('void init(){', file=codefile)
    for n in  bignodes:
      print(f'func_data[{n.chain[0]}] = func_{n.chain[0]};', file=codefile)
    print('}', file=codefile)

    for n in  bignodes:
      ops = n.chain

      code = [f'void* func_{ops[0]}(){{']
      ll = []
      for op in ops:
        a0, a1, a2 = x[op:op+3]
        op0 = f'tb[{a0}]'
        op1 = f'tb[{a1}]'
        op2 = f'{a2}'

        if op +2 in d.writepos: op2 = f'tb[{op+2}]'

        if op in d.writepos: op0 = f'tb[tb[{op}]]'
        else:
          if a0 not in d.writepos:
            op0 = ctypes.c_int16(x[a0]).value
        if op+1 in d.writepos: op1 = f'tb[tb[{op+1}]]'
        if op0 == op1:
          code.append(f'{op1} = 0;')
        else:
          if op0 == 0: continue
          code.append(f'{op1} -= {op0};')
          assert code[-1] != 'tb[0] -= 0;', op0
        if op1 == 'tb[4]':
          code.append('hook_disp();')



      branch_op = f'func_{op2}'
      if n.varbranch:
        branch_op = f'get_func({op2})'
      elif a2 == 0:
        branch_op = f'func_{op+3}'

      assert len(n.nxt) <= 2
      nl =len(n.nxt) 
      if nl == 0:
        cond =f'''exit(1); return nullptr;'''
      elif nl == 1:
        cond = f'return (void*){branch_op};'
      else:
        cond = f'''
  if ((int16_t){op1} <= 0) return (void*){branch_op};
  else return (void*)func_{op+3};
  '''

      code.append(cond)
      for a in n.nxt:
        code.append(f'// NXT >>>  {a.chain[0]}')
      code.append('}')

      sx = '\n'.join(code)

      def tsf(pattern, repl, sx):
        while True:
          nsx=re.sub(pattern, repl, sx)
          if len(nsx) == len(sx): break
          sx = nsx
        return sx

      pattern0='''(?P<A>\S+) = 0;
(?P<B>\S+) = 0;
(?P=A) -= (?P<C>\S+);
(?P=B) -= (?P=A);
(?P=A) = 0;'''
      repl0 = '''\g<B> = \g<C>;
\g<A> = 0;'''

      pattern1='''(?P<A>\S+) = 0;
(?P=A) = 0;
(?P=A) -= (?P<C>\S+);
(?P<B>\S+) -= (?P=A);
(?P=A) = 0;'''
      repl1 = '''\g<B> += \g<C>;
\g<A> = 0;'''

      pattern2='''(?P=A) = (?P<C>\S+);
(?P=A) = (?P=C);'''
      repl2 = '''\g<A> += \g<C>;'''
      pr_list = []
      pr_list.append((pattern0, repl0))
      pr_list.append((pattern1, repl1))
      pr_list.append((pattern2, repl2))


      for pattern, repl in ((pattern0, repl0), (pattern1, repl1)):
        sx = tsf(pattern, repl, sx)

      print(sx, file=codefile)
    print(f'''
func_t entry_func(){{
return func_{b};
}}''', file=codefile)
    print('// ENTRY >> ', b, file=codefile)



def blk_analysis(ctx):
  start = -1
  done = set()
  def do_desc(x):
    if x in done: return
    done.add(x)
    print('Go ', x, disk_code.blk_desc.get(x, 'Done'), disk_code.next_desc.get(x,[]))
    for a in disk_code.next_desc.get(x, []):
      do_desc(a)


  do_desc(start)

def s16(a): return ctypes.c_int16(a)

def run_l2(x, stopb=[], toggle_conds=[], toggle_jumps = [], track_conds=[], mem_watch = [], overrides = {}, good=[], bad=[]):
  stop_access = set([pwd_start-2038 + i for i in flags.stop_access])
  if not stopb: stopb = flags.stopb
  np.seterr(all='ignore')
  ops = []
  readpos = []
  vals = defaultdict(lambda: set())
  xvals = []
  jumps = set()
  edges = set()
  #x[0] = np.int16(5307)
  if flags.startb: x[0] = flags.startb

  tc = {}
  for v in track_conds: tc[v] = defaultdict(list)
  mw = {}
  for v in mem_watch: mw[v] = defaultdict(list)
  conds = []

  curchar = -1

  first=1
  goodlist = set()
  while True:
    op = x[0]
    pos = x[op]
    if op in bad: return None
    if op in good: goodlist.add(op)

    if not first and pos in stop_access:
      print('stopping cause access ', pos)
      break
    if pwd_start <= pos+2038 <= pwd_end:
      cpos = pos+2038-pwd_start
      curchar = cpos
      print('READING ', cpos, op, x[pos])


    ops.append((op, pos, x[pos], x[1],np.int16(x[pos]-x[1])))
    readpos.append(pos)
    if not first and op in stopb: break
    first = 0

    if x[6] == 1:
      print('OUTPUT CHAR ', chr(x[4]))
      if flags.stop_at_output: break
      #return
      x[4] = 0
      x[6] = 0
    if pos <= -2: break
    if pos < 0:
      x[0] += 1
      edges.add((op, x[0]))
      continue


    r1 = x[pos]
    vals[pos].add(r1)
    r2 = x[1]
    diff = r1-r2
    if op == 8186:
      xvals.append(r1)
      print('VAL >> ', r1)
    if op == 8253:
      print('GOT DIFF ', diff, r1, r2, x[2887])
    if op in overrides:
      diff = overrides[op]
      r1=r2=0

    if op in track_conds:
      tc[op][curchar].append(diff)
    if pos in mem_watch:
      tmp = mw[pos][curchar]
      if diff != 0 and (len(tmp) == 0 or tmp[-1] != diff):
        tmp.append(np.uint16(diff))

    x[1] = np.int16(diff)
    if flags.debug: 
      print(op, pos, disk_code.l2_fixed.get(op, -1), r1, r2, diff)

    if pos == 2:
      x[3] = diff
    else:
      x[pos] = diff

    conds.append(op)
    if (r1 < r2) ^ (op in toggle_conds):
      x[0] += 1
    x[0] += 1
    if pos == 0:
      if op in toggle_jumps:
        x[0] = op + 1
      jumps.add((op, x[0]))
    edges.add((op, x[0]))

  ops_list = ops
  ops = set(ops)
  readpos = set(readpos)
  data = Attributize(ops=ops, readpos=readpos, vals=vals, jumps=jumps, edges=edges, x=x, op=op, conds=conds, ops_list = ops_list, tc=tc, mw=mw, goodlist=goodlist)
  print(xvals)
  return data

def is_ro(addr):
  return int(disk_code.l2_fixed.get(addr, 1))

class Operation:
  def __init__(self, addr, cx):
    self.cx = cx
    self.addr = addr
    self.typs = ('LOADX', 'NEGX', 'OP', 'JUMP', 'NOP', 'ZEROX', 'ZEROE')
    self.signed = 0
    self.typ = None
    self.op = None
    self.neg_op = False
    self.cond = False
    self.n = None

  def setup(self, typ, n, op=None, neg_op=False, cond=False, signed=0):
    self.signed = 'us'[signed]
    self.neg_op = neg_op
    self.typ = typ
    assert typ in self.typs
    self.n = n
    self.op = op
    self.cond = int(cond)
    return self


  def __repr__(self):
    prefix= f'{self.addr:05d}: '
    suffix = ''
    comment = ''

    if self.op is not None and  self.op > 2:
      comment = f' //   ro={is_ro(self.op)}, v={self.cx[self.op]}'

    if self.typ == 'LOADX':
      if self.neg_op:
        suffix = f'X_{self.signed} <= -tb[{self.op}]'
      else:
        suffix = f'X_{self.signed} <= tb[{self.op}]'

    elif self.typ == 'NEGX':
      suffix = 'X <= -X'
    elif self.typ == 'ZEROE':
      suffix = f'tb[{self.op}] <= 0'
    else:
      suffix = f'{self.typ} {self.op} (COND={int(self.cond)})'

    return prefix + suffix + comment

def optimize_ops(ops):
  ops = list(ops)

  while True:
    n = len(ops)

    for i in range(n-1):
      a = ops[i]
      b = ops[i+1]
      if a.typ == 'NEGX' and b.typ == 'NEGX':
        del ops[i]
        del ops[i]

      if a.typ == 'OP' and b.typ == 'NOP':
        a.cond = 0
        del ops[i+1]

      if a.typ == 'LOADX' and b.typ == 'OP' and a.op == b.op:
        ops[i].setup('ZEROE', a.n + b.n, op=a.op)
        del ops[i+1]
      if a.typ == 'NOP':
        del ops[i]

      if len(ops) != n: break

    if n == len(ops): break
  return ops




class L2Analyse:
  def __init__(self, x):
    self.x = x
    self.edges = set()
    self.seen = set()
    self.unresolved_jumps = []
    self.chains = []
    self.cx = list(self.x)

  def dfs_l2(self, op):
    if op in self.seen: return
    chain = []
    split_at = None

    while True:
      if op in self.seen: return
      self.seen.add(op)
      chain.append(op)
      if self.x[op] == 0: break
      if self.x[op+1] == 0:
        split_at = op
        break
      self.edges.add((op, op+1))
      op += 1
    self.chains.append(chain)


    print('GOT CHAIN ', chain)

    if split_at is not None:
      self.edges.add((op, op+2))
      self.dfs_l2(op+2)
    else: self.edges.add((op, op+1))


  def transpile(self, start):
    v1 = None


    def find_op(addr):
      op = Operation(addr, self.cx)
      a0, a1, a2, a3= self.cx[addr:addr+4]
      if a0 == 1 and a2 == 2 and a3 == 2:
        return op.setup('LOADX', 4, a1, neg_op=True, signed=1)

      if a0 == 1 and a2 == -1:
        return op.setup('LOADX', 3, a1, neg_op=False, signed=1)

      if a0 == 2 and a1 == -1:
        return op.setup('NEGX', 2)
      if a0 == 0:
        return op.setup('JUMP', 0)
      if a0 == -1:
        return  op.setup('NOP', 1)
      if a0 == 1:
        return  op.setup('ZEROX', 1)

      return op.setup('OP', 1, a0, cond=True)


    print()
    print()
    print()
    print()
    print('TRANSPILE ', start)
    lst = []
    addr =start
    ops = []
    while True:
      op=find_op(addr)
      ops.append(op)
      print('FUU ', op)
      if op.n == 0: break
      addr += op.n

    for i in range(start, addr):
      print(i, self.cx[i])

    print('END AT ', addr)
    ops = optimize_ops(ops)
    for op in ops:
      print(op)


def analyse_l2(ctx):
  b, x = pickle.load(open(ctx.pickle_start, 'rb'))
  x[pwd_start] = b'@'[0]
  x = x[2038:]
  x = list(map(np.int16, x))

  a = L2Analyse(x)
  a.edges.add((-1, x[0]))
  a.dfs_l2(x[0])
  for jump in disk_code.jumps:
    a.edges.add(jump)
    a.dfs_l2(jump[1])


  #a.transpile(5199)
  #a.transpile(5213)
  #a.transpile(5227)
  #a.transpile(3317)
  for addr in ctx.transpile_req:
    a.transpile(addr)

  #a.transpile(5307)
  #a.transpile(5325)
  #a.transpile(5371)
  #a.transpile(5387)
  #a.transpile(5394)
  #a.transpile(5410)
  print(x[5410])


def s16_tb(buf):
  x = []
  for i in range(0, len(buf), 2):
    x.append(struct.unpack('<H', buf[i:i + 2])[0])
  return x


def load_file(fil):
  buf = open(fil, 'rb').read()
  if flags.has_header:
    buf = buf[2038*2:]
  x = []
  for i in range(0, len(buf), 2):
    x.append(struct.unpack('<H', buf[i:i + 2])[0])
  x = list(map(np.int16, x))
  return x

def load_l2(pwd=None):
  if pwd is None and flags.initpass:
    pwd = flags.initpass.encode()
  if flags.infile:
    buf = open(flags.infile, 'rb').read()
    if flags.has_header:
      buf = buf[2038*2:]
    x = []
    for i in range(0, len(buf), 2):
      x.append(struct.unpack('<H', buf[i:i + 2])[0])
  else:
    b, x = pickle.load(open(flags.pickle_start, 'rb'))
    x = x[2038:]

  if pwd:
    for i, c in enumerate(pwd):
      if flags.signed_load:
        x[pwd_start-2038+i] = np.int8(c)
      else:
        x[pwd_start-2038+i] = np.uint8(c)

  x = list(map(np.int16, x))
  print('PWD IS ', x[pwd_start-2038:pwd_end-2038])
  return x

def solve_l2(ctx):
  #pwd = b'@\x00\x4e\x06\x43\x06'

  if flags.use_final:
    pwd = solve_pwd
    print(len(pwd))
    x = load_l2(pwd)
  else:
    x = load_l2()



  def findv(v):
    for i in range(9000):
      if x[i] == v:
        return i
    return None

  posdata = findv(0x1122 // 2 - 2 - 2038)
  posdata = findv(0x118e // 2 - 2 - 2038)
  posop=findv(posdata)
  print(posdata, posop)

  posdata = findv(0x1122 // 2 - 2 - 2038)
  posop=findv(posdata)
  print(posdata, posop)



  print(min(x))
  print(np.mean(x))
  overrides = {}
  #overrides = {8253:0}

  data = run_l2(x, overrides=overrides)
  tmp = list(data.readpos)
  tmp.sort()
  if flags.gen_graph: get_nodes(data.edges, 1)
  #5697 {b'@ aa'}
  #5691 {b'@ aa'}
  #5712 {b'@ aa'}
  #5704 {b'@ aa'}

  #5744 {b'@  aa'}
  #8220 {b'@  aa'}



  if flags.outfile:
    print(min(data.x))
    print(np.mean(data.x))
    print(type(data.x[0]))
    ser = bytearray(struct.pack(f'<{len(data.x)}h', *map(int, data.x)))
    assert len(ser) %2 == 0
    open(ctx.outfile, 'wb').write(ser)

  fixed = {}
  return
  for k, v in data.vals.items():
    fixed[k] = len(v) == 1
  print(fixed)

  print()
  print()
  print('JUMPS >> ', data.jumps)




def l2_analyse_loop1(ctx):
  loop1_branch = 5637
  loop1_end = 5638
  loop2_branch = 6256
  loop2_end = 6257


  passlist = []
  charset = list(map(ord, 'abcde'))
  for c in charset[:5]:
    passlist.append(f'{flags.initpass}{chr(c)}aa'.encode())

  if flags.passlist:
    passlist = list([a.encode() for a in flags.passlist])


  def analyse_to(to, count):

    res = {}
    for pwd in passlist:
      print('O PWD ', pwd)
      x = load_l2(pwd)
      t = []
      for i in range(count):
        r = run_l2(x, stopb=[to])
        x = r.x
        t.append(Attributize(x=list(x), ops=r.ops))
      res[pwd] = t
    return res

  def analyse(loop_branch, loop_end):

    res = {}
    for pwd in passlist:
      print('O PWD ', pwd)
      x = load_l2(pwd)
      t = []
      cnt  =0

      if 0:
        r = run_l2(x, stopb=[loop2_end])
        x = r.x
      print('FIRST LOOP END')
      for i in range(flags.analyse_count):
        while True:
          r = run_l2(x, stopb=[loop_branch, loop_end])
          cnt+=1
          x = r.x
          t.append(Attributize(x=list(map(np.uint16, x)), ops=r.ops))
          if r.op == loop_end: break
      res[pwd] = t
    return res

  if flags.analyse_to:
    res = analyse_to(flags.analyse_to, flags.analyse_count)
  else:
    if 0:
      res = analyse(loop1_branch, loop1_end)
    else:
      res = analyse(loop2_branch, loop2_end)
  print('HAVE ', len(res))
  data = list(res.items())
  restrict_entries = set([7926])
  restrict_entries = None
  for i in range(len(data)-1):
    print('DIFF AGAINST ', i)
    print()

    da = data[0][1]
    db = data[i+1][1]

    for j in range(len(da)):
      print()
      print(Display.diff_lists(da[j].x, db[j].x, restrict_entries=restrict_entries))

  return
  print('======== INTER DIFF')
  print('======== INTER DIFF')
  print('======== INTER DIFF')
  for e in res.values():
    print('========XXXXXXXXXXXx')
    print('========XXXXXXXXXXXx')
    print('========XXXXXXXXXXXx')
    print('========XXXXXXXXXXXx')
    for i in range(len(e)-1):
      print('DIFf for ', i)
      print(Display.diff_lists(e[i].x, e[i+1].x, restrict_entries=restrict_entries))

#  ops = defaultdict(lambda: set())
#  for pwd, e in res.items():
#    for a in e:
#      for u in a.ops:
#        ops[u[0]].add(pwd)
#
#  for k, v in ops.items():
#    if len(v) <= 10:
#      print(k, v)
#
#
  return





  if 1:
    a, b= res.values()
    print()
    print()
    print()
    print()

    for i in range(len(a)):
      print('SAME DIF DIFf for ', i)
      print(Display.diff_lists(a[i], b[i]))

def l2_explore_end(ctx):
  bad_end = 1452
  good_end = 1675
  ends = [bad_end, good_end]
  if 0:
    x = load_l2()
    r = run_l2(x, stopb=ends)
    for a in r.jumps:
      x = load_l2()
      try:
        res = run_l2(x, stopb=ends, toggle_jumps=[a[0]])
        print(res.op, a)
      except:
        pass
    return

  if 0:
    for a in r.conds:
      x = load_l2()
      res = run_l2(x, stopb=ends, toggle_conds=[a])
      print(res.op)
  for i in range(200):
    # OK IF 2922 == -105
    x = load_l2()
    x[2922] = -i
    res = run_l2(x, stopb=ends)
    print(i, res.op)


def l2_diff_exec(ctx):

  for pwd in flags.passlist:
    pwd = pwd.encode()
    x = load_l2(pwd)
    with open(f'./logs/trace_{pwd.decode()}', 'w') as f:
      for i in range(flags.analyse_count):
        r = run_l2(x, stopb=[flags.analyse_to])
        x = r.x
        for e in r.ops_list:
          print(e, file=f)

def l2_full_graph(ctx):
  x = load_l2(b'@')
  edges =  run_l2(x).edges

  x = load_l2(b'a')
  edges.update(run_l2(x).edges)
  get_nodes(edges)


def find_jumps(x):
  n = len(x)
  print(n)
  i = 0
  while i < n:

    if x[i] == 1 and x[i+1] == 1 and x[i+3] == 2 and x[i+4] == 2 and x[i+2]+1 == x[i+5]:
      for k in range(100):
        if x[i+k*6:i+(k+1)*6] != x[i:i+6]:
          break

      if k > 6:
        print('MAYBE JUMP ', i, k)
      i += 6 * k
    else:
      i += 1

def find_real_conds(x):
  n = len(x)
  print(n)
  i = 0
  while i < n:

    if x[i] == 1 and x[i+1] > 2 and x[i+2] == 1 and x[i+3] > 2 and x[i+4] == 1:
      print('MAYBE COND ', i, x[i:i+5])
      i += 5

    else:
      i += 1

def l2_analyse_patterns(ctx):
  x = load_l2(b'@')
  find_real_conds(x)

  a = list(set(x))
  n = len(x)
  a.sort()
  print(a)
  for i in range(n):
    if x[i] in flags.stop_access:
      print('HAVE V ', i, x[i])


def l2_track_conds(ctx):
  conds = [948,1196,2045,2293,3044,3379,3627,3924,4172,5013,5452,6071,6316,6592,6904,7152,7434,7682,8288,8536,8869,9117,]
  conds = [x+1 for x in conds]
  conds.append(8241)
  conds.append(8186)
  mem_watch = []
  mem_watch.append(7926)
  mem_watch.append(2681)
  x = load_l2()
  for i in range(20):
    print('GOTT ', struct.pack('<h', x[2681+i]))

  r = run_l2(x, track_conds =conds, stopb=[2095], mem_watch=mem_watch)

  for cond, dx in sorted(r.tc.items()):
    print(f'========= on cond {cond}')
    for curchar, vals in sorted(dx.items()):
      print(curchar, vals)

  for mw, dx in sorted(r.mw.items()):
    print(f'========= on MEM WATCH {mw}')
    for curchar, vals in sorted(dx.items()):
      print(curchar, vals)

def l2_decode(ctx):
  pass
  def compute(pwd):
    x = 8352
    for i in range(0, len(pwd), 2):
      c = pwd[i] + ((pwd[i+1]-0x20)<<7)
      for j in range(16):
        if c >> j & 1:
          x += 1
        x *= 2
        print(ctypes.c_int16(x).value)
      print(ctypes.c_int16(x).value)

  compute(flags.initpass.encode())


#  1 [1, 2, 4, 8, 16, 32, 64, 128, 129, 258, 516, 1032, 2064, 4128, 4129] A@
#  1 [1, 2, 4, 8, 16, 32, 64, 128, 129, 258, 516, 1032, 2064, 4128] @@
#  1 [1, 2, 4, 8, 16, 32, 33, 66, 132, 133, 266, 532, 1064, 2128, 4256] @A
#  1 [1, 2, 4, 8, 16, 17, 34, 68, 136, 137, 274, 548, 1096, 2192, 4384] @B
#
#
#
#
#3 [4128, 8256, 16512, -32512, 512, 513, 1026, 2052, 4104, 8208, 16416, 16417, -32702, 132, 264, 528, 1056, 2112, 4224, 4225] @A
#3 [4128, 8256, 16512, -32512, 512, 513, 1026, 2052, 4104, 8208, 8209, 16418, -32700, 136, 272, 544, 1088, 2176, 4352, 4353] @B
#
#
#3 [4128, 8256, 16512, -32512, 512, 513, 1026, 2052, 4104, 8208, 16416, -32704, 128, 256, 512, 1024, 2048, 4096, 4097] @@
#3 [4128, 8256, 16512, -32512, 512, 513, 1026, 2052, 4104, 8208, 16416, -32704, 128, 256, 512, 1024, 2048, 4096] A@
#3 [4128, 8256, 16512, -32512, 512, 513, 1026, 2052, 4104, 8208, 16416, -32704, 128, 256, 512, 1024, 2048, 2049, 4098, 4099] B@
#
#

#3 [8352, 16704, -32128, 1280, 1281, 2562, 5124, 10248, 20496, -24544, 16448, 16449, -32638, -32637, 262, 263, 526, 1052, 2104, 4208, 8416]
#1 [1, 2, 4, 8, 16, 32, 64, 65, 130, 260, 261, 522, 1044, 2088, 4176, 8352]
#  3 [8352, 16704, -32128, 1280, 1281, 2562, 5124, 10248, 20496, -24544, 16448, 16449, -32638, -32637, 262, 263, 526, 1052, 2104, 4208, 8416]
#  3 [8352, 16704, -32128, 1280, 1281, 2562, 5124, 10248, 20496, -24544, -24543, 16450, -32636, -32635, 266, 267, 534, 1068, 2136, 4272, 8544]

#  5 [8416, 16832, -31872, 1792, 1793, 3586, 7172, 14344, 28688, -8160, -16320, -16319, -32638, 260, 520, 1040, 2080, 4160, 4161, 8322, 8323]
#  7 [8323, 16646, -32244, 1048, 1049, 2098, 4196, 8392, 16784, -31968, 1600, 1601, 3202, 6404, 6405, 12810, 25620, -14296, -28592, -28591, 8354]



def l2_run_multiple(ctx):
  passlist = []
  #for c in charset:
  for c in range(256):
    passlist.append(f'{flags.initpass}{chr(c)}aa'.encode())

  if flags.passlist:
    passlist = list([a.encode() for a in flags.passlist])

  if 0:
    good = [8782]
    bad = [8773]
    res = {}
    for pwd in passlist:
      x = load_l2(pwd)
      r = run_l2(x, good=good, bad=bad)
      if r is None or len(r.goodlist) ==0: continue
      print('O PWD ', pwd)
  else:

    mw = [7926]
    res = {}
    
    #for pwd in flags.passlist:
    for i in range(8):
      pwd = flags.initpass.encode()
      pwd = bytearray(pwd)
      pwd[6] = 1<<i
      pwd
      x = load_l2(pwd)
      #stopb = 4964
      #r = run_l2(x, stopb=[stopb], mem_watch=mw)
      #if r.op == stopb:
      #  print('MIGHT FOR', pwd)

      r = run_l2(x, mem_watch=mw)
      res[bytes(pwd)] = r.mw

    for k, v in res.items():
      print(f'{v[7926][7][-1]:016b} {k}')


def maybe_final(ctx):
  #r = gen1(b'@fuckoffmate')


  import glob
  for f in glob.glob('./turing_data/test_*.out'):
    data = open(f, 'rb').read()
    base = (2038 + 2681)*2
    print(data[base:base+20])
  return


  if flags.use_final:
    r = gen1(solve_pwd)
  else:
    #r = gen1(flags.initpass.encode())
    r = gen1(b'@' + b'a'*29)
  #offset 0x1208
  open(f'./turing_data/final.out', 'wb').write(r)

def l2_list_ops():
  ops = set()
  edges = set()

  x = load_l2(solve_pwd)
  r = run_l2(x)
  edges.update(r.edges)
  ops.update(r.ops)
  x = load_l2(b'@aaaaaaa')
  r = run_l2(x)
  edges.update(r.edges)
  ops.update(r.ops)
  x = load_l2(b'jambonkpaa')
  r = run_l2(x)
  edges.update(r.edges)
  ops.update(r.ops)
  for op,pos, a1,a2,res in sorted(ops):
    print(f'OP={op} POS={pos} a1={a1} a2={a2} res={res}')
  if flags.gen_graph:
    nedges = set()
    for a, b in edges:
      if b == a+2:
        nedges.add((a&-2,a+1&-2))
        nedges.add((a+1&-2,a+2&-2))
      else:
        nedges.add((a&-2,b&-2))
    edges =set()
    for a, b in nedges:
      if a!=b: edges.add((a,b))
    get_nodes(edges, 1)



def l2_test(ctx):
  x = load_l2()
  for i in range(20):
    v = 0x10000+x[2681+i]
    print(chr(v>>9))

  return
  if 1:
    l2_list_ops()
    return

  if 0:
    ass=open('./dump.turing3.mem', 'rb').read()
    bs=open('./dump.turing4.mem', 'rb').read()
    a = ass[:20000]
    a=s16_tb(ass[2038*2:])
    b=s16_tb(bs[2038*2:])

    ass = ass[2038*2:]
    #for f in glob.glob('./suspicious_floppy_v1.0.img'):
    for f in glob.glob('./alldata/img/TMP.DAT'):
      x = open(f, 'rb').read()
      print(f, x.find(ass[:100]))
    return
  
    for i in range(len(a)):
      if a[i]!=b[i]:
        print(i, a[i], b[i])
    return

  else:
    #dd = open('./suspicious_floppy_v1.0.img', 'rb').read()
    #print(hex(dd.find(b'Enter the password')))
    #return
    x = load_l2()
    #print(x[2681:2700])

    x = x[:10000]
    for i in range(len(x)-20):
      for j in range(20):
        if x[i+j]>=0: break
      else: print('MIGHT AT ', i)
      if x[i] in (2709, 2715, 2721, 2760, 2832, 9489, 0x29e//2, 0x210 // 2, 339):
        print(i, x[i])
    return
    #x[1463] = 155
    #overrides = {9118:0}
    overrides = {}
    x[2936] = -1
    r = run_l2(x, overrides=overrides)

def l2_diff_mems(ctx):
  for i in range(1, len(ctx.infiles)):
    a = load_file(ctx.infiles[i])
    b = load_file(ctx.infiles[0])
    print(Display.diff_lists(a, b))
    


def l2_final(ctx):
  x= load_l2()
  want = x[2681:2701]
  print(want)
  #a@aaaxyzjambonkapalala

  nc = 30

  def decode(nwant):
    res = list()
    for i in range(nc//2):
      v = nwant[i] ^ (33*i)
      res.append((v&0x7f)+0x20)
      res.append((v>>7)+0x20)
    return res

  print(bytes(decode([4161, 8416, 11267, 11578, 8270, 8680, 10121, 8236, 8664, 8677, 8582, 11181, 11097, 11128, 11035])))
  #return


  for pos in range(30):
    for sum in range(pos*128):
      nwant = [np.uint16(a - np.int16(0xffff&0xc00*pos+sum)) for a in want]

      res = decode(nwant)
      if res[pos] != 64: continue
      s = 0
      for j in range(pos): s += res[j]
      #if s!=sum: continue
      for v in res:
        if not curses.ascii.isprint(v): break
      else:
        #if s!=sum: continue
        print(bytes(res))



app()
#writemem "dump.test.mem" 0 0x2000000
#writemem "dump.turing4.mem" 0x97c0:0x223 0x30000
