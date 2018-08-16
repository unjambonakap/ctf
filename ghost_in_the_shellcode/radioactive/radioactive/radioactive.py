#!/usr/bin/env python

import os
import sys
import pwd
import socket
import SocketServer
from Crypto.Cipher import AES
from Crypto import Random
import binascii

class RadioactiveServer(SocketServer.ForkingMixIn, SocketServer.TCPServer):
    allow_reuse_address = True

class RadioactiveHandler(SocketServer.BaseRequestHandler):
    def handle(self):
        key = open("secret", "rb").read()
        #drop_privs()
        cipher = AES.new(key, AES.MODE_ECB)

        self.request.send("Waiting for command:\n")
        tag, command = self.request.recv(1024).strip().split(':')
        print 'recv ',tag,command
        command = binascii.a2b_base64(command)
        pad = "\x00" * (16 - (len(command) % 16))
        command += pad

        blocks = [command[x:x+16] for x in xrange(0, len(command), 16)]
        print blocks
        cts = [str_to_bytes(cipher.encrypt(block)) for block in blocks]
        print cts

        command = command[:-len(pad)]

        t = reduce(lambda x, y: [xx^yy for xx, yy in zip(x, y)], cts)
        t = ''.join([chr(x) for x in t]).encode('hex')

        print t
        match = True
        for i, j in zip(tag, t):
            if i != j:
                match = False

        del key
        del cipher

        if match:
            eval(compile(command, "script", "exec"))
        else:
            self.request.send("Checks failed!\n")

        return


def main():

    HOST, PORT = "0.0.0.0", 4324
    server = RadioactiveServer((HOST, PORT), RadioactiveHandler)

    server.serve_forever()

    return

def drop_privs():
    pw = pwd.getpwnam("dragons")

    try:
        os.setgid(pw[3])
        os.setuid(pw[2])
        os.setegid(pw[3])
        os.seteuid(pw[2])
        os.chdir(pw[5])
    except OSError:
        sys.exit(-2)

    return

def str_to_bytes(x):
    return [int(ord(y)) for y in x]

if __name__ == '__main__':
    main()
