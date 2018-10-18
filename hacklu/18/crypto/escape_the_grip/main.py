#!/usr/bin/env python
# use --local flag to test locally
# $ python main.py --actions=test --data-file=./data.pickle  # Do all the queries
# $ python main.py --actions=solve --data-file=./data.pickle  # Compute the flag


from chdrft.cmds import CmdsList
from chdrft.main import app
from chdrft.utils.cmdify import ActionHandler
from chdrft.utils.misc import Attributize
import chdrft.utils.misc as cmisc
import glog
from  matrix import matrix as M
import keystream
from math import floor, factorial
from chdrft.tube.connection import Connection
import re
import data
import pickle

global flags, cache
flags = None
cache = None

n = 5
nf = factorial(keystream.n)
n1f = factorial(keystream.n-1)
nr = keystream.rounds

def args(parser):
  clist = CmdsList().add(test).add(solve)
  parser.add_argument('--data-file', default='./data.pickle')
  parser.add_argument('--local', action='store_true')
  ActionHandler.Prepare(parser, clist.lst)


class Solver:
  def __init__(self, conn):
    if flags.local:
      self.chall = keystream.generate_challenge()
    else:
      self.conn = conn
      data = self.conn.recv_until('Round number').decode()
      mx = re.search('Challenge: 0x(\\w+)', data)
      self.chall = int(mx.group(1), 16)
      conn.recv_until('Request key stream')

  def query(self, x):
    if flags.local:
      return keystream.generate_keystream_block(x)
    res = self.conn.send_and_expect(str(x)+'\n', 'Request key stream').decode()
    mx = re.search('> 0x(\\w+)', res)
    return int(mx.group(1), 16)


  def query_last(self, i):
    x = permv(i)
    v0=nf ** (nr)
    vbase = -keystream.offset % nf
    v = vbase + v0 * x
    res =  self.query(v)
    print('on query ', i, hex(res))
    return res


def permv(x):
  return factorial(keystream.n-x)

def test(ctx):

  if 0:
    x = permv(1)
    v0=nf ** (nr)
    vbase = -keystream.offset % nf
    v = vbase + v0 * x
    #print(keystream.rasta_standard(keystream.key, keystream.rounds, keystream.n, v0, M))
    print(keystream.rasta_standard(keystream.key, keystream.rounds, keystream.n, v, M))

    return


  with Connection('arcade.fluxfingers.net', 1820) as conn:
    s = Solver(conn)

    reslist =[s.query_last(i) for i in range(keystream.n)]
    data = cmisc.Attributize()
    data.reslist = reslist
    data.chall = s.chall
    pickle.dump(data, open(flags.data_file, 'wb'))


def solve(ctx):
  for guess in range(0, 2):
    tb = [guess]
    data = pickle.load(open(flags.data_file, 'rb'))

    for i in range(1, keystream.n):
      for j in range(keystream.n):
        if M[j][i] != M[j][i-1]: break
      else:
        assert 0
      eq = (data.reslist[i] != data.reslist[0])
      tb.append(eq ^ tb[i-1])

    final_state = keystream.matrix_mul(tb, M, keystream.n)
    final_state = keystream.list_to_num(final_state)

    key_guess = final_state^data.reslist[0]
    if isinstance(data.chall, str):
      data.chall = int(data.chall[2:], 16)

    print(hex(data.chall), 'CHALL')
    print(hex(keystream.list_to_num(keystream.key)), 'KEY')
    print(hex(key_guess), 'GUESSED KEY')
    print(hex(final_state), 'GUESSED STATE')
    print(hex(data.chall ^ key_guess), 'FLAG GUESS')

    va=  key_guess ^ data.chall
    print(va.to_bytes(100, 'big'))




#flag{__xXx_Rasta_best_cipher_in_the_world_xXx__}



def main():
  ctx = Attributize()
  ActionHandler.Run(ctx)


app()
