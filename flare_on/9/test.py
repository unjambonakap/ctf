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
    path = 'C:/Users/benoit/work/you_are_very_good_at_this.exe'
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

    funcs = ida.find_imported_funcs('kernel32')
    print(funcs)

    read_addr = funcs['ReadFile'][0]
    print('read addr >> ', read_addr)
    read_pos = idc.DbgDword(read_addr)

    idc.AddBpt(read_pos)
    print('read pos bpt >> ', hex(read_pos))

    go(read_pos)


def solve(prefix):

    nc = 'a'
    test_buf = prefix + nc + 'aabc'
    setup()
    read_data = stage2(test_buf)

    h = Hooker(read_data, prefix)
    assert h.hook()
    h.run()
    h.off()

    data = Attributize()
    for i in range(len(h.ins)):
        x = h.ins[i]
        m = x.mnem
        if re.search('mov\s+ah, ', m):
            data.char = h.ins[i + 1].eax
        elif re.search('xor\s+al, ', m):
            data.xor = True
        elif re.search('mov\s+cl, ', m):
            data.rol_ins = h.ins[i + 1]
        elif re.search('cmpxchg bl, dl', m):
            data.cmp_ins = x
            break

    ah = (data.char >> 8 & 0xff)
    al = (data.rol_ins.eax) & 0xff
    assert data.xor
    assert al ^ ah == ord(nc)
    cl = (data.rol_ins.ecx) & 0xff
    al = ops.rol(al, cl, 8)

    assert al == (data.cmp_ins.eax & 0xff)
    bl = data.cmp_ins.ebx & 0xff
    need = ops.ror(bl, cl, 8) ^ ah
    assert isprint(need)
    return chr(need)

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
    res = 'Is_th1s_3v3'

    nx = 0x30
    nx = len(res) + 20
    for i in range(len(res), nx):
        print('trying for ', res)
        need = solve(res)
        res += need
        print('FOUND NEW CHAR >> ', need, res)
        time.sleep(0.5)

#run with
#import test as test; test=reload(test); test.main()
