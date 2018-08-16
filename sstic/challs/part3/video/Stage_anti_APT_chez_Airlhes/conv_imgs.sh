set -e
BASE=$PWD

g++ -std=c++11 ./conv_img.cpp
BIN=$BASE/a.out

cd /tmp/imgs
function do_one {
  set -e
  $BIN $1 $1.tsf
  convert $1.tsf $1.png
}
export -f do_one
export BIN

ls *.p7 | parallel  do_one
