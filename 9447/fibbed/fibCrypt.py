import random
import os
import math
from gmpy2 import is_prime
import binascii


def genPrime(numBytes):
  while True:
    rand = int(os.urandom(numBytes).encode('hex'), 16)
    if is_prime(rand):
      return rand


def mult(m1, m2, p):
  r = [[0, 0], [0, 0]]
  for i in range(2):
    for j in range(2):
      t = 0
      for k in range(2):
        t += m1[i][k] * m2[k][j]
      r[i][j] = t % p
  return r


def calcM(p, l, base):
  if l == 0:
    return [[base[1], base[0]], [base[0], base[1]]]
  x1 = [[base[0], base[1]], [base[1], (base[0] + base[1]) % p]]
  x2 = mult(x1, x1, p)
  for i in bin(l)[3:]:
    if i == '1':
      x1 = mult(x1, x2, p)
      x2 = mult(x2, x2, p)
    else:
      x2 = mult(x1, x2, p)
      x1 = mult(x1, x1, p)
  return x1


def genKey(p):
  numBytes = int(math.ceil(math.log(p, 256)))
  exp = int(os.urandom(numBytes).encode('hex'), 16) % p
  r = calcM(p, exp, (0, 1))
  return (r, exp)


prime=981725946171163877
pos=0xb3f467a7ce66e68+(1)
a1=453665378628814896
a2=152333692332446539
res=calcM(prime, pos, (a1,a2))
data="59719af4dbb78be07d0398711c0607916dd59bfa57b297cd220b9d2d7d217f278db6adca88c9802098ba704a18cce7dd0124f8ce492b39b64ced0843862ac2a6"
from Crypto.Cipher import AES
import binascii
import hashlib
import fibCrypt

IV = "0123456789ABCDEF"


def decrypt(text, passphrase):
  key = hashlib.sha256(passphrase).digest()
  aes = AES.new(key, AES.MODE_CBC, IV)
  return aes.decrypt(binascii.unhexlify(text))
print(res)
print(len(data))
print(decrypt(data, str(res)))
