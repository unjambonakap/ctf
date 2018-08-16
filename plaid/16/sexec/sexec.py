from cryptography.exceptions import InvalidTag
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from twisted.internet.protocol import Factory, ProcessProtocol
from twisted.internet import reactor
from twisted.protocols.basic import NetstringReceiver
import asn1
import numpy as np
import os
import random
import struct
import json

rand = random.SystemRandom()

def uniform(n, lower=-5, upper=5):
    return np.array([rand.randint(lower, upper) for _ in xrange(n)], dtype=np.int)

def op(a, b):
    c = np.fft.ifft(np.fft.fft(a, a.size * 2) * np.fft.fft(b, b.size * 2)).real
    return (c[0:a.size] - c[a.size:]).astype(np.int)

def parse_pk(s, q):
    return asn1.bitstring_to_ints(asn1.decoder.decode(s, asn1Spec=asn1.PublicKey())[0], q)

def parse_sk(s, q):
    return asn1.bitstring_to_ints(asn1.decoder.decode(s, asn1Spec=asn1.SecretKey())[0], q)

class Parameters(object):
    def __init__(self, param):
        if isinstance(param, str):
            param = asn1.decoder.decode(param, asn1Spec=asn1.Parameters())[0]
            self.N = int(param.getComponentByName('N'))
            self.Q = int(param.getComponentByName('Q'))
            self.a = np.array(asn1.bitstring_to_ints(param.getComponentByName('a'), self.Q))
        else:
            self.N, self.Q, self.a = param
        if len(self.a) != self.N:
            raise Exception('Parameter a is wrong size')

    def encode(self):
        param = asn1.Parameters()
        param.setComponentByName('N', self.N)
        param.setComponentByName('Q', self.Q)
        param.setComponentByName('a', asn1.ints_to_bitstring(self.a, self.Q))
        return asn1.encoder.encode(param)

class ShellProcessProtocol(ProcessProtocol):
    def __init__(self, onData, onError):
        self.outReceived = onData
        self.errReceived = onData
        self.outConnectionLost = lambda: onError()
        self.processEnded = lambda x: onError()

class Shell(NetstringReceiver):
    @property
    def iv(self):
        return self.iv1 + struct.pack('>I', self.iv2)

    def connectionLost(self, reason):
        if self.process:
            try:
                self.process.transport.signalProcess('KILL')
                self.process.transport.loseConnection()
            except:
                pass
            try:
                self.process_timer.cancel()
            except:
                pass
            self.process = None
            self.process_timer = None

    def connectionMade(self):
        self.process = None
        self.secret = uniform(4, 0, 255).astype(np.uint8)
        self.secret_bits = np.unpackbits(self.secret)
        self.aes_key = ''.join([chr(x) for x in self.secret]) + '\x00\x01\x02\x03\x04\x05\x06\x07\x08\x09\x0A\x0B'

        sk = uniform(self.factory.param.N)
        print sk, self.factory.pk, self.factory.param.a, self.factory.param.N, self.factory.param.Q
        pub = op(self.factory.param.a, sk) + uniform(self.factory.param.N)
        print self.secret, self.secret_bits
        enc = op(self.factory.pk, sk) + uniform(self.factory.param.N) + (self.secret_bits * (self.factory.param.Q / 2))
        pub %= self.factory.param.Q
        enc %= self.factory.param.Q
        d=dict(secret=list(self.secret_bits), q=self.factory.param.Q, pk=list(self.factory.pk), sk=list(sk), a=list(self.factory.param.a), enc=list(enc), pub=list(pub))
        nd=dict()
        for k,v in d.items():
          if isinstance(v, list):
            v=[int(x) for x  in v]
          nd[k]=v
        json.dump(nd, open('/tmp/params', 'wb'))

        ct = asn1.Ciphertext()
        ct.setComponentByName('pub', asn1.ints_to_bitstring(pub, self.factory.param.Q))
        ct.setComponentByName('enc', asn1.ints_to_bitstring(enc, self.factory.param.Q))
        self.sendString(asn1.encoder.encode(ct))

        self.iv1 = os.urandom(12)
        self.iv2 = 0
        self.sendString(self.iv1)

    def stringReceived(self, data):
        if len(data) < 4:
            self.transport.loseConnection()
            return
        tag = data[:4]
        data = data[4:]
        decryptor = Cipher(algorithms.AES(self.aes_key), modes.GCM(self.iv, tag, min_tag_length=4), default_backend()).decryptor()
        self.iv2 += 1
        try:
            data = decryptor.update(data) + decryptor.finalize()
        except InvalidTag:
            self.transport.loseConnection()
            return

        if self.process is None:
            self.process = ShellProcessProtocol(self.sendString, self.transport.loseConnection)
            reactor.spawnProcess(self.process, data, [data], {})
            self.process_timer = reactor.callLater(5, lambda: self.connectionLost(None))
            return
        else:
            self.process.transport.write(data)
            return

    def processError(self, err):
        self.transport.loseConnection()

class ShellFactory(Factory):
    protocol = Shell
    
    def __init__(self, param, pk):
        self.param = param
        self.pk = np.array(pk)

if __name__ == '__main__':
    import sys
    param = Parameters(open(sys.argv[1]).read())
    pk = parse_pk(open(sys.argv[2]).read(), param.Q)

    reactor.listenTCP(9999, ShellFactory(param, pk))
    reactor.run()
