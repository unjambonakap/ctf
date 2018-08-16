import st1
from obf import *
from types import *

print """#!/usr/bin/python
import types
import dis
from sys import getsizeof, stdout
from ctypes import c_byte
"""
def _(s):
  return s[::-1].decode(''.join([chr(x) for x in [99,98,102,105,104,108,111,122][::-2]]))

print obfuscate(_, False)

for n in dir(st1):
  if n.startswith("__"):
    continue

  o = getattr(st1, n)
  if type(o) is not FunctionType:
    print "  # Skipping:", o
    continue

  print obfuscate(o, True)

print "crackme()"

