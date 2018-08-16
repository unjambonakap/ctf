#!/usr/bin/env python

from chdrft.main import app
from chdrft.tube.connection import Connection
from chdrft.utils.misc import PatternMatcher
from chdrft.utils.cache import Cachable
import re
import time

global flags, cache
flags = None
cache = None


def args(parser):
  pass


def go1(s, pwd, win=0):
  s.send('login ' + pwd + '\n')
  if win:
    pattern=b'Login successful'
  else:
    pattern = b'what you entered: (\w{12})'
  res = s.recv_until(PatternMatcher.fromre(pattern))
  print(res)
  m = re.search(pattern, res)
  if not win:
    return int(m.group(1), 16)
  return 0


@Cachable.cachedf()
def get_data(conn):
  prev = go1(conn, 'abc')
  tmp = go1(conn, 'abc')
  print('INIT >> ', hex(tmp))
  init=tmp
  prev = tmp

  tb = []
  for i in range(6 * 8 + 1):
    cur = go1(conn, str(i))
    tb.append(cur ^ prev)
    prev = cur
  return [init, tb]



def solve(conn, init, data):
  want=(0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1, 0, 1, 1, 0, 1, 1, 0, 0, 1, 0, 0, 0, 0, 1, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 0, 1, 1, 1, 1, 0, 0, 0, 0, 1)

  got=init

  #b'\nOkay, sure! Let me grab that flag for you.\nflag{more_MATH_than_crypto_but_thats_n0t_a_CATegory}\n'


  for i in range(len(want)):
    if want[i]==0:
      continue
    got^=data[i]
    u=go1(conn, str(i), i==len(want)-1)
    print(hex(u), hex(got))
    assert u==got
  print(got)
  conn.send('getflag\n')
  time.sleep(1)
  print(conn.recv(2048))
  time.sleep(1)
  print(conn.recv(2048))


def main():
  with Connection('school.fluxfingers.net', 1513) as conn:
    data = get_data(conn)
    print(data)
    solve(conn, *data)


app()
