
from challenge import CodeBasedEncryptionScheme

from random import SystemRandom
from os import urandom



if __name__ == "__main__":
    cipher = CodeBasedEncryptionScheme.new()
    random = SystemRandom()
    BLK = 1
    k = list(cipher.key)
    print(k)
    print('GOOOT ', len(k))
    for i in range(1024 + 512*3):
        pt = urandom(BLK)
        ct = cipher.encrypt(pt)
        cipher.get_rels(ct, pt)
        with open("plaintext_{:04d}".format(i), "wb") as f:
            f.write(pt)
        with open("ciphertext_{:04d}".format(i), "wb") as f:
            f.write(ct)
        assert(pt == cipher.decrypt(ct))

    with open("flag.txt", "rb") as f:
       flag = f.read().strip()

    while len(flag) % BLK != 0:
        flag += b"\0"

    cts = list()
    for i in range(len(flag) // BLK):
        cts.append(cipher.encrypt(flag[i*BLK:i*BLK + BLK]))

    for i, ct in enumerate(cts):
        with open("flag_{:02d}".format(i), "wb") as f:
            f.write(ct)
