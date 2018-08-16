#!/usr/bin/env python

invmap = {
    0x1e: "A",
    0x30: "B",
    0x2e: "C",
    0x20: "D",
    0x12: "E",
    0x21: "F",
    0x22: "G",
    0x23: "H",
    0x17: "I",
    0x24: "J",
    0x25: "K",
    0x26: "L",
    0x32: "M",
    0x31: "N",
    0x18: "O",
    0x19: "P",
    0x10: "Q",
    0x13: "R",
    0x1f: "S",
    0x14: "T",
    0x16: "U",
    0x2f: "V",
    0x11: "W",
    0x2d: "X",
    0x15: "Y",
    0x2c: "Z",
    0x02: "1",
    0x03: "2",
    0x04: "3",
    0x05: "4",
    0x06: "5",
    0x07: "6",
    0x08: "7",
    0x09: "8",
    0x0a: "9",
    0x0b: "0",
    0x1c: "RETURN",
    0x01: "ESCAPE",
    0x0e: "BACKSPACE",
    0x0f: "TAB",
    0x39: "SPACE",
    0x0c: "MINUS",
    0x0d: "EQUALS",
    0x1a: "LEFTBRACKET",
    0x1b: "RIGHTBRACKET",
    0x60: "BACKSLASH",
    0x2b: "NONUSHASH",
    0x27: "SEMICOLON",
    0x28: "APOSTROPHE",
    0x2b: "GRAVE",
    0x33: "COMMA",
    0x34: "PERIOD",
    0x35: "SLASH",
    0x3a: "CAPSLOCK",
    0x3b: "F1",
    0x3c: "F2",
    0x3d: "F3",
    0x3e: "F4",
    0x3f: "F5",
    0x40: "F6",
    0x41: "F7",
    0x42: "F8",
    0x43: "F9",
    0x44: "F10",
    0x62: "PRINTSCREEN",
    0x61: "SCROLLLOCK",
    0x61: "PAUSE",
    0x52: "INSERT",
    0x47: "HOME",
    0x62: "PAGEUP",
    0x53: "DELETE",
    0x2b: "END",
    0x61: "PAGEDOWN",
    0x4d: "RIGHT",
    0x4b: "LEFT",
    0x50: "DOWN",
    0x48: "UP",
    0x64: "NUMLOCKCLEAR",
    0x65: "KP_DIVIDE",
    0x66: "KP_MULTIPLY",
    0x4a: "KP_MINUS",
    0x4e: "KP_PLUS",
    0x72: "KP_ENTER",
    0x6d: "KP_1",
    0x6e: "KP_2",
    0x6f: "KP_3",
    0x6a: "KP_4",
    0x6b: "KP_5",
    0x6c: "KP_6",
    0x67: "KP_7",
    0x68: "KP_8",
    0x69: "KP_9",
    0x70: "KP_0",
    0x71: "KP_PERIOD",
    0x60: "NONUSBACKSLASH",
    0x63: "KP_EQUALS",
    0x63: "F13",
    0x64: "F14",
    0x62: "HELP",
    0x61: "UNDO",
    0x71: "KP_COMMA",
    0x47: "CLEAR",
    0x1c: "RETURN2",
    0x63: "KP_LEFTPAREN",
    0x64: "KP_RIGHTPAREN",
    0x63: "KP_LEFTBRACE",
    0x64: "KP_RIGHTBRACE",
    0x0f: "KP_TAB",
    0x0e: "KP_BACKSPACE",
    0x33: "KP_COLON",
    0x0c: "KP_HASH",
    0x39: "KP_SPACE",
    0x47: "KP_CLEAR",
    0x1d: "LCTRL",
    0x2a: "LSHIFT",
    0x38: "LALT",
    0x1: "RCTRL",
    0x36: "RSHIFT"
}

#invmap = {}
#for i, code in enumerate('31 30 26 24 29 27 51 53 48 50'.split(' ')):
#  invmap[int(code)] = str(i+1)
#
#codes = '''54 55 47 46 42 40 45 43 11 13 8 10 14 15
#63 62 58 56 61 57 1 5 0 2 6 7 23 22 18 16 21 35 37 32 34 38'''.split()
#vals = '<>qwertyuiop-=asdfghjkl;+*zxcvbnm,./'
#for code, v in zip(codes, vals):
#  invmap[int(code)]=v
#
#
#invmap = {}
#
#codes='''00 02 03 04 05 06
#10 12 13 14 15 16
#20 22 23 24 25 26
#30 32 33 34 35 36
#41 42 43 44 45 46
#51 52 53 54 55 56
#60 62 63 64 65
#72 73 74 75 76'''
#
#vals = '7890<>654321UIOP-=YTREWQJKL;+*HGFDSANM,.?BVCXZ'
#codes=codes.split()
#assert len(vals) == len(codes)
#for c, v in zip(codes, vals):
#  cc = int(c[0]) * 8 + int(c[1])
#  invmap[cc] = v

import csv
data = csv.reader(open("data.csv", "r"))
head = True
#we store it as a list of times, state
k0, k1, k2, k3, k4, k5 = ([], []), ([], []), ([], []), ([], []), ([], []), ([], [])
kr1, kr2 = ([], []), ([], [])
print(data.__next__())
for row in data:
  k0[0].append(row[3].strip())
  k0[1].append(row[4].strip())
  k1[0].append(row[5].strip())
  k1[1].append(row[6].strip())
  k2[0].append(row[7].strip())
  k2[1].append(row[8].strip())
  k3[0].append(row[9].strip())
  k3[1].append(row[10].strip())
  k4[0].append(row[11].strip())
  k4[1].append(row[12].strip())
  k5[0].append(row[13].strip())
  k5[1].append(row[14].strip())
  kr1[0].append(row[15].strip())
  kr1[1].append(row[16].strip())
  kr2[0].append(row[17].strip())
  kr2[1].append(row[18].strip())


def cleanup(k):
  for i in range(len(k[0])):
    if k[0][i] != '':
      k[0][i] = float(k[0][i])
    else:
      k[0][i] = 500.0
    if k[1][i] != '':
      k[1][i] = int(k[1][i])
    else:
      k[1][i] = 2


cleanup(k0)
cleanup(k1)
cleanup(k2)
cleanup(k3)
cleanup(k4)
cleanup(k5)
cleanup(kr1)
cleanup(kr2)



def findtimeindex(times, time):
  beg, end = 0, len(times)-1
  while end - beg >= 1:
    mid = (beg + end+1) // 2
    if times[mid] > time:
      beg, end = beg, mid-1
    else:
      beg, end = mid, end
  return beg


def get(klist, kr1):
  res = ''
  for i in range(len(kr1[0])):
    if kr1[1][i] == 0:
      #we read the code
      t = kr1[0][i]
      i0 = findtimeindex(klist[0][0], t)
      i1 = findtimeindex(klist[1][0], t)
      i2 = findtimeindex(klist[2][0], t)
      i3 = findtimeindex(klist[3][0], t)
      i4 = findtimeindex(klist[4][0], t)
      i5 = findtimeindex(klist[5][0], t)
      v0 = 1 ^ 1 ^ klist[0][1][i0]
      v1 = 1 ^ 1 ^ klist[1][1][i1]
      v2 = 1 ^ 1 ^ klist[2][1][i2]
      v3 = 1 ^ 0 ^ klist[3][1][i3]
      v4 = 1 ^ 0 ^ klist[4][1][i4]
      v5 = 1 ^ 1 ^ klist[5][1][i5]
      value = (v0 << 0) | (v1 << 1) | (v2 << 2) | (v3 << 3) | (v4 << 4) | (v5 << 5)
      #value = (v0 << 5) | (v1 << 4) | (v2 << 3) | (v3 << 2) | (v4 << 1) | (v5 << 0)
      nv = invmap.get(value, "unk")
      if len(nv) == 1: res += nv
  return res


import itertools
klist0 = (k0, k1, k2, k3, k4, k5)
#for klist in itertools.permutations():
print(get(klist0, kr1))
