#!/usr/bin/env python

from chdrft.utils.binary import ArmCompiler, patch_file
from chdrft.utils.misc import cwdpath
import sys
import subprocess as sp
import re

sol = """Should_hav:'g0ne_to_tashi_$tatio"""
sol = """Should_hav"""

for i in range(len(sol) // 2, 0x17):

    x = ArmCompiler()
    data = x.get_assembly('cmp r1, #%d' % (i + 1))
    patch_file('./libvalidate.so', 0xf8a, data)

    open('./flag', 'w').write(sol)

    res = sp.check_output([cwdpath('run.sh'), sol]).decode()
    m = re.search('SOL IS <<(.*)>>', res)
    print('got res >> ', res)
    assert m
    sol = m.group(1)
