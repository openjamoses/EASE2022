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
path_output = '/Volumes/Cisco/Summer2022/Docker/Dataset/v2/RQ4/files2/'

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

data_file2 = open(path_output + 'Top10_files_by_size.csv', mode='w', newline='', encoding='utf-8')
data_writer2 = csv.writer(data_file2, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
data_writer2.writerow(['Category', 'file_type', 'perc_size', 'size'])

data_file22 = open(path_output + 'Top10_files_by_size_1.csv', mode='w', newline='', encoding='utf-8')
data_writer22 = csv.writer(data_file22, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
data_writer22.writerow(['Category', 'file_type', 'perc_size'])


data_file3 = open(path_output + 'Top10_files_by_num.csv', mode='w', newline='', encoding='utf-8')
data_writer3 = csv.writer(data_file3, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
data_writer3.writerow(['Category', 'file_type', 'perc_number', 'perc_storage'])


data_file33 = open(path_output + 'Top10_files_by_num_1.csv', mode='w', newline='', encoding='utf-8')
data_writer33 = csv.writer(data_file33, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
data_writer33.writerow(['Category', 'file_type', 'perc_number'])
list_topic = set()
for cat in set(topic):
    list_topic.add(check_automl(cat))
for cat in list_topic:
    cat_str = cat
    if '/' in cat:
        cat_str = str(cat_str).split('/')[0]

    print(cat)
    data_file = open(path_output + 'layers_files_{}.csv'.format(cat_str), mode='w', newline='', encoding='utf-8')
    data_writer = csv.writer(data_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    data_writer.writerow(['Category', 'Repos', 'file_type', 'total_size', 'total_number', 'perc_size', 'perc_num'])


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

    data_file_size_cat = {}
    data_file_counts_cat = {}
    data_file_counts_size_cat = {}
    data_file_size_cat_val = {}
    for key, val in dict_layer_size.items():
        data_final = {}
        data_final_num = {}
        data_final_num_size = {}
        data_path = {}
        total_size = 0
        total_num = 0
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


        sorted_d = dict(sorted(data_final.items(), key=operator.itemgetter(1), reverse=True))
        counter = 0
        for key2, val2 in sorted_d.items():
            key_str_2 = key2
            if len(val2) == 1:
                key_str_2 = file_categories_dir(data_path[key2][0])
                # key_str_2 = data_path[key2][0]
            l_val = []
            for v in val2:
                if str(v) != 'nan':
                    l_val.append(v)
            if counter < 50:

                if key_str_2 in data_file_size_cat.keys():
                    data_file_size_cat[key_str_2].append(round((np.sum(l_val) * 100 / total_size), 4))
                    data_file_size_cat_val[key_str_2].append(np.sum(l_val))
                else:
                    data_file_size_cat[key_str_2] = [round((np.sum(l_val) * 100 / total_size), 4)]
                    data_file_size_cat_val[key_str_2] = [np.sum(l_val)]
                data_writer.writerow([cat, key, key_str_2, np.sum(val2), len(val2), round((np.sum(val2) * 100 / total_size), 4),
                                      round((len(val2) * 100 / total_num), 4)])
            counter += 1
            if key2 in data_final_num_size.keys():
                data_final_num_size[key2].append(round((np.sum(l_val) * 100 / total_size), 4))
            else:
                data_final_num_size[key2] = [round((np.sum(l_val) * 100 / total_size), 4)]
            #data_writer.writerow(
            #    [cat, key, key_str_2, np.sum(val2), len(val2), round((np.sum(val2) * 100 / total_size), 4),
            #     round((len(val2) * 100 / total_num), 4)])

        counter = 0
        sorted_d = dict(sorted(data_final_num.items(), key=operator.itemgetter(1), reverse=True))
        for key2, val2 in sorted_d.items():
            if counter < 50:
                key_str_2 = key2
                if len(data_final[key2]) == 1:
                    key_str_2 = file_categories_dir(data_path[key2][0])
                    #key_str_2 = data_path[key2][0]
                mean_valL = []
                try:
                    for v in data_final_num_size[key2]:
                        str(v).isnumeric()
                        mean_valL.append(v)
                except:
                    pass
                mean_ = 0
                if len(mean_valL) > 0:
                    mean_ = np.mean(mean_valL)
                else:
                    print('len is zero:', key, key2)

                if key_str_2 in data_file_counts_cat.keys():
                    data_file_counts_cat[key_str_2].append(val2)
                    data_file_counts_size_cat[key_str_2].append(mean_)
                else:
                    data_file_counts_cat[key_str_2] = [val2]
                    data_file_counts_size_cat[key_str_2] = [mean_]
            counter += 1

    data_file.close()
    counter = 0
    dict_tem_file_size_cat = {}
    dict_tem_file_size_cat2 = {}
    for key, val in data_file_size_cat.items():
        v_l = []
        for v in val:
            if str(v) != 'nan':
                v_l.append(v)
        perc_val = 0
        if len(v_l) > 0:
            perc_val = np.mean(v_l) #TODO: change this line to median instead of mean
        dict_tem_file_size_cat[key] = perc_val
        dict_tem_file_size_cat2[key] = v_l

    sorted_d = dict(sorted(dict_tem_file_size_cat.items(), key=operator.itemgetter(1), reverse=True))
    for key, val in sorted_d.items():
        if counter < 12:
            #print(key, np.mean(val), val)
            '''v_l = []
            for v in val:
                if str(v) != 'nan':
                    v_l.append(v)
            perc_val = 0
            if len(v_l) > 0:
                perc_val = np.mean(v_l)
            print(key, perc_val)'''
            for v in dict_tem_file_size_cat2.get(key):
                data_writer22.writerow([cat, key, v])
            data_writer2.writerow([cat, key, val, convert_size(np.mean(data_file_size_cat_val[key]))])
        counter += 1

    counter = 0
    data_file_counts_cat_temp2 = {}
    for key, val in data_file_counts_cat.items():
        data_file_counts_cat[key] = np.mean(val) #TODO: change this line to median instead of mean
        data_file_counts_cat_temp2[key] = val
    sorted_d = dict(sorted(data_file_counts_cat.items(), key=operator.itemgetter(1), reverse=True))
    for key, val in sorted_d.items():
        if counter < 12:
            v_l = []
            for v in data_file_counts_size_cat[key]:
                if str(v) != 'nan':
                    v_l.append(v)
            perc_val = 0
            if len(v_l) > 0:
                perc_val = np.mean(v_l)
            for v in data_file_counts_cat_temp2.get(key):
                data_writer33.writerow([cat, key, v])
            data_writer3.writerow([cat, key, val, perc_val])
        counter += 1

data_file2.close()
data_file3.close()
data_file33.close()
data_file22.close()
