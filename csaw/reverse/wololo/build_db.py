#!/usr/bin/python
import binascii
import struct

f=open('res.db', 'wb')


txt="""
ADMIN=1
USERNAME=captainfalcon
PASSWORD=fc03329505475dd4be51627cc7f0b1f1
ISAWESOME=1
"""
USERNAME="captainfalcon"
PASSWORD="fc03329505475dd4be51627cc7f0b1f1"

def writeHeader(f,t,s):
    tb=[0]*0x11
    tb[0]=t
    pos=1
    for i in s:
        tb[pos]=ord(i)
        pos+=1
    tb=[chr(x) for x in tb]
    f.write(''.join(tb))


f.write('WOLO')
numRows=4
f.write(struct.pack('<I', 1))
f.write(struct.pack('<H', 4))
f.write(struct.pack('<H', numRows))

writeHeader(f,5,"USERNAME")
writeHeader(f,6,"PASSWORD")
writeHeader(f,0,"ADMIN")
writeHeader(f,0,"ISAWESOME")

szMap={5:0x10, 6:0x20, 0:0x1}

def writeRow(f):
    tb=[0]*0x32

    startPos=0
    pos=startPos
    for i in USERNAME:
        tb[pos]=ord(i)
        pos+=1

    startPos+=0x10
    pos=startPos
    for i in PASSWORD:
        tb[pos]=ord(i)
        pos+=1

    startPos+=0x20
    pos=startPos
    tb[pos]=1
    pos+=1

    tb[0x31]=1

    tb=[chr(x) for x in tb]

    f.write(''.join(tb))

for i in range(numRows):
    writeRow(f)
f.close()


