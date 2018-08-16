#!/usr/bin/python

import time
import random
from signal import SIGTERM, SIGCHLD, signal, alarm

FLAG1 = ''
FLAG2 = ''


def cycleLen(data, place):
  seen = {}
  count = 0
  while not place in seen:
    seen[place] = 1
    count += 1
    place = data[place]
  return count


def realSign(data):
  res = 1
  for i in range(256):
    res *= cycleLen(map(ord, data), i)
  return res


import base64, SocketServer, os, sys, hashlib


class ServerHandler(SocketServer.BaseRequestHandler):

  def fail(self, message):
    print 'FAIL MOFO'
    self.request.sendall(message + "\n")
    self.request.close()

  def pow(self):
    proof = base64.b64encode(os.urandom(9))
    proof='a'*12
    self.request.sendall(proof)
    test = self.request.recv(20)
    ha = hashlib.sha1()
    ha.update(test)
    print(test, ha.digest())
    if test[0:12] != proof or not ha.digest().endswith('\x00\x00\x00'):
      self.fail("Bad proof of work.")

  def sign(self, invalid):
    data = base64.b64decode(self.request.recv(172))
    if len(data) != 128:
      self.fail("Bad data")
      return
    if data == invalid:
      self.fail("Same data")
      return
    self.request.sendall(str(realSign(self.SECRET + data)) + "\n")

  def check(self):
    for i in range(0x10):
      compare = os.urandom(128)

      self.request.sendall("You need to sign:\n")
      self.request.sendall(base64.b64encode(compare) + "\n")
      sig = int(self.request.recv(620))
      if sig != realSign(self.SECRET + compare):
        return False
    compare = ''.join(map(chr, range(128)))
    self.request.sendall("You need to sign:\n")
    self.request.sendall(base64.b64encode(compare) + "\n")
    sig = int(self.request.recv(620))
    return sig == realSign(self.SECRET + compare)

  def handle(self):
    #alarm(600)
    self.pow()
    print('GOGOGO DONE')
    self.SECRET = os.urandom(128)
    for i in range(0x10000):
      self.request.sendall(
          "\n1) Sign something\n2) Give me signiture of data\n")
      res=self.request.recv(2)
      op = int(res)
      if op == 1:
        self.sign('')
      elif op == 2:
        print i
        if self.check():
          print "CHAMPION"
          self.request.sendall(FLAG1)
          if i < 350:
            self.request.sendall(FLAG2)
        else:
          self.request.sendall("Failed signing\n")
        break
      else:
        self.fail("Bad option")
        break
    self.request.close()


class ThreadedServer(SocketServer.ForkingMixIn, SocketServer.TCPServer):
  pass


if __name__ == "__main__":
  HOST = sys.argv[1]
  PORT = int(sys.argv[2])

  FLAG1 = open('flag1.txt', 'r').read()
  FLAG2 = open('flag2.txt', 'r').read()
  server = ThreadedServer((HOST, PORT), ServerHandler)
  server.allow_reuse_address = True
  server.serve_forever()
