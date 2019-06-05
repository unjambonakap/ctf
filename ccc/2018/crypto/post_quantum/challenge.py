#!/usr/bin/python3

from BitVector import BitVector
from random import SystemRandom

if 1:
  P = 3
  Q = 7
  BL = Q * 8
else:
  P = 1
  Q = 3
  BL = Q * 16


def matrix_vector_multiply(columns, vector):
  cols = len(columns)
  assert (cols == len(vector))
  rows = len(columns[0])
  result = BitVector(size=rows)
  for i, bit in zip(range(cols), vector):
    assert (len(columns[i]) == rows)
    if bit == 1:
      result = result ^ columns[i]
  return result


def bitvector_to_bytes(bitvector):
  return bitvector.int_val().to_bytes(len(bitvector) // 8, 'big')


def bitvector_from_bytes(bytes):
  return BitVector(size=len(bytes) * 8, intVal=int.from_bytes(bytes, 'big'))


class CodeBasedEncryptionScheme(object):

  @classmethod
  def new(cls, bitlength=BL):
    key = cls.keygen(bitlength)
    return cls(key)

  def __init__(self, key):
    self.key = key
    self.key_length = len(self.key)
    self.random = SystemRandom()

  @classmethod
  def keygen(cls, bitlength):
    key = SystemRandom().getrandbits(bitlength)
    key = BitVector(size=bitlength, intVal=key)
    return key

  def add_encoding(self, message):
    message = int.from_bytes(message, 'big')
    message = BitVector(size=self.key_length // Q, intVal=message)
    out = BitVector(size=self.key_length)
    for i, b in enumerate(message):
      for j in range(Q): out[i * Q + j] = b
    return out

  def decode(self, message):
    out = BitVector(size=self.key_length // Q)
    for i in range(self.key_length // Q):
      s = 0
      for j in range(Q):
        s += message[i * Q + j] == 1
      if s > Q / 2:
        decoded_bit = 1
      else:
        decoded_bit = 0
      out[i] = decoded_bit
    return bitvector_to_bytes(out)

  def encrypt(self, message):

    message = self.add_encoding(message)

    columns = [
        BitVector(size=self.key_length, intVal=self.random.getrandbits(self.key_length))
        for _ in range(self.key_length)
    ]

    # compute the noiseless mask
    y = matrix_vector_multiply(columns, self.key)

    # mask the message
    y ^= message

    # add noise: make a third of all equations false
    for i in range(self.key_length // Q):
      cnds = list(range(Q))
      for j in range(P):
        e = self.random.choice(cnds)
        cnds.remove(e)
      #noise_index = self.random.randrange(inverse_error_probability)
        y[i * Q + e] ^= 1

    columns = [bitvector_to_bytes(c) for c in columns]
    columns = b"".join(columns)

    return columns + bitvector_to_bytes(y)

  def decrypt(self, ciphertext):

    y = ciphertext[-self.key_length // 8:]
    columns = ciphertext[:-self.key_length // 8]
    columns = [
        bitvector_from_bytes(columns[i:i + self.key_length // 8])
        for i in range(0, len(columns), self.key_length // 8)
    ]
    y = bitvector_from_bytes(y)

    y ^= matrix_vector_multiply(columns, self.key)
    result = self.decode(y)
    return result

  def get_rels(self, ciphertext, plain):

    y = ciphertext[-self.key_length // 8:]
    columns = ciphertext[:-self.key_length // 8]
    columns = [
        bitvector_from_bytes(columns[i:i + self.key_length // 8])
        for i in range(0, len(columns), self.key_length // 8)
    ]
    y = bitvector_from_bytes(y)
    y ^= self.add_encoding(plain)
    res = []
    N = BL
    if 0:
      key = [
          1, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 1, 0, 0, 1, 1, 1, 1, 0, 0, 0, 1, 0, 1, 1, 0, 0, 1, 1, 0,
          0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 1, 1, 0, 1
      ]
    else:
      key = self.key

    cnt = 0
    for i in range(BL):
      tmp = []
      v = 0

      for j in range(BL):
        u = columns[j][i]
        v ^= u & key[j]
        tmp.append(u)
      cnt += v == y[i]
      tmp.append(y[i])
      res.append(tmp)
    #assert cnt == 32, cnt
    return res
