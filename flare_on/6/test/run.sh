#!/bin/bash


arm-linux-androideabi-g++ -mthumb -march=armv7-a -g -pie -fPIC -fPIE libvalidate.so ./test.cpp

adb push ./a.out /data/local
adb push ./libvalidate.so /data/local
adb push ./flag /data/local
echo "DONE PUSH, go for <$1>" 1>&2
cmd="
#setrlimit 4 -1 -1
#mkdir /data/core 
#echo /data/core/%e.%p /proc/sys/kernel/core_pattern 

cd /data/local

export LD_LIBRARY_PATH=\$PWD 
chmod 777 ./a.out

./a.out < flag
exit \$?
"
adb shell <<EOF
$cmd
EOF

