#!/usr/bin/python

import idc
import idautils
import time
import struct

func_start = 0x40108c
func_end = 0x4010d9


def go(addr):
    while idc.GetRegValue('eip')!= addr:
        idc.GetDebuggerEvent(idc.WFNE_CONT | idc.WFNE_SUSP, -1)


idc.AddBpt(func_end)
idc.AddBpt(func_start)

go(func_end)

n = 0x25
buf_addr = idc.DbgDword(idautils.cpu.ebp + 0xc)
data_addr = idc.DbgDword(idautils.cpu.ebp + 0x8)
len_addr = idautils.cpu.ebp + 0x10
assert idc.DbgWrite(len_addr, struct.pack('<I', n))

print 'steaaart', hex(buf_addr)
res = ''
for i in range(n):

    for c in range(256):
        assert idc.DbgWrite(buf_addr + i, chr(c)) == 1
        idc.RefreshDebuggerMemory()
        idautils.cpu.eip=func_start
        go(func_end)
        if idautils.cpu.edi != data_addr + n - i:
            print 'FOUND ONE', c
            print 'have ', hex(idautils.cpu.edi), hex(data_addr + n - i)
            res += chr(c)
            break
    else:
        assert 0
    print 'on %d: %s' % (i, res)
