#!/bin/bash

set -eu

export DIR=$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )
export ROOT_DIR=/home/benoit/programmation

function do_one {
  set -eu
  num=$1; shift
  echo "Processing $num"
  { time $ROOT_DIR/build/matasano/set8/matasano/set8_sample_main.cpp --ex $num ; } > $DIR/output_$num.txt 2>&1
  echo "Done processing $num"
}


function main {
  set -eu
  pushd $ROOT_DIR
  #waf -v --prefix=~/opt_opa --build=release --out=./build configure install --targets=matasanoset8main
  popd

  pushd $DIR

  export -f do_one
  do_one 65
  #seq 57 64 | parallel -I{} "do_one {}"
  popd
}
main "$@"

