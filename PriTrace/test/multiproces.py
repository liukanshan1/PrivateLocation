import multiprocessing
import time
from test import paillier


def add(x, y):
	return x+y

if __name__ == '__main__':

    print('-----------')
    public_key, private_key, partial_private_keys = paillier.generate_paillier_keypair(n_length=512)
    A = [12.34566, 1.23, 3.45, 5.67, 12, 14, 12.34566, 1.23, 3.45, 5.67, 12, 14, 12.34566, 1.23, 3.45, 5.67, 12, 14,
         12.34566, 1.23, 3.45, 5.67, 12, 14, 12.34566, 1.23, 3.45, 5.67, 12, 14, 12.34566, 1.23, 3.45, 5.67, 12, 14,
         12.34566, 1.23, 3.45, 5.67, 12, 14, 12.34566, 1.23, 3.45, 5.67, 12, 14, 12.34566, 1.23, 3.45, 5.67, 12, 14,
         12.34566, 1.23, 3.45, 5.67, 12, 14, 12.34566, 1.23, 3.45, 5.67, 12, 14, 12.34566, 1.23, 3.45, 5.67, 12, 14,
         12.34566, 1.23, 3.45, 5.67, 12, 14, 12.34566, 1.23, 3.45, 5.67, 12, 14, 12.34566, 1.23, 3.45, 5.67, 12, 14,
         12.34566, 1.23, 3.45, 5.67, 12, 14, 12.34566, 1.23, 3.45, 5.67, 12, 14, 12.34566, 1.23, 3.45, 5.67, 12, 14,
         12.34566, 1.23, 3.45, 5.67, 12, 14, 12.34566, 1.23, 3.45, 5.67, 12, 14, 12.34566, 1.23, 3.45, 5.67, 12, 14,
         12.34566, 1.23, 3.45, 5.67, 12, 14, 12.34566, 1.23, 3.45, 5.67, 12, 14, 12.34566, 1.23, 3.45, 5.67, 12, 14,
         12.34566, 1.23, 3.45, 5.67, 12, 14, 12.34566, 1.23, 3.45, 5.67, 12, 14, 12.34566, 1.23, 3.45, 5.67, 12, 14,
         12.34566, 1.23, 3.45, 5.67, 12, 14, 12.34566, 1.23, 3.45, 5.67, 12, 14, 12.34566, 1.23, 3.45, 5.67, 12, 14,
         12.34566, 1.23, 3.45, 5.67, 12, 14, 12.34566, 1.23, 3.45, 5.67, 12, 14, 12.34566, 1.23, 3.45, 5.67, 12, 14,
         12.34566, 1.23, 3.45, 5.67, 12, 14, 12.34566, 1.23, 3.45, 5.67, 12, 14, 12.34566, 1.23, 3.45, 5.67, 12, 14,
         12.34566, 1.23, 3.45, 5.67, 12, 14, 12.34566, 1.23, 3.45, 5.67, 12, 14, 12.34566, 1.23, 3.45, 5.67, 12, 14,
         12.34566, 1.23, 3.45, 5.67, 12, 14, 12.34566, 1.23, 3.45, 5.67, 12, 14, 12.34566, 1.23, 3.45, 5.67, 12, 14,
         12.34566, 1.23, 3.45, 5.67, 12, 14, 12.34566, 1.23, 3.45, 5.67, 12, 14, 12.34566, 1.23, 3.45, 5.67, 12, 14,
         12.34566, 1.23, 3.45, 5.67, 12, 14, 12.34566, 1.23, 3.45, 5.67, 12, 14, 12.34566, 1.23, 3.45, 5.67, 12, 14,
         12.34566, 1.23, 3.45, 5.67, 12, 14, 12.34566, 1.23, 3.45, 5.67, 12, 14, 12.34566, 1.23, 3.45, 5.67, 12, 14,
         12.34566, 1.23, 3.45, 5.67, 12, 14, 12.34566, 1.23, 3.45, 5.67, 12, 14, 12.34566, 1.23, 3.45, 5.67, 12, 14,
         12.34566, 1.23, 3.45, 5.67, 12, 14, 12.34566, 1.23, 3.45, 5.67, 12, 14, 12.34566, 1.23, 3.45, 5.67, 12, 14,
         12.34566, 1.23, 3.45, 5.67, 12, 14, 12.34566, 1.23, 3.45, 5.67, 12, 14, 12.34566, 1.23, 3.45, 5.67, 12, 14,
         12.34566, 1.23, 3.45, 5.67, 12, 14, 12.34566, 1.23, 3.45, 5.67, 12, 14, 12.34566, 1.23, 3.45, 5.67, 12, 14,
         12.34566, 1.23, 3.45, 5.67, 12, 14, 12.34566, 1.23, 3.45, 5.67, 12, 14, 12.34566, 1.23, 3.45, 5.67, 12, 14,
         12.34566, 1.23, 3.45, 5.67, 12, 14, 12.34566, 1.23, 3.45, 5.67, 12, 14, 12.34566, 1.23, 3.45, 5.67, 12, 14,
         12.34566, 1.23, 3.45, 5.67, 12, 14, 12.34566, 1.23, 3.45, 5.67, 12, 14, 12.34566, 1.23, 3.45, 5.67, 12, 14,
         12.34566, 1.23, 3.45, 5.67, 12, 14, 12.34566, 1.23, 3.45, 5.67, 12, 14, 12.34566, 1.23, 3.45, 5.67, 12, 14,
         12.34566, 1.23, 3.45, 5.67, 12, 14, 12.34566, 1.23, 3.45, 5.67, 12, 14, 12.34566, 1.23, 3.45, 5.67, 12, 14,
         12.34566, 1.23, 3.45, 5.67, 12, 14, 12.34566, 1.23, 3.45, 5.67, 12, 14, 12.34566, 1.23, 3.45, 5.67, 12, 14,
         12.34566, 1.23, 3.45, 5.67, 12, 14, 12.34566, 1.23, 3.45, 5.67, 12, 14, 12.34566, 1.23, 3.45, 5.67, 12, 14,
         12.34566, 1.23, 3.45, 5.67, 12, 14, 12.34566, 1.23, 3.45, 5.67, 12, 14, 12.34566, 1.23, 3.45, 5.67, 12, 14,
         12.34566, 1.23, 3.45, 5.67, 12, 14, 12.34566, 1.23, 3.45, 5.67, 12, 14, 12.34566, 1.23, 3.45, 5.67, 12, 14,
         ]

    cores = multiprocessing.cpu_count()
    pool = multiprocessing.Pool(processes=6)
    start = time.perf_counter()
    for i in range(10):
        res = pool.apply_async(public_key.encrypt, A)
        #res = pool.map(private_key.decrypt, res)
    print(time.perf_counter() - start)

    print('-----')
    start = time.perf_counter()
    for i in range(10):
        for x in A:
            c = public_key.encrypt(x)
            #private_key.decrypt(c)
    print(time.perf_counter() - start)

    print('###############')
    x1 = list(range(5))
    y1 = list(range(5))
    x_y = zip(x1, y1)
    print(pool.map(add, x_y))
