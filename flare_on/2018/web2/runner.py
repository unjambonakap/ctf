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
from chdrft.emu.func_call import AsyncMachineCaller, FuncCallWrapperGen, SimpleAllocator, FunctionCaller, AsyncFunctionCaller, SimpleBufGen, DummyAllocator
import unicorn as uc
from chdrft.emu.elf import ElfUtils
from chdrft.emu.trace import TraceEvent, WatchedMem
import chdrft.emu.trace as trace
import traceback as tb
import numpy as np
import binascii
import struct


global flags, cache
flags = None
cache = None


def args(parser):
  clist = CmdsList().add(test).add(test_uc)
  ActionHandler.Prepare(parser, clist.lst)
  parser.add_argument('--binary')


def go(*argv):
  x = GdbDebugger()
  elf = x.get_elf()
  x.add_entry_bpt()

  #x.do_execute('set confirm off')
  #end_bpt = x.set_bpt(elf.get_symbol('test_end'), cb=lambda *args: print('kappa'))
  #start_bpt = x.set_bpt(elf.get_symbol('test_wrap'))
  #iter_bpt = x.set_bpt(0x08049559)

  #buf_pos = elf.get_symbol('g_buf')
  #len_pos = elf.get_symbol('g_len')

  print(x.do_execute('b main'))
  print(x.do_execute('info breakpoints'))
  print('laaa')
  x.run(silent=0)
  print(x.do_execute('info breakpoints'))
  print('STOP')
  cur_str = bytearray(b'\x00')
  x.resume()

  tb = []
  cnt = 0
  while True:
    x.show_context()
    if x.is_bpt_active(end_bpt):
      res = x.mem.read_u32(x.reg.esp+4)
      if res == 1:
        print('FOUND SOL ', cur_str)
        break
      tb.append(cnt)
      cur_str[-1] += 1
      cnt = 0

    elif x.is_bpt_active(start_bpt):
      if cur_str[-1] == 128:
        bst = np.argmax(tb)
        cur_str[-1] = bst
        print('ON >> ', cur_str)
        cur_str.append(0)
        x.mem.write_u32(len_pos, len(cur_str))

      x.mem.write(buf_pos, cur_str)


    elif x.is_bpt_active(iter_bpt):
      cnt += 1

    else:
      assert 0
    x.resume()
  print('DONE HERE KAPPA')


def test(ctx):
  launch_gdb('runner', 'go', ctx.binary)

  elf = x.get_elf()

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
      bx = b'0'*50
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
  kern, elf = kernel.Kernel.LoadFromElf(ctx.binary, stack_params=ctx.stack_params, heap_params=ctx.heap_params)

  g_glob.kern = kern
  #kern.mu.hook_add(uc.UC_ERR_WRITE_PROT, kernel.safe_hook(kern.hook_bad_mem_access), None, 0, 2**32-1)
  kern.mu.hook_add(uc.UC_HOOK_MEM_WRITE_UNMAPPED | uc.UC_HOOK_MEM_FETCH_UNMAPPED, kernel.safe_hook(kern.hook_unmapped))
  #kern.mu.hook_add(uc.UC_HOOK_CODE, kernel.safe_hook(kern.hook_code), None, code_low, code_high)
  kern.mu.hook_add(uc.UC_HOOK_CODE, kernel.safe_hook(g_glob.notify), None, 0x0804942e, 0x0804942e)

  #kern.mu.hook_add( uc.UC_HOOK_MEM_READ | uc.UC_HOOK_MEM_WRITE, kernel.safe_hook(kern.hook_mem_access), None, stack_low, stack_high)
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

def test_uc(ctx):
  ctx.stack_params = (2**30, 2**20)
  ctx.heap_params = (2**29, 2**20)
  kern, elf = load_kern(ctx)
  event_log = open('/tmp/evens_{}.out'.format(ctx.runid), 'w')
  vmop_log = open('/tmp/vmop_{}.out'.format(ctx.runid), 'w')
  kern.tracer.cb = lambda x: event_handle(x, event_log, vmop_log)
  ef = ElfUtils(ctx.binary)
  kern.tracer.diff_mode = False

  runner = KernelRunner(kern)
  caller = AsyncMachineCaller(runner, kern.arch, kern.regs, kern.mem)
  client = Client()
  fc = FuncCallWrapperGen(ef, code_db=client.g_code, caller=caller)

  bufacc = MemBufAccessor(kern.mem)
  bufgen = SimpleBufGen(bufacc.read, bufacc.write)
  allocator = DummyAllocator(ctx.heap_params[0], ctx.heap_params[1], bufgen)
  fcaller = AsyncFunctionCaller(allocator, fc)


  ctx.client = client
  handler = AsyncHandler(ctx, kern, fcaller)

  sol=get_sol(kern)
  open('./data.in', 'wb').write(struct.pack('<I', len(sol)) + sol)
  

  start_addr = elf.get_symbol('_start')

  kern.mu.hook_add(uc.UC_HOOK_CODE, kernel.safe_hook(handler), None, start_addr, start_addr+1)
  #kern.mu.hook_add(uc.UC_HOOK_CODE, kernel.safe_hook(handler), None, end_addr, end_addr+1)

  #input_addr = elf.get_symbol('opa_input')
  #output_addr = elf.get_symbol('opa_output')
  #kern.mem.write_u32(input_addr, 12)
  #kern.mem.write_u32(input_addr+4, 88)

  try:
    kern.start()
  except uc.UcError as e:
    print('%s' % e)
    tb.print_exc()

  #print(kern.mem.read(output_addr, 20))
  return


def main():
  g_data.set_m32(True)
  ctx = Attributize()
  ActionHandler.Run(ctx)


app()
#b'wasm_rulez_js_droolz@flare-on.com'
