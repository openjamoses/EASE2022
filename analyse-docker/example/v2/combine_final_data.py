import csv
import pandas as pd

path = '/Volumes/Cisco/Summer2022/Docker/Dataset/repos/combined/'
path_tag = '/Volumes/Cisco/Fall2021/Devops/Final-project/v2/docker-analyser/example/outputs/csv/'
# df_topic = pd.read_csv('../../purpose.csv')
df_topic = pd.read_excel(open(path + 'combined_initial_ml_docker_repositories.xlsx', 'rb'), engine="openpyxl",
                         sheet_name='filtered')

Repos = df_topic.Repos.values.tolist()
manual_topic = df_topic.manual_topic.values.tolist()
topic = df_topic.topic.values.tolist()
latest_image = df_topic.latest_image.values.tolist()

df_topic = pd.read_csv(path_tag + 'tags_matching0.csv')  # tags_matching - final
reposL = df_topic.repos.values.tolist()
total_dockerfiles = df_topic.total_dockerfiles.values.tolist()
matching_image = df_topic.matching_image.values.tolist()
all_images = df_topic.all_images.values.tolist()
dockerfiles = df_topic.dockerfiles.values.tolist()
notags = df_topic.notags.values.tolist()
base_images = df_topic.base_images.values.tolist()
purpose = df_topic.purpose.values.tolist()
docker_compose = df_topic.docker_compose.values.tolist()
compose_versions = df_topic.compose_versions.values.tolist()
compose_services = df_topic.compose_services.values.tolist()
compose_networks = df_topic.compose_networks.values.tolist()
compose_volume = df_topic.compose_volume.values.tolist()
compose_env = df_topic.compose_env.values.tolist()
other_dockerfiles = df_topic.other_dockerfiles.values.tolist()
WhatL = df_topic.What.values.tolist()
WhenL = df_topic.When.values.tolist()
MLcomponentL = df_topic.MLcomponent.values.tolist()
WhyL = df_topic.Why.values.tolist()
MaincomponentL = df_topic.Maincomponent.values.tolist()
NoteL = df_topic.Note.values.tolist()


data_file = open(path  + '/tags_matching_final.csv', mode='w', newline='', encoding='utf-8')
data_writer = csv.writer(data_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
data_writer.writerow(['repos', 'manual_topic','topic', 'total_dockerfiles', 'matching_image', 'all_images','latest_image', 'dockerfiles', 'notags', 'base_images',
     'purpose', 'docker_compose', 'compose_versions', 'compose_services', 'compose_networks',
     'compose_volume', 'compose_env', 'other_dockerfiles' ,'What', 'When', 'MLcomponent' ,'Why', 'Maincomponent'
     ,'Note'])
for index in range(len(Repos)):  # 264
    if not 'remove' in str(manual_topic[index]):
        What = ''
        When = ''
        MLcomponent = ''
        Why = ''
        Maincomponent = ''
        Note = ''
        if Repos[index] in reposL:
            index_of = reposL.index(Repos[index])
            if str(WhatL[index_of]) != 'nan':
                What = WhatL[index_of]
            if str(WhenL[index_of]) != 'nan':
                When = WhenL[index_of]
            if str(MLcomponentL[index_of]) != 'nan':
                MLcomponent = MLcomponentL[index_of]
            if str(WhyL[index_of]) != 'nan':
                Why = WhyL[index_of]
            if str(MaincomponentL[index_of]) != 'nan':
                Maincomponent = MaincomponentL[index_of]
            if str(NoteL[index_of]) != 'nan':
                Note = NoteL[index_of]
            data_writer.writerow(
                [Repos[index], manual_topic[index], topic[index], total_dockerfiles[index_of], matching_image[index_of], all_images[index_of], latest_image[index],
                 dockerfiles[index_of], notags[index_of], base_images[index_of],
                 purpose[index_of], docker_compose[index_of], compose_versions[index_of], compose_services[index_of], compose_networks[index_of],
                 compose_volume[index_of], compose_env[index_of], other_dockerfiles[index_of], What, When, MLcomponent, Why,
                 Maincomponent, Note])
        else:
            data_writer.writerow(
                [Repos[index], manual_topic[index], topic[index], '', '',
                 '', latest_image[index],
                 '', '', '', '', '', '', '', '', '', '', '', What, When, MLcomponent, Why, Maincomponent, Note])


