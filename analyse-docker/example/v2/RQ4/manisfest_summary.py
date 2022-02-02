import os
import pandas as pd
import numpy as np
import csv
import math
def convert_size(size_bytes):
    if size_bytes == 0:
        #return "0B"
        return 0
    size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
    i = int(math.floor(math.log(size_bytes, 1024)))
    p = math.pow(1024, i)
    s = round(size_bytes / p, 2)
    #return "%s %s" % (s, size_name[i])
    return s
def check_automl(topic_):
    Lib_data = {'Toolkit': ['AutoML','automl', 'Machine Learning', 'tool'],
               'Model':['model'],
               'Documentation':['tutorials/ documentation'],
               'Application System': ['application', 'application/autopilot'],
               'MLOps/ AIOps':['mlops'],
               'DL Framwork':['DL framwork']}
    topic = topic_
    for key, val in Lib_data.items():
        if topic_ in val:
            topic = key
            break
    return topic
path_details = '/Volumes/Cisco/Summer2022/Docker/Dataset/downloads/combined/layers/'
path_input = '/Volumes/Cisco/Summer2022/Docker/Dataset/v2/'
path_output = '/Volumes/Cisco/Summer2022/Docker/Dataset/v2/general/'
df_data = pd.read_excel(open(path_input + 'combined_initial_ml_docker_repositories.xlsx', 'rb'), engine="openpyxl", sheet_name='filtered2')
#data.head()

#df_data = pd.read_csv(path_input+'tags_matching - final.csv')
repos_final = df_data.Repos.values.tolist()
topic = df_data.manual_topic.values.tolist()
latest_imageL = df_data.latest_image.values.tolist()
repos_final2 = []
manual_topic2 = []
latest_imageL2 = []
for i in range(len(latest_imageL)):
    for val in eval(latest_imageL[i]):
        latest_imageL2.append(str(val).split(':')[0])
        repos_final2.append(repos_final[i])
        manual_topic2.append(topic[i])

repos_manifest_data = {}
list_dir = [dir for dir in os.listdir(path_details) if 'Manifest_Config_info' in str(dir)]
# list_dir
for file_ in list_dir:
    df = pd.read_csv(path_details + file_)
    # print(df.columns)
    Image = df.Image.values.tolist()
    config_size = df.config_size.values.tolist()
    architecture = df.architecture.values.tolist()
    os_ = df.os.values.tolist()
    config_env_count = df.config_env_count.values.tolist()
    rootfs_layers_count = df.rootfs_layers_count.values.tolist()
    history = df.rootfs_layers.values.tolist()
    for i in range(len(Image)):
        if Image[i] in latest_imageL2:
            repos = repos_final2[latest_imageL2.index(Image[i])]
            if repos in repos_manifest_data.keys():
                repos_manifest_data[repos].append([config_size[i], architecture[i], os_[i], config_env_count[i], rootfs_layers_count[i], history[i]])
            else:
                repos_manifest_data[repos] = [
                    [config_size[i], architecture[i], os_[i], config_env_count[i], rootfs_layers_count[i], history[i]]]
list_dir = [dir for dir in os.listdir(path_details) if 'Manifest_details' in str(dir)]
manifest_digest_data = {}
manifest_layers_digest_data = {}
list_layers = []
for file_ in list_dir:
    df = pd.read_csv(path_details + file_)
    Image = df.Image.values.tolist()
    layer_digest = df.layers_digest.values.tolist()
    layers_size = df.layers_size.values.tolist()
    for i in range(len(Image)):
        if Image[i] in latest_imageL2:
            repos = repos_final2[latest_imageL2.index(Image[i])]
            if repos in manifest_layers_digest_data.keys():
                if Image[i] in manifest_layers_digest_data[repos].keys():
                    manifest_layers_digest_data[repos][Image[i]] += layers_size[i]
                else:
                    manifest_layers_digest_data[repos][Image[i]] = layers_size[i]
            else:
                manifest_layers_digest_data[repos] = {}
                manifest_layers_digest_data[repos][Image[i]] = layers_size[i]
            if repos in manifest_digest_data.keys():
                manifest_digest_data[repos].add(layer_digest[i])
            else:
                manifest_digest_data[repos] = set([layer_digest[i]])

data_file = open(path_output + 'Docker_images_statistics_.csv', mode='w', newline='', encoding='utf-8')
data_writer = csv.writer(data_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
data_writer.writerow(['Category', 'configsize', 'architecture', 'os', 'environment', 'layers','layers_size', 'rootfs_layers', 'files', 'max_level'])

#print(manifest_digest_data)
#print(repos_manifest_data)
list_topic = set()
for cat in set(topic):
    list_topic.add(check_automl(cat))

for cat in list_topic:
    #if not 'remove' in cat:
    config_size_data = {}
    architecture_data = set()
    os_data = set()
    config_env_count_data = {}
    history_data = {}
    layers_data = {}
    rootfs_layers_data = {}

    dict_num_files = {}
    dict_level_files = {}
    dict_manifest_conf_info = {}
    layets_list_data = []
    layets_list_data_size = []

    print(cat)

    for repo_index in range(len(repos_final)):
        path_to_file = path_details + 'details/' + str(repos_final[repo_index])
        if cat == check_automl(topic[repo_index]) and os.path.exists(path_to_file):
            if repos_final[repo_index] in repos_manifest_data.keys():
                data_repo = repos_manifest_data.get(repos_final[repo_index])
                #print(data_repo)
                #for key, val in data_repo.items():
                key = repos_final[repo_index]
                for data_ in data_repo:
                    architecture_data.add(data_[1])
                    os_data.add(data_[2])
                    if key in config_size_data.keys():
                        config_size_data[key] += data_[0]
                        config_env_count_data[key] += data_[3]
                        rootfs_layers_data[key] += len(data_[4].split('/'))
                        # print(history_list[image_index])
                        # history_data[image] += history_list[image_index]
                    else:
                        config_size_data[key] = data_[0]
                        config_env_count_data[key] = data_[3]
                        rootfs_layers_data[key] = len(data_[4].split('/'))

            if repos_final[repo_index] in manifest_digest_data.keys():
                layets_list_data.append(len(manifest_digest_data.get(repos_final[repo_index])))
                layets_list_data_size.append(np.mean(list(manifest_layers_digest_data[repos_final[repo_index]].values())))
            if os.path.exists(path_to_file):
                list_dir_ = [dir_ for dir_ in os.listdir(path_to_file) if 'Image_layers_info' in str(dir_)]
                for dir_ in list_dir_:
                    data = pd.read_csv(path_to_file + '/' + dir_)
                    Image_ = data.Image.values.tolist()
                    layer_digest = data.layer_digest.values.tolist()
                    file_name = data.file_name.values.tolist()
                    file_size = data.file_size.values.tolist()
                    extension = data.extension.values.tolist()
                    file_path = data.file_path.values.tolist()
                    file_level= data.level.values.tolist()
                    level_list = []
                    #print(file_level)
                    for lev_ in file_level:
                        if str(lev_) != 'nan':
                            level_list.append(lev_)
                    if len(level_list)> 0:
                        dict_level_files[repos_final[repo_index]] = np.max(level_list)
                    #print(file_level)
                    if len(level_list) > 0:
                        if repos_final[repo_index] in dict_num_files.keys():
                            dict_num_files[repos_final[repo_index]] += len(file_size)
                        else:
                            dict_num_files[repos_final[repo_index]] = len(file_size)

    #print(config_size_data)
    data_writer.writerow(
        [cat, convert_size(np.median(list(config_size_data.values()))), architecture_data, os_data, np.median(list(config_env_count_data.values())), np.median(layets_list_data), np.median(layets_list_data_size), np.median(list(rootfs_layers_data.values())), np.median(list(dict_num_files.values())),
         np.median(list(dict_level_files.values()))])


data_file.close()