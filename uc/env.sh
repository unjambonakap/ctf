#!/bin/bash

DIR=$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )

workon env3
export PYTHONPATH=$PYTHONPATH:$DIR/build/python
