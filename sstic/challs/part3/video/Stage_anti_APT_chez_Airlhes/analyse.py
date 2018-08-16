#!/usr/bin/env python

#screw you vim
import binascii


def main():
  obs = 'cyan purple cyan purple blue purple red blue black red blue cyan white yellow blue red black purple white green yellow black red yellow cyan white black cyan black green white yellow blue yellow blue purple blue purple black white blue cyan blue green blue white blue white red white green cyan red yellow cyan green blue red green cyan red yellow purple white green purple cyan yellow white black red cyan white black cyan black blue red white purple black green red purple'
  #obs='green black red purple black blue purple black green white red blue cyan'

  color_map = dict(black=0,
                   white=0xffffff,
                   red=0x0000ff,
                   green=0x00ff00,
                   blue=0xff0000,
                   cyan=0xffff00,
                   purple=0xff00ff,
                   yellow=0x00ffff)
  color_map = dict(black=0,
                   white=0xffffff,
                   red=0xff0000,
                   green=0x00ff00,
                   blue=0x0000ff,
                   cyan=0x00ffff,
                   purple=0xff00ff,
                   yellow=0xffff00)
  obs = [color_map[x] for x in obs.split(' ')]
  st = 0

  color_list = [0x4F488EB3, 0x4FB771B3, 0x4F4871B3, 0x4FB78E4C, 0x4F488E4C, 0x4FB7714C, 0x4F48714C,
                0x4FB78EB3]
  color_list = [x ^ 0x4FB78EB3 for x in color_list]
  color_map = {a: i for i, a in enumerate(color_list)}

  xorpad = binascii.unhexlify(
      '2830A43F6D280423362A32DCAD0BA04BE8201F64840AF4C4C78A8DC0A2C44019A143823814FD6C90E07E2A40DFD3F23E7238C4964D987C16')

  def get_hash(x):
    return ' '.join([str(int(a)) for a in x])

  mp = {}
  def get_svals(v):
    tb = []
    for j in range(3):
      tb.append(v % 7 + 1)
      v = v // 7 + 1
    return tb

  def get_smask(v):
    tb = []
    for j in range(3):
      tb.append(v % 7 + 1)
      v = v // 7
    return tb

  def do_xor(x, y):
    return [a ^ b for a, b in zip(x, y)]

  def get_cols(x):
    return [color_list[a] for a in x]


  # inititial data, hardcoded
  last = [6, 6]
  testv = obs
  print([hex(x) for x in testv[:10]])
  res = []
  for i in range(0, len(testv), 3):
    cnd = None
    for v in range(256):
      a = get_svals(v)
      b = get_smask(v)
      nlast = list(last)
      tvals = []
      tmask = []
      for j in range(3):
        nlast[0] += a[j]
        nlast[1] += b[j]
        nlast[0] %= 8
        nlast[1] %= 8
        tvals.append(nlast[0])
        tmask.append(nlast[1])

      # compute colors observed if we were to send this data
      tvals = get_cols(tvals)
      tmask = get_cols(tmask)
      exp_mask = testv[i:i + 3]
      exp_vals = testv[i:i + 3]
      # check if this is what we observed
      if tmask == exp_vals and (1 or tmask == exp_mask):
        # 1 or -_-
        assert cnd is None, 'More than one candidate, bad'
        cnd = v, nlast
    assert cnd is not None, str(i)
    v, last = cnd
    # undo xorpad
    v2 = xorpad[i // 3] ^ v
    res.append(v2)

    print('for ', i, hex(v2), hex(v))
  res = bytes(res)
  open('/tmp/res.out', 'wb').write(res[4:])
  print(binascii.hexlify(res))
  #1800000078da0b1634172bdac558f9cb6e6257f3be7b5b003250077e


main()
