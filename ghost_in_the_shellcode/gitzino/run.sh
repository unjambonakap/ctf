#!/bin/bash

preload=$PWD/build/gitzino/libgitzino.so 
exe=$PWD/gitzino/gitzino

set -eu
action=$1

if [[ $action == "gdb" ]]; then
    gdb -ex "set environment LD_PRELOAD=$preload" \
        -ex "b *0x8049598" \
        $exe

        #-ex "b *0x8048e73" \
        #-ex "b *0x8048e3f" \
        #-ex "b *0x8048e57" \

elif [[ $action == "run" ]]; then
    LD_PRELOAD=$preload $exe

elif [[ $action == "run2" ]]; then
    gdb -ex "" \
        -ex "b *0x8049598" \
        -ex "b *0x80498e2" \
        -ex "b *0x80498d1" \
        -ex "r" \
        $exe
else
    echo "invalid action"
fi;
