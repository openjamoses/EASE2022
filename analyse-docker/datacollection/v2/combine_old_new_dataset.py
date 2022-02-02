import pandas as pd
import csv

path_output = '/Volumes/Cisco/Summer2022/Docker/Dataset/repos/combined/'
path = '/Volumes/Cisco/Summer2022/Docker/Dataset/repos/'
data_file = open(path_output + 'combined_initial_ml_docker_repositories.csv', mode='w', newline='',
                              encoding='utf-8')
data_writer = csv.writer(data_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
data_writer.writerow(['Repos','ML_Related','both', 'topic', 'commits', 'contributors', 'issues','pulls', 'releases','repo_size','stars','forks','open_issues','archived','created_at', 'updated_at','docker_files_count', 'file_names', 'file_paths','language','homepage', 'description'])

data_df = pd.read_csv(path + 'ml_docker_repositories.csv')
Repos = data_df.Repos.values.tolist()
ML_Related = data_df.ML_Related.values.tolist()
topic = data_df.topic.values.tolist()
commits = data_df.commits.values.tolist()
contributors = data_df.contributors.values.tolist()
issues = data_df.issues.values.tolist()
pulls = data_df.pulls.values.tolist()
releases = data_df.releases.values.tolist()
repo_size = data_df.repo_size.values.tolist()
stars = data_df.stars.values.tolist()
forks = data_df.forks.values.tolist()
open_issues = data_df.open_issues.values.tolist()
archived = data_df.archived.values.tolist()
created_at = data_df.created_at.values.tolist()
updated_at = data_df.updated_at.values.tolist()
docker_files_count = data_df.docker_files_count.values.tolist()
file_names = data_df.file_names.values.tolist()
file_paths = data_df.file_paths.values.tolist()
language = data_df.language.values.tolist()
homepage = data_df.homepage.values.tolist()
description = data_df.description.values.tolist()


df_data = pd.read_excel(open(path + 'Ml Docker projects-v2.xlsx', 'rb'),  engine="openpyxl", sheet_name='initial')

#data_df = pd.read_csv(path + 'ml_docker_repositories.csv')
Repos2 = df_data.Repos.values.tolist()
#ML_Related = data_df.ML_Related.values.tolist()
topic2 = df_data.topic.values.tolist()
commits2 = df_data.commits.values.tolist()
contributors2 = df_data.contributors.values.tolist()
issues2 = df_data.issues.values.tolist()
pulls2 = df_data.pulls.values.tolist()
releases2 = df_data.releases.values.tolist()
repo_size2 = df_data.repo_size.values.tolist()
stars2 = df_data.stars.values.tolist()
forks2 = df_data.forks.values.tolist()
open_issues2 = df_data.open_issues.values.tolist()
archived2 = df_data.archived.values.tolist()
created_at2 = df_data.created_at.values.tolist()
updated_at2 = df_data.updated_at.values.tolist()

docker_files_count2 = df_data.docker_files_count.values.tolist()
file_names2 = df_data.file_names.values.tolist()
file_paths2 = df_data.file_paths.values.tolist()

language2 = df_data.language.values.tolist()
homepage2 = df_data.homepage.values.tolist()
description2 = df_data.description.values.tolist()


for i in range(len(Repos2)):
    ml_related = ''
    both = 0
    if Repos2[i] in Repos:
        index = Repos.index(Repos2[i])
        ml_related = ML_Related[index]
        both = 2
    data_writer.writerow(
        [Repos2[i], ml_related, both, topic2[i], commits2[i], contributors2[i], issues2[i], pulls2[i], releases2[i],
         repo_size2[i], stars2[i], forks2[i], open_issues2[i], archived2[i], created_at2[i], updated_at2[i], docker_files_count2[i],
         file_names2[i], file_paths2[i], language2[i], homepage2[i], description2[i]])

for i in range(len(Repos)):
    if not Repos[i] in Repos2:
        data_writer.writerow(
            [Repos[i], ML_Related[i], 1, topic[i], commits[i], contributors[i], issues[i], pulls[i], releases[i],
             repo_size[i], stars[i], forks[i], open_issues[i], archived[i], created_at[i], updated_at[i],
             docker_files_count[i],
             file_names[i], file_paths[i], language[i], homepage[i], description[i]])

data_file.close()