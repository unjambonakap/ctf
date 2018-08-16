#!/usr/bin/env python

import binascii

data='0 0 -1 3 0 0 2 1 1 0 1 0 0 -1 0 0 1 1 0 -1 1 0 1 1 0 1 1 0 0 0 1 1 0 1 0 0 1 0 1 1 0 0 0 1 0 1 1 1 0 0 0 1 0 1 1 1 0 1 0 0 0 0 1 1 0 0 0 1 1 0 1 1 0 1 1 1 1 1 0 1 0 0 2 0 0 0 1 1 0 1 0 1 0 0 1 1 0 1 1 0 1 0 1 1 0 1 0 0 1 0 1 1 0 0 0 1 1 0 1 1 0 -1 0 0 0 0 1 1 0 0 1 0 1 -1 0 0 1 1 1 0 0 1 1 1 0 1 0 0 0 0 1 1 0 0 1 1 0 1 1 1 0 1 1 1 1 0 1 1 0 0 0 1 1 0 1 1 0 1 1 1 1 1 0 1 0 0 0 1 0 0 1 1 0 0 1 1 1 0 1 1 0 1 0 0 0 0 1 1 0 1 1 1 1 1 0 1 0 1 0 2 1 1 0 1 0 0 1 0 0 1 1 1 0 0 0 1 0 1 1 1 0 1 1 0 0 1 1 1 0 0 1 1 1 0 1 1 0 1 0 1 0 0 1 1 0 0 0 1 1 0 -1 0 1'
tb=[int(x) for x in data.split(' ')]
tb=[max(0,min(1,x)) for x in tb]
n=len(tb)
s=sum([tb[i]<<(n-1-i) for i in range(n)])
s=sum([tb[i]<<i for i in range(n)])
print(binascii.a2b_hex(str(s)))
