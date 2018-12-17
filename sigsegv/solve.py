#!/usr/bin/env python

from chdrft.cmds import CmdsList
from chdrft.main import app
from chdrft.utils.cmdify import ActionHandler
from chdrft.utils.misc import Attributize
import chdrft.utils.misc as cmisc
import glog
import numpy as np
import requests
import hashlib

global flags, cache
flags = None
cache = None


def args(parser):
  clist = CmdsList().add(test).add(s1).add(s2).add(s0)
  ActionHandler.Prepare(parser, clist.lst)


def test(ctx):
  print('on test')

def s1(ctx):
  import chdrft.utils.misc as cmisc
  import chdrft.crypto.common as ccrypto
  content = b'\x4f\x01\x13\x1e\x09\x59\x34\x09\x0b\x05\x26\x53\x31\x41\x5a\x18\x0e\x53\x1d\x15\x1c\x10\x11\x13\x5b\x06\x16\x69\x15\x29\x55\x1d\x55\x5d\x06\x1d\x0e\x1f\x0c\x14\x13\x5b\x06\x16\x69\x1e\x2a\x40\x5a\x1d\x18\x53\x19\x06\x00\x16\x02\x56\x0a\x1f\x16\x69\x07\x30\x14\x1b\x0a\x5d\x07\x1b\x08\x06\x13\x02\x56\x0b\x05\x06\x3b\x53\x33\x55\x16\x10\x19\x16\x1b\x47\x1f\x00\x47\x15\x13\x0b\x1f\x25\x16\x2b\x53\x1f\x45\x52\x1b\x1d\x0a\x1f\x5b'
  print(content)

  solver = ccrypto.VigenereSolver(content)
  #for i in range(2, 30):
  #  print(i, np.mean(solver.get_n_guess_score(i)))


  tlen = 17
  key = []
  pwd = bytearray(b'a'*17)
  target = b'sigsegv{'
  pwd[:len(target)] = target
  known = {}
  for i, c in enumerate(target):
    known[i] = c
  n = len(content)
  pwd[16] = ord('}')

  x = ccrypto.XorpadSolver([content], pwd)
  x.solve()
#sigsegv{jsIsE4zy}
  print(x.pad)
  #known[(len(content)-1)%17] = content[-1] ^ ord('}')
  #print(len(content)%17)
  #known = {}

  for grpid in range(tlen):
    grp = solver.get_group(grpid, tlen)
    if grpid in known:
      key.append(known[grpid])
      print(bytes(ccrypto.xor(grp, key[-1])))
    else:
      res = solver.solve_single_pad(grp)

      tmp = cmisc.asq_query(res).where(lambda x: x[0].nbad == 0).to_list()
      print('\n\n\n', grpid, len(tmp))
      cnds = []
      cnt = 0
      for sc, i in tmp:
        if not ccrypto.isgoodchar(i): continue
        cnt += 1
        cnd = bytes(ccrypto.xor(grp, i))
        ix = ccrypto.get_incidence_freq(cnd)
        cnds.append((-sc.score, i))
      print(cnt)
      key.append(max(cnds)[1])
      print(bytes(ccrypto.xor(grp, key[-1])))
  print('KEY >> ', bytes(key))
  print(bytes(ccrypto.xorpad(content, key)))


def s2(ctx):
  #sigsegv{W3llPl4y3d}
  a='736967736567767b57336c6c506c347933647d'
  import binascii
  print(binascii.unhexlify(a))


def s0(ctx):

  #r = requests.request('AUTREiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiii', 'http://51.158.73.218:8880/.htaccess',)
  #print(r.content)
  def checkit(a):
    a = a.encode()
    n = len(a)
    for i in range(n):
      if a[i] != ord('0'): break
    if i == 0: return 0
    if a[i] != ord('e'):
      return 0
    for j in range(i+1, n):
      if a[j] > 90: return 0
    return 1


  assert checkit('0e123418218')
  assert checkit('000e123418218')
  assert not checkit('000e1234182a8')
  assert not checkit('100e1234182a8')

  for i in range(2**35):
    x = 'a141632028'+'Shrewk'
    r = hashlib.md5(x.encode()).hexdigest()
    print(checkit(r))
    print(r)
    break
    if checkit(r):
      print('PASS  = ', i)
      break

#ȃǹǷȃǵǷȆȋǜǑǣǤǕǗǑǓǕǣǤǠǑǣǣǙǖǑǓǙǜǕȍ
#sigsegv{lAsTEGACEsTPAssIfACIlE}
#sigsegv{LAstEGACEstpAssIFACILE}
#sigsegv{LaStegaCEstPasSiFACILE}

def main():
  ctx = Attributize()
  ActionHandler.Run(ctx)


app()
