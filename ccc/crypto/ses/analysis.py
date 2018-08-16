#!/usr/bin/env python

from chdrft.cmds import CmdsList
from chdrft.main import app
from chdrft.utils.cmdify import ActionHandler
from chdrft.utils.misc import Attributize
import chdrft.utils.misc as cmisc
import glog
import binascii
from chdrft.utils.swig import swig


global flags, cache
flags = None
cache = None


def args(parser):
  clist = CmdsList().add(test)
  ActionHandler.Prepare(parser, clist.lst)


def test(ctx):
  sbox = binascii.a2b_hex(
      'c61963bc974832ed64bbc11e35ea904f99463ce3c8176db23be49e416ab5cf10'
      '78a7dd0229f68c53da057fa08b542ef127f8825d76a9d30c855a20ffd40b71ae'
      'a17e04dbf02f558a03dca679528df728fe215b84af700ad55c83f9260dd2a877'
      '1fc0ba654e91eb34bd6218c7ec334996409fe53a11ceb46be23d4798b36c16c9'
      '08d7ad725986fc23aa750fd0fb245e815788f22d06d9a37cf52a508fa47b01de'
      'b66913cce738429d14cbb16e459ae03fe9364c93b8671dc24b94ee311ac5bf60'
      '6fb0ca153ee19b44cd1268b79c4339e630ef954a61bec41b924d37e8c31c66b9'
      'd10e74ab805f25fa73acd60922fd87588e512bf4df007aa52cf389567da2d807'
  )

  la = swig.opa_crypto_linear_cryptanalysis_swig
  sx = la.SboxDesc()
  sx.init(8, sbox)
  blk = la.SboxBlock()
  blk.init(sx)
  print(blk.fast_eval1(1))
  print(blk.fast_eval1(0))
  rels = blk.get_relations()
  print(rels.str().decode())
  return
  


  for i in range(256):
    if i == sbox[i]: print(i)
    if 255 ^ i == sbox[i]: print(i)



def main():
  ctx = Attributize()
  ActionHandler.Run(ctx)


app()
