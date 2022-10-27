import fractions
import random

import paillier

from test.fixedpoint import FixedPointNumber


def encoding(scalar):
    return (fractions.Fraction(scalar) * 2 ** 53).numerator

def decoding(res, exponent):
    return res / (2 ** exponent)

def pop_encoding(scalar):
    return scalar * 10 ** 16

def pop_decoding(res, exponent):
    return res / (10 ** exponent)

if __name__ == '__main__':

    public_key, private_key, partial_private_key = paillier.generate_paillier_keypair(n_length=512)

    print('-----测试四个浮点数编码方法-----')

    count0 = count1 = count2 = 0
    NUM = 10000000
    """for i in range(NUM):
        m = random.random()

        # Encoding
        encode_m = encoding(m)
        pop_encode_m = pop_encoding(m)
        btc_encode_m = FixedPointNumber.encode(m)

        # Decoding
        decode_m = decoding(encode_m, 53)
        pop_decode_m = pop_decoding(pop_encode_m, 16)
        btc_decode_m = btc_encode_m.decode()

        if decode_m != m:
            count0 += 1

        if pop_decode_m != m:
            count1 += 1

        if btc_decode_m != m:
            count2 += 1

    print(count0, count1, count2)
    print(count0/NUM, count1/NUM, count2/NUM)"""

    print("-------")
    count0 = count1 = count2 = 0

    NUM = 10000000
    for i in range(NUM):
        m = random.random()
        n = random.random()
        p = random.random()
        q = random.random()

        # Encoding
        encode_m = encoding(m)
        encode_n = encoding(n)
        encode_p = encoding(p)
        encode_q = encoding(q)

        pop_encode_m = pop_encoding(m)
        pop_encode_n = pop_encoding(n)
        pop_encode_p = pop_encoding(p)
        pop_encode_q = pop_encoding(q)

        btc_encode_m = FixedPointNumber.encode(m)
        btc_encode_n = FixedPointNumber.encode(n)
        btc_encode_p = FixedPointNumber.encode(p)
        btc_encode_q = FixedPointNumber.encode(q)

        # computation
        cmp = (m + n - p) * q
        encode_cmp = (encode_m + encode_n - encode_p) * encode_q
        pop_encode_cmp = (pop_encode_m + pop_encode_n - pop_encode_p) * pop_encode_q
        btc_encode_cmp = (btc_encode_m + btc_encode_n - btc_encode_p) * btc_encode_q

        # Decodeing
        decode_cmp = decoding(encode_cmp, 106)
        pop_decode_cmp = pop_decoding(pop_encode_cmp, 32)
        btc_decode_cmp = btc_encode_cmp.decode()

        if decode_cmp != cmp:
            count0 += 1

        if pop_decode_cmp != cmp:
            count1 += 1

        if btc_decode_cmp != cmp:
            count2 += 1

    print(count0, count1, count2)
    print(count0 / NUM, count1 / NUM, count2 / NUM)
    """print("--computation--")
    count = 0
    for i in range(1000):
        m = random.random()
        n = random.random()
        p = random.random()

        # Encoding
        encode_m = encoding(m)
        encode_n = encoding(n)
        encode_p = encoding(p)

        # computation
        cmp = (m + n)
        encode_cmp = (encode_m + encode_n)

        decode_cmp = decoding(encode_cmp, 53)

        if cmp != decode_cmp:
            count +=1

    print(count)"""




