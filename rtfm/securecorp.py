#!/usr/bin/env python
#VqYSn6/eOfYcNSOcE7uqXkd13gDcFEhF2myE6+dqYS6mR/SZzEKZia/aAaUezOUFtuCAEC771b8jcau8gFa2M4MYztDYwPGOcvZpdei2mF4=

from chdrft.cmds import CmdsList
from chdrft.main import app
from chdrft.utils.cmdify import ActionHandler
from chdrft.utils.misc import Attributize
import chdrft.utils.misc as cmisc
import glog
from chdrft.tube.connection import Connection
import re
import numpy as np
from chdrft.utils.misc import PatternMatcher
import base64
import binascii
from Crypto.Cipher import AES
from chdrft.utils.fmt import Format

global flags, cache
flags = None
cache = None


def args(parser):
  clist = CmdsList().add(test)
  ActionHandler.Prepare(parser, clist.lst)


def encode(j):
  return (j // 3, j % 3)


class PaddingOracle:

  def __init__(self, q):
    self.q = q
    self.n = 16
    self.decode_db = {}

  def decode(self, blk):
    n = self.n
    blk = bytes(blk)
    if blk in self.decode_db:
      return self.decode_db[blk]

    msg = bytearray([0] * n)
    msg.extend(blk)

    for i in range(n):
      for j in range(i):
        msg[n - 1 - j] ^= i + 1
      for v in range(256):
        msg[n - 1 - i] = v
        if self.q(msg):
          if i == 0:
            msg[n - 2] = 1
            if not self.q(msg): continue
            # bad luck where the aes dec^msg[n-1] is a valid padding of size > 1
          break
      else:
        assert 0
      for j in range(i + 1):
        msg[n - 1 - j] ^= i + 1
    res = msg[:n]
    res = bytes(res)

    self.decode_db[blk] = res
    return res

  def recover_msg(self, msg):
    buckets = Format(msg).bucket(self.n).v
    res = []
    for i in range(1, len(buckets)):
      dec = cmisc.xorlist(buckets[i - 1], self.decode(buckets[i]))
      res.append(dec)
    return b''.join(res)

  def pad(self, m):
    c = self.n - len(m) % self.n
    return m + bytes([c] * c)

  def encode(self, m):
    m = self.pad(m)
    buckets = Format(m).bucket(self.n).v
    res = bytearray([0] * (len(m) + self.n))

    if self.decode_db:
      cur = next(self.decode_db.keys())
    else:
      cur = b'a' * self.n

    res[-self.n:] = cur

    for i in reversed(range(len(buckets))):
      dec = self.decode(cur)
      cur = cmisc.xorlist(dec, buckets[i])
      res[i * self.n:(i + 1) * self.n] = cur
    return res


def step1(conn):
  res = [encode(0) for i in range(5)]
  for i in range(5):
    reslist = []
    for j in reversed(range(12)):
      pos = encode(j)
      res[i] = pos
      if pos[0] == 3 and pos[1] != 1: continue
      msg = '|'.join([f'{x},{y}' for x, y in res])

      matcher = PatternMatcher.fromre(b'(SECONDS)|(GIVE ME A ROOM CODE)')
      mx = conn.send_and_expect(msg, matcher).decode()
      try:
        xx = re.search('IN ONLY ([\w.]+)', mx).group(1)
        time = float(xx)
        print('TIIIMIE ', time, xx)
        reslist.append((time, pos))
      except:
        print('FUU ', mx)
        sx = 'YOU THIS TOKEN:\n>>> '
        rem = mx[mx.find(sx) + len(sx):]
        token = rem[:rem.find('\n')]
        print('TOKEN IS ', token)
        roomnum = re.findall('\|    (\S+)', rem)
        print('ROOM ', roomnum)
        roomnum.append('ADMIN')
        roomnum.append('GUEST')
        roomnum.append('DEBUG')
        #roomnum.append('/x#@-')
        #roomnum.append('[:$*;')
        #roomnum.append('/x#@-[:$*;')
        for i in range(110):
          roomnum.append(base64.b64encode(str(i).encode()).decode())
        conn.recv_until('AND YOUR TOKEN')
        return token, roomnum
    print('BEST ', res[i])
    res[i] = max(reslist)[1]
    #15nWb83h5WtH5RlL+Bw3XktAhQ+xMjj8C9ZbEJ2P+g2ZRw9gnvA6N+HkryyDCPFxvgzNxa0ST2Frg8CTkJMV8OjeLJauytWd3zEeHi8jfXTCM=


def doit():
  with Connection('localhost', 4445) as conn:

    token, roomnum = step1(conn)

    conn.recv_until('AND YOUR TOKEN')

    def query(rn, data):
      tt = base64.b64encode(data).decode()
      tmp = conn.send_and_expect(f'{rn}|{tt}\n', 'AND YOUR TOKEN')
      return tmp.find(b'ACCESS GRANTED') != -1, tmp

    tbin0 = bytearray(base64.b64decode(token))

    debug_room = None
    for rn in roomnum:
      print('QUERY ROOM ', rn)
      _, res = query(rn, tbin0)
      if res.find(b'WELCOME TO ROOM "DEBUG"') != -1:
        debug_room = rn
        break
    print('DEBUG ROMO ">> ', debug_room)

    def q_padding(data):
      _, tmp = query(debug_room, data)
      return tmp.find(b'Invalid padding') == -1

    oracle = PaddingOracle(q_padding)
    print(len(tbin0))
    #res = oracle.recover_msg(tbin0)
    print(res)

    admin_token = b'{"guid": "dc5928bd15b87de8b3335f67e6712444", "level": "ADMIN"}'
    enc_token = oracle.encode(admin_token)
    print(query(roomnum[0], enc_token))

    return


def test(ctx):
  doit()


def main():
  ctx = Attributize()
  ActionHandler.Run(ctx)


app()
