#!/usr/bin/python
from scapy.all import *;
from subprocess import *;
from hashlib import md5;
from struct import pack,unpack

p = rdpcap('bottle')
for i in range(30):
	if not p[i].haslayer(DNS):
		continue
	if DNSQR in p[i]:
		if DNSRR in p[i] and len(p[i][DNSRR].rdata)>0: # downstream/server
			print "S[%i]: %r" % (i,p[i][DNSRR].rdata)
		else: # upstream/client
			print "C[%i]: %r" % (i,p[i][DNSQR].qname)



#tb=[ord('D'), 0x03, 0xc5, 0xe9, 0x01];
#challenge=tb[0:4];
#p=Popen(["./a.out", "aegpumiplhhpz12ynd1efljwlkjcgwy.pirate.sea."], stdout=PIPE);
#res=p.stdout.read();
#res=res[1:17].encode("hex");
#print res;
#
#t="swordfish".ljust(32, chr(0));
#print md5(("".join(chr(ord(t[i])^challenge[i%4]) for i in range(len(t))))).digest().encode("hex");
#
#
