import crackme
from obf import *
from types import *
from random import shuffle

def space_print(s, spcount):
  for ln in s.splitlines():
    print (" " * spcount) + ln

print "def crackme():"

cr = dir(crackme)
shuffle(cr)

for n in cr:
  if n.startswith("__"):
    continue

  o = getattr(crackme, n)
  if type(o) is not FunctionType:
    print "  # Skipping:", o
    continue

  space_print("global %s" % n, 2)
  space_print(obfuscate(o, True), 2)  

print "  main()"

