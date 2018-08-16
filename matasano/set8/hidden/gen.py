#!/usr/bin/env python

from chdrft.main import app

global flags, cache
flags = None
cache = None

def args(parser):
  pass

def main():
  ex=range(57,65)
  for i in ex:
    h_fmt='''#pragma once
#include <matasano/ex_base.h>

OPA_NAMESPACE(matasano)

void ex_{i}();

OPA_NAMESPACE_END(matasano)
'''.format(i=i)

    c_fmt='''#include "matasano/ex_{i}.h"

OPA_NAMESPACE(matasano)

void ex_{i}(){{

}}

OPA_NAMESPACE_END(matasano)
'''.format(i=i)
    open('./src/ex_{i}.cpp'.format(i=i), 'w').write(c_fmt)
    open('./inc/matasano/ex_{i}.h'.format(i=i), 'w').write(h_fmt)


  pass

app()
