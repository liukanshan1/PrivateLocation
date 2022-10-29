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

    five = public_key.encrypt(5)
    print(private_key.decrypt(five))
    print(private_key.decrypt(five ** 2))
    print(private_key.decrypt(five * five))

    # gf_numpy = np.array([[1.0, 1.0, 1.0], [1.0, 1.0, 1.0], [1.0, 1.0, 1.0]])
    # enc_gf = np.zeros((len(gf_numpy), len(gf_numpy[0])), dtype=paillier.EncryptedNumber)
    # for i in range(len(gf_numpy)):
    #     for j in range(len(gf_numpy[i])):
    #         enc_gf[i][j] = public_key.encrypt(gf_numpy[i][j])
    #
    # qf_numpy = np.array([[1.1, 2.2, 3.3], [4.4, 5.5, 6.6], [7.7 , 8.8, 9.9]])
    # enc_qf = np.zeros((len(qf_numpy), len(qf_numpy[0])), dtype=paillier.EncryptedNumber)
    # for i in range(len(qf_numpy)):
    #     for j in range(len(qf_numpy[i])):
    #         enc_qf[i][j] = public_key.encrypt(qf_numpy[i][j])
    #         # print(private_key.decrypt(enc_qf[i][j]), qf_numpy[i][j].item())
    #
    # enc_q_g_dist, q_g_dist1 = sc.sdot(enc_qf, enc_gf)
    # for i in range(len(qf_numpy)):
    #     for j in range(len(qf_numpy[i])):
    #         print(private_key.decrypt(enc_q_g_dist[i][j]))
    # print("0")


