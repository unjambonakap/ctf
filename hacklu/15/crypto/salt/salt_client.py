#!/usr/bin/python3
import nacl
from nacl.public import Box, PublicKey, PrivateKey
import socket
import os
from binascii import hexlify

CMD_STORE = 0
CMD_LOOKUP = 1

server_pk = None
if 1:
  server_pk = PublicKey(
      b'0\xe8\xcfWx\xb7\xa4\x9aVy\xc7\x03\xe0\xa0\xf4\x8c\xb3\x9f\xebP\xc8\xb9\x8d\xa7<_uK\xf3Z\xc6x')
else:
  server_sk = PrivateKey(
      b'Q\xf2<\xf8F\xa3\x97i\x7f%p\xe2?\x85%\x9f\xba\xd3\xc5\x11\xd8D\x92\x97aw9\x97\x1e\xa5\xe1\xeb')


my_sk = PrivateKey.generate()
box = Box(my_sk, server_pk)


filename = hexlify(os.urandom(16)).decode('utf8')
contents = hexlify(os.urandom(32)).decode('utf8')
print('going to create file {0} with contents {1}'.format(filename, contents))


def do_request(command, data):
  data = '#'.join(data)
  nonce = nacl.utils.random(Box.NONCE_SIZE)
  nonce = bytes([nonce[0] & 0xFE]) + nonce[1:]  # see comment in server
  req = my_sk.public_key.encode() + bytes([command]) + box.encrypt(
      data.encode('utf8'), nonce)
  print('request: ', req)
  s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  s.connect(('localhost', 1512))
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


def test():
  print('result of STORE: <<<{0}>>>'.format(do_request(CMD_STORE,
                                                       (filename, contents))))
  print('result of LOOKUP: <<<{0}>>>'.format(do_request(CMD_LOOKUP,
                                                        (filename,))))


def get_data(test):
  req = None
  res = None

  if test:
    #going to create file ae5b207d43e19fe168c168477fb812a9 with contents bd6b1f3ecde7869862b32c025a95144b83a274b52441378de9eb2aed58b73db3

    req = b'h\x04\xcb\xad\x92\xcaH^\xd4\xd8\xa5\x14\x13w\xd8\x13<\x92\\e\x1bu\x8a\x04\xed\xf0\x15\x83Sd18\x01r&+\x05\\\xa2\x02\xe4\xbdJe"\x04p\xb0\x91\xbfp\x8c\xd8\xe8\x9b\x11fE\x01\xfc\xc1\x82}E\x07*\x07\x90e_Kq3\x89]\x17\xed\xcb\x1f\nM\x11\xe5U\x07>p\xe1\xbd\x9b\xdaL.\x1df\xc0`}!R!S\xcdpY'
    res = b's&+\x05\\\xa2\x02\xe4\xbdJe"\x04p\xb0\x91\xbfp\x8c\xd8\xe8\x9b\x11f\x12\xd8\xc1\xdc\xb1\x95\xfa\xdbQ\xda\xf9D\xc4\xa6l\x0b\'`\x98W\xdd<k\x8fS\x96\x06\x14\x01\xd0\xc4\xe1+\xdd\xe2\xa4\xdd\xf8\xd0\x05\xb7\xf6\xfb\x14v\x84\xe4\xd3q\xbf\xf9p\xd0C\xcf\x1f\xae\xe0\xc6\xd60\x02\xca\x1a[0\xc7\xe5%\xd0ah\x99\xbc\xc7\xd3\x05\x17\xb3x\x11'
  else:
    res = b"e\xc8\x9b\xc4\xfd\x04\x9b\x843a\x940U\xc4\x7fa\x11W\xa9uf\xa9\xf4%\r6C\x8d\xe1Z\x95\xb1^\x92\xddF\xa7\xbb\x86\x19\xbaCW\xde\x9bo\xd3Z\x8d\x85kx\x81a\xb0\x0b\xc9\x14'L\xc6i\xc4V\x86=\xba\x11~\xcc\x9bw#i\xc7\xb2\xc0Z\x9d\x1d\xb3\x96\\\xf9\xffG\x8a\xa2"
    req = b'\xa0f?u\xfb;AZf\xfc@{M!\xcdP\x92\xf6\x0f\xea\x1d\xad@\xc5\x8c\xd0R\xd8\xfdX81\x01d\xc8\x9b\xc4\xfd\x04\x9b\x843a\x940U\xc4\x7fa\x11W\xa9uf\xa9\xf4%w;`s[\xad\xa8V\x90\xe0w,\xb6<\xbd\xb1\xcbh=\x0b\x80\xba\xd8\x9bM\x17\xc6\x1f\x83<G\xcfV\x93\x00E\xe97\xcc\x9a.\xa1\xe6\x13\x11\xe9<\xae'
  return req, res


def solve():
  s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  s.connect(('149.13.33.84', 1512))

  req, res = get_data(0)
  req = bytearray(req)
  req[PublicKey.SIZE] = 0
  req = bytes(req)
  client_pk = req[:PublicKey.SIZE]
  cmd = req[PublicKey.SIZE]
  encrypted_data = req[PublicKey.SIZE + 1:]
  nonce = encrypted_data[:Box.NONCE_SIZE]

  known = b"you need to send more parameters! seriously, why would you just send one parameter? I should just let this fail with a silent error. sending just one parameter is stupid."

  s.sendall(req)
  s.shutdown(socket.SHUT_WR)

  resp = b''
  while True:
    buf = s.recv(2048)
    if len(buf) == 0:
      break
    resp += buf
  print(resp)
  data2 = resp[Box.NONCE_SIZE + 16:]
  print(data2)
  print(len(data2), len(known))
  data = res[Box.NONCE_SIZE + 16:]
  res = ''
  for i in range(len(data)):
    res += (chr(data2[i] ^ known[i] ^ data[i]))
  print(res)


if 1:
  solve()
else:
  test()
