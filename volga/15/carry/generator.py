import struct
import math


class Generator:

    def __init__(self, q, init_state=1):
        assert (init_state != 0)
        self.q = q
        self.taps_mask = 0
        self.m = 0
        t = (q + 1) >> 1
        while t:
            self.taps_mask = (self.taps_mask << 1) | (t & 1)
            t >>= 1
            self.m += 1
        self.state = init_state & ((1 << self.m) - 1)
        self.c = 0

    def next_bit(self):

        def sum_all(l):
            acc = 0
            while l:
                acc += (l & 1)
                l >>= 1
            return acc

        self.c += sum_all(self.taps_mask & self.state)
        ret_bit = self.state & 1
        new_bit = self.c & 1
        self.c >>= 1
        self.state = (self.state >> 1) | (new_bit << (self.m - 1))
        return ret_bit

    def next_byte(self):
        byte = 0
        for i in xrange(8):
            byte |= self.next_bit() << 7 - i
        return byte

    def generate_gamma(self, length):
        gamma = [0 for i in xrange(length)]
        for i in xrange(length):
            gamma[i] = self.next_byte()
        return gamma


def encrypt(data, key):
    assert (len(key) == 8)
    assert (struct.unpack('<I', key[4:])[0] != 0)
    assert (struct.unpack('<I', key[:4])[0] != 0)
    state = struct.unpack('<I', key[:4])[0]
    q = struct.unpack('<I', key[4:])[0]
    generator = Generator(q, state)
    gamma = generator.generate_gamma(len(data))
    return ''.join([chr(ord(ch) ^ g) for ch, g in zip(data, gamma)])


def decrypt(data, key):
    return encrypt(data, key)


# check
def sanity_check():
    s = 'A' * 150
    key = '324dfwer'
    s_enc = encrypt(s, key)
    s_dec = decrypt(s_enc, key)
    assert (s == s_dec)


def sanity_check_detailed():
    print 'c  reg  a'
    generator = Generator(37, 0b10011)
    for i in xrange(20):
        print generator.c, bin(generator.state)[2:].zfill(
            5), generator.next_bit()
    print 'c reg a'
    generator = Generator(11, 0b001)
    for i in xrange(10):
        print generator.c, bin(generator.state)[2:].zfill(
            3), generator.next_bit()

#
# main
#

if __name__ == '__main__':
    key = '????????'
    with open('test.txt', 'rb') as f:
        test = f.read()
    with open('flag.png', 'rb') as f:
        flag = f.read()
    test_enc = encrypt(test, key)
    flag_enc = encrypt(flag, key)
    with open('test.txt.bin', 'wb+') as f:
        f.write(test_enc)
    with open('flag.png.bin', 'wb+') as f:
        f.write(flag_enc)
