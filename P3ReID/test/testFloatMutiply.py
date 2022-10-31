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

    ev1 = public_key.encrypt(3)
    v2 = 4
    # Step-1
    e_result = ev1 / v2
    print(private_key.decrypt(e_result))
    print(e_result.exponent)
    e_result1 = cp.partial_decrypt(e_result)
    print(e_result1.exponent)
    # Step-2
    e_result2 = csp.partial_decrypt(e_result)
    print(e_result2.exponent)
    result = csp.final_decrypt(e_result1, e_result2) / (10 ** e_result.exponent)
    print(result)
    print(sc.scomp(ev1, v2))



