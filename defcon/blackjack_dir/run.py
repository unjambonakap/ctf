#!/usr/bin/python

import chdrft.utils as utils
import subprocess as sp
import pickle
import socket
from final_solver import Client, Player, ResponseType


def buildSeq():
    try:
        infile='blackjack'
        ofile='mod_blackjack'

        sp.check_call('cp ./%s ./%s'%(infile, ofile), shell=True)
        sp.check_call('chmod +x ./%s'%ofile, shell=True)

        sp.check_call('make appServer.so > /dev/null', shell=True)
        asm=utils.getDisassembly(['mov eax,8049f54h', 'jmp eax'])
        utils.patchFile(ofile, 0x8049f17, asm)

        sp.check_call('LD_PRELOAD=$PWD/appServer.so ./%s'%ofile, shell=True)
    finally:
        sp.call('killall %s >/dev/null 2>&1'%ofile, shell=True)



def execSeq():
    res=pickle.load(open('./dump_seq.txt', 'rb'))
    print res
    actions=[]
    for i in res['seq']:
        s='H'*i['numHit']
        if i['stand']:
            s+='S'
        x=abs(i['bet'])
        actions.append((x,s,False,i['bet']>0))

    with Client() as c:
        x=c.getNextMsg()
        assert x[0]==ResponseType.ASKNAME
        c.send(res['name'])

        p=Player(c, '', actions)
        p.setup()
        c.send('-1')
        s=c.s
        print s.recv(2048)
        c.send('ls')





if __name__=='__main__':
    mode=0
    if mode==1:
        buildSeq()
    else:
        execSeq()

