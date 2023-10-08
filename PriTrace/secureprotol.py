from encryption import paillier
import random
import time
import numpy as np
import multiprocessing



class SecureComputing(object):
    DEFAULT_SIGMA = 118

    def __init__(self, cp, csp):
        self.cp = cp
        self.csp = csp

    def sparalmul(self, evector1, evector2, n_len, sigm_len=None):

        pool = multiprocessing.Pool(processes=6)

        if len(evector1) != len(evector2):
            raise Exception('error operation! the dot product requires two vector has the same size')
        else:
            if sigm_len is None:
                sigm_len = self.DEFAULT_SIGMA

            evec_zip = zip(evector1, evector2)
            res = pool.starmap(self.smul, evec_zip)

            return res

    def sbatchdot_vector(self, evector1, evector2, n_len, sigm_len=None):

        if len(evector1) != len(evector2):
            raise Exception('error operation! the dot product requires two vector has the same size')
        else:
            if sigm_len is None:
                sigm_len = self.DEFAULT_SIGMA

            delta = n_len // (2 * sigm_len + 2 * 2)
            size = len(evector1)
            enc_dot = self.cp.public_key.encrypt(0.0)
            enc_dot.exponent = 44
            for i in range(0, size, delta):
                elist = []
                for j in range(i, i+delta):
                    elist.append(evector1[j])
                    elist.append(evector2[j])
                ciphertexts = self.batch_smul(elist)
                for k in range(len(ciphertexts)):
                    enc_dot = enc_dot + ciphertexts[k]

            return enc_dot

    def sdot_vector(self, evector1, evector2, sigm_len=None):

        if len(evector1) != len(evector2):
            raise Exception('error operation! the dot product requires two vector has the same size')
        else:
            if sigm_len is None:
                sigm_len = self.DEFAULT_SIGMA

            size = len(evector1)
            enc_dot = self.smul(evector1[0], evector2[0])
            for i in range(1, size):
                enc_dot = enc_dot + self.smul(evector1[i], evector2[i], sigm_len)

            return enc_dot

    def batchPDec(self, elist, L):

        delta = len(elist)
        eres = elist[0]
        for i in range(1, delta):
            eres = eres + (elist[i] * (L ** i))

        dres = self.csp.final_decrypt(self.cp.partial_decrypt(eres),
                                      self.csp.partial_decrypt(eres))

        plaintexts = []
        for i in range(delta):
            plaintexts.append(dres % (L ** (i+1)) // (L ** i))

        return plaintexts

    def sbatchdot(self, enc_qf, enc_gf, sigm_len=None):

        n_len = self.cp.public_key.n.bit_length()

        if sigm_len is None:
            sigm_len = self.DEFAULT_SIGMA

        size_probe = len(enc_qf)
        size_gallery = len(enc_gf)
        enc_q_g_dist = np.zeros((size_probe, size_gallery), dtype=paillier.EncryptedNumber)
        for i in range(size_probe):
            for j in range(size_gallery):
                enc_q_g_dist[i][j] = self.sbatchdot_vector(enc_qf[i], enc_gf[j], n_len, sigm_len)

        delta = n_len // 152
        L = 2 ** 152
        q_g_dist = np.zeros((size_probe, size_gallery), dtype=float)
        group = size_gallery // delta
        for i in range(size_probe):
            for t in range(group):
                elist = enc_q_g_dist[i][t * delta : (t + 1) * delta]
                plaintexts = self.batchPDec(elist, L)
                for k in range(len(plaintexts)):
                    q_g_dist[i][t * delta + k] = plaintexts[k]
            if group * delta < size_gallery:
                elist = enc_q_g_dist[i][group * delta: size_gallery]
                plaintexts = self.batchPDec(elist, L)
                for k in range(len(plaintexts)):
                    q_g_dist[i][group * delta + k] = plaintexts[k]

        """for i in range(size_probe):
            for j in range(size_gallery):
                q_g_dist[i][j] = self.csp.final_decrypt(self.cp.partial_decrypt(enc_q_g_dist[i][j]),
                                                        self.csp.partial_decrypt(enc_q_g_dist[i][j]))"""

        return enc_q_g_dist, q_g_dist

    def sparaldot(self, enc_qf, enc_gf, sigm_len=None):

        n_len = self.cp.public_key.n.bit_length()

        if sigm_len is None:
            sigm_len = self.DEFAULT_SIGMA

        size_probe = len(enc_qf)
        size_gallery = len(enc_gf)
        enc_q_g_dist = np.zeros((size_probe, size_gallery), dtype=paillier.EncryptedNumber)
        for i in range(size_probe):
            for j in range(size_gallery):
                res = self.sparalmul(enc_qf[i], enc_gf[j], sigm_len)
                enc_dot = res[0]
                for k in range(1, len(res)):
                    enc_dot = enc_dot + res[k]
                enc_q_g_dist[i][j] = enc_dot

        delta = n_len // 152
        L = 2 ** 152
        q_g_dist = np.zeros((size_probe, size_gallery), dtype=float)
        group = size_gallery // delta
        for i in range(size_probe):
            for t in range(group):
                elist = enc_q_g_dist[i][t * delta: (t + 1) * delta]
                plaintexts = self.batchPDec(elist, L)
                for k in range(len(plaintexts)):
                    q_g_dist[i][t * delta + k] = plaintexts[k]
            if group * delta < size_gallery:
                elist = enc_q_g_dist[i][group * delta: size_gallery]
                plaintexts = self.batchPDec(elist, L)
                for k in range(len(plaintexts)):
                    q_g_dist[i][group * delta + k] = plaintexts[k]

        return enc_q_g_dist, q_g_dist

    def sdot(self, enc_qf, enc_gf, sigm_len=None):

        if sigm_len is None:
            sigm_len = self.DEFAULT_SIGMA

        size_probe = len(enc_qf)
        size_gallery = len(enc_gf)
        enc_q_g_dist = np.zeros((size_probe, size_gallery), dtype=paillier.EncryptedNumber)
        for i in range(size_probe):
            for j in range(size_gallery):
                enc_q_g_dist[i][j] = self.sdot_vector(enc_qf[i], enc_gf[j], sigm_len)

        q_g_dist = np.zeros((size_probe, size_gallery), dtype=float)
        for i in range(size_probe):
            for j in range(size_gallery):
                q_g_dist[i][j] = self.cp.final_decrypt(self.cp.partial_decrypt(enc_q_g_dist[i][j]),
                                                       self.csp.partial_decrypt(enc_q_g_dist[i][j]))
        return enc_q_g_dist, q_g_dist

    def batch_smul(self, elist, sigm_len=None):

        bit_len = 0

        if sigm_len is None:
            sigm_len = self.DEFAULT_SIGMA

        L = 2 ** (sigm_len + 2)

        # Step-1
        rlist = []
        r = self.get_random_with_sigmbits(sigm_len)
        rlist.append(r)
        er = self.cp.public_key.encrypt(r)
        eRes = elist[0] + er
        for i in range(1, len(elist)):
            r = self.get_random_with_sigmbits(sigm_len)
            rlist.append(r)
            er = self.cp.public_key.encrypt(r)
            etmp = elist[i] + er
            etmp = etmp * (L ** i)
            eRes = eRes + etmp

        eRes1 = self.cp.partial_decrypt(eRes)
        bit_len += eRes1.ciphertext.bit_length()

        # Step-2
        eRes2 = self.csp.partial_decrypt(eRes)
        res = self.csp.final_decrypt(eRes1, eRes2)
        delta = len(elist) // 2
        eXY = []
        for i in range(delta):
            etmp = res % (L ** (2*i+2)) // (L ** (2*i))
            X = etmp // L
            Y = etmp % L
            eXY.append(self.csp.public_key.encrypt(X * Y))

            bit_len += eXY[i].ciphertext(False).bit_length()

        # Step-3
        ciphertexts = []
        for i in range(len(eXY)):
            er1_mul_r2 = self.cp.public_key.encrypt(rlist[2*i] * rlist[2*i+1])
            er1_mul_r2.exponent = elist[2*i].exponent
            if elist[2*i].exponent > 0:
                ciphertexts.append((eXY[i] + (elist[2*i] * - rlist[2*i+1]) + (elist[2*i+1] * -rlist[2*i]) - er1_mul_r2)
                                   / (10 ** elist[2*i].exponent))
            else:
                # return ex_add_r1_mul_y_add_r2 + (ev1 * -r2) + (ev2 * -r1) - er1_mul_r2, sum_time
                ciphertexts.append((eXY[i] + (elist[2*i] * - rlist[2*i+1]) + (elist[2*i+1] * -rlist[2*i]) - er1_mul_r2))

        return ciphertexts

    def smul(self, ev1, ev2, sigm_len=None):

        if ev1.public_key != ev2.public_key:
            raise Exception('an error operation')
        elif ev1.exponent != ev2.exponent:
            raise Exception('ev1 (ev1.exponent=%i) should has the same exponent with ev2 (ev2.exponent=%i)'
                            % (ev1.exponent, ev2.exponent))
        else:
            if sigm_len is None:
                sigm_len = self.DEFAULT_SIGMA

            # L = 10 ** (sigm_len // 3)
            L = 2 ** (sigm_len + 2)

            # Step-1
            # starTim = time.perf_counter()
            r1 = self.get_random_with_sigmbits(sigm_len)
            r2 = self.get_random_with_sigmbits(sigm_len)
            er1 = self.cp.public_key.encrypt(r1)
            er2 = self.cp.public_key.encrypt(r2)
            er1.exponent = er2.exponent = ev1.exponent

            ev1_add_r1 = ev1 + er1
            ev2_add_r2 = ev2 + er2
            eRes = (ev1_add_r1 * L) + ev2_add_r2
            eRes1 = self.cp.partial_decrypt(eRes)
            # sum_time = time.perf_counter() - starTim

            # Step-2
            # starTim = time.perf_counter()
            eRes2 = self.csp.partial_decrypt(eRes)
            Res = self.csp.final_decrypt(eRes1, eRes2)
            x_add_r1 = Res // L
            y_add_r2 = Res % L
            ex_add_r1_mul_y_add_r2 = self.csp.public_key.encrypt(x_add_r1 * y_add_r2)
            ex_add_r1_mul_y_add_r2.exponent = eRes.exponent
            # sum_time += time.perf_counter() - starTim

            # Step-3
            er1_mul_r2 = self.cp.public_key.encrypt(r1 * r2)
            er1_mul_r2.exponent = ev1.exponent
            if ev1.exponent > 0:
                # return (ex_add_r1_mul_y_add_r2 + (ev1 * -r2) + (ev2 * -r1) - er1_mul_r2) / (10 ** ev1.exponent), sum_time
                return (ex_add_r1_mul_y_add_r2 + (ev1 * -r2) + (ev2 * -r1) - er1_mul_r2) / (10 ** ev1.exponent)
            else:
                # return ex_add_r1_mul_y_add_r2 + (ev1 * -r2) + (ev2 * -r1) - er1_mul_r2, sum_time
                return ex_add_r1_mul_y_add_r2 + (ev1 * -r2) + (ev2 * -r1) - er1_mul_r2

    def conv_smul(self, ev1, ev2, sigm_len=None):

        bit_len = 0
        if ev1.public_key != ev2.public_key:
            raise Exception('an error operation')
        elif ev1.exponent != ev2.exponent:
            raise Exception('ev1 (ev1.exponent=%i) should has the same exponent with ev2 (ev2.exponent=%i)'
                            % (ev1.exponent, ev2.exponent))
        else:
            if sigm_len is None:
                sigm_len = self.DEFAULT_SIGMA

            startTim = time.perf_counter()
            # Step-1
            r1 = self.get_random_with_sigmbits(sigm_len)
            r2 = self.get_random_with_sigmbits(sigm_len)
            er1 = self.cp.public_key.encrypt(r1)
            er2 = self.cp.public_key.encrypt(r2)
            er1.exponent = er2.exponent = ev1.exponent

            X = ev1 + er1
            Y = ev2 + er2
            X1 = self.cp.partial_decrypt(X)
            Y1 = self.cp.partial_decrypt(Y)

            bit_len += X1.ciphertext.bit_length()
            bit_len += Y1.ciphertext.bit_length()
            sum_time = time.perf_counter() - startTim

            startTim = time.perf_counter()
            # Step-2
            X2 = self.csp.partial_decrypt(X)
            Y2 = self.csp.partial_decrypt(Y)
            x_add_r1 = self.csp.final_decrypt(X1, X2)
            y_add_r2 = self.csp.final_decrypt(Y1, Y2)
            ex_add_r1_mul_y_add_r2 = self.csp.public_key.encrypt(x_add_r1 * y_add_r2)
            ex_add_r1_mul_y_add_r2.exponent = X.exponent

            bit_len += ex_add_r1_mul_y_add_r2.ciphertext(False).bit_length()

            sum_time += time.perf_counter() - startTim

            startTim = time.perf_counter()
            # Step-3
            er1_mul_r2 = self.cp.public_key.encrypt(r1 * r2)
            er1_mul_r2.exponent = ev1.exponent
            if ev1.exponent > 0:
                res = (ex_add_r1_mul_y_add_r2 + (ev1 * -r2) + (ev2 * -r1) - er1_mul_r2) / (10 ** ev1.exponent)
                sum_time += time.perf_counter() - startTim
                return res, sum_time
            else:
                res = ex_add_r1_mul_y_add_r2 + (ev1 * -r2) + (ev2 * -r1) - er1_mul_r2
                sum_time += time.perf_counter() - startTim
                return res, sum_time

    def get_random_with_sigmbits(self, sigm_len):
        """Return a cryptographically random number less than :attr:`n`"""
        return random.SystemRandom().randrange(1 << sigm_len - 1, 1 << sigm_len)


if __name__ == '__main__':

    """public_key, private_key, partial_private_keys = paillier.generate_paillier_keypair(n_length=512)

    cp = paillier.ThresholdPaillier(public_key, partial_private_keys.sk1)
    csp = paillier.ThresholdPaillier(public_key, partial_private_keys.sk2)
    sc = SecureComputing(cp, csp)"""

    """qf = np.zeros((1,3), dtype=float)
    gf = np.zeros((5,3), dtype=float)
    enc_qf = np.zeros((1,3), dtype=paillier.EncryptedNumber)
    enc_gf = np.zeros((5,3), dtype=paillier.EncryptedNumber)
    for i in range(len(qf)):
        for j in range(len(qf[i])):
            qf[i][j] = i + j * 1.2
            enc_qf[i][j] = public_key.encrypt(qf[i][j])
    print(qf)
    for i in range(len(gf)):
        for j in range(len(gf[i])):
            gf[i][j] = i + j * 1.3
            enc_gf[i][j] = public_key.encrypt(gf[i][j])
    print(gf)

    enc_q_g_dist, q_g_dist1 = sc.sdot(enc_qf, enc_gf)
    for i in range(len(enc_q_g_dist)):
        for j in range(len(enc_q_g_dist[i])):
            print(private_key.decrypt(enc_q_g_dist[i][j]), q_g_dist1[i][j])"""

    for k in range(2, 9):
        n_len = 256 * k
        public_key, private_key, partial_private_keys = paillier.generate_paillier_keypair(n_length=n_len)

        cp = paillier.ThresholdPaillier(public_key, partial_private_keys.sk1)
        csp = paillier.ThresholdPaillier(public_key, partial_private_keys.sk2)
        sc = SecureComputing(cp, csp)

        count = n_len // 240
        evals = []
        for i in range(count * 2):
            evals.append(public_key.encrypt(random.random()))

        print('--------', n_len)
        #print('----------Conv_SMUL-------------')
        start = time.perf_counter()
        for t in range(10):
            for j in range(0, count * 2, 2):
                sc.conv_smul(evals[j], evals[j + 1])
        print(round((time.perf_counter() - start) * 100))

        #print('----------Ours_SMUL-------------')
        start = time.perf_counter()
        for t in range(10):
            for j in range(0, count * 2, 2):
                sc.smul(evals[j], evals[j + 1])
        print(round((time.perf_counter() - start) * 100))


        #print('----------BatchSMUL-------------')
        start = time.perf_counter()
        for t in range(10):
            sc.batch_smul(evals)
        print(round((time.perf_counter() - start) * 100))


        """LEN = 78
        L = 2 ** LEN
        delta = n_len // LEN
        print(delta)
        evals = []
        for i in range(delta):
            evals.append(public_key.encrypt(random.random()))"""

        """print('--------', n_len)
        #print('-----PDec-----')
        start = time.perf_counter()
        for t in range(10):
            for j in range(delta):
                ev1 = cp.partial_decrypt(evals[j])
                ev2 = csp.partial_decrypt(evals[j])
                csp.final_decrypt(ev1, ev2)
        print(round((time.perf_counter() - start) * 100))

        #print('-------BatchPDec--------')
        start = time.perf_counter()
        for t in range(10):
            for i in range(delta):
                res = evals[i] * (L ** i)

            res1 = cp.partial_decrypt(res)
            res2 = csp.partial_decrypt(res)
            csp.final_decrypt(res1, res2)
        print(round((time.perf_counter() - start) * 100))"""

    """print('----------Conv_SMUL-------------')
    f_x = random.random()
    f_y = random.random()
    ev1 = public_key.encrypt(f_x)
    ev2 = public_key.encrypt(f_y)

    print(private_key.decrypt(sc.conv_smul(ev1, ev2)[0]) == f_x * f_y)
    print(private_key.decrypt(sc.smul(ev1, ev2)) == f_x * f_y)
    #sc.conv_smul(ev1, ev2)"""

    """print('----------BatchSMUL-------------')
    elist = []
    delta = 2048 // 240
    for i in range(delta):
        f_x = random.random()
        f_y = random.random()
        ev1 = public_key.encrypt(f_x)
        ev2 = public_key.encrypt(f_y)
        elist.append(ev1)
        elist.append(ev2)
    sc.batch_smul(elist)"""

    """print('-------PDec--------')
    f_x = random.random()
    ev = public_key.encrypt(f_x)
    ev1 = cp.partial_decrypt(ev)
    print(ev1.ciphertext.bit_length() / 8 / 1024)

    print('-------BatchPDec--------')
    LEN = 78
    L = 2 ** LEN
    delta = 2048 // LEN
    for i in range(delta):
        f_x = random.random()
        ev = public_key.encrypt(f_x)
        res = ev * (L ** i)

    res1 = cp.partial_decrypt(res)
    print(res1.ciphertext.bit_length() / 8 / 1024 / delta)"""


    """count_mul = count_cmp = 0
    conv_time = imp_time = 0
    for i in range(100):
        f_x = random.random()
        f_y = random.random()
        if i % 4 == 1:
            f_x = f_x * -1
        if i % 4 == 2:
            f_y = f_y * -1
        if i % 4 == 3:
            f_x = f_x * -1
            f_y = f_y * -1
        ev1 = public_key.encrypt(f_x)
        ev2 = public_key.encrypt(f_y)
        conv_time += sc.conv_smul(ev1, ev2)[1]
        imp_time += sc.smul(ev1, ev2)[1]
        if private_key.decrypt(sc.conv_smul(ev1, ev2)) != f_x * f_y:
            count_mul += 1
        if private_key.decrypt(sc.scmp(public_key.encrypt(f_x), public_key.encrypt(f_y))) == 0:
            count_cmp += 1
    print(count_mul, count_cmp)
    print(conv_time / 100, imp_time / 100)"""


