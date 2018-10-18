#!/usr/bin/env python

from chdrft.cmds import CmdsList
from chdrft.main import app
from chdrft.utils.cmdify import ActionHandler
from chdrft.utils.misc import Attributize
import chdrft.utils.misc as cmisc
import glog
from chdrft.dbg.gdbdebugger import GdbDebugger
from chdrft.dbg.gdbdebugger import GdbDebugger, launch_gdb
import numpy as np
from chdrft.emu.binary import guess_arch
import chdrft.emu.kernel as kernel
from chdrft.emu.structures import StructBuilder, CodeStructExtractor, Structure, StructBackend, g_data, MemBufAccessor
from chdrft.emu.func_call import AsyncMachineCaller, FuncCallWrapperGen, FunctionCaller, AsyncFunctionCaller, SimpleBufGen
import unicorn as uc
from chdrft.emu.elf import ElfUtils
from chdrft.emu.trace import TraceEvent, WatchedMem
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

charset = [i for i in range(128) if curses.ascii.isprint(i)]


class LibcHelper:

  def __init__(self):
    self.x = ctypes.cdll.LoadLibrary(ctypes.util.find_library('c'))


libc = LibcHelper()

rmp = {}
f = 1, 0
for i in range(256):
  rmp[f[0]] = i
  f = (f[0] + f[1]) % (2**64), f[0]

global flags, cache
flags = None
cache = None


def args(parser):
  clist = CmdsList().add(test).add(test_uc).add(test_pin).add(test_perm)
  ActionHandler.Prepare(parser, clist.lst)
  parser.add_argument('--binary')
  parser.add_argument('--core')
  parser.add_argument('--fast_read', action='store_true')


def pin_run(content):
  cmd = 'stdbuf -i0 -o0 pin -t ~/programmation/tools/pin-3.7-97619-g0d0c92f4f-gcc-linux/source/tools/ManualExamples/obj-intel64/inscount0.so -- ./magic'
  print(content)
  with Process(cmd, shell=True) as p:
    p.recv_until('Enter key')
    p.send(b'\n'.join(content))
    p.close_stdin()
    res = p.get_to_end(1)
  with open('./inscount.out', 'r') as f:
    inscount = int(f.read().split()[1])
  return res, inscount


def test_pin(ctx):
  content = []
  content.append(bytearray(b'a' * 5))
  for i in range(128):
    if curses.ascii.isprint(i):
      content[0][2] = i
      res = pin_run(content)
      print(i, res[1])
  print(res)


class Solver:

  def __init__(self, x):
    elf = x.get_elf()
    x.add_entry_bpt()
    main_addr = 0x4038D4
    self.main_bpt = x.set_bpt(main_addr)

    self.check_addr = 0x0000000000403B5D
    self.check_bpt = x.set_bpt(self.check_addr)

    failure_addr = 0x0000000000402CC7
    self.failure_bpt = x.set_bpt(failure_addr)

    self.polycheckers_addr = 0x0402F06
    #self.polycheckers_bpt = x.set_bpt(self.polycheckers_addr)

    badlen_addr = 0x0402E2B
    self.badlen_bpt = x.set_bpt(badlen_addr)
    badpolycheckers_addr = 0x0402F0F
    self.badpolycheckers_bpt = x.set_bpt(badpolycheckers_addr)
    self.x = x

    init_perm_addr = 0x0000000000403BC7
    self.init_perm_bpt = x.set_bpt(init_perm_addr)
    self.polycheckers_ret_addr = 0x0000000000402F08
    self.polycheckers_ret_bpt = x.set_bpt(self.polycheckers_ret_addr)

  def go(self, content):

    with ManagedBidirectionalFifo() as fx:
      #fx.activate()
      time.sleep(0.1)
      x = self.x

      buf = b'\r\n'.join(content) + b'\r\n'
      fname = 'data.in'
      with open(fname, 'wb') as f:
        f.write(buf)

      #self.x.run_managed_fifo(fx)
      self.x.run_with_fifo(input=fname, silent=True)

      self.fib1_check_addr = 0x000400D79
      self.fib1_bpt = x.set_hard_bpt_exe(self.fib1_check_addr)

      x.resume()

      if 0:
        print('SENDING', buf)
        fx.fifo.send(buf)
        fx.fifo.wfile.flush()
        fx.fifo.wfile.close()
        print('DONE SENDING')
        x.resume()
        x.show_context()

        #print(fx.fifo.recv(10))
        #print('AFTER SEND >> ', fx.fifo.recv_until('Enter key', timeout=2))
      status = Attributize()
      status.challengeround = 0
      status.challengeiter = []
      status.polycall = []
      status.fibdata = []
      status.ok = 0

      cur_target = None
      while True:
        assert x.get_status() != x.statuses.TERMINATED
        x.resume()
        if x.is_bpt_active(self.badlen_bpt):
          wantlen_be = x.regs.rax
          status.wantlen_be = wantlen_be
          status.badlen = 1
          break
        if x.is_bpt_active(self.check_bpt):
          status.challengeiter.append(0)
          status.challengeround += 1

        if x.is_bpt_active(self.polycheckers_ret_bpt):
          res = x.regs.rax
          if res != 0: continue

          assert status.challengeround == len(content)
          base_addr = 0x605100
          stride = 9 * 32
          len_offset = 0x10
          pos_offset = 0xc
          target_offset = 0
          content_offset = 0x20
          itercount = x.mem.read_u32(x.regs.rbp - 4)

          for itercount in range(32):
            addr = base_addr + stride * itercount
            n = x.mem.read_u32(addr + len_offset)
            pos = x.mem.read_u32(addr + pos_offset)
            target = x.mem.read_u64(addr + target_offset)
            content_addr = addr + content_offset
            print(itercount, n, pos, target, content_addr)
          return

          rbp_in_offset = -0x18
          buf_addr = x.mem.read_u64(x.regs.rbp + rbp_in_offset)
          print('Trying ', n, pos, itercount)

          for cnd in itertools.product(charset, repeat=n):
            cx = bytearray(cnd)
            x.regs.rip = self.polycheckers_addr
            x.regs.rcx = target
            x.regs.rdx = content_addr
            x.regs.rsi = n
            x.regs.rdi = buf_addr

            x.mem.write(buf_addr, cx)
            x.resume()
            assert x.is_bpt_active(self.polycheckers_ret_bpt)
            if x.regs.rax != 0:
              content[-1][pos:pos + n] = cx
              print('FOUND FOR', cx, pos, content[-1])
              break
          else:
            assert 0

          #for j in range(n):
          #  target = x.mem.read_u64(addr + content_off + 8 * j)
          #  print(target, pos)
          #  expected[pos+j] = rmp[target]
          #nmax = max(nmax, pos + n)

        if x.is_bpt_active(self.badpolycheckers_bpt):
          status.badpoly = 1
          break

        if x.is_bpt_active(self.init_perm_bpt):
          status.on_init_perm = 1
          status.file_access = x.mem.get_str(x.regs.rdi)
          break

        #if x.regs.ins_pointer == self.fib1_check_addr:
        #  target = x.regs.rax
        #  x.regs.rdx = x.regs.rax
        #  status.fibdata.append(target)

      return status


def go(*argv):
  x = GdbDebugger()

  c0 = bytearray(b'#' * 0x200)
  content = [c0]
  c0[2:5] = b'ds '
  c0[44:44 + 2] = b'in'
  c0[16:16 + 1] = b'.'
  solver = Solver(x)

  status = solver.go(content)

  res = []
  print(status)
  for i in status.fibdata:
    res.append(rmp[i])
  print(bytes(res))


def test(ctx):
  launch_gdb('runner', 'go', ctx.binary)


class Client:

  def __init__(self):
    g_code = StructBuilder()
    g_code.add_extractor(CodeStructExtractor('int test(const char *a, int len);', ''))
    g_code.build(extra_args=StructBuilder.opa_common_args())
    self.g_code = g_code
    self.consts = g_code.consts
    self.tb1 = []
    self.tb2 = []


class Glob:

  def __init__(self):
    self.reset()
    self.kern = None

  def reset(self):
    self.counter = 0
    self.tb1 = []
    self.tb2 = []

  def notify(self, *args):
    self.counter += 1
    self.tb1.append(self.kern.regs.cl)
    self.tb2.append(self.kern.regs.al)


def get_sol(kern):
  target_addr = kern.elf.get_symbol('pb')
  target = kern.mem.read(target_addr, 0x58)
  buf = bytearray()
  bad = 0
  for i in range(len(target)):
    buf.extend([0, target[i]])
    if target[i] & 0x80: bad += 1
  buf.extend([0] * 2 * bad)
  return buf


class AsyncHandler:

  def __init__(self, ctx, kern, caller_func):
    self.ctx = ctx
    self.kern = kern
    self.caller_func = caller_func
    self.handler = self.handle()

  def __call__(self, *args, **kwargs):
    next(self.handler)

  def handle(self):
    nmax = 30
    buf = self.caller_func.allocator.alloc(0x300)
    mem = self.kern.mem
    try:

      bx = get_sol(self.kern)
      bx = b'0' * 50
      mem.write(buf, bx)
      g_glob.reset()

      yield self.caller_func.test(buf, len(bx))

      res = self.caller_func.result()
      print(bytes(g_glob.tb1))
      print(bytes(g_glob.tb2))
      print(res)

      #for n in range(1, nmax):
      #  print(n)
      #  cur = bytearray()
      #  for i in range(n):
      #    tb = []
      #    cur.append(0)
      #    for c in range(256):
      #      cur[i] = c
      #      self.kern.mem.write(buf, cur)
      #      g_glob.reset()

      #      yield self.caller_func.test(buf, n)
      #      res = self.caller_func.result()
      #      tb.append(g_glob.counter)

      #      if res:
      #        print('FOUND RESULT ', cur)
      #        yield
      #        self.kern.stop()
      #        return
      #    print('GOT >> ', tb)
      #    best = np.argmax(tb)
      #    cur[i] = best

      print('no solution found')
      #yield
      self.kern.stop()

    except Exception as e:
      tb.print_exc()
      raise e


g_glob = Glob()


def load_kern(ctx):
  code_low = 1
  code_high = 0
  stack_low = 1
  stack_high = 0
  log_file = '/tmp/info.out_{}'.format(ctx.runid)
  kern, elf = kernel.Kernel.LoadFromElf(ctx.core, hook_imports=True, orig_elf=ctx.binary)

  g_glob.kern = kern
  #kern.mu.hook_add(uc.UC_ERR_WRITE_PROT, kernel.safe_hook(kern.hook_bad_mem_access), None, 0, 2**32-1)
  kern.mu.hook_add(
      uc.UC_HOOK_MEM_WRITE_UNMAPPED | uc.UC_HOOK_MEM_FETCH_UNMAPPED,
      kernel.safe_hook(kern.hook_unmapped)
  )
  #kern.mu.hook_add(uc.UC_HOOK_CODE, kernel.safe_hook(kern.hook_code), None, code_low, code_high)

  if 0:
    kern.mu.hook_add(
        uc.UC_HOOK_MEM_READ | uc.UC_HOOK_MEM_WRITE, kernel.safe_hook(kern.hook_mem_access), None, 1,
        0
    )
  return kern, elf


class KernelRunner:

  def __init__(self, kern):
    self.kern = kern

  def __call__(self, end_pc):
    pass


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


class KernBaseImports:

  def __init__(self, kern):
    self.kern = kern
    self.mem = kern.mem
    self.regs = kern.regs
    for x in KernBaseImports.__dict__.keys():
      if not isinstance(x, str) or not x.endswith('_hook'): continue
      self.kern.defined_hooks[x[:-5]] = getattr(self, x)
    self.buffer = b''
    self.f = None

  def fseek_hook(self, _):
    stream = self.regs.rdi
    offset = self.regs.rsi
    whence = self.regs.rdx
    self.f.seek(offset, whence)
    return 0

  def ftell_hook(self, _):
    return self.f.tell()

  def fread_hook(self, _):
    buf = self.regs.rdi
    sz = self.regs.rsi
    n = self.regs.rdx
    read = self.f.read(sz * n)
    self.mem.write(buf, read)
    return len(read)

  def fclose_hook(self, _):
    print('FCLOSE')
    self.f.close()
    return 0

  def malloc_hook(self, _):
    n = self.regs.rdi
    return self.kern.heap.alloc(n)

  def fopen_hook(self, _):
    pos = self.regs.rdi
    fname = self.mem.get_str(pos)
    self.f = open(fname, 'rb')
    assert 0

    return 4

  def strlen_hook(self, _):
    pos = self.regs.rdi
    res = len(self.mem.get_str(pos))
    return res

  def rand_hook(self, _):
    return libc.x.rand()

  def srand_hook(self, _):
    print('ON SRAND')
    libc.x.srand(self.regs.rdi)
    return 0

  def puts_hook(self, _):
    print('PUTS >> ', self.mem.get_str(self.regs.rdi))
    return 0

  def printf_hook(self, _):
    fmt = self.mem.get_str(self.regs.rdi)
    print('PRINTF >> ', fmt)
    if fmt.startswith(b'Congrats'):
      print(self.mem.get_str(self.regs.rsi))
    return 0

  def memcmp_hook(self, _):
    a = self.regs.rdi
    b = self.regs.rsi
    n = self.regs.rdx
    if self.mem.read(a, n) == self.mem.read(b, n):
      return 0
    return 1

  def memcpy_hook(self, _):
    n = self.regs.rdx
    self.mem.write(self.regs.rdi, self.mem.read(self.regs.rsi, n))
    return n

  def fgets_hook(self, _):
    buf = self.regs.rdi
    n = self.regs.rsi

    print('FGETS ', n)
    assert 0
    cnd = self.buf[:n - 1]
    firstnl = self.buf.find(b'\n')
    if firstnl != -1:
      cnd = cnd[firstnl + 1]
    cnd += b'\x00'
    print('GETS ', cnd)
    self.mem.write(buf, cnd)
    if len(cnd) == 1: return 0
    return buf


class AsyncHandler:

  def __init__(self, solver, kern):
    self.kern = kern
    self.solver = solver
    self.regs = kern.regs
    self.mem = kern.mem
    self.handler = self.handle()

  def __call__(self, *args, **kwargs):
    next(self.handler)

  def handle(self):
    first = True
    while True:
      if not first: yield
      first = False

      res = self.regs.rax

      base_addr = 0x605100
      stride = 9 * 32
      len_offset = 0x10
      pos_offset = 0xc
      target_offset = 0
      content_offset = 0x20
      itercount = self.mem.read_u32(self.regs.rbp - 4)

      #for itercount in range(32):
      addr = base_addr + stride * itercount
      n = self.mem.read_u32(addr + len_offset)
      pos = self.mem.read_u32(addr + pos_offset)
      target = self.mem.read_u64(addr + target_offset)
      content_addr = addr + content_offset

      rbp_in_offset = -0x18
      buf_addr = self.mem.read_u64(self.regs.rbp + rbp_in_offset)
      print(
          'ON POLYCHECK >> ', res, self.solver.challenge_round, n, pos, itercount, hex(target),
          hex(content_addr), hex(buf_addr), res
      )

      if 0:
        force = self.solver.challenge_round == 12 and itercount == 6
      else:
        force = 0
      bypass = 0 and self.solver.challenge_round == 12 and itercount >= 5
      if not bypass and not force and res != 0: continue
      was_ok = res
      now_sp = self.solver.get_sp_snapshot()
      prev_sp = self.solver.sp_content
      prev = bytes(self.solver.cur_buf[pos:pos + n])

      # fuckoff
      #for i in range(len(now_sp)):
      #  if now_sp[i] != prev_sp[i]:
      #    print('diff at ', hex(i))

      cnt = 0
      if 0:
        tb = []
        self.kern.ignore_mem_access = False
        open(f'/tmp/logswrite_before.out', 'w').write('\n'.join(self.kern.info))
        self.kern.info = []

      def prepare_exec(buf):
        self.regs.rip = self.solver.polycheckers_addr
        self.regs.rcx = target
        self.regs.rdx = content_addr
        self.regs.rsi = n
        self.regs.rdi = buf_addr + pos
        self.solver.restore_sp()

        self.mem.write(buf_addr+pos, buf)

      cx = None

      if 0 or force:
        code = self.mem.read(target, 0x300)
        print(code, target)
        self.kern.arch.mc.disp_ins(code, target)

        self.kern.ignore_mem_access = False
        prepare_exec(prev)
        yield
        with open(f'/tmp/logswrite_before.out', 'w') as f:
          f.write('\n'.join(self.kern.info))
        print('RESULT >> ', self.regs.rax)
        self.kern.info = []
        s1 = self.solver.get_sp_snapshot()

        prepare_exec(prev)
        yield
        with open(f'/tmp/logswrite_before.out2', 'w') as f:
          f.write('\n'.join(self.kern.info))
        print('RESULT >> ', self.regs.rax)
        self.kern.info = []
        s2 = self.solver.get_sp_snapshot()
        assert s1 == s2
        print(self.regs.rsp)
        for i in range(len(s1)):
          if s1[i] != now_sp[i]: print('diFF at ', hex(self.solver.ctx_at + i))
        assert now_sp == s1

      if 1:
        cx = self.solver.fast_solve(target, n, content_addr, prev_sp)
      else:
        print('try solve')
        for cnd in itertools.product(charset, repeat=n):
          cnt += 1
          cx = bytearray(cnd)
          prepare_exec(cx)
          yield
          if self.regs.rax != 0:
            print('OK FOR ', cx)
            break
          #open(f'/tmp/logswrite{cnt}.out', 'w').write('\n'.join(self.kern.info))
          #self.kern.info = []
        else:
          assert 0

      if bytes(cx) == bytes(prev):
        assert now_sp == self.solver.get_sp_snapshot()

      if force:
        print('FAST SOLVE >> ', cx, prev, bytes(cx) == bytes(prev))
      if 0 and was_ok and bytes(cx) != bytes(prev):
        code = self.mem.read(target, 0x300)
        print(code, target)
        self.kern.arch.mc.disp_ins(code, target)
        assert bytes(cx) == bytes(prev)

      self.solver.cur_buf[pos:pos + n] = cx
      print('FOUND FOR', cx, pos, self.solver.cur_buf, prev)
      prepare_exec(cx)
      yield
      assert self.regs.rax != 0
      #assert 0
    self.kern.stop()
    yield


class UCSolver:

  def __init__(self, kern):
    self.kern = kern
    self.imports_helper = KernBaseImports(kern)
    self.regs = kern.regs
    self.mem = kern.mem
    self.cur_buf = None
    self.caller = swig_unsafe.hack_ctf_flare_on_2018_magic_swig
    self.ofile = open('./test.cur.out', 'wb')

    self.check_addr = 0x0000000000403B5D
    self.challenge_round = 0
    self.hook_addr(self.check_addr, self.newchallenge_hook)

    failure_addr = 0x0000000000402CC7
    self.hook_addr(failure_addr, self.failure_hook)

    self.polycheckers_addr = 0x0402F06
    #self.polycheckers_bpt = x.set_bpt(self.polycheckers_addr)
    self.polychecker_hook = AsyncHandler(self, self.kern)

    self.prev_polychecker_addr = 0x402F03
    self.hook_addr(self.prev_polychecker_addr, self.prev_polychecker_hook)

    init_perm_addr = 0x0000000000403BC7
    #self.init_perm_bpt = x.set_bpt(init_perm_addr)
    self.polycheckers_ret_addr = 0x0000000000402F08
    self.hook_addr(self.polycheckers_ret_addr, self.polychecker_hook)

    self.replace_file_addr = 0x403167
    self.hook_addr(self.replace_file_addr, self.replace_file_hook)
    read_file_addr = 0x0403050
    self.hook_addr(read_file_addr, self.read_file_hook)

    self.tempfile = './magic.perm'
    self.file_cont = open(flags.binary, 'rb').read()
    self.fast_read = flags.fast_read
    if self.fast_read:
      self.tempfile = None
    else:
      self.write_tempfile(self.file_cont)

    self.kern.defined_hooks['fopen'] = self.fopen_hook
    self.kern.defined_hooks['fgets'] = self.fgets_hook

  def fast_solve(self, target, n, content_addr, sp_content):
    func_data = self.mem.read(target, 0x1000)
    content_data = self.mem.read(content_addr, 9 * 32)
    sol = self.caller.do_solve(func_data, n, content_data, sp_content)
    return sol

  def write_tempfile(self, buf):
    with open(self.tempfile, 'wb') as f:
      f.write(buf)

  def fgets_hook(self, _):
    bufaddr = self.regs.rdi
    print('FGETS >> ', self.regs.rsi)
    if self.challenge_round >= len(self.content):
      self.content.append(bytearray(b'a' * 100))
    print('HOOK >> ', self.content[self.challenge_round])
    self.cur_buf = self.content[self.challenge_round]
    self.mem.write(bufaddr, self.cur_buf + b'\n')
    return bufaddr

  def fopen_hook(self, _):
    print('START FOPEN')
    self.imports_helper.f = open(self.tempfile, 'rb')
    return 4

  def read_file_hook(self, *args):
    if not self.fast_read: return

    buf_ptr = self.regs.rsi
    len_ptr = self.regs.rdx

    n = len(self.file_cont)
    addr = self.kern.heap.alloc(n)
    self.mem.write(addr, self.file_cont)
    self.mem.write_ptr(buf_ptr, addr)
    self.mem.write_ptr(len_ptr, n)
    self.kern.mc.ret_func()

  def replace_file_hook(self, *args):
    fname = self.regs.rdi
    bufaddr = self.regs.rsi
    n = self.regs.rdx
    buf = self.mem.read(bufaddr, n)
    import hashlib
    print('replace ', self.mem.get_str(fname), hashlib.md5(buf).hexdigest())
    if self.fast_read: self.file_cont = buf
    else: self.write_tempfile(buf)

    self.kern.mc.ret_func()

  def newchallenge_hook(self, *args):
    if self.challenge_round > 0:
      now = self.content[self.challenge_round - 1]
      self.ofile.write(now + b'\n')
      self.ofile.flush()
      print((b'\n'.join(self.content[:self.challenge_round])).decode())
    print('ON ROUND >> ', self.challenge_round)
    price = self.mem.get_str(self.regs.rbp - 0xa0)
    print('CURPRICE ', price)
    self.challenge_round += 1

  def hook_addr(self, addr, handler):
    self.kern.mu.hook_add(uc.UC_HOOK_CODE, kernel.safe_hook(handler), None, addr, addr + 1)

  def get_sp_snapshot(self):
    return self.mem.read(self.regs.rsp - 0x300, 0x300)

  def restore_sp(self):
    self.mem.write(self.regs.rsp - 0x300, self.sp_content)

  def prev_polychecker_hook(self, *args):
    self.sp_content = self.get_sp_snapshot()
    self.ctx_at = self.regs.rsp - 0x300
    itercount = self.mem.read_u32(self.regs.rbp - 4)
    #if self.challenge_round == 12 and itercount == 5:
    #  self.kern.ignore_mem_access = False

  def failure_hook(self, *args):
    print('ON FAILURE')
    self.kern.stop()

  def go(self, content):
    self.imports_helper.buf = b'\n'.join(content)
    self.content = content


def test_uc(ctx):
  kern, elf = load_kern(ctx)
  event_log = open('/tmp/evens_{}.out'.format(ctx.runid), 'w')
  vmop_log = open('/tmp/vmop_{}.out'.format(ctx.runid), 'w')
  kern.tracer.cb = lambda x: event_handle(x, event_log, vmop_log)
  ef = ElfUtils(ctx.binary)
  kern.tracer.diff_mode = False
  solver = UCSolver(kern)
  global charset
  kern.ignore_mem_access = True

  clist = list([bytearray(x.rstrip(b'\n')) for x in open('./test.in', 'rb').readlines()])
  solver.go(clist)

  #runner = KernelRunner(kern)
  #caller = AsyncMachineCaller(runner, kern.arch, kern.regs, kern.mem)
  #client = Client()
  #fc = FuncCallWrapperGen(ef, code_db=client.g_code, caller=caller)

  #bufacc = MemBufAccessor(kern.mem)
  #bufgen = SimpleBufGen(bufacc.read, bufacc.write)
  #allocator = DummyAllocator(ctx.heap_params[0], ctx.heap_params[1], bufgen)
  #fcaller = AsyncFunctionCaller(allocator, fc)
  #ctx.client = client
  #handler = AsyncHandler(ctx, kern, fcaller)

  #kern.mu.hook_add(uc.UC_HOOK_CODE, kernel.safe_hook(handler), None, start_addr, start_addr+1)
  #kern.mu.hook_add(uc.UC_HOOK_CODE, kernel.safe_hook(handler), None, end_addr, end_addr+1)

  try:
    kern.start()
  except uc.UcError as e:
    print('%s' % e)
    tb.print_exc()

  #print(kern.mem.read(output_addr, 20))
  return


def test_perm(ctx):
  lines = open('./test.in').readlines()
  tb = []
  for line in lines:
    x = defaultdict(list)
    line.strip()
    for i, c in enumerate(line):
      x[c].append(i)
    print(len(line))
    tb.append(x)
  n = len(lines[0]) - 1
  can = defaultdict(lambda: set(range(n)))
  for i in range(len(lines) - 1):
    for j in range(n):
      can[j].intersection_update(tb[i + 1][lines[i][j]])
    break
  for i in range(n):
    print(i, can[i])
  print(lines)


def main():
  g_data.set_m32(False)
  ctx = Attributize()
  ActionHandler.Run(ctx)


app()
#b'wasm_rulez_js_droolz@flare-on.com'
