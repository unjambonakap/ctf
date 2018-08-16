#!/usr/bin/env python


import sys
import subprocess as sp
import struct
import mmap
import array
import binascii
import elftools.elf.elffile as EF
import tempfile
import distorm3 as ds3

FILE='./custom_aerosol'

def setMode(mode):
    f=open('./solver_mode.in', 'wb')
    f.write(struct.pack('<I', mode))
    f.close()

def curPw():
    n=0x26
    x=bytearray('flag{x3a'+'a'*n)
    x=x[:n]
    x[n-1]='}'
    x[9]='6'
    x[13]='y'
    print len(x)
    return x


def getAssembly(code):
    f=tempfile.NamedTemporaryFile()
    f2=tempfile.NamedTemporaryFile()
    f.write('BITS 32\n')
    f.write(code)
    f.flush()

    sp.check_call('nasm %s -o %s'%(f.name, f2.name), shell=True)

    ops=None
    with open(f2.name, 'rb') as g:
        ops=g.read(100)
    return ops

def patchFile(fname, pos, patch):
    off=None
    vaddr=None
    sz=None

    ofile='mod_aerosol'
    sp.check_call('cp ./%s ./%s'%(fname, ofile), shell=True)

    with open(ofile) as f:
        elf=EF.ELFFile(f)
        for s in elf.iter_sections():
            if s.name=='.text':
                vaddr=s['sh_addr']
                off=s['sh_offset']
                sz=s['sh_size']



    assert off is not None
    with open(ofile, 'r+b') as f:
        mm=mmap.mmap(f.fileno(), 0)
        pos=pos-vaddr+off
        mm[pos:pos+len(patch)]=patch
        mm.close()
    return ofile



def doMode1():
    sp.check_call('./%s test'%(FILE), shell=True)


def doMode2():
    espOffset=0x28+5*4+0x1dc
    outAddr=0x804970e
    ops=['mov [esp+%d], ecx'%espOffset, 'mov ebx, %d'%outAddr, 'jmp ebx']
    ops=getAssembly('\n'.join(ops))
    ofile=patchFile(FILE, 0x80492dc, ops)
    print ofile
    sp.call('./%s test'%(ofile), shell=True)


def doMode3():
    espOffset=0x28+5*4+0x1dc
    outAddr=0x804970e
    patchAddr=0x804be76
    ops=['mov [esp+%d], eax'%espOffset, 'mov ebx, %d'%outAddr, 'jmp ebx']
    ops=getAssembly('\n'.join(ops))
    ofile=patchFile(FILE, patchAddr, ops)
    print ofile
    sp.call('./%s test'%(ofile), shell=True)


def doMode4():
    espOffset=0x28+5*4+0x1dc
    outAddr=0x804970e
    patchAddr=0x804c8e9
    ops=['mov [esp+%d], ecx'%espOffset, 'mov ebx, %d'%outAddr, 'jmp ebx']
    ops=getAssembly('\n'.join(ops))
    ofile=patchFile(FILE, patchAddr, ops)
    print ofile
    sp.call('./%s test'%(ofile), shell=True)





if __name__=='__main__':

    sp.check_call('make', shell=True)

    mode=4

    setMode(mode)
    if mode==1:
        doMode1()
    elif mode==2:
        doMode2()
    elif mode==3:
        doMode3()
    elif mode==4:
        doMode4()
    else:
        test()






