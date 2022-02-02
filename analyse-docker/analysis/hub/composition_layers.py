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

def get_layers(data):
    topic_dict = {'mlops': 'MLops', 'application': 'Application', 'tool': 'ToolKit', 'AutoML':'AutoML', 'Machine Learning': 'Machine Learning',
                  'tutorials/ documentation': 'Documentation', 'model': 'Model', 'DL framwork': 'DL Framwork'}
    data_file = open(path_output + '/RQ1c/processed_layers.csv', mode='w', newline='', encoding='utf-8')
    data_writer = csv.writer(data_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    data_writer.writerow(['Topic', 'Repos','ProjectID', 'Tag', 'Metrics','Values'])
    dict_topic_repo = {}
    for top in set(manual_topic):
        list_repo = set()
        for i in range(len(Repo)):
            if top == manual_topic[i]:
                list_repo.add(Repo[i])
        dict_topic_repo[topic_dict.get(top)] = list(list_repo)
    for repo, images_lists in data.items():
        for doker_image in images_lists:
            layers_count_data = {}
            layers_size_data = {}
            flag = 0
            for i in range(11):
                image_name = doker_image
                if '/' in str(doker_image):
                    image_name = str(doker_image).split('/')[0]
                if '/' in str(image_name):
                    image_name = str(image_name).replace('/', '_')
                #pd_layers = pd.read_csv(path_layer+'layers{}/Image_layers_info_1_{}.csv'.format(i))


                if os.path.exists(path_layer+'layers{}/details/Image_layers_info_1_{}.csv'.format(i, image_name)):

                    list_dir = [dir for dir in os.listdir(path_layer+'layers{}'.format(i)) if 'Manifest_details_' in str(dir)]

                    print(list_dir)
                    for file_ in list_dir:
                        pd_layers = pd.read_csv(path_layer+'layers{}/{}'.format(i, file_))

                        Image = pd_layers.Image.values.tolist()
                        RepoTag = pd_layers.RepoTag.values.tolist()
                        layers_size = pd_layers.layers_size.values.tolist()
                        layers_digest = pd_layers.layers_digest.values.tolist()

                        for a in range(len(Image)):
                            #if 'share' in str(file_path[a]).lower():
                            if Image[a] in layers_count_data.keys():
                                if RepoTag[a] in layers_count_data.get(Image[a]).keys():
                                    layers_count_data[Image[a]][RepoTag[a]] += 1
                                    layers_size_data[Image[a]][RepoTag[a]] += layers_size[a]

                                else:
                                    layers_count_data[Image[a]][RepoTag[a]] = 1
                                    layers_size_data[Image[a]][RepoTag[a]] = layers_size[a]
                            else:
                                layers_count_data[Image[a]] = {}
                                layers_count_data[Image[a]][RepoTag[a]] = 1
                                layers_size_data[Image[a]] = {}
                                layers_size_data[Image[a]][RepoTag[a]] = layers_size[a]


                        flag += 1
                for key, val in layers_count_data.items():
                    current_topic = topic_dict.get(manual_topic[Repo.index(repo)])
                    print(current_topic, repo)
                    for key2, val2 in val.items():
                        data_writer.writerow([current_topic, repo, 'P{}'.format(dict_topic_repo.get(current_topic).index(repo)), key2,'Layers count', val2])
                        data_writer.writerow(
                            [current_topic, repo, 'P{}'.format(dict_topic_repo.get(current_topic).index(repo)), key2,
                             'Memory',layers_size_data[key][key2] ])
                print(doker_image, layers_count_data)
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
