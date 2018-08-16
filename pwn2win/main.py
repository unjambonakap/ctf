#!/usr/bin/env python

from chdrft.cmds import CmdsList
from chdrft.main import app
from chdrft.utils.cmdify import ActionHandler
from chdrft.utils.misc import Attributize
import chdrft.utils.misc as cmisc
import glog
import math
import pprint
from chdrft.utils.path import FileFormatHelper
import subprocess as sp
from chdrft.utils.cache import Cachable
from chdrft.struct.base import Box, ListTools
from collections import defaultdict
import io
import time
from chdrft.emu.trace import Display
from queue import Queue
import networkx.algorithms.cycles
import networkx as nx
from chdrft.utils.fmt import Format
from collections import deque

from chdrft.utils.swig import swig
swig.setup(args=[])
algo = swig.opa_algo_swig

from vispy import app as vapp
from vispy import gloo
from vispy.util import load_data_file
from vispy.visuals.collections import PathCollection, PolygonCollection
from vispy.visuals.transforms import PanZoomTransform
from vispy.color import Color, get_colormap, Colormap
from chdrft.graph.base import OpaGraph
import z3

import gdspy

global flags, cache
flags = None
cache = None
import numpy as np

CELL_INPUTS = ('A', 'B', 'C', 'CLK', 'D', 'clock', 'reset_n', 'in')
CELL_OUTPUTS = ('Q', 'Y', 'unlocked')
CELL_ALIMS = ('vdd', 'gnd')

def args(parser):
  clist = CmdsList().add(test).add(build_circuit).add(build_design).add(do_proc_stats).add(debug_netlist).add(do_read_desc)
  clist.add(list_cells).add(compute_logic_table).add(test_karnaugh)

  ActionHandler.Prepare(parser, clist.lst)
  parser.add_argument('--cell', default='mkShiftReg')
  parser.add_argument('--cell_fmt', default='*', nargs='*')
  parser.add_argument('--binary')
  parser.add_argument('--desc_file')
  parser.add_argument('--cell_logic_desc', type=FileFormatHelper.Read)
  parser.add_argument('--filename')
  parser.add_argument('--patch', action='store_true')
  parser.add_argument('--display_circuit', action='store_true')
  parser.add_argument('--simulate', action='store_true')


cell_to_data = {}
global gid
gid = 0


def get_cell_info(cell, pos=np.array([0., 0.]), mirror_x=False, rot180=False):
  global gid
  gid += 1

  if not cell.name in cell_to_data:
    res = []
    for e in cell.elements:
      if isinstance(e, gdspy.CellReference):
        rd = get_cell_info(
            e.ref_cell,
            e.origin,
            mirror_x=e.x_reflection,
            rot180=e.rotation is not None,
        )
        res.extend(rd)

      elif isinstance(e, gdspy.Polygon):
        assert len(e.points) == 4
        res.append(cmisc.Attributize(pos=e.points, layer=e.layer, type='poly', cell_name=cell.name))

    for label in cell.labels:
      res.append(
          cmisc.Attributize(
              pos=label.position,
              layer=label.layer,
              text=label.text,
              type='label',
              cell_name=cell.name
          )
      )
    cell_to_data[cell.name] = res


  seen_gid = {}
  seen_gid[None] = gid
  gid += 1
  nres = []
  finalid = 0
  for e in cell_to_data[cell.name]:
    ne = e._do_clone()
    ne.pos = np.array(e.pos)
    if rot180: ne.pos = -ne.pos
    if mirror_x:
      ne.pos = ne.pos * np.array([1, -1])


    ne.pos += pos
    ne.idx = finalid
    finalid+=1

    cid = ne.get('cellid', None)
    if cid not in seen_gid:
      seen_gid[cid] = gid
      gid += 1
    ne.cellid = seen_gid[cid]

    ne.cell_name = ne.cell_name
    nres.append(ne)
  return nres


def dump_cell_info(cinfo):
  f = io.StringIO()

  print(len(cinfo), file=f)
  for e in cinfo:
    pos = np.around(e.pos * 10000).astype(np.int32)
    if e.type == 'poly':
      box = Box().union_points(pos)
      minv = np.amin(pos, axis=0)
      maxv = np.amax(pos, axis=0)
      if (minv[0] == 1804000 and minv[1] == 2677000 and
        maxv[0] == 1827000 and maxv[1] == 2683000):
        print('Patching ')
        # FUUUUUCK YOU
        for i in range(4):
          for j in range(2):
            if pos[i,j] == 1827000:
              pos[i,j] = 1828000

    print(e.idx, [0, 1][e.type == 'poly'], e.layer, e.cell_name+'_'+str(e.cellid), end='', file=f)
    if e.type == 'poly':
      for i in range(4):
        print('', pos[i, 0], pos[i, 1], end='', file=f)
      print(file=f)
    else:
      print('', pos[0], pos[1], e.text, file=f)
  return f.getvalue()


class Cell:
  def __init__(self, name, pins, logic_desc=None):
    self.name, self.cellid = name.split('_')
    self.pins = pins
    self.inputs = {}
    self.outputs = {}
    self.output = None
    self.alims = {}
    self.pins_typ = {}
    self.pin_to_name = {}
    self.data = None
    self.logic_desc = logic_desc

    for pid, pname, idx in pins:
      typ = None
      if pname in CELL_INPUTS:
        self.inputs[pname] = pid
        typ = 'input'

      elif pname in CELL_ALIMS:
        self.alims[pname] = pid
        typ = 'alim'
      elif pname in CELL_OUTPUTS:
        assert self.output is None
        self.output = pid
        self.outputs[pname] = pid
        typ = 'output'
      else:
        assert 0, pname
      self.pin_to_name[pid] = pname
      self.pins_typ[pname] = typ

  @property
  def is_reg(self):
    return self.name == 'LDCZ'

  def compute(self, vals):
    ins = {}
    for name, pid in self.inputs.items():
      ins[name] = vals[pid]
    res = self.evaluate(**ins)
    assert res is not None
    if self.output is not None:
      vals[self.output] = res


  def evaluate(self, **kwargs):
    if self.is_reg:
      return self.evaluate_ldcz(**kwargs)
    else:
      table = self.logic_desc[self.name]
      return self.evaluate_table(table, **kwargs)


  def evaluate_ldcz(self, D=None, CLK=None):
    if self.data is None: self.data = 0
    if CLK:
      self.data = D
    return self.data

  def evaluate_table(self, table, **kwargs):
    return table.op.repl(kwargs)()

    #k = list(kwargs.items())
    #k.sort()
    #k = tuple(k)
    #assert k in table, k
    #return table[k]


class Operation:
  def __init__(self):
    self.typ = None
    self.ops = []
    self.basev = None

  @property
  def is_none(self):
    return not self.typ and not self.basev

  def __mul__(self, v):
    if self.is_none: return v
    res = Operation()
    res.typ = '*'
    res.ops = [self, v]
    return res


  def __or__(self, v):
    if self.is_none: return v
    res = Operation()
    res.typ = '|'
    res.ops = [self, v]
    return res

  def __and__(self, v):
    if self.is_none: return v
    res = Operation()
    res.typ = '&'
    res.ops = [self, v]
    return res

  def __invert__(self):
    assert not self.is_none
    res = Operation()
    res.typ = '!'
    res.ops = [self]
    return res

  def repl(self, repl_basev):
    res = Operation()
    res.typ = self.typ
    for x in self.ops:
      res.ops.append(x.repl(repl_basev))
    return res

  def __str__(self):
    if len(self.ops) == 1:
      return '%s %s'%(self.typ, self.ops[0])
    return '(%s %s %s)'%(self.ops[0], self.typ, self.ops[1])

  def __call__(self):
    ops = list([op() for op in self.ops])
    if self.typ == '!':
      return ~ ops[0]
    elif self.typ == '|':
      return ops[0] | ops[1]
    elif self.typ == '&':
      return ops[0] & ops[1]
    else: assert 0



class Operand(Operation):
  def __init__(self, basev):
    super().__init__()
    self.basev = basev

  def repl(self, repl_basev):
    return Operand(repl_basev[self.basev])

  def __call__(self):
    return self.basev

  def __str__(self):
    return str(self.basev)


def karnaugh_simplify(table):
  keys = list(table.keys())[0]
  operands = dict({u:u for u,_ in keys})
  cnt = 0
  n = len(table)
  for e in table.values(): cnt += e
  negate = cnt >= n / 2
  res = Operation()


  for entry, val in table.items():
    if negate ^ (val == 0): continue
    operand = Operation()
    entryv = dict(entry)
    for k, v in operands.items():
      wx = entryv[k]
      v = Operand(v)
      if not wx: v = ~ v
      operand = operand & v
    res = res | operand

  if negate: res = ~ res
  return res


def test(ctx):
  gdsii = gdspy.GdsLibrary()
  gdsii.read_gds(
      cmisc.
      path_here('./shiftreg_e7f285dccca5788b157d72e7fde31a92ed765c64ec86d56164426b7c1cde1625.gds2'),
  )
  xvals = set()
  yvals = set()
  cinfo = get_cell_info(gdsii.cell_dict[ctx.cell])
  dump_cell_info(cinfo)


def proc_stats(stats_filename):
  lines = open(stats_filename, 'r').readlines()

  res = []
  edges = cmisc.defaultdict(lambda: [])
  for line in lines:
    if not line.startswith('Processing layers'): continue
    cx = line.rpartition(' : ')[2]

    mp = {}
    for e in cx.split(','):
      tmp = e.split('=')
      if len(tmp) < 2: continue
      mp[tmp[-2]] = eval(tmp[-1])
    if mp['a.ratio1'] > 0.9 or mp['a.ratio2'] > 0.9:
      a = mp['a.first']
      b = mp['b.first']
      edges[a].append(b)
      edges[b].append(a)
  return edges


def read_layer_info(content):
  lines = content.splitlines()
  for line in lines[1:]:
    yield int(line)


def parse_netlist(s, layer1, layer2):
  lines = s.splitlines()[1:]
  tmp = (layer1, layer2)
  merges = []
  for line in lines:
    content = line.strip().split(' ')
    na = int(content[0])
    pos = 1
    group = []
    for i in range(na):
      idx = int(content[pos])
      group.append(idx)
      pos += 1

    merges.append(cmisc.Attributize(group=group))
  return merges


def read_desc(desc_file):
  lines = open(desc_file, 'r').readlines()[1:]
  layers = defaultdict(lambda: [])
  by_id = {}

  for line in lines:
    content = line.strip().split()
    idx, typ, layer = int(content[0]), int(content[1]), int(content[2])
    res = Attributize(typ=typ, layer=layer, cell_name=content[3])
    pos = 4
    if typ == 1:
      tmp = list([int(x) for x in content[pos:]])
      tmp = np.reshape(tmp, (4, 2))
      res.box = Box().union_points(tmp)
    else:
      tmp = list([int(x) for x in content[pos:pos+2]])
      res.box = Box(tmp, tmp)
      res.text = content[-1]

    res.good = False
    tb = layers[layer]
    res.idx = idx
    assert idx == len(by_id), content
    by_id[idx] = res
    tb.append(res)
  return layers, by_id

def get_stats_filename(cell, runid, title):
  return cmisc.path_here(f'./stats/{title}.{cell}-{runid}.txt')


@Cachable.cachedf(fileless=False)
def compute_netlist(cell, runid, binary, desc_file, a, b):
  fname = get_stats_filename(cell, runid, 'netlist_%d_%d'%(a,b))
  args = '--extract_netlist  --params="{layer1: %d, layer2: %d}"' % (a, b)
  res = sp.check_output('%s %s > %s 2>/dev/null < %s' % (binary, args, fname, desc_file), shell=True).decode()
  return fname

def get_netlist(ctx, desc_file, a, b):
  fname= compute_netlist(ctx.cell, ctx.runid, ctx.binary, desc_file, a,b)
  res = open(fname, 'r').read()
  return parse_netlist(res, a, b)


def parse_gdsii():
  gdsii = gdspy.GdsLibrary()
  gdsii.read_gds(
      cmisc.
      path_here('./shiftreg_e7f285dccca5788b157d72e7fde31a92ed765c64ec86d56164426b7c1cde1625.gds2'),
  )
  return gdsii

@Cachable.cachedf(fileless=False)
def write_cell_desc(cell, runid):
  gdsii = parse_gdsii()
  cinfo = get_cell_info(gdsii.cell_dict[cell])
  data = dump_cell_info(cinfo)
  fname = get_stats_filename(cell, runid, 'desc_base')
  open(fname, 'w').write(data)
  return fname


@Cachable.cachedf(fileless=False)
def get_well_split_desc(cell, runid, binary, desc_file, circuit_desc):
  args = '--split_wells  --params="{gate: %d, well: %d}"' % (
      circuit_desc.gate, circuit_desc.n_or_p_layer
  )
  res = sp.check_output('%s %s 2>/dev/null < %s' % (binary, args, desc_file), shell=True).decode()
  fname = get_stats_filename(cell, runid, 'desc_split')
  open(fname, 'w').write(res)
  return fname


@Cachable.cachedf(fileless=False)
def get_wells_info_cached(cell, runid, binary, desc_file, circuit_desc):
  args = '--extract_wells_info  --params="{layer1: %d, layer2: %d}"' % (
      circuit_desc.n_or_p_layer, circuit_desc.nwell
  )
  fname = get_stats_filename(cell, runid, 'well_info')
  res = sp.check_output('%s %s > %s 2>/dev/null < %s' % (binary, args, fname, desc_file), shell=True).decode()
  return fname

def get_wells_info(ctx, desc_file):
  fname = get_wells_info_cached(ctx.cell, ctx.runid, ctx.binary, desc_file, ctx.circuit_desc)
  res = open(fname, 'r').read()
  wells_info = set(read_layer_info(res))
  return wells_info


@Cachable.cachedf(fileless=False)
def extract_norp_gate_edges_cached(cell, runid, binary, desc_file, circuit_desc):
  args = '--extract_netlist --only_edges  --params="{layer1: %d, layer2: %d}"' % (
      circuit_desc.n_or_p_layer, circuit_desc.gate
  )
  fname = get_stats_filename(cell, runid, 'gates_info')
  sp.check_output('%s %s > %s 2>/dev/null < %s' % (binary, args, fname, desc_file), shell=True).decode()
  return fname

def extract_norp_gate_edges(ctx, desc_file):
  fname = extract_norp_gate_edges_cached(ctx.cell, ctx.runid, ctx.binary, desc_file, ctx.circuit_desc)
  res = open(fname, 'r').read()
  lines = res.splitlines()[1:]
  res = []
  for line in lines:
    tmp = line.split()
    res.append((int(tmp[0]), int(tmp[1])))
  return res


@Cachable.cachedf(fileless=False)
def get_stats(cell, runid, binary, desc_file):
  res = sp.check_output('%s 2>/dev/null < %s' % (binary, desc_file), shell=True).decode()
  fname = get_stats_filename(cell, runid, 'stats')
  open(fname, 'w').write(res)
  return fname


class Transistor:

  def __init__(self, a, b, gate, is_npn=True):
    self.a = a
    self.b = b
    self.gate = gate
    self.is_npn = is_npn

  def blocking(self, gate_val):
    return int(self.is_npn) ^ int(gate_val)

  def __str__(self):
    return f'Transistor(a={self.a}, b={self.b}, gate={self.gate}, npn={self.is_npn})'


class Pin:

  def __init__(self, **kwargs):
    self.state = 0
    self.priority = 10
    self.fixed = False
    self.dbg = ''

    self.__dict__.update(kwargs)

  def update_state(self, state, priority):

    state_change = self.state != state
    any_changes = self.state != state or self.priority != priority
    self.state = state
    self.priority = priority
    return any_changes, state_change

  def __lt__(self, other):
    if self.priority > other.priority: return True
    if self.priority < other.priority: return False
    return not self.fixed and other.fixed

  def conflicts(self, other):
    if other is None: return False
    return self.state != other.state and self.fixed == other.fixed and self.priority == other.priority

  def __str__(self):
    return f'Pin(state={self.state}, priority={self.priority}, dbg={self.dbg})'


class PinState:

  def __init__(self, **kwargs):
    self.reset()
    self.__dict__.update(kwargs)

  def reset(self):
    self.nets = []
    self.state = 0
    self.priority = 10

  def update(self, pin):
    self.nets.append(pin)

  def compute(self):
    best = None
    conflict = False
    for e in self.nets:
      if e.conflicts(best): conflict = True
      elif best is None or best < e:
        best = e
        conflict = False

    assert not conflict
    return best.state, best.priority


class BaseSimulator:

  def __init__(self, transistors, node_to_labels):
    self.transistors = transistors
    self.node_to_labels = dict({k: list(v) for k, v in node_to_labels.items()})
    self.label_to_node = {}
    self.node_to_transistors = defaultdict(list)

    for node, labels in self.node_to_labels.items():
      assert len(labels) == 1
      self.label_to_node[labels[0]] = node
    assert len(self.label_to_node) == len(node_to_labels)

    self.net_rmp = cmisc.Remap()
    self.pins = dict()
    for transistor in self.transistors:
      for a in (transistor.a, transistor.b, transistor.gate):
        if not a in self.pins: self.pins[a] = Pin()
        self.net_rmp.get(self.pins[a])

      self.node_to_transistors[self.get(transistor.gate)].append(transistor)

    for k, v in self.label_to_node.items():
      self.get(v).dbg = k

    self.ALIM_PRIO = 0
    self.INPUT_PRIO = 1

    self.get('vdd').__dict__.update(state=1, priority=self.ALIM_PRIO, fixed=True)
    self.get('gnd').__dict__.update(state=0, priority=self.ALIM_PRIO, fixed=True)

  def get(self, x):
    x = self.norm(x)
    return self.pins[x]

  def norm(self, k):
    if isinstance(k, str): k = self.label_to_node[k]
    return k

  def compute(self, nsteps=-1, **kwargs):
    for k, v in kwargs.items():
      self.get(k).update_state(v, self.INPUT_PRIO)
    while True:
      if nsteps == 0: break
      nsteps -= 1
      if not self.compute_step(): break
      time.sleep(0.1)

  def compute_step(self):
    n = self.net_rmp.n
    uj = OpaGraph.UnionJoin(n)
    has_changes = False
    alims = defaultdict(list)

    for tr in self.transistors:
      if not self.is_tr_blocking(tr):
        a = self.get(tr.a)
        b = self.get(tr.b)
        if a.fixed: alims[b].append(a)
        elif b.fixed: alims[a].append(b)
        else: uj.join(self.net_rmp.get(a), self.net_rmp.get(b))

    for group in uj.groups():
      s = PinState()
      for e in group:
        v = self.net_rmp.rget(e)
        for alim in alims[v]:
          s.update(alim)
        s.update(v)
      nstate, nprio = s.compute()

      for e in group:
        v = self.net_rmp.rget(e)
        any_change, state_change = v.update_state(nstate, nprio)
        if state_change and v in self.node_to_transistors: has_changes = True
      if has_changes: break
    return has_changes

  def is_tr_blocking(self, tr):
    gate = self.get(tr.gate)
    return tr.blocking(gate.state)

  def __str__(self):
    return Display.disp(self.status(), num_size=0)

  def status(self):
    tb = {}
    for k, v in self.label_to_node.items():
      tb[k] = str(self.get(v))
    for i, v in self.pins.items():
      tb[str(i)] = str(v)
    return tb

  def status2(self):
    tb = {}
    for k, v in self.pins.items():
      tb[str(self.node_to_labels.get(k, [k])[0])] = v.state
    return Display.disp(tb, num_size=0)

  def get_netlist_colors(self):
    colors = []
    for k, v in self.pins.items():
      colors.append((k, 'rg' [v.state]))
    colors.sort()
    return list([x[1] for x in colors])

def compute_netlist_full(ctx, desc_file):
  stats_filename = get_stats(ctx.cell, ctx.runid, ctx.binary, desc_file)

  compute_connections = []
  stats = proc_stats(stats_filename)
  lines = set(ctx.circuit_desc.metal_connect + [ctx.circuit_desc.gate, ctx.circuit_desc.n_or_p_layer])

  for k, conn in stats.items():
    if not k in lines: continue
    for v in conn:
      compute_connections.append((k, v))

  for layer in lines:
    compute_connections.append((layer, layer))

  netlists = {}
  for a, b in compute_connections:
    netlist = get_netlist(ctx, desc_file, a, b)
    netlists[(a, b)] = netlist
    netlists[(b, a)] = netlist
  return netlists


def get_circuit(ctx):
  circuit_desc = ctx.circuit_desc

  assert ctx.binary
  desc_file = write_cell_desc(ctx.cell, ctx.runid)
  ndesc_file = get_well_split_desc(ctx.cell, ctx.runid, ctx.binary, desc_file, circuit_desc)
  wells_info = get_wells_info(ctx, ndesc_file)
  norp_gate_edges = extract_norp_gate_edges(ctx, ndesc_file)

  netlists = compute_netlist_full(ctx, ndesc_file)
  layers, by_id = read_desc(ndesc_file)
  pprint.pprint(netlists)

  netlist_layers = set()

  uj = algo.UnionJoin(len(by_id))
  for k, merges in netlists.items():
    netlist_layers.update(k)

    if circuit_desc.gate in k and circuit_desc.n_or_p_layer in k: continue
    for v in merges:
      if len(v.group) == 0: continue
      x0 = v.group[0]
      for x in v.group[1:]:
        uj.merge(x0, x)

  for v in layers[circuit_desc.n_or_p_layer]:
    v.is_n = not v.idx in wells_info

  groups = uj.get_groups()
  reprs = uj.get_clusters()

  repr_to_label = defaultdict(lambda: set())
  for lid in netlist_layers:
    layer = layers[lid]
    for v in layer:
      if v.typ == 0: repr_to_label[reprs[v.idx]].add(v.text)

  gate_to_well = [defaultdict(lambda: []), defaultdict(lambda: [])]
  print('Wells info >> ', wells_info)
  print('Norp gates >> ', norp_gate_edges)
  print('NRERPR >> ', len(groups))
  for a, b in norp_gate_edges:
    doping = by_id[a]
    gate_to_well[doping.is_n][b].append(doping.idx)

  transistors = []
  seen = set()
  for n_doping in (0, 1):
    for k, v in gate_to_well[n_doping].items():
      print(reprs[k], v, k)
      gate_repr = reprs[k]
      assert len(v) >= 2
      lst = set()
      for a in v:
        lst.add(reprs[a])
      lst = list(lst)
      lst.sort()

      print(k, v, lst, gate_repr)
      for i in range(len(lst)):
        for j in range(i):
          h = (lst[j], lst[i], gate_repr, n_doping)
          if h in seen: continue
          seen.add(h)
          transistors.append(Transistor(lst[j], lst[i], gate_repr, is_npn=n_doping))

  print('Gates >> ')
  for e in transistors:
    print(e)
  pprint.pprint(repr_to_label)
  for e in by_id.values():
    e.nodisplay= not e.layer in netlist_layers

  return Attributize(transistors=transistors, repr_to_label=repr_to_label, by_id=by_id, groups=groups,)

def build_circuit(ctx):
  data = get_circuit(ctx)

  def build_entry_to_color_map(colors):
    res = {}
    for color, group in zip(colors, data.groups):
      for e in group: res[e] = Color(color)
    return res

  if ctx.simulate:
    sim = BaseSimulator(data.transistors, data.repr_to_label)
    ninputs = 0
    for i in range(3):
      if not 'ABC' [i] in sim.label_to_node: break
      ninputs += 1
    if 'Q' in sim.label_to_node:
      print('start computation')
      sim.compute(D=0, CLK=0, nsteps=10)
      print(sim)
      if 0:
        maps = []
        for i in range(2):
          sim.compute(nsteps=1)
          colors = sim.get_netlist_colors()
          maps.append(build_entry_to_color_map(colors))
        disp_circuit(data.by_id, *maps)
        return

      sim.compute(D=1, CLK=0)
      print(sim.status2())

      sim.compute(D=0, CLK=0)
      print(sim.status2())

      sim.compute(D=0, CLK=1)
      print(sim.status2())
      sim.compute(D=1, CLK=1)
      print(sim.status2())

      sim.compute(D=1, CLK=0)
      print(sim.status2())

      sim.compute(D=1, CLK=1)
      print(sim.status2())
      sim.compute(D=0, CLK=1)
      print(sim.status2())

      sim.compute(D=0, CLK=0)
      print(sim.status2())

      sim.compute(D=1, CLK=0)
      print(sim.status2())

    elif ninputs == 1:
      for i in range(2):
        sim.compute(A=i)
        print(sim.status2())
    elif ninputs == 2:
      for i in range(2):
        for j in range(2):
          sim.compute(A=i, B=j)
          print(sim.status2())
    else:
      for i in range(2):
        for j in range(2):
          for k in range(2):
            sim.compute(A=i, B=j, C=k)
            print(sim.status2())

  if ctx.display_circuit:
    cmap = get_colormap('viridis')
    colors = cmap[np.linspace(0, 1, len(data.groups))]
    map1 = build_entry_to_color_map(colors)
    disp_circuit(data.by_id, map1)


@Cachable.cachedf(fileless=False)
def get_circuit_netlist(ctx):
  circuit_desc = ctx.circuit_desc
  assert ctx.binary
  desc_file = write_cell_desc(ctx.cell, ctx.runid)
  ndesc_file = get_well_split_desc(ctx.cell, ctx.runid, ctx.binary, desc_file, circuit_desc)
  wells_info = get_wells_info(ctx, ndesc_file)
  netlists = compute_netlist_full(ctx, ndesc_file)
  layers, by_id = read_desc(ndesc_file)

  netlist_layers = set()

  uj = algo.UnionJoin(len(by_id))
  for k, merges in netlists.items():
    netlist_layers.update(k)

    if circuit_desc.gate in k and circuit_desc.n_or_p_layer in k: continue
    for v in merges:
      if len(v.group) == 0: continue
      x0 = v.group[0]
      for x in v.group[1:]:
        uj.merge(x0, x)


  groups = uj.get_groups()
  reprs = uj.get_clusters()

  repr_to_label = defaultdict(lambda: set())
  for lid in netlist_layers:
    layer = layers[lid]
    for v in layer:
      k = v.idx
      if v.typ == 0: repr_to_label[reprs[k]].add((v.cell_name, v.text, v.idx))
  return repr_to_label


class CircuitEvaluate:
  def __init__(self, g, start_nodes, end_nodes, cells):
    self.g = g
    self.cells = cells
    self.start_nodes = start_nodes
    self.end_nodes = end_nodes
    self.order = list(nx.algorithms.dag.topological_sort(g))
    self.rorder = list(self.order)
    self.rorder.reverse()
    self.flip_flops = []
    for cid in self.order:
      cell = self.g.nodes[cid]['cell']
      if cell and cell.is_reg:
        self.flip_flops.append(cell)
    self.res = {}

    self.vals = {}
    for n in self.order:
      self.vals[n] = 0

    self.clk = self.start_nodes['clock']

  def disp_registers(self):
    res = []
    for cell in self.flip_flops:
      res.append(cell.data)
    print(Format(res).bit().v)

  def get_inner(self):
    return list(self.vals.values())

  def regs(self):
    res = []
    for v in self.flip_flops:
      res.append(v.data)
    return res

  def reset(self):
    self.set_inputs(reset_n=0)
    self.clock()
    self.clock()
    self.set_inputs(reset_n=1)
    self.compute()

  def set_inputs(self, **kwargs):
    for k, v in kwargs.items():
      self.vals[self.start_nodes[k]] = v

  def compute(self, gate=False):
    for n in [self.order, self.rorder][not gate]:
      c = self.g.node[n]['cell']
      if c is None: continue
      if gate ^ c.is_reg: c.compute(self.vals)
    for end_node, pid in self.end_nodes.items():
      self.res[end_node] = self.vals[pid]
    return self.res


  def compute2(self, target, vals):
    if target in vals: return vals[target]
    c = self.g.node[target]['cell']
    for pred in self.g.predecessors(target):
      self.compute2(pred, vals)
    c.compute(vals)
    return vals[target]


  def clock(self, **kwargs):
    self.set_inputs(**kwargs)
    #nvals = {}
    #for flip_flop in self.flip_flops:
    #  flip_flop.clock(self.vals, nvals)


    self.vals[self.clk] = 1
    self.compute(gate=True)
    self.compute(gate=False)
    self.vals[self.clk] = 0
    return self.compute(gate=True)



def disp_circuit(by_id, *map_to_col_list):
  canvas = vapp.Canvas(size=(800, 800), keys='interactive', title='Floating Pwn2Win Mask')
  gloo.set_viewport(0, 0, 800, 800)
  gloo.set_viewport(0, 0, canvas.size[0], canvas.size[1])
  gloo.set_state("translucent", depth_test=False)

  panzoom = PanZoomTransform(canvas, aspect=1)
  polys = PolygonCollection("agg", color="local", transform=panzoom)
  shift = np.zeros((1, 2))

  for colmap in map_to_col_list:
    nshift = np.zeros((1, 2))
    minp = np.zeros((1, 2))
    for entry in by_id.values():
      if entry.box.empty(): continue
      if entry.nodisplay: continue
      key = entry.idx
      if not key in colmap: continue

      points = np.concatenate((entry.box.poly() / 1e5 + shift, np.zeros((4, 1))), axis=1)
      nshift = np.maximum(nshift, np.amax(points, axis=0)[:2])
      minp = np.minimum(minp, np.amin(points, axis=0)[:2])
      polys.append(points, color=colmap[key].rgba)
    shift = (nshift - minp) * 1.1
    shift[0, 1] = 0
  polys.update.connect(canvas.update)

  @canvas.connect
  def on_draw(e):
    gloo.clear('white')
    polys.draw()

  @canvas.connect
  def on_resize(event):
    width, height = event.size
    gloo.set_viewport(0, 0, width, height)

  canvas.show()
  vapp.run()

def do_proc_stats(ctx):
  print(proc_stats(ctx.filename))


def debug_netlist(ctx):
  circuit_desc = ctx.circuit_desc
  assert ctx.binary
  desc_file = write_cell_desc(ctx.cell, ctx.runid)
  ndesc_file = get_well_split_desc(ctx.cell, ctx.runid, ctx.binary, desc_file, circuit_desc)
  wells_info = get_wells_info(ctx, ndesc_file)
  netlists = compute_netlist_full(ctx, ndesc_file)
  layers, by_id = read_desc(ndesc_file)

  netlist_layers = set()

  uj = algo.UnionJoin(len(by_id))
  s = 0
  for k, merges in netlists.items():
    s += len(merges)
    netlist_layers.update(k)

    if circuit_desc.gate in k and circuit_desc.n_or_p_layer in k: continue
    for v in merges:
      if len(v.group) == 0: continue
      x0 = v.group[0]
      for x in v.group[1:]:
        uj.merge(x0, x)

  for v in layers[circuit_desc.n_or_p_layer]:
    v.is_n = not v.idx in wells_info
  print(s)

  groups = uj.get_groups()
  reprs = uj.get_clusters()
  e = 150388
  for x in groups[reprs[e]]:
    print(x)


def do_read_desc(ctx):
  write_cell_desc(ctx.cell, ctx.runid)

def list_cells(ctx):
  gdsii = parse_gdsii()
  res = list(gdsii.cell_dict.keys())
  print(res)
  return res

def logic_table_to_map(table):
  mp = {}
  for input, output in table:
    assert len(output) == 1
    k1 = list(input.items())
    k1.sort()
    mp[tuple(k1)] = list(output.values())[0]
  return mp

def compute_logic_table(ctx):
  lsts = ['TVEG', 'EUCC', 'TMRO', 'CUWR', 'ZAGR', 'RGJP', 'DHEA', 'KZBF', 'SSNP', 'CNLZ']

  res = {}

  for cell in cmisc.filter_glob_list(lsts, ctx.cell_fmt, blacklist_default=False):
    print('processing ', cell)
    ctx.cell = cell
    data =get_circuit(ctx)

    sim = BaseSimulator(data.transistors, data.repr_to_label)
    ninputs = 0
    inputs = []
    outputs = []
    for pin_name in sim.label_to_node.keys():
      if pin_name in CELL_INPUTS:
        inputs.append(pin_name)
      elif pin_name in CELL_OUTPUTS:
        outputs.append(pin_name)
    print(inputs, outputs)


    table_data =[]
    for mask in range(2**len(inputs)):
      cur_in = {}
      for i, k in enumerate(inputs):
        cur_in[k] = mask >> i & 1
      sim.compute(**cur_in)

      cur_out = {k:sim.get(k).state for k in outputs}
      table_data.append((cur_in, cur_out))
    res[cell] = logic_table_to_map(table_data)

  return res

def build_design(ctx):

  repr_to_label = get_circuit_netlist(ctx)
  print('la')
  logics = dict()
  for k, v in ctx.cell_logic_desc.items():
    logics[k] = Attributize(op=karnaugh_simplify(v), table=v)


  cells_pins = defaultdict(list)
  cell_type_to_pinname = defaultdict(set)

  for pid, groups in repr_to_label.items():
    for cell, pname, idx in groups:
      cells_pins[cell].append((pid, pname, idx))

  cells = {}
  for cell_name, pins in cells_pins.items():
    c = Cell(cell_name, pins, logics)
    cells[c.cellid] = c
    for _, pname, idx in pins: cell_type_to_pinname[c.name].add(pname)

  for cell in cells.values():
    typ = cell_type_to_pinname[cell.name]
    assert typ == set(cell.pins_typ.keys())

  pid_to_pins = defaultdict(list)
  for cell in cells.values():
    for pid, name in cell.pin_to_name.items():
      pid_to_pins[pid].append((cell, name))

  for k, v in pid_to_pins.items():
    tmp = defaultdict(int)
    for u in v: tmp[u[1]] += 1
    assert (tmp['input'] == 0 and tmp['output'] == 0) or tmp['output'] == 1, v

  g = nx.DiGraph()
  for pid in repr_to_label.keys():
    g.add_node(pid, cell=None)

  for cell in cells.values():
    cell.node = None
    if len(cell.outputs) == 0: continue
    if cell.name == 'mkShiftReg': continue
    output0, = cell.outputs.values()
    cell.node = output0
    g.node[output0]['cell'] = cell

    for a in cell.inputs.values():
      g.add_edge(a, output0)


  start_nodes = []
  end_nodes = []
  for n, deg in g.in_degree():
    if deg==0:
      data = pid_to_pins[n]
      for cell, name in data:
        if cell.pins_typ[name] == 'alim':
          break
      else:
        start_nodes.append(n)

  for n, deg in g.out_degree():
    if deg==0:
      data = pid_to_pins[n]
      for cell, name in data:
        if cell.pins_typ[name] == 'alim':
          break
      else:
        end_nodes.append(n)





  starts = {}
  ends = {}
  print(start_nodes, end_nodes)
  for dest, src in ((starts, start_nodes), (ends, end_nodes)):
    for v in src:
      lst = []
      for cell, name in pid_to_pins[v]:
        if cell.name == ctx.cell: lst.append(name)
      assert len(lst) == 1, 'Fuu for %s'%v
      dest[lst[0]] = v

  ev = CircuitEvaluate(g, starts, ends, cells)


  cnt = 0
  for ff in ev.flip_flops:
    seen = set()
    q = deque()
    seen.add(ff.inputs['D'])
    q.append(ff.inputs['D'])
    print(len(seen))

    adj_cells = []
    while len(q)>0:
      a = q.popleft()
      for pred in g.predecessors(a):
        cell = g.node[pred]['cell']
        if not cell: continue
        if cell.is_reg:
          adj_cells.append(cell)
          break
        if pred in seen: continue
        seen.add(pred)
        q.append(pred)
    print(ff.node, adj_cells)
    assert len(adj_cells) <= 1
    cnt += len(adj_cells)
  print(cnt)




  seen = set()
  q = deque()
  seen.add(ends['unlocked'])
  q.append(ends['unlocked'])
  print(len(seen))

  adj_cells = []
  others = []
  while len(q)>0:
    a = q.popleft()
    for pred in g.predecessors(a):
      cell = g.node[pred]['cell']
      if not cell:
        others.append(pred)
        continue

      if cell.is_reg:
        adj_cells.append(cell)
        continue
      if pred in seen: continue
      seen.add(pred)
      q.append(pred)
  print(adj_cells, others)

  print(len(adj_cells), len(ev.flip_flops))
  inputs = list([z3.BitVec('x_%d'%i, 1) for i in range(len(ev.flip_flops))])
  vals = {}
  for ix, ff in enumerate(ev.flip_flops):
    vals[ff.node] = inputs[ix]

  res = ev.compute2(ends['unlocked'], vals)
  s = z3.Solver()
  s.add(res == 1)
  s.check()
  ans = []
  for ix in inputs:
    ans.append(s.model()[ix].as_long())
  ans = ans[::-1]

  passwd = bytes(Format(ans).bin2byte(lsb=False).v)
  print('GOT PASS >> ', passwd)


  tmp =[]
  ev.reset()
  ev.disp_registers()
  inputstr = Format(passwd).bitlist(bitorder_le=False).v

  for bit in inputstr:
    res = ev.clock(**{'in':bit})
    data = ev.regs()
    print(bit, res, Format(data).bit().v)
  ev.compute()
  print(ev.vals[ends['unlocked']])



def test_karnaugh(ctx):
  for k, table in ctx.cell_logic_desc.items():
    print('Processing logic ', k)
    op = karnaugh_simplify(table)

    print(op, type(op), pprint.pformat(table))
    for entry, val in table.items():
      entryv = dict(entry)
      nop = op.repl(entryv)
      print(nop, nop(), val)


def main():
  ctx = Attributize()
  ctx.circuit_desc = FileFormatHelper.Read(cmisc.path_here('./layers.desc.yaml'), mode='attr_yaml')
  ActionHandler.Run(ctx)


app()
