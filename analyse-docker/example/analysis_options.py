import operator

import pandas as pd
import csv
import os
import numpy as np
path = '../outputs/csv/'
path_output = '../outputs/csv/processed/'
if not os.path.exists(path_output):
    os.makedirs(path_output)

data_file = open(path_output + 'options_repos_combined.csv', mode='w', newline='',
                                  encoding='utf-8')
data_writer = csv.writer(data_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
data_writer.writerow(['Repo','topic','releases','repo_size','stars','Tags', 'options_weight', 'purple_category_weight', 'docker_image', 'docker_files_count', 'file_names', 'file_paths', 'language', 'description'])

data_file2 = open(path_output + 'options_repos_summary_data.csv', mode='w', newline='',
                                  encoding='utf-8')
data_writer2 = csv.writer(data_file2, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
data_writer2.writerow(['repos','topic','ml_category','purpose','weight'])


data_file3 = open(path_output + 'options_repos_purpose_data_1.csv', mode='w', newline='',
                                  encoding='utf-8')
data_writer3 = csv.writer(data_file3, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
data_writer3.writerow(['purpose','avg_weight', 'median_weight'])

df = pd.read_csv(path+'results_options v1.csv')

repos = df.repos.values.tolist()
repo_version = df.repo_version.values.tolist()
option = df.option.values.tolist()
option_count = df.option_count.values.tolist()
category = df.category.values.tolist()

df_input = pd.read_csv('../input.csv')
Repos = df_input.Repos.values.tolist()
topic = df_input.topic.values.tolist()
docker_image = df_input.docker_image.values.tolist()
releases = df_input.releases.values.tolist()
size = df_input.repo_size.values.tolist()
stars = df_input.stars.values.tolist()
docker_files_count = df_input.docker_files_count.values.tolist()
file_names = df_input.file_names.values.tolist()
file_paths = df_input.file_paths.values.tolist()
language = df_input.language.values.tolist()
homepage = df_input.homepage.values.tolist()
description = df_input.description.values.tolist()

topic_mapping = {'DL Framework':['tensorflow', 'keras','mxnet','torch'], 'Deep Learning':['cnn', 'deep-learning', 'neural-network'], 'Machine Learning':['machine-learning', 'sklearn'], 'Reinforcement Learning':['reinforcement-learning', 'rnn'], 'AI': ['computer-vision', 'artificial-intelligence', 'object-detection', 'image-processing'], 'mlops':['mlflow', 'serving', 'mlops']}

dict_purpose_all = {}
for index in range(len(Repos)):
    dict_options = {}
    tags_ = set()
    dict_category = {}
    for i in range(len(repos)):
        if Repos[index] == repos[i]:
            tags_.add(repo_version[i])
            if repo_version[i] in dict_options.keys():
                if option[i] in dict_options[repo_version[i]].keys():
                    dict_options[repo_version[i]][option[i]] += option_count[i]
                else:
                    dict_options[repo_version[i]][option[i]] = option_count[i]
            else:
                dict_options[repo_version[i]] = {}
                dict_options[repo_version[i]][option[i]] = option_count[i]

            if repo_version[i] in dict_category.keys():
                if category[i] in dict_category[repo_version[i]].keys():
                    dict_category[repo_version[i]][category[i]] += option_count[i]
                else:
                    dict_category[repo_version[i]][category[i]] = option_count[i]
            else:
                dict_category[repo_version[i]] = {}
                dict_category[repo_version[i]][category[i]] = option_count[i]
    #total_tags = 0

    dict_data_options = {}
    dict_data_category = {}
    for key, val in dict_options.items():
        #total_tags += 1
        for key2, val2 in val.items():
            dict_data_options[key2] = round((val2/len(list(dict_options.keys()))),2)
    for key, val in dict_category.items():
        #total_tags += 1
        for key2, val2 in val.items():
            dict_data_category[key2] = round((val2/len(list(dict_options.keys()))),2)
    sorted_data_options = dict(sorted(dict_data_options.items(), key=operator.itemgetter(1), reverse=True))
    sorted_data_category = dict(sorted(dict_data_category.items(), key=operator.itemgetter(1), reverse=True))
    ml_category = ''
    for top, sub_top in topic_mapping.items():
        if topic[index] in sub_top:
            ml_category = top

    options_count_str = ''
    category_count_str = ''
    for key, val in sorted_data_options.items():
        options_count_str += key+':'+str(val)+', '
    for key, val in sorted_data_category.items():
        category_count_str +=  key+':'+str(val)+', '
        if key in dict_purpose_all.keys():
            val_p = dict_purpose_all.get(key)
            val_p.append(val)
            dict_purpose_all[key] = val_p
        else:
            dict_purpose_all[key] = [val]

        data_writer2.writerow([Repos[index], topic[index], ml_category, key, val])
    data_writer.writerow(
        [Repos[index], topic[index], releases[index], size[index], stars[index], len(tags_), options_count_str, category_count_str,
         docker_image[index], docker_files_count[index], file_names[index], file_paths[index], language[index], description[index]])

    #data_writer.writerow([Repos[index], len(tags_), options_count_str, category_count_str])
data_file.close()
data_file2.close()

for key, val in dict_purpose_all.items():
    data_writer3.writerow([key, np.mean(val), np.median(val)])
data_file3.close()




