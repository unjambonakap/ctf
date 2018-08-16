from dis import dis, hasjabs, hasconst, hasname, haslocal, hasjrel
from opcode import HAVE_ARGUMENT
from ctypes import *
from sys import getsizeof
from struct import pack
from os import urandom
from random import randint
from types import *

__all__ = ["obfuscate"]

def db(v):
  return pack("<B", v)

def dw(v):
  return pack("<H", v)

def dd(v):
  return pack("<I", v)

def dq(v):
  return pack("<Q", v)


def JUMP_ABSOLUTE(where):
  return db(0x71) + dw(where)

def JUMP_FORWARD(offset):
  return db(0x6e) + dw(offset)

def LOAD_CONST(which):
  return db(0x64) + dw(which)

def RETURN_VALUE():
  return db(0x53)

def NOP():
  return db(0x09)

def __decode():
  state = getattr(REPLACEME, "e", True)
  c = REPLACEME.func_code.co_code
  off = getsizeof("") - 1
  ptr = (c_byte * len(c)).from_address(id(c) + off)
  key = map(ord, c[3:16])
  sz = "REPLACEMETOO"
  i = 0
  while i < sz:
    ptr[3 + 13 + i] ^= key[i % 13]
    i += 1
  if not state:
    setattr(REPLACEME, "e", True)
    return
  else:
    setattr(REPLACEME, "e", False)
  
  pass # Real fall through.

#dis(__decode)

def fixup_codec(bytecode, offset, names_offset, consts_offset, varnames_offset):
  i = 0
  c = map(ord, bytecode)
  n = len(c)

  return_fixed = False

  def fixup(off):
    # c and i have lambda-bindings.
    org = c[i+1] | (c[i+2] << 8)
    org += off
    c[i+1] = org & 0xff
    c[i+2] = (org >> 8) & 0xff

  while i < n:
    op = c[i]
    op_len = [1, 3][op >= HAVE_ARGUMENT]

    if op in hasconst:
      fixup(consts_offset)
    elif op in hasname:
      fixup(names_offset)
    elif op in haslocal:
      fixup(varnames_offset)
    #elif op in hasjabs:     
    # fixup(offset)

    # Fix the return so that None is not returned.
    if not return_fixed and op == 0x53:  # RETURN_VALUE
      prev = i - 3
      if c[prev] != 0x64:  # LOAD_CONST
        raise Exception("Codec return fix failed.")
      c[prev:prev+3] = [0x09] * 3  # NOP NOP NOP
      return_fixed = True


    i += op_len

  # Remove RETURN_VALUE.
  if c[-1] != 0x53:
    raise Exception("Why is RETURN_VALUE not there?!")

  c = c[:-1]

  return ''.join(map(chr, c))

def fixup_code(bytecode, offset, hook_return=True, obfuscate=True):

  # Phase 1: Initial scan and filling.
  i = 0
  fc = [0] * offset
  c = map(ord, bytecode)
  n = len(c)  

  relocs = []  # Tuple of: instruction addr, original destination.
  mapping = {}

  while i < n:
    op = c[i]
    emit = True
    op_len = [1, 3][op >= HAVE_ARGUMENT]

    # Add obfuscation if needed.
    combo_breaker = randint(0,1) == 0
    if obfuscate and combo_breaker:
      obf_sz = randint(1, 9)
      fc.extend(map(ord, JUMP_FORWARD(obf_sz)))
      for _ in range(obf_sz):
        # XXX DEBUG
        fc.append(randint(0, 0x8F))
        #fc.append(0x09)

    # Now the instruction is in a stable spot.
    mapping[i] = len(fc)

    # Check for later relocations.
    if op in hasjabs:
      org_dst = c[i+1] | (c[i+2] << 8)
      relocs.append((i, org_dst, "ABS"))
    elif op in hasjrel:
      org_dst = (c[i+1] | (c[i+2] << 8)) + 3 + i
      relocs.append((i, org_dst, "REL"))      

    # Check if this is a return address.
    if hook_return and op == 0x53:  # RETURN_VALUE
      # Add a far jump instead.
      dst = n + 3
      relocs.append((i, dst, "ABS"))
      fc.extend(map(ord, JUMP_ABSOLUTE(dst)))
      emit = False

    # Emit the instruction.
    if emit:
      fc.extend(c[i:i+op_len])

    i += op_len

  # Add two more mappings.
  mapping[n] = len(fc)
  mapping[n + 3] = len(fc) + 3

  # Phase 2: Fixups.
  for r_i, r_dst, r_type in relocs:
    i = mapping[r_i]
    dst = mapping[r_dst]    
    if r_type == "ABS":
      pass
    elif r_type == "REL":
      dst -= i + 3

    fc[i+1] = dst & 0xff
    fc[i+2] = (dst >> 8) & 0xff


  return ''.join(map(chr, fc[offset:])) 

# Replace one item in the list with something else. Search from the end
# backwards.
def rreplace(li, what, with_what):
  i = len(li) - 1
  while i >= 0:
    if li[i] != what:
      i -= 1
      continue
    li[i] = with_what
    return
  raise Exception("rreplace did not find item to replace")

# Customizes representation of objects if needed.

class ReprCodeWrapper():
  def __init__(self, o):
    self.o = o

  def __repr__(self):
    o = self.o
    return ("types.CodeType("
                "%u, %u, %u, %u, %s, %s, %s, %s, '', '', 0, '')") % (
        o.co_argcount, o.co_nlocals, o.co_stacksize, o.co_flags,
        repr(o.co_code), repr(o.co_consts), repr(o.co_names),
        repr(o.co_varnames)
        )

class ReprStringWrapper():
  def __init__(self, o):
    self.o = o

  def __repr__(self):
    e = self.o.encode("zlib")[::-1]  # Pro encryption!
    return "_(%s)" % repr(e)

def customize_repr(obj, encrypt_str=False):
  t = type(obj)
  
  pod = set([
      NoneType,
      TypeType,
      BooleanType,      
      IntType,
      LongType,
      FloatType,
      UnicodeType,
      TupleType,
      DictType,
      ListType
  ])

  if not encrypt_str:
    pod.add(StringType)

  if t in pod:
    return obj

  if t is CodeType:
    return ReprCodeWrapper(obj)

  if t is StringType:
    return ReprStringWrapper(obj)  

  raise Exception("Type %s not supported!" % t)

# Obfuscates the function and prints it to stdout.
def obfuscate(f, encrypt_str=False):
  out = ""
  code = f.func_code
  key = urandom(13)

  # XXX DEBUG
  #key = "\x00" * 13  

  fixed_code = fixup_code(code.co_code, 0x10)
  fixed_code = ''.join([
    chr(ord(c) ^ ord(key[i % 13])) for i, c in enumerate(fixed_code)])

  d_code = __decode.func_code
  d_namesoff = len(code.co_names)
  d_constsoff = len(code.co_consts)  
  d_varsoff = code.co_nlocals

  fixed_decode = fixup_codec(
      d_code.co_code, 3 + 13 + len(fixed_code) + 6,
      d_namesoff, d_constsoff, d_varsoff)
  fixed_decode = fixup_code(
      fixed_decode, 3 + 13 + len(fixed_code) + 6,
      False, True)

  new_code = ""

  # 0
  new_code += JUMP_ABSOLUTE(
      3 +  # Size of this opcode.
      13 + # Key size.
      len(fixed_code))

  # 3
  new_code += key

  # 3 + 13
  new_code += fixed_code   # XOR this later.

  # 3 + 13 + len(orginal code)
  new_code += JUMP_FORWARD(3)

  # 3 + 13 + len(orginal code) + 3
  new_code += JUMP_FORWARD(0)
  #new_code += RETURN_VALUE()
  #new_code += NOP()  
  #new_code += NOP()
  #new_code += NOP()

  # 3 + 13 + len(orginal code) + 6
  new_code += fixed_decode
  new_code += JUMP_ABSOLUTE(16)

  # Stringify!
  out += "%s = types.FunctionType(\n" % f.func_name
  out += "    types.CodeType(\n"
  out += "        %u, %u, %u, %u,\n" % (
      code.co_argcount,
      code.co_nlocals + d_code.co_nlocals,
      code.co_stacksize + d_code.co_stacksize,
      code.co_flags
      )
  out += "        %s,\n" % repr(new_code)

  # Fix consts; also fix whatever the decoder requires.
  fixed_consts = list(code.co_consts) + list(d_code.co_consts)
  rreplace(fixed_consts, "REPLACEMETOO", len(fixed_code))
  fixed_consts = [customize_repr(x, encrypt_str) for x in fixed_consts]
  fixed_consts = tuple(fixed_consts)

  out += "        %s,\n" % repr(fixed_consts)

  # Fix names; also fix whatever the decoder requires.
  fixed_names = list(code.co_names) + list(d_code.co_names)
  rreplace(fixed_names, "REPLACEME", f.func_name)
  fixed_names = [customize_repr(x, encrypt_str) for x in fixed_names]  
  fixed_names = tuple(fixed_names)

  out += "        %s,\n" % repr(fixed_names)

  # co_varnames, filename, name, firstlineno, lnotab
  
  # XXX DEBUG
  #out += "        (),\n"
  fixed_varnames = list(code.co_varnames) + list(d_code.co_varnames)
  fixed_varnames = [customize_repr(x, encrypt_str) for x in fixed_varnames]    
  fixed_varnames = tuple(fixed_varnames)
  out += "        %s,\n" % repr(fixed_varnames)
  
  out += "        '', '', 0, ''\n"
  out += "    ), globals()\n"
  out += ")\n\n"

  return out

