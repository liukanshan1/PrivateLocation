from encryption import paillier
from location.location import Location
from secomp.secureprotol import SecureComputing
import math
from geopy import distance


if __name__ == '__main__':
    loc1 = Location(12.00, 23.103, 113.370, 10, False)
    loc2 = Location(12.00, 23.105, 113.357, 10, True)
    print(loc1, " ", loc2)
    print(distance.distance((23.103, 113.370), (23.105, 113.357)).km * 1000)
    x1, y1, z1 = loc1.toXYZ()
    x2, y2, z2 = loc2.toXYZ()
    print(math.sqrt((x1 + x2) ** 2 + (y1 + y2) ** 2 + (z1 + z2) ** 2))
    # print('----------Intermediate value-----------')
    # print(x1, " ", y1, " ", z1)
    # print(x2, " ", y2, " ", z2)
    # print(x1*x2, " ", y1*y2, " ", z1*z2)
    print('----------Encrypted version-----------')
    public_key, private_key, partial_private_keys = paillier.generate_paillier_keypair(n_length=256)
    cp = paillier.ThresholdPaillier(public_key, partial_private_keys.sk1)
    csp = paillier.ThresholdPaillier(public_key, partial_private_keys.sk2)
    sc = SecureComputing(cp, csp)
    # encrypt
    enc_loc1 = loc1.enc(public_key)
    enc_loc2 = loc2.enc(public_key)
    # print(private_key.decrypt(enc_loc1.x), " ", private_key.decrypt(enc_loc1.y), " ", private_key.decrypt(enc_loc1.z))
    # print(private_key.decrypt(enc_loc2.x), " ", private_key.decrypt(enc_loc2.y), " ", private_key.decrypt(enc_loc2.z))
    enc_distant = sc.sdistance(enc_loc1, enc_loc2)
    print(math.sqrt(private_key.decrypt(enc_distant)))



