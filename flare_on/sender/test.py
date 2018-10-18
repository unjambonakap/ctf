#!/usr/bin/env python

import scapy.all as x
import re
import binascii

def main():
    reader=x.rdpcap('../challenge.pcap')

    data=b''

    for a in reader:
        r=a[x.TCP].payload
        r=bytes(r)
        if not r.startswith(b'POST'):
            continue


        data+=r[-4:]


    data=bytearray(data)
    for i in range(len(data)):
        if chr(data[i]).islower() or chr(data[i]).isupper():
            data[i]^=0x20


    res=binascii.a2b_base64(data)
    open('key.txt', 'wb').write(res)

    tb=[102, 108, 97, 114, 101, 98, 101, 97, 114, 115, 116, 97, 114, 101, 102, 108, 97, 114, 101, 98, 101, 97, 114, 115, 116, 97, 114, 101, 102, 108, 97, 114, 101, 98]
    res=bytearray(res)
    print(res)
    for i in range(len(tb)):
        res[i]=(res[i]-tb[i])%256
    print(res)


    open('key2.txt', 'wb').write(res)

if __name__=='__main__':
    main()
