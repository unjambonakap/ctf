#!/usr/bin/python

from operator import indexOf;
import re;
import time;
import socket;
import sys;
from battleships import *;
from redbeard import *;

msgSuccess = ["Hahaha, is this your first sea-fight?!", "HrhrhrhrHrrrrrr!", "*Sing* 13 men on the dead man's chest, and a buddle of rum...","W0000ty!","rofl","You callin you'self mighty pirate? Hohohoho...","Still want your 500P?!","You better sail home while you can!"];
msgFail = ["GrrrrrRrrrRrr.","Must be the wind...","Uhm.","o_O","O_o","What-the...?!","Hahaha - this means nothing!","A lucky man you are.",":x","This can't be...","GrrrRrrrrRrrrrrrrrrrrrrrrrrrrrrrr.","There must be something wrong with me cannons."];

pos=0;
rem=14;
tb=[];
ration=3;
def nothing(s):
	global tb, pos;
	while True:
		d=s.recv(10240);
		if (not d):
			break;
		for l in d.split("\n"):
			l=l.rstrip();
			print "received "+l;
			if (l.startswith(">>>")):
				return 1;
			elif (l.startswith("Cap'n Redbeard> ")):
				l=l[l.index(">")+2:];
				for p, e in enumerate(msgSuccess):
					if (l.find(e)!=-1):
						tb.append((p, len(msgSuccess)));
				for p, e in enumerate(msgFail):
					if (l.find(e)!=-1):
						tb.append((p, len(msgFail)));
			elif (l.find("[i] Your opponent")!=-1):
				if (l.find(" hit ")!=-1 or l.find(" sunk ")!=-1):
					global rem;
					rem-=1;

				l=l[10:];
				tmp=l[l.index("[")+1:l.index("]")];
				a,b=tmp.split(",");
				if (pos%5>=ration):
					tb.extend([(int(a), 10), (int(b), 10)]);
				pos+=1;
			elif (l.find("You lost")!=-1):
				return 3;
	return 0;


server="pirates.fluxfingers.net";
port=2204;
name="TA_MAMAN";

s=socket.socket(socket.AF_INET, socket.SOCK_STREAM);
print "connecting\n";
s.connect((server, port));

print "connected\n";


nothing(s);
s.send(name);
nothing(s);

cnt=0;
while(rem>=5):
	print "REMAINING "+str(rem);
	s.send("0 0");
	nothing(s);
	cnt+=1;

print tb;





code="";
codea="nr=ni/30269.0 + nj/30307.0 + nk/30323.0; nr-=(int)nr;\n"; 
codeb="ni=(171*ni)%30269; nj=(172*nj)%30307; nk=(170*nk)%30323;\n";
for p, (a, b) in enumerate(tb):
	cond="if (%s!=(int)(nr*%s)) continue;\n"% (a, b);
	code+=codeb+codea+cond;

fd=open("bf.c", "r");
content=fd.read();
fd.close();
content=content.replace("//INSERT", code);
fd=open("res.c", "w");
fd.write(content);
fd.close();

os.system("gcc -O1 -O2 -lpthread res.c");
#os.system("./a.out");
p=os.popen("./a.out");
l=p.read();
p.close();
if (l==""):
	print "failed, dunno what, can't find seed";
	sys.exit(-1);

def findShoot(board):

	for ship in board.ships:
		if ship.alive:
			for field in ship.fields:
				if field.hit == False:
					return field;
	print "fail here\n";
	sys.exit(-1);


l=l.split("\n");
lb=l[0].split(" ");
la=[];
for e in lb:
	la.append(int(e));

print la;

#la=(8556, 14019, 30321);
player=ConsolePlayer("ur mom");
rb=CaptainRedbeard((3, 5), player, None);
#p1.setOpp(rb);
rb.rand.setstate((1, tuple(la), None));

rb.createBoard(10, [4,3,3,2,1,1]);
print rb.board.__str__();
print "\n\n\n\n";
print "rand", len(tb);
for i in range(len(tb)):
	rb.randInt(0, 1);
cntr=len(tb)+18;
rb.board.hit(Point(0, 0));

print rb.rand.getstate();
tb=[];
ret=0;
while not rb.board.lost():
	np=findShoot(rb.board);
	rb.board.hit(np);
	s.send("%d %d"%(np.x, np.y));
	ret=nothing(s);
	if (ret==3):
		print "LOST";
		sys.exit(-1);

while (ret!=1 and nothing(s)!=1):
	pass

for i in range(len(tb)):
	rb.randInt(0, 1);
	print rb.rand.getstate();
cntr+=len(tb);

print cntr;
print rb.rand.getstate();


ratio=4; pos=0;
rb.setHitRatio((4,5))
rb.createBoard(10, [4,3,3,2,1,1]);
print rb.board.__str__();
print "\n\n\n\n\n\n";
time.sleep(1);

res=0;
tb=[];
while not rb.board.lost():
	np=findShoot(rb.board);
	rb.board.hit(np);
	s.send("%d %d"%(np.x, np.y));
	ret=nothing(s);
	if (ret==3):
		print "LOST";
		sys.exit(-1);
	elif (ret==2):
		print "WON";
		break;


for i in range(len(tb)):
	rb.randInt(0, 1);



ratio=5; pos=0;
rb.setHitRatio((5,5))
rb.createBoard(10, [4,3,3,2,1,1]);
print rb.board.__str__();
tb=[];
while not rb.board.lost():
	np=findShoot(rb.board);
	rb.board.hit(np);
	s.send("%d %d"%(np.x, np.y));
	ret=nothing(s);
	if (ret==3):
		print "LOST";
		sys.exit(-1);
	elif (ret==2):
		print "WON";
		break;


nothing(s);


s.close();
