#!/usr/bin/env python

import scapy.all as scapy
from chdrft.utils.misc import DictWithDefault
from chdrft.crypto.common import XorpadSolver
from chdrft.utils.cache import CacheDB


fil = './pillowtalk.pcap'
x = scapy.rdpcap(fil)
data = []
for packet in x:
    if packet[scapy.TCP].flags & 0x8:
        data.append(bytearray(bytes(packet[scapy.TCP].payload)))

text = [data[i] for i in range(3, len(data), 2)]

print('start here')

with CacheDB() as cache:
    solver = cache.get_cachable('xorpad', XorpadSolver, text)
    solver.solve()



    #0  hi?
    #1  `id`?
    #2  yeah, like i'd system everything out?
    #3  %x%x%x%s%s%s%s%s%n%n%n%n%n%n%n%n%n?
    #4  0x4141414141414141?
    #5  woot, looks like im all finished here then?
    #6  so, the point of this challenge is to make someone siS?tJA"I?wnh?dehBdO alz  xt?t J?Wick ZER?OZ?Kssf
    #7  pad whats??
    #8  do you understand??
    #9  computers? yes sometimes. crypto? nope?
    #012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678
    #0         1         2         3         4         5         6         7         8         9         0         1         2         3         4
    #0
    #10  so, the problem with this service is it reuses the saJO ZK"?Asy ?ano?yEu cwntdpGewQSL mgpBAD?NL?Xe ?NH Zrm?BZLx?PyNzZfLX?VHT Dt zxZexEyzC vaxeUHVSn?bHWh ?   ??
    #11  maybe i need to re-re-watch http://www.youtube.com/waSIh?RmuoTfmGv-TIo
    #12  maybe?
    #13  or maybe i will just watch this one in loop for hours?YiLG5?Cb eY wjT HettsrtxeXpm??Twy yEQBXXLZOymCWMtAu Z?zX E? JUcDZ
    #14  don't distract me, I'm trying to make a challenge!?
    #15  too late! you know you are already watching it?
    #16  damnit, that awesome video and hotfuzz being on bbcamBXiAEpBEa?
    #17  the top comment on that video is "No penises were harJOd????Cx xBe fLkCng yftdyEswCMOm RrvVxBNLN?bh?S?wCoqEXU?qCAe?qAz?KZRK?gUo oiA z?qg?wcw aS?BUoBc???
    #18  The key is: WhyDoFartsSmell?SoTheDeafCanEnjoyThemAlso?
    #19  \xc3?
    #012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678
    #0         1         2         3         4         5         6         7         8         9         0         1         2         3         4
    #0
    #20  clever, right? I hope the pcap worked.?
