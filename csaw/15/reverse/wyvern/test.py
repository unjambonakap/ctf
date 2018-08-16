#!/usr/bin/python

import idaapi
import idc
import idautils
import time
import struct
import chdrft.ida.common as ida
from curses.ascii import isprint
from chdrft.utils.misc import Attributize
import re
import chdrft.utils.ops as ops

start = 0x40e120


def wait_susp():
  while True:
    res = idc.GetDebuggerEvent(idc.WFNE_SUSP, -1)
    if res == idc.WFNE_NOWAIT:
      break


def go(addr):
  while True:
    idc.GetDebuggerEvent(idc.WFNE_CONT | idc.WFNE_SUSP, -1)
    if idc.GetRegValue('eip') == addr:
      break


def get_str(addr):
  s = ''
  n = 0x100
  while True:
    x = idc.DbgRead(addr, n)
    for j in range(len(x)):
      if ord(x[j]) == 0:
        s += x[:j]
        return s
    s += x
    addr += len(x)
  return s


def setup_buf_bpt(ptr, n, enable):
  for i in range(n):
    u = ptr + i
    if enable:
      idc.AddBptEx(u, 1, idc.BPT_RDWR)
    else:
      idc.DelBpt(u)


def disable_trace():
  idc.EnableTracing(idc.TRACE_INSN, 0)


def start_trace():
  idc.ClearTraceFile('')
  idc.EnableTracing(idc.TRACE_INSN, 1)
  idc.SetStepTraceOptions(idc.ST_OVER_LIB_FUNC)


def ida_continue():
  idc.GetDebuggerEvent(idc.WFNE_CONT, 0)


class Hooker(idaapi.DBG_Hooks):

  def __init__(self, buf, round):
    super(Hooker, self).__init__()
    self.done = False
    self.exited = False
    self.check_ea = 0x402a7f
    self.fgets_ea = 0x40e1f5
    self.buf=buf
    self.next=None
    self.round=round
    self.pos=0

    idc.AddBpt(self.fgets_ea)
    idc.AddBpt(self.check_ea)
    self.res_val = None

  def dbg_bpt(self, tid, ea):
    #if ea == self.cond_ea:
    #    self.done = True
    #    self.res_val = idc.DbgDword(idautils.cpu.esi)
    print('ON >> ', hex(ea), 'want ')

    if ea == self.fgets_ea:
      next_addr=0x40e1fa
      idautils.cpu.rip=next_addr
      idautils.cpu.rax=len(self.buf)
      idc.DbgWrite(idautils.cpu.rdi, self.buf)
    elif ea==self.check_ea:
      eax=idautils.cpu.eax
      ecx=idautils.cpu.ecx
      print('GOT >>> ', self.pos, self.round, hex(eax), hex(ecx), self.buf)
      if eax!=ecx or self.round==self.pos:
        self.got=[eax, ecx]
        self.done=1
      self.pos+=1

    return 0

  def dbg_process_exit(self, pid, tid, ea, code):
    print('exited >> ', pid, tid, ea, code)
    self.exited = True

  def off(self):
    idc.StopDebugger()
    print('gogo exit')

    while not self.exited:
      idc.GetDebuggerEvent(idc.WFNE_ANY, 1)

    self.unhook()

  def run(self):
    while not self.done and not self.exited:
      ida_continue()


def stop_debugger():
  idc.StopDebugger()
  print('gogo exit')

  while not self.exited:
    idc.GetDebuggerEvent(idc.WFNE_ANY, 1)


def setup():
  path = '/home/benoit/programmation/hack/csaw/15/reverse/wyvern/wyvern_c85f1be480808a9da350faaa6104a19b'
  for i in range(10):
    res = idc.StartDebugger(
        path, '',
        '/home/benoit/programmation/hack/csaw/15/reverse/wyvern')
    if res == 1:
      break
    idc.StopDebugger()
    time.sleep(1)
  else:
    assert False, 'Could not start debugger'
  wait_susp()


def solve(prefix, c):
  idc.AddBpt(start)
  n=0x1c
  ans=prefix+c*(n-len(prefix))
  ans+='\n'
  ans=bytearray(ans.encode())
  ans.append(0)
  print(len(ans))

  setup()
  h = Hooker(bytes(ans), len(prefix))
  assert h.hook()
  h.run()
  print('NEXT NEEDED >> ', h.got)
  h.off()
  time.sleep(0.1)
  return h.got

def go():

  n=0x1c
  cur=''
  for i in range(n):
    c='a'
    got=solve(cur, c)
    cur+=chr(ord(c)+got[0]-got[1])
    print('CURRENT SOLUTION >> ', cur)


def main():

  idc.AddBpt(start)

  n=0x1c
  ans='r'*n
  ans+='\n'
  ans=bytearray(ans.encode())
  ans.append(0)

  for j in range(n):
    for i in range(ord('A'), ord('z')):
      setup()
      print('GOING FOR >> ', i)
      ans[j]=i
      ans[0]=0x64

      h = Hooker(bytes(ans), j+1)
      assert h.hook()
      h.run()
      print('NEXT NEEDED >> ', h.next)
      print('CHR >> ', chr(h.next))
      return
      h.off()
      time.sleep(1)
    return

#run with
#import test as test; test=reload(test); test.main()
