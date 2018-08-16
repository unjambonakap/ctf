#!/usr/bin/env python


import concurrent.futures
from chdrft.utils.libc import LibcDatabase
import struct
import os, sys
import chdrft.utils.fingerprinting as fingerprinting



def libc_exact_compare(pattern, libc_db):
    results = []
    num_workers = 30
    with concurrent.futures.ThreadPoolExecutor(max_workers=num_workers) as executor:
        for f in os.listdir(libc_db.libc_dir):
            if not f.endswith('.so'):
                continue
            libc_file = os.path.join(libc_db.libc_dir, f)

            def f(libc_file, pattern):
                res = fingerprinting.libc_match(libc_file, pattern)
                return (res, libc_file)
            results.append(executor.submit(f, libc_file, pattern))
    for i in results:
        success, libc = i.result()
        if success:
            print('found >> ', libc)

def main():

    offsets={}
    if 0:
        offsets['fflush']=0xf75935c0
        offsets['fgets']=0xf75938d0
        offsets['puts']=0xf7595370
        offsets['__libc_start_main']=0xf754b570
        offsets['snprintf']=0xf757cd50
    else:
        offsets['fflush']=0xf7688f30
        offsets['fgets']=0xf7689220
        #offsets['puts']=0xf7595370
        offsets['__libc_start_main']=0xf763f970
        offsets['snprintf']=0xf7672c10

    fil='./tmp/lib32/libc.so.6'
    fil='/usr/lib32/libc.so.6'
    fil='./tmp2/lib32/libc-2.19.so'

    res = fingerprinting.libc_match(fil, offsets)
    print(res)
    return


    libc_dir = '/home/benoit/server2/libcs'
    with LibcDatabase(libc_dir) as libc_db:
        libc_exact_compare(offsets, libc_db)

main()
