#!/usr/bin/python
import pickle;
import numpy;

f=open("f", "r");



x=pickle.load(f);

print x[2];
f.close();

