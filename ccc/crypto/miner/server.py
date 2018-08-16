#!/usr/bin/env python

from chdrft.cmds import CmdsList
from chdrft.main import app
from chdrft.utils.cmdify import ActionHandler
from chdrft.utils.misc import Attributize
import chdrft.utils.misc as cmisc
import glog
from protocol import RatchetProtocol
import protocol
from miner import SignatureScheme
from pickle import load, dump
import random
import os
import sys
from chdrft.tube.connection import Connection, Server
import traceback as tb
import gmpy2
import numpy as np
import json

#this is a reresentative sample of text messages exchanged via messaging apps:
messages = [
    'Hi',
    'haha',
    'lol',
    'rofl',
    ':)',
    ':-)',
    ':D',
    #'FreeDeniz', # removed, because it's Twitter (and not an IM App)
]



def get_random_message():
  v = random.random()
  if v < 0.75:
    return random.choice(messages)
  elif v < 0.99:
    return 'https://xkcd.com/' + str(random.randint(1, 1933))
  else:
    return 'https://www.youtube.com/user/thejuicemedia'


global flags, cache
flags = None
cache = None

other = dict(alice='bob', bob='alice')
REQ_FLAG = 'Would you send me the flag, please?'


def args(parser):
  clist = CmdsList().add(server).add(gen_key).add(client).add(hack_client)
  ActionHandler.Prepare(parser, clist.lst)
  parser.add_argument('--init', action='store_true')
  parser.add_argument('--who', type=str, default='alice')
  parser.add_argument('--host', default='localhost')
  parser.add_argument('--port', default=1234, type=int)


def gen_key(ctx):
  sx = SignatureScheme.new()
  dump(sx.sk, open(f'./private-data/{ctx.who}.key', 'wb'))
  dump(sx.pk, open(f'./public-data/{ctx.who}.key', 'wb'))
  r = make_ratchet(sx, None)
  r._new_private_element()
  dump(r.public_element, open(f'./public-data/{ctx.who}.pe', 'wb'))
  dump(r.private_exponent, open(f'./public-data/{ctx.who}.se', 'wb'))


def remote_sig(ctx):
  pk = load(open(f'./public-data/{ctx.other}.key', 'rb'))
  return SignatureScheme(None, pk)


def local_sig(ctx):
  sk = load(open(f'./private-data/{ctx.who}.key', 'rb'))
  pk = load(open(f'./public-data/{ctx.who}.key', 'rb'))
  return SignatureScheme(sk, pk)


def make_ratchet(local, remote):
  return RatchetProtocol(
      local,
      remote,
      protocol.GENERATOR,
      protocol.GROUP_ORDER,
      protocol.MODULUS,
  )


def get_ratchet(ctx):
  ratchet = make_ratchet(local_sig(ctx), remote_sig(ctx))
  ratchet.remote_public_element = load(open(f'./public-data/{ctx.other}.pe', 'rb'))
  ratchet.private_exponent = load(open(f'./public-data/{ctx.who}.se', 'rb'))
  return ratchet


def client(ctx):
  r = get_ratchet(ctx)
  with Connection(ctx.host, ctx.port) as conn:
    for i in range(300):
      msg=random.choice(('jambon', 'kappa', 'abc', 'a', 'b', 'c', 'd'))
      data = r.prepare_send_message(msg)
      conn.send(data + b'\x00')
      ans = conn.recv_until(b'\x00')[:-1]
      message = r.on_recv_message(ans)
      print('Received response to ', msg, 'is', message)


def hack_client(ctx):

  local_pk = load(open(f'./public-data/bob.key', 'rb'))
  remote_pk = load(open(f'./public-data/alice.key', 'rb'))
  lsig = SignatureScheme(None, local_pk)
  rsig = SignatureScheme(None, remote_pk)

  ratchet = make_ratchet(lsig, rsig)

  import glob
  msgs = glob.glob('./public-data/messages/b2a*')
  msgs.sort()
  data = {}

  tb = []
  hl = 256
  for msg_id, msg_fname in enumerate(msgs):
    content = open(msg_fname, 'rb').read()
    signed_data, signature = content.rsplit(b"|", 1)

    h = lsig.hash2(signed_data, msg_id + 1)
    data[msg_id + 1] = [h, signed_data, protocol.decode_int(signature)]

    tb.append([np.array(h, dtype='object'), protocol.decode_int(signature)])
    #signature_valid = lsig.verify(data, protocol.decode_int(signature))
    #assert signature_valid

  N = local_pk.n
  fk = local_sig(ctx)
  last_sig = tb[-1][1]

  def inv(x):
    ix = gmpy2.invert(x, N)
    assert x * ix % N == 1
    return ix


  for i in range(1, len(tb)):
    tb[-i][1] = tb[-i][1] * inv(tb[-i - 1][1]) % N


  for i, (h, x) in enumerate(tb):
    v = fk.sk.r
    for j in range(hl):
      if h[j] == 1: v = v* fk.sk.s[j] %N 
    v = pow(v, 2**i, N)
    assert v == x, i


  mat = []

  last = tb[-1]
  tb = tb[:-1]
  n = len(tb)
  tmp = []
  

  hlist = []
  for i in range(n):
    x = inv(pow(tb[i][1], 2**(n - i), N)) * last[1] % N
    hdiff = last[0] - tb[i][0]
    tmp.append([x, hdiff])
    hlist.append(list(hdiff))
    #print(list(hdiff)) for dumping to sage
  json.dump(hlist, open('./mat.data', 'w'))
  if 0: return
  

  data = Attributize(json.load(open('./tsf.data', 'r')))
  print(data.base)
  slast = 1
  for i, (u, v) in enumerate(data.make_unimodular):
    slast = gmpy2.powmod(slast, u, N) * gmpy2.powmod(tmp[data.base[i]][0], v, N) % N

  scoeffs = [1] * hl
  scoeffs[0] = slast

  for i in range(1, hl):
    scoeffs[i] = tmp[data.mat_id[i-1]][0]


  if 0:
    for have, hdiff in tmp:
      x = 1
      for j, v in enumerate(hdiff):
        x = x * gmpy2.powmod(fk.sk.s[j], (2**(n)) * v, N) % N
      assert x == have

  sexpr = [0] * hl

  if 1:
    for i in range(hl):
      print('processing ', i)
      cur = 1
      for j in range(hl):
        cur = cur * gmpy2.powmod(scoeffs[j], data.imat[i][j], N) % N

      sexpr[i] = cur
      assert cur == (gmpy2.powmod(fk.sk.s[i], 2**n, N))
  else:
    for i in range(hl):
      sexpr[i] = pow(fk.sk.s[i], 2**(n), N)
    r = pow(fk.sk.r, 2**(n), N)

  r = last[1]
  for i in range(hl):
    if last[0][i]:
      r = r * inv(sexpr[i]) % N

  ratchet.remote_public_element = 1
  public_element, iv, ciphertext = ratchet._encrypt_message(REQ_FLAG)
  public_element = 1
  signed_data = protocol.encode_int(public_element, 256) + b"|" + protocol.encode_int(iv, 16) + b"|" + protocol.encode_bytes(ciphertext)



  nmsg_id = n+2
  nh = lsig.hash2(signed_data, nmsg_id)
  print(nh)

  forged_sig = r
  for i, v in enumerate(nh):
    if v: forged_sig = forged_sig * sexpr[i]
  forged_sig = forged_sig * forged_sig * last_sig % N

  data = signed_data + b"|" + protocol.encode_int(forged_sig, 256)

  with Connection(ctx.host, ctx.port) as conn:

    conn.send(data + b'\x00')
    res= conn.recv_until(b'\x00')[:-1]
    ratchet.public_element = 1
    flagans = ratchet.on_recv_message(res, hack=True)
    print(flagans)





def server(ctx):
  STATE_FILE = "private-data/state_alice.pickle"

  if ctx.init:
    alices_state = get_ratchet(ctx)
  else:
    with open(STATE_FILE, "rb") as f:
      alices_state = load(f)

  with open("flag.txt", "r") as f:
    FLAG = f.read()

  cnt = 0
  with Server(ctx.port) as conn:
    while True:
      cnt += 1
      try:
        msg = conn.recv_until(b'\x00')[:-1]

        if ctx.init:
          with open('./public-data/messages/b2a-%04d.txt' % cnt, 'wb') as f:
            f.write(msg)

        message = alices_state.on_recv_message(msg)
        print('RECV msg ', message)
      except Exception as e:
        tb.print_exc()
        break

      if message == REQ_FLAG:
        response = FLAG
      elif message == "exit" or message == "quit":
        exit(0)
      else:
        response = get_random_message()
      response = alices_state.prepare_send_message(response)

      if ctx.init:
        with open('./public-data/messages/a2b-%04d.txt' % cnt, 'wb') as f:
          f.write(response)

      conn.send(response + b'\x00')
  if ctx.init:
    dump(alices_state, open(STATE_FILE, 'wb'))


def main():
  ctx = Attributize()
  ctx.other = other[flags.who]
  ActionHandler.Run(ctx)


app()
