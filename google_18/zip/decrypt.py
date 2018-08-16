import os
import zipfile
import zlib
import hashlib
from struct import pack, unpack, calcsize
import sys
from better_zip import LFSRCipher
import yaml
import struct

POLY_SZ = 20

data = open("flag.zip", "rb").read()
dataread = data[:]


def getu(format):
  global dataread
  r = unpack(format, dataread[:calcsize(format)])
  dataread = dataread[calcsize(format):]
  return r[0]


head = getu("4s")
assert (head == b'PK\x03\x04')
assert (getu("H") == 90)
assert (getu("B") == 0x01)
assert (getu("B") == 0x80)
assert (getu("3H") == 0)
crc = getu("I")
sz = getu("I")
filz = getu("I")
namz = getu("H")
assert (getu("H") == 0)
name = getu(str(namz) + "s")
print(hex(crc), sz, filz, namz, name)
key_iv = getu("20s")
cipher_iv = getu("20s")
datapng = dataread[:filz]
#open('./file.png', 'wb').write(datapng)
c = LFSRCipher(b'0' * POLY_SZ, POLY_SZ, key_iv, cipher_iv)
lfsr_data = []
for x in c.lfsr:
  lfsr_data.append(x.r)

d = c.crypt(datapng)
print(d[:20], 'a')
d = d[:20]
blk_size, = struct.unpack('>I', d[8:12])
print(blk_size)
#print([hex(ord(x)) for x in d[:20]])

#known = struct.pack('>I2B', 480)
known_end = struct.pack('>I', 0) + b'IEND\xae\x42\x60\x82'

second_block_pos = 8 + blk_size + 12
#sec_block = struct.pack('>I', 9) + b'pHYs'
sec_block = b'\x00' * 3
import binascii
print(binascii.hexlify(known_end))
print(binascii.hexlify(sec_block))

config = {}
tb = []


def add_known(buf, offset):

  for i, x in enumerate(buf):
    for j in range(8):
      tb.append(dict(pos=offset * 8 + i * 8 + j, val=(ord(x) >> j) & 1))


sz = len(datapng)
add_known(d, 0)
add_known(sec_block, second_block_pos)
add_known(known_end, sz - 12)
canlist = 'PLTE IDAT cHRM gAMA sBIT bKGD hIST tRNS pHYs tIME tEXt zTXt'.split()
for x in canlist:
  add_known(bytes(x), second_block_pos+4)


height_pos = 20
add_known(struct.pack('>BB', 0, 0), height_pos)
#add_known(struct.pack('>I', 480), height_pos)

for bit_depth in (1,2,4,8,16):
  add_known(struct.pack('>B', bit_depth), height_pos+4)

for color_type in (0, 2, 3, 4, 6):
  add_known(struct.pack('>B', color_type), height_pos+5)

for compression in (0, ):
  add_known(struct.pack('>B', compression), height_pos+6)

for filter in (0, ):
  add_known(struct.pack('>B', filter), height_pos+7)

for interlace in (0, 1):
  add_known(struct.pack('>B', interlace), height_pos+8)


config["known"] = tb
config["lfsr"] = lfsr_data
open('config.yaml', 'w').write(yaml.dump(config))
