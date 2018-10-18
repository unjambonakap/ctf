#!/usr/bin/python

import idaapi
import idc
import idautils
import time
import struct
import chdrft.ida.common as ida
from curses.ascii import isprint
from chdrft.utils.misc import Attributize
import re
import chdrft.utils.ops as ops

start = 0x401c48


def wait_susp():
    while True:
        res = idc.GetDebuggerEvent(idc.WFNE_SUSP, -1)
        if res == idc.WFNE_NOWAIT:
            break


def go(addr):
    while True:
        idc.GetDebuggerEvent(idc.WFNE_CONT | idc.WFNE_SUSP, -1)
        if idc.GetRegValue('eip') == addr:
            break


def get_str(addr):
    s = ''
    n = 0x100
    while True:
        x = idc.DbgRead(addr, n)
        for j in range(len(x)):
            if ord(x[j]) == 0:
                s += x[:j]
                return s
        s += x
        addr += len(x)
    return s


def step():
    go(f1_addr)
    res = get_str(idautils.cpu.ebp)
    f = open('/tmp/res.out', 'a+')
    f.write(res)
    f.close()
    return res


def analyse_read():
    read_buf = idc.DbgDword(idautils.cpu.esp + 0x8)
    nread = idc.DbgDword(idautils.cpu.esp + 0xc)
    nread_out = idc.DbgDword(idautils.cpu.esp + 0x10)
    return Attributize(None, **locals())


def setup_buf_bpt(ptr, n, enable):
    for i in range(n):
        u = ptr + i
        if enable:
            idc.AddBptEx(u, 1, idc.BPT_RDWR)
        else:
            idc.DelBpt(u)


def stage2(data):
    read_data = analyse_read()
    ret_addr = idc.DbgDword(idautils.cpu.esp)
    idautils.cpu.esp += 0x14 + 4
    idautils.cpu.eip = ret_addr
    data += '\r\n'
    idc.DbgWrite(read_data.read_buf, data)
    idc.DbgWrite(read_data.nread_out, struct.pack('<I', len(data)))

    return read_data


def disable_trace():
    idc.EnableTracing(idc.TRACE_INSN, 0)


def start_trace():
    idc.ClearTraceFile('')
    idc.EnableTracing(idc.TRACE_INSN, 1)
    idc.SetStepTraceOptions(idc.ST_OVER_LIB_FUNC)


def ida_continue():
    idc.GetDebuggerEvent(idc.WFNE_CONT, 0)


class Hooker(idaapi.DBG_Hooks):

    def __init__(self, item):
        super(Hooker, self).__init__()
        self.done = False
        self.exited = False
        self.cond_ea = idc.LocByName('fill_main') + 260
        self.item = item

        final_ea = idc.LocByName('finalize_write_file') - 0x00D01CF0
        fill_main_ea = idc.LocByName('fill_main') - 0xd015d0
        self.fill_obj = 0x00D0176A + fill_main_ea
        self.fill_ret = 0x00D018C9 + fill_main_ea
        self.choose_item = 0x00D01DB4 + final_ea
        self.file_ea = 0x00D01EE6 + final_ea

        idc.AddBpt(self.fill_obj)
        idc.AddBpt(self.fill_ret)
        idc.AddBpt(self.choose_item)
        idc.AddBpt(self.file_ea)
        self.res_val = None

    def dbg_bpt(self, tid, ea):
        #if ea == self.cond_ea:
        #    self.done = True
        #    self.res_val = idc.DbgDword(idautils.cpu.esi)
        print('ON >> ', hex(ea), 'want ', hex(self.fill_obj))

        if ea == self.fill_obj:
            idc.DbgWrite(idautils.cpu.edx + 0x638, struct.pack('<I', 0xc0000000))
            idc.DbgWrite(idautils.cpu.edx, open('/tmp/data.out', 'rb').read())
            idautils.cpu.eip = self.fill_ret
            print('JUMPING')

        elif ea == self.choose_item:
            idautils.cpu.eax = self.item

        elif ea == self.file_ea:
            buf = idc.DbgRead(idautils.cpu.edi, idautils.cpu.esi)
            x = open('/tmp/chall11_out_%d.out' % self.item, 'wb')
            x.write(buf)
            x.close()

            self.done = 1
        return 0

    def dbg_process_exit(self, pid, tid, ea, code):
        print('exited >> ', pid, tid, ea, code)
        self.exited = True

    def off(self):
        idc.StopDebugger()
        print('gogo exit')

        while not self.exited:
            idc.GetDebuggerEvent(idc.WFNE_ANY, 1)

        self.unhook()

    def run(self):
        while not self.done:
            ida_continue()


def stop_debugger():
    idc.StopDebugger()
    print('gogo exit')

    while not self.exited:
        idc.GetDebuggerEvent(idc.WFNE_ANY, 1)


def setup(num):
    path = 'C:/Users/benoit/work/CryptoGraph.exe'
    for i in range(10):
        res = idc.StartDebugger(path, str(num), 'C:/Users/benoit/work')
        print('got res >> ', res)
        if res == 1:
            break
        idc.StopDebugger()
        time.sleep(1)
    else:
        assert False, 'Could not start debugger'
    wait_susp()


def solve(num):

    print('\n\n')
    setup(num)

    h = Hooker()
    assert h.hook()
    h.run()
    h.off()
    print('for %d got %d' % (num, h.res_val))
    if h.res_val == 0:
        print('found for ', num)
        return True
    return False
#('0x18fdc0', 'mov     ah, [esp+ebx+0B4h]')
#('0x18fdc7', 'retn')
#('0x18fdc4', 'xor     al, ah')
#('0x18fdc6', 'retn')
#('0x18fdc0', 'mov     cl, [esp+ebx+88h]')
#('0x18fdc7', 'retn')
#('0x18fdc4', 'cmpxchg bl, dl')
#('0x18fdc7', 'retn')
#('0x18fdc4', 'cmpxchg bl, dl')
#('0x18fdc7', 'retn')
#('0x18fe9c', 'mov     ebx, large fs:30h')
#('0x18fea3', 'retn')


def main():

    idc.AddBpt(start)
    if 0:
        tb = []
        for i in range(256):
            if solve(255 - i):
                tb.append(i)
            print('CURRENT IS >> ', tb)

        print('results are >> ', tb)
    else:

        for i in range(0x10):
            print('GOING FOR >> ', i)
            setup(205)
            h = Hooker(i)
            assert h.hook()
            h.run()
            h.off()
            time.sleep(1)

#run with
#import test as test; test=reload(test); test.main()
