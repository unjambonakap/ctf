#!/usr/bin/env python

import struct
import binascii
from Crypto.Hash import MD5


class RC5:

  def __init__(self, w, R, key):
    self.w = w  # block size (32, 64 or 128 bits)
    self.R = R  # number of rounds (0 to 255)
    self.key = key  # key (0 to 2040 bits)
    # some useful constants
    self.T = 2 * (R + 1)
    self.w4 = w // 4
    self.w8 = w // 8
    self.mod = 2**self.w
    self.mask = self.mod - 1
    self.b = len(key)

    self.__keyAlign()
    self.__keyExtend()
    print([hex(x) for x in self.S])
    print([hex(x) for x in self.L])
    self.__shuffle()

  def __lshift(self, val, n):
    n %= self.w
    return ((val << n) & self.mask) | ((val & self.mask) >> (self.w - n))

  def __rshift(self, val, n):
    n %= self.w
    return ((val & self.mask) >> n) | (val << (self.w - n) & self.mask)

  def __const(self):  # constants generation
    if self.w == 16:
      return (0xB7E1, 0x9E37)  # return P, Q values
    elif self.w == 32:
      return (0xB7E15163, 0x9E3779B9)
    elif self.w == 64:
      return (0xB7E151628AED2A6B, 0x9E3779B97F4A7C15)

  def __keyAlign(self):
    if self.b == 0:  # key is empty
      self.c = 1
    elif self.b % self.w8:
      self.key += b'\x00' * (self.w8 - self.b % self.w8)  # fill key with \x00 bytes
      self.b = len(self.key)
      self.c = self.b // self.w8
    else:
      self.c = self.b // self.w8
    L = [0] * self.c
    for i in range(self.b):
      L[i // self.w8] = (L[i // self.w8] << 8) + self.key[i]
    self.L = L

  def __keyExtend(self):
    P, Q = self.__const()
    self.S = [(P + i * Q) % self.mod for i in range(self.T)]

  def __shuffle(self):
    i, j, A, B = 0, 0, 0, 0
    print(3 * max(self.c, self.T))
    for k in range(3 * max(self.c, self.T)):
      A = self.S[i] = self.__rshift((self.S[i] + A + B), 3)
      B = self.L[j] = self.__rshift((self.L[j] + A + B), A + B)
      i = (i + 1) % self.T
      j = (j + 1) % self.c

  def encryptBlock(self, data):
    A = int.from_bytes(data[:self.w8], byteorder='little')
    B = int.from_bytes(data[self.w8:], byteorder='little')
    A = (A + self.S[0]) % self.mod
    B = (B + self.S[1]) % self.mod
    for i in range(1, self.R + 1):
      A = (self.__lshift((A ^ B), B) + self.S[2 * i]) % self.mod
      B = (self.__lshift((A ^ B), A) + self.S[2 * i + 1]) % self.mod
    return (A.to_bytes(self.w8, byteorder='little') + B.to_bytes(self.w8, byteorder='little'))

  def decryptBlock(self, data):
    A = int.from_bytes(data[:self.w8], byteorder='little')
    B = int.from_bytes(data[self.w8:], byteorder='little')
    print(hex(A))
    for i in range(self.R, 0, -1):
      B = self.__lshift(B - self.S[2 * i + 1], A) ^ A
      A = self.__lshift(A - self.S[2 * i], B) ^ B
    B = (B - self.S[1]) % self.mod
    A = (A - self.S[0]) % self.mod
    return (A.to_bytes(self.w8, byteorder='little') + B.to_bytes(self.w8, byteorder='little'))

  def encryptFile(self, inpFileName, outFileName):
    with open(inpFileName, 'rb') as inp, open(outFileName, 'wb') as out:
      run = True
      while run:
        text = inp.read(self.w4)
        if not text:
          break
        if len(text) != self.w4:
          text = text.ljust(self.w4, b'\x00')
          run = False
        text = self.encryptBlock(text)
        out.write(text)

  def decryptFile(self, inpFileName, outFileName):
    with open(inpFileName, 'rb') as inp, open(outFileName, 'wb') as out:
      run = True
      while run:
        text = inp.read(self.w4)
        if not text:
          break
        if len(text) != self.w4:
          run = False
        text = self.decryptBlock(text)
        if not run:
          text = text.rstrip(b'\x00')
        out.write(text)

  def encryptBytes(self, data):
    res, run = b'', True
    while run:
      temp = data[:self.w4]
      if len(temp) != self.w4:
        data = data.ljust(self.w4, b'\x00')
        run = False
      res += self.encryptBlock(temp)
      data = data[self.w4:]
      if not data:
        break
    return res

  def decryptBytes(self, data):
    res, run = b'', True
    while run:
      temp = data[:self.w4]
      if len(temp) != self.w4:
        run = False
      res += self.decryptBlock(temp)
      data = data[self.w4:]
      if not data:
        break
    return res.rstrip(b'\x00')


def rc4_decrypt(data, key):
  S = list(range(256))
  j = 0
  out = []

  #KSA Phase
  for i in range(256):
    j = (j + S[i] + key[i % len(key)]) % 256
    S[i], S[j] = S[j], S[i]

  #PRGA Phase
  i = j = 0
  for char in data:
    i = (i + 1) % 256
    j = (j + S[i]) % 256
    S[i], S[j] = S[j], S[i]
    out.append(char ^ S[(S[i] + S[j]) % 256])
  return bytearray(out)


def proc_file(fname):
  data = open(fname, 'rb').read()
  drand = data[:0x10]
  dhash = data[0x10:0x20]
  data = data[0x20:]

  res = rc4_decrypt(data, drand)
  print(res)
  print(MD5.new(res).hexdigest())
  print(binascii.hexlify(dhash))
  open(fname+'.dec', 'wb').write(res)


def solve(data):
  proc_file('./files/res_00.out')
  proc_file('./files/res_01.out')
  proc_file('./files/res_02.out')
  proc_file('./files/res_03.out')
  proc_file('./files/res_04.out')
  proc_file('./files/res_05.out')
  proc_file('./files/res_06.out')
  #hurray rc5
  #key= b'551C2016B00B5F00'
  #print(len(key))
  #rc5 = RC5(32, 21, key)
  #print('\n\n')
  #print([hex(x) for x in rc5.S])
  #print([hex(x) for x in rc5.L])
  #buf='83562691fc37d28507a4bcef454660d7'
  #buf='7cc90ed95dc8135493bcc457ab3803b24c8406a775e6db8c938cad7129227b08'
  #data=binascii.unhexlify(buf)
  #print(data)
  #res=rc5.decryptBytes(data)
  #print(binascii.hexlify(res))


def main():

  data = None
  solve(data)


main()
