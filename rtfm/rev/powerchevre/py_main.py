#!/usr/bin/env python

from chdrft.cmds import CmdsList
from chdrft.main import app
from chdrft.utils.cmdify import ActionHandler
from chdrft.utils.misc import Attributize
import chdrft.utils.misc as cmisc
import glog
import binascii

global flags, cache
flags = None
cache = None


def args(parser):
  clist = CmdsList().add(test)
  ActionHandler.Prepare(parser, clist.lst)


def test(ctx):
  print('on test')
  tb = 'chien;chat;loup;louis;hack;chevre;brebis;sqli;blind;aslr;pown;powershell;Microsoft;rand;list;pro;louve;lion;lionne;got;python;perl;c;java;cobol;cisco;pizza;hell;enfer;hacker;discord;hackathon;enfant;chinois;russe;poutine;trump;alfresco;sharepoint;jee;ropchain;mignon;sexy;slurp;infauxsec;initialiser;ok;non;oui;pied;chaussure;lit;chaise;fauteuil;table;sql;mongodb;mysql;oracle;avion;voiture;moto;suzuki;bmw;ordinateur;gsm;cyber;digital;damso;vald;orelsan;infected;shell;ouai;apple;linux;arch;maki;sushi;biere;houblon;Coucou;Louis;Roi;Renne;Fanfreluche;socket;chaussette;Celestin;brocante;brebis;soupe;chou;levre;baiser;embrasser;dormir;boire;jean;moulin;harry;potter;ecole;sorcier'.split(';')
  #tb = {x:i for x,i in enumerate(tb)}
  content = 'NjM2ODY5NjU2RTc2MzY4NjE3NDM2QzZGNzU3MDZDNkY3NTY5NzM2Njg2MTYzNkI5NjM2ODY1NzY3MjY1NjI3MjY1NjI2OTczNjczNzE2QzY5NzYyNkM2OTZFNjQ2MTczNkM3Mjc3MDZGNzc2RTM3MDZGNzc2NTcyNzM2ODY1NkM2QzRENjk2MzcyNkY3MzZGNjY3NDY3MjYxNkU2NDU2QzY5NzM3NDcwNzI2RjY2QzZGNzU3NjY1NzZDNjk2RjZFNkM2OTZGNkU2RTY1NzY3NkY3NDY3MDc5NzQ2ODZGNkU3MDY1NzI2Qzc2M0I2QTYxNzY2MTYzNkY2MjZGNkM1NjM2OTczNjM2RjA3MDY5N0E3QTYxNjg2NTZDNkMzNjU2RTY2NjU3MjA2ODYxNjM2QjY1NzI2NDY5NzM2MzZGNzI2NDc2ODYxNjM2QjYxNzQ2ODZGNkU3NjU2RTY2NjE2RTc0NjM2ODY5NkU2RjY5NzMzNzI3NTczNzM2NTM3MDZGNzU3NDY5NkU2NTc0NzI3NTZENzA1NjE2QzY2NzI2NTczNjM2RjI3MzY4NjE3MjY1NzA2RjY5NkU3NDZBNjU2NTQ3MjZGNzA2MzY4NjE2OTZFMzZENjk2NzZFNkY2RTczNjU3ODc5NjczNkM3NTcyNzA4Njk2RTY2NjE3NTc4NzM2NTYzNjk2RTY5NzQ2OTYxNkM2OTczNjU3MkU2RjZCODZFNkY2RTZGNzU2OTU3MDY5NjU2NDY2MzY4NjE3NTczNzM3NTcyNjU2QzY5NzQ3NjM2ODYxNjk3MzY1MjY2NjE3NTc0NjU3NTY5NkM3NDYxNjI2QzY1MzczNzE2QzM2RDZGNkU2NzZGNjQ2MjZENzk3MzcxNkM0NkY3MjYxNjM2QzY1NjYxNzY2OTZGNkU3NjZGNjk3NDc1NzI2NTM2RDZGNzQ2RjA3Mzc1N0E3NTZCNjk2MjZENzc3NkY3MjY0Njk2RTYxNzQ2NTc1NzIyNjc3MzZENjM3OTYyNjU3MjU2NDY5Njc2OTc0NjE2QzA2NDYxNkQ3MzZGNzY2MTZDNjQzNkY3MjY1NkM3MzYxNkUwNjk2RTY2NjU2Mzc0NjU2NDczNjg2NTZDNkM3NkY3NTYxNjk3NjE3MDcwNkM2NTZDNjk2RTc1NzgzNjE3MjYzNjgzNkQ2MTZCNjk3Mzc1NzM2ODY5NTYyNjk2NTcyNjUyNjg2Rjc1NjI2QzZGNkU0MzZGNzU2MzZGNzU0NEM2Rjc1Njk3Mzg1MjZGNjk1MjY1NkU2RTY1MzQ2NjE2RTY2NzI2NTZDNzU2MzY4NjUzNzM2RjYzNkI2NTc0NjM2ODYxNzU3MzczNjU3NDc0NjUzNDM2NTZDNjU3Mzc0Njk2RTE2MjcyNkY2MzYxNkU3NDY1NjI3MjY1NjI2OTczNDczNkY3NTcwNjVDNjM2ODZGNzU2QzY1NzY3MjY1NTYyNjE2OTczNjU3MkY2NTZENjI3MjYxNzM3MzY1NzI2NDZGNzI2RDY5NzIyNjI2RjY5NzI2NTE2QTY1NjE2RTZENkY3NTZDNjk2RTc2ODYxNzI3Mjc5RDcwNkY3NDc0NjU3Mg=='
  import base64


  def find_longuest(x):
    cnds = []
    print(x)
    for i, a in enumerate(tb):
      if x.startswith(a.encode()):
        cnds.append((len(a), i, a))
    return max(cnds)[1:]



  res =base64.b64decode(content)

  ans = []
  i = 0
  while len(res) != 0:

    print(res)
    c, now = find_longuest(binascii.unhexlify(res[:30]))

    res = res[2*len(now) :]
    if i%3 !=2:
      ans.append(res[0])
      res = res[1:]
    i += 1
    if len(ans)%2==0:
      print(binascii.unhexlify(bytearray(ans)))


  print(res)
  



def main():
  ctx = Attributize()
  ActionHandler.Run(ctx)


app()
