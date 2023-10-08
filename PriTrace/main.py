from encryption import paillier
from location.shapes import Rectangle
from location.location import Location
from secomp.secureprotol import SecureComputing
import math
from geopy import distance
from datetime import datetime


if __name__ == '__main__':
    # Generate public and private key
    public_key, private_key, partial_private_keys = paillier.generate_paillier_keypair(n_length=256)
    cp = paillier.ThresholdPaillier(public_key, partial_private_keys.sk1)
    csp = paillier.ThresholdPaillier(public_key, partial_private_keys.sk2)
    sc = SecureComputing(cp, csp)
    # Server side
    loc1 = Location([datetime(2022, 10, 1, 10, 30, 00), datetime(2022, 10, 1, 12, 30, 00)],
                    113.420498, 23.111519, 100, True)
    loc2 = Location([datetime(2022, 10, 1, 10, 30, 00), datetime(2022, 10, 1, 12, 30, 00)],
                    113.420794, 23.112188, 100, True)
    loc3 = Location([datetime(2022, 10, 1, 10, 30, 00), datetime(2022, 10, 1, 12, 30, 00)],
                    113.42353, 23.11112, 100, True)
    loc4 = Location([datetime(2022, 10, 1, 10, 30, 00), datetime(2022, 10, 1, 12, 30, 00)],
                    113.423238, 23.110463, 100, True)
    meilin_M = Rectangle(loc1, loc2, loc3, loc4)
    enc_rec = meilin_M.encrypt(public_key)

    
    # User side
    uloc1 = Location([datetime(2022, 10, 1, 9, 30, 00), datetime(2022, 10, 1, 11, 30, 00)],
                     113.422384, 23.111253, 10) # 在里面 时间匹配
    uloc2 = Location([datetime(2022, 10, 1, 9, 30, 00), datetime(2022, 10, 1, 10, 28, 00)],
                     113.422384, 23.111253, 10) # 在里面 时间不匹配
    uloc3 = Location([datetime(2022, 10, 1, 10, 28, 00), datetime(2022, 10, 1, 11, 30, 00)],
                     113.41907, 23.110031, 10) # 在外面 时间匹配
    uloc4 = Location([datetime(2022, 10, 1, 9, 30, 00), datetime(2022, 10, 1, 10, 12, 00)],
                     113.41907, 23.110031, 10) # 在外面 时间不匹配
    enc_locs = [uloc1.enc(public_key), uloc2.enc(public_key), uloc3.enc(public_key), uloc4.enc(public_key)]

    for enc_loc in enc_locs:
        print(sc.is_inside_area(enc_loc, enc_rec,
                                area_time=[datetime(2022, 10, 1, 10, 30, 00), datetime(2022, 10, 1, 12, 30, 00)]))


    # loc1 = Location(12.00, 23.103, 113.370, 10, False)
    # loc2 = Location(12.00, 23.105, 113.380, 10, True)
    # print(loc1, " ", loc2)
    # print(distance.distance((23.103, 113.370), (23.105, 113.380)).km * 1000)
    # x1, y1, z1 = loc1.toXYZ()
    # x2, y2, z2 = loc2.toXYZ()
    # print(math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2 + (z1 - z2) ** 2))
    # # print('----------Intermediate value-----------')
    # # print(x1, " ", y1, " ", z1)
    # # print(x2, " ", y2, " ", z2)
    # # print(x1*x2, " ", y1*y2, " ", z1*z2)
    # print('----------Encrypted version-----------')
    # public_key, private_key, partial_private_keys = paillier.generate_paillier_keypair(n_length=256)
    # cp = paillier.ThresholdPaillier(public_key, partial_private_keys.sk1)
    # csp = paillier.ThresholdPaillier(public_key, partial_private_keys.sk2)
    # sc = SecureComputing(cp, csp)
    # # encrypt
    # enc_loc1 = loc1.enc(public_key)
    # enc_loc2 = loc2.enc(public_key)
    # # print(private_key.decrypt(enc_loc1.x), " ", private_key.decrypt(enc_loc1.y), " ", private_key.decrypt(enc_loc1.z))
    # # print(private_key.decrypt(enc_loc2.x), " ", private_key.decrypt(enc_loc2.y), " ", private_key.decrypt(enc_loc2.z))
    # enc_distant = sc.sdistance(enc_loc1, enc_loc2)
    # print(math.sqrt(private_key.decrypt(enc_distant)))



