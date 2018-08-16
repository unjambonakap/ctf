#!/usr/bin/env python
from unicorn import *
from chdrft.main import app
from chdrft.utils.misc import cwdpath, Attributize, Arch, opa_print, to_list, lowercase_norm
from chdrft.utils.math import rotlu32, modu32
from chdrft.emu.elf import ElfUtils, MEM_FLAGS
from chdrft.emu.binary import X86Machine, cs_print_x86_insn, Memory, Regs
from chdrft.emu.syscall import SyscallDb
from chdrft.emu.code_db import g_code, g_asm
from chdrft.emu.structures import StructureReader, Structure, BufferMemReader
from chdrft.emu.trace import Tracer, TraceDiff, WatchedMem, TraceEvent, VmOp
from chdrft.emu.kernel import Kernel, load_elf
from chdrft.tube.sock import Sock
import multiprocessing as mp

import binascii
import ctypes
import pprint as pp
import threading
import time

import struct
from capstone.x86_const import *
import traceback
import jsonpickle
import sys
from unicorn.x86_const import *


import json
import base64
from chdrft.utils.misc import Attributize
from chdrft.emu.elf import ElfUtils


def get1(a):
  x = Attributize()
  x.data = base64.b64decode(a['Data'])
  x.offset = a['Offset']
  return x

def try_one(tb, buf):
  stack_seg=0x100000
  stack_size=0x10000

  entry_addr = 0x51466a42e705
  offset_addr_size = [[0x0000000000001000, 0x00002b0000000000, 0x00001ef000000000],
                 [0x00002afffffe1000, 0x000049f000000000, 0x0000161000000000],
                 [0x000049effffe1000, 0x0000000000020000, 0x00002afffffe0000],]

  def read_handler(data):
    print('read handler KAPAPA', data)
    addr=data.args[1].val._val
    print(buf)
    print('read handler iat  addr ', hex(addr))
    kern.mem.write(addr, buf)
    kern.regs.rax=len(buf)

  got_exc=0

  def safe_hook(func):
    def hook_func(uc, *args):
      try:
        func(uc, *args)
      except Exception as e:
        traceback.print_exc()
        print('FUUU')
        print('Got exceptino , stopping emu>> ', e)
        got_exc=1
        uc.emu_stop()

    return hook_func



  mu = Uc(UC_ARCH_X86, UC_MODE_64)
  log_file = '/tmp/info.out'
  kern = Kernel(mu, log_file, read_handler=read_handler)
  kern.regs.rip = entry_addr

  mu.mem_map(stack_seg, stack_size, UC_PROT_WRITE|UC_PROT_READ)
  kern.regs.rsp=stack_seg+stack_size-0x100
  mapped=[]
  for e in tb:
    for offset, addr, size in offset_addr_size:
      if offset<=e.offset<offset+size:
        cur_addr=addr+e.offset-offset
        print('mapping addr ', hex(cur_addr), e.data[0xc:30])
        mu.mem_map(cur_addr, len(e.data), UC_PROT_EXEC|UC_PROT_READ)
        mapped.append(cur_addr)
        mu.mem_write(cur_addr, e.data)
        break
  mapped.sort()

  mu.hook_add(UC_HOOK_INTR, safe_hook(kern.hook_intr))
  mu.hook_add(UC_HOOK_MEM_FETCH_UNMAPPED, safe_hook(kern.hook_unmapped))

  mu.hook_add(UC_HOOK_INSN, safe_hook(kern.hook_syscall), None, 1, 0, UC_X86_INS_SYSCALL)
  mu.hook_add(UC_HOOK_CODE, safe_hook(kern.hook_code), None, 0, -1)
  mu.hook_add(UC_HOOK_MEM_READ | UC_HOOK_MEM_WRITE, safe_hook(kern.hook_mem_access), None,
              1, 0)

  #addrx=0x000049e7e541be38
  #insn=kern.mem.read(addrx, 0x200)
  #kern.dec.disp_ins(insn, addrx)
  #sys.exit(0)


  input_start=0x000000000010ec00
  input_end=input_start+0x20
  print('look at ', hex(input_start), hex(input_end))
  read_log=[]
  def input_read(uc, access, address, size, value, user_data):
    if kern.ignore_mem_access:
      return
    offset=address-input_start
    read_log.append([hex(kern.regs.rip), offset, size])

  mu.hook_add(UC_HOOK_MEM_READ, safe_hook(input_read), None,
              input_start, input_end)



  print('BUF >> ', binascii.hexlify(kern.mem.read(0x000049e7e541be38, 0x200)))

  event_log = open('/tmp/events.out', 'w')
  kern.tracer.cb = lambda x: event_handle(x, event_log)

  while True:
    try:
      print('starting >> ', hex(kern.regs.rip))
      kern.start()
    except UcError as e:
      print(e)
    except AssertionError as e:
      break
    if got_exc:
      break
    np=None
    for e in mapped:
      if e>=kern.regs.rip:
        np=e
        break
    if not np:
      break
    if kern.regs.rip==np:
      break
    print('GO from ', hex(kern.regs.rip), 'to', hex(np), 'with', hex(kern.regs.rax))
    kern.regs.rip=np
  return read_log


def main():
  tb = json.loads(open('/tmp/dat1', 'r').read())
  tb = list([get1(x) for x in tb])
  for e in tb:
    print(hex(e.offset))

#Type           Offset             VirtAddr           PhysAddr
#FileSiz            MemSiz              Flags  Align
#LOAD           0x0000000000001000 0x00002b0000000000 0x00002b0000000000
#0x00001ef000000000 0x00001ef000000000  R E    1000
#LOAD           0x00002afffffe1000 0x000049f000000000 0x000049f000000000
#0x0000161000000000 0x0000161000000000  R E    1000
#LOAD           0x000049effffe1000 0x0000000000020000 0x0000000000020000
#0x00002afffffe0000 0x00002afffffe0000  R E    1000

  fx=open('/tmp/t1', 'wb')
  for e in tb:
    fx.write(e.data)

  buf=bytearray(b'a'*0x20)

  def setx(pos, v):
    buf[pos*2:pos*2+len(v)]=v
  def set32(pos, v):
    setx(pos, binascii.hexlify(struct.pack('<I', v)))
  setx(0, b'29')
  ## need 256+0x65 / 3 = 119 iterations -> put at 256-119 = 137 = 0x89
  setx(2, b'7ed1')
  setx(0xb, b'8c')
  setx(1, b'89')
  setx(0xc, b'89341bec')
  setx(8, b'd54ec08c')
  set32(4, 3174346476^0x0000000024b87838)
  #buf=bytearray(b'29897ED13878B824D54EC08C89341BEC')
  buf.append(0)
  print('GOT BUF >>', buf)

  if 0:
    i=15
    buf[i]=buf[i]^1

  #setx(1, b'ff')

  buf2=bytes(buf)
  res=try_one(tb, buf2)
  print('EVENT KAPPA', len(res))

    #print('WRITING >> ', buf)
    #self.info.append('WRITING >> ' + bytes(buf).decode())
    #self.dump_log()



def event_handle(e, fevent):
  if isinstance(e, TraceEvent):
    fevent.write(str(e) + '\n\n')
    fevent.flush()

main()
