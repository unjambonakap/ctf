from Crypto.Cipher import AES
from Crypto.Hash import MD5

import string
import sys
import binascii

pass_beg = "wcwteseawx"
brute  = "eeeeee"
possible = "qgertzasdfwhyxcvbn"
plain = "674e2"

crypted = "\
\x40\x40\xa9\x8a\xd1\xae\x25\xdf\x8b\xe9\x7d\xf6\x5f\x90\xa9\x80"

# first 16 byte's are enough
# ------------
#\x97\xf3\x95\x80\xe4\x11\x65\x55\x0a\xdc\xf8\x29\x41\x7b\x00\x2c\
#\x0f\x81\xb3\xb1\xbc\xdc\x83\x91\x1e\x06\x52\xd8\xa9\x28\x04\x35\
#\x41\x6a\x33\x2f\x7a\x3f\x8b\x34\x91\x24\x9b\x3b\x66\x96\x25\x0c\
#\x4c\x24\x36\xe6\x62\x1d\x0c\xf2\x38\x2b\x2d\x7e\x24\x8f\x08\x76\
#\x92\xd0\x6a\xeb\x23\x29\x1b\x47\x96\x24\x45\xcd\x76\x47\x99\xdf\
#\x49\x7c\xf2\xc3\xcc\x02\xd1\xbe\xb7\xe1\xae\xed\xe6\x82\x37\x30\
#\xc3\xd2\x92\x08\x0f\xde\xa5\x21\xd9\x8b\xf8\xde\x60\x7c\x0e\x29"


brutedeepth = 0
brutelen = len(brute)


def check(tocheck):
	global pass_all

	pass_all = pass_beg + tocheck

	x = AES.new(pass_all, AES.MODE_ECB)
	dec = x.decrypt(crypted)

	print("key: " + tocheck + ", decrypted: " + binascii.hexlify(dec[0:5]))

	if(dec[0:5] == plain):
		print("RIGHT ONE! (" + pass_all + ")")
		return 1
	else:
		return 0


		
def scan(deepth):
	global brute
	
	for i in range(0, len(possible)):
		brute = brute[0:brutelen-deepth] + possible[i]

		if(deepth > 1):
			scan((deepth-1))
		else:
			if(check(brute) == 1):
				sys.exit()


scan(6)
