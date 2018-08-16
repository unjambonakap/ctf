#!/bin/bash


rsync -avz -r ./gitzino_spark spark@localhost:~/prog/
ssh spark@localhost <<EOF
cd prog/gitzino_spark
mvn clean compile assembly:single
EOF
