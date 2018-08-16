#!/usr/bin/env python

#do recv >>  187 >> b"Congratulations! You have won $53687091200!\nHoly shit you have a lot of money.
#Here's a flag: i_think_casinos_are_kinda_dumb\nHow much money would you like to bet? (You have $53687091200)\n"

from Crypto.PublicKey import RSA, DSA
from Crypto.Random import random, atfork
from Crypto.Cipher import PKCS1_OAEP
import Crypto
import binascii
import sys
from chdrft.tube.process import Process
from chdrft.tube.connection import Connection
from chdrft.utils.misc import PatternMatcher
import re
import time

_server_pub_enc = RSA.importKey(
    '-----BEGIN PUBLIC KEY-----\nMIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQDGRrsdIqf8K39Ncwzsi9k2lr5G\nJ8aEFkYGrYqOQRbU5xOReMj8wWHgnSUC0fjH0gjffGiUC2HfrrNIQvXKGiSBetOu\nIWOmFiESG8IhrPyvLwX53NbMWeCihzbYGJxGyiL0bvDHxqDxzuvteSaEfNm1miPA\nQ9rs5vFnHM0R3kFjdQIDAQAB\n-----END PUBLIC KEY-----')
server_pub_enc = PKCS1_OAEP.new(_server_pub_enc)
server_pub_sig = DSA.construct(
    [
        6492988819243051335053735606322819439099395961135352303030066825351059776939776358522765113843576255727411249922052441719518573282010295240606387519552263,
        5720927070571587652595864015095152811124313453716975619963331476834195150780326792550956895343289380256771573459290257563350163686508250507929578552744739,
        6703916277208300332610863417051397338268350992976752494932363399494412092698152568009978917952727431041521105933065433917303157931689721949082879497208537,
        1022875313346435070370368907571603203095488145799])


class Oracle:

    def __init__(self, x):
        self.x = x

    def send_num(self, a):
        self.x.send(a+b'\n')

    def get(self, sig, bet):
        self.send_num(binascii.b2a_hex(sig))
        self.send_num(binascii.b2a_hex(bet))
        res = self.x.recv_until(PatternMatcher.frombytes(b'EOF<<\n')).decode()
        print('got >> ', res)

        if re.search('>>FAILED', res):
            return False
        m = re.search('E=(\w+)\nD=(\w+)', res)
        assert m
        return m.group(1).encode(), m.group(2).encode()


def get_rsa_key_from_db(n, x):
    return RSA.construct((n, int(x[0], 16), int(x[1], 16))).exportKey('PEM')

remote = '52.6.11.111'
remote_port = 4321


def send_with_sig(dsa, conn, msg):
    sig = dsa.sign(msg, 2)
    out = msg+b'~'+(','.join(map(str, sig))).encode()
    conn.send(out)


def get_guess_for(val):
    fmt = 'I hereby commit to a guess of {}'.format(val)
    return fmt


def main():
    dsa = DSA.generate(512)

    data = [dsa.key.y, dsa.key.g, dsa.key.p, dsa.key.q]
    data_str = ','.join(map(str, data))
    chunk_size = 64
    chunks = []

    for i in range((len(data_str)+chunk_size-1)//chunk_size):
        tmp = data_str[64*i:64*i+64].encode()
        chunks.append(binascii.b2a_hex(server_pub_enc.encrypt2(tmp)[0]))
    enc_key = b','.join(chunks)

    n = 0x345080e693fa74f29d5ccac2f13556bea2541231949e14d7cd86068e5adcbc3d5622936f770fab224beea0da967057fdd9cd8419561c77445fa8b358720afc9f3703acc4b3b6901140587d83477fd271d3499797f9582bb1a5c985804ff905055cc4efecedd70cacc219ca3ba49537d6268ab66aa1c639c1963e089f3a63aac9b8b
    n = 0x167c731ae38435961bd5322b2b0ec685027147d194b8096fc2bcadacbece96d29b11c93dff0417644387aaca8cbdaa3bc895fd787c8fed999c19efcda1b0603b79370e675fc3a7e5536c8b07566b845a2fb513735d7ddb5051d04fe129eae00f17896ca892087388249b4e68acf46ed6938338a03b3a542b2c20f861cbc86eab10751
    n = 0x3ada6f51c3e3009b4b63bb14b710624f321248b12741559e29a487eaaa05167dfd9f712e1825769ba612595b81945e0def05c379cc11a4419a3bfa00f14c6ca43ec21306955fc16621025898b59219cc1c4e0474719dbc715f9c31344c9af39a3d954fedc39651f244ee2c333fe257125a97d4db45135b53eb2383714f302bcf6b6
    n = 0x29b32eb59e7ee1c467e1cc952af0d531d9d3128fbd6aecab8394fddc016e7786267b212bdaf6d343fef51a7a8ebec644c65d040f70b99e5a5c570024328431d17800ecd478bcb6fb92c0dfd76fd7cea637d9317c1cdd90b9b30f548daa7e39fb5a9d289246e4b90ec665e797bc76587d4d19e2edb2e6269621910f83b17726240de12c18e69a
    n = 0xc56f3ad5b3eca2ea9920c4fb01a84bf6538e2a5dd9f776a9fa1b22590a8609bb4a03ed13c7c07aa82d792c5676c8296381518838b03444079604b88b1d5048d2da88c036201c1599da302532b94a0ba9902750748d491bbfb1c0da674b6cbba0c1fb6bb693080eabdd0c7096757c8b80fe8ca6d82cb1bc5151a30fa40f9ea982675b1

    k = RSA.construct((n, 12))
    x = PKCS1_OAEP.new(k)

    assert len(sys.argv) > 1
    with Connection(remote, remote_port) as conn, Process(sys.argv[1]) as proc:

        print('ENCRYPT MOFO')
        try:
            len_sig = len(x.encrypt2(b'kfwefappa')[1])
        except:
            print('EJSUS FAIL')
            raise
        print('ENCRYPT MOFO')
        sent_sig = 'YOU KAPPA FUCK'
        prefix = '\x00'*(len_sig-len(sent_sig))
        sig = prefix+sent_sig
        sig = sig.encode()

        db = []

        y = Oracle(proc)
        y.send_num(hex(n)[2:].encode())
        odd_max = 2
        if 0:
            for i in range(0, odd_max):
                s = get_guess_for(i)
                print('ON STEP >> ', i)
                nbit = 10
                for A in range(2**nbit):
                    s2 = ''
                    for j in range(nbit):
                        if A >> j & 1:
                            s2 += ' '
                        else:
                            s2 += '\n'
                    s2 = s+s2
                    gen = x.encrypt2(s2.encode())[1]
                    print(gen)
                    print(hex(n))
                    work = gen
                    res = y.get(sig, work)
                    if res:
                        db.append(res)
                        break
                else:
                    assert False
        else:
            db.append([
                b'a0fbbacc479a8a3af09aebdbb9ae30834a10699d9d618108514d88f308161577809ae60e182c75e0f95797806179363a4c17da900373a3879ac3a692dc5f8f8b1e022eee294dd7013858394fa2f366179f64c9ab0ff28c89b3a78b1a6b6a8852de7a3f5de4dbe6ae0667941e8283f4c3eaa22572cc4dd4dceef54251bd3cf4690d301',
                b'2a1fed419b80c8145524c84c9c1f2efdf598d18da0eecfd2892a8956358827e613cf05c505e9b902277727c889a7ff32ea0b4bbe018fc8acc33743cfa14d31597a0e879135edc1257c8815208817dc7f6ed470c4e75742890ec7f7604c7025afa4f0f6193e3df2925320553ea1c9be3982369dd2b35b2b858fc7ea029e132693e355'
            ])

            db.append([
                b'42de041b5d51a89aa133a02dcb108a0714344d6cd0e23cee44d0e64a7c03fcd7163a8195f106ab8664215d9d13efa63871189ddbf25a7aedb1803c6ae5d8c75bd3aa78ac934f68ff1b55d4984bd66b8e79d1b490d553f1f0b3d93c04101e78603e94e5577f6525f934bef8016497820831e9e6a4571e446334a98e1b9d99f015a1735',
                b'70f611574824ae1ca492657f842feb2fea44283f7e7cc1da42997df2a54402975a490b9ca3990c95536c93c317976d7db1c844575b5f3f12bd9cc4f83808f31635749dd58da1b4cb392b08131766472895db3beb16f5317f4477a0df71f84c22de477066ce0bc4468df5a68e2527390c561c8c177b823f824b6926acf17599447f509'
            ])

        print('sending')
        conn.trash(1)
        conn.send(enc_key)

        while True:
            time.sleep(0.5)
            pattern = b'You have \$([0-9]+)\)\n'
            res = conn.recv_until(PatternMatcher.fromre(pattern))
            monies = int(re.search(pattern, res).group(1))
            assert res

            conn.send('{}\n'.format(monies))

            conn.recv_until(PatternMatcher.frombytes(b'At what odds'))
            conn.send('{}\n'.format(odd_max))

            conn.recv_until(PatternMatcher.frombytes(b'Alright, what is your'))
            send_with_sig(dsa, conn, binascii.b2a_hex(sig))

            res = conn.recv_until(PatternMatcher.frombytes(b'Now what is your'))
            rng = re.search(
                b'the secure RNG is ([0-9]+)\n',
                res).group(1).decode()
            rng = int(rng)
            print('rng is >> ', rng)
            want = rng % odd_max
            uu = get_rsa_key_from_db(n, db[want])
            print(uu)
            privkey = PKCS1_OAEP.new(RSA.importKey(uu))
            guess = privkey.decrypt(sig)
            guess = int(guess[len("I hereby commit to a guess of "):])
            send_with_sig(dsa, conn, uu)


main()
