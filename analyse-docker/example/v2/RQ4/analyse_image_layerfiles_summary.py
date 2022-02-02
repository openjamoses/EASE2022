import pandas as pd
import csv
import numpy as np
import operator
import os

from example.v2.RQ4.file_types_categories import file_categories2, file_categories_dir, general_categories

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
# path_details_layers = '/Volumes/Cisco/Fall2021/Devops/Final-project/v2/docker-analyser/dockerhub/outputs-server1/combine-layers/details/'
path_details = '/Volumes/Cisco/Summer2022/Docker/Dataset/downloads/combined/layers/'
path_output = '/Volumes/Cisco/Summer2022/Docker/Dataset/v2/RQ4/'
data_file2 = open(path_output + 'Docker_images_file_memory_summary2.csv', mode='w', newline='', encoding='utf-8')
data_writer2 = csv.writer(data_file2, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

data_file = open(path_output + 'Docker_images_file_composition_summary2.csv', mode='w', newline='', encoding='utf-8')
data_writer = csv.writer(data_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)


list_topic = set()
for cat in set(topic):
    list_topic.add(check_automl(cat))
row = ['File Types']
row2 = ['File Types']
for cat in list_topic:
    row.append(cat+'(median)')
    row2.append(cat + '(median)')
    row2.append(cat + '(MB)')
    row2.append('')
data_writer.writerow(row)
data_writer2.writerow(row2)

data_perc_counts_overal = {}
data_file_size_overal = {}
for cat in list_topic:
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
                        if repos_final[repo_index] in dict_layer_size.keys():
                            if entension_str in dict_layer_size[repos_final[repo_index]].keys():
                                dict_layer_size[repos_final[repo_index]][entension_str].append(file_size[l_id])
                                dict_file_full_path[repos_final[repo_index]][entension_str].append([file_path[l_id]])
                            else:
                                dict_layer_size[repos_final[repo_index]][entension_str] = [file_size[l_id]]
                                dict_file_full_path[repos_final[repo_index]][entension_str] = [file_path[l_id]]
                        else:
                            dict_layer_size[repos_final[repo_index]] = {}
                            dict_layer_size[repos_final[repo_index]][entension_str] = [file_size[l_id]]

                            dict_file_full_path[repos_final[repo_index]] = {}
                            dict_file_full_path[repos_final[repo_index]][entension_str] = [file_path[l_id]]


    data_file_counts_cat_perc = {}
    data_file_size_cat_val = {}
    #print(dict_layer_size)
    for key, val in dict_layer_size.items():
        data_final = {}
        data_final_num = {}
        data_final_num_size = {}
        data_path = {}
        total_size = 0
        total_num = 0
        print(' ----: ', key)
        for key2, val2, in val.items():
            key2_str = file_categories2(key2)
            if key2_str in data_final.keys():
                for v in val2:
                    data_final[key2_str].append(v)
            else:
                data_final[key2_str] = val2
            total_size += np.sum(val2)
            total_num += len(val2)
            data_path[key2_str] = dict_file_full_path[key][key2]
        for key2, val2 in data_final.items():

            data_final_num[key2] = round((len(val2) * 100 / total_num), 4)
        #sorted_d = dict(sorted(data_final.items(), key=operator.itemgetter(1), reverse=True))
        #counter = 0
        for key2, val2 in data_final.items():
            key_str_2 = key2
            if len(val2) == 1:
                key_str_2 = file_categories_dir(data_path[key2][0])
                # key_str_2 = data_path[key2][0]
            l_val = []
            for v in val2:
                if str(v) != 'nan':
                    l_val.append(v)
            if key_str_2 in data_file_size_cat_val.keys():
                data_file_size_cat_val[key_str_2].append(np.sum(l_val))
                data_file_counts_cat_perc[key_str_2].append(data_final_num.get(key2))
            else:
                data_file_size_cat_val[key_str_2] = [np.sum(l_val)]
                data_file_counts_cat_perc[key_str_2] = [data_final_num.get(key2)]

    for key, val in data_file_size_cat_val.items():
        key_category = general_categories(key)
        if key_category in data_perc_counts_overal.keys():
            data_perc_counts_overal[key_category][cat] = data_file_counts_cat_perc[key]
            data_file_size_overal[key_category][cat] = val
        else:
            data_perc_counts_overal[key_category] = {}
            data_perc_counts_overal[key_category][cat] = data_file_counts_cat_perc[key]

            data_file_size_overal[key_category] = {}
            data_file_size_overal[key_category][cat] = val

for key, val in data_file_size_overal.items():
    row_size = [key]
    row_num = [key]
    for topic_ in list_topic:
        mean_value_ = 0
        std_value_ = 0
        if topic_ in val.keys():
            mean_value_ = np.median(val[topic_])
            #std_value_ = np.std(val[topic_])
        row_size.append(mean_value_)
        row_size.append(convert_size(mean_value_))
        row_size.append('')
        #row_size.append(std_value_)

        mean_num_ = 0
        std_num_ = 0
        if topic_ in data_perc_counts_overal[key].keys():
            mean_num_ = np.median(data_perc_counts_overal[key][topic_])
            #std_num_ = np.std(data_perc_counts_overal[key][topic_])
        row_num.append(mean_num_)
        #row_num.append(std_num_)
    data_writer2.writerow(row_size)
    data_writer.writerow(row_num)

data_file.close()
data_file2.close()
