#!/usr/bin/python

import traceback as tb
import idaapi
import idc
import idautils
import time
import struct
import chdrft.ida.common as ida
import re
import chdrft.utils.ops as ops
import binascii

start = 0x401c48

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


def step():
  go(f1_addr)
  res = get_str(idautils.cpu.ebp)
  f = open('/tmp/res.out', 'a+')
  f.write(res)
  f.close()
  return res



def setup_buf_bpt(ptr, n, enable):
  for i in range(n):
    u = ptr + i
    if enable:
      idc.AddBptEx(u, 1, idc.BPT_RDWR)
    else:
      idc.DelBpt(u)

  return read_data

def write_u32(addr, v):
  idc.DbgWrite(addr, struct.pack('<I', v))
def write_u16(addr, v):
  idc.DbgWrite(addr, struct.pack('<H', v))

def read_u32(addr):
  return struct.unpack('<I', idc.DbgRead(addr, 4))[0]


def req_web(host, path):
  x = 'http://'+host+path
  import subprocess as sp
  return sp.check_output(['curl', x])




def disable_trace():
  idc.EnableTracing(idc.TRACE_INSN, 0)


def start_trace():
  idc.ClearTraceFile('')
  idc.EnableTracing(idc.TRACE_INSN, 1)
  idc.SetStepTraceOptions(idc.ST_OVER_LIB_FUNC)


def ida_continue():
  idc.GetDebuggerEvent(idc.WFNE_CONT, 0)

def do_ret():
  retaddr=idc.DbgDword(idautils.cpu.esp)
  idautils.cpu.esp+=4
  idautils.cpu.eip=retaddr

class Hooker(idaapi.DBG_Hooks):

  def __init__(self, data):
    super(Hooker, self).__init__()
    self.done = False
    self.exited = False
    self.data = data

    self.send_req_ea = idc.LocByName('send_req')
    self.decrypt_ea = idc.LocByName('decrypt')
    self.malloc2_ea = idc.LocByName('malloc2')
    decrypt_func = idaapi.get_func(self.decrypt_ea)
    self.decrypt_end_ea = decrypt_func.endEA - 1

    idc.AddBpt(self.send_req_ea)
    #idc.AddBpt(self.decrypt_ea)
    idc.AddBpt(self.decrypt_end_ea)
    self.reqid = 0
    self.bufs = []

  def prepare(self):
    for i in range(5):
      self.bufs.append(idaapi.Appcall.malloc2(0x8000))

  def dbg_bpt(self, tid, ea):
    try:
      if self.done:
        print('should be done')
        return 0
      if ea == self.send_req_ea:
        print('ON SEND REQ')
        self.reqid += 1
        a = read_u32(idautils.cpu.esp+4)
        b = read_u32(idautils.cpu.esp+8)
        print(a,b)
        a = get_str(a)
        b = get_str(b)
        print(a,b)
        content = req_web(a,b)

        do_ret()
        ea = self.bufs[self.reqid-1]
        idautils.cpu.eax = ea
        idc.DbgWrite(ea, content)
        print('GOT CONTENT >> ', content)
        if self.reqid >= 4:
          self.done = 1

      elif ea == self.decrypt_end_ea:
        tmp = read_u32(idautils.cpu.eax)
        rem = idc.DbgRead(idautils.cpu.eax+4, 0x3000)
        print('DECRYPTING >>>', tmp, rem)

    except Exception as e:
      tb.print_exc()
      self.done = 1
      print('FAILURE')

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
    while not self.done:
      ida_continue()
  def get_time(self, t):
    return t/3600, t/60%60, t%60


def stop_debugger():
  idc.StopDebugger()
  print('gogo exit')

  while not self.exited:
    idc.GetDebuggerEvent(idc.WFNE_ANY, 1)


def setup():
  args = r'"C:\Users\benoit\AppData\Roaming\Microsoft\Internet Explorer\browserassist.dll"'
  path = r'C:\Users\benoit\work\binstall'
  exe = r'C:\Users\benoit\work\binstall\build\firefox.exe'
  idc.StopDebugger()

  res = idc.StartDebugger(exe, args, path)
  print('starting dbugger')
  time.sleep(1)
  wait_susp()


def main():
  data = dict()

  h = Hooker(data)
  print('HOOKER SETUP')
  setup()
  print('RUNNIG NOW')
  ida_continue()
  ida_continue()
  wait_susp()
  h.prepare()
  try:
    try:
      assert h.hook()
      h.run()
    except:
      pass
    h.off()
  except:
    h.unhook()

#cp('k9btBW7k2y')

#run with
# import flare as test; test=reload(test); test.main()
