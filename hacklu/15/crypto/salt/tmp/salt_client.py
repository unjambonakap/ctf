#!/usr/bin/python3
import nacl
from nacl.public import Box, PublicKey, PrivateKey
import socket
import os
from binascii import hexlify

CMD_STORE = 0
CMD_LOOKUP = 1

server_pk = PublicKey(b'0\xe8\xcfWx\xb7\xa4\x9aVy\xc7\x03\xe0\xa0\xf4\x8c\xb3\x9f\xebP\xc8\xb9\x8d\xa7<_uK\xf3Z\xc6x')
my_sk = PrivateKey.generate()
box = Box(my_sk, server_pk)

filename = hexlify(os.urandom(16)).decode('utf8')
contents = hexlify(os.urandom(32)).decode('utf8')
print('going to create file {0} with contents {1}'.format(filename, contents))

def do_request(command, data):
  data = '#'.join(data)
  nonce = nacl.utils.random(Box.NONCE_SIZE)
  nonce = bytes([nonce[0] & 0xFE]) + nonce[1:] # see comment in server
  req = my_sk.public_key.encode() + bytes([command]) + box.encrypt(data.encode('utf8'), nonce)
  print('request: ', req)
  s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  s.connect(('149.13.33.84', 1512))
  s.sendall(req)
  s.shutdown(socket.SHUT_WR)

  resp = b''
  while True:
    buf = s.recv(2048)
    if len(buf) == 0:
      break
    resp += buf
  print('response: ', resp)
  plain_resp = box.decrypt(resp).decode('utf8')
  return plain_resp

print('result of STORE: <<<{0}>>>'.format(do_request(CMD_STORE, (filename, contents))))
print('result of LOOKUP: <<<{0}>>>'.format(do_request(CMD_LOOKUP, (filename,))))
