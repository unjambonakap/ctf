#!/bin/bash

#for webservmethod in GET POST PUT TRACE CONNECT OPTIONS PROPFIND PROPPATCH MKCOL COPY MOVE LOCK UNLOCK;
#do
#  printf "$webservmethod " ;
#  curl -X $webservmethod http://51.158.73.218:8880/index.php
#
#done

for webservmethod in GET HEAD POST OPTIONS HEAD HEAD;
do
curl  -v -X  $webservmethod -i 51.158.73.218:8880
done

