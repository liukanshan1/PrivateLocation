import random
from test import paillier

if __name__ == '__main__':
    """n_length = 256
    p = getprimeover(n_length // 2)
    q = p
    while q == p:
        q = getprimeover(n_length // 2)
    n = p * q
    n_len = n.bit_length()
    g = n + 1
    lmd = extended_euclidean_algorithm(41 - 1, 43 - 1)
    print(lmd)"""
    public_key, private_key, partial_private_keys = paillier.generate_paillier_keypair(n_length=256)
    m = -12.456
    encrypted_number = public_key.encrypt(m)
    print(private_key.decrypt(encrypted_number))

    print('------')
    m = -1239945
    ciphertext = public_key.raw_encrypt(m)
    decryption = private_key.raw_decrypt(ciphertext)
    cp = paillier.ThresholdPaillier(public_key, partial_private_keys.sk1)
    csp = paillier.ThresholdPaillier(public_key, partial_private_keys.sk2)

    partial_ciphertext1 = cp.partial_raw_decrypt(ciphertext)
    partial_ciphertext2 = csp.partial_raw_decrypt(ciphertext)
    plaintext = csp.final_raw_decrypt(partial_ciphertext1, partial_ciphertext2)
    print(plaintext)

    print("----------")
    m = -12.34566
    encrypted_number = public_key.encrypt(m)
    partial_decrypted_number1 = cp.partial_decrypt(encrypted_number)
    partial_decrypted_number2 = csp.partial_decrypt(encrypted_number)
    print(csp.final_decrypt(partial_decrypted_number1, partial_decrypted_number2))

    print('------测试加减乘除------')
    cp = paillier.ThresholdPaillier(public_key, partial_private_keys.sk1)
    csp = paillier.ThresholdPaillier(public_key, partial_private_keys.sk2)
    count_add = count_sub = count_mul = 0
    for i in range(1000):
        if i % 4 == 0:
            x = random.random()
            y = random.random()
        elif i % 4 == 1:
            x = random.random()
            y = random.random() * (-1)
        elif i % 4 == 2:
            x = random.random() * (-1)
            y = random.random()
        else:
            x = random.random() * (-1)
            y = random.random() * (-1)
        if private_key.decrypt(public_key.encrypt(x) + y) != \
                private_key.decrypt(public_key.encrypt(x) + public_key.encrypt(y)):
            count_add += 1
        if private_key.decrypt(public_key.encrypt(x) - y) != \
                private_key.decrypt(public_key.encrypt(x) - public_key.encrypt(y)):
            count_sub += 1
        if x * y != private_key.decrypt(public_key.encrypt(x) * y):
            count_mul += 1
    print(count_add, count_sub, count_mul)

    x = 0.2
    y = -2
    print(private_key.decrypt(public_key.encrypt(x) * y))
    print(private_key.decrypt(public_key.encrypt(x) / y))
    
    print('########测试加密和解密##########')
    """count = count1 = 0
    for i in range(1000):
        if i % 4 == 0:
            x = random.random()
            y = random.random()
        elif i % 4 == 1:
            x = random.random()
            y = random.random() * (-1)
        elif i % 4 == 2:
            x = random.random() * (-1)
            y = random.random()
        else:
            x = random.random() * (-1)
            y = random.random() * (-1)
        xaddy0 = x + y
        xsuby0 = x - y

        exsuby = public_key.encrypt(x).__sub__(public_key.encrypt(y))
        xsuby = private_key.decrypt(exaddy)
        xsuby1 = csp.final_decrypt(cp.partial_decrypt(exaddy), csp.partial_decrypt(exaddy))

        if xsuby != xsuby0:
            count += 1
        if xsuby1 != xsuby0:
            count1 += 1
            #print(xaddy0, xaddy1)
    print(count, count1)"""