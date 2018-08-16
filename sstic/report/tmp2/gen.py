#!/usr/bin/env python

import binascii
import subprocess as sp
import mmap
from chdrft.tube.serial import Serial
import re
import traceback
import time

def get_ok_pos(data):
  res=re.findall(b'(Sorry|Success)', data)
  for pos, e in enumerate(res):
    if e==b'Success':
      return pos
  return None

def solve(buf, pos):
  res=None

  proc=None
  try:
    filename='test.nsh'
    with open('./hda-contents/%s'%filename, 'w') as f:
      f.write('echo -off\n')
      for i in range(256):
        buf[pos]=i
        bufhex=binascii.hexlify(buf)
        f.write('foo.efi %s\n'%bufhex.decode())
      f.write('echo DONE_KAPPA\n')
      f.write('echo DONE_KAPPA > done_file\n')

    cmd='qemu-system-x86_64 -L . -hda fat:hda-contents -bios bios.bin  -nographic -serial pty -monitor stdio -S'
    proc=sp.Popen(cmd, shell=True, stdin=sp.PIPE, stdout=sp.PIPE, stderr=sp.PIPE)
    data=b''
    pts=None
    while True:
      data+=proc.stderr.read(1)
      m=re.search(b'(/dev/pts/[0-9]+)\s', data)
      if m:
        pts=m.group(1).decode()
        break
    print(data)
    print(pts)
    proc.stdin.write(b'c\n')
    proc.stdin.flush()


    with Serial(pts) as conn:
      data=b''
      while True:
        data+=conn.recv(1)
        if data.find(b'Shell>')!=-1:
          break
      print('START HERE')
      conn.send(b'fs0:\r\n')
      time.sleep(0.5)

      conn.send(('%s\r\n'%filename).encode())

      data=b''
      while True:
        data+=conn.recv(1)
        if data.find(b'DONE_KAPPA')!=-1:
          break

      print('res >>', data)
      res=get_ok_pos(data)
  except Exception as e:
    print('exception >> ', e)
    traceback.print_exc()
    pass
  proc.stdin.write(b'q\n')
  proc.stdin.flush()
  proc.kill()
  return res


#idaapi.get_fileregion_offset(0x10000976)
byte_offset=2422

def main():
  buf=bytearray([0]*16)
  sp.check_call('cp ./orig.efi ./hda-contents/foo.efi', shell=True)
  with open('./hda-contents/foo.efi', 'r+b') as efi:
    mp=mmap.mmap(efi.fileno(), 0)
    for pos in range(16):
      if 0:
        print(mp[byte_offset])
        print(binascii.hexlify(mp[byte_offset-10:byte_offset+10]))

      mp[byte_offset]=pos+1
      res=solve(buf, pos)
      buf[pos]=res
      print('currently on ', binascii.hexlify(buf))
main()

