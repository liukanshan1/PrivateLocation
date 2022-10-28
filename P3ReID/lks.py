from cmath import sqrt
from encryption import paillier
from secomp.secureprotol import SecureComputing

import numpy as np

if __name__ == '__main__':

    x1, y1, x2, y2 = 1, 2, 5, 7
    r1, r2 = 1, 2

    user = [x1, x1 ** 2, y1, y1 ** 2]
    serv = [x2, x2 ** 2, y2, y2 ** 2]

    distant = sqrt(user[1] + user[3] + serv[1] + serv[3] - 2 * (user[0] * serv[0] + user[2] * serv[2]))
    print(distant)
    max_distant = (r1 + r2)**2
    print(max_distant)

    print('----------Encrypted version-----------')
    public_key, private_key, partial_private_keys = paillier.generate_paillier_keypair(n_length=256)
    cp = paillier.ThresholdPaillier(public_key, partial_private_keys.sk1)
    csp = paillier.ThresholdPaillier(public_key, partial_private_keys.sk2)
    sc = SecureComputing(cp, csp)
    # encrypt
    enc_x1 = public_key.encrypt(user[0])
    enc_x2 = public_key.encrypt(serv[0])
    enc_x1x2 = sc.smul(enc_x1, enc_x2)
    x1x2 = private_key.decrypt(enc_x1x2)
    print(x1x2 == user[0] * serv[0])
    enc_y1 = public_key.encrypt(user[2])
    enc_y2 = public_key.encrypt(serv[2])
    enc_y1y2 = sc.smul(enc_y1, enc_y2)
    y1y2 = private_key.decrypt(enc_y1y2)
    print(y1y2 == user[2] * serv[2])



