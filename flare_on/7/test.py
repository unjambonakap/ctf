#!/usr/bin/env python
import binascii

a0 = [31, 100, 116, 97, 0, 84, 69, 21, 115, 97, 109, 29, 79, 68, 21, 104, 115,
      104, 21, 84, 78]
print('a0 >>', ''.join(map(chr, a0)))

a1 = [
    87, 97, 114, 110, 105, 110, 103, 33, 32, 84, 104, 105, 115, 32, 112, 114,
    111, 103, 114, 97, 109, 32, 105, 115, 32, 49, 48, 48, 37, 32, 116, 97, 109,
    112, 101, 114, 45, 112, 114, 111, 111, 102, 33
]

print('a1 >>', ''.join(map(chr, a1)))

a2 = [
    80, 108, 101, 97, 115, 101, 32, 101, 110, 116, 101, 114, 32, 116, 104, 101,
    32, 99, 111, 114, 114, 101, 99, 116, 32, 112, 97, 115, 115, 119, 111, 114,
    100, 58, 32
]

print('a2 >>', ''.join(map(chr, a2)))
a3 = [
    89, 32, 85, 32, 116, 97, 109, 112, 101, 114, 32, 119, 105, 116, 104, 32,
    109, 101, 63
]

print('a3 >>', ''.join(map(chr, a3)))
a4 = [
    85, 115, 101, 32, 116, 104, 101, 32, 102, 111, 108, 108, 111, 119, 105, 110,
    103, 32, 101, 109, 97, 105, 108, 32, 97, 100, 100, 114, 101, 115, 115, 32,
    116, 111, 32, 112, 114, 111, 99, 101, 101, 100, 32, 116, 111, 32, 116, 104,
    101, 32, 110, 101, 120, 116, 32, 99, 104, 97, 108, 108, 101, 110, 103, 101,
    58, 32
]
print('a4 >>', ''.join(map(chr, a4)))

a5 = [
    84, 104, 97, 110, 107, 32, 121, 111, 117, 32, 102, 111, 114, 32, 112, 114,
    111, 118, 105, 100, 105, 110, 103, 32, 116, 104, 101, 32, 99, 111, 114, 114,
    101, 99, 116, 32, 112, 97, 115, 115, 119, 111, 114, 100, 46
]
print('a5 >>', ''.join(map(chr, a5)))
