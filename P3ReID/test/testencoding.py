import math
import random

from encoding import EncodedNumber
import paillier

from test.fixedpoint import FixedPointNumber
from test.encoding_o import EncodedNumber1


def encodingby10(sacle, precious):
    return math.floor(sacle * 10 ** precious)


def decodingby10(res, precious):
    return round(res / (10 ** precious), 16)


if __name__ == '__main__':
    public_key, private_key, partial_private_key = paillier.generate_paillier_keypair(n_length=256)

    """enc = EncodedNumber.encode(public_key, 1.2250738585074075)
    print(math.frexp(1.2250738585074075))
    print(enc.encoding, enc.exponent)
    negexp = EncodedNumber.BASE ** enc.exponent
    dec = negexp * enc.encoding
    print(enc.decode())"""

    """print(encodingby10(0.90071993, 16) + encodingby10(0.2250738, 16))
    print(decodingby10(encodingby10(0.90071993, 16) + encodingby10(0.02250738, 16), 16))
    print(0.90071993 + 0.02250738)

    enc = EncodedNumber.encode(public_key, 0.2250738, precision=1e-8)
    print(enc.encoding, enc.exponent)
    print(EncodedNumber.decode(enc.encoding, precision=1e-8, max_exponent=16))

    print(EncodedNumber.encode(public_key, 123).encoding)"""

    print('-----测试四个浮点数编码方法-----')
    m = -0.999999
    encode = EncodedNumber.encode(m)
    print(encode.decode())
    count = p_count = fate_count = pop_count = 0
    for i in range(1000):
        m = random.random() * (-1) ** i
        encode = EncodedNumber.encode(m)
        p_encode = EncodedNumber1.encode(public_key, m)
        fate_encode = FixedPointNumber.encode(m)
        pop_encode = m * 2 ** 64
        decode = encode.decode();
        p_decode = p_encode.decode();
        fate_decode = fate_encode.decode()
        pop_decode = pop_encode / (2 ** 64)
        if decode != m:
            count += 1
        if p_decode != m:
            p_count += 1
        if fate_decode != m:
            #print(fractions.Fraction(m))
            fate_count += 1
        if pop_decode != m:
            pop_count += 1

    print(count, p_count, fate_count, pop_count)


