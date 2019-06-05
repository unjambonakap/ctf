#!/usr/bin/env python

from chdrft.cmds import CmdsList
from chdrft.main import app
from chdrft.utils.cmdify import ActionHandler
from chdrft.utils.misc import Attributize
import chdrft.utils.misc as cmisc
import glog
import chdrft.utils.Z as Z
from challenge import CodeBasedEncryptionScheme

global flags, cache
flags = None
cache = None


def args(parser):
  clist = CmdsList().add(test)
  parser.add_argument('--dir', default='data')

  ActionHandler.Prepare(parser, clist.lst, global_action=1)


#111101001010101000100110111010001100010110011001

def test(ctx):
  A = CodeBasedEncryptionScheme.new()
  res = []
  for cipher in Z.glob.glob(f'./{flags.dir}/ciphertext_*'):
    plain = cipher.replace('cipher', 'plain')
    cc = open(cipher, 'rb').read()
    pc = open(plain, 'rb').read()
    rels = A.get_rels(cc, pc)
    res.extend(rels)
  print(len(res), len(res[0]))
  print('\n'.join([''.join(map(str, rel)) for rel in res]))


def solve(ctx):
  A = CodeBasedEncryptionScheme.new()
  from BitVector import BitVector
  kk = '11111000010000100010011110010101101111010010110010000100'
  kk = list(map(int, kk))
  #kk = [ 1,1,0,0,1,0,1,0,1,0,0,1,0,1,0,0,1,1,0,1,1,1,0,1,1,0,1,1,0,1,1,1,1,0,1,1,1,1,1,0,1,0,1,1,1,0,0,0]

  A.key = BitVector(bitlist=kk)
  res = b''

  lst = cmisc.get_input([f'./{flags.dir}/flag_*'])
  for fl in lst:
    cc = open(fl, 'rb').read()
    res += A.decrypt(cc)
  print(res)

#35C3_le's_hope_these_Q_computers_will_wait_until_we're_ready
def main():
  ctx = Attributize()
  ActionHandler.Run(ctx)


app()
