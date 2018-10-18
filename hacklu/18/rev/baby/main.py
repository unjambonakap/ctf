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
import unicorn.x86_const as ucx86
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
from chdrft.dbg.gdbdebugger import GdbDebugger, launch_gdb
from concurrent.futures import wait
import tempfile
import re
import multiprocessing
import pprint
from collections import OrderedDict
import pickle

charset = [i for i in range(128) if curses.ascii.isprint(i)]

global flags, cache
flags = None
cache = None

flag='alag{Yay_if_th1s_is_yer_f1rst_gnisrever_flag!}'

def args(parser):
  clist = CmdsList().add(test)
  ActionHandler.Prepare(parser, clist.lst)


def load_kern(ctx):
  code_low = 1
  code_high = 0
  stack_low = 1
  stack_high = 0
  kern, elf = kernel.Kernel.LoadFrom(elf='./public/chall', arch=guess_arch('x86_64'))

  #kern.mu.hook_add(uc.UC_ERR_WRITE_PROT, kernel.safe_hook(kern.hook_bad_mem_access), None, 0, 2**32-1)
  kern.mu.hook_add(
      uc.UC_HOOK_MEM_WRITE_UNMAPPED | uc.UC_HOOK_MEM_FETCH_UNMAPPED,
      kernel.safe_hook(kern.hook_unmapped)
  )
  kern.mu.hook_add(uc.UC_HOOK_INSN, kernel.safe_hook(kern.hook_syscall), None, 1, 0, ucx86.UC_X86_INS_SYSCALL)
  kern.mu.hook_add(uc.UC_HOOK_CODE, kernel.safe_hook(kern.hook_code), None, code_low, code_high)
  kern.mu.hook_add(
      uc.UC_HOOK_MEM_READ | uc.UC_HOOK_MEM_WRITE, kernel.safe_hook(kern.hook_mem_access), None, 1, 0
  )
  kern.tracer.ignore_unwatched = True
  #kern.tracer.watched.append(WatchedRegs('regs', regs, cmisc.to_list('rip rcx rdx rsp')))
  #kern.tracer.watched.append(WatchedMem('all', kern.mem, 0, n=2**32, sz=1))

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
    self.kern.syscall_handlers['write'] = self.write_handler
    self.kern.syscall_handlers['read'] = self.read_handler

  def hook_addr(self, addr, handler=None):
    if handler is None: handler = self
    self.kern.mu.hook_add(uc.UC_HOOK_CODE, kernel.safe_hook(handler), None, addr, addr + 1)

  def write_handler(self, data):
    print(data.raw_args)
    print('WRITE HANDLER', self.mem.read(data.raw_args[1], data.raw_args[2]))
    self.regs.rax = data.raw_args[2]

  def read_handler(self, data):
    print('READ HANDLER ', data.raw_args)
    self.mem.write(data.raw_args[1], flag.encode())
    #self.kern.stop()

    self.regs.rax = len(flag)

  def failure_hook(self, *args):
    print('ON FAILURE')
    self.kern.stop()


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
  print('main')
  kern, elf = load_kern(ctx)
  kern.tracer.diff_mode = False
  event_log = open('/tmp/evens_{}.out'.format(ctx.runid), 'w')
  vmop_log = open('/tmp/vmop_{}.out'.format(ctx.runid), 'w')
  kern.tracer.cb = lambda x: event_handle(x, event_log, vmop_log)

  solver = UCSolver(kern)
  kern.ignore_mem_access = False

  tb = kern.mem.read(0x40010c, 0x2e)
  for i in range(128):
    ans = bytearray([i])
    for j in range(0x2e):
      ans.append(ans[-1] ^ tb[j])
    print(ans)

#flag{Yay_if_th1s_is_yer_f1rst_gnisrever_flag!}

  try:
    print('starting')
    kern.start()
  except uc.UcError as e:
    print('%s' % e)
    tb.print_exc()

  #print(kern.mem.read(output_addr, 20))
  return

def main():
  g_data.set_m32(False)
  ctx = Attributize()
  ActionHandler.Run(ctx)
app()

