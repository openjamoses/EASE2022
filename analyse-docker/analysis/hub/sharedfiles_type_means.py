import operator

import pandas as pd
import csv
import numpy as np
import os
path_input = '/Volumes/Cisco/Fall2021/Devops/Final-project/v2/docker-analyser/'
path = '/Volumes/Cisco/Fall2021/Devops/Final-project/v2/docker-analyser/outputs/csv/'
path_output = '/Volumes/Cisco/Fall2021/Devops/Final-project/v2/docker-analyser/outputs/csv/analysis/processed/'
path_tag_log = '/Volumes/Cisco/Fall2021/Devops/Final-project/v2/docker-analyser/outputs/logs/'
df_input = pd.read_csv(path_input+'selected.csv')
Repo = df_input.Repos.values.tolist()
docker_image = df_input.docker_image.values.tolist()
manual_topic = df_input.manual_topic.values.tolist()

path_download = '/Volumes/Cisco/Fall2021/Devops/Final-project/v2/docker-analyser/dockerhub/outputs/dockerhub/downloads'

path_layer = '/Volumes/Cisco/Fall2021/Devops/Final-project/v2/docker-analyser/dockerhub/outputs/layers/'

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
#path = './images'
if not os.path.exists(ROOT_DIR+'/outputs'):
    os.makedirs(ROOT_DIR+'/outputs')
if not os.path.exists(ROOT_DIR+'/outputs/dockerhub'):
    os.makedirs(ROOT_DIR+'/outputs/dockerhub')
#if not os.path.exists('../outputs/dockerhub/dockerimages'):
#    os.makedirs('../outputs/dockerhub/dockerimages')
path_download = ROOT_DIR+'/outputs/dockerhub/downloads'
if not os.path.exists(path_download):
    os.makedirs(path_download)
path = ROOT_DIR+'/outputs/dockerhub'
def check_isnumeric(val):
    is_numeric = False
    try:
        if '.' in str(val):
            val = str(val).replace('.','')
        float(str(val))
        is_numeric = True
    except:
        pass
    return is_numeric
def get_layers(data):
    topic_dict = {'mlops': 'MLops', 'application': 'Application', 'tool': 'ToolKit', 'AutoML': 'AutoML',
                  'Machine Learning': 'Machine Learning',
                  'tutorials/ documentation': 'Documentation', 'model': 'Model', 'DL framwork': 'DL Framwork'}

    dict_topic_repo = {}
    for top in set(manual_topic):
        list_repo = set()
        for i in range(len(Repo)):
            if top == manual_topic[i]:
                list_repo.add(Repo[i])
        dict_topic_repo[topic_dict.get(top)] = list(list_repo)
    for top in set(manual_topic):
        data_file = open(path_output + '/RQ1b/processed_{}_mean.csv'.format(topic_dict.get(top).lower()), mode='w', newline='',
                         encoding='utf-8')
        data_writer = csv.writer(data_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        data_writer.writerow(['Topic', 'Repos', 'ProjectID', 'FileType', 'Sharedfiles', 'Memory'])

        for repo, images_lists in data.items():
            if manual_topic[Repo.index(repo)] == top:
                for doker_image in images_lists:
                    shared_files_data = {}
                    memory_files_data = {}
                    total_files_data = {}
                    total_memory_files_data = {}
                    extension_data = {}
                    flag = 0
                    for i in range(11):
                        image_name = doker_image
                        if '/' in str(doker_image):
                            image_name = str(doker_image).split('/')[0]
                        if '/' in str(image_name):
                            image_name = str(image_name).replace('/', '_')
                        #pd_layers = pd.read_csv(path_layer+'layers{}/Image_layers_info_1_{}.csv'.format(i))


                        if os.path.exists(path_layer+'layers{}/details/Image_layers_info_1_{}.csv'.format(i, image_name)):
                            pd_layers = pd.read_csv(path_layer+'layers{}/details/Image_layers_info_1_{}.csv'.format(i, image_name))
                            Image = pd_layers.Image.values.tolist()
                            RepoTag = pd_layers.RepoTag.values.tolist()
                            layer_digest = pd_layers.layer_digest.values.tolist()
                            file_name = pd_layers.file_name.values.tolist()
                            file_path = pd_layers.file_path.values.tolist()
                            file_size = pd_layers.file_size.values.tolist()
                            extension = pd_layers.extension.values.tolist()
                            level = pd_layers.level.values.tolist()

                            for a in range(len(Image)):
                                if 'share' in str(file_path[a]).lower():
                                    if Image[a] in shared_files_data.keys():
                                        if extension[a] in shared_files_data.get(Image[a]).keys():
                                            shared_files_data[Image[a]][extension[a]] += 1
                                            memory_files_data[Image[a]][extension[a]] += file_size[a]
                                        else:
                                            shared_files_data[Image[a]][extension[a]] = 1
                                            memory_files_data[Image[a]][extension[a]] = file_size[a]
                                    else:
                                        shared_files_data[Image[a]] = {}
                                        shared_files_data[Image[a]][extension[a]] = 1
                                        memory_files_data[Image[a]] = {}
                                        memory_files_data[Image[a]][extension[a]] = file_size[a]
                                if Image[a] in total_files_data.keys():
                                    total_files_data[Image[a]] += 1
                                    total_memory_files_data[Image[a]] += file_size[a]
                                else:
                                    total_files_data[Image[a]] = 1
                                    total_memory_files_data[Image[a]] = file_size[a]

                            flag += 1

                    for key, val in shared_files_data.items():
                        current_topic = topic_dict.get(manual_topic[Repo.index(repo)])
                        print(current_topic, repo)
                        index_count = 0
                        sorted_d = dict(sorted(val.items(), key=operator.itemgetter(1), reverse=True))
                        total = total_files_data[key]
                        list_size = []
                        list_comp = []
                        for key2, val2 in sorted_d.items():
                            if check_isnumeric(key2) == False:
                                list_size.append(round((memory_files_data[key][key2]*100/total_memory_files_data.get(key)),4))
                                list_comp.append(round((val2*100/total),2))
                                index_count += 1
                                if index_count == 6:
                                    break
                        data_writer.writerow(
                            [current_topic, repo, 'P{}'.format(dict_topic_repo.get(current_topic).index(repo)), key2,np.mean(list_comp), np.mean(list_size)])

                        print(doker_image, shared_files_data)
        data_file.close()
data = {}
for i in range(len(Repo)):
    tags_log = []
    repo_name = str(Repo[i]).split('/')[1]
    image_ = docker_image[i].strip()
    list_images = []
    split_image = image_.split(', ')
    for image in split_image:
        list_images.append(image)
    data[Repo[i]] = list_images
get_layers(data)




topic_dict = {'mlops': 'MLops', 'application': 'Application', 'tool': 'ToolKit', 'tutorials/ documentation': 'Documentation', 'model': 'Model'}
#data_file = open(path_output + '/RQ1/processed_options_selected.csv', mode='w', newline='', encoding='utf-8')
#data_writer = csv.writer(data_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
#data_writer.writerow(['Topic', 'Repos', 'Tag', 'Metrics', 'Value'])
