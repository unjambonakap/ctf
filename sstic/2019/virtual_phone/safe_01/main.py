#!/usr/bin/env python

from chdrft.cmds import CmdsList
from chdrft.main import app
from chdrft.utils.cmdify import ActionHandler
from chdrft.utils.misc import Attributize
import chdrft.utils.misc as cmisc
import glog
import chdrft.utils.Z as Z
from chdrft.cmds import CmdsList
from chdrft.main import app
from chdrft.utils.cmdify import ActionHandler
from chdrft.utils.misc import Attributize
import chdrft.utils.misc as cmisc
import glog
import numpy as np
from chdrft.emu.binary import arch_data, Arch
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
import networkx as nx
import numpy as np
import pygraphviz
from networkx.drawing.nx_agraph import write_dot
import glob
from chdrft.utils.proc import MemoryRegions, MemoryRegionPermission
from chdrft.emu.base import snapshot_mem, seg_mem_from_snapshot, StreamRW
from chdrft.graph.base import UnionJoinLax
import llvmlite.ir as ll
import llvmlite.binding as llvm
import angr
import logging
import claripy

global flags, cache
flags = None
cache = None


def fmt_c_val(x):
  return hex(x) + 'ull'
def fmt_v(x):
  return f'{x:016x}'

dwarf_start = 0x400258
dwarf_read_start = 0x400600
dwarf_read_end = 0x400b00
dwarf_read_rg = Z.Range1D(dwarf_read_start, dwarf_read_end)
WIN_PC = 0x5e
FAIL_PC = 0x6a
g_dwarf_ir_stop_pc = 0x76
g_mainfunc_name = 'mainfunc'

g_dwarf_ir_file = './dwarf.state.ir.pickle'
g_dwarf_file = './dwarf.state.pickle'


def args(parser):
  clist = CmdsList().add(test)
  parser.add_argument('--pid')
  parser.add_argument('--core')
  parser.add_argument('--elf-outfile')
  parser.add_argument('--infile')
  parser.add_argument('--angr-size', type=int)
  parser.add_argument('--c-outfile')
  parser.add_argument('--maps')
  parser.add_argument('--data')
  parser.add_argument('--pc-src', type=cmisc.to_int)
  parser.add_argument('--pc-dest', type=cmisc.to_int)
  parser.add_argument('--dwarf-file')
  parser.add_argument('--out-dwarf-file')
  parser.add_argument('--dump_dwarf', action='store_true')
  parser.add_argument('--hook-all', action='store_true')
  parser.add_argument('--fixed-sp', action='store_true')
  parser.add_argument('--stop-before', action='store_true')
  parser.add_argument('--run-ir', action='store_true')
  parser.add_argument('--debug', action='store_true')
  parser.add_argument('--debug-tgt', action='store_true')
  parser.add_argument('--tgt-run-all', action='store_true')
  parser.add_argument('--tgt-hit-count', type=int, default=1)
  parser.add_argument('--tgt-repeat', type=int, default=1)
  parser.add_argument('--prepare-dwarf-ir', action='store_true')
  parser.add_argument('--pc-debug', type=cmisc.to_int, nargs='*', default=[])
  parser.add_argument('--tgt-spec', type=str)
  ActionHandler.Prepare(parser, clist.lst, global_action=1)


def load_kern(ctx):
  code_low = 1
  code_high = 0
  stack_low = 1
  stack_high = 0
  log_file = '/tmp/info.out_{}'.format(ctx.runid)
  kern, elf = kernel.Kernel.LoadFrom(elf=ctx.core, core=True)

  #kern.mu.hook_add(uc.UC_ERR_WRITE_PROT, kernel.safe_hook(kern.hook_bad_mem_access), None, 0, 2**32-1)
  kern.mu.hook_add(
      uc.UC_HOOK_MEM_WRITE_UNMAPPED | uc.UC_HOOK_MEM_FETCH_UNMAPPED,
      kernel.safe_hook(kern.hook_unmapped)
  )

  if flags.hook_all:
    kern.mu.hook_add(uc.UC_HOOK_CODE, kernel.safe_hook(kern.hook_code), None, code_low, code_high)
    kern.mu.hook_add(
        uc.UC_HOOK_MEM_READ | uc.UC_HOOK_MEM_WRITE, kernel.safe_hook(kern.hook_mem_access), None, 1,
        0
    )

    #kern.tracer.watched.append(WatchedRegs('regs', regs, cmisc.to_list('rip rcx rdx rsp')))
    kern.tracer.watched.append(WatchedMem('dwarf_stack', kern.mem, 0, n=2**32, sz=1))
  kern.tracer.ignore_unwatched = True

  return kern, elf


class KernelRunner:

  def __init__(self, kern):
    self.kern = kern

  def __call__(self, stop_pc):
    pass


class UCSolver:

  def __init__(self, kern):
    self.kern = kern
    self.regs = kern.regs
    self.mem = kern.mem
    self.stack = kern.stack
    self.handler = self.handle()
    self.kern.notify_hook_code = self.notify_hook_code
    self.flag_addr = None

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

  def snapshot_mem(self):
    segs = []
    for addr, sz, _ in self.kern.maps:
      segs.append(Z.Range1D(addr, n=sz))
    return snapshot_mem(self.mem, segs)

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

  def puts(self, *args, **kwargs):
    print(self.regs)
    print(self.mem.get_str(self.regs.x0))
    self.kern.stop()
    assert 0

  def stack_op(self, *args, **kwargs):
    d_stack_pos = self.regs.x19
    d_stack_addr = self.regs.x26

    op = self.regs.w7
    op_pos = self.regs.x0
    op_offset = op_pos - dwarf_start
    if flags.dump_dwarf and op_offset == 1:
      mem_snapshot = self.snapshot_mem()
      stack = self.mem.read_nu64(d_stack_addr, 64)
      dump_obj = cmisc.Attr(
          flag_addr=self.flag_addr, mem_snapshot=mem_snapshot, stack=stack, stack_pos=d_stack_pos
      )
      Z.pickle.dump(dump_obj, open(g_dwarf_file, 'wb'))

      assert 0

    if not app.flags.hook_all:
      self.kern.tracer.start_vm_op(f'dwarf_PC={op_offset:x}')
    #print(Display.mem_summary(self.mem, d_stack_addr, 64, word_size=8, istart=0))
    #print()

  def execute_stack_entry(self, *args, **kwargs):
    print('EXECUTE STACK')
    print(self.regs.x0)
    print(self.regs.x1)
    buf = self.mem.read(self.regs.x0, self.regs.x1 - self.regs.x0)
    print(Display.mem_summary(self.mem, self.regs.sp, 100, word_size=8, istart=-1))
    print(buf.hex())
    d_stack_addr = self.regs.x26
    print(self.regs.reg_list())

    self.kern.tracer.watched.append(WatchedRegs('regs', self.regs, cmisc.to_list('x19 w7 x0')))
    self.kern.tracer.watched.append(WatchedMem('all', self.mem, d_stack_addr, n=64, sz=8))

    print(self.kern.context_str())

  def get_cfa(self, mu, address, size, _2):
    self.kern.handle_ins_log(address, size)

  def hook_intr(self, intno, addr):
    pass

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

    #0xffffbf57fde4


class MemContent:

  def __init__(self):
    self.data = Z.Intervals(use_range_data=True, merge=0)
    self.elf_by_name = None

  def get_info(self, addr):
    q = self.data.query_data_raw(addr)
    if q is None: return ''
    info = f'file={q.region.file}'
    sym = q.elf.find_symbol_by_addr(addr)
    if sym is not None:
      info += f' sym={sym[0]}+{sym[1]}'
    return info


def maybe_add_maps(kern):
  mc = MemContent()

  regions = MemoryRegions()
  regions.build_from_maps(open(flags.maps, 'r').read())
  elf_by_name = {}
  for region in regions.regions:

    if 'r' not in str(region.perms): continue
    fname = os.path.basename(region.file)
    if not fname: continue
    fname = os.path.join('./deps', fname)

    if not os.path.exists(fname):
      print('skipping ', region)
      continue
    if fname not in elf_by_name:
      elf_by_name[fname] = ElfUtils(fname, offset=region.start_addr - region.offset)
    print('Adding mapped region ', hex(region.start_addr), region.size, fname, hex(region.offset))
    mc.data.add(
        region.start_addr,
        n=region.size,
        is_int=1,
        data=cmisc.Attr(elf=elf_by_name[fname], region=region)
    )

    for mp in kern.maps:
      if region.start_addr <= mp[0] < region.end_addr:
        break
    else:

      content = open(fname, 'rb').read()[region.offset:region.offset + region.size]
      flag_mp = [
          (MemoryRegionPermission.X, uc.UC_PROT_EXEC),
          (MemoryRegionPermission.R, uc.UC_PROT_READ),
          (MemoryRegionPermission.W, uc.UC_PROT_WRITE),
      ]
      flag_mem = 0
      for k, v in flag_mp:
        if region.perms.perm & k: flag_mem |= v

      kern.mem_map(region.start_addr, region.size, flag_mem)
      kern.mu.mem_write(region.start_addr, content)

  mc.elf_by_name = elf_by_name
  kern.mem_content = mc


def test(ctx):
  kern, elf = load_kern(ctx)
  kern.tracer.diff_mode = False
  event_log = open('/tmp/evens_{}.out'.format(ctx.runid), 'w')
  vmop_log = open('/tmp/vmop_{}.out'.format(ctx.runid), 'w')
  kern.tracer.cb = lambda x: event_handle(x, event_log, vmop_log)

  solver = UCSolver(kern)
  solver.flag_addr = kern.regs.x0
  kern.ignore_mem_access = False
  print(hex(kern.regs.pc))
  print(hex(kern.regs.sp))
  print(hex(kern.regs.x0))
  print(hex(kern.regs.q0))
  print(hex(kern.regs.q1))
  print(kern.mem.get_str(kern.regs.x0, n=10))
  print(hex(kern.regs.cpacr_el1))
  kern.regs.cpacr_el1 |= 0x300000
  print(hex(kern.regs.cpacr_el1))
  kern.regs.tpidr_el0 = 0xffffbf6f8b30
  maybe_add_maps(kern)

  solver.hook_addr(0x0000ffffbf413ccc, solver.failure_hook)
  #solver.hook_addr(0xffffbf6e3f38,solver.failure_hook)
  puts_addr = 0xffffbf3b4330
  solver.hook_addr(puts_addr, solver.puts)
  if ctx.data is not None:
    kern.mem.write(kern.regs.x0, ctx.data.encode() + b'\x00')

  get_cfa_addr = 0xffffbf4b2de4
  solver.hook_addr(get_cfa_addr, solver.get_cfa)

  execute_stack_op_off = 0xb8F0
  libgcc = kern.mem_content.elf_by_name['./deps/libgcc_s.so.1']

  find_fde_addr = libgcc.get_dyn_symbol('_Unwind_Find_FDE')

  execute_stack_addr = execute_stack_op_off + libgcc.offset

  vm_op_addr = 0xffffbf4b3c58
  #solver.hook_addr(vm_op_addr, kern.hook_code)
  solver.hook_addr(execute_stack_addr, solver.execute_stack_entry)
  stack_op_addr = 0xB92C + libgcc.offset
  solver.hook_addr(stack_op_addr, solver.stack_op)
  try:
    kern.start()
  except uc.UcError as e:
    print('%s' % e)
    tb.print_exc()


def test_maps(ctx):
  regions = MemoryRegions()
  regions.build_from_maps(open('./maps.txt', 'r').read())
  files = set()
  for region in regions.regions:
    if region.file.startswith('/'): files.add(region.file)
  print(' '.join(files))


def decode_dwarf(ctx):
  elf = ElfUtils('./decrypted_file')
  dwarf_end = 0x403000
  dwarf = elf.get_range(dwarf_start, dwarf_end)
  with open('./dwarf.out', 'wb') as f:
    f.write(dwarf)

  dwarf = elf.get_range(dwarf_start + 0x85d, dwarf_end)
  with open('./dwarf2.out', 'wb') as f:
    f.write(dwarf)

  print(dwarf)


FORCE_BRANCH = 1
CAN_BRANCH = 2


class OpStatus:

  def __init__(self):
    self.reset()

  def reset(self):
    self.branches = []
    self.flag = 0
    self.action = 0
    self.inner_sp = 0


class StackRemapper:

  def __init__(self, init_pos, vals):
    self.init_pos = init_pos
    self.minv = min(vals)
    self.maxv = max(vals)
    self.vals = vals

  def to_idx(self, i, force=0):
    if not force and i not in self.vals: return None
    return i - self.init_pos


class DwarfImpl:

  def __init__(self, mem, regs, stack_init=None, stack=None, stack_pos=None, dry=0):
    self.ir = None
    self.z3 = 0
    self.dry = dry
    self.fixed_stack_pos = 0
    self.mem = mem
    self.regs = regs
    self.stack_accesses = set()
    self.mem_ref = 0
    self.access_remapper = None
    if stack is None:
      self.stack = [0] * 64
      self.stack[0] = stack_init
      self.stack_pos = 1
    else:
      self.stack = list(stack)
      self.stack_pos = stack_pos
      assert len(stack) == 64

    self.pc_debug = set()
    self.orig_stack = list(self.stack)

    self.hit_count = 0
    self.op = OpStatus()
    self.pc = 0
    self.stop_pc = set()
    self.stop_pc_after = set()
    self.debug = 0
    self.program = None
    self.cnt = defaultdict(int)
    self.M = 2**64 - 1
    self.pc_depth = defaultdict(set)
    self.watched_access = []
    self.log_loop_pc = None
    self.mark_access = None
    self.hook_pc = {}

    def litx(v):

      def f():
        return self.push1(v)

      return f

    for i in range(32):
      setattr(self, f'op_lit{i}', litx(i))

    self.blk_main = None
    self.blk_loop = []
    self.cur_blk_loop = None

  def extract_stack(self, rel_poslist):
    res = []
    for i in rel_poslist:
      res.append(self.stack[self.stack_pos + i])
    return res

  def finalize_log_blk(self, blk):
    blk.end_stack_pos = self.stack_pos
    blk.end_stack = list(self.stack)
    def add_ops(ops, stack_top):
      res = []
      res_rmp = []
      for op in ops:
        if op < stack_top:
          res.append(op)
          res_rmp.append(op-stack_top)
      return res, res_rmp
    blk.inputs, blk.inputs_rmp = add_ops(blk.reads, blk.start_stack_pos)
    blk.outputs, blk.outputs_rmp = add_ops(blk.writes, blk.end_stack_pos)


  def extract_mem(self):
    bsize = dwarf_read_rg.n // 8
    return self.mem.read_nu64(dwarf_read_rg.low, bsize)

  def make_log_blk(self):
    return cmisc.Attr(start_stack=list(self.stack), start_stack_pos=self.stack_pos, reads=set(), writes=set(), end_stack_pos=None)

  def setup_log(self):
    self.blk_main = self.make_log_blk()

  def finalize_log(self):
    self.finalize_log_blk(self.blk_main)

  def setup_for_ir(self, pc):
    if self.fixed_sp is None: return
    for i in range(self.fixed_sp[pc]):
      idx = self.access_remapper.to_idx(i)
      if idx is None: continue
      res = self.ir.builder.gep(self.ir.stack, [self.ir.u64_t(idx)])
      self.stack[i] = self.ir.builder.load(res)

  def finalize_for_ir(self, pc, blk):
    if self.fixed_sp is None: return
    diff = blk.end_stack_pos - self.access_remapper.init_pos

    for i in range(blk.end_stack_pos):
      idx = self.access_remapper.to_idx(i)
      if idx is None: continue
      sptr = self.ir.builder.gep(self.ir.stack, [self.ir.u64_t(idx)])
      self.ir.builder.store(self.stack[i], sptr)

    return diff

  def get(self, p):
    if self.ir:
      if self.fixed_sp:
        pos = self.get_sp() - p - 1
        return self.stack[pos]

      else:
        stack_v = self.ir.builder.load(self.ir.stack_pos)
        stack_v = self.ir.builder.sub(stack_v, self.ir.u64_t(p + 1))
        res = self.ir.builder.gep(self.ir.stack, [stack_v])
        return self.ir.builder.load(res)

    pos = self.stack_pos - p - 1
    assert pos >= 0
    self.notify_read(pos)
    return self.stack[self.stack_pos - p - 1]

  def notify_read(self, pos):
    self.stack_accesses.add(pos)
    if pos in self.watched_access:
      print(f'GOT WATCH {pos} : {self.status()}')

    for x in [self.blk_main, self.cur_blk_loop]:
      if x is not None:
        x.reads.add(pos)
  def notify_write(self, pos):
    for x in [self.blk_main, self.cur_blk_loop]:
      if x is not None:
        x.writes.add(pos)


  def top(self):
    return self.get(0)

  def pop1(self, no_read=0):
    if self.ir:
      if self.fixed_sp:
        self.op.inner_sp -= 1
        return self.stack[self.get_sp()]

      else:
        stack_v = self.ir.builder.load(self.ir.stack_pos)
        nstack_v = self.ir.builder.sub(stack_v, self.ir.u64_t(1))
        res = self.ir.builder.gep(self.ir.stack, [nstack_v])
        res = self.ir.builder.load(res)

        self.ir.builder.store(nstack_v, self.ir.stack_pos)
      return res
    else:
      self.stack_pos -= 1
      assert self.stack_pos >= 0, self.status()
      if not no_read:
        self.notify_read(self.stack_pos)
        return self.stack[self.stack_pos]

  def status(self):
    return f'{self.pc:x} {self.stack_pos}'

  def get_sp(self):
    return self.fixed_sp[self.pc] + self.op.inner_sp

  def push1(self, v):
    if isinstance(v, int): v = self.norm_ext(v)

    if self.ir:
      if self.fixed_sp:
        self.stack[self.get_sp()] = v
        self.op.inner_sp += 1
      else:
        stack_v = self.ir.builder.load(self.ir.stack_pos)
        sptr = self.ir.builder.gep(self.ir.stack, [stack_v])
        self.ir.builder.store(v, sptr)
        nstack_v = self.ir.builder.add(stack_v, self.ir.u64_t(1))
        self.ir.builder.store(nstack_v, self.ir.stack_pos)
    else:
      if isinstance(v, int): v = self.norm_ext(v)
      assert self.stack_pos >= 0
      self.stack_accesses.add(self.stack_pos)
      self.notify_write(self.stack_pos)
      self.stack[self.stack_pos] = v
      self.stack_pos += 1

  def norm_ext(self, v):
    if self.ir:
      if isinstance(v, int):
        return self.ir.u64_t(v)
      return v

    if self.z3: return z3.BitVecVal(v, 64)
    return v

  def op_and(self):
    if self.ir:
      a = self.pop1()
      b = self.pop1()
      self.push1(self.ir.builder.and_(a, b))
    else:
      self.push1(self.pop1() & self.pop1())

  def op_xor(self):
    if self.ir:
      self.push1(self.ir.builder.xor(self.pop1(), self.pop1()))
    else:
      self.push1(self.pop1() ^ self.pop1())

  def op_or(self):
    if self.ir:
      self.push1(self.ir.builder.or_(self.pop1(), self.pop1()))
    else:
      self.push1(self.pop1() | self.pop1())

  def op_plus(self):
    if self.ir:
      self.push1(self.ir.builder.add(self.pop1(), self.pop1()))
    else:
      self.push1(self.pop1() + self.pop1() & self.M)

  def op_minus(self):
    a = self.pop1()
    b = self.pop1()
    if self.ir:
      self.push1(self.ir.builder.sub(b, a))
    else:
      self.push1((b - a) & self.M)

  def op_mul(self):
    if self.ir:
      self.push1(self.ir.builder.mul(self.pop1(), self.pop1()))
    else:
      self.push1(self.pop1() * self.pop1() & self.M)

  def op_reg31(self):
    assert 0

  def op_const1u(self, a):
    self.push1(a & 0xff)

  def op_const4u(self, a):
    self.push1(a & 0xffffffff)

  def op_const8u(self, a):
    self.push1(a)

  def op_swap(self):
    a = self.pop1()
    b = self.pop1()
    self.push1(a)
    self.push1(b)

  def op_deref(self):
    self.op_deref_size(8)

  def set_addr(self, x):
    self.op.branches.append(self.npc + x)

  def op_bra(self, x):
    a = self.pop1()
    self.op.flag |= CAN_BRANCH
    self.set_addr(x)
    if a != 0:
      self.op.action = 1

  def op_skip(self, x):
    self.op.branches = []
    self.set_addr(x)
    self.op.flag |= FORCE_BRANCH

  def op_dup(self):
    self.push1(self.top())

  def op_deref_size(self, sz):
    a = self.pop1()
    if self.ir:
      ptr = self.ir.builder.add(self.ir.data, a)
      res = self.ir.builder.load(self.ir.builder.inttoptr(ptr, self.ir.u64_ptr_t))
      if sz == 1:
        res = self.ir.builder.and_(res, self.ir.u64_t(0xff))
      elif sz == 4:
        res = self.ir.builder.and_(res, self.ir.u64_t(0xffffffff))
      else:
        assert sz == 8

    elif self.z3:
      res = z3.BitVec(f'MEM_REF_{self.mem_ref}', 64)
      self.mem_ref += 1
    elif self.dry:
      res = 0
    else:
      #assert a >= self.flag_addr or dwarf_read_start <= a <= dwarf_read_end, hex(a)
      res = self.mem.read_u(a, sz)

    self.push1(res)

  def op_pick(self, x):
    self.push1(self.get(x))

  def op_rot(self):
    a = self.pop1()
    b = self.pop1()
    c = self.pop1()
    self.push1(a)
    self.push1(c)
    self.push1(b)

  def op_shr(self):
    a = self.pop1()
    b = self.pop1()
    if self.ir:
      b = self.ir.builder.lshr(b, a)
    elif self.dry:
      pass
    else:
      b >>= a
    self.push1(b)

  def op_shl(self):
    a = self.pop1()
    b = self.pop1()
    if self.ir:
      b = self.ir.builder.shl(b, a)
    elif self.dry:
      pass
    else:
      b <<= a
      b &= self.M
    self.push1(b)

  def op_drop(self):
    a = self.pop1(no_read=1)

  def run_dfs(self, pc=None):
    self.pc = pc
    orig_sp = self.stack_pos
    orig_stack = list(self.stack)
    self.pc_depth[self.pc].add(self.stack_pos)
    if not self.run_ins(): return

    for npc in list(self.op.branches):
      self.run_dfs(npc)

    self.stack_pos = orig_sp
    self.stack = orig_stack

  def run(self, pc=None, stop_pc=[], stop_pc_after=[]):
    with cmisc.TempOverride() as to:
      self.pc = pc
      if stop_pc or stop_pc_after:
        to.override_attr(self, 'stop_pc_after', stop_pc_after)
        to.override_attr(self, 'stop_pc', stop_pc)

      while True:
        self.pc_depth[self.pc].add(self.stack_pos)

        if not self.run_ins(): break

    #for k, v in self.pc_depth.items():
    #  print(f'{k:x} -> {v}')
  def is_cond(self, pc):
    ins = self.program[pc]
    return ins.name == 'DW_OP_bra'

  def run_ins(self, update_pc=1, force=0):
    self.op.reset()

    self.cnt[self.pc] += 1
    if not force and self.pc in self.stop_pc:
      return 0
    ins = self.program[self.pc]

    orig_stack_pos = self.stack_pos
    self.npc = self.pc + ins.size + 1
    self.op.branches.append(self.npc)
    func_name = 'op_' + ins.name[6:]
    getattr(self, func_name)(*ins.args)

    if self.pc in self.hook_pc:
      self.hook_pc[self.pc]()

    if self.log_loop_pc == self.pc:
      if self.cur_blk_loop:
        self.finalize_log_blk(self.cur_blk_loop)
        self.blk_loop.append(self.cur_blk_loop)
      self.cur_blk_loop = self.make_log_blk()

    opc = self.pc
    if self.debug or opc in self.pc_debug:
      print(
          'ON ', hex(self.pc), ins.name, ins.size, list(map(hex, ins.args)), orig_stack_pos,
          self.stack_pos, list(map(hex, self.stack[max(0, self.stack_pos - 7):self.stack_pos]))
      )

    if update_pc:
      self.pc = self.op.branches[self.op.action]
    if opc in self.stop_pc_after:
      self.hit_count -= 1
      return self.hit_count > 0

    return 1

  def snapshot(self):
    rg = Z.Range1D(dwarf_read_start, dwarf_read_end)

    dump_obj = cmisc.Attr(
        mem_snapshot=snapshot_mem(self.mem, [dwarf_read_rg]),
        stack=self.stack,
        stack_pos=self.stack_pos,
        pc=self.pc,
    )
    return dump_obj


def read_dwarf_program(fname, base_offset=0):
  res = {}
  for line in open(fname, 'r').readlines():
    line = line.strip()
    if not line: continue
    if line[0] == '#': continue
    d = line.split()
    offset, size, bytecode, name, *args = d

    offset = base_offset + int(offset, 16)
    size = int(size, 16)
    args = list(map(cmisc.to_int, args))
    if size == 2:
      args[0] = Z.ctypes.c_int16(args[0]).value
    res[offset] = cmisc.Attr(off=offset, size=size, name=name, args=args)

  return res


def load_dwarf_data(**kwargs):
  dwarf_file = flags.dwarf_file
  if flags.prepare_dwarf_ir: dwarf_file = g_dwarf_ir_file

  orig_pc = None
  if dwarf_file:
    f = open(dwarf_file, 'rb')
    data = Z.pickle.load(f)
    data.flag_addr = None
    mem = seg_mem_from_snapshot(data.mem_snapshot)
    pc = getattr(data, 'pc', 1)
    orig_pc = pc
    if flags.pc_src: pc = flags.pc_src
  else:
    f = open(g_dwarf_file, 'rb')
    data = Z.pickle.load(f)
    mem = seg_mem_from_snapshot(data.mem_snapshot)
    print(len(mem.get_str(data.flag_addr, 10)))
    mem.write(data.flag_addr, bytes(range(32)))
    pc = 1

  dwarf = DwarfImpl(mem, None, stack=data.stack, stack_pos=data.stack_pos, **kwargs)
  dwarf.orig_pc = orig_pc
  if flags.pc_dest:
    if flags.stop_before:
      dwarf.stop_pc.add(flags.pc_dest)
    else:
      dwarf.stop_pc_after.add(flags.pc_dest)
  if flags.prepare_dwarf_ir:
    dwarf.stop_pc.add(g_dwarf_ir_stop_pc)

  if flags.pc_src:
    pc = flags.pc_src
  dwarf.pc = pc
  flags.pc_src = pc
  dwarf.pc_debug.update(flags.pc_debug)

  program = read_dwarf_program('./dwarf.algo.clean')
  program.update(read_dwarf_program('./dwarf.algo.clean.part2', base_offset=0x85d))
  dwarf.program = program
  dwarf.flag_addr = data.flag_addr
  dwarf.fixed_stack_pos = flags.fixed_sp

  if 0 and data.flag_addr is not None:
    dwarf.mem.write_u8(data.flag_addr + 0, 3)
    print('DWARF FLAG ', mem.get_str(data.flag_addr, 10))

  dwarf.stop_pc_after.update((WIN_PC, FAIL_PC))
  return dwarf


def go_dwarf(ctx):
  dwarf = load_dwarf_data()

  dwarf.debug = flags.debug
  print(Display.disp_list(dwarf.stack[:dwarf.stack_pos]))
  print(f'GO DWARF {dwarf.pc:x} {dwarf.stack_pos}')

  dwarf.run(pc=dwarf.pc)

  if flags.prepare_dwarf_ir:
    out_file = g_dwarf_ir_file
  else:
    out_file = flags.out_dwarf_file

  if out_file:
    Z.pickle.dump(dwarf.snapshot(), open(out_file, 'wb'))


def test_dwarf(ctx):
  prog = read_dwarf_program('./dwarf.algo.clean')
  for k, v in prog.items():
    print(k, v)


def identify_blocks(g, branch_node=set()):
  uj = UnionJoinLax()

  can_collapse = set()
  for n in g:
    if n not in branch_node and g.in_degree(n) == 1 and g.out_degree(n) == 1: can_collapse.add(n)
    uj.root(n)  # create in uj

  for a, b in g.edges():
    if a in can_collapse and b in can_collapse:
      uj.join(a, b, dict(src=a, dst=b))
  return uj


def contract_blocks(g, uj):
  n_map = {}
  ng = nx.DiGraph()
  for blk in uj.groups():
    emin = min(blk)
    n = f'{emin:x}_{max(blk):x}'

    r = uj.root(emin)
    ng.add_node(n, ops=blk, src=uj.data.src[r], dst=uj.data.dst[r])
    for x in blk:
      n_map[x] = n

  for a, b in g.edges():
    assert b in uj.par
    assert a in uj.par
    if uj.root(a) != uj.root(b):
      ng.add_edge(n_map[a], n_map[b], **g[a][b])
  return ng


def norm_node_name(N):
  return N.replace(' ', '').replace("'", '')


def contract_block(g, blk, N, attrs):
  g.add_node(N, **attrs)
  blk = set(blk)

  for x in blk:
    for o in list(g.successors(x)):
      if o not in blk:
        g.add_edge(N, o, **g[x][o])
    for o in list(g.predecessors(x)):
      if o not in blk:
        g.add_edge(o, N, **g[o][x])
    g.remove_node(x)


def find_next_graph_op(g, ix):
  if len(g) == 1: return None
  if nx.algorithms.dag.is_directed_acyclic_graph(g):
    return cmisc.Attr(loop=0, name=g_mainfunc_name, nodes=list(g.nodes()), attrs=dict())

  branch_nodes = set()
  for n in g:
    if g.out_degree(n) > 1: branch_nodes.add(n)

  def trywalk(x, dest):
    lst = []
    while True:
      lst.append(x)
      if x == dest: return lst
      if g.out_degree(x) == 0: return None
      if g.out_degree(x) > 1: return None
      x = next(g.successors(x))

  for n in list(g.nodes()):
    if n not in g: continue

    scc = list(g.successors(n))
    if len(scc) != 2: continue
    for i in range(2):
      ll = trywalk(scc[i], n)
      if ll is None: continue
      fd = 1
      loop_entry = []
      for j in range(len(ll)):
        if g.in_degree(ll[j]) == 2: loop_entry.append(j)
      assert len(loop_entry) == 1
      print('LOOP ENTRY', loop_entry, ll)
      le = loop_entry[0]
      ll = ll[le:] + ll[:le]

      assert len(loop_entry) == 1
      src = g.nodes[ll[0]]['src']
      dst = g.nodes[n]['dst']
      N = f'LOOP_{ix}_{src:x}_{dst:x}'
      N = norm_node_name(N)
      return cmisc.Attr(loop=1, name=N, branch_point=n, nodes=ll, is_cond=g[n][scc[i]]['is_cond'], attrs=dict(src=src, dst=dst))

  uj = UnionJoinLax()
  ng = nx.DiGraph(g)

  def merge_nodes(lst, update_dict={}):
    uj.join_multiple(lst, update_dict)

    r = lst[0]
    for i in lst[1:]:
      for x in ng.successors(i):
        if uj.root(x) != uj.root(r): ng.add_edge(r, x, **ng[i][x])
      for x in ng.predecessors(i):
        if uj.root(x) != uj.root(r): ng.add_edge(x, r, **ng[x][i])
    for i in lst[1:]:
      ng.remove_node(i)

  while True:
    for a in ng.nodes():
      if ng.out_degree(a) == 1:
        b = next(ng.successors(a))
        if ng.in_degree(b) == 1:
          merge_nodes([a, b], dict(src=a, dst=b))
          break
      elif ng.out_degree(a) == 2:
        b, c = list(ng.successors(a))
        if ng.in_degree(b) != 1 or ng.in_degree(c) != 1: continue
        if ng.out_degree(b) != 1 or ng.out_degree(c) != 1: continue
        nb = next(ng.successors(b))
        nc = next(ng.successors(c))
        if nb == nc:
          merge_nodes([a, b, c, nb], dict(src=a, dst=nb))
          break

    else:
      break

  groups = uj.groups()
  groups = [(len(x), x) for x in groups]
  nn, best = max(groups)
  if nn == 1: return None
  rx = uj.root(next(iter(best)))
  src = g.nodes[uj.data.src[rx]]['src']
  dst = g.nodes[uj.data.dst[rx]]['dst']
  return cmisc.Attr(loop=0, name=f'dasg_{ix}_{src:x}_{dst:x}', nodes=best, attrs=dict(src=src, dst=dst))


def dump_graph(bg, fname):
  write_dot(bg, f"{fname}.dot")
  Z.sp.check_output(f'dot -Tps {fname}.dot > {fname}.dot.ps', shell=1)


def build_dwarf_graph(dump_graph=1, **kwargs):
  dwarf = load_dwarf_data(**kwargs)
  bg = nx.DiGraph()

  branch_node = set()

  dwarf.dry = 1
  def dfs(pc):
    if pc in bg: return
    bg.add_node(pc)
    dwarf.pc = pc
    dwarf.stack_pos = 32
    if not dwarf.run_ins():
      return

    if dwarf.op.flag: branch_node.add(pc)
    for i, br in enumerate(list(dwarf.op.branches)):
      dfs(br)
      bg.add_edge(pc, br, is_cond=i)

  dfs(dwarf.pc)
  if 0:
    write_dot(bg, f"{flags.runid}_bg.dot")
    Z.sp.check_output(f'dot -Tps {flags.runid}_bg.dot > {flags.runid}_bg.dot.ps', shell=1)

  uj = identify_blocks(bg, branch_node)
  ng = contract_blocks(bg, uj)
  for n in ng:
    #works because block does not contain branches
    ng.node[n]['ops'] = list(sorted(ng.node[n]['ops']))

  if dump_graph:
    print(len(ng))
    write_dot(ng, f"{flags.runid}_ng_loop.dot")
    Z.sp.check_output(f'dot -Tps {flags.runid}_ng_loop.dot > {flags.runid}_ng_loop.dot.ps', shell=1)

  return ng


def dwarf_graph(ctx):
  ng = build_dwarf_graph()

  to_llvm(ng)
  return
  ops = detect_loops(ng)
  Z.pprint(ops)

  if 1:
    print(len(ng))
    write_dot(ng, f"{flags.runid}_ng.dot")
    Z.sp.check_output(f'dot -Tps {flags.runid}_ng.dot > {flags.runid}_ng.dot.ps', shell=1)


def test1(ctx):
  a = cmisc.Attr(awe=123)
  Z.pickle.loads(Z.pickle.dumps(arch_data[Arch.arm64]))


def analyse_dwarf_seq(dwarf, program, src, dest, stack_pos):
  stack = [z3.BitVec(f'arg_{i}', 64) for i in range(64)]
  print((stack[0] + stack[1]).num_args())
  print(stack[0].num_args())

  dwarf.z3 = 1
  dwarf.stack = stack
  dwarf.stack_pos = stack_pos
  dwarf.run(program, src, dest)
  print(dwarf.stack_pos, stack_pos)
  for i in range(dwarf.stack_pos):
    print(type(stack[i]), stack[1].num_args())
    print(z3.simplify(stack[i]).sexpr())

    print()


def dwarf_z3(ctx):
  dwarf = load_dwarf_data()
  #analyse_dwarf_seq(dwarf, program, 0xb25, 0xc2f, 29)
  #b25 -> c2f: x -> f^k(x) (k=6)

  analyse_dwarf_seq(dwarf, program, 0x292, 0x2f3, 29)


def dwarf_gen_all(ctx):
  do_gen_all(ctx.pc_src, ctx.pc_dest)

def do_gen_all(pci, pcf):
  flags.pc_src = pci
  flags.pc_dest = pcf

  g = build_dwarf_graph(dump_graph=0)
  chains = find_chains(g)
  Z.pprint(chains)
  g_contract = nx.DiGraph(g)

  cb = CodeBuilder()

  for chain in chains:
    opi = g.node[chain[0]]['ops']
    opf = g.node[chain[-1]]['ops']
    st = opi[0]
    nd = opf[-1]
    flags.pc_src = st
    flags.pc_dest = nd
    print('Processing chain ', chain, st, nd)
    ng = build_dwarf_graph(dump_graph=0, dry=1)
    dwarf = load_dwarf_data()

    nnode = f'CHAIN_{st:x}_{nd:x}'
    if len(ng) == len(g_contract):
      nnode = g_mainfunc_name
    cb.build_code(ng, dwarf, name=nnode, pc_start=st)
    contract_block(g_contract, chain, nnode, dict(src=st, dst=nd))

    s = chain[-1]
    for t in g.successors(s):
      if t == chain[0]:
        g_contract.add_edge(nnode, nnode, **g[s][t])

  flags.pc_src = pci
  flags.pc_dest = pcf

  print('STEP 2 \n\n\n')
  g = g_contract
  print(list(g.nodes()))
  print(list(g.edges()))
  ix = 0
  while True:
    ix += 1
    dump_graph(g, f'./graphs/t_{flags.runid}_{ix:02d}')
    op = find_next_graph_op(g, ix)
    print('\n\n\n')
    print('GOGO for op ', ix, op)
    if op is None: break
    if len(op.nodes) == len(g):
      op.name = g_mainfunc_name

    subg = g.subgraph(op.nodes)
    if not op.loop:
      list(nx.algorithms.dag.topological_sort(subg))  # crash if not acyclic

    cb.build_code_op(subg, name=op.name, op=op)
    contract_block(g, op.nodes, op.name, op.attrs)

    print('result >> ')
    print(list(g.nodes()))
    print(list(g.edges()))

  cb.finalize()
  return cb


def find_root(g):
  cnds = []
  for n in g.nodes():
    if g.in_degree(n) == 0:
      cnds.append(n)

  print(g.nodes())
  print(g.edges())
  assert len(cnds) == 1, cnds
  return cnds[0]


def identify_chain(g, x):
  lst = []
  while True:
    lst.append(x)
    sc = list(g.successors(x))
    if len(sc) != 1: break
    x = sc[0]
    if g.in_degree(x) > 1: break
  return lst


def find_chains(g):
  r = find_root(g)
  seen = set()
  chains = []

  def dfs(x):
    if x in seen: return
    nc = identify_chain(g, x)
    seen.update(nc)
    chains.append(nc)
    for nx in g.successors(nc[-1]):
      dfs(nx)

  dfs(r)
  return chains


def compare_call_ret_and_dwarf_exec(call_ret, dwarf):
  print(dwarf.stack)

  print('SP1', dwarf.stack_pos)
  print('SP2', call_ret.stack_pos)
  print('JIT stack DIFF', call_ret.diff)

  sp1 = dwarf.stack[:dwarf.stack_pos]
  sp2 = call_ret.stack[:call_ret.stack_pos]
  print(Display.disp_list(sp1))
  print(Display.disp_list(sp2))
  print()
  print(Display.diff_lists(sp1, sp2))

def do_call_function(cfptr, mem, stack, stack_pos): 
  p_u64 = ctypes.POINTER(ctypes.c_uint64)
  cfunc = ctypes.CFUNCTYPE(ctypes.c_int64, p_u64, p_u64, p_u64)(cfptr)

  rstack = list(stack)
  c_stack = (ctypes.c_uint64 * 64)(*rstack)
  result = ctypes.c_uint64(0)

  bsize = dwarf_read_rg.n // 8
  dx = mem.read_nu64(dwarf_read_rg.low, bsize)
  data = (ctypes.c_uint64 * bsize)(*dx)
  data_ptr = ctypes.cast(data, ctypes.c_void_p).value

  data_ptr = ctypes.c_void_p(data_ptr - dwarf_read_rg.low)
  data_ptr = ctypes.cast(data_ptr, p_u64)
  stack_ptr = ctypes.cast(c_stack, ctypes.c_void_p).value + (stack_pos) * 8
  stack_ptr = ctypes.cast(stack_ptr, p_u64)

  diff = cfunc(data_ptr, stack_ptr, ctypes.pointer(result))
  end_stack_pos = stack_pos + diff
  nstack = np.ctypeslib.as_array(c_stack).tolist()
  return cmisc.Attr(stack=nstack, stack_pos=end_stack_pos, diff=diff)


class CodeBuilder:

  def __init__(self):
    llvm.initialize()
    llvm.initialize_native_target()
    llvm.initialize_native_asmprinter()
    self.module = ll.Module()
    flags.fixed_sp = True
    self.builder = ll.IRBuilder()

    self.u64_t = ll.IntType(64)
    self.u64_ptr_t = self.u64_t.as_pointer()
    # PROTYPE:
    # u64 diff_stack func(u64 data_ptr, u64 *stack_top, u64 *result)
    self.fnty = ll.FunctionType(self.u64_t, [self.u64_t, self.u64_ptr_t, self.u64_ptr_t])
    self.funcs = {}

  def finalize(self):
    strmod = str(self.module)
    llmod = llvm.parse_assembly(strmod)
    print(llmod)

    pmb = llvm.create_pass_manager_builder()
    pmb.opt_level = 9
    pmb.inlining_threshold = 100


    pm = llvm.create_module_pass_manager()
    pmb.populate(pm)

    pm.run(llmod)
    target_machine = llvm.Target.from_default_triple().create_target_machine()

    ee = app.global_context.enter_context(llvm.create_mcjit_compiler(llmod, target_machine))
    ee.finalize_object()
    print('GOOT')
    print(target_machine.emit_assembly(llmod))
    print(len(target_machine.emit_assembly(llmod).splitlines()))

    if flags.elf_outfile:
      with open(flags.elf_outfile, 'wb') as f:
        f.write(target_machine.emit_object(llmod))

    self.cfptr = ee.get_function_address(g_mainfunc_name)
    if not flags.run_ir: return

    dwarf = load_dwarf_data()
    dwarf.run(pc=dwarf.orig_pc, stop_pc=[dwarf.pc])
    call_ret= do_call_function(self.cfptr, dwarf.mem, dwarf.orig_stack, dwarf.stack_pos)

    dwarf = load_dwarf_data()
    dwarf.run(pc=dwarf.orig_pc, stop_pc=[dwarf.pc])
    dwarf.debug = 0
    dwarf.run(pc=dwarf.pc)

    compare_call_ret_and_dwarf_exec(call_ret, dwarf)

  def build_code_op(self, g, op, name):
    self.g = g
    func = ll.Function(self.module, self.fnty, name=name)
    self.funcs[name] = func
    self.func = func
    self.builder = ll.IRBuilder()

    builder = self.builder
    data = func.args[0]
    stack = func.args[1]
    res = func.args[2]

    func_entry = func.append_basic_block()
    builder.position_at_end(func_entry)

    if 0:
      builder.ret(diff_var)
      return

    blks = defaultdict(cmisc.Attr)
    self.blks = blks
    for node in g.nodes():
      blks[node].entry = self.func.append_basic_block(name='begin_' + node)

    if op.loop:
      order = op.nodes
      blks['END'].entry = self.func.append_basic_block(name='loop_end')
    else:
      order = list(nx.algorithms.dag.topological_sort(g))

    for k, v in blks.items():
      builder.position_at_end(v.entry)
      v.name = k
      v.diff = builder.phi(self.u64_t)

    blk0 = blks[order[0]]
    builder.position_at_end(func_entry)

    #fty = ll.FunctionType(self.u64_t, [])
    #builder.asm(fty, "int 3;", "=r",
    #                (), True, name="stop")

    builder.branch(blk0.entry)
    print('BRANCH entry ', blk0.name)

    blk0.diff.add_incoming(self.u64_t(0), func_entry)

    def add_cond(b1, b2, is_cond_p1, cur_diff, cur_blk):
      if is_cond_p1:
        b1, b2 = b2, b1

      cur_diff = builder.sub(cur_diff, self.u64_t(1))
      stack_top = self.builder.gep(stack, [cur_diff])
      cond_var = self.builder.load(stack_top)
      cond = builder.icmp_unsigned('==', cond_var, self.u64_t(0))

      b1.diff.add_incoming(cur_diff, cur_blk.entry)
      b2.diff.add_incoming(cur_diff, cur_blk.entry)
      builder.cbranch(cond, b1.entry, b2.entry)

    for node in order:
      fx = self.funcs[node]
      blk = blks[node]
      bx = blk.entry

      builder.position_at_end(bx)
      stack_top = self.builder.gep(stack, [blk.diff])
      diff = builder.call(fx, [data, stack_top, res])
      cur_diff = builder.add(blk.diff, diff)

      scc = list(g.successors(node))
      odeg = len(scc)
      if odeg == 0:
        builder.ret(cur_diff)
      elif odeg == 1:
        if op.loop and node == op.branch_point:
          add_cond(blks[scc[0]], blks['END'], op.is_cond, cur_diff, blk)
        else:
          nblk = blks[scc[0]]
          nblk.diff.add_incoming(cur_diff, bx)

          builder.branch(nblk.entry)
      else:
        add_cond(blks[scc[0]], blks[scc[1]], g[node][scc[0]]['is_cond'], cur_diff, blk)

    if op.loop:
      blk = blks['END']
      builder.position_at_end(blk.entry)
      builder.ret(blk.diff)

  def build_code(self, g, dwarf, name=None, pc_start=None):
    # graph is a path. Need correct ordering
    assert len(g.edges()) == len(g)-1
    chain = list(nx.algorithms.dag.topological_sort(g))
    assert len(chain) == len(g)



    self.g = g
    self.dwarf = dwarf
    func = ll.Function(self.module, self.fnty, name=name)
    self.func = func
    self.funcs[name] = func

    dw0 = load_dwarf_data(dry=1)
    dw0.stack_pos = 32 # center, should not go out of bounds
    start_stack_pos = dw0.stack_pos
    dw0.run_dfs(pc=pc_start)

    nsp_map = {}
    for k, v in dw0.pc_depth.items():
      assert len(v) == 1
      nsp_map[k] = list(v)[0]

    dwarf.fixed_sp = nsp_map

    accesses = dw0.stack_accesses
    accesses.add(start_stack_pos)
    dwarf.access_remapper = StackRemapper(start_stack_pos, accesses)

    builder = self.builder
    dwarf.buider = builder
    res_ptr = func.args[2]
    dwarf.ir = cmisc.Attr(
        builder=builder,
        data=func.args[0],
        stack=func.args[1],
        u64_t=self.u64_t,
        u64_ptr_t=self.u64_ptr_t,
    )

    self.node_data = defaultdict(cmisc.Attr)
    func_entry = func.append_basic_block()
    builder.position_at_end(func_entry)
    dwarf.debug = 0

    dwarf.setup_for_ir(pc_start)

    for n in chain:
      blk = self.do_1(n)
      if g.out_degree(n) == 0:
        builder.position_at_end(blk.end)

        res = dwarf.finalize_for_ir(blk.pc_last, blk)
        if blk.pc_last == WIN_PC:
          builder.store(self.u64_t(1), res_ptr)
        elif blk.pc_last == FAIL_PC:
          builder.store(self.u64_t(0), res_ptr)

        builder.ret(self.u64_t(res))
      if g.in_degree(n) == 0:
        builder.position_at_end(func_entry)
        builder.branch(blk.entry)

    for n in chain:
      nsc = g.out_degree(n)
      if nsc == 0: continue
      bn = self.node_data[n]
      scc = g.successors(n)
      v1 = next(scc)
      b1 = self.node_data[v1]

      builder.position_at_end(bn.end)
      if nsc == 1:
        builder.branch(b1.entry)
      else:
        assert 0

    return self.func

  def do_1(self, n, stop_at=None):

    ops = self.g.node[n]['ops']
    blk = self.node_data[n]

    entry = self.func.append_basic_block(name='begin_' + n)
    end = self.func.append_basic_block(name='end_' + n)
    self.dwarf.ir.blk = entry

    blk.entry = entry
    blk.end = end
    blk.pc_last = ops[-1]
    self.builder.position_at_end(entry)
    print(ops)

    for op in ops:
      self.dwarf.pc = op
      self.dwarf.op.reset()
      #if op in self.dwarf.stop_pc: break
      if self.dwarf.is_cond(op):
        break
      self.dwarf.run_ins(update_pc=0, force=1)
      if stop_at is not None or stop_at == op: break
    blk.end_stack_pos = self.dwarf.get_sp()
    self.builder.branch(end)
    return blk


def write_c_code(ctx):
  dwarf = load_dwarf_data()
  check_func = '''
  //stop before 0xac
  uint64_t checkitv[4] = {0x658302a68e8e1c24,0xdc7564f1612e5347, 0xd9c69b74a86ec613,0x65850b36e76aaed5};
  if (checkitv[0] !=stack[-2-2]) return 0;
  if (checkitv[1] !=stack[-2-3]) return 0;
  if (checkitv[2] !=stack[-2-0]) return 0;
  if (checkitv[3] !=stack[-2-1]) return 0;
  return 1;
  '''
  load_func = '''
    for (int i =0; i<4; ++i){
      stack[3+i] = input[i];
    }
  '''

  do_write_code(dwarf.extract_mem(), dwarf.stack, dwarf.stack_pos, check_func, load_func)

def do_write_code(data, stack, stack_pos, check_func, load_func):

  def fmt_array(arr):
    return ','.join(map(fmt_c_val, arr))

  tmpl = r'''
#include <cstdio>
#include <cstdlib>
#include <cstdint>
#include <cstring>
#include<string>
extern "C" {
int64_t mainfunc(char *data, uint64_t *stack, uint64_t *res);
void good(){
puts("good");
}
void bad(){
puts("bad");
}
}

bool checkit(const uint64_t *input, uint64_t *stack){
   ${CHECK_FUNC};
}



uint64_t go(const uint64_t *input) {
  uint64_t stack[] = {
    ${STACK_DATA}
  };
  uint64_t data[] = {
    ${DATA}
  };

  int64_t stack_pos = ${STACK_POS};
  uint64_t res;
  if (input != nullptr){
  ${LOAD_FUNC}
  }

   int64_t diff = mainfunc((char*)data - ${DATA_OFFSET}, stack + stack_pos, &res);
   int64_t top = stack_pos + diff;

   for (int i=0; i<top; ++i){
   printf("%d >> %Lx\n", i, stack[i]);
   }
   puts("");
   return checkit(input, stack+top);
   return res;
}

int main(int argc, char **argv){
  uint64_t res = 0;
  if (argc == 2) res= go((const uint64_t*)argv[1]);
  else {
  int n = strlen(argv[1]);
  std::string tmp(n/2, 0);
  for (int i=0; i<n/2; ++i){
    std::string cur;
    cur += argv[1][2*i];
    cur += argv[1][2*i+1];
    tmp[i] = strtol(cur.data(), nullptr, 16);
  }
res= go((const uint64_t*)tmp.data());
  }
  if (res) {
  good();
  }else bad();
  return 0;
}
'''

  code = cmisc.template_replace(
      tmpl,
      STACK_DATA=fmt_array(stack),
      STACK_POS=stack_pos,
      DATA=fmt_array(data),
      DATA_OFFSET=dwarf_read_start,
    LOAD_FUNC=load_func,
    CHECK_FUNC=check_func,
  )
  print(code)
  print('Written to ', flags.c_outfile)

  with open(flags.c_outfile, 'w') as f:
    f.write(code)


logging.getLogger('angr').setLevel('FATAL')
def solve_angr(ctx):
  import angr
  import logging
  import claripy

  #proj = angr.Project('./a.out')
  proj = angr.Project(ctx.infile)
  good_func = proj.loader.find_symbol('good')
  bad_func = proj.loader.find_symbol('bad')

  argv1 = claripy.BVS("argv1", 64 * ctx.angr_size)
  initial_state = proj.factory.entry_state(args=[ctx.infile, argv1])
  sm = proj.factory.simulation_manager(initial_state)
  sm.explore(find=good_func.rebased_addr, avoid=bad_func.rebased_addr)
  found = sm.found[0]
  buf = found.solver.eval(argv1, cast_to=bytes)
  buf = StreamRW(buf, arch=Arch.x86_64)
  res = buf.read_nu64(0,ctx.angr_size)
  print(list(map(hex, res)))
  return res


import tabulate
def disp_blk(blk):
  ops = blk.inputs + blk.outputs
  minv = min(ops)
  maxv = max(ops)
  minv = min(minv, blk.start_stack_pos, blk.end_stack_pos)
  maxv = max(maxv, blk.start_stack_pos, blk.end_stack_pos)
  tb = np.zeros((3,maxv+1-minv)).tolist()

  for i in range(minv, maxv+1):
    s = str(i) + '\t'
    if i == blk.start_stack_pos:
      s += 'I\t'
    if i == blk.end_stack_pos:
      s += 'O\t'
    idx= i - minv
    tb[0][idx] = s
    tb[1][idx] = tb[2][idx] = ''
    if i in blk.inputs:
      tb[1][idx] = fmt_v(blk.start_stack[i])
    if i in blk.outputs:
      tb[2][idx] = fmt_v(blk.end_stack[i])

  print(tabulate.tabulate(tb))
  print('\n\n')

def gather_stats(tgt, inputs=None):
  dwarf = load_dwarf_data()
  dwarf.log_loop_pc = tgt[2]
  for step in range(flags.tgt_repeat):
    dwarf.debug = 0
    dwarf.mark_access = False
    dwarf.run(pc=dwarf.pc, stop_pc=[tgt[0]])

    dwarf.mark_access = True

    if flags.debug_tgt:
      dwarf.debug=1

    dwarf.hit_count = flags.tgt_hit_count
    dwarf.setup_log()
    dwarf.run(pc=dwarf.pc, stop_pc_after=[tgt[1]])
    dwarf.finalize_log()

    print('MAIN BLOCK')
    disp_blk(dwarf.blk_main)

    for i, blk in enumerate(dwarf.blk_loop):
      print('Loop block ', i)
      disp_blk(blk)
  return dwarf.blk_main

  if 0:
    if not flags.tgt_run_all:
      return
    mb = dwarf.blk_main

    invals = []
    outvals = []
    def hookfunc_entry():
      invals.append(list(map(fmt_v, dwarf.extract_stack(mb.inputs_rmp))))
    def hookfunc_entry_end():
      outvals.append(list(map(fmt_v, dwarf.extract_stack(mb.outputs_rmp))))



    dwarf = load_dwarf_data()
    dwarf.hook_pc[tgt[0]] = hookfunc_entry
    dwarf.hook_pc[tgt[1]] = hookfunc_entry_end
    dwarf.run(pc=dwarf.pc)

    print(tabulate.tabulate(invals))
    print('\n')
    print(tabulate.tabulate(outvals))

def compute_stats(ctx):
  blks = []
  #start, stop, loop_cond
  blks.append((0x15d,0x175, 0x16a))
  blks.append((0x197,0x1e0, 0x2fb))
  blks.append((0x152,0x21c, 0x210))
  blks.append((0x7d,0x9c, 0x21f))
  blks.append((0x76,0xae, 0xa8))
  blks.append((0xb3, 0x145, 0x142))
  blks.append((0xb3, 0x153, None))
  blks.append((0x76, 0xb3, None))


  if flags.tgt_spec:
    tgt =eval(flags.tgt_spec)
  else: tgt = blks[-1]



  return gather_stats(tgt)



def do_create_func(tgt, check_idx, load_idx):


  cb = do_gen_all(tgt[0], tgt[1])
  print('GENERATE FUNC ')
  dwarf = load_dwarf_data()
  dwarf.run(pc=dwarf.orig_pc, stop_pc=[tgt[0]])

  inx = dwarf.stack
  call_ret = do_call_function(cb.cfptr, dwarf.mem, dwarf.stack, dwarf.stack_pos)

  print(Display.disp_list(call_ret.stack))

  load_func = []
  check_func = []

  for i, idx in enumerate(check_idx):
    check_func.append(f'printf("CHECK GOT >> %d %Lx\\n", {idx}, input[{i}]);')
  for i, idx in enumerate(check_idx):
    want= call_ret.stack[call_ret.stack_pos+idx]
    check_func.append(f'if (stack[{idx}] != input[{i}]) return 0;')

  for i, idx in enumerate(load_idx):
    load_func.append(f'printf("LOAD GOT >> %d %Lx\\n", {idx}, input[{i+len(check_idx)}]);')
  for i, idx in enumerate(load_idx):
    load_func.append(f'stack[stack_pos + {idx}] = input[{i+len(check_idx)}];')

  check_func.append('return 1;')
  check_func='\n'.join(check_func)
  load_func='\n'.join(load_func)

  do_write_code(dwarf.extract_mem(), dwarf.stack, dwarf.stack_pos, check_func, load_func)

  if 0:
    print('starting stuff at ', dwarf.stack_pos, dwarf.pc, tgt, dwarf.orig_pc)

    dwarf.debug = 0
    dwarf.run(pc=dwarf.pc)

    compare_call_ret_and_dwarf_exec(call_ret, dwarf)


def create_func(ctx):
  tgt =eval(flags.tgt_spec)

  check_idx=  [-1, -2]
  load_idx = [-1, -2]
  do_create_func(chck_idx, load_idx)


def execute_func(func_spec, in_args):
  dwarf = load_dwarf_data()
  for p,v in zip(func_spec.in_pos, in_args):
    dwarf.stack[dwarf.stack_pos+p] = v
  print('I', Display.disp_list(dwarf.stack[:dwarf.stack_pos]))
  dwarf.run(pc=func_spec.tgt[0], stop_pc_after=[func_spec.tgt[1]])
  print('O', Display.disp_list(dwarf.stack[:dwarf.stack_pos]))

  return dwarf.extract_stack(func_spec.out_pos)


def execute_func_bin(binfile, func_spec, in_args, out_args):
  inx = out_args + in_args
  buf = StreamRW(bytearray([0]*len(inx)*8), arch=Arch.x86_64)
  buf.write_nu64(0, inx)
  res = sp.check_output([binfile, bytes(buf.buf).hex(), 'a'])
  print(res)


class AngrSolver:
  def __init__(self, infile):

    #proj = angr.Project('./a.out')
    proj = angr.Project(infile)
    self.good_func = proj.loader.find_symbol('good')
    self.bad_func = proj.loader.find_symbol('bad')
    self.proj = proj


  def solve1(self, fixed_input, n_find, fixed_output):

    b1 = StreamRW(bytearray([0]*len(fixed_input)*8), arch=Arch.x86_64)
    b1.write_nu64(0, fixed_input)
    b2 = StreamRW(bytearray([0]*len(fixed_output)*8), arch=Arch.x86_64)
    b2.write_nu64(0, fixed_output)

    inx =  claripy.BVV(bytes(b1.buf))
    input_var =  claripy.BVS('unknown', 64 * n_find)

    data = claripy.Concat(claripy.BVV(bytes(b2.buf + b1.buf)), input_var)


    initial_state = self.proj.factory.entry_state(args=['abc', data])
    sm = self.proj.factory.simulation_manager(initial_state)
    sm.explore(find=self.good_func.rebased_addr, avoid=self.bad_func.rebased_addr)
    found = sm.found[0]
    buf = found.solver.eval(input_var, cast_to=bytes)
    buf = StreamRW(buf, arch=Arch.x86_64)
    res = buf.read_nu64(0, n_find)
    return res


def final_solve(ctx):
  bijective_tgt = 0x154,0x20f, None
  kdf_tgt = 0xb3,0x145,None
  bin_outfile='./a.out'

  kdf_func = cmisc.Attr(tgt=kdf_tgt, in_pos=[-2,-1], out_pos=[-2,-1])
  enc_func = cmisc.Attr(tgt=bijective_tgt, in_pos=[-5,-4,-3,-2,-1,], out_pos=[-3,-2])
  solver = AngrSolver(bin_outfile)

  if 0:
    do_create_func(enc_func.tgt, enc_func.out_pos, enc_func.in_pos)
    Z.sp.check_output(f'g++ {ctx.elf_outfile} {ctx.c_outfile} -o {bin_outfile}', shell=1)

  if 0:
    if 1:
      kx = [0x00000000db1a2f74 , 0xdb7242d7a8cba517 , 0x000000000000000e]
      in0 = [0xed61585259b19819 , 0xb0b3765ea1a16594]
    else:
      kx = [0x00001000ae331bdc,  0xae0197bfd1b0a1cb,  0x0000000000000000]
      in0 = [0x0f0e0d0c0b0a0908 , 0x0706050403020100]
    inx = kx + in0
    expected =execute_func(enc_func, inx)
    print('QQ', Display.disp_list(inx))
    print(Display.disp_list(expected))

    execute_func_bin(bin_outfile, enc_func, inx, expected)


    nc = solver.solve1(kx, 2, expected)
    print('got' ,Display.disp_list(nc))
    print('want', Display.disp_list(in0))
    return


    print(nc)
    return

  want_res = [0x65850b36e76aaed5,0xd9c69b74a86ec613 ,0xdc7564f1612e5347,0x658302a68e8e1c24]



  def do_reverse(k, c):
    for i in reversed(range(15)):
      args = k + [i]
      print()
      print('DEC ', i, Display.disp_list(k), Display.disp_list(c))
      nc = solver.solve1(args, 2, c)
      print('GOT >> ', Display.disp_list(nc))
      c = nc
    return c


  niter = 4

  if 0:
    tmp_res =[ 0x991cf534d118b2e6,  0x0f39a19e0cfe22df, 0xebf6c7c4613a969d , 0x244a3a2cad4ebe77]
    tmp_res = [0x3285e90bbc697556  ,0xfb42b874487351e0  ,0x0db8a48aeac08b0f  ,0x8385276fcb3a07f2]
    want_res = tmp_res
    niter = 2


  c0, c1=want_res[:2], want_res[2:]

  def undo_iter(c0, c1):
    print('\n\n=========================')
    print('UNNDODOOD ITER ')
    print(Display.disp_list(c0))
    print(Display.disp_list(c1))
    k0 = execute_func(kdf_func, c0)

    p1 = do_reverse(k0, c1[::-1])
    p1 = p1[::-1]
    k1 = execute_func(kdf_func, p1)
    p0 = do_reverse(k1, c0[::-1])
    p0 = p0[::-1]
    return p0, p1

  for i in range(niter):
    c0, c1 = undo_iter(c0, c1)


  print(Display.disp_list(c0))
  print(Display.disp_list(c1))



def main():
  g_data.set_m32(False)
  ctx = Attributize()
  if flags.pid:
    flags.core = f'core.{flags.pid}'
    flags.maps = f'maps.{flags.pid}.txt'
  ActionHandler.Run(ctx)

# KEY DERIVATION
# K1=KDF(X0)
# ENC


#7d74495f745f6e73:695f6c306f635f73
#77447b4349545353:315f4d565f667234
#695f6c306f635f73:7d74495f745f6e73

def get_key(ctx):
  lst = '77447b4349545353:315f4d565f667234:695f6c306f635f73:7d74495f745f6e73'.split(':')
  lst = list(map(bytes.fromhex, lst))
  for x in itertools.permutations(list(range(4))):
    res = b''
    for j in x: res += lst[j][::-1]
    b'SSTIC{Dw4rf_VM_1s_co0l_isn_t_It}'
    print(res)
# Generating full elf as well as the dot graphs at each contraction step
# python main.py --actions=dwarf_gen_all --dwarf-file=./dwarf.state.ir2.pickle  --fixed-sp  --runid=tx1 --elf-outfile=./full.elf

app()
