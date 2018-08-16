# coding: utf-8

from pyDes import *
a=des("ABCdefgh", ECB, pad=None)
a.encrypt('aaaaaaaa')
