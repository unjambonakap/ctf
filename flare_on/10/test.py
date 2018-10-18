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

    def __init__(self, read_data, prefix):
        super(Hooker, self).__init__()
        self.read_data = read_data
        self.done = False
        self.exited = False
        self.prefix = prefix
        setup_buf_bpt(read_data.read_buf, 0x30, False)
        setup_buf_bpt(read_data.read_buf + len(self.prefix), 2, True)
        disable_trace()
        self.ins = []
        self.ctx = 0

    def dbg_bpt(self, tid, ea):
        print('dbg break >> ', hex(ea))
        if ea == self.read_data.read_buf:
            pass
        elif ea == self.read_data.read_buf + len(self.prefix):
            print('starting trace')
            start_trace()
        elif ea == self.read_data.read_buf + len(self.prefix) + 1:
            self.done = True
            pass
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

    def dbg_trace(self, tid, ea):
        if ea >> 12 == 0x18f:
            self.ctx = 3
        if self.ctx == 0:
            return 1
        self.ctx -= 1

        idc.RefreshDebuggerMemory()
        idc.MakeUnknown(ea, 20, 0)
        idc.MakeCode(ea)
        mnem = idc.GetDisasm(ea)
        print(hex(ea), mnem)
        regs = 'eax ebx ecx edx esi edi eip'.split(' ')
        regs = {x: idc.GetRegValue(x) for x in regs}
        self.ins.append(Attributize(None, mnem=mnem, **regs))
        return 1

    def run(self):
        while not self.done:
            ida_continue()


def setup():
    path = 'C:/Users/benoit/work/loader.exe'
    for i in range(10):
        res = idc.StartDebugger(path, '', 'C:/Users/benoit/work')
        print('got res >> ', res)
        if res == 1:
            break
        idc.StopDebugger()
        time.sleep(1)
    else:
        assert False, 'Could not start debugger'
    wait_susp()
    # mov eax, 0; retn
    deb_override='\xb8\x00\x00\x00\x00\xc3'
    funcs = ida.find_imported_funcs('kernel32')
    deb_ea=funcs['IsDebuggerPresent'][0]
    deb_ea=idc.DbgDword(deb_ea)
    idc.DbgWrite(deb_ea, deb_override)


def main():

    start_ea = idc.LocByName('start')
    idc.AddBpt(start_ea)

    setup()


#run with
#import test as test; test=reload(test); test.main()
