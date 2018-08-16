#!/usr/bin/python

from operator import indexOf;
import re;
import socket;
import sys;
from battleships import *;
from redbeard import *;

msgSuccess = ["Hahaha, is this your first sea-fight?!", "HrhrhrhrHrrrrrr!", "*Sing* 13 men on the dead man's chest, and a buddle of rum...","W0000ty!","rofl","You callin you'self mighty pirate? Hohohoho...","Still want your 500P?!","You better sail home while you can!"];
msgFail = ["GrrrrrRrrrRrr.","Must be the wind...","Uhm.","o_O","O_o","What-the...?!","Hahaha - this means nothing!","A lucky man you are.",":x","This can't be...","GrrrRrrrrRrrrrrrrrrrrrrrrrrrrrrrr.","There must be something wrong with me cannons."];

pos=0;
rem=14;
tb=[];
def nothing(s):
	global tb, pos;
	while True:
		for l in s.recv(10240).split("\n"):
			l=l.rstrip();
			print "received "+l;
			if (l.startswith(">>>")):
				return;
			elif (l.startswith("Cap'n Redbeard> ")):
				l=l[l.index(">")+2:];
				if (l in msgSuccess):
					tb.append((indexOf(msgSuccess, l), len(msgSuccess)));
				elif (l in msgFail):
					tb.append((indexOf(msgFail, l), len(msgFail)));
			elif (l.startswith("[i] Your opponent missed while shooting at") or l.startswith("[i] Your opponent hit a ship while shooting at ")):
				if (l.find("hit")):
					global rem;
					rem-=1;

				l=l[10:];
				tmp=l[l.index("[")+1:l.index("]")];
				a,b=tmp.split(",");
				if (pos%5>=3):
					tb.extend([(int(a), 10), (int(b), 10)]);
				pos+=1;
			elif (l.startswith("You lost")):
				sys.exit(-1);


server="pirates.fluxfingers.net";
port=2204;
name="TA_MAMAN";

#s=socket.socket(socket.AF_INET, socket.SOCK_STREAM);
#print "connecting\n";
#s.connect((server, port));
#
#print "connected\n";
#
#nothing(s);
#s.send(name);
#
#while(rem>=5):
#	print "REMAINING "+str(rem);
#	nothing(s);
#	s.send("0 0");
#
#print tb;
#
#
#s.close();
#
#
#
#

tb=[(2, 8), (1, 8), (6, 8), (2, 8), (6, 10), (1, 10), (3, 12), (1, 8), (0, 10), (7, 10), (6, 8), (3, 8), (2, 12), (2, 8), (6, 12), (7, 8), (0, 10), (3, 10), (6, 8), (0, 10), (4, 10), (3, 8), (9, 12)];

code="";
codea="nr=ni/30269.0 + nj/30307.0 + nk/30323.0; nr-=(int)nr;\n"; 
codeb="ni=(171*ni)%30269; nj=(172*nj)%30307; nk=(170*nk)%30323;\n";
for p, (a, b) in enumerate(tb):
	cond="if ((%s!=nr*%s) continue;\n"% (b, a);
	code+=codea+cond+codeb;
code+='printf("%d %d %d\\n", ni, nj, nk);\n';

fd=open("bf.c", "r");
content=fd.read();
fd.close();
content=content.replace("//INSERT", code);
fd=open("res.c", "w");
fd.write(content);
fd.close();


