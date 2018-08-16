#!/usr/bin/env python

import opa.crypto


sudoku_full = [[1, 7, 2, 5, 4, 9, 6, 8, 3],
               [6, 4, 5, 8, 7, 3, 2, 1, 9],
               [3, 8, 9, 2, 6, 1, 7, 4, 5],
               [4, 9, 6, 3, 2, 7, 8, 5, 1],
               [8, 1, 3, 4, 5, 6, 9, 7, 2],
               [2, 5, 7, 1, 9, 8, 4, 3, 6],
               [9, 6, 4, 7, 1, 5, 3, 2, 8],
               [7, 3, 1, 6, 8, 2, 5, 9, 4],
               [5, 2, 8, 9, 3, 4, 1, 6, 7], ]
mat = []
for x in sudoku_full:
    mat += x
print(mat)


cipher = 'DKBRHSBTJVPHFKYJASSTZBOCOXXMRCKTNRJGGRSCBQJBRZVKPGAJOVANNEIHIKITIHKHUOFYISZBOCSIGEXQZYWEFANOAVEWQBJNYVUUYEAOIRRSWY'


def tsf(x):
    return [ord(a)-ord('A') for a in x]


def itsf(x):
    return ''.join([chr(a+ord('A')) for a in x])


def getm(a, b):
    a*=3
    b*=3
    tb = []
    for i in range(3):
        for j in range(3):
            tb += [sudoku_full[b+i][a+j]]
    return tb


def main():
    x = opa.crypto.HillCipher.get()

    m = 3
    u = getm(1,1)
    u=[3,4,1,2,5,9,7,6,8]
    print(u)

    x.setKey(u, m, 26)
    for i in range(0, len(cipher), m):
        y = tsf(cipher[i:i+m])
        print(itsf(x.decrypt(y)), end='')
    print()


main()
