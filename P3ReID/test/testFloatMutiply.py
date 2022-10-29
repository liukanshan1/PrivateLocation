import numpy as np

from encryption import paillier
from model.opt import opt
from model.model_util import loadNetwork, extractFeatures, list_pictures
from secomp.secureprotol import SecureComputing
if __name__ == '__main__':
    public_key, private_key, partial_private_keys = paillier.generate_paillier_keypair(n_length=256)
    cp = paillier.ThresholdPaillier(public_key, partial_private_keys.sk1)
    csp = paillier.ThresholdPaillier(public_key, partial_private_keys.sk2)
    sc = SecureComputing(cp, csp)

    five = public_key.encrypt(1.1)
    print(private_key.decrypt(five * 2 ))
    print(private_key.decrypt(sc.smul(five,five)))



