import pandas as pd
import csv
import numpy as np
import operator
import os

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
#Image_list = []
#layers_size_list = []
#layers_digest_list = []
read_image = []
list_dir = [dir for dir in os.listdir(path_details) if 'Manifest_details' in str(dir)]
#list_dir
dir_num = 0

dict_layer_size_csl = {}
layers_num = {}
for file_ in list_dir:
    dir_num += 1
    df = pd.read_csv(path_details+file_)
    #print(df.columns)
    Image = df.Image.values.tolist()
    layers_size = df.layers_size.values.tolist()
    layers_digest_ = df.layers_digest.values.tolist()
    for i in range(len(Image)):
        digest_ = layers_digest_[i].split(':')[-1]
        concat_image_layer = Image[i]+'/'+layers_digest_[i]
        if not concat_image_layer in read_image:
            #print(Image[i])
            if Image[i] in latest_imageL2:
                index_of = latest_imageL2.index(Image[i])
                if repos_final2[index_of] in dict_layer_size_csl.keys():
                    if Image[i] in dict_layer_size_csl[repos_final2[index_of]].keys():
                        if digest_ in dict_layer_size_csl[repos_final2[index_of]][Image[i]].keys():
                            dict_layer_size_csl[repos_final2[index_of]][Image[i]][digest_] += layers_size[i]
                        else:
                            dict_layer_size_csl[repos_final2[index_of]][Image[i]][digest_] = layers_size[i]
                    else:
                        dict_layer_size_csl[repos_final2[index_of]][Image[i]] = {}
                        dict_layer_size_csl[repos_final2[index_of]][Image[i]][digest_] = layers_size[i]
                else:
                    dict_layer_size_csl[repos_final2[index_of]] = {}
                    dict_layer_size_csl[repos_final2[index_of]][Image[i]] = {}
                    dict_layer_size_csl[repos_final2[index_of]][Image[i]][digest_] = layers_size[i]

            #Image_list.append(Image[i])
            #layers_size_list.append(layers_size[i])
            #layers_digest_list.append(layers_digest_[i][layers_digest_[i].index(':')+1:])
            read_image.append(concat_image_layer)

#print(len(Image_list))
'''list_notfound = []
# dict_filesize_fsl = {}
dict_layer_size_fsl = {}
layers_num = {}
for index in range(len(repos_final)):
    # print(latest_imageL[index])
    for image in eval(latest_imageL[index]):
        # image = str(image).replace(':','/')
        file_ = str(image).replace('/', '_')
        # file_ = file_.replace(':', '/')
        path_to_file = path_details + 'details/' + str(repos_final[index])
        # print(path_to_file+'/'+file_+'.csv')
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
                for l_id in range(len(layer_digest)):
                    if repos_final[index] in dict_layer_size_fsl.keys():
                        if Image_[l_id] in dict_layer_size_fsl[repos_final[index]].keys():
                            dict_layer_size_fsl[repos_final[index]][Image_[l_id]] += file_size[l_id]
                            layers_num[repos_final[index]][Image_[l_id]].add(layer_digest[l_id])
                        else:
                            dict_layer_size_fsl[repos_final[index]][Image_[l_id]] = file_size[l_id]
                            layers_num[repos_final[index]][Image_[l_id]] = set([layer_digest[l_id]])
                    else:
                        dict_layer_size_fsl[repos_final[index]] = {}
                        dict_layer_size_fsl[repos_final[index]][Image_[l_id]] = file_size[l_id]
                        layers_num[repos_final[index]] = {}
                        layers_num[repos_final[index]][Image_[l_id]] = set([layer_digest[l_id]])

            # if os.path.exists(path_to_file+'/'+list_dir_[0]):
            # print(image, 'found..1')
            # else:
            #    print(image, 'not found..level2')
        else:
            list_notfound.append(image)
print(len(list_notfound))'''

# path_details_layers = '/Volumes/Cisco/Fall2021/Devops/Final-project/v2/docker-analyser/dockerhub/outputs-server1/combine-layers/details/'
path_details = '/Volumes/Cisco/Summer2022/Docker/Dataset/downloads/combined/layers/'
path_output = '/Volumes/Cisco/Summer2022/Docker/Dataset/v2/RQ4/'
data_file1 = open(path_output + 'Docker_images_total_1.csv', mode='w', newline='', encoding='utf-8')
data_writer1 = csv.writer(data_file1, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
data_writer1.writerow(['Category', 'image', 'total_layers'])

data_file = open(path_output + 'Docker_images_layers_22.csv', mode='w', newline='', encoding='utf-8')
data_writer = csv.writer(data_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
data_writer.writerow(['Category', 'image', 'metrics', 'layer_size'])

for cat in set(topic):

    layers_size = {}
    image_layer_dict = {}
    image_layer_CLS_dict = {}
    #layers_num_category = {}
    dict_layer_size = {}
    for repo_index in range(len(repos_final)):

        path_to_file = path_details + 'details/' + str(repos_final[repo_index])
        if cat == topic[repo_index] and os.path.exists(path_to_file):
            # for image in eval(latest_imageL[index]):
            # images_ = docker_image[repos_.index(repos_final[repo_index])]
            # split_image = images_.split(', ')
            # print(Repos)
            if repos_final[repo_index] in dict_layer_size_csl.keys():
                image_layer_CLS_dict[repos_final[repo_index]] = dict_layer_size_csl.get(repos_final[repo_index])
                #layers_num_category[repos_final[repo_index]] = layers_num.get(repos_final[repo_index])
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
                    for l_id in range(len(layer_digest)):
                        if repos_final[repo_index] in dict_layer_size.keys():
                            if Image_[l_id] in dict_layer_size[repos_final[repo_index]].keys():
                                if layer_digest[l_id] in dict_layer_size[repos_final[repo_index]][Image_[l_id]].keys():
                                    dict_layer_size[repos_final[repo_index]][Image_[l_id]][layer_digest[l_id]] += file_size[l_id]
                                else:
                                    dict_layer_size[repos_final[repo_index]][Image_[l_id]][layer_digest[l_id]] = \
                                    file_size[l_id]
                            else:
                                dict_layer_size[repos_final[repo_index]][Image_[l_id]] = {}
                                dict_layer_size[repos_final[repo_index]][Image_[l_id]][layer_digest[l_id]] = file_size[
                                    l_id]
                        else:
                            dict_layer_size[repos_final[repo_index]] = {}
                            dict_layer_size[repos_final[repo_index]][Image_[l_id]] = {}
                            dict_layer_size[repos_final[repo_index]][Image_[l_id]][layer_digest[l_id]] = file_size[
                                l_id]

    #data_value_CLS = []
    for key, val in dict_layer_size.items():
        if key in image_layer_CLS_dict.keys():
            for key2, val2 in val.items():
                #print(key2, val2)
                #if key2 in image_layer_CLS_dict[key].keys():
                list_val = []
                for k, v in val2.items():
                    try:
                        if str(v) != 'nan':
                            list_val.append(v)
                        #data_writer.writerow([check_automl(cat), key2, 'FLS', convert_size(v)])
                    except Exception as e:
                        print('Error in ', key, k, v, e)
                print(key2, list_val)
                try:
                    data_writer.writerow([check_automl(cat), key2, 'FLS', convert_size(np.sum(list_val))])
                except:
                    pass
            for key2_, val2_ in image_layer_CLS_dict.get(key).items():
                list_val2 = []
                for k_, v_ in val2_.items():
                    try:
                        if k_ in list(val.get(key2_).keys()):
                            #if v_ > 0:
                            #print('sucess: ', k_, list(val.get(key2_).keys()))
                            list_val2.append(v_)
                            #data_writer.writerow([check_automl(cat), key2, 'CLS', convert_size(v_)])

                    except Exception as e:
                        print('Error2 in ', k_, v_, e)
                try:
                    data_writer.writerow([check_automl(cat), key2, 'CLS', convert_size(np.sum(list_val2))])
                except:
                    pass
                data_writer1.writerow([check_automl(cat), key2, len(val2)])
        #    list_val.append(val2)
        # data_value.append(np.mean(list_val))
        #data_writer.writerow([check_automl(cat), key, 'FLS', convert_size(np.mean(list(val.values())))])

    #data_value_FLS = []
    '''for key, val in image_layer_CLS_dict.items():
        #num_val = []
        for key2, val2 in val.items():
            list_val = []
            for v in val2:
                try:
                    list_val.append(convert_size(v))
                except Exception as e:
                    print('Error in ', key, v)

            data_writer.writerow([check_automl(cat), key2, 'CLS', np.sum(list_val)])
            data_writer1.writerow([check_automl(cat), key2, len(val2)])
            #num_val.append(len(layers_num_category[key][key2]))'''
        # data_value_FLS.append(np.mean(list_val))
        #data_writer.writerow([check_automl(cat), key, 'CLS', convert_size(np.mean(list(val.values())))])

        #data_writer1.writerow([check_automl(cat), key, np.mean(num_val)])
data_file.close()
data_file1.close()