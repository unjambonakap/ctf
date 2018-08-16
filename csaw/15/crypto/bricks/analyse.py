import struct
from chdrft.utils.misc import Attributize
import itertools


def load_data():
  data = open('./bricks.dat', 'rb').read()
  data = data[:-19]
  iv = struct.unpack('<I', b'CASH')

  print(len(data))

  tb = []
  last = iv
  for i in range(len(data) // 4):
    x = struct.unpack('<I', data[4 * i:4 * i + 4])[0]
    tb.append(x)
  return tb


def hex2(a):
  return '%08x'%a

def rol(a, b):
  b %= 32
  res = (a << b) % 2 ** 32
  res |= a >> (32 - b)
  return res


def f1():
  tb = load_data()
  mp = Attributize(other=lambda x: [])
  for pos, a in enumerate(tb):
    mp[a].append(pos * 4)
  res = []
  for k, v in mp._elem.items():
    if len(v) > 5:
      print('GOT ', v[0])
      res.append([k, v])

  res.sort(key=lambda a: a[1][0])
  v = [a[0] for a in res]
  last = 0
  for x in res:
    print(hex2(x[0]), x[0], x[1])

  for i in range(3, len(v)):
    d = (v[i] - v[i - 1]) % (2 ** 32)
    d2 = v[i] ^ v[i - 1] ^ v[i - 2] ^ v[i-3]
    d1 = (v[i] ^ v[i - 1]) ^ (2 ** 32 - 1)
    d3 = v[i] ^ v[i - 2]
    print(hex2(v[i]), d, hex2(d), hex2(d2), hex2(d1), hex2(d3))
  #print(mp)

  start2 = res[0][1][0] // 4

  def get_bin(x):
    a = bin(x)[2:]
    a = '0' * (32 - len(a)) + a
    spacing = 2
    return ' '.join([a[i * spacing:i * spacing + spacing]
                     for i in range(32 // spacing)])

  def cnt_bit(x):
    res = 0
    for i in range(32):
      res += (x >> i) & 1
    return res

  l = []
  nx = 14
  nn = len(tb)

  tmp2 = []
  tmp2 = tb[0x2ee7b:0x2eefc]
  #tmp2 += tb[start2:start2 + 0x30]
  print(hex2(start2 * 4))

  tmp2 = [bin2vec(a, 32) for a in tmp2]

  for i in range(32):
    cnt = [0] * 32
    cnt2 = [0] * 32
    nxt = 1
    tot = len(tmp2) - nxt
    for j in range(32):
      for k in range(tot):
        dst = tmp2[k + nxt][j]
        if tmp2[k][i] == dst:
          cnt[j] += 1
    print()
    for j in range(32):
      bound = 0.9
      cnt[j]/=tot
      if cnt[j] >= bound:
        print(i, j, cnt[j])
      if cnt[j] <= 1-bound:
        print('inv', i, j, cnt2[j])

  start, end = start2, start2 + 0x20
  start, end = 0xbba10 // 4, nn - 10
  print('starting at >> ', start)
  f = b''
  pos=0
  for x in range(start, end, 1):
    a = rol(tb[x], 18)
    b = tb[x + 1]
    d1 = (a ^ b)
    d1 = a
    tmp = []
    for j in range(nx):
      tmp.append(d1 >> j & 1)
    l.append(tmp)

    d2 = tb[x] ^ tb[x + 2]
    d3 = tb[x] ^ tb[x + 10]
    uu=get_bin(rol(tb[x], 18*pos))
    pos+=1
    print(uu, hex2(tb[x]), '\t\t', hex2(d3), '\t\t d2:', hex2(d2),
          '\t\t', hex2(rol(d2, 4) ^ d3), hex2(tb[x]), hex2(x))
    f += struct.pack('>I', d2)

  return
  for perm in itertools.permutations(range(nx)):
    tb2 = []
    for e in l:
      tb2.append([e[i] for i in perm])
    print(tb2)

  print('')
  for x in tb[start:start + 0x40:2]:
    a = bin(x)[2:]
    a = '0' * (32 - len(a)) + a
    print(a)


def test2():
  tb = load_data()
  mp = Attributize(other=lambda x: [])
  for i in range(2, len(tb)):
    u = tb[i] ^ tb[i - 2]
    mp[u].append(i * 4)
  res = []
  for k, v in mp._elem.items():
    if len(v) > 5:
      print(hex2(k), len(v))


def bin2vec(a, n):
  return [(a >> i & 1) for i in range(n)]


def try_solve(lst):
  from sage.all import GF, MatrixSpace, VectorSpace, matrix
  A = []
  B = []
  NK = 32

  R = GF(2)
  for uu in lst:
    A.append(bin2vec(uu[0], NK))
    B.append(bin2vec(uu[1], NK))

  A = matrix(R, A)
  print('rank is >> ', A.rank())
  B = matrix(R, B)
  try:
    X = A.solve_right(B)
  except:
    return 0
  print(A.str())
  print()
  print(B.str())
  print()
  print(X)
  print()
  print((A * X - B).str())
  print()
  return 1


def go_sage():
  from sage.all import GF, MatrixSpace, VectorSpace
  x = load_data()
  start = 190934 + 0x40
  tmp = x[start:start + 0x20]

  start = 0xbba10 // 4 + 0x30
  print(hex2(start * 4))
  tmp2 = x[0x2ee9b:0x2eefc]
  print('\n'.join([hex2(a) for a in tmp2]))
  for v in range(10000):
    print('\nGOGO ', v)
    y = []
    for i in range(0, len(tmp2) - 1, 5):
      y.append([tmp2[i] ^ v, tmp2[i + 1]])
    print('\n'.join([hex2(a[0]) for a in y]))
    return

    if try_solve(y):
      return


if __name__ == '__main__':
  go_sage()
