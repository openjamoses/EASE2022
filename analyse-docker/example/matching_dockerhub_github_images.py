import operator

import pandas as pd
import csv
import os
import numpy as np
path = '/Volumes/Cisco/Fall2021/Devops/Final-project/v2/data/selected/'
path_details = '../outputs/csv/processed/'

df_data = pd.read_csv(path+'Manifest_details_1.csv')
Image = df_data.Image.values.tolist()
config_size = df_data.config_size.values.tolist()
RepoTag = df_data.RepoTag.values.tolist()
layers_digest = df_data.layers_digest.values.tolist()
layers_size = df_data.layers_size.values.tolist()


data_file = open(path + 'MLDocker_statistics.csv', mode='w', newline='',
                                  encoding='utf-8')
data_writer = csv.writer(data_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
data_writer.writerow(['Repo','topic','GHTags','DHTags','layers_digest','layer_total_size', 'layer_median_size', 'layer_mean_size', 'layer_min_size', 'layer_max_size', 'layer_median_level', 'layer_mean_level', 'layer_min_level', 'layer_max_level','total_dockerfiles','base_images', 'top5_options', 'top5_instructions'])


digest_list = []
for digest in layers_digest:
    #print(digest, digest[digest.index(':'): len(digest)])
    digest_list.append(digest[digest.index(':')+1: len(digest)])

#Image = df_data.Image.values.tolist()
#Image = df_data.Image.values.tolist()

for doker_image in set(Image):
    print(doker_image)
    if '/' in str(doker_image):
        image_name = str(doker_image).split('/')[0]
    if '/' in str(image_name):
        image_name = str(image_name).replace('/', '_')
    df_layers = pd.read_csv(path + 'details/Image_layers_info_1_{}.csv'.format(image_name))
    Image_ = df_layers.Image.values.tolist()
    RepoTag_ = df_layers.RepoTag.values.tolist()
    layer_digest_ = df_layers.layer_digest.values.tolist()
    file_name_ = df_layers.file_name.values.tolist()
    file_path_ = df_layers.file_path.values.tolist()
    file_size_ = df_layers.file_size.values.tolist()
    extension_ = df_layers.extension.values.tolist()
    level_ = df_layers.level.values.tolist()

    file_size_data = {}
    file_size_type_data = {}
    level_data = {}
    for i in range(len(Image)):
        if Image[i] == doker_image:
            for j in range(len(Image_)):
                if layer_digest_[j] == digest_list[i]:
                    if layers_digest[i] in file_size_data.keys():
                        file_size_data[digest_list[i]] = file_size_data[digest_list[i]].append(file_size_[j])
                        level_data[digest_list[i]] = level_data[digest_list[i]].append(level_[j])
                        if extension_[j] in file_size_type_data.get(digest_list[i]).keys():
                            file_size_type_data[digest_list[i]][extension_[j]] = file_size_type_data[digest_list[i]][extension_[j]].append(file_size_[j])
                        else:
                            file_size_type_data[digest_list[i]][extension_[j]] = [file_size_[j]]
                    else:
                        file_size_data[digest_list[i]] = [file_size_[j]]
                        level_data[digest_list[i]] = [level_[j]]
                        file_size_type_data[digest_list[i]] = {}
                        file_size_type_data[digest_list[i]][extension_[j]] = [file_size_[j]]
                    #print('yes: ', layer_digest_[i])
                #else:
                #    print('    ---: ', layer_digest_[i], ' not found')
    for key, val in file_size_data.items():
        data_writer.writerow(
            ['', '', '', RepoTag[i], key, np.sum(file_size_data.get(key)), np.median(val),
             np.mean(val), np.min(val), np.max(val), np.median(level_data.get(key)), np.mean(level_data.get(key)),
             np.min(level_data.get(key)), np.max(level_data.get(key)), '', '', '',
             ''])
data_file.close()
