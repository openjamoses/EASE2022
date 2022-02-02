import pandas as pd
import csv
import numpy as np
import operator
import os

from example.v2.RQ4.file_types_categories import file_categories, file_categories2, file_categories_dir

path_input = '/Volumes/Cisco/Summer2022/Docker/Dataset/v2/'
#path = '/Volumes/Cisco/Fall2021/Devops/Final-project/v2/docker-analyser/outputs/csv/'
path_output = '/Volumes/Cisco/Summer2022/Docker/Dataset/v2/RQ3/baseimages/'
path_csv = '/Volumes/Cisco/Summer2022/Docker/Dataset/v2/raw/Dockefile/'

df_data = pd.read_excel(open(path_input + 'combined_initial_ml_docker_repositories.xlsx', 'rb'), engine="openpyxl", sheet_name='filtered2')
#data.head()

#df_data = pd.read_csv(path_input+'tags_matching - final.csv')
repos_final = df_data.Repos.values.tolist()
topic = df_data.manual_topic.values.tolist()
#df_data = pd.read_csv(path_input+'input.csv')
#repos_ = df_data.Repos.values.tolist()
latest_imageL = df_data.latest_image.values.tolist()
repos_final2 = []
manual_topic2 = []
latest_imageL2 = []
for i in range(len(latest_imageL)):
    for val in eval(latest_imageL[i]):
        latest_imageL2.append(str(val).split(':')[0])
        repos_final2.append(repos_final[i])
        manual_topic2.append(topic[i])



#path_details = '/Volumes/Cisco/Fall2021/Devops/Final-project/v2/docker-analyser/dockerhub/outputs-server1/combine-layers/others/'
path_details = '/Volumes/Cisco/Summer2022/Docker/Dataset/downloads/combined/layers/'
path_output = '/Volumes/Cisco/Summer2022/Docker/Dataset/v2/RQ4/'
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


# path_details_layers = '/Volumes/Cisco/Fall2021/Devops/Final-project/v2/docker-analyser/dockerhub/outputs-server1/combine-layers/details/'
path_details = '/Volumes/Cisco/Summer2022/Docker/Dataset/downloads/combined/layers/'
path_output = '/Volumes/Cisco/Summer2022/Docker/Dataset/v2/RQ4/files/'

def check_extension(file_name, extension_):
    if str(extension_) == 'none':
        return file_name
    else:
        extension_ = str(extension_).replace('..', '.')
        flag = 0
        if '.' in extension_:

            for x in str(extension_).split('.'):
                try:
                    if str(x) != '':
                        int(x)
                except:
                    flag += 1
                    pass
        if flag > 0:
            return extension_
        else:
            return file_name

list_topic = set()
for cat in set(topic):
    list_topic.add(check_automl(cat))
CAT = [#'Toolkit',
       'DL Framwork',
       #'Model',
       # 'MLOps/ AIOps',
       'Application System']

search_for = [#'a9db9699ff4fe27071053b9ab84bce5abea7a3d3b4effc46cb18d46b',
              #'29c6859f0ee838dbbfa7c1b7b983b63456908f1ec919c87f7c42bb37',
              #'59289d1622a57731acff6181861325e771dee7a4ec15a9b349cab9fe',
              #'e0e10909911e0df1655a24b1bd415152da29e54deb70bf12a8f4f769',
              #'89d0bbe36a0f0ca557bad26c88606913c2a3e65d8a4521dc9b6c82b3',
              #'1a008818806306c066bce7f8ee317276859fbcaf08de19417f3f6b2f',
              #'a9db9699ff4fe27071053b9ab84bce5abea7a3d3b4effc46cb18d46b',
              # '29c6859f0ee838dbbfa7c1b7b983b63456908f1ec919c87f7c42bb37',
              '.11-2.1.2.3',
              '.3-199.1.2'
              ]
for cat in list_topic:
    if cat in CAT:
        cat_str = cat
        if '/' in cat:
            cat_str = str(cat_str).split('/')[0]

        print(cat)


        layers_size = {}
        image_layer_dict = {}
        image_layer_CLS_dict = {}
        #layers_num_category = {}
        dict_layer_size = {}
        dict_file_full_path = {}
        for repo_index in range(len(repos_final)):
            path_to_file = path_details + 'details/' + str(repos_final[repo_index])
            if cat == check_automl(topic[repo_index]) and os.path.exists(path_to_file):
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
                        for l_id in range(len(layer_digest)):
                            entension_str = check_extension(file_name[l_id], extension[l_id])
                            if entension_str in search_for:
                                print(entension_str, Image_[l_id],layer_digest[l_id], file_path[l_id])


