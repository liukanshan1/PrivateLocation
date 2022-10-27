import time
import multiprocessing

from encryption import paillier
import numpy as np

from test.opt import opt
from model_util import loadNetwork, extractFeatures, list_pictures

if __name__ == '__main__':

    public_key, private_key, partial_private_keys = paillier.generate_paillier_keypair(n_length=1024)
    model = loadNetwork(opt.weight)
    print('ok')

    queryPath = list_pictures('D:\\python-workspace\\datasets\\Market-1501\\query1')
    pf = extractFeatures(model, queryPath).numpy()


    """encode = EncodedNumber.encode(pf[0][0].item())
    cipher = public_key.encrypt(encode)
    plain = private_key.decrypt(cipher)
    print(plain)

    print('--------------')
    for i in range(len(pf)):
        for j in range(len(pf[i])):
            if private_key.decrypt(public_key.encrypt(pf[i][j].item())) != pf[i][j].item():
                print(private_key.decrypt(public_key.encrypt(pf[i][j].item())), pf[i][j].item())"""

    """print('-------Single thread--------')
    for e in range(12):
        start = time.perf_counter()
        for k in range(10):
            for i in range(2 ** e):
                public_key.encrypt(pf[0][i].item())
        print(round((time.perf_counter() - start) / 10 * 1000))"""


    print('-------Multiple thread--------')
    pool = multiprocessing.Pool(processes=1)
    for e in range(2):
        tensor_val = pf[0][:2 ** e]
        val = np.zeros(2 ** e, dtype=float)
        for i in range(2 ** e):
            val[i] = tensor_val[i].item()
        start = time.perf_counter()
        for k in range(10):
            res = pool.map(public_key.encrypt, val)
        print(round((time.perf_counter() - start) / 10 * 1000))
