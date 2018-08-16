#!/usr/bin/bash

if [ $# -lt 2 ]; then
    #echo "need 2 args";
    exit 2;
fi;

curl  127.0.0.1:8080/test?file=$1\&signature=$2 2>/dev/null| grep -E "^1$" &>/dev/null

if [ $? -eq 0 ]; then
    exit 0;
fi;
exit 1;
