import time

import numpy as np
import random
import torch
import multiprocessing

from encryption import paillier
from model.opt import opt
from model_util import loadNetwork, extractFeatures, extractFeature, list_pictures
from secureprotol import SecureComputing

if __name__ == '__main__':

    model = loadNetwork(opt.weight)
    print('model loading success!')

    queryPath = 'D:\\python-workspace\\datasets\\Market-1501\\query1'
    probe = list_pictures(queryPath)
    qf = extractFeatures(model, probe)

    pool = multiprocessing.Pool(processes=6)
    public_key, private_key, partial_private_keys = paillier.generate_paillier_keypair(n_length=1024)

    # encrypt query
    qf_numpy = qf.numpy()
    enc_qf = np.zeros((len(qf_numpy), len(qf_numpy[0])), dtype=paillier.EncryptedNumber)
    for i in range(len(qf_numpy)):
        qf_val = []
        for j in range(len(qf_numpy[i])):
            qf_val.append(qf_numpy[i][j].item())
        enc_qf[i] = pool.map(public_key.encrypt, qf_val)

    cp = paillier.ThresholdPaillier(public_key, partial_private_keys.sk1)
    csp = paillier.ThresholdPaillier(public_key, partial_private_keys.sk2)
    sc = SecureComputing(cp, csp)

    print('----------gallery10-----------')
    galleryPath = 'D:\\python-workspace\\datasets\\Market-1501\\num_gallery\\gallery10'
    gallery = list_pictures(galleryPath)
    gf = extractFeatures(model, gallery)
    g_g_dist = np.dot(gf, np.transpose(gf))
    k = len(gallery) // 2
    g_dist_k = np.zeros(len(gallery))
    for i in range(len(gallery)):
        g_dist_k[i] = float(sorted(g_g_dist[i], reverse=True)[k:k + 1][0])

    # encrypt gallery
    gf_numpy = gf.numpy()
    enc_gf = np.zeros((len(gf_numpy), len(gf_numpy[0])), dtype=paillier.EncryptedNumber)
    for i in range(len(gf_numpy)):
        gf_val = []
        for j in range(len(gf_numpy[i])):
            gf_val.append(gf_numpy[i][j].item())
        enc_gf[i] = pool.map(public_key.encrypt, gf_val)

    start = time.perf_counter()
    for t in range(2):
        enc_q_g_dist, q_g_dist1 = sc.sparaldot(enc_qf, enc_gf)


        for j in range(len(q_g_dist1)):
            initial_rank = np.argpartition(-q_g_dist1[j], range(k))[:k]
            count = 0
            for index in initial_rank:
                if q_g_dist1[j][index] >= g_dist_k[index] * 2 ** 106:
                    count += 1

    print(round((time.perf_counter() - start) / 2))

    print('----------gallery12-----------')
    galleryPath = 'D:\\python-workspace\\datasets\\Market-1501\\num_gallery\\gallery12'
    gallery = list_pictures(galleryPath)
    gf = extractFeatures(model, gallery)
    g_g_dist = np.dot(gf, np.transpose(gf))
    k = len(gallery) // 2
    g_dist_k = np.zeros(len(gallery))
    for i in range(len(gallery)):
        g_dist_k[i] = float(sorted(g_g_dist[i], reverse=True)[k:k + 1][0])

    # encrypt gallery
    gf_numpy = gf.numpy()
    enc_gf = np.zeros((len(gf_numpy), len(gf_numpy[0])), dtype=paillier.EncryptedNumber)
    for i in range(len(gf_numpy)):
        gf_val = []
        for j in range(len(gf_numpy[i])):
            gf_val.append(gf_numpy[i][j].item())
        enc_gf[i] = pool.map(public_key.encrypt, gf_val)

    start = time.perf_counter()
    for t in range(2):
        enc_q_g_dist, q_g_dist1 = sc.sparaldot(enc_qf, enc_gf)

        for j in range(len(q_g_dist1)):
            initial_rank = np.argpartition(-q_g_dist1[j], range(k))[:k]
            count = 0
            for index in initial_rank:
                if q_g_dist1[j][index] >= g_dist_k[index] * 2 ** 106:
                    count += 1

    print(round((time.perf_counter() - start) / 2))

    print('----------gallery14-----------')
    galleryPath = 'D:\\python-workspace\\datasets\\Market-1501\\num_gallery\\gallery14'
    gallery = list_pictures(galleryPath)
    gf = extractFeatures(model, gallery)
    g_g_dist = np.dot(gf, np.transpose(gf))
    k = len(gallery) // 2
    g_dist_k = np.zeros(len(gallery))
    for i in range(len(gallery)):
        g_dist_k[i] = float(sorted(g_g_dist[i], reverse=True)[k:k + 1][0])

    # encrypt gallery
    gf_numpy = gf.numpy()
    enc_gf = np.zeros((len(gf_numpy), len(gf_numpy[0])), dtype=paillier.EncryptedNumber)
    for i in range(len(gf_numpy)):
        gf_val = []
        for j in range(len(gf_numpy[i])):
            gf_val.append(gf_numpy[i][j].item())
        enc_gf[i] = pool.map(public_key.encrypt, gf_val)

    start = time.perf_counter()
    for t in range(2):
        enc_q_g_dist, q_g_dist1 = sc.sparaldot(enc_qf, enc_gf)

        for j in range(len(q_g_dist1)):
            initial_rank = np.argpartition(-q_g_dist1[j], range(k))[:k]
            count = 0
            for index in initial_rank:
                if q_g_dist1[j][index] >= g_dist_k[index] * 2 ** 106:
                    count += 1

    print(round((time.perf_counter() - start) / 2))

    print('----------gallery16-----------')
    galleryPath = 'D:\\python-workspace\\datasets\\Market-1501\\num_gallery\\gallery16'
    gallery = list_pictures(galleryPath)
    gf = extractFeatures(model, gallery)
    g_g_dist = np.dot(gf, np.transpose(gf))
    k = len(gallery) // 2
    g_dist_k = np.zeros(len(gallery))
    for i in range(len(gallery)):
        g_dist_k[i] = float(sorted(g_g_dist[i], reverse=True)[k:k + 1][0])

    # encrypt gallery
    gf_numpy = gf.numpy()
    enc_gf = np.zeros((len(gf_numpy), len(gf_numpy[0])), dtype=paillier.EncryptedNumber)
    for i in range(len(gf_numpy)):
        gf_val = []
        for j in range(len(gf_numpy[i])):
            gf_val.append(gf_numpy[i][j].item())
        enc_gf[i] = pool.map(public_key.encrypt, gf_val)

    start = time.perf_counter()
    for t in range(2):
        enc_q_g_dist, q_g_dist1 = sc.sparaldot(enc_qf, enc_gf)

        for j in range(len(q_g_dist1)):
            initial_rank = np.argpartition(-q_g_dist1[j], range(k))[:k]
            count = 0
            for index in initial_rank:
                if q_g_dist1[j][index] >= g_dist_k[index] * 2 ** 106:
                    count += 1

    print(round((time.perf_counter() - start) / 2))

    print('----------gallery20-----------')
    galleryPath = 'D:\\python-workspace\\datasets\\Market-1501\\num_gallery\\gallery20'
    gallery = list_pictures(galleryPath)
    gf = extractFeatures(model, gallery)
    g_g_dist = np.dot(gf, np.transpose(gf))
    k = len(gallery) // 2
    g_dist_k = np.zeros(len(gallery))
    for i in range(len(gallery)):
        g_dist_k[i] = float(sorted(g_g_dist[i], reverse=True)[k:k + 1][0])

    # encrypt gallery
    gf_numpy = gf.numpy()
    enc_gf = np.zeros((len(gf_numpy), len(gf_numpy[0])), dtype=paillier.EncryptedNumber)
    for i in range(len(gf_numpy)):
        gf_val = []
        for j in range(len(gf_numpy[i])):
            gf_val.append(gf_numpy[i][j].item())
        enc_gf[i] = pool.map(public_key.encrypt, gf_val)

    start = time.perf_counter()
    for t in range(2):
        enc_q_g_dist, q_g_dist1 = sc.sparaldot(enc_qf, enc_gf)

        for j in range(len(q_g_dist1)):
            initial_rank = np.argpartition(-q_g_dist1[j], range(k))[:k]
            count = 0
            for index in initial_rank:
                if q_g_dist1[j][index] >= g_dist_k[index] * 2 ** 106:
                    count += 1

    print(round((time.perf_counter() - start) / 2))




