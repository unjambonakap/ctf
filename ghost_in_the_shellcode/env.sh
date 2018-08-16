#!/bin/bash

DIR=$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )

workon env3
export PYTHONPATH=$DIR/install_local/python:$PYTHONPATH
export PATH=$DIR/install_local/bin:$PATH
