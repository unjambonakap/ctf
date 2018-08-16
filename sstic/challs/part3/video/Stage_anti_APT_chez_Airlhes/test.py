#!/usr/bin/python

import traceback
import idaapi
import idc
import idautils
import time
import struct
import chdrft.ida.common as ida
from chdrft.utils.misc import Attributize
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


def analyse_read():
  read_buf = idc.DbgDword(idautils.cpu.esp + 0x8)
  nread = idc.DbgDword(idautils.cpu.esp + 0xc)
  nread_out = idc.DbgDword(idautils.cpu.esp + 0x10)
  return Attributize(None, **locals())


def setup_buf_bpt(ptr, n, enable):
  for i in range(n):
    u = ptr + i
    if enable:
      idc.AddBptEx(u, 1, idc.BPT_RDWR)
    else:
      idc.DelBpt(u)


def stage2(data):
  read_data = analyse_read()
  ret_addr = idc.DbgDword(idautils.cpu.esp)
  idautils.cpu.esp += 0x14 + 4
  idautils.cpu.eip = ret_addr
  data += '\r\n'
  idc.DbgWrite(read_data.read_buf, data)
  idc.DbgWrite(read_data.nread_out, struct.pack('<I', len(data)))

  return read_data

def write_u32(addr, v):
  idc.DbgWrite(addr, struct.pack('<I', v))
def write_u16(addr, v):
  idc.DbgWrite(addr, struct.pack('<H', v))

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
    self.want_str = data['s']
    self.count = 0
    self.sent_data=[]
    self.screen_data=[]

    self.screen_buf_ea = idc.LocByName('screen_buffer')

    self.push_screen_ea = idc.LocByName('push_screen')
    self.deque_ea = 0x00403C15
    self.prepare_reg_send = 0x0040364F
    self.prepare_str_ea = 0x00403517
    self.test_time_start = idc.LocByName('loc_403E61')
    self.test_time_end=0x00403E66
    self.test_time_mod=0x00403767
    self.enqueue_ea = 0x004035F0
    self.enqueue_func=idc.LocByName('enqueu_shared')
    self.test_time_func = idc.LocByName('should_exfiltrate')

    if 0 :
      idc.AddBpt(self.test_time_mod)
      idc.AddBpt(self.test_time_end)

    #idc.AddBpt(self.push_screen_ea)
    idc.AddBpt(self.deque_ea)
    idc.AddBpt(self.prepare_str_ea)
    idc.AddBpt(self.prepare_reg_send)
    idc.AddBpt(self.enqueue_ea)
    #idc.AddBpt(self.enqueue_func)
    self.screen_count=0
    self.time=0
    self.dec_data=[]
    self.enc_data=[]
    self.tmp_tb=None
    self.cur_byte=0
    self.tb2=[]

  def save_screen(self):
    w=1280
    h=720
    buf=idc.DbgRead(self.screen_buf_ea, w*h*4)
    filename='/tmp/imgs/f1_%05d.p7'%self.screen_count
    open(filename, 'wb').write(buf)

    self.screen_count+=1
    self.last_edi=None

  def dbg_bpt(self, tid, ea):
    #if ea == self.cond_ea:
    #    self.done = True
    #    self.res_val = idc.DbgDword(idautils.cpu.esi)
    #print('ON >> ', hex(ea), 'want ')

    try:
      if ea == self.push_screen_ea:
        tmp=idc.DbgRead(self.screen_buf_ea, 6)
        self.screen_data.append(tmp)
        print('pushing screen here', tmp)
        self.count += 1
        if 0 and self.count == 10000:
          self.done = 1
        if self.count%10==0:
          self.save_screen()

      elif ea == self.deque_ea:
        recv_word = idautils.cpu.eax
        mask=idc.DbgDword(idautils.cpu.ebp-0x6070)
        self.dec_data.append([recv_word, mask])
        if 1 and len(self.dec_data)==0x1000/8:
          self.done=1
        print('DEQUE >> ', hex(recv_word), hex(mask))

      elif ea == self.prepare_reg_send:
        if 1: return
        idc.DbgWrite(idautils.cpu.esp+0x3c-0x1d, chr(self.cur_byte))

        abc=idc.DbgRead(idautils.cpu.esp+0x3c-0x1d, 1)
        print('SENDING CHAR >> ', abc, self.cur_byte)
        self.tmp_tb=[]
        self.last_edi=idautils.cpu.edi

      elif ea == self.enqueue_func:
        print('SKIPPING ENQUEUE')
        if 0: return
        do_ret()
      elif ea == self.enqueue_ea:
        #if 0: return
        if self.tmp_tb is not None:
          nedi=idautils.cpu.edi
          send_word=(nedi-self.last_edi)%8
          self.last_edi=nedi
          self.tmp_tb.append(send_word)
          self.tb2.append([nedi, hex(idautils.cpu.eax)])
          print('GOT TB LEN ', self.tmp_tb)
          if len(self.tmp_tb)==3:
            self.enc_data.append(self.tmp_tb)
            self.tmp_tb=None
            self.cur_byte+=1
            self.last_edi=None
            if self.cur_byte==256:
              self.done=1

          print('ENQUEUE >> ', send_word)
      elif ea == self.prepare_str_ea:

        if 1: return
        buf_len = idc.DbgDword(idautils.cpu.esi + 0x38)
        buf_addr = idc.DbgDword(idautils.cpu.esi + 0x34)
        buf = idc.DbgRead(buf_addr, buf_len)
        print(buf_len, buf_addr, buf)
        assert len(self.want_str) <= buf_len
        idc.DbgWrite(buf_addr, self.want_str)
        idc.DbgWrite(idautils.cpu.esi + 0x38, struct.pack('<I', len(self.want_str)))

        print('string is set')

        #self.done = 1
      elif ea==self.test_time_end:
        if self.time>=3600*24:
          self.done=1
          #entre 23h et 1h
        else:
          idautils.cpu.eip=self.test_time_start
          resv=idautils.cpu.eax
          h,m,s=self.get_time(self.time)
          print 'REsult: %d:%d:%d >> %d'%(h,m,s,resv)
          self.time+=60

      elif ea==self.test_time_mod:
        h,m,s=self.get_time(self.time)
        addr=idautils.cpu.ebx
        write_u16(addr+4*2, h)
        write_u16(addr+5*2, m)
        write_u16(addr+6*2, s)
    except:
      traceback.print_exc()
      print('FAILED here')
      self.done=1


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
  path = 'C:/Users/benoit/work/Airlhes_screensaver.scr'
  for i in range(10):
    idc.StopDebugger()
    res = idc.StartDebugger(path, '', 'C:/Users/benoit/work')
    print('got res >> ', res)
    if res == 1:
      break
    idc.StopDebugger()
    time.sleep(1)
  else:
    assert False, 'Could not start debugger'
  wait_susp()


def main():
  print('\n\n')
  start = 0x401000
  idc.AddBpt(start)
  setup()
  data = dict(s=binascii.unhexlify('010ff0'))

  h = Hooker(data)
  try:
    assert h.hook()
    h.run()
  except:
    pass
  print(h.sent_data)
  print(h.screen_data)
  h.off()
  print(h.dec_data)
  print('ENC DATA >> ', h.enc_data)
  print 'tb2 >> ', h.tb2
  return h.dec_data

#run with
#import test as test; test=reload(test); test.main()
