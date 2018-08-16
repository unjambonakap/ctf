#!/usr/bin/python

import base64, SocketServer, sys
from Crypto.Cipher import AES
import binascii
import hashlib
import fibCrypt

FLAG = ""
IV = "0123456789ABCDEF"


def encrypt(message, passphrase):
  key = hashlib.sha256(passphrase).digest()
  aes = AES.new(key, AES.MODE_CBC, IV)
  message += "\x00" * (16 - len(message) % 16)
  return binascii.hexlify(aes.encrypt(message))


class ServerHandler(SocketServer.BaseRequestHandler):

  def handle(self):
    p = fibCrypt.genPrime(8)

    self.request.sendall(str(p) + "\n")
    (key, secret) = fibCrypt.genKey(p)
    self.request.sendall(str(key[0][0]) + "," + str(key[0][1]) + "\n")

    parts = self.request.recv(200).split(",")
    theirKey = (int(parts[0]), int(parts[1]))

    shared = fibCrypt.calcM(p, secret, theirKey)
    mess = encrypt(FLAG, str(shared))
    self.request.sendall(mess + "\n")
    self.request.close()


class ThreadedServer(SocketServer.ForkingMixIn, SocketServer.TCPServer):
  pass


if __name__ == "__main__":
  HOST = sys.argv[1]
  PORT = int(sys.argv[2])

  FLAG = open('flag.txt', 'r').read()
  server = ThreadedServer((HOST, PORT), ServerHandler)
  server.allow_reuse_address = True
  server.serve_forever()
