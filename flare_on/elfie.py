#!/usr/bin/python

import idc
import idautils
import time
import struct

func_start = 0x40108c
func_end = 0x4010d9

f1_addr=0x401680


def go(addr):
    while True:
        idc.GetDebuggerEvent(idc.WFNE_CONT | idc.WFNE_SUSP, -1)
        if idc.GetRegValue('eip')== addr:
            break

def get_str(addr):
    s=''
    n=0x100
    while True:
        x=idc.DbgRead(addr, n)
        for j in range(len(x)):
            if ord(x[j])==0:
                s+=x[:j]
                return s
        s+=x
        addr+=len(x)
    return s

idc.AddBpt(f1_addr)
def step():
    go(f1_addr)
    res=get_str(idautils.cpu.ebp)
    f=open('/tmp/res.out', 'a+')
    f.write(res)
    f.close()
    return res

