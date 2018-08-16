#!/usr/bin/env python

from chdrft.utils.misc import path_from_script, cwdpath
import opa.crypto as crypto
from curses.ascii import isalnum, islower


pass_db = path_from_script(__file__, '../../data/crackstation-human-only.txt')
pass_db = '/usr/share/dict/cracklib-small'

fil = path_from_script(
    __file__,
    './dogecrypt-b36f587051faafc444417eb10dd47b0f30a52a0b')

#fil = '/tmp/test.abc'


with open(fil, 'rb') as f:
    content = f.read()
content = content[12:]


x = crypto.Cracker()
mode = crypto.ZipState()
checker = crypto.AsciiChecker()

x.set_state(mode)
x.set_content(content)
x.set_checker(checker)

charset = ' '
for y in range(0, 128):
    c = chr(y)
    if islower(c):
        charset += c

#x.do_bruteforce(charset, 4)


x.do_dictionary(pass_db)
