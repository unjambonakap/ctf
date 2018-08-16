#!/usr/bin/env python3
from nacl.public import Box, PublicKey, PrivateKey
import threading
import re
import socket

# private NaCl key
#from private_key import server_sk

server_sk = PrivateKey(
    b'Q\xf2<\xf8F\xa3\x97i\x7f%p\xe2?\x85%\x9f\xba\xd3\xc5\x11\xd8D\x92\x97aw9\x97\x1e\xa5\xe1\xeb')

CMD_STORE = 0
CMD_LOOKUP = 1


def connection_handler_(s):
  # receive input - for simplicity, you just send one command per TCP connection and then close the connection for writing
  print('waiting for input...')
  input = b''
  while True:
    buf = s.recv(2048)
    if len(buf) == 0:
      break
    input += buf
  print('input complete')

  # unpack the request (client_pk, command, encrypted_data (including nonce))
  client_pk = input[:PublicKey.SIZE]
  cmd = input[PublicKey.SIZE]
  encrypted_data = input[PublicKey.SIZE + 1:]
  nonce = encrypted_data[:Box.NONCE_SIZE]

  # client always uses nonces that start with 0, server always uses nonces that start with 1
  if (nonce[0] & 1) == 1:
    raise Exception('bad nonce')

  my_box = Box(server_sk, PublicKey(client_pk))
  plaintext = my_box.decrypt(encrypted_data)

  # the client already picked a random nonce for the request, so we can just increment it by one for the reply
  answer_nonce = bytes([nonce[0] + 1]) + nonce[1:]

  def reply(str):
    s.sendall(my_box.encrypt(str.encode('utf8'), answer_nonce))

  params = plaintext.decode('utf8').split('#')
  name = params[0]
  if not re.match('^[a-zA-Z0-9_]+$', name):
    return reply('evil filename detected, aborting!!!')
  path = 'notes/' + name

  if cmd == CMD_STORE:
    if len(params) < 2:
      return reply(
          "you need to send more parameters! seriously, why would you just send one parameter? I should just let this fail with a silent error. sending just one parameter is stupid.")
    content = params[1]
    with open(path, 'w') as f:
      print(content, file=f)
      return reply('note stored securely and successfully')
  elif cmd == CMD_LOOKUP:
    with open(path, 'r') as f:
      return reply(f.read())


def connection_handler(s):
  try:
    connection_handler_(s)
  finally:
    s.close()


ssock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ssock.bind(('0.0.0.0', 1512))
ssock.listen(16)

while True:
  clientsock, clientaddr = ssock.accept()
  threading.Thread(target=connection_handler, args=(clientsock,)).start()
