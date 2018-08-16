#!/usr/bin/env python

import pefile
import sys

x=pefile.PE('./cryptochief.exe')
pos=0x8a3d0
sx=x.get_memory_mapped_image()[pos:pos+600]
l=sx.find('\x00')
sx=sx[:l]
sys.stdout.write(sx)

