#!/usr/bin/env python

from chdrft.tube.connection import Connection
from chdrft.utils.misc import DictWithDefault, Attributize, PatternMatcher
import base64
from pprint import pprint
import binascii
import math
import os
import random
import sys
import re
import traceback as tb
from Crypto.Hash import SHA
n = 128


def cycleLen(data, place):
  seen = {}
  count = 0
  while not place in seen:
    seen[place] = 1
    count += 1
    place = data[place]
  return count


def realSign(data):
  res = 1
  for i in range(len(data)):
    res *= cycleLen(data, i)
  return res


def get_cycle(mp, i, mx):
  seen = {}
  lst = []
  while not i in seen:
    lst.append(i)
    if i >= mx:
      return (lst, 0)
    seen[i] = 1
    i = mp[i]
  return (lst, 1)


def analyse(base):

  n = 128
  data = base + [random.randint(0, 2 * n - 1) for i in range(n)]

  data = {i: data[i] for i in range(len(data))}
  idata = {v: k for k, v in data.items()}
  cnt = 0
  tot = DictWithDefault(0)
  seen = {}
  for i in range(n):
    lst, typ = get_cycle(data, i, n)
    if typ == 0:
      if not lst[-2] in seen:
        seen[lst[-2]] = 1
        tot[lst[-1]] += 1
      cnt += 1
      print(len(lst))
  tb = []
  print('####')
  for i in range(n, 2 * n):
    print(tot[i])
    if tot[i] == 0:
      tb.append(i)
  print(tb, len(tb))
  print(cnt)


class TrueOracle:

  def __init__(self, key):
    self.key = key
    self.count = 350

  def sign(self, data):
    assert self.count > 0
    self.count -= 1
    return realSign(self.key + data)


class ServerOracle:

  def __init__(self, conn):
    self.conn = conn
    self.count = 350

  def sign(self, data):
    assert self.count > 0
    self.count -= 1
    self.conn.recv_until(
        PatternMatcher.frombytes(b'Give me signiture of data\n'))
    self.conn.send('1\n')
    data = base64.b64encode(bytes(data))
    assert len(data) == 172
    self.conn.send(data)
    res = int(self.conn.recv_until(PatternMatcher.frombytes(b'\n')))

    return res

  def chall(self, ans):
    self.conn.recv_until(
        PatternMatcher.frombytes(b'Give me signiture of data\n'))
    self.conn.send('2\n')

    for i in range(0x11):
      print('GOGO on chall ', i)
      pattern = b'(.{172})\n'
      res = self.conn.recv_until(PatternMatcher.fromre(pattern), timeout=1)
      c = re.search(pattern, res).group(1)
      res = ans.sign(list(base64.b64decode(c)))
      self.conn.send('%620d' % res)

    res = self.conn.recv_fixed_size(2048, timeout=2)
    print(self.conn.buf)
    print('RES >>> ', res)


class Solver:

  def __init__(self, oracle, n):
    self.oracle = oracle
    self.n = n
    self.to_eval = []

  def prepare_evals(self, data):
    self.eval_data = data

  def ask_eval(self, pos, values):
    self.to_eval.append([pos, values])

  def do_evals(self):
    n = self.n
    self.eval_data[self.static_elem - n] = self.static_elem
    eval_val = self.oracle.sign(self.eval_data)
    res = []
    for cur in self.to_eval:
      self.eval_data[self.static_elem - n] = cur[0]
      v = self.oracle.sign(self.eval_data)
      self.eval_data[self.static_elem - n] = self.static_elem
      assert v % eval_val == 0
      tmp = v // eval_val - 1
      res.append([cur[0], tmp])
    self.to_eval = []
    return res

  def filter_walk(self, walk, can):
    data = [0] * n
    data[self.static_elem - n] = self.static_elem

    prev = walk[0]
    for i in walk:
      data[i - n] = prev
      prev = i
    base_score = self.oracle.sign(data)

    depths = Attributize(other=lambda x: set([]))
    for i in range(n - 1):
      depths[i + 1].add(walk[i])
    vals = []
    cnt = 0
    for i in range(n):
      if len(can[i]) == 1:
        cnt += 1
      data[self.static_elem - n] = i
      cur = self.oracle.sign(data)
      assert cur % base_score == 0
      v = cur // base_score - 1
      depths[v].add(i)
      vals.append(v)
    if cnt > 0:
      print('COULd SPARE ', cnt)

    for i in range(n):
      can[i].intersection_update(depths[vals[i] - 1])
      if len(can[i]) == 0:
        raise "FAIL"

  def go(self):
    n = self.n
    base_data = [n + i for i in range(n)]
    base = self.oracle.sign(base_data)

    static_elem = None
    for i in range(n):
      base_data[i] ^= 1
      cur = self.oracle.sign(base_data)
      base_data[i] ^= 1
      v = n + i
      if base * 2 == cur:
        static_elem = v
        break
    assert static_elem
    self.static_elem = static_elem
    print('static elem >> ', static_elem)

    walk = []
    for i in range(n):
      if i + n != static_elem:
        walk.append(n + i)

    can = {}
    for i in range(n):
      can[i] = set(range(2 * n))

    self.filter_walk(walk, can)
    print('go reverse')
    walk.reverse()
    self.filter_walk(walk, can)

    pprint(can)
    print(self.oracle.count)
    s = 0
    cnd = set()
    for i in can.values():
      s += len(i) - 1
      cnd.update(i)

    statics = set(range(n, 2 * n))
    statics.difference_update(cnd)
    print(statics)
    roots = []

    self.graph = can
    self.canv = Attributize(other=lambda x: set())

    toproc = Attributize(other=lambda x: [])
    for i in range(n):
      if len(can[i]) == 1: continue
      print('UNDEcideD >> ', i, can[i])
      root, depth = self.rec(i)
      toproc[root].append([i, depth])

    print(toproc)
    while True:
      data = [n + i for i in range(n)]
      cur_round = []
      to_measure = []

      for root, entries in toproc._elem.items():
        if len(entries) == 0: continue
        for entry, depth in entries:
          if len(self.graph[entry]) == 1: continue
          print(entry, self.graph[entry])

          data[root - n] = list(self.graph[entry])[0]
          to_measure.append([entry, [depth, data[root - n]]])
          break

      if len(to_measure) == 0:
        break
      self.prepare_evals(data)

      mp = {}
      for entry, data in to_measure:
        self.ask_eval(entry, [2, 3, 434])
        mp[entry] = data
      res = self.do_evals()

      for e, val in res:
        depth, target = mp[e]
        print('target .. ', e, target, self.graph[e], depth, val)
        assert target in self.graph[e]
        if val == depth + 1:
          self.graph[e] = set([target])
        else:
          self.graph[e].remove(target)

    #print('HAVE NO W>> ', self.oracle.count)
    #for k, v in self.graph.items():
    #  print(k, self.oracle.key[k], v)
    #  assert self.oracle.key[k] == list(v)[0]
    #print(self.oracle.key)
    #print(self.graph)
    return [list(self.graph[i])[0] for i in range(n)]

  def rec(self, p):
    if p >= 128:
      return p, 0
    for i in self.graph[p]:
      root, depth = self.rec(i)
      return root, depth + 1
    assert 0


def pow(conn):
  res = conn.recv_fixed_size(12)
  i = random.randint(0, 2 ** 32 - 1)
  i = 2131672237762560000
  while True:
    i += 1
    i %= 2 ** 32
    x = res + ('%08x' % i).encode()
    if i % 10000 == 0:
      print(i)

    tmp = SHA.SHA1Hash(x).digest()

    if tmp.endswith(b'\x00\x00\x00'):
      print(tmp, x)
      print('found it')
      conn.send(x)
      break
  pass


def test2():
  n = 128
  key = [random.randint(0, 2 * n - 1) for i in range(n)]
  analyse(key)
  server = 'wob-key-e1g2l93c.9447.plumbing'
  port = 9447

  while True:
    try:
      with Connection(server, port) as conn:
        if 1:
          pow(conn)
        oracle = ServerOracle(conn)
        solver = Solver(oracle, n)
        key = solver.go()

        true_oracle = TrueOracle(key)
        oracle.chall(true_oracle)
        break
    except Exception as e:
      print('failed', e)
      tb.print_exc()
      pass


def main():
  random.seed(1)
  test2()


main()
