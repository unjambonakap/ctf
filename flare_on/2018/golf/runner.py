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
from chdrft.emu.trace import TraceEvent, WatchedMem, WatchedRegs
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

charset = [i for i in range(128) if curses.ascii.isprint(i)]

global flags, cache
flags = None
cache = None

code_desc='''
ctx_t: {
  fields: [
    {name: r15, type: u64},
    {name: r14, type: u64},
    {name: r13, type: u64},
    {name: r12, type: u64},
    {name: r11, type: u64},
    {name: r10, type: u64},
    {name: r9, type: u64},
    {name: r8, type: u64},
    {name: rdi, type: u64},
    {name: rsi, type: u64},
    {name: rbp, type: u64},
    {name: rsp, type: u64},
    {name: rbx, type: u64},
    {name: rdx, type: u64},
    {name: rcx, type: u64},
    {name: rax, type: u64},
    {name: s1, type: u64},
    {name: data, type: u64},
  ]
}

s0_t: {
  fields: [
    {name: 'ctx', type: ctx_t*},
    {name: 'guest_rflags', type: u64},
    {name: 'guest_rip', type: u64},
  ]
}

'''

def get_code():
  g_code = Structures.YamlStructBuilder()
  g_code.add_yaml(code_desc)
  g_code.build()
  return g_code

def args(parser):
  clist = CmdsList().add(test_uc)
  ActionHandler.Prepare(parser, clist.lst)
  parser.add_argument('--binary')
  parser.add_argument('--base', type=int, default=0x100000)


def load_kern(ctx):
  code_low = 1
  code_high = 0
  stack_low = 1
  stack_high = 0
  log_file = '/tmp/info.out_{}'.format(ctx.runid)
  kern, elf = kernel.Kernel.LoadFrom(pe=ctx.binary, arch=guess_arch('x64'), base=ctx.base)

  #kern.mu.hook_add(uc.UC_ERR_WRITE_PROT, kernel.safe_hook(kern.hook_bad_mem_access), None, 0, 2**32-1)
  kern.mu.hook_add(uc.UC_HOOK_MEM_WRITE_UNMAPPED | uc.UC_HOOK_MEM_FETCH_UNMAPPED,
                   kernel.safe_hook(kern.hook_unmapped))
  #kern.mu.hook_add(uc.UC_HOOK_CODE, kernel.safe_hook(kern.hook_code), None, code_low, code_high)

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
    self.cur_buf = None
    self.code = get_code()


    self.bufsz = 0x1000
    self.buf = self.kern.heap.alloc(self.bufsz)

    self.check0_addr = flags.base+0x40c3
    self.check3_addr = flags.base+0x38d7
    self.check2_addr = flags.base+0x3c2a
    self.check1_addr = flags.base+0x3e62
    self.checks = [self.check0_addr, self.check1_addr, self.check2_addr, self.check3_addr]
    self.vmop_func = flags.base+0x23ac
    self.hook_addr(flags.base+0x427f)

    self.handler = self.handle()

    self.init_vm()
    self.vmread_addr=flags.base+0x2FC0
    self.vmwrite_addr=flags.base+0x2FCC
    self.compare_addr = flags.base +0x1574
    self.hook_addr(self.vmread_addr, self.vmread_hook)
    self.hook_addr(self.vmwrite_addr, self.vmwrite_hook)
    self.hook_addr(self.compare_addr, self.compare_hook)
    self.vmcs = {}
    self.compares = []
  def compare_hook(self, *args):
    self.compares.append((self.regs.rcx, self.regs.rdx))
    #self.regs.rcx = self.regs.rdx

  def vmread_hook(self, *args):
    wx = self.regs.rcx
    self.kern.mc.ret_func()

  def vmwrite_hook(self, *args):
    wx = self.regs.rcx
    vx = self.regs.rdx
    self.vmcs[wx] = vx
    self.kern.mc.ret_func()



  def hook_addr(self, addr, handler=None):
    if handler is None: handler = self
    self.kern.mu.hook_add(uc.UC_HOOK_CODE, kernel.safe_hook(handler), None, addr, addr + 1)

  def failure_hook(self, *args):
    print('ON FAILURE')
    self.kern.stop()

  def call_check(self, ptr):
    self.mem.bzero(self.buf, self.bufsz)
    self.regs.rdi = self.buf
    self.regs.r15 = self.bufsz
    self.regs.rip = ptr

  def retrieve_checks(self):
    mc = self.kern.arch.mc
    data= []
    for i, ptr in enumerate(self.checks):
      self.call_check(ptr)
      yield
      content = self.mem.read(self.buf, self.bufsz)
      data.append(content)
      print(content[:30])
    self.content = data


  def __call__(self, *args, **kwargs):
    next(self.handler)

  def init_vm(self):
    self.ins_pad = self.kern.heap.alloc(0x4000)
    self.pass_pad = self.kern.heap.alloc(0x30)
    self.s0_pad = self.kern.heap.alloc(0x50)
    self.s1_pad = self.kern.heap.alloc(0xa0)
    self.s0 = Structures.Structure(self.code.typs.s0_t.make_ptr())
    self.s0.set_alloc_backend(self.kern.heap)
    self.p0 = self.s0.get_pointee()[0]
    self.kern.stack.push(bytearray([0]*0x100))
    self.pctx = self.p0.ctx.get_pointee()[0]

    #print(pointee.backend.buf)
    #print(pointee[0].guest_rip.backend.buf)
    #pointee[0].guest_rip.smart_set(0x123)
    #print(pointee[0].pretty_str())
    #print(pointee[0].raw)
    pass

  def handle(self):
    for _ in  self.retrieve_checks():
      yield


    self.kern.stack.push(self.kern.ret_hook_addr)
    cur_rsp = self.regs.rsp
    vmcs_GUEST_RSP = 0x681c
    vmcs_GUEST_RIP = 0x681e
    vmcs_GUEST_RFLAGS = 0x6820
    csp0 = cur_rsp + 8

    password = bytearray(b'a'*24)
    bc=ord('a')
    password = bytearray(range(bc, bc+24))
    self.kern.arch.call_data.set_active('win')

    found=b'We4r_ur_v1s0r_w1th_'
    password[0:len(found)] = found
    print('PASSPWD >> ', hex(self.pass_pad))

    #sumx = 0x16b
    #5: 0x46

    #5-6: 0xa0
    #6-7: 0x86
    #8: 0x33

    
    v = [0]*5
    v[0] = 0x46
    v[4] = 0x33
    v[1] = 0x16b-v[0]-v[4]-0x86
    v[2] = 0xa0 - v[1]
    v[3] = 0x86 - v[2]
    v = bytearray(v)
    password[-len(v):] = v
    print(found + bytearray(v))
    print(bytes(v))
    print(password)
    print(binascii.hexlify(v))
    self.mem.write(self.pass_pad, password)
    abc
    #We4r_ur_v1s0r_w1th_Fl4R3



    self.rval = defaultdict(list)
    cx = 0
    def r2val_hook(*args):
      self.rval[cx].append((self.regs.cl, self.regs.dl))
      self.regs.rcx = self.regs.rdx

    self.xorv = []
    def xorv_hook(*args):
      if cx == 2: self.xorv.append(self.regs.dl)


    self.hook_addr(flags.base + 0x184a, r2val_hook)
    self.hook_addr(flags.base + 0x2335, xorv_hook)

    offsets = [0, 5, 14, 19]

    for cx in range(len(offsets)):
      if cx >= 4: continue
      if cx == 3:
        self.kern.mu.hook_add(uc.UC_HOOK_CODE, kernel.safe_hook(self.kern.hook_code), None, 1, 0)
        self.kern.ignore_mem_access = False
        self.kern.mu.hook_add(uc.UC_HOOK_MEM_READ | uc.UC_HOOK_MEM_WRITE,
                        kernel.safe_hook(self.kern.hook_mem_access), None, 1, 0)

        self.kern.tracer.ignore_unwatched = True
        self.kern.tracer.watched.append(WatchedRegs('regs', self.regs, cmisc.to_list('rip rcx rdx rsp')))
        self.kern.tracer.watched.append(WatchedMem('stack', self.mem, cur_rsp-0x100, n=0x200, sz=1))


      self.mem.write(self.ins_pad, self.content[cx])
      print('on ITER >> ', cx, self.content[cx][:10])
      self.pctx.rcx.set(self.pass_pad + offsets[cx])
      cur_ip = self.ins_pad
      self.vmcs[vmcs_GUEST_RSP] = cur_rsp
      self.vmcs[vmcs_GUEST_RIP] = cur_ip
      self.vmcs[vmcs_GUEST_RFLAGS] = 0
      while True:
        self.pctx.rsp.set(cur_rsp)
        self.p0.guest_rip.smart_set(cur_ip)
        self.p0.guest_rflags.smart_set(self.vmcs[vmcs_GUEST_RFLAGS])
        payload = self.mem.read(cur_ip, 1)
        if payload[0] == 1: break

        self.kern.tracer.start_vm_op()
        yield self.kern.mc(self.vmop_func, self.s0.get())
        cur_rsp = self.vmcs[vmcs_GUEST_RSP]
        cur_ip = self.vmcs[vmcs_GUEST_RIP]
        self.kern.tracer.end_vm_op()
        print(self.vmcs)
        print('RAX > ', self.pctx.rax.get())
      res = bytearray(b'.'*24)
      if cx == 0:
        #for a, b in self.compares:
        #  res[a-bc] = b
        pass
      print(self.rval[cx])

      #if cx == 1:
      #  r2v = 0x75
      #  for a, b in self.rval[cx]:
      #    a ^= r2v
      #    b ^= r2v
      #    res[a-bc] = b

      #if cx == 2:
      #  print(self.xorv)
      #  r2v = 0x52
      #  for i, (a, b) in enumerate(self.rval[cx]):
      #    a ^= r2v ^ self.xorv[i]
      #    b ^= r2v ^ self.xorv[i]
      #    print('READ ', hex(a), hex(b))
      #    res[a-bc] = b

      print(res)






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

def test_uc(ctx):
  kern, elf = load_kern(ctx)
  kern.tracer.diff_mode = False
  event_log = open('/tmp/evens_{}.out'.format(ctx.runid), 'w')
  vmop_log = open('/tmp/vmop_{}.out'.format(ctx.runid), 'w')
  kern.tracer.cb = lambda x: event_handle(x, event_log, vmop_log)

  solver = UCSolver(kern)
  global charset
  kern.ignore_mem_access = True

  kern.mem.write(kern.ret_hook_addr, kern.arch.mc.nop)
  kern.forward_ret_hook  = solver
  kern.regs.ins_pointer = kern.ret_hook_addr

  try:
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
