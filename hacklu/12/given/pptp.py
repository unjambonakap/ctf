#
# challenge written by sqall (http://twitter.com/sqall01) of the FluxFingers for hack.lu 2012
#

from pyDes import *
import binascii
import hashlib


class PPTP:
    # constant for hash function
    constant = "Trololol"

    def lm_hash(self, input_password):
        # only use the first 14 bytes
        input_password = input_password[0:14]

        # convert all characters to uppercase chars
        input_password = input_password.upper()

        # split given password in two parts via 8 bytes
        password_part1 = input_password[0:8]

        # concat two 0 bytes to reach 8 bytes
        password_part2 = input_password[8:14] + "\0\0"

        # hash part 1
        part1_des = des(password_part1)
        hash_part1 = part1_des.encrypt(self.constant)

        # hash part 2
        print 'go', binascii.b2a_hex(self.constant), binascii.b2a_hex(password_part2)
        part2_des = des(password_part2)
        hash_part2 = part2_des.encrypt(self.constant)

        # concat hash parts
        output_hash = hash_part1 + hash_part2

        # return hash as hex value
        return binascii.hexlify(output_hash)

    def response_lm(self, challenge, password):
        # generate lm_hash for response
        password_hash = self.lm_hash(password)

        if len(challenge) != 16:
            raise ValueError("Challenge has to be 8 byte hex value.")

        # create three passwords for the response
        password_res1 = password_hash[0:16]
        password_res2 = password_hash[12:28]
        password_res3 = password_hash[28:32] + "000000000000"
        print 'pas>> ', password_res1, password_res2, password_res3

        # response part 1
        part1_des = des(binascii.unhexlify(password_res1))
        res_part1 = part1_des.encrypt(binascii.unhexlify(challenge))

        # response part 2
        part2_des = des(binascii.unhexlify(password_res2))
        res_part2 = part2_des.encrypt(binascii.unhexlify(challenge))

        # response part 3
        part3_des = des(binascii.unhexlify(password_res3))
        res_part3 = part3_des.encrypt(binascii.unhexlify(challenge))
        print 'RES IS ', binascii.hexlify(res_part3)

        # create full response and return
        response = res_part1 + res_part2 + res_part3
        return binascii.hexlify(response)

    def newTechnologie_hash(self, input_password):
        # only use the first 14 bytes
        input_password = input_password[0:14]

        # use sha1 as hash algo
        m = hashlib.sha1()

        # hash password
        m.update(input_password)

        # return hash as hex value
        return binascii.hexlify(m.digest())

    def response_newTechnologie(self, challenge, password):
        # generate newTechnologie_hash for response
        password_hash = self.newTechnologie_hash(password)

        if len(challenge) != 16:
            raise ValueError("Challenge has to be 8 byte hex value.")

        # create three passwords for the response
        password_res1 = password_hash[0:16]
        password_res2 = password_hash[16:32]
        password_res3 = password_hash[32:40] + "00000000"

        # response part 1
        part1_des = des(binascii.unhexlify(password_res1))
        res_part1 = part1_des.encrypt(binascii.unhexlify(challenge))

        # response part 2
        part2_des = des(binascii.unhexlify(password_res2))
        res_part2 = part2_des.encrypt(binascii.unhexlify(challenge))

        # response part 3
        part3_des = des(binascii.unhexlify(password_res3))
        res_part3 = part3_des.encrypt(binascii.unhexlify(challenge))

        # create full response and return
        response = res_part1 + res_part2 + res_part3
        return binascii.hexlify(response)
