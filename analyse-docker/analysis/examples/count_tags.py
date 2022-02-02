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

df_input = pd.read_csv(path_input+'input.csv')
Repo1 = df_input.Repos.values.tolist()

df_input = pd.read_csv(path+'results_options_1.csv')
repos = df_input.repos.values.tolist()
repo_version = df_input.repo_version.values.tolist()
option_count = df_input.option_count.values.tolist()
category = df_input.category.values.tolist()
def select_tags(list_tags):
    tags_ = []
    for i in range(len(list_tags)):
        if i==0 or i==(len(list_tags)-1) or i == round((len(list_tags)/2)) or i==round(len(list_tags)*0.25) or  i==round(len(list_tags)*0.75):
            #if 'pre' in str(list_tags[i]) and i < len(list_tags)-1:
            #    tags_.append(list_tags[i+1])
            #else:
            tags_.append(list_tags[i])
    return tags_
topic_dict = {'mlops': 'MLops', 'application': 'Application', 'tool': 'ToolKit', 'tutorials/ documentation': 'Documentation', 'model': 'Model'}
data_file = open(path_output + '/RQ1/count_tags.csv', mode='w', newline='', encoding='utf-8')
data_writer = csv.writer(data_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
data_writer.writerow(['Repos', 'Images', 'Tag'])

category_set = set(category)
#for topic in set(manual_topic):
#    if not 'remove' in str(topic):
#        print(topic)
for i in range(len(Repo)):
    tags_log = []
    index = Repo1.index(Repo[i])
    repo_name = str(Repo[i]).split('/')[1]
    path_log_ = path_tag_log+"tags_"+repo_name+"_{}.txt".format(index)
    if not os.path.exists(path_log_):
        index = i
    if os.path.exists(path_tag_log+"tags_"+repo_name+"_{}.txt".format(index)):
        with open(path_tag_log+"tags_"+repo_name+"_{}.txt".format(index), "r") as f:
            for line in str(f.read()).split('\n'):
                if line != '':
                    tags_log.append(str(line.split(' ')[0]).replace("b'refs/tags/", ""))
        #print(i, len(tags_log), select_tags(tags_log))
    selected_tag_list = select_tags(tags_log)

    data_writer.writerow([Repo[i], len(tags_log), len(selected_tag_list)])
data_file.close()