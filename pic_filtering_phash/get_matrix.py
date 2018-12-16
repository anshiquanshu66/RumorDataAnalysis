# encoding:utf-8

import numpy as np
import imagehash
from PIL import Image
from sklearn.externals import joblib
import time
import os


def get_phash_table(image_paths, sz):
    phash_list = []

    start_time = time.time()
    for i in range(sz):
        phash_list.append(imagehash.phash(Image.open(image_paths[i])))
        if i % 50 == 0:
            print('Img {}/{} Done. It took {:.1f}s...'.format(i + 1, sz, time.time() - start_time))
            start_time = time.time()

    joblib.dump(phash_list, 'pkl/phash_list_{}.pkl'.format(sz))


def similarity_distance(p_hash1, p_hash2):
    similarity = 1 - (p_hash1 - p_hash2) / len(p_hash1.hash) ** 2
    return similarity


def get_similarity_matrix(sz):
    print('Get Started Generating Matrix...')

    phash_list = joblib.load('pkl/phash_list_{}.pkl'.format(sz))
    matrix = np.zeros((sz, sz))

    start_time = time.time()
    for i in range(sz):
        for j in range(i + 1, sz):
            matrix[i][j] = similarity_distance(phash_list[i], phash_list[j])

        if i % 50 == 0:
            print('----------------------------------------------')
            print('Handling matrix the {}/{} lines...'.format(i + 1, sz))
            print('It takes {:.1f}s'.format(time.time() - start_time))
            start_time = time.time()

    joblib.dump(matrix, 'pkl/matrix_{}.pkl'.format(sz))


# 先撤回mv
def recover():
    src_dir = '../../pics_filtered_img_rumor_filtered'
    des_dir = '../../test'
    for root, dirs, files in os.walk(src_dir):
        for file in files:
            img = file.split('-')[1]
            os.system('mv {} {}'.format(os.path.join(src_dir, file), os.path.join(des_dir, img)))


def choose_sampling_truth():
    src_dir = '../../pics_sampling_img_truth'
    out_dir = '../../truth_filtered'

    rumor_pics_num = 17588
    truth_pics_num = 21749

    all_files = []
    rm_files = []
    for _, _, files in os.walk(src_dir):
        all_files = files.copy()
        for file in files:
            if '.jpg' not in file:
                rm_files.append(file)
                all_files.remove(file)
    print('After removing N-JPG files, all_files={}, rm_files={}'.format(len(all_files), len(rm_files)))

    rm_num = truth_pics_num - rumor_pics_num - len(rm_files) - random.randint(0, 500)
    rm_files += random.sample(all_files, rm_num)

    print('Get Started Sampling, rm_files = {}'.format(len(rm_files)))

    # mv cmd
    for rm_file in rm_files:
        os.system('mv {} {}'.format(os.path.join(src_dir, rm_file), out_dir))

    print('Moving Successfully, and [{} truth-imgs | {} rumor-imgs] remained.'.format(
        truth_pics_num - len(rm_files), rumor_pics_num))