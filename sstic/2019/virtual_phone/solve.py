#!/usr/bin/env python

from chdrft.cmds import CmdsList
from chdrft.main import app
from chdrft.utils.cmdify import ActionHandler
from chdrft.utils.misc import Attributize
import chdrft.utils.misc as cmisc
import glog
import chdrft.utils.Z as Z
from chdrft.display.ui import GraphHelper
import numpy as np
import Crypto.Cipher.AES as AES
import z3

global flags, cache
flags = None
cache = None


def args(parser):
  clist = CmdsList().add(test).add(display)
  ActionHandler.Prepare(parser, clist.lst, global_action=1)


a = Z.np.load('./power/arr_0.npy')
tlow = a[826300:827300]
thigh = a[980650:981600]
c1 = Z.dsp_utils.compute_normed_correl(a, tlow)
tc1 = np.argwhere(c1 > 20).ravel()
c2 = Z.dsp_utils.compute_normed_correl(a, thigh)
tc2 = np.argwhere(c2 > 20).ravel()


def display(ctx):
  g = GraphHelper(run_in_jupyter=0)
  global a

  if 0:
    x = g.create_plot()
    x.add_plot(a)
    g.run()
    return
  x = g.create_plot()
  x.add_plot(tlow + 1)
  x.add_plot(thigh)
  x = g.create_plot()
  #correl = Z.signal.correlate(shift_seq, self.pulse_shape, mode='valid')
  c1 = Z.dsp_utils.compute_normed_correl(a, tlow)
  c2 = Z.dsp_utils.compute_normed_correl(a, thigh)
  c1 = c1 / np.max(c1)
  c2 = c2 / np.max(c2)
  a = a / np.max(a)
  x.add_plot(a)
  x.add_plot(c1 + 2)
  x.add_plot(c2 + 2)
  g.run()


def test(ctx):
  _, bits = extract_data()
  print(len(bits))

  bits = np.array(bits)
  for i in range(2):
    print(bytes(Z.Format(bits).bin2byte(lsb=0).v))
    print(bytes(Z.Format(bits).bin2byte(lsb=1).v))
    bits = 1 - bits


@Z.Cachable.cachedf(fileless=0)
def extract_data():
  d1 = []
  d2 = []
  global tc2
  global tc1
  for x in tc1:
    d1.append((x, (c1[x], 0)))

  for x in tc2:
    d2.append((x, (c2[x], 1)))

  Z.pprint(d1)
  Z.pprint(d2)
  lst = set(list(tc1))
  lst.update(list(tc2))
  lst = list(lst)
  lst.sort()
  interlist = Z.Intervals.FromIndices(lst, merge_dist=100)
  print(interlist)

  r = interlist.group_by(d1)
  r = interlist.group_by(d2, r)

  data = []
  for k, v in sorted(r.items()):
    bx = max(v)
    data.append((int(k.mid), bx[1]))

  poslist, bits = list(zip(*data))
  return poslist, bits


def try_dec1(key):
  a = Z.binascii.a2b_hex('D072DD3F639C2D0E1FF69AB965782F668D7BFFAC766AEEAB5DA84AE373F8C0DC')
  b = Z.binascii.a2b_hex('c5a87bbe1d229bdb2b672811598f30f50dc78e6be85308dc876f752d9bd21e2f')

  aes = AES.new(key, AES.MODE_ECB)
  for func in (aes.decrypt, aes.encrypt):
    for plain, cipher in ((a, b), (b, a)):
      res = func(plain)
      if res == cipher:
        print('FOUND FOR ', func, plain, cipher, key)
        return 1
  return True


def try_find_key(ctx):
  _, bits = extract_data()

  bits = np.array(bits)
  cnds = []
  for i in range(2):
    cnds.append(bytes(Z.Format(bits).bin2byte(lsb=0).v))
    cnds.append(bytes(Z.Format(bits).bin2byte(lsb=1).v))
    bits = 1 - bits

  # 23d87cdf97bb95abe6273c384190c765f552ab86f6de30a8db74435c95e6e3138f54af689812d8f9359cf0f4d453a0c11ec68ce470216c09e74c8947adaf23e902415d61ddf2c0ffe459cbb40f7de42bdb7cd14093100a570e8c29819765e2d8d276f86471b52ac29aa2ce2bb72cd45006279e82bec253ae9675fe45824f6001

  for cnd in list(cnds):
    cnds.append(cnd[::-1])

  for cnd in cnds:
    print(Z.binascii.hexlify(cnd).decode())
    #print(try_dec1(cnd))


class SD:

  def __init__(self):
    self.bb = None
    self.iter = self.notify_input_iter()
    self.seq = [0xf, 0]
    self.pos = 0

  def notify_input_iter(self):
    while True:
      res = self.seq[self.pos]
      yield res
      self.pos += 1

  def notify_input(self):
    self.bb = next(self.iter)

  def secure_device(self, a, b, op):
    BB = Z.Format(self.bb).bitlist(size=4).v
    al = Z.Format(a).bitlist(size=8).v
    bl = Z.Format(b).bitlist(size=8).v
    opl = Z.Format(op).bitlist(size=2).v

    def g(a, b, c):
      # selector
      return (a and (not c)) or (b and c)

    def prepare(l, kx):
      res = [0] * 8
      for i in range(8):
        res[i] = g(l[i], l[i + 7 & 7], kx)
      return res

    def f(x, y, k1, k2, u):

      out_u = (u and (x ^ y)) or (x and y)
      t1 = g(x ^ y, x ^ y ^ u, k1)
      t2 = g(x and y, x or y, k1)
      out = g(t2, t1, k2)
      return out_u, out

    xl = prepare(al, BB[2])
    yl = prepare(bl, BB[3])

    k1 = g(BB[0], not BB[0], opl[0])
    k2 = g(BB[1], not BB[1], opl[1])
    res = [0] * 8
    u = 0

    for i in range(8):
      u, res[i] = f(xl[i], yl[i], k1, k2, u)
    return Z.Format(res).bit2num().v


def test_secure_device(ctx):
  sd = SD()
  sd.notify_input()
  print(sd.secure_device(0, 0, 0))


def solve_step2(ctx):
  from step2 import get_safe1_key
  tb = []
  for i in range(8):
    sd = get_safe1_key.sd
    tx = []
    for j in range(16):
      sd.bb = j
      res = getattr(get_safe1_key, f'step{i+1}')()
      tx.append(res)
      print(res)
    tb.append(tx)
  Z.pickle.dump(tb, open('./step2.bytes_cnd.pickle', 'wb'))


def step2_find_key(ctx):
  tb = Z.pickle.load(open('./step2.bytes_cnd.pickle', 'rb'))

  from chdrft.utils.swig import swig
  c = swig.opa_crypto_swig
  cracker = c.Cracker.createJob()
  crackerp = c.CrackerParams()
  kl = 8

  target_hash = Z.binascii.a2b_hex(
      '00c8bb35d44dcbb2712a11799d8e1316045d64404f337f4ff653c27607f436ea'
  )
  a = c.PatternChecker_getCl()
  x = c.PatternCheckerParams()
  x.from_string(0, target_hash)
  a.set_params(x)
  b = c.Sha256_getCl()

  mc = c.MapperAndChecker_getCl()
  mcp = c.MapperAndCheckerParams()
  mcp.mapper = b
  mcp.checker = a
  mc.set_params(mcp)

  pattern = c.Pattern()
  pattern.init = b'0' * 8
  pattern.shard_at = 2
  pattern.mp = c.vi([i for i in range(kl)])
  for i in range(kl):
    print(len(tb[i]))
    pattern.per_char_vals.push_back(c.vi(tb[i]))
  tmp = c.PatternVector()
  tmp.push_back(pattern)
  crackerp.patterns = tmp
  crackerp.checker = mc
  crackerp.n_res = 1
  cracker.init(crackerp)

  runner = swig.opa_threading_swig.Runner()
  runner.run_cmd()
  dispatcher = runner.dispatcher()
  dispatcher.process_job(cracker.get_job())

  res = cracker.res().tb
  for v in res:
    print('Result >> ', v)
    import hashlib
    print(hashlib.sha256(v.encode()).digest())


def step2_get_aes_key(ctx):
  key = Z.binascii.a2b_hex(b'8fa4dfa9d4edbbf0')
  import hashlib
  aes_key = hashlib.scrypt(
      key, salt=b"sup3r_s3cur3_k3y_d3r1v4t10n_s4lt", n=1 << 0xd, r=1 << 3, p=1 << 1, dklen=32
  )
  print(aes_key.hex())
  print(f'/root/tools/add_key.py {aes_key.hex()}')


def main():
  ctx = Attributize()
  ActionHandler.Run(ctx)


app()
