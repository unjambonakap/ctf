#!/usr/bin/env python

from chdrft.utils.binary import X86Machine, patch_file


x=X86Machine(0)
a=x.get_disassembly('mov eax, 0x80495d5; jmp eax')
patch_file('./cryptoserv', 0x8049575, a)
