#!/usr/bin/env python

from chdrft.cmds import CmdsList
from chdrft.main import app
from chdrft.utils.cmdify import ActionHandler
from chdrft.utils.misc import Attributize
import chdrft.utils.misc as cmisc
import glog
from chdrft.tube.connection import Connection
import numpy as np

from sklearn.datasets import make_hastie_10_2
from sklearn.ensemble import GradientBoostingClassifier

global flags, cache
flags = None
cache = None


def args(parser):
  clist = CmdsList().add(test)
  ActionHandler.Prepare(parser, clist.lst)


def test(ctx):
  print('on test')
  with Connection('finale-docker.rtfm.re', 6969) as conn:
    def recv_profile():
      content = conn.recv_until('\n\n').decode()
      data = []
      for line in content.split('\n'):
        pos =  line.find(': ')
        if pos == -1: continue
        rem = line[pos+2:]
        if rem == 'oui':
          rem = 1
        elif rem == 'non':
          rem = 0
        else: rem = float(rem)
        data.append(rem)
      return data

    train = []
    for i in range(1500):
      train.append(recv_profile())
    train = np.array(train)
    train_y =  train[:,-1]
    train_x =  train[:,:-1]

    print(train_y)
    clf = GradientBoostingClassifier(n_estimators=100, learning_rate=1.0,
                                     max_depth=2, random_state=0).fit(train_x, train_y)
    #sigsegv{I_L0v3_Tent4cl3s}


    for i in range(500):
      u = recv_profile()
      res= clf.predict(np.array(u)[None,:])
      conn.send('NO'[int(res[0])] + '\n')
    conn.interactive()




def main():
  ctx = Attributize()
  ActionHandler.Run(ctx)


app()
