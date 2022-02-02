import pandas as pd
import csv
import numpy as np
path_input = '/Volumes/Cisco/Fall2021/Devops/Final-project/v2/docker-analyser/'
path = '/Volumes/Cisco/Fall2021/Devops/Final-project/v2/docker-analyser/outputs/csv/'
path_output = '/Volumes/Cisco/Fall2021/Devops/Final-project/v2/docker-analyser/outputs/csv/analysis/processed/'
path_tag_log = '/Volumes/Cisco/Fall2021/Devops/Final-project/v2/docker-analyser/outputs/logs/'
df_input = pd.read_csv(path_input+'selected.csv')
Repo = df_input.Repos.values.tolist()
docker_image = df_input.docker_image.values.tolist()
manual_topic = df_input.manual_topic.values.tolist()

df_input = pd.read_csv(path+'options_raw_details_1.csv')
repos = df_input.repos.values.tolist()
repo_version = df_input.repo_version.values.tolist()
option_count = df_input.total_counts.values.tolist()
option = df_input.option.values.tolist()
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
data_file = open(path_output + 'RQ1/processed_instructions_selected.csv', mode='w', newline='', encoding='utf-8')
data_writer = csv.writer(data_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
data_writer.writerow(['Topic', 'Repos', 'Tag', 'Metrics', 'Value'])

instruct_dict = ['USER', 'FROM', 'ENV', 'ADD', 'COPY', 'ARG', 'MAINTAINER', 'CMD', 'USER', 'VOLUME', 'RUN', 'SHELL', 'LABEL', 'WORKDIR', 'ENTRYPOINT']
option_set = set(option)
for topic in set(manual_topic):
    if not 'remove' in str(topic):
        print(topic)
        for i in range(len(Repo)):
            if manual_topic[i] == topic:
                data_options_dict = {}
                for j in range(len(repos)):
                    topic_str = topic
                    if topic in topic_dict.keys():
                        topic_str = topic_dict.get(topic)
                    if Repo[i] == repos[j]: # in selected_tag_list:
                        if repo_version[j] in data_options_dict.keys():
                            if option[j] in data_options_dict.get(repo_version[j]).keys():
                                data_options_dict[repo_version[j]][option[j]] += option_count[j]
                            else:
                                data_options_dict[repo_version[j]][option[j]] = option_count[j]
                        else:
                            data_options_dict[repo_version[j]] = {}
                            data_options_dict[repo_version[j]][option[j]] = option_count[j]
                for key, val in data_options_dict.items():
                    total_val = np.sum(list(val.values()))
                    for cat in option_set:
                        if cat in val.keys():
                            val2 = round((val.get(cat) * 100 / total_val),2)
                        else:
                            val2 = 0.0
                        if cat in instruct_dict:
                            data_writer.writerow([topic_str, Repo[i], key, cat, val2])
data_file.close()
