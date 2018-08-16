#!/usr/bin/env python

from asq.initiators import query


cnd=open('./stage1.txt', 'r').readlines()
dico=open('/usr/share/cracklib/cracklib-small', 'r').readlines()


dico=query(dico).select(lambda x: x.strip()).where(lambda x: x.islower() and x.isalpha()).select(lambda x: x.upper()).to_list()

for _a in cnd:

    a=_a.strip()
    for b in dico:
        if b.endswith(a):
            print('match ', b)

