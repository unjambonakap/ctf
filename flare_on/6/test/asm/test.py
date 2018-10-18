#!/usr/bin/env python

from chdrft.utils.binary import ArmCompiler
x=ArmCompiler()
res=x.get_assembly(['ldr r1, [r2]; ldr r2, [r5]', 'add r2, #0'])
