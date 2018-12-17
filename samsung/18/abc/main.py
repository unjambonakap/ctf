#!/usr/bin/env python

from chdrft.cmds import CmdsList
from chdrft.main import app
from chdrft.utils.cmdify import ActionHandler
from chdrft.utils.misc import Attributize
import chdrft.utils.misc as cmisc
import glog
from chdrft.tools.elf_mod import extract_binary_syms
import chdrft.struct.base as cbase
from chdrft.emu.binary import x64_mc
import base64
from chdrft.utils.fmt import Format
from chdrft.tube.connection import Connection
import os
from collections import defaultdict

global flags, cache
flags = None
cache = None

def get_uniq(x):
  x = list(x)
  assert len(x) == 1
  return x[0]



def args(parser):
  clist = CmdsList().add(test).add(go)
  parser.add_argument('--binary')
  parser.add_argument('--rundir', default='./out')
  ActionHandler.Prepare(parser, clist.lst)

class Intervals:
  def __init__(self, collection):
    self.mp = {}
    self.intervals = []
    for inter, x in collection:
      self.intervals.append(inter)
      self.mp[inter] = x

  def find(self, a):
    for inter in self.intervals:
      if inter.contains(a):
        return  self.mp[inter]
    return None



class BinHelper:
  def __init__(self, fname, sym_data):
    self.fname = fname
    self.f = open(fname, 'rb').read()
    self.sd = sym_data


  def get_func(self, name):
    if isinstance(name, str): f = self.sd[name]
    else: f=name

    data = self.f[f.offset:f.offset+f.realsz]
    return data

  def get_func_ins(self, name):
    data = self.get_func(name)
    return x64_mc.disp_ins(data, addr=f.offset)


  def find_strs_exact(self, x):
    x = Format(x).tobytes().v

    for s in self.sd.s:
      if s.value == x:
        yield s

  def find_strs(self, x):
    x = Format(x).tobytes().v

    for s in self.sd.s:
      if s.value.find(x) !=-1:
        yield s

def outdeg_filter(lst):
  lst = cmisc.to_list(lst)
  tgt = defaultdict(lambda: 0)
  for x in lst:
    tgt[x] += 1
  def check(x):
    for k, v in tgt.items():
      if x.outdeg['sym.imp.'+k] != v: return False
    return True
  return check

def r2_extract_all(filename):
  import r2pipe
  p = r2pipe.open(filename)
  p.cmd('aac')

  def do_cmd(x):
    return cmisc.Attributize.RecursiveImport(p.cmdj(x))
  res = cmisc.Attributize()

  funcs = cmisc.Attributize({d['name']:d for d in do_cmd('aflj')})
  strs = do_cmd('izj')
  xrefs = do_cmd('axj')
  xrefs = {v['addr']: v for v in xrefs}

  for x in strs:
    x.value = base64.b64decode(x.string)
    x.xrefs = []

  for f in funcs.values():
    f.outdeg = defaultdict(lambda: 0)

  funcs_inter = Intervals([(cbase.Range1D(x.offset, n=x.size-1), x) for x in funcs.values()])
  strs_inter = Intervals([(cbase.Range1D(x.vaddr, n=x.size-1), x) for x in strs])

  for k,v in xrefs.items():
    a =  strs_inter.find(v)
    b = funcs_inter.find(k)
    if not a or not b: continue
    #print(a.value, b.name, hex(v), hex(k))
    a.xrefs.append(b)

  for f in funcs.values():
    f.codexrefs_funcs = []
    for xref in f.codexrefs:
      u = funcs_inter.find(xref.addr)
      if u is None: continue
      f.codexrefs_funcs.append(cmisc.Attributize(func=u.name, addr=xref.addr, obj=u))
      u.outdeg[f.name] += 1

  return cmisc.Attributize(funcs_inter=funcs_inter, strs_inter=strs_inter, f=funcs, s=strs)

def find_in_list(lst, sublist):
  for i in range(len(lst)-len(sublist)+1):
    for j in range(len(sublist)):
      if lst[i+j] != sublist[j]: break
    else: yield i

def patch_read_num_func(bh):
  d_atoi = bh.sd.f['sym.imp.atoi']
  read_num_xref = d_atoi.codexrefs_funcs[0]
  inslist = x64_mc.get_ins(bh.get_func(read_num_xref.obj), addr=read_num_xref.obj.offset)
  for ins in inslist:
    if ins.mnemonic!='mov': continue
    if ins.mnemonic=='call': break
    if ins.op_str.startswith('edx, '):
      return [(ins.address+2, 0)]

def patch_format_vuln(bh):
  view_s = get_uniq(bh.find_strs('View memo name'))
  fx = outdeg_filter('printf printf strcmp printf')
  func_view = get_uniq(filter(fx, view_s.xrefs))

  inslist = x64_mc.get_ins(bh.get_func(func_view), addr=func_view.offset)
  mlist = list([ins.mnemonic for ins in inslist])

  pos = get_uniq(find_in_list(mlist, cmisc.to_list('mov mov lea mov call lea mov mov mov mov call')))
  tins1 = inslist[pos +5]
  tins2 = inslist[pos +8]
  yield (tins1.address+3, tins1.bytes[3]+6)
  yield (tins2.address+2, 0xc6)

  prev_s = get_uniq(bh.find_strs_exact('[%s]\\n')).vaddr
  target_s = prev_s + 6


def patch_mod_vuln(bh):
  mod_s = get_uniq(bh.find_strs('Modify memo name'))
  func_mod = get_uniq(filter(outdeg_filter('printf strcmp printf printf realloc'), mod_s.xrefs))
  inslist = x64_mc.get_ins(bh.get_func(func_mod), addr=func_mod.offset)

  for ins in inslist:
    if ins.mnemonic!='cmp' or ins.op_str!= 'dx, ax': continue
    yield (ins.address+3, 0x90)
    yield (ins.address+4, 0x90)
    return


def solve(fname):
  a = r2_extract_all(fname)
  d_read = a.f['sym.imp.read']
  d_realloc = a.f['sym.imp.realloc']

  bh = BinHelper(fname, a)



  mod_memo_f = d_realloc.codexrefs_funcs[0]



  patches = []
  patches.extend(patch_read_num_func(bh))
  patches.extend(patch_format_vuln(bh))
  patches.extend(patch_mod_vuln(bh))

  print(fmt_patches(patches))
  assert len(patches) <= 5
  return patches

def fmt_patches(patches):
  import io
  x = io.StringIO()
  for addr, b in patches:
    print(f'{hex(addr)}, {hex(b)}', file=x)
  if len(patches)!=5:
    print(file=x)
  return x.getvalue()

def test(ctx):
  solve(ctx.binary)


def go(ctx):

  with Connection('abc.eatpwnnosleep.com', 55555, logfile='./conn.log') as conn:
    for itx in range(100):
      print('ON ITER ', itx)
      conn.logfile_obj.flush()
      px = cmisc.TwoPatternMatcher(f'[*] TRY {itx+1}/100', '[!] Fail!')
      conn.recv_until(px)
      if px.b_check:
        print('FAIL  on ', itx-1)
        return


      r = conn.recv_until('[?]').decode()
      lines = r.splitlines()
      data = []
      print(r)
      for line in lines:
        if not line.startswith('[') and line:
          data.append(line)
      fname = f'{ctx.rundir}/f_{ctx.runid}_{itx}.bin'

      with open(fname, 'wb') as f:
        f.write(base64.b64decode(get_uniq(data)))
      patches = solve(fname)
      conn.send(fmt_patches(patches))
    print(conn.recv_timeout(2))


#SCTF{H0w_b34u7ifu1_7h3_4u7om47ic_p47ch3r_i5!}


def main():
  ctx = Attributize()
  ActionHandler.Run(ctx)


app()
