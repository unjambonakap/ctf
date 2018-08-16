#!/usr/bin/python

import curses.ascii as ca
import sys


f=open('./weissman.csawlz', 'rb')
resF=open('./hash.htm', 'rb')

x=f.read()
sol=resF.read()
resF.close()
f.close()

normalPacket=0x13

charList={}
x=x[0x3c:]

l=len(x)
i=0

POS=0
l=10000

knownOp={}

knownOp[0xa]=2
knownOp[0x13]=0
knownOp[0xc]=2

def isControl(c):
    return ord(c) in knownOp



def rawText(i):
    s=""
    while not isControl(x[i]):
        if ca.isprint(x[i]):
            s+=x[i]
        else:
            s+='\\x%02x'%ord(x[i])
        i+=1
    return (s,i)


textPos=0
curText=""

fd=False
cntStep=0
cnt=0
lst=[]

while i<l:
    if fd:
        cntStep+=1
        if cntStep==2:
            print curText
            print sol[0:len(curText)]

            sys.exit(0)

    if not isControl(x[i]):
        print curText
        print ">> GOT %x"%ord(x[i])
        s=x[i:i+20]
        for j in s:
            print ord(j)
    assert isControl(x[i])
    v=ord(x[i])

    startOp=i+1
    opSize=knownOp[v]
    ops=[ord(u) for u in x[startOp:startOp+opSize]]
    i+=1
    i+=opSize

    if v==0x13:
        sz=9
        s=""
        for j in range(sz):
            s+=x[i+j]
        lst.append(s)
        print "POS >> %x"%POS, s
        curText+=s
        i+=sz

        if not curText==sol[0:len(curText)]:
            if cnt==2:
                print curText
                print "#######################"
                print sol[0:len(curText)+10]
                sys.exit(0)

        POS+=1
    #elif v==18:
    #    i+=knownOp[v]
    #    (s,i)=rawText(i)
    #    print "### 18 TEXT #### >> ",s
    #    opt=['%x'%ord(u) for u in x[i+1:i+lx+1]]
    #    print ">>>>>>>>>>>>>>>>>>>>> OPT v == %x, OPT "%v, ' '.join(opt)

    #    POS+=1
    elif v==0xa:
        #rel=ops[1]&0xf
        #n=ops[1]>>5

        print "ON 0xa >>> ", ops
        print "0xa >> ", ['%02x'%j for j in ops]
        #print ops
        #print len(lst), rel
        #pos=len(lst)-rel-1
        #print pos
        #txt=lst[pos-2:pos+2]
        #txt=txt[0:n+1]
        #curText+=txt
        cnt+=1

    elif v in knownOp:
        fd=True
        opt=['%x'%ord(u) for u in x[startOp:startOp+opSize]]
        print ">>>>>>>>>>>>>>>>>>>>> OPT v == %x, OPT "%v, ' '.join(opt)
        curText+='?????'

    #else:
    #    print "GOT >>> ", v
    #    disp=20
    #    for j in range(disp):
    #        print ord(x[i+j]),
    #    print ""
    #    print "TEXT"

    #    for j in range(disp):
    #        cc=x[i+j]
    #        if ca.isprint(cc):
    #            sys.stdout.write(cc)
    #    print ""
    #    break




