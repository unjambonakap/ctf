#!/usr/bin/env python

from chdrft.cmds import CmdsList
from chdrft.main import app
from chdrft.utils.cmdify import ActionHandler
from chdrft.utils.misc import Attributize
import chdrft.utils.misc as cmisc
import glog
from chdrft.tube.connection import Connection
import re
import numpy as np

global flags, cache
flags = None
cache = None


def args(parser):
  clist = CmdsList().add(test)
  ActionHandler.Prepare(parser, clist.lst)


def test(ctx):
  with Connection('finale-docker.rtfm.re', 10000) as conn:

    data =conn.recv_until('Your actual')
    m = re.search('width : ([0-9]+) - height : ([0-9]+)', data.decode())
    width = int(m.group(1))
    height = int(m.group(2))
    print(width, height)

    res = conn.recv_until('>')
    m = re.search('x : ([0-9]+) - y : ([0-9]+)', res.decode())
    x = int(m.group(1))
    y = int(m.group(2))
    mp = -np.ones((width, height), dtype=int)


    def get_new(action):
      conn.send(action + '\n')
      res = conn.recv_until(')').decode()
      m  =re.search('\(([0-9]+) - ([0-9]+)\)', res)
      x = int(m.group(1))
      y = int(m.group(2))
      return res.find('OK -') != -1, x, y

    vx = [-1,1,0,0]
    vy = [0,0,1,-1]
    mp[x,y] = 0
    vs = 'WENS'
    q = [[x,y,0,-1]]
    while len(q) > 0:
      x,y,i,prev = q[-1]
      if i == 4:
        q.pop(len(q)-1)
        assert get_new(vs[prev^1])
        continue

      q[-1][2] += 1
      nx,ny = x+vx[i], y+vy[i]
      if mp[nx,ny] != -1: continue
      ok, ex, ey = get_new(vs[i])
      if ok:
        print(ex, ey)
        assert ex==nx and ey == ny
        mp[nx,ny] = 0
        q.append([nx,ny,0,i])
      else:
        mp[nx,ny] = 1
  go(x,y)





def main():
  ctx = Attributize()
  ActionHandler.Run(ctx)


app()
