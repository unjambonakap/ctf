import socket
import sys
from Crypto.Cipher import AES
import binascii
import hashlib
import fibCrypt

IV = "0123456789ABCDEF"


def decrypt(text, passphrase):
  key = hashlib.sha256(passphrase).digest()
  aes = AES.new(key, AES.MODE_CBC, IV)
  return aes.decrypt(binascii.unhexlify(text))


def read_until(sock, end):
  s = ''
  while not s.endswith(end):
    s += sock.recv(1)
  return s


if __name__ == "__main__":
  HOST = sys.argv[1]
  PORT = int(sys.argv[2])

  sock = socket.socket()
  sock.connect((HOST, PORT))

  p = int(read_until(sock, "\n"))
  (key, secret) = fibCrypt.genKey(p)
  sock.sendall(str(key[0][0]) + "," + str(key[0][1]) + "\n")

  parts = read_until(sock, "\n").split(",")
  theirKey = (int(parts[0]), int(parts[1]))

  shared = fibCrypt.calcM(p, secret, theirKey)
  text = sock.recv(200)
  print decrypt(text[:-1], str(shared))
