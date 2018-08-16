#!/usr/bin/python
import os;
import random;


for i in range(10000):
	print random.WichmannHill(os.urandom(32))._seed[2];


