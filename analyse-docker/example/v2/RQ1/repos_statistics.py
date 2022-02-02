import pandas as pd
import csv

df_topic = pd.read_excel(open(path + 'combined_initial_ml_docker_repositories.xlsx', 'rb'), engine="openpyxl", sheet_name='images')

Repos = df_topic.Repos.values.tolist()
manual_topic = df_topic.manual_topic.values.tolist()
DockerRepos = df_topic.DockerRepos.values.tolist()
#purple_category_weight = df_topic.purple_category_weight.values.tolist()
docker_image = df_topic.docker_images.values.tolist()