#!/usr/bin/env python

import struct
import pickle


m1 = 0x2dad
intervals = []
intervals.append((0x1208, 0x1248))
intervals.append((0x5c4d, 0x5c8d))
def check_in(x):
  for a0, b0 in intervals:
    if 2*x+1 >= a0+1 and 2*x < b0: return 1
  return 0
def poly(x, a0, a1, a2):
  x[a1] = (x[a1] - x[a0]) & 0xffff
  return a2 and (x[a1] == 0 or (x[a1] >> 15 & 1))

def do_step(b, x):
  if poly(x,  x[b], x[b+1], x[b+2]):
    if x[b+2] == 0xffff:
      return None
    b = x[b+2]
  else:
    b += 3
  return b

def make_secret(x, m2):

  b = m2
  rnd = 0
  output = []
  mb = 0
  while True:
    mb = max(b, mb)
    rnd += 1
    if b + 3  > m1: break

    mb = max(mb, x[b+1], x[b+2])
    va = x[b+0]
    vb = x[b+1]
    if check_in(va) or check_in(vb):
      print('Using here', hex(va), hex(vb), hex(x[va]), hex(x[vb]), hex(rnd))
    b = do_step(b, x)

    #if rnd == 3: 
    #  break
    if x[4]:
      output.append(x[2] & 0xff)
      print(bytes(output))
      x[2] = 0
      x[4] = 0
      if bytes(output) == b'Welcome to FLARE spy messenger by Nick Harbour.\r\nYour preferred covert communication tool since 1776.\r\nPlease wait while I check that password...':
        print(b)
        pickle.dump((b, x), open('./turing_data/state.start', 'wb'))
        ser = bytearray(struct.pack('<65536H', *x))
        open('./turing_data/state.start.x.bin', 'wb').write(ser)
        return

  print(bytes(output))
  print(hex(mb*2))
  print(mb)

def make_secret_solve(x, m2):

  b, x = pickle.load(open('./turing_data/state.start', 'rb'))
  print('START ', b)
  rnd = 0
  #taint = set()
  #for a, b in intervals[0:1]:
  #  for i in range(a//2, b//2):
  #    taint.add(i)
  #stop = set((0x120a//2,))

  while True:
    rnd += 1
    if b + 3  > m1: break

    va = x[b+0]
    vb = x[b+1]
    if check_in(va) or check_in(vb):
      print('got on ', rnd)
    #if vb in taint:
    #  taint.add(va)
    #  print('taint', hex(va), x[va])
    #if va in taint:
    #  print('USE COND ', x[va], x[vb])
    b = do_step(b, x)
    #if va in stop or vb in stop:
    #  print('stopping here')
    #  break

    #if rnd == 3: 
    #  break
    if x[4]:
      break


def decode():
  if 0:
    addr = 0x97c0 * 16 + 0x0223
    buf = open('./dump.test.mem', 'rb').read()[addr:]
    buf = buf[:0x20000]
  else:
    buf = open('./dump.turing2.mem', 'rb').read()[:0x20000]

  x = []
  for i in range(0, len(buf), 2):
    x.append(struct.unpack('<H', buf[i:i+2])[0])

  ser = bytearray(struct.pack('<65536H', *x))
  open('./turing_data/cur.start.x.bin', 'wb').write(ser)


  if 0:
    make_secret(x, 5)
  else:
    make_secret_solve(x, 5)


decode()
