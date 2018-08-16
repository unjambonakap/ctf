import math
from pyasn1.type import namedtype, univ
from pyasn1.codec.ber import decoder, encoder

class Parameters(univ.Sequence):
    componentType = namedtype.NamedTypes(
        namedtype.NamedType('N', univ.Integer()),
        namedtype.NamedType('Q', univ.Integer()),
        namedtype.NamedType('a', univ.BitString())
    )

class PublicKey(univ.BitString): pass

class SecretKey(univ.BitString): pass

class Ciphertext(univ.Sequence):
    componentType = namedtype.NamedTypes(
        namedtype.NamedType('pub', univ.BitString()),
        namedtype.NamedType('enc', univ.BitString())
    )

def bitstring_to_ints(b, q):
    def pack(bits):
        x = 0
        for bit in bits:
            x = (x << 1) | bit
        return x
    elembits = int(math.ceil(math.log(q) / math.log(2)))
    if len(b) % elembits != 0:
        raise Exception('Bad number of bits in bitstring')
    return [pack(b[i:i+elembits]) for i in xrange(0, len(b), elembits)]

def ints_to_bitstring(b, q):
    def unpack(bits, x, nbits):
        for i in xrange(nbits-1, -1, -1):
            bits.append(int(x & (1 << i) != 0))
    elembits = int(math.ceil(math.log(q) / math.log(2)))
    bits = []
    for x in b:
        unpack(bits, x, elembits)
    return bits
