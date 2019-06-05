#!/usr/bin/env python

from chdrft.cmds import CmdsList
from chdrft.main import app
from chdrft.utils.cmdify import ActionHandler
from chdrft.utils.misc import Attributize
import chdrft.utils.misc as cmisc
import glog
import chdrft.utils.Z as Z
import chdrft.utils.K as K
import sqlite3
import sys
from sm4 import encrypt, decrypt, encrypt_ecb
import llvmlite.ir as ll
import llvmlite.binding as llvm
import ctypes
import numpy as np
import logging
import z3

arch = K.guess_arch('aarch64')

smem_base = 0x413000

global g_ctx
global flags, cache
g_ctx = None
flags = None
cache = None
g_qemu_path = '/home/benoit/packets/qemu/'
g_gdb_binary = '/home/benoit/packet/gdb-8.2.1/opt/bin/aarch64-linux-gnu-gdb'

qemu_bin = '/home/benoit/packets/qemu/aarch64-softmmu/qemu-system-aarch64'
qemu_bin = 'qemu-system-aarch64'

good_file_path = '/root/safe_02/decrypted_file'
bad_file_path = '/root/safe_02/decrypted_fbad'
init = 0xFFFF000008590198
init_start_km = 0xFFFF000008590194
ioctl_start_km = 0xFFFF000008590038
feed = 0xFFFF000008590198
qq_start_km = 0xFFFF000008590200
query_start_km = 0xFFFF0000085903E8
trace_to = 0x000000000e2000a8
dispatch_func = 0x00E2005A4
init_done = 0xE0310DC
ioctl_done_km = 0xFFFF0000085901E0
init_done_km = 0xFFFF00000859019C
init_done_km_after_free = 0xFFFF0000085901a4
feed_start_km = 0xFFFF0000085904DC
feed_done_km = 0xFFFF000008590524
qq_done_km = 0xFFFF000008590230
query_done_km = 0xFFFF000008590428
bl2_entrypoint = 0x00E030000
bl2_entrypoint_ret = 0x000000000E035A20

kern_smc_addr = 0xffff000010093958
kern_vec_smc = 0xffff000010082280

kern_uart_putchar = 0xffff0000103c6e78
op_begin = 0x0E200C34
proc_done_elf = 0x4008C8
tsp_init = 0x00E034098
tsp_handler = 0xE034158
tsp_handler_end = 0xE034414
oem_svc_handler = 0xE032014

dispatch_loop192 = 0x000000000e200884
oem_loop192 = 0x0E031608
oem_svc_br = 0xE0311BC

work_begin = 0x0E200C98
work_end = 0x0E200CA8
setup_begin = 0x0E200CF8
setup_end = 0x0E200D4C

vmop_begin = 0xE200E84
vmop_end = 0xE2010A8
end_trigger = 0x0000E2009D8
result_check1 = 0x000000000e20085c
result_check2 = 0x000000000e200af8
dispatcher_quit = 0x000E2007EC

g_key_pos = 0x100020
g_check_pos = 0x100000
g_mem_len = 0x100040
g_key_len = 0x20
g_mainfunc_name = 'gogo'

g_final_expected = b'pr.a.rfg.cnf.fv.snpvyr@ffgvp.bet'
g_check_start_op = 0xaf30  # when final check starts

kern_svc_ret = 0xffff00001009395c
ev_loop192 = cmisc.Attr(
    addr=0xe0316f0,
    name='loop192',
    regs=['x0', 'x23'],
    mem=[cmisc.Attr(reg='x0', size=8, offset=0),
         cmisc.Attr(reg='x23', size=8, offset=0)]
)
g_PREV_KEY = 'prev'


def out(*args, **kwargs):
  if g_ctx.printfile is not None:
    print(*args, **kwargs, file=g_ctx.printfile)
  print(*args, **kwargs)


hook_mem_r_begin = 0xe203204

key_0123 = bytearray(range(32))
key_aaaa = bytes.fromhex('a' * 64)
key_ffff = bytes.fromhex('f' * 64)
key_0000 = bytes.fromhex('0' * 64)


def args(parser):
  app.override_flags['pickle_cache'] = True
  clist = CmdsList()
  parser.add_argument('--qemu-pts')
  parser.add_argument('--cmd')
  parser.add_argument('--action2')
  parser.add_argument('--infile')
  parser.add_argument('--evtype')
  parser.add_argument('--infiles', nargs='*', type=str)
  parser.add_argument('--outfile')
  parser.add_argument('--elf-outfile')
  parser.add_argument('--output-dir', type=str, default='/tmp')
  parser.add_argument('--trace-to', type=cmisc.to_int, default=0)
  parser.add_argument('--trace-to-str')
  parser.add_argument('--trace-from-str')
  parser.add_argument('--trace-from', type=cmisc.to_int, default=0)
  parser.add_argument('--nskip-from', type=cmisc.to_int, default=0)
  parser.add_argument('--stop-line', type=cmisc.to_int, default=-1)
  parser.add_argument('--inscount', type=cmisc.to_int, default=2**100)
  parser.add_argument('--count', type=cmisc.to_int, default=1)
  parser.add_argument('--modkey', type=str)
  parser.add_argument('--debug-ids', type=cmisc.to_int, nargs='*')

  parser.add_argument('--debug-regs', action='store_true')
  parser.add_argument('--cheat-mode', action='store_true')
  parser.add_argument('--dispatcher-ev', action='store_true')
  parser.add_argument('--func-analysis-ev', action='store_true')
  parser.add_argument('--br-probes-ev', action='store_true')
  parser.add_argument('--enable-aes-to-dec', action='store_true')
  parser.add_argument('--enable-aes-to-enc', action='store_true')
  parser.add_argument('--vmop-probes-ev', action='store_true')
  parser.add_argument('--kern-ev', action='store_true')
  parser.add_argument('--op-probes-ev', action='store_true')
  parser.add_argument('--disable-bypass', action='store_true')
  parser.add_argument('--only-name', action='store_true')
  parser.add_argument('--enable-full-print', action='store_true')
  parser.add_argument('--setup-begin', action='store_true')
  parser.add_argument('--solve-ev', action='store_true')
  parser.add_argument('--only-gdb', action='store_true')
  parser.add_argument('--recover-output', action='store_true')
  parser.add_argument('--simplify-set', action='store_true')

  parser.add_argument('--from-shell', action='store_true')
  parser.add_argument('--bad-prog', action='store_true')
  default_key = key_0123.hex()
  parser.add_argument('--prog-key', type=str, default=default_key)
  parser.add_argument('--key-a', action='store_true')
  ActionHandler.Prepare(parser, clist.lst, global_action=1)


class InterfaceScripter(Z.ExitStack):

  def __init__(self, cmd_args=None, p=None, done_check_pattern=None, pattern_size=20, **cmd_kwargs):
    super().__init__()
    self.p = p
    self.cmd_args = cmd_args
    self.cmd_kwargs = cmd_kwargs
    self.done_check_pattern = done_check_pattern
    self.pattern_size = pattern_size
    self.pending = None

  def run(self, data):
    pattern = self.generate_pattern()
    send_done_cmd = self.done_check_pattern.format(pattern)
    self.p.send(data + send_done_cmd)
    self.ev = Z.threading.Event()
    self.pending = pattern

  def check_waiting(self):
    return self.pending is not None

  def run_and_wait(self, data):
    self.run(data)
    return self.wait()

  def wait(self):
    glog.info(f'Waiting for pattern {self.pending}')
    res = self.p.recv_until(self.pending)
    a = res[:-len(self.pending)]
    self.pending = None
    return a

  def __call__(self, data):
    return self.run_and_wait(data)

  def generate_pattern(self):
    return Z.os.urandom(self.pattern_size).hex()

  def __enter__(self):
    super().__enter__()
    if self.p is None:
      self.p = Z.Process(self.cmd_args, **self.cmd_kwargs)
    self.enter_context(self.p)
    Z.time.sleep(0.1)
    return self


class EnterCtxRetry(Z.ExitStack):

  def __init__(self, obj, try_count=1, retry_wait_s=1):
    super().__init__()
    self.obj = obj
    self.try_count = try_count
    self.retry_wait_s = retry_wait_s

  def __enter__(self):
    super().__enter__()
    for i in range(self.try_count):
      try:
        self.obj.__enter__()
      except KeyboardInterrupt:
        raise
      except Exception:
        glog.info(f'On try {i}, exception: {Z.tb.format_exc()}')
        continue

      self.push(self.obj)
      break
    else:
      raise Exception('max retry for EnterCtxRetry')

    return self.obj


def get_qemu_interface(cmd=None, p=None):
  interface = InterfaceScripter(
      cmd=cmd, p=p, done_check_pattern='\np /x 0x11{}\n', shell=1, pattern_size=7
  )
  app.global_context.enter_context(interface)
  return interface


def get_shelllike_interface(cmd, **kwargs):
  interface = InterfaceScripter(cmd, done_check_pattern=';echo {};\n', shell=1)
  app.global_context.enter_context(EnterCtxRetry(interface, **kwargs))
  return interface


def get_gdb_interface(cmd):
  interface = InterfaceScripter(cmd, done_check_pattern='\np /x 0x11{}\n', shell=1, pattern_size=7)
  return app.global_context.enter_context(interface)


def find_qemu_pts(tube):
  m = b'char device redirected to (/dev/pts/[0-9]+)\s'
  pm = cmisc.PatternMatcher.fromre(m)
  res = tube.recv_until(pm)
  cdev = pm.result.group(1)
  return cdev


def get_qemu(pts=None):
  if pts is None:
    flash_file = cmisc.path_here('../flash.bin')
    rom_file = cmisc.path_here('../rom.bin')
    cmd = f'{qemu_bin} -nographic -machine virt,secure=on -cpu max -smp 1 -m 1024 -bios {rom_file} -semihosting-config enable,target=native -device loader,file={flash_file},addr=0x04000000 -netdev user,id=network0,hostfwd=tcp:127.0.0.1:5555-192.168.200.200:22 -net nic,netdev=network0 -serial stdio -monitor pty 2>&1'
    px = Z.Process(cmd, shell=1)
    app.global_context.enter_context(px)
    pts = find_qemu_pts(px)
    print('GOOOT PTS >> ', pts)
  return get_qemu_interface(p=Z.Serial(pts))


def get_ssh():
  return get_shelllike_interface(
      'sshpass -p sstic ssh root@0.0.0.0 -p 5555', try_count=10, retry_wait_s=1
  )


def get_gdb():
  elf_aarch64 = cmisc.path_here('./resources/decrypted_file')
  return get_gdb_interface(f'aarch64-linux-gnu-gdb -q {elf_aarch64}')


def get_gdb_res(x):
  import re
  res = int(re.search('= 0x([0-9a-f]+)', x.decode()).group(1), 16)
  glog.info(f'GOT res {res:x}')
  return res


def test_interface(ctx):
  if 1:
    with Z.Serial('/dev/pts/1') as sx:
      sx.send('help\n')
      print(sx.recv(10))
      print(sx.trash())
      return
  if 1:
    ssh = get_ssh()
    print(ssh('ls'))
    return
  if 0:
    ix = get_shelllike_interface('/bin/bash')
    print(ix('ls'))

  if 1:
    qx = get_qemu(flags.qemu_pts)
    print(qx('help').decode())

  if 0:
    qx = get_gdb()
    print(qx('help').decode())


def extract_tz_app(ctx):
  start = 0x44DBD8
  end = 0x54EBE8
  elf = Z.ElfUtils('./resources/decrypted_file')
  res = elf.get_range(start, end)
  with open('./tz.app', 'wb') as f:
    f.write(res)


def qemu_trace(ctx):

  gx = get_gdb()
  if flags.from_shell:
    qx, sx = get_qemu_and_ssh(self.ctx)
  else:
    qx = get_qemu(ctx.qemu_pts)
    sx = get_ssh()

  Z.time.sleep(0.2)
  qx('stop')
  print('stopping')
  qx('trace-file off')

  qx('gdbserver')
  gx('target remote :1234')

  #gx(f'hb *{init_done}')
  ##gx(f'hb *{feed}')
  gx(f'hb *{init_start_km}')
  #gx(f'hb *{qq}')

  sx.run(ctx.prog_cmd)

  if 0:
    bpt_ioctl_start_km = gx(f'hb *{ioctl_start_km}')
    gx.resume()
    u = get_gdb_res(gx('p $x1'))
    print(u)
    assert u == 0xc0105300
    gx('c')
    assert get_gdb_res(gx('p $x1')) == 0xc0105301
    gx('c')
    assert get_gdb_res(gx('p $x1')) == 0xc0105302
    gx('c')
    assert get_gdb_res(gx('p $x1')) == 0xc0105303
    gx(f'hb *{ioctl_done_km}')
    print(gx(f'trace-run {ioctl_done_km}').decode())
    return

  if 0:
    gx(f'hb *{ioctl_start_km}')
    gx(f'hb *{init_done_km}')
    gx(f'hb *{feed_done_km}')
    gx(f'hb *{ioctl_done_km}')
    gx('c')
    assert get_gdb_res(gx('p $x1')) == 0xc0105300
    gx('c')
    x20 = get_gdb_res(gx('p $x20'))
    print('got ', hex(x20))

    gx(f'set $x21={x20}')
    gx(f'set $pc={feed_start_km}')
    return
    gx(f'trace-run {feed_done_km}')
    return
    gx('c')
    assert get_gdb_res(gx('p $pc')) == feed_done_km

    gx(f'set $pc={qq_start_km}')
    gx('c')
    assert get_gdb_res(gx('p $pc')) == ioctl_done_km

    gx(f'set $pc={query_start_km}')
    gx('c')
    assert get_gdb_res(gx('p $pc')) == ioctl_done_km
    print('GOOT XO>> ', get_gdb_res(gx('p $x0')))
    return
    #gx('c')
    #assert get_gdb_res(gx('p $x1')) == 'c0105302'
    print(gx(f'trace-run {ioctl_end}').decode())

    #gx('dump memory ./dumps/securemem-e030-e1550000.bin 0xe030000 0xe155000')
    #gx('dump memory ./dumps/securemem-e2-e3.bin 0xe200000 0xe300000')
    return

  print('goog la', ctx.trace_file)
  gx('c')

  qx(f'trace-file set {ctx.trace_file}')
  qx('trace-event guest_mem_before_exec on')
  qx('trace-event guest_user_syscall on')
  qx('trace-event guest_user_syscall_ret on')
  qx('trace-event exec_tb on')
  qx('trace-event memory_region_ram_device_read on')
  qx('trace-event memory_region_ram_device_write on')
  qx('trace-event exec_tb_nocache on')

  print(gx('context').decode())
  qx('trace-file on')
  gx.run('c')
  gx.wait()
  print(gx('context').decode())
  assert 0
  if 1:
    sx.wait()
    qx('stop')
  else:
    gx('c')

  print(gx('context').decode())
  qx('trace-file flush')
  qx('trace-file off')
  qx('trace-event guest_mem_before_exec off')
  qx('trace-event guest_user_syscall off')
  qx('trace-event guest_user_syscall_ret off')
  qx('trace-event exec_tb off')
  qx('trace-event exec_tb_nocache off')
  qx('trace-event memory_region_ram_device_read off')
  qx('trace-event memory_region_ram_device_write off')

  gx('del 1')
  gx('del 2')
  gx.run('c')
  sx.wait()
  qx('stop')
  gx.wait()
  print('all done')
  #sx.wait()
  proc_trace_file(ctx)
  #print(sx.wait())


def proc_trace_file(ctx):
  temp_file = '/tmp/abc'
  Z.sp.check_output(
      f'{g_qemu_path}/scripts/simpletrace.py {g_qemu_path}/trace-events-all  {ctx.trace_file} > {temp_file}',
      shell=1
  )
  out_db = f'/tmp/test_{flags.runid}.db'
  to_tracegraph(cmisc.Attr(infile=temp_file, outfile=out_db))


class Converter:

  def __init__(self, outfile):
    self.conn = sqlite3.connect(outfile)
    self.outfile = outfile

    init_cmd = '''
CREATE TABLE IF NOT EXISTS info (key TEXT PRIMARY KEY, value TEXT);
CREATE TABLE IF NOT EXISTS lib (name TEXT, base TEXT, end TEXT);
CREATE TABLE IF NOT EXISTS bbl (addr TEXT, addr_end TEXT, size INTEGER, thread_id INTEGER);
CREATE TABLE IF NOT EXISTS ins (rowid int PRIMARY KEY, bbl_id INTEGER, ip TEXT, dis TEXT, op TEXT not null default '') WITHOUT ROWID;
CREATE TABLE IF NOT EXISTS mem (ins_id INTEGER, ip TEXT, type TEXT, addr TEXT, addr_end TEXT, size INTEGER, data TEXT not null default '', value TEXT not null default '');
CREATE TABLE IF NOT EXISTS thread (thread_id INTEGER, start_bbl_id INTEGER, exit_bbl_id INTEGER)
'''
    self.conn.executescript(init_cmd)
    self.conn.commit()
    self.exec_id = -1
    self.pc = None
    self.ins_data = []
    self.mem_data = []

  def add_exec(self, d):
    self.exec_id += 1
    self.pc = d.pc
    self.ins_data.append((self.exec_id, self.pc))

  def add_mem(self, d):
    is_w = int(d.info[2:], 16) & 1
    vaddr = int(d['__cpu'], 16)
    vaddr_end = int(d.vaddr, 16)
    sz = vaddr_end - vaddr
    assert sz > 0 and sz < 30000
    sz = 10
    self.mem_data.append((self.exec_id, self.pc, hex(vaddr), hex(vaddr_end), 'RW' [is_w], sz))

  def finish(self):
    self.cur = self.conn.cursor()
    self.cur.executemany('insert into ins(rowid, ip) values (?,?)', self.ins_data)
    self.cur.executemany(
        'insert into mem(ins_id, ip,type,addr,addr_end,size) values (?,?,?,?,?,?)', self.mem_data
    )
    self.cur.close()
    self.conn.commit()
    self.conn.close()
    cmd = f'/home/benoit/packet/Tracer/TraceGraph/tracegraph {self.outfile}'
    print('Display it with ')
    print(cmd)


def to_tracegraph(ctx):

  cmisc.failsafe(lambda: Z.os.remove(ctx.outfile))
  c = Converter(ctx.outfile)
  for line in open(ctx.infile, 'r').readlines():
    line = line.strip()
    if not line: continue
    d = line.split(' ')
    typ = d[0]
    data = dict([x.split('=') for x in d[2:]])
    data = cmisc.Attr(data)

    if typ.startswith('exec_tb'):
      c.add_exec(data)
    elif typ.startswith('guest_mem_before'):
      c.add_mem(data)

  c.finish()


def make_sbin(ctx):
  blank = 0xe2000000 - 0xe1550000
  Z.sp.check_output(f'cat /dev/null | head -c {blank} > null_{blank}.bin', shell=1)
  Z.sp.check_output(
      f'cat ./securemem-e030-e1550000.bin ./null_{blank}.bin ./securemem-e2-e3.bin > ./securemem.bin',
      shell=1
  )


def modify_sec_app(ctx):
  if ctx.qemu_pts:
    qx = get_qemu(ctx.qemu_pts)
    qx.p.trash()
    qx('cont')

  a = open('./tz.app', 'rb').read()
  b = open('./resources/decrypted_file', 'rb').read()
  offset = list(Z.swig.opa_algo_swig.kmp_matches(b, a))[0]
  res = bytearray(b)

  res[offset] = 0xcc

  outfile = './resources/decrypted_file.bad'
  outfile_dest = bad_file_path
  open(outfile, 'wb').write(res)
  Z.sp.check_output(f'sshpass -p sstic scp -P 5555 {outfile} root@0.0.0.0:{outfile_dest} ', shell=1)
  Z.sp.check_output(
      f'sshpass -p sstic ssh -p 5555 root@0.0.0.0  "chmod +x {outfile_dest}"', shell=1
  )


import queue
from concurrent.futures import Future


class EventLoop:

  def __init__(self):
    self.q = queue.Queue()
    self.res = {}
    self.id = 0

  def get_id(self):
    with Z.threading.Lock() as lock:
      r = self.id
      self.id += 1
    return r

  def create_action(self, func):
    fx = Future()
    x = cmisc.Attr(func=func, future=fx, id=self.get_id())
    self.res[x.id] = x
    self.q.put(x.id)
    return x

  def finish(self):
    print('KKK')
    self.q.put(None)

  def do_sync(self, func):
    x = self.create_action(func)
    return x.future.result()

  def do_async(self, func):
    x = self.create_action(func)
    return x.future

  def run(self):
    while True:
      e = self.q.get()
      if e is None: break
      x = self.res[e]
      r = self.execute_action(x)
      x.future.set_result(r)

  def execute_action(self, x):
    try:
      return x.func()
    except Exception as e:
      glog.error(f'Failed executing {e}')
      Z.tb.print_exc()
      raise


class SyncWrapper:

  def __init__(self, obj, el):
    self.obj = obj
    self.el = el

  def __getattr__(self, name):

    def f(*args, **kwargs):
      f = getattr(self.obj, name)
      func = lambda: f(*args, **kwargs)
      x = self.el.create_action(func)
      return x.future.result()

    return f


class SyncGetterWrapper:

  def __init__(self, obj, el):
    self.obj = obj
    self.el = el

  def __getattr__(self, name):

    def f():
      return getattr(self.obj, name)

    x = self.el.create_action(f)
    return x.future.result()


class ASyncWrapper:

  def __init__(self, obj, el):
    self.obj = obj
    self.el = el

  def __getattr__(self, name):

    def f(*args, **kwargs):
      f = getattr(self.obj, name)
      func = lambda: f(*args, **kwargs)
      x = self.el.create_action(func)
      return x.future

    return f


def get_query_end_action(x0):
  if x0 & 0xffff == 1:
    return cmisc.Attr(done=1, failure=0, res=x0 >> 16)

  if x0 & 0xffff == 0xffff:
    return cmisc.Attr(done=1, failure=1, res=0)
  return cmisc.Attr(done=0)


class RunnerCtx:

  def __init__(self, ctx, el, gdb):
    self.el = el
    self.gdb = gdb
    self.ctx = ctx

  def entry(self):
    try:
      self.run()
    except:
      Z.tb.print_exc()
    finally:
      self.el.finish()

  def run(self):
    gx = SyncWrapper(self.gdb, self.el)
    ggx = SyncGetterWrapper(self.gdb, self.el)
    agx = ASyncWrapper(self.gdb, self.el)
    if self.ctx.only_gdb:
      qx = None
      sx = None
    else:
      if self.ctx.from_shell:
        qx, sx = get_qemu_and_ssh(self.ctx)
      else:
        qx = get_qemu(self.ctx.qemu_pts)
        sx = get_ssh()

    Z.time.sleep(0.2)
    if qx:
      qx('stop')
      qx('trace-file off')

      qx('gdbserver')

    gx.do_execute('target remote :1234')
    print('Target connected')

    if 0:
      gx.run_to(init_start_km)
      print('goog ', self.ctx.trace_file)
      qx(f'trace-file set {self.ctx.trace_file}')
      #qx('trace-event guest_mem_before_exec on')
      #qx('trace-event guest_user_syscall on')
      #qx('trace-event guest_user_syscall_ret on')
      qx('trace-event exec_tb on')
      qx('trace-event exec_tb_nocache on')

      print(gx.do_execute('context'))
      qx('trace-file on')
      gx.run_to(query_done_km)

      print(gx.do_execute('context'))
      qx('trace-file flush')
      qx('trace-file off')
      qx('trace-event guest_mem_before_exec off')
      qx('trace-event guest_user_syscall off')
      qx('trace-event guest_user_syscall_ret off')
      qx('trace-event exec_tb off')
      qx('trace-event exec_tb_nocache off')
      qx('trace-event memory_region_ram_device_read off')
      qx('trace-event memory_region_ram_device_write off')
      return

    if 0:
      while True:
        print(gx.get_ins_str())
        gx.resume()
        time.sleep(0.1)

    if 0:
      sx.run(self.ctx.prog_cmd)
      gx.run_to(init_done_km)
      print(gx.do_execute('gef config context.enable False'))
      smc_addr = 0xffff000010093958

      gx.set_bpt(bl2_entrypoint_ret)
      gx.set_bpt(bl2_entrypoint)

      eret_pt = 0xe2022cc
      gx.set_bpt(eret_pt)
      gx.set_bpt(bl2_entrypoint_ret)
      gx.set_bpt(0xe037434)
      gx.set_bpt(query_done_km)

      max_iter_query = 3

      def do_snapshot():
        print()
        print()
        snapshot = gx.get_snapshot(nstack=0)
        print(Z.Display.regs_summary(snapshot.regs, gx.get_regs()))
        print(Z.Display.disp_list(snapshot.mem))

      while True:
        do_snapshot()
        gx.resume()
        do_snapshot()

        if gx.get_reg('pc') == query_done_km:
          ax = get_query_end_action(gx.get_reg('x0'))
          print(ax)
          if ax.done:
            break

          max_iter_query -= 1
          if max_iter_query == 0:
            print('MAX iter done')
            break

        gx.step_into()

      return

    def read_pairs(fname):
      for i, line in enumerate(open(fname, 'r').readlines()):
        a, b = line.strip().split(':')
        a = int(a, 16)
        yield a, b

    aes_to_enc = []
    aes_to_dec = []
    for (addr_read,
         reg_read), (addr_write, reg_write
                    ) in zip(read_pairs('./aese_list.txt'), read_pairs('./aese_list2.txt')):
      aes_to_dec.append(
          cmisc.Attr(
              access_reg=reg_read,
              addr=addr_write + 0x4,
              name=f'aes_to_dec_{addr_read:x}',
              regs=[cmisc.Attr(name='readaddr(%s)' % reg_read, reg=reg_read)],
              mem=[cmisc.Attr(name='readval(%s)' % reg_write, reg=reg_write, size=4, offset=5)]
          )
      )

    for (addr_read, reg_read), (addr_write, reg_write) in zip(
        read_pairs('./aesd_read_dec.txt'), read_pairs('./aesd_write_enc.txt')
    ):
      aes_to_enc.append(
          cmisc.Attr(
              access_reg=reg_write,
              addr=addr_read,
              name=f'aes_to_enc_{addr_read:x}',
              regs=[cmisc.Attr(name='writeaddr(%s)' % reg_write, reg=reg_write)],
              mem=[cmisc.Attr(name='writeval(%s)' % reg_read, reg=reg_read, size=4, offset=5)]
          )
      )
    aes_to_dec_by_addr = {x.addr: x for x in aes_to_dec}
    aes_to_enc_by_addr = {x.addr: x for x in aes_to_enc}

    ctx = self.ctx
    self.done_event = cmisc.Attr(addr=proc_done_elf, name='result_is_out', finished=1)
    self.ctx.aes_to_dec = aes_to_dec
    self.ctx.aes_to_enc = aes_to_enc

    oem_funcs = list(load_function_list('./trace/oem_functions_list.txt'))
    self.ctx.br_funcs_list = list(
        Z.itertools.chain(oem_funcs, load_function_list('./trace/functions_br_counts'))
    )
    for func in self.ctx.br_funcs_list:
      func.regs = []
      for r in ['x19', 'x22', 'x0', 'x21']:
        func.regs.append(cmisc.Attr(reg=r, name=r))

    self.ctx.br_funcs_list.append(cmisc.Attr(addr=dispatch_func, name='dispatcher', regs=['x0']))

    self.ctx.br_funcs_list.append(
        cmisc.Attr(
            addr=0xE200624,
            name='str1',
            regs=[cmisc.Attr(reg='x1', name='val'),
                  cmisc.Attr(reg='x0', name='dest')]
        )
    )
    self.ctx.br_funcs_list.append(
        cmisc.Attr(
            addr=0xE200704,
            name='str2',
            regs=[cmisc.Attr(reg='x0', name='val'),
                  cmisc.Attr(reg='x4', name='dest')]
        )
    )
    self.ctx.br_funcs_list.append(
        cmisc.Attr(
            addr=0xE200d0c,
            name='str3',
            regs=[cmisc.Attr(reg='x1', name='val'),
                  cmisc.Attr(reg='x0', name='dest')]
        )
    )
    self.ctx.br_funcs_list.append(
        cmisc.Attr(addr=0xE200B98, name='ldr1_end', regs=[cmisc.Attr(reg='x0', name='res')])
    )
    self.ctx.br_funcs_list.append(
        cmisc.Attr(addr=0xE200B94, name='ldr1_begin', regs=[cmisc.Attr(reg='x0', name='addr')])
    )
    self.ctx.br_funcs_list.append(
        cmisc.Attr(addr=0xE200c80, name='ldr2_end', regs=[cmisc.Attr(reg='x0', name='res')])
    )
    self.ctx.br_funcs_list.append(
        cmisc.Attr(addr=0xE200c7c, name='ldr2_begin', regs=[cmisc.Attr(reg='x0', name='addr')])
    )
    self.ctx.br_funcs_list.append(
        cmisc.Attr(addr=0xE200C30, name='do_stuff1', regs=[cmisc.Attr(reg='x0', name='action')])
    )

    self.ctx.br_funcs_list.append(
        cmisc.Attr(
            addr=0x0E200878,
            name='res_check2',
            regs=[cmisc.Attr(reg='w19', name='v1'),
                  cmisc.Attr(reg='w4', name='v2')]
        )
    )
    self.ctx.br_funcs_list.append(
        cmisc.Attr(addr=0xE2009F4, name='final_check', regs=[cmisc.Attr(reg='x4', name='v1')])
    )

    self.ctx.br_funcs_list.append(
        cmisc.Attr(
            addr=0x0E200AF0,
            name='func9',
            regs=[cmisc.Attr(reg='x19', name='v1'),
                  cmisc.Attr(reg='x20', name='v2')]
        )
    )
    self.ctx.br_funcs_list.append(
        cmisc.Attr(
            addr=0xe0315e4,
            name='funcd_vals',
            regs=[cmisc.Attr(reg='x0', name='v1'),
                  cmisc.Attr(reg='x23', name='v2')]
        )
    )

    def do_ret(x, gx, data):
      print('GOOOT ', hex(gx.get_reg('lr')))
      gx.run_to(gx.get_reg('lr'))


#    RESTORING HERE 1 418c1c
#    RESTORING HERE 3 ffff00001009395c
#    Exception return from AArch64 EL3 to AArch64 EL1 NEW=e035a1c, PC 0xe200094 ++++ e200094
#    RESTORING HERE 3 e2022e0
#    Exception return from AArch64 EL3 to AArch64 EL1 NEW=e035a1c, PC 0xe2022e0 ++++ e2022e0
#    RESTORING HERE 3 e2008a0
#    generating eret e035a24
#    Exception return from AArch64 EL3 to AArch64 EL1 NEW=e035a20, PC 0xe2008a0 ++++ e2008a0
#    RESTORING HERE 3 e2001e8
#    generating eret e035a24
#    Exception return from AArch64 EL3 to AArch64 EL1 NEW=e035a20, PC 0xffff00001009395c ++++ ffff00001009395c
#
#
#    RESTORING HERE 1 418c1c
#    RESTORING HERE 3 ffff00001009395c
#    Exception return from AArch64 EL3 to AArch64 EL1 NEW=e035a1c, PC 0xe200094 ++++ e200094
#    RESTORING HERE 3 e2022e0
#    Exception return from AArch64 EL3 to AArch64 EL1 NEW=e035a1c, PC 0xe2022e0 ++++ e2022e0
#    RESTORING HERE 3 e2008a0
#    generating eret e035a24
#    Exception return from AArch64 EL3 to AArch64 EL1 NEW=e035a20, PC 0xe2008a0 ++++ e2008a0
#    RESTORING HERE 3 e2001e8
#    generating eret e035a24
#    Exception return from AArch64 EL3 to AArch64 EL1 NEW=e035a20, PC 0xffff00001009395c ++++ ffff00001009395c
#    RESTORING HERE 1 ffff000010093980
#    RESTORING HERE 1 ffff000010081a08
#    generating eret ffff000010083460
#    Exception return from AArch64 EL1 to AArch64 EL1 NEW=ffff000010083418, PC 0xffff000010081a08 ++++ ffff000010081a08
#    RESTORING HERE 1 ffff00001057d86c
#    Exception return from AArch64 EL1 to AArch64 EL1 NEW=ffff000010083418, PC 0xffff00001057d86c ++++ ffff00001057d86c
#    RESTORING HERE 1 ffff00001057d86c
#    Exception return from AArch64 EL1 to AArch64 EL1 NEW=ffff000010083418, PC 0xffff00001057d86c ++++ ffff00001057d86c
#    RESTORING HERE 1 ffff00001057d86c
#    Exception return from AArch64 EL1 to AArch64 EL1 NEW=ffff000010083418, PC 0xffff00001057d86c ++++ ffff00001057d86c
#    Exception return from AArch64 EL1 to AArch64 EL1 NEW=ffff000010083418, PC 0xffff000010093980 ++++ ffff000010093980

    self.ctx.kern_funcs = [
        cmisc.Attr(addr=qq_done_km, name='QQ_DONE'),
        cmisc.Attr(addr=kern_svc_ret, name='kern svc ret'),
        cmisc.Attr(addr=0xffff000010093960, name='kern svc ret2'),
        cmisc.Attr(addr=0xffff000010093964, name='kern svc ret3'),
        cmisc.Attr(addr=0xffff000010093968, name='kern svc ret4'),
        cmisc.Attr(addr=0xffff00001009396c, name='kern svc ret5'),
        cmisc.Attr(addr=0xffff000010093980, name='kern svc ret6'),
        cmisc.Attr(addr=query_done_km, name='QUERY DONE'),
        cmisc.Attr(addr=0xffff000008590418, name='QUERY DONE2'),
        cmisc.Attr(addr=0xffff00000859041c, name='QUERY DONE2'),
        cmisc.Attr(addr=0xffff000008590420, name='QUERY DONE2'),
        cmisc.Attr(addr=0xffff000008590424, name='QUERY DONE2'),
        cmisc.Attr(addr=0xffff000008590414, name='QUERY BEGIN'),
    ]

    self.ctx.funcs = []
    funcs = self.ctx.funcs
    self.ctx.funcs.append(self.done_event)
    self.ctx.funcs.append(ev_loop192)
    self.ctx.funcs.extend(aes_to_dec)
    self.ctx.funcs.extend(aes_to_enc)
    self.ctx.funcs.extend(self.ctx.kern_funcs)

    self.ctx.memset = cmisc.Attr(name='memset', addr=0xe0360c4, regs=['x0', 'x1', 'x2'], bypass=1)
    self.ctx.memcpy = cmisc.Attr(name='memcpy', addr=0xe036070, regs=['x0', 'x1', 'x2'], bypass=1)
    self.ctx.cache_invalidate = cmisc.Attr(name='cache_invalidate', addr=0x00E035B08, bypass=1)

    self.ctx.end_ops = [cmisc.Attr(addr=0xe0310dc, name='ret-1', finished=1)]
    self.ctx.funcs.extend(self.ctx.end_ops)

    bypass_funcs = []
    if not ctx.disable_bypass:
      memcpy2 = cmisc.Attr(name='memcpy2', addr=0x0E202928, regs=['x0', 'x1', 'x2'], bypass=1)

      cache_invalidate2 = cmisc.Attr(
          name='cache_invalidate2', addr=0x0E2023D4, regs=['x0', 'x1', 'x2'], bypass=1
      )
    bypass_funcs = [
        self.ctx.memcpy, self.ctx.memset, self.ctx.cache_invalidate, memcpy2, cache_invalidate2
    ]
    self.ctx.op_probes = list(
        Z.itertools.chain(bypass_funcs, self.ctx.br_funcs_list, self.ctx.end_ops)
    )
    self.ctx.funcs.extend(self.ctx.op_probes)

    vmop_read_ev = cmisc.Attr(
        name='vmop_read',
        addr=0xE20108C,
        regs=[cmisc.Attr(reg='x24', name='dest'),
              cmisc.Attr(reg='x0', name='val')]
    )
    vmop_write_ev = cmisc.Attr(
        name='vmop_write',
        addr=0xE200FC8,
        regs=[cmisc.Attr(reg='x2', name='content')],
        mem=[
            cmisc.Attr(name='newval', reg='x20', size=8, offset=0, count=2),
        ]
    )

    vmop_ev = cmisc.Attr(
        name='vmop',
        addr=vmop_begin,
        regs=[cmisc.Attr(reg='x0', name='dest'),
              cmisc.Attr(reg='x1', name='idx')],
        mem=[
            cmisc.Attr(name='replace', reg='x0', size=4, offset=8, count=1),
            cmisc.Attr(name='is_write', reg='x0', size=8, offset=0x10, count=1)
        ]
    )

    #vmop_probes = [vmop_begin_ev, vmop_end_ev, vmop_sm4e_1, vmop_sm4e_2, vmop_sm4e_3, vmop_sm4e_4]
    vmop_probes = [vmop_ev, vmop_write_ev, vmop_read_ev]
    #vmop_probes += bypass_funcs
    self.ctx.funcs.extend(vmop_probes)
    self.ctx.bypass_funcs = bypass_funcs

    for func in self.ctx.op_probes:
      func.get_or_insert('mem', []).extend([cmisc.Attr(reg='sp', size=8, offset=0x40, count=3)])

    setup_end_event = cmisc.Attr(name='setup_end', addr=setup_end)
    funcs.append(setup_end_event)
    self.br_points = [
        cmisc.Attr(name='oem_br1', regs=['x0'], addr=0xE0311BC),
        cmisc.Attr(name='chk_1337', regs=['x1'], addr=0x00E203644),
        cmisc.Attr(name='check_d', regs=['x2'], addr=0xE200774),
        cmisc.Attr(name='check_x', regs=['x2'], addr=0xe203604),
        cmisc.Attr(name='check_y', regs=['x30'], addr=0x000E036C10),
        cmisc.Attr(name='check_z', regs=['x8'], addr=0xe202234),
        cmisc.Attr(name='store_x', regs=['x8'], addr=0xe035590),
        cmisc.Attr(name='eret1', regs=['x8'], addr=0xe202608),
        cmisc.Attr(name='eret2', regs=['x8'], addr=0xe035a20),
    ]

    print(list(aes_to_enc_by_addr.keys()))

    def update_access_tb_pos(x, gx, data):
      data['access'] = gx.get_reg(x.access_reg) - 0xe04a5d8 >> 4

    funca = aes_to_dec_by_addr[0xe031210]
    funca.name = 'funca_read_mem'
    funcb = aes_to_enc_by_addr[0xe03128c]
    funcb.name = 'funca_write_mem'
    funcb.cb = update_access_tb_pos
    funca.cb = update_access_tb_pos

    funcc = cmisc.Attr(
        name='funcc_op',
        addr=0xe031400,
        regs=[
            cmisc.Attr(reg='x0', name='v2'),
            cmisc.Attr(reg='x20', name='v1'),
            cmisc.Attr(reg='x19', name='res')
        ],
    )
    funcd = cmisc.Attr(
        name='funcd_op',
        addr=0xe0315ec,
        regs=[
            cmisc.Attr(reg='x23', name='v1'),
            cmisc.Attr(reg='x0', name='v_x22'),
            cmisc.Attr(reg='x19', name='res')
        ],
    )
    funce = cmisc.Attr(
        name='funce_op',
        addr=0xe0316f8,
        regs=[cmisc.Attr(reg='x19', name='res')],
        mem=[
            cmisc.Attr(name='v_x19', reg='x23', size=4, offset=0, count=1),
            cmisc.Attr(name='v_x22', reg='x0', size=4, offset=0, count=1)
        ]
    )

    funcf = cmisc.Attr(
        name='funcf_op',
        addr=0xe03185c,
        regs=[
            cmisc.Attr(reg='x19', name='res'),
        ],
        mem=[
            cmisc.Attr(name='v_x19', reg='x22', size=4, offset=0, count=1),
        ]
    )

    funcg = cmisc.Attr(
        name='funcg_op',
        addr=0xe031bc8,
        regs=[
            cmisc.Attr(reg='x19', name='res'),
            cmisc.Attr(reg='x22', name='x22'),
            cmisc.Attr(reg='x0', name='v_x19'),
        ],
    )

    #funch=  cmisc.Attr(name='funch_op', addr=0xe03185c , regs=[cmisc.Attr(reg='x19', name='res')],
    #                         mem=[ cmisc.Attr(name='v_x19', reg='x22', size=4, offset=0, count=1),
    #                              ] )
    funci = cmisc.Attr(
        name='funci_op',
        addr=0xe031e78,
        regs=[cmisc.Attr(reg='x19', name='res'),
              cmisc.Attr(reg='x22', name='v2')],
        mem=[
            cmisc.Attr(name='v2', reg='x23', size=4, offset=0, count=1),
            cmisc.Attr(name='v1', reg='x0', size=4, offset=0, count=1),
        ]
    )

    ctx.func_analysis = [
        funca,
        funcb,
        funcc,
        funcd,
        funce,
        funcf,
        funcg,
        funci,
    ]
    ctx.funcs.extend(ctx.func_analysis)
    ctx.funcs.extend(self.br_points)
    dispatcher_evs = [
        cmisc.Attr(name='el2_br', regs=[cmisc.Attr(reg='x0', name='br'),], addr=0xE0311BC),
        cmisc.Attr(name='el3_br1', regs=[cmisc.Attr(reg='x0', name='br'),], addr=0x0E20095C),
        cmisc.Attr(name='el3_br2', regs=[cmisc.Attr(reg='x0', name='br'),], addr=0xE2007E8),
    ]

    ctx.funcs.extend(dispatcher_evs)

    cur_events = []
    cur_events.append(self.done_event)
    cur_events.append(setup_end_event)
    if ctx.solve_ev:
      cur_events.extend(ctx.func_analysis)
      cur_events.append(get_func_by_name(funcs, 'ldr1_end'))
      cur_events.append(get_func_by_name(funcs, 'ldr1_begin'))
      cur_events.append(get_func_by_name(funcs, 'str1'))
      cur_events.append(get_func_by_name(funcs, 'str2'))
      cur_events.append(get_func_by_name(funcs, 'str3'))
      cur_events.append(get_func_by_name(funcs, 'res_check2'))
      cur_events.extend(oem_funcs)


    if ctx.dispatcher_ev:
      cur_events.extend(dispatcher_evs)

    if ctx.vmop_probes_ev:
      cur_events.extend(vmop_probes)
    if ctx.func_analysis_ev:
      cur_events.extend(ctx.func_analysis)

    if ctx.enable_aes_to_dec:
      cur_events.extend(ctx.aes_to_dec)
    if ctx.enable_aes_to_enc:
      cur_events.extend(ctx.aes_to_enc)
    if ctx.kern_ev:
      cur_events.extend(ctx.kern_funcs)
    if ctx.br_probes_ev:
      cur_events.extend(ctx.br_funcs_list)
      cur_events.extend(self.br_points)

    if ctx.op_probes_ev:
      cur_events.extend(ctx.op_probes)

    if ctx.cheat_mode:
      fd = get_func_by_name(ctx.funcs, 'funcd_vals')

      def cheat_cb(x, gx, data):
        gx.set_reg('x0', gx.get_reg('x23'))

      fd.cb = cheat_cb
      cur_events.append(fd)

    #bypass_intr_check = cmisc.Attr(name='bypass_intr_check', addr=0x0E203640, cb=bypassit, regs=['x1'])
    #ctx.funcs.append(bypass_intr_check)
    #cur_events.append(bypass_intr_check)

    self.ctx.funcs_map = {a.addr: a for a in self.ctx.funcs}
    if ctx.trace_from_str:
      ev = get_func_by_name(ctx.funcs, ctx.trace_from_str)
      cur_events.append(ev)
      ctx.trace_from = ev.addr
    if ctx.trace_to_str:
      ev = get_func_by_name(ctx.funcs, ctx.trace_to_str)
      cur_events.append(ev)
      ctx.trace_to = ev.addr

    ctx.cur_events = {a.addr: a for a in cur_events}
    ctx.default_regs = []
    if ctx.debug_regs:
      ctx.default_regs.extend(cmisc.to_list('ESR_EL1 x0 x1 x2 x3 ELR_EL1 ELR_EL3'))
      for func in funcs:
        func.get_or_insert('regs', []).extend(ctx.default_regs)
    globals()[self.ctx.action2](gx, sx, qx, self.ctx)

    if ctx.recover_output:
      print('done la')
      qx.run('cont')
      print('got command output >>>  ', sx.wait())


def do_tracing(gx, sx, qx, ctx):
  qx('cont')
  print(sx.run('ls'))
  sx.run(ctx.prog_cmd)
  gx.run_to(init_done_km_after_free)
  #gx.run_to(kern_vec_smc)
  gx.run_to(kern_smc_addr)
  #gx.set_bpt(tsp_handler)
  inslist = []
  count_query = 0

  print(gx.do_execute('gef config context.enable False'))

  trace_to = feed_done_km
  trace_to = qq_done_km
  trace_to = query_done_km
  print('hheere start trace')
  if 1:
    inslist.extend(gx.trace_to(trace_to, disp_ins=1, max_ins=10))
    print('RESULT >> ', len(inslist))
    for x in inslist:
      print(x)

    Z.pickle.dump(inslist, open(f'/tmp/inslist_{ctx.runid}.pickle', 'wb'))

    return

  while True:
    #print(gx.do_execute(f'trace-run {query_done_km}'))
    count_query += 1
    inslist.extend(gx.trace_to(trace_to, disp_ins=1))
    #gx.run_to(query_done_km)
    x0 = gx.get_reg('x0')
    print('Got return at ', hex(x0))
    ax = get_query_end_action(gx.get_reg('x0'))
    print(ax)
    if ax.done:
      break
    if count_query == 3:
      print('stopping here')
      break
    gx.step_into()
    #if x0 == 0xf2000006:
    #  return
    #gx.resume()
  Z.pickle.dump(inslist, open(f'/tmp/inslist_{ctx.runid}.pickle', 'wb'))
  print('DONE WITH ', len(inslist), count_query)
  return


def do_tracing_op(gx, sx, qx, ctx):
  qx('cont')
  print(sx.run('ls'))
  print('laaa', ctx.prog_cmd)

  count_query = 0

  sx.run(ctx.prog_cmd)
  gx.run_to(setup_begin)
  #gx.run_to(work_begin)

  trace_from = ctx.trace_from
  trace_to = ctx.trace_to

  print(gx.do_execute('gef config context.enable False'))
  printfile = Z.os.path.join(
      ctx.output_dir, f'printfile_{ctx.runid}_{trace_from:x}_{trace_to:x}.log'
  )

  if trace_from:
    gx.run_to(trace_from)
    gx.set_bpt(trace_from)
    for i in range(ctx.nskip_from):
      gx.resume()

  for x in g_ctx.bypass_funcs:
    g_ctx.cur_events[x.addr] = x
  for x in g_ctx.cur_events.keys():
    gx.set_bpt(x)
  if not trace_from:
    gx.resume()
  print('Now go')

  with open(printfile, 'w') as f:
    g_ctx.printfile = f
    want_regs = g_ctx.default_regs
    for i in range(g_ctx.count):
      inscount = ctx.inscount
      print(f'Processing on {trace_from:x} xx {gx.get_pc():x}')
      assert not trace_from or gx.get_pc() == trace_from
      out('\n\n\n')
      do_inslist_print([gx.get_ins_info(gx.get_pc(), funcs=ctx.funcs_map).res])

      stop_pc = list([trace_to] + list(ctx.cur_events.keys()))
      while inscount > 0:

        inslist = gx.trace_to(
            stop_pc,
            disp_ins=1,
            max_ins=min(1000, inscount + 10),
            funcs=ctx.funcs_map,
            regs=want_regs,
            want_prev_regs=0,
        )
        inscount -= len(inslist)
        pc = gx.get_pc()

        do_inslist_print(inslist[:-1])

        if pc in ctx.cur_events:
          ev = ctx.cur_events[pc]
          if 'cb' in ev:
            ev['cb'](ev, gx, inslist[-1].data)
          if not ev.get('bypass', 0):
            out(f'ON EVENT >> {ev.addr:x} {ev.name} >> {gx.get_ins_str_gdb()}')
            do_inslist_print([inslist[-1]])
            out()

          if ev.get('finished', 0):
            print('finished')
            return
          if ev.get('bypass', 0):
            print('RUUUNE TO ', gx.get_reg('lr'))
            gx.run_to(gx.get_reg('lr'))
            print('END UP ON ', gx.get_pc())
            do_inslist_print([gx.get_ins_info(gx.get_pc(), funcs=ctx.funcs_map).res])
        if gx.get_pc() == trace_to: break

      if trace_to and trace_to != trace_from:
        while gx.get_pc() != trace_from:
          print('\n\n\n==========================================')
          gx.resume()
          do_inslist_print([gx.get_ins_info(gx.get_pc(), funcs=ctx.funcs_map).res])
  print('DONE LA')

  #Z.pickle.dump(inslist, open(f'/tmp/inslist_{ctx.runid}.pickle', 'wb'))
  return


def normalize_regs(reglist):
  nregs = []
  for reg in reglist:
    if reg[0] == 'v':
      nregs.append(reg + '.q.s[0]')
      nregs.append(reg + '.q.u[0]')
    else:
      nregs.append(reg)
  return nregs


def get_putchar(gx, sx, qx, ctx):
  print(sx.run('ls'))
  sx.run(ctx.prog_cmd)
  print('starting la')
  gx.run_to(init_done_km_after_free)
  gx.run_to(kern_vec_smc)
  memcpy_addr = 0xffff0000105612c0
  gx.set_bpt(memcpy_addr)
  print('heere')
  for i in range(100):
    gx.resume()
    x0 = gx.get_reg('x0')
    x1 = gx.get_reg('x1')
    x2 = gx.get_reg('x2')
    print(hex(x1), hex(x1), x2)
    print(gx.get_memory(x1, 10))
    print()


def testit(ctx_filename):
  ctx = Z.pickle.load(open(ctx_filename, 'rb'))
  global g_ctx
  g_ctx = ctx
  el = EventLoop()
  x = Z.GdbDebugger()
  x.do_execute('gef config gef.disable_color = True')

  rctx = RunnerCtx(ctx, el, x)
  th = Z.threading.Thread(target=rctx.entry)
  th.start()
  el.run()


def get_qemu_and_ssh(ctx):
  qx = get_qemu(ctx.qemu_pts)
  qx.p.trash()
  qx('cont')
  sx = get_ssh()
  sx('echo 0 > /proc/sys/kernel/randomize_va_space')
  return qx, sx


def test_bpt(ctx):
  qx = get_qemu(ctx.qemu_pts)
  gx = get_gdb()

  qx('gdbserver')
  gx('target remote :1234')
  #gx('b *0x00E030958')
  gx('b *0x10')
  gx('b *0xb0')
  gx('b *0xe00b000')
  gx('b *0xe003000')
  gx('continue')


def test1(ctx):
  ctx_filename = './ctx.pickle'
  ctx.runid = 'gdb_' + ctx.runid
  with open(ctx_filename, 'wb') as f:
    print(ctx)
    Z.pickle.dump(ctx, f)

  Z.launch_gdb(
      'solve',
      'testit',
      args=[ctx_filename],
      gdb_cmd=g_gdb_binary,
      gdb_args=['-q', './resources/decrypted_file']
  )


def do_tracing_op_full_trace(gx, sx, qx, ctx):
  qx('cont')
  print(sx.run('ls'))
  print('laaa', ctx.prog_cmd)
  sx.run(ctx.prog_cmd)
  printfile = Z.os.path.join(ctx.output_dir, f'fx_{ctx.runid}.log')

  count_query = 0

  run_addr = dispatch_loop192

  gx.run_to(run_addr)
  print('running trace')
  inslist = gx.trace_to(dispatch_func, disp_ins=1, max_ins=0x6000)
  with open(printfile, 'w') as f:
    g_ctx.printfile = f
    do_inslist_print(inslist)
  return


def get_func_by_name(funcs, name):
  for x in funcs:
    if x.name == name:
      return x


def do_tracing_op3(gx, sx, qx, ctx):
  qx('cont')
  printfile = Z.os.path.join(ctx.output_dir, f'fx_{ctx.runid}.log')

  count_query = 0

  events = ctx.cur_events

  if ctx.evtype == 'aes_to_dec':
    events.extend(ctx.br_funcs_list)
    events.extend(ctx.aes_to_dec)

  if ctx.evtype == 'loop192':
    events[ev_loop192.addr] = ev_loop192

  if 0:
    events.append(cmisc.Attr(addr=0xE200624, name='str1'))
    events.append(cmisc.Attr(addr=0xE200704, name='str2'))

  ev_map = {}

  reglist = cmisc.to_list('x0 x1 x2 x3 x4 x19')
  nregs = normalize_regs(reglist)
  reglist = []

  print(sx.run('ls'))
  print('laaa', ctx.prog_cmd)
  sx.run(ctx.prog_cmd)
  print(gx.do_execute('gef config context.enable False'))
  if ctx.setup_begin:
    gx.run_to(setup_begin)
  else:
    gx.run_to(setup_end)

  print('end setup')

  if ctx.trace_from:
    gx.run_to(ctx.trace_from)
    gx.set_bpt(ctx.trace_from)
    for i in range(ctx.nskip_from):
      gx.resume()

  for k in events.keys():
    gx.set_bpt(k)
    #ev.regs = normalize_regs(ev.get('regs', nregs))
  if not ctx.trace_from:
    gx.resume()

  print('NOW GO')
  import hashlib
  end = set([ctx.trace_to])

  lst = []
  with open(printfile, 'w') as f:
    g_ctx.printfile = f
    i = 0
    while True:
      addr = gx.get_pc()

      assert addr in events, hex(addr)
      ev = events[addr]
      if ev.get('skip', 0): continue
      #h=hashlib.md5(str(i).encode()).hexdigest()
      out(f'ON EVENT >> {ev.addr:x} {ev.name} >> {gx.get_ins_str_gdb()}')

      if not ctx.only_name:
        ins_res = gx.get_ins_info(gx.get_pc(), funcs=ctx.funcs_map, regs=g_ctx.default_regs).res
        if 'cb' in ev:
          ev['cb'](ev, gx, ins_res.data)
        do_inslist_print([ins_res])
        out('')

      if ev.get('finished', 0):
        print('DONE La')
        break

      if addr in end:
        i += 1
        if i >= ctx.count:
          break

      gx.resume()
      f.flush()

  #Z.pickle.dump(lst, open(ctx.outfile, 'wb'))
  return


def do_tracing_op_full_trace(gx, sx, qx, ctx):
  qx('cont')
  print(sx.run('ls'))
  print('laaa', ctx.prog_cmd)
  sx.run(ctx.prog_cmd)
  printfile = Z.os.path.join(ctx.output_dir, f'fx_{ctx.runid}.log')


def inslist_print(ctx):
  lst = Z.pickle.load(open(ctx.infile, 'rb'))
  do_inslist_print(lst)


def do_inslist_print(lst):
  for ins in lst:
    if not ins.failed:
      del ins['failed']
      del ins['ins_data']
    if ins.pc in g_ctx.funcs_map:
      ins.label = g_ctx.funcs_map[ins.pc].name
    desc = ''
    if 'label' in ins:
      desc += f'LABEL: {ins.label}'
    else:
      desc += f'       '

    out(f'{desc}>> {ins.ins_str2}', Z.Display.disp(ins.get("data", "")))
    if g_ctx.enable_full_print:
      if ins.regs: out(Z.Display.disp(ins.regs))
      if ins.mem: out(Z.Display.disp(ins.mem))


def do_diff(ctx):
  lsts = []
  for filename in ctx.infiles:
    lsts.append(iter(Z.pickle.load(open(filename, 'rb'))))

  for i in Z.itertools.count():
    a, b = [next(a) for a in lsts]
    if a.pc != b.pc:
      print('DIFF at ', i)
      break

    diff = Z.Display.diff_dicts(a, b)
    if diff:
      print(a.ins_str)
      print(diff)
      print()


def test_ins_ops(ctx):
  arch = K.guess_arch('aarch64')
  print(arch.typ)
  ins = arch.mc.get_one_ins(bytes.fromhex('b8616a80')[::-1])
  ins_str = arch.mc.ins_str(ins)
  print(ins_str)
  print(arch.mc.get_reg_ops(ins))
  arch.mc.print_insn(ins)


def qemu_cmd(ctx):
  qx = get_qemu(ctx.qemu_pts)
  qx(ctx.cmd)


def test_gdb(gx, sx, qx, ctx):
  print(gx.get_reg('ESR_EL1'))
  print(gx.get_register('ESR_EL1'))


def ops_to_graph(ctx):

  cmisc.failsafe(lambda: Z.os.remove(ctx.outfile))
  c = Converter(ctx.outfile)
  for i, line in enumerate(open(ctx.infile, 'r').readlines()[:-1]):
    line = line.strip()
    if not line: continue
    tb = dict([x.split(':') for x in line.split(' ')])
    x0 = int(tb['x0'], 16) + int(tb.get('offset', '0'), 16)
    print('adding ', x0)
    c.add_exec(cmisc.Attr(pc=i))
    c.add_mem(cmisc.Attr(info=hex(1), __cpu=hex(x0)[2:], vaddr=hex(x0 + 1)[2:], pc=i))

  c.finish()


def decode_ops(gx, sx, qx, ctx):
  qx('cont')
  printfile = Z.os.path.join(ctx.output_dir, f'fx_{ctx.runid}.log')

  count_query = 0

  events = ctx.cur_events

  if ctx.evtype == 'oem_loop192':
    events.append(ev_loop192)

  elif ctx.evtype == 'aes_to_dec':
    events.extend(ctx.br_funcs_list)
    events.extend(ctx.aes_to_dec)


def collect_stats(ctx):

  for i in range(-1, 64):
    keymod = ''
    if i != -1:
      iB = i // 8
      ib = 1 << (i & 7)
      keymod = f'key[{iB}]^={ib};'
    name = f'loop192_log-modbit_{i}'
    cmd = f'stdbuf -o 0 python solve.py --actions=test1 --qemu-pts=$CUR_PTS --verbosity=DEBUG   --from-shell  --output-dir=./trace/  --action2=do_tracing_op3 --runid={name} --modkey="{keymod}" --outfile=./trace/{name}.pickle --evtype=oem_loop192'
    ctx.cmd = 'cont'
    qemu_cmd(ctx)

    print()
    print('processing ', i, cmd)
    Z.sp.check_output(cmd, shell=1)


def diff_two(id, a, b):
  fields = ['mem_x0', 'mem_x23']
  intervals = Z.Intervals(is_int=1)
  for i, (u, v) in enumerate(zip(a, b)):
    diff = 0
    for f in fields:
      if u[f] != v[f]: diff = 1
    if diff: intervals.add(i, i + 1)
  print(id, intervals)


def diff_stats(ctx):
  pickles = {}
  for i in range(-1, 64):
    name = f'loop192_log-modbit_{i}'
    pickle_file = f'./trace/{name}.pickle'
    try:
      pickles[i] = Z.pickle.load(open(pickle_file, 'rb'))[:-1]
    except:
      pass

  main = pickles[-1]
  for i in range(64):
    if i in pickles:
      diff_two(i, main, pickles[i])


def load_function_list(fname, filter_small=1):
  for line in open(fname, 'r').readlines():
    line = line.strip()
    a, b, c = line.split()
    a = int(a)
    if filter_small and a > 2000: continue
    b = int(b[3:], 16)
    yield cmisc.Attr(name=c, count=a, addr=b)


def read_secure_mem(gx, sx, qx, ctx):
  if qx:
    qx('cont')
    print(sx.run('ls'))
    print('laaa', ctx.prog_cmd)
    sx.run(ctx.prog_cmd)

  op_begin = 0xE200E84
  op_end = 0xE2010A8

  gx.run_to(op_begin)

  x0 = gx.get_reg('x0')
  gx.set_bpt(op_end)

  def read1(addr):
    gx.set_memory(x0 + 0x10, Z.struct.pack('<Q', 0))
    gx.set_reg('pc', op_begin)
    gx.set_reg('x0', x0)
    gx.set_reg('x1', addr)

    if 1:
      gx.resume()
    else:
      do_inslist_print(gx.trace_to(op_end, disp_ins=1))

    got = gx.get_memory(x0, 8)
    res, = Z.struct.unpack('<Q', got)
    return res

  if 0:
    print(hex(read1(0x818)))
    print(hex(read1(0x81c)))
    print(hex(read1(0x820)))
    return

  #return
  data = []
  for i in range(0, 0x1000000, 4):
    print('processing ', hex(i))
    data.append(read1(i))
    print('GOOOT ', hex(data[-1]))
  Z.pickle.dump(data, open('./smem.decoded.pickle', 'wb'))


def dump_smem(ctx):
  x = Z.pickle.load(open('./smem.decoded.pickle', 'rb'))
  r = bytearray()
  for a in x:
    r += a
  open('./smem.raw.bin', 'wb').write(r)


class SMemAccessor:

  def __init__(self, raw_data=[], key=None):
    self.data = open('./smem.data', 'rb').read()
    self.data += b'\x00' * 0x40
    self.raw_data = raw_data
    if raw_data:
      self.raw_data.append(bytes([0] * 16))
      self.raw_data.append(bytes([0] * 16))

      if key is None:
        self.raw_data.append(bytes([0] * 16))
        self.raw_data.append(bytes([0] * 16))
      else:
        self.raw_data.append(key[:16])
        self.raw_data.append(key[16:])

      self.raw_data.append(bytes([0] * 16))
      self.bytes = bytearray(b''.join(self.raw_data))
    self.k = bytes.fromhex('545b6269383f464d1c232a3100070e15')[::-1]
    self.n = bytes.fromhex('0625f824d5dc439cb4c150382078cc93')[::-1]

  def get(self, q):
    kq = q & ~0xf
    if self.raw_data:
      return self.raw_data[kq // 16]

    tgt = self.data[kq:kq + 0x10]

    u = Z.swig_unsafe.hack_ctf_sstic_2019_swig

    k = Z.struct.unpack('<IIII', self.k)
    k = [x ^ kq for x in k]
    ks = Z.struct.pack('<IIII', *k)
    kk = u.opa_crypto_sm4ekey(self.n, ks)

    #rev32
    tgt = b''.join([tgt[i:i + 4][::-1] for i in range(0, 16, 4)])

    kk = Z.struct.unpack('<IIII', kk)
    kk = Z.struct.pack('<IIII', *kk[::-1])
    res = u.opa_crypto_sm4e(tgt, kk)
    return res[::-1]

  def access(self, q):
    if self.bytes:
      return Z.struct.unpack('<I', self.bytes[q:q + 4])[0]

    oq = q & 0xf
    assert q < len(self.data)
    u = self.get(q) + self.get(q + 16)
    return Z.struct.unpack('<I', u[oq:oq + 4])[0]

  def access_write(self, q, v):
    if self.bytes:
      self.bytes[q:q + 4] = Z.struct.pack(
          '<I',
          v,
      )
      return
    assert 0
    oq = q & 0xf
    assert q < len(self.data)
    u = self.get(q) + self.get(q + 16)
    return Z.struct.unpack('<I', u[oq:oq + 4])[0]


smem_dec_fname = './smem.decoded.pickle'


def smem_dec_all(ctx):
  u = SMemAccessor()
  data = []
  for i in range(0, len(u.data), 16):
    data.append(u.get(i))
  Z.pickle.dump(data, open(smem_dec_fname, 'wb'))


def test_smem(ctx):

  want = 0x0000000005f58629
  q = 0x0000000000077b34
  q = 0x67d8e
  #q =0x00000000000007baaa
  smem = SMemAccessor()
  print(hex(smem.access(q)))


def test_algo(ctx):
  smem = SMemAccessor(raw_data=Z.pickle.load(open(smem_dec_fname, 'rb')))

  key = ctx.keybin
  dx = get_data(ctx)
  key = bytearray(key)
  compute_one(smem, key)


def test_algo2(ctx):
  smem = SMemAccessor(raw_data=Z.pickle.load(open(smem_dec_fname, 'rb')))

  key = ctx.keybin
  dx = get_data(ctx)
  key = bytearray(key)

  if 1:
    print(len(dx))
    for i in range(4, 0x20, 4):
      key[i:i + 2] = dx[i // 4].to_bytes(4, 'little')
      print(key[i:i + 2])

  sx = set()
  for i, (a, b) in enumerate(Z.itertools.product(range(256), repeat=2)):
    key[2] = a
    key[3] = b

    have = compute_one(smem, key)
    sx.add(have)
    print(hex(have), hex(dx[0]), a, b, len(sx), i)
    if have == dx[0]:
      print('ON for ', key[2:4])
      assert 0


def compute_one(smem, key):
  i = 7
  cur = key[3]
  v = key[2]
  rnd = 0x20
  kp = 4
  for u in range(16):

    if u != 0 and u % 4 == 0:
      cur ^= rnd
      print('DOTI ', u, hex((cur & 0xff) << 8 | v & 0xff))
      cur ^= key[kp + 1]
      v ^= key[kp]
      kp += 2
      kp %= 8
      prev = (cur & 0xff) << 8 | v & 0xff
      rnd -= 1
      if rnd == 0x17: rnd = 0x20
    cur = i << 16 | (cur & 0xff) << 8 | (v & 0xff)
    cur += 0x1000
    print(hex(cur))
    v = smem.access(cur)
    i -= 1
    if i < 0: i = 9

  cur = prev
  nprev = 0
  for u in range(32):

    if u % 4 == 0:
      #cur ^= key[5]^rnd
      #v ^= key[4]
      nprev = (cur & 0xff) << 8 | v & 0xff
      cur = prev
      rnd -= 1
      if rnd == 0x17: rnd = 0x20
    else: cur = (cur & 0xff) << 8 | (v & 0xff)
    cur |= i << 16
    cur += 0x1000
    v = smem.access(cur)
    i -= 1
    if i < 0: i = 9

  rnd = 0x10
  for u in range(32):

    if u % 4 == 0:
      xprev = (cur & 0xff) << 8 | v & 0xff
      cur ^= key[5] ^ rnd
      v ^= key[4]
      prev = (cur & 0xff) << 8 | v & 0xff
      rnd -= 1
      if rnd == 0x17: rnd = 0x20

    cur = (cur & 0xff) << 8 | (v & 0xff)
    cur |= i << 16
    cur += 0x1000
    v = smem.access(cur)
    i -= 1
    if i < 0: i = 9

  cur = prev
  V1 = prev
  v2 = xprev
  nprev = 0
  for u in range(32):
    if u % 4 == 0:
      #cur ^= key[5]^rnd
      #v ^= key[4]
      nprev = (cur & 0xff) << 8 | v & 0xff
      cur = prev
      rnd -= 1
      if rnd == 0x17: rnd = 0x20
    else: cur = (cur & 0xff) << 8 | (v & 0xff)
    cur |= i << 16
    cur += 0x1000
    v = smem.access(cur)
    i -= 1
    if i < 0: i = 9
  cur = prev
  nprev = 0
  for u in range(32):

    if u % 4 == 0:
      #cur ^= key[5]^rnd
      #v ^= key[4]
      nprev = (cur & 0xff) << 8 | v & 0xff
      cur = prev
      rnd -= 1
      if rnd == 0x17: rnd = 0x20
    else: cur = (cur & 0xff) << 8 | (v & 0xff)
    cur |= i << 16
    cur += 0x1000
    v = smem.access(cur)
    i -= 1
    if i < 0: i = 9
  return prev << 16 | xprev


#LABEL: ldr1_begin>> => 0xe200b94:	ldr	w0, [x0] addr:0000000000100000  #invlid
#LABEL: ldr1_end>> => 0xe200b98:	mov	x2, x0 res:00000000612e7270
#LABEL: ldr1_begin>> => 0xe200b94:	ldr	w0, [x0] addr:0000000000100004
#LABEL: ldr1_end>> => 0xe200b98:	mov	x2, x0 res:000000006766722e
#LABEL: ldr1_begin>> => 0xe200b94:	ldr	w0, [x0] addr:0000000000100008 # invlaid
#LABEL: ldr1_end>> => 0xe200b98:	mov	x2, x0 res:00000000666e632e
#LABEL: ldr1_begin>> => 0xe200b94:	ldr	w0, [x0] addr:000000000010000c
#LABEL: ldr1_end>> => 0xe200b98:	mov	x2, x0 res:000000002e76662e
#LABEL: ldr1_begin>> => 0xe200b94:	ldr	w0, [x0] addr:0000000000100010  #invliad
#LABEL: ldr1_end>> => 0xe200b98:	mov	x2, x0 res:0000000076706e73
#LABEL: ldr1_begin>> => 0xe200b94:	ldr	w0, [x0] addr:0000000000100014
#LABEL: ldr1_end>> => 0xe200b98:	mov	x2, x0 res:0000000066407279
#LABEL: ldr1_begin>> => 0xe200b94:	ldr	w0, [x0] addr:0000000000100018  # invlaid
#LABEL: ldr1_end>> => 0xe200b98:	mov	x2, x0 res:0000000070766766
#LABEL: ldr1_begin>> => 0xe200b94:	ldr	w0, [x0] addr:000000000010001c
#LABEL: ldr1_end>> => 0xe200b98:	mov	x2, x0 res:000000007465622e


def get_tcg_code(ev, regs):
  code = f'''
if (pc == 0x{ev.addr:x}){{ // {ev.name}

    TCGv_i64 tcg_pc = tcg_const_i64(pc);
    TCGv_i64 x0 = read_cpu_reg(s, {regs[0]}, true);
    TCGv_i64 x1 = read_cpu_reg(s, {regs[1]}, true);
    TCGv_i64 x2 = read_cpu_reg(s, {regs[2]}, true);
    TCGv_i64 x3 = read_cpu_reg(s, {regs[3]}, true);

    F5_Func *genfn;
    genfn = gen_helper_f5_func;
    genfn(tcg_pc, x0, x1, x2, x3);
    tcg_temp_free_i64(tcg_pc);
    tcg_temp_free_i64(x0);
    tcg_temp_free_i64(x1);
    tcg_temp_free_i64(x2);
    tcg_temp_free_i64(x3);
}}

'''
  return code


def gen_tcg_code(ctx):
  lst = list(
      Z.itertools.chain(
          load_function_list('./trace/oem_functions_list.txt', filter_small=0),
          #load_function_list('./trace/functions_br_counts')
      )
  )

  code = '''
static void opa_maybe_dump_ins(CPUARMState *env, DisasContext *s, uint32_t pc) {

if (pc == 0xE200E84){

    TCGv_i64 tcg_pc = tcg_const_i64(pc);
    TCGv_i64 x0 = read_cpu_reg(s, 0, true);
    TCGv_i64 x1 = read_cpu_reg(s, 1, true);
    TCGv_i64 is_write = tcg_temp_new_i64();
    TCGv_i64 tmp = tcg_temp_new_i64();
    TCGv_i64 data = tcg_temp_new_i64();

    tcg_gen_addi_i64(tmp, x0, 8);
    int memidx = get_mem_index(s);

    do_gpr_ld_memidx(s, data, tmp, 3,
                      false, false, memidx,
                      false, 0, 0, 0);
    tcg_gen_addi_i64(tmp, tmp, 8);
    do_gpr_ld_memidx(s, is_write, tmp, 3,
                      false, false, memidx,
                      false, 0, 0, 0);
    F5_Func *genfn;
    genfn = gen_helper_f5_func;
    genfn(tcg_pc, x1, data, is_write, x0);
    tcg_temp_free_i64(is_write);
    tcg_temp_free_i64(tmp);
    tcg_temp_free_i64(data);
    tcg_temp_free_i64(tcg_pc);
}
  '''
  for x in lst:
    code += get_tcg_code(x, [19, 22, 2, 23])

  code += '}'
  print(code)


def get_data(ctx):

  tb = [
      0x00000000612e7270,
      0x000000006766722e,
      0x00000000666e632e,
      0x000000002e76662e,
      0x0000000076706e73,
      0x0000000066407279,
      0x0000000070766766,
      0x000000007465622e,
  ]
  return tb


class VM:

  def __init__(self, program, key=None, analysis=0):
    self.program = program
    self.reg = [0] * 0x10
    self.M = 2**64 - 1
    self.args = []
    self.analysis = analysis
    self.smem = SMemAccessor(raw_data=Z.pickle.load(open(smem_dec_fname, 'rb')), key=key)

  def feed_op(self, op):
    self.desc = None
    self.args = []
    return getattr(self, op.name)(*op.args)

  def exec(self):
    #x19, x22, x2
    for op in self.program:
      self.feed_op(op)

  def FUNC_RW_RAM(self, idx, data, is_write, *args):
    self.args = [idx, data, is_write]

    if is_write:
      self.desc = cmisc.Attr(args=[idx, data], rargs=[idx, data], type='ram_mem_w')
      self.smem.access_write(idx, data)
      return None
    else:
      self.desc = cmisc.Attr(args=[idx], rargs=[idx], type='ram_mem_r', ret=g_PREV_KEY)
      r = self.smem.access(idx)
      #print('R RAM ', hex(idx), hex(r))
      return r

  def reg_id(self, addr):
    return addr
    return addr - 0xe04a5d8 >> 4

  def FUNCA(self, a0, *args):
    self.desc = cmisc.Attr(args=[a0], rargs=[self.reg[a0]], type='mem_r', ret=g_PREV_KEY)

    self.args = [a0]
    a0 = self.reg_id(a0)
    #print(f'REG READ {a0:x} >> {self.reg[a0]:x}')
    return self.reg[a0]

  def FUNCB(self, a0, _, data, *args):
    self.desc = cmisc.Attr(args=[a0, data], rargs=[a0, data], type='mem_w', ret=a0)

    self.args = [a0, data]
    a0 = self.reg_id(a0)
    #print(f'REG WRITE {a0:x} >> {data:x}')
    self.reg[a0] = data
    return self.reg[a0]

  def FUNCC(self, a0, a1, *args):
    self.desc = cmisc.Attr(args=[a0, a1], rargs=[self.reg[a0], self.reg[a1]], type='+', ret=a0)
    self.args = [a0, a1]
    a0 = self.reg_id(a0)
    a1 = self.reg_id(a1)
    r = self.reg[a0] + self.reg[a1]
    #print(f'FC {a0:02x} >> {self.reg[a0]:08x} + {self.reg[a1]:08x}  >>>> {r:08x}')
    self.reg[a0] = r
    return self.reg[a0]

  def FUNCD(self, a0, a1, _, a2, *args):
    self.desc = cmisc.Attr(args=[a0, a1], rargs=[self.reg[a0], self.reg[a1]], type='&', ret=a0)

    self.args = [a0, a1]
    a0 = self.reg_id(a0)
    a1 = self.reg_id(a1)
    r = self.reg[a0] - self.reg[a1] & self.M
    #print(f'FD {a0:02x} >> {self.reg[a0]:08x} - {self.reg[a1]:08x}  >>>> {r:08x}')
    self.reg[a0] = r
    return self.reg[a0]

  def FUNCE(self, a0, a1, *args):
    self.desc = cmisc.Attr(args=[a0, a1], rargs=[self.reg[a0], self.reg[a1]], type='^', ret=a0)
    self.args = [a0, a1]
    a0 = self.reg_id(a0)
    a1 = self.reg_id(a1)
    r = self.reg[a0] ^ self.reg[a1]
    #print(f'FE {a0:02x} >> {self.reg[a0]:08x} ^ {self.reg[a1]:08x}  >>>> {r:08x}')
    self.reg[a0] = r
    return self.reg[a0]

  def FUNCF(self, a0, a1, *args):
    self.desc = cmisc.Attr(args=[a0, a1], rargs=[self.reg[a0], 1], type='-', ret=a0)

    self.args = [a0, a1]
    a0 = self.reg_id(a0)
    r = self.reg[a0] - 1 % self.M
    #print(f'FF {a0:02x} >> {self.reg[a0]:08x} - 1  >>>> {r:08x}')
    self.reg[a0] = r
    return self.reg[a0]

  def FUNCG(self, a0, a1, *args):
    self.desc = cmisc.Attr(args=[a0, a1], rargs=[self.reg[a0], a1], type='+', ret=a0)
    self.args = [a0, a1]
    a0 = self.reg_id(a0)
    r = self.reg[a0] + a1 % self.M
    #print(f'FG {a0:02x} >> {self.reg[a0]:08x} + {a1:08x}  >>>> {r:08x}')
    self.reg[a0] = r
    return self.reg[a0]

  def FUNCH(self, a0, a1, *args):
    self.desc = cmisc.Attr(args=[a0, a1], rargs=[self.reg[a0], a1], type='-', ret=a0)
    self.args = [a0, a1]
    a0 = self.reg_id(a0)
    r = self.reg[a0] - a1 % self.M
    #print(f'FH {a0:02x} >> {self.reg[a0]:08x} - {a1:08x}  >>>> {r:08x}')
    self.reg[a0] = r
    return self.reg[a0]

  def FUNCI(self, a0, a1, *args):
    if self.analysis:
      self.desc = cmisc.Attr(args=[a0, a1], rargs=[self.reg[a0], a1], type='&', ret=a0)

    self.args = [a0, a1]
    a0 = self.reg_id(a0)
    r = self.reg[a0] & a1
    #print(f'FI {a0:02x} >> {self.reg[a0]:08x} & {a1:08x}  >>>> {r:08x}')
    self.reg[a0] = r
    return self.reg[a0]

  def FUNCJ(self, *args):
    pass


def read_prog(fname):
  funcs = load_function_list('./trace/oem_functions_list.txt', filter_small=0)
  mp = {}
  for func in funcs:
    mp[func.addr] = func.name[:5]

  mp[0xE200E84] = 'FUNC_RW_RAM'

  ops = []
  for i, line in enumerate(open(fname, 'r').readlines()):

    if i == flags.stop_line: break
    d = list(map(lambda x: int(x, 16), line.strip().split(',')))
    ops.append(cmisc.Attr(name=mp[d[0]], args=d[1:]))
  return ops


def annotate(ctx):
  prog = read_prog(ctx.infile)
  for i, x in enumerate(prog):
    print(x)
    if i > 293: break
  return
  vm = VM(prog)
  vm.exec()


def guess_op(i, al, vms, rlist):
  nx = len(vms)
  opstb = []
  for j in range(len(vms[0].args)):
    for k in range(nx):
      if vms[k].args[j] != vms[0].args[j]:
        break
    else:
      continue

    def op1(a):
      return a

    def op2(a):
      return a & 0xff

    def op3(a):
      return a >> 8 & 0xff

    def op4(a):
      return a >> 16 & 0xffff

    def op5(a):
      return a << 16 & 0xffff0000

    def op6(a):
      return (a >> 8) | (a << 8 & 0xff00)

    def op7(a):
      return (a >> 8) | ((a ^ 3) << 8 & 0xff00)

    if i == 71:
      inter_op = [op1, op2, op3, op4, op5, op6, op7]
    else:
      inter_op = [op1, op2, op3, op4, op5, op6]

    ops_map = {
        op1: cmisc.Attr(type='+', rargs=[g_PREV_KEY, 0]),
        op2: cmisc.Attr(type='&', rargs=[g_PREV_KEY, 0xff]),
        op3: cmisc.Attr(type='op3', rargs=[g_PREV_KEY]),
        op4: cmisc.Attr(type='op4', rargs=[g_PREV_KEY]),
        op5: cmisc.Attr(type='op5', rargs=[g_PREV_KEY]),
        op6: cmisc.Attr(type='op6', rargs=[g_PREV_KEY]),
        op7: cmisc.Attr(type='op7', rargs=[g_PREV_KEY]),
    }

    for op in inter_op:
      for k in range(nx):
        if op(rlist[k]) != vms[k].args[j]:
          break
      else:
        opstb.append(ops_map[op])
        break
    else:
      tb = []
      for k in range(nx):
        tb.append(vms[k].args[j] ^ rlist[k])
      for k in range(nx):
        if tb[0] != tb[k]:

          Z.pprint(tb)
          Z.pprint(rlist)
          for kk in range(nx):
            print('Laa', kk, hex(vms[kk].args[j]), hex(op5(rlist[kk])), hex(rlist[kk]))
          print(i, al)
          assert 0
      opstb.append(cmisc.Attr(type='^', rargs=[g_PREV_KEY, tb[0]]))
    opstb[-1].tgt = j
    opstb[-1].args = opstb[-1].rargs

  nz = opstb

  if al.name == 'FUNCB' or al.name == 'FUNC_RW_RAM':
    assert len(nz) <= 1
  else:
    assert len(nz) == 0
  res = cmisc.safe_select(nz, 0)
  if res:
    res.ret = g_PREV_KEY
    res.arglist = [cmisc.Attr(const=0, wx=g_PREV_KEY)]
    if len(res.args) == 2:
      res.arglist.append(cmisc.Attr(const=1, val=res.args[1]))

  return res


@Z.Cachable.cachedf(fileless=0)
def get_opslist(simplify_set):
  return get_opslist_nocache(simplify_set)


def get_opslist_nocache(simplify_set, debug_ids=[], stop_at=None):
  plist = []
  plist.append(read_prog('./trace/exec.abcd'))
  plist.append(read_prog('./trace/exec.aaaa'))
  plist.append(read_prog('./trace/exec.0000'))
  plist.append(read_prog('./trace/exec.ffff'))

  vms = []
  for p in plist:
    vms.append(VM(p, analysis=1))
  nx = len(vms)

  rlist = []
  opslist = []
  for i, al in enumerate(vms[0].program):
    if i == stop_at: break
    nrlist = []
    for vm in vms:
      nrlist.append(vm.feed_op(vm.program[i]))
    if i <= 16: continue
    if vms[0].desc is None: continue

    opx = guess_op(i, al, vms, rlist)
    descs = []
    for vm in vms:
      descs.append(vm.desc)

    if opx:
      opx.id = i
      opslist.append(opx)
      #print(i, al, opx, descs[0].rargs)
    arglist = []
    for k in range(len(descs[0].rargs)):
      if opx and k == opx.tgt:
        arglist.append(cmisc.Attr(const=0, wx=g_PREV_KEY))
        continue

      #arg[k] is constant
      for j in range(nx):
        if descs[j].rargs[k] != descs[0].rargs[k]:
          arglist.append(cmisc.Attr(const=0, wx=descs[j].args[k]))
          break

      else:
        arglist.append(cmisc.Attr(const=1, val=descs[j].rargs[k]))

    if simplify_set and nrlist[0] is not None and cmisc.is_array_constant(nrlist):
      op = cmisc.Attr(
          type='set', arglist=[cmisc.Attr(const=1, val=nrlist[0])], ret=descs[0].get('ret', None)
      )
    else:
      op = cmisc.Attr(type=descs[0].type, arglist=arglist, ret=descs[0].get('ret', None))
    op.id = i
    opslist.append(op)

    if op.id in debug_ids:
      print()
      print('====== ', i, descs)
      Z.pprint(op)
      Z.pprint(opx)
      print(Z.Display.disp_list(rlist))
      print(Z.Display.disp_list(nrlist))

    rlist = nrlist
  return opslist


@Z.Cachable.cachedf(fileless=0)
def get_opslist_small(simplify_set):
  return get_opslist(simplify_set)[:0x2be0]


def get_smem():
  return SMemAccessor(raw_data=Z.pickle.load(open(smem_dec_fname, 'rb')))


def formalize_algo(ctx):
  opslist = get_opslist(ctx.simplify_set)

  cb = CodeBuilder()
  cb.build_code(g_mainfunc_name, opslist)
  cb.finalize()

  key = bytearray(key_0123)
  key[:8] = bytes([172, 173, 170, 139, 91, 85, 48, 111])
  smem = get_smem()
  bmem = K.BufMem(smem.bytes, arch=arch)
  bmem.write(g_key_pos, key)
  res = do_call_function(cb.cfptr, bmem)
  print('Result is ', hex(res.resv))
  print(res.data.read(g_key_pos, 0x20))
  print(res.data.read(g_check_pos, 0x20))


def test_inv_smem(ctx):
  smem = SMemAccessor(raw_data=Z.pickle.load(open(smem_dec_fname, 'rb')))
  tmp = b''.join(smem.raw_data)
  for i in range(0, len(tmp) - 0x10000, 0x10000):
    for j in range(256):
      x = set()
      for k in range(256):
        x.add(tmp[i + j + k * 256])
      print(hex(i), j, len(x))


def test_z3(ctx):
  smem = SMemAccessor(raw_data=Z.pickle.load(open(smem_dec_fname, 'rb')))
  mem = z3.Array('X', z3.IntSort(), z3.IntSort())
  for i in range(len(smem.bytes)):
    print('on ', i)
    z3.Store(mem, i, smem.bytes[i])

  orig = z3.BitVec('x', 16)
  end = z3.BitVecVal(0x6708, 16)
  eqs = [orig & 0xff == end >> 8]
  eqs.append(z3.Select(mem, orig | 0x20000) & 0xff == end & 0xff)
  print('Solving')
  z3.solve(eqs)


def create_smem_bin(ctx):
  smem = SMemAccessor(raw_data=Z.pickle.load(open(smem_dec_fname, 'rb')))
  open('./data.bin', 'wb').write(smem.bytes)


def do_call_function(cfptr, mem):
  p_u64 = ctypes.POINTER(ctypes.c_uint64)
  cfunc = ctypes.CFUNCTYPE(ctypes.c_int64, p_u64)(cfptr)

  bsize = g_mem_len
  dx = mem.read(0, g_mem_len)
  data = (ctypes.c_uint8 * bsize)(*dx)
  data_ptr = ctypes.cast(data, ctypes.c_void_p).value
  data_ptr = ctypes.cast(data_ptr, p_u64)

  resv = cfunc(data_ptr)
  res_data = np.ctypeslib.as_array(data).tolist()
  res_data = bytes(res_data)
  print('goot', hex(len(res_data)))
  res_data = K.BufMem(res_data, arch=arch)
  return cmisc.Attr(data=res_data, resv=resv)


class CodeBuilder:

  def __init__(self):
    llvm.initialize()
    llvm.initialize_native_target()
    llvm.initialize_native_asmprinter()
    self.module = ll.Module()
    flags.fixed_sp = True
    self.builder = ll.IRBuilder()

    self.u64_t = ll.IntType(64)
    self.u32_t = ll.IntType(32)
    self.u64_ptr_t = self.u64_t.as_pointer()
    self.u32_ptr_t = self.u32_t.as_pointer()
    # PROTYPE:
    # u64 diff_stack func(u64 data_ptr, u64 *stack_top, u64 *result)
    self.fnty = ll.FunctionType(self.u64_t, [self.u64_t])
    self.funcs = {}

  def finalize(self):
    strmod = str(self.module)
    llmod = llvm.parse_assembly(strmod)
    print(llmod)

    pmb = llvm.create_pass_manager_builder()
    pmb.opt_level = 9

    pm = llvm.create_module_pass_manager()
    pmb.populate(pm)

    pm.run(llmod)
    target_machine = llvm.Target.from_default_triple().create_target_machine()

    ee = app.global_context.enter_context(llvm.create_mcjit_compiler(llmod, target_machine))
    ee.finalize_object()
    self.cfptr = ee.get_function_address(g_mainfunc_name)
    print(target_machine.emit_assembly(llmod))

    if flags.elf_outfile:
      with open(flags.elf_outfile, 'wb') as f:
        f.write(target_machine.emit_object(llmod))

  def build_code(self, name, ops):
    func = ll.Function(self.module, self.fnty, name=name)
    self.funcs[name] = func
    self.func = func
    self.builder = ll.IRBuilder()

    builder = self.builder
    data = func.args[0]
    regs = cmisc.defaultdict(lambda: self.u64_t(0))

    func_entry = func.append_basic_block()
    builder.position_at_end(func_entry)
    const8 = self.u64_t(8)
    const16 = self.u64_t(16)
    const3 = self.u64_t(3)
    constff = self.u64_t(0xff)
    constffff = self.u64_t(0xffff)
    constff00 = self.u64_t(0xff00)
    constff0000 = self.u64_t(0xff0000)
    constffff0000 = self.u64_t(0xffff0000)

    for op in ops:
      args = []

      for arg in op.arglist:
        if arg.const:
          args.append(self.u64_t(arg.val))
        else:
          assert regs[arg.wx] is not None
          args.append(regs[arg.wx])

      r = None

      if op.type == 'set':
        r = args[0]
      elif op.type == '+':
        r = builder.add(args[0], args[1])
      elif op.type == '-':
        r = builder.sub(args[0], args[1])
      elif op.type == '^':
        r = builder.xor(args[0], args[1])
      elif op.type == '&':
        r = builder.and_(args[0], args[1])
      elif op.type == '<<':
        r = builder.shl(args[0], args[1])
      elif op.type == '>>':
        r = builder.lshr(args[0], args[1])
      elif op.type == 'mem_r':
        r = args[0]
      elif op.type == 'mem_w':
        r = regs[args[0]] = args[1]

      elif op.type == 'ram_mem_r':
        ptr = builder.add(data, args[0])
        r = builder.zext(builder.load(builder.inttoptr(ptr, self.u32_ptr_t)), self.u64_t)
      elif op.type == 'ram_mem_w':
        print('WRITING TO RAM ', args[0], args[1], op.arglist)
        ptr = builder.add(data, args[0])
        builder.store(builder.trunc(args[1], self.u32_t), builder.inttoptr(ptr, self.u32_ptr_t))

      elif op.type == 'op3':
        r = builder.and_(builder.lshr(args[0], const8), constff)
      elif op.type == 'op4':
        r = builder.and_(builder.lshr(args[0], const16), constffff)
      elif op.type == 'op5':
        r = builder.and_(builder.shl(args[0], const16), constffff0000)

      elif op.type == 'op6':
        a = builder.and_(builder.shl(args[0], const8), constff00)
        b = builder.and_(builder.lshr(args[0], const8), constff)
        r = builder.or_(a, b)

      elif op.type == 'op7':
        a = builder.and_(builder.shl(builder.xor(args[0], const3), const8), constff00)
        b = builder.and_(builder.lshr(args[0], const8), constff)
        r = builder.or_(a, b)
      else:
        assert 0

      if op.ret is not None:
        assert r is not None
        regs[op.ret] = r
        regs[g_PREV_KEY] = r

    builder.ret(regs[g_PREV_KEY])
    return func


logging.getLogger('angr').setLevel('FATAL')


def solve_angr(ctx):
  import angr
  import logging
  import claripy

  #proj = angr.Project('./a.out')
  proj = angr.Project(ctx.infile)
  good_func = proj.loader.find_symbol('good')
  bad_func = proj.loader.find_symbol('bad')

  argv1 = claripy.BVS("argv1", 8 * 8)
  initial_state = proj.factory.entry_state(args=[ctx.infile, argv1])
  sm = proj.factory.simulation_manager(initial_state)
  print('gogo explore')
  sm.explore(find=good_func.rebased_addr, avoid=bad_func.rebased_addr)
  found = sm.found[0]
  buf = found.solver.eval(argv1, cast_to=bytes)
  print(buf)
  return res


def test_algo_final(ctx):
  opslist = get_opslist_small(ctx.simplify_set)
  for op in opslist:
    #if op.type in ('ram_mem_r', 'ram_mem_w'):
    #  if op.arglist[0].const:
    print(op)


class Z3Helper:

  def __init__(self):
    self.id = 0

  def get_bvv(self, v, sz):
    return z3.BitVecVal(v, sz)

  def get_bv(self, n, name=None):
    if name is None:
      name = f'x{self.id}'
      self.id += 1
    return z3.BitVec(name, n)

  def simplify(self, x):
    if z3.is_expr(x): return z3.simplify(x)
    return x

  def is_const(self, x):
    return not z3.is_expr(x) or z3.is_bv_value(x)

  def lshr(self, x, v, mask=None):
    x = z3.LShR(x, v)
    if mask is not None:
      x = x & mask
    return x

  def extract1(self, x, pos, sz):
    if isinstance(x, int): return x >> pos & (2**sz - 1)
    return z3.Extract(pos + sz - 1, pos, x)

  def extract(self, x, sz, n=None):
    if n is None: n = x.size()
    assert n % sz == 0
    tb = []
    for i in range(0, n, sz):
      tb.append(self.extract1(x, i, sz))
    return tb

  def sub_force(self, target, subs):
    res = z3.simplify(z3.substitute(target, subs))
    assert self.is_const(res), f'{target} xx {subs}'
    return res

  def solve(self, cond, subs, target):
    s = z3.Solver()
    s.add(cond)

    for a, b in subs:
      s.add(a == b)

    s.check()
    model = s.model()
    return model[target]

  def enumerate(self, s, var):
    res = []
    while s.check() == z3.sat:
      m = s.model()
      res.append(m[var].as_long())
      s.push()
      s.add(var != res[-1])
    for i in range(len(res)):
      s.pop()
    return res



def z3_algo_final(ctx):
  sz = 32
  helper = Z3Helper()
  key = []
  expected_res = []
  actual_res = []

  for i in range(g_key_len):
    key.append(helper.get_bv(8, f'key{i}'))
    expected_res.append(helper.get_bv(8, f'expected_res{i}'))
    actual_res.append(helper.get_bv(8, f'actual_res{i}'))

  key.append(helper.get_bvv(0, 8)) # padding
  key.append(helper.get_bvv(0, 8))

  def make_num(x=0, sz_=None):
    if sz_ is None: sz_ = sz
    return z3.BitVecVal(x, sz_)

  regs = cmisc.defaultdict(make_num)
  res_conds = [cmisc.Attr() for i in range(g_key_len)]

  const8 = make_num(8)
  const16 = make_num(16)
  const3 = make_num(3)
  constff = make_num(0xff)
  constffff = make_num(0xffff)
  constff00 = make_num(0xff00)
  constff0000 = make_num(0xff0000)
  constffff0000 = make_num(0xffff0000)

  s = z3.Solver()
  for a, b in zip(expected_res, actual_res):
    s.add(a == b)

  conds = []
  fbox = []

  opslist = get_opslist(True)
  ANS = b''
  for op in opslist:
    args = []
    if op.id == 43035: break # when final check is being done. we are done then

    for arg in op.arglist:
      if arg.const:
        args.append(arg.val)
      else:
        assert regs[arg.wx] is not None
        args.append(regs[arg.wx])

    r = None

    if op.type == 'set':
      r = args[0]
    elif op.type == 'mem_r':
      r = args[0]
    elif op.type == 'mem_w':
      r = regs[args[0]] = args[1]

    elif op.type == 'ram_mem_r':
      if op.arglist[0].const:
        assert g_key_pos <= args[0] < g_key_pos + g_key_len
        pid = args[0] - g_key_pos

        if pid % 8 == 0:
          s.push()
          conds = []
          fbox = []

        r = z3.Concat(*key[pid:pid + 4][::-1])
      else:
        a0 = helper.simplify(args[0])
        a0_var = helper.get_bv(sz)
        conds.append(a0 == a0_var)
        fbox_res = helper.get_bv(8)
        print('Creating link ', a0, a0_var, fbox_res)
        fbox.append((a0_var, fbox_res))
        fbox_res = z3.Concat(z3.BitVecVal(0, sz - 8), fbox_res)
        r = fbox_res

    elif op.type == 'ram_mem_w':
      if g_key_pos <= args[0] < g_key_pos + g_key_len:
        pid = args[0] - g_key_pos
        r1 = z3.Concat(*actual_res[pid:pid + 4][::-1])
        a1 = helper.simplify(args[1])
        for i, b in enumerate(helper.extract(a1, 8)):
          res_conds[pid + i].var = b

        if pid % 8 == 4:
          ANS += solve_keyrange(s, helper, res_conds, conds, fbox, key, pid-4)
          print('NOW ', ANS, ANS.hex())
          s.pop()
          if pid + 4 == g_key_len: break


      elif g_check_pos <= args[0] < g_check_pos + g_key_len:
        pid = args[0] - g_check_pos
        r1 = z3.Concat(*expected_res[pid:pid + 4][::-1])
        a1 = helper.simplify(args[1])
        for i, b in enumerate(helper.extract(a1, 8, 32)):
          res_conds[pid + i].val = b

    elif op.type == 'op3':
      r = helper.lshr(args[0], 8, 0xff)
    elif op.type == 'op4':
      r = helper.lshr(args[0], 16, 0xffff)
    elif op.type == 'op5':
      r = args[0] << 16 & 0xffff0000

    elif op.type == 'op6':
      r = (args[0] << 8 & 0xff00) | helper.lshr(args[0], 8, 0xff)

    elif op.type == 'op7':
      r = ((args[0] ^ 3) << 8 & 0xff00) | helper.lshr(args[0], 8, 0xff)
    else:
      a0 = helper.simplify(args[0])
      a1 = helper.simplify(args[1])
      if not op.arglist[0].const and not op.arglist[1].const:
        print()
        print(
            helper.is_const(a0), helper.is_const(a1), op.type, op.id, z3.simplify(a0),
            z3.simplify(a1)
        )
      try:
        assert helper.is_const(a0) == op.arglist[0].const, str(a0)
        assert helper.is_const(a1) == op.arglist[1].const, str(a1)
      except:
        print('FAIL ON ', op)
        print('Got ', a0)
        print('Got ', a1)
        raise

      r = eval(f'args[0] {op.type} args[1]')

    if op.ret is not None:
      assert r is not None
      regs[op.ret] = r
      regs[g_PREV_KEY] = r

  print('NOW ', ANS, ANS.hex())

def solve_keyrange(s, helper, res_conds, conds, fbox, key, pos):
  if pos == 0:
    return  bytes([172, 173, 170, 139, 91, 85, 48, 111])
  #acadaa8b5b55306fb3c6dfc3b2d1c807
  #acadaa8b5b55306fb3c6dfc3b2d1c80770084644225febd7
  #acadaa8b5b55306fb3c6dfc3b2d1c80770084644225febd71a9189aa26ec740e


  #9e915a63d3c4d57eb3da968570d69e95@challenge.sstic.org
  #SSTIC{acadaa8b5b55306fb3c6dfc3b2d1c80770084644225febd71a9189aa26ec740e}

  print('Try solve keyrange ', pos)
  print(res_conds)

  smem = get_smem()
  bmem = K.BufMem(smem.bytes, arch=arch)
  s.check()
  model = s.model()
  nodes = []
  var_to_nodes = Z.defaultdict(list)

  def get_subs(ctx, varlist):
    resvar = None
    sub = []
    for var in a.varlist:
      if var in ctx:
        sub.append((var, ctx[var]))
      else:
        assert resvar is None
        resvar = var
    return sub, resvar

  def process_fbox(bmem, helper, ctx, fbox):
    subs, fixvar = get_subs(ctx, a.varlist)
    expected = ctx[fbox.outvar]

    res = []
    for i in range(256):
      nsubs = list(subs)
      nsubs.append((fixvar, helper.get_bvv(i, 8)))
      v = helper.sub_force(fbox.inexpr, nsubs).as_long()
      val = bmem.read_u8(v)
      if val == expected:
        res.append(i)

    assert len(res) == 1
    return fixvar, helper.get_bvv(res[0], 8)

  def process_end_node(helper, ctx, a):
    sub, resvar = get_subs(ctx, a.varlist)
    res = helper.solve(a.var == a.val, sub, resvar)
    return resvar, res




  for cond in conds:
    s.add(cond)

  assert s.check() == z3.sat
  assert s.check() == z3.sat

  for i in range(pos, pos+8):
    s.add(res_conds[i].var == helper.get_bvv(res_conds[i].val, 8))
  assert s.check() == z3.sat

  for i, (a, b) in enumerate(reversed(fbox)):
    expected = s.model()[b]
    var_in = z3.simplify(a)

    can = []
    cnds =helper.enumerate(s, var_in)
    print('GOOT num vars >> ', len(cnds), i, len(fbox))

    for y in cnds:
      val = bmem.read_u8(y)
      if val == expected:
        can.append(y)
    assert len(can) == 1
    s.add(var_in == can[0])
    assert s.check() == z3.sat
  tb = []
  m = s.model()
  for i in range(pos, pos+8):
    tb.append(m[key[i]].as_long())
  return bytes(tb)

  #else:
  #  for i in range(8):
  #    var = z3.simplify(res_conds[i].var)
  #    varlist = z3_list_vars(var)
  #    node = cmisc.Attr(var=var, varlist=varlist, val=res_conds[i].val, fbox=0)
  #    print(var, varlist)
  #    nodes.append(node)

  #  for a, b in fbox:
  #    var_in = z3.simplify(a)
  #    varlist = z3_list_vars(var_in) + [b]
  #    node = cmisc.Attr(varlist=varlist, inexpr=a, outvar=b, fbox=1)
  #    nodes.append(node)

  #  q = Z.deque()
  #  for node in nodes:
  #    node.deg = len(node.varlist)
  #    for v in node.varlist:
  #      var_to_nodes[v].append(node)

  #    if node.deg == 1:
  #      q.append(node)

  #  print(len(q))


  #  solve_ctx = dict()
  #  while q:
  #    a = q.popleft()
  #    var = None
  #    val = None
  #    print()
  #    print('processing ', a)
  #    if a.fbox:
  #      var, val = process_fbox(bmem, helper, solve_ctx, a)
  #    else:
  #      var, val = process_end_node(helper, solve_ctx, a)
  #    print('NEW FIND ', var, val)

  #    solve_ctx[var] = val
  #    for node in var_to_nodes[var]:
  #      print('FREE 1 ', node)
  #      node.deg -= 1
  #      if node.deg == 1:
  #        q.append(node)

  #  print(solve_ctx)
  #  Z.create_kernel()

  #  #print(model[expected_res].as_long().to_bytes(g_key_len, 'little'))
  #  #print(model[actual_res].as_long().to_bytes(g_key_len, 'little'))

def debug_ops(ctx):
  get_opslist_nocache(True, ctx.debug_ids)


@cmisc.yield_wrapper
def z3_list_vars(expr):
  import z3

  def visitor2(e, seen):
    import z3
    if e in seen:
      return
    seen[e] = True
    yield e
    if z3.is_app(e):
      for ch in e.children():
        for e in visitor2(ch, seen):
          yield e
      return
    if z3.is_quantifier(e):
      for e in visitor2(e.body(), seen):
        yield e
      return

  seen = {}
  for e in visitor2(expr, seen):
    if z3.is_const(e) and e.decl().kind() == z3.Z3_OP_UNINTERPRETED:
      yield e
    else:
      pass


def main():

  ctx = Attributize()
  global g_ctx
  g_ctx = ctx
  if flags.key_a:
    flags.prog_key = key_aaaa.hex()

  key = bytearray.fromhex(flags.prog_key)
  if flags.modkey: exec(flags.modkey)

  flags.prog_key = key.hex()
  flags.keybin = key

  if flags.bad_prog:
    ctx.prog = bad_file_path
  else:
    ctx.prog = good_file_path
  flags.printfile = None

  ctx.prog_cmd = f'{ctx.prog} {flags.prog_key}'
  ctx.trace_file = f'/tmp/trace_{flags.runid}.out'
  ActionHandler.Run(ctx)


app()
