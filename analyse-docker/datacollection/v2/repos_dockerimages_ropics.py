import pandas as pd
import csv

path_output = '/Volumes/Cisco/Summer2022/Docker/Dataset/repos/combined/'
path = '/Volumes/Cisco/Summer2022/Docker/Dataset/repos/'
data_file = open(path_output + 'combined_ml_docker_repositories_images.csv', mode='w', newline='',
                              encoding='utf-8')
data_writer = csv.writer(data_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
data_writer.writerow(['Repos','ML_Related','both','manual_topic', 'NewLabels','Review', 'topic', 'commits', 'contributors', 'issues','pulls', 'releases','repo_size','stars','forks','open_issues','docker_images','archived','created_at', 'updated_at','docker_files_count', 'file_names', 'file_paths','language','homepage', 'description'])

data_df = pd.read_excel(open(path_output + 'combined_initial_ml_docker_repositories.xlsx', 'rb'),  engine="openpyxl", sheet_name='notarchived')
Repos = data_df.Repos.values.tolist()
ML_Related = data_df.ML_Related.values.tolist()
topic = data_df.topic.values.tolist()
both = data_df.both.values.tolist()

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

df_data = pd.read_excel(open(path + 'Ml Docker projects-v2.xlsx', 'rb'),  engine="openpyxl", sheet_name='purpose')
RepoL = df_data.Repo.values.tolist()
manual_topic = df_data.manual_topic.values.tolist()
NewLabels = df_data.NewLabels.values.tolist()
Review = df_data.Review.values.tolist()
docker_image = df_data.docker_image.values.tolist()

for i in range(len(Repos)):
    if both[i] == 1:
        data_writer.writerow(
            [Repos[i], ML_Related[i], both[i], '', '', '', topic[i],
             commits[i],
             contributors[i], issues[i], pulls[i], releases[i], repo_size[i], stars[i], forks[i], open_issues[i],
             '', archived[i], created_at[i], updated_at[i], docker_files_count[i], file_names[i],
             file_paths[i], language[i], homepage[i], description[i]])
    elif both[i] != 1 and Repos[i] in RepoL:
        index = RepoL.index(Repos[i])
        if not 'remove' in str(manual_topic[index]).lower():
            data_writer.writerow(
                [Repos[i], ML_Related[i], both[i], manual_topic[index], NewLabels[index], Review[index], topic[i], commits[i],
                 contributors[i], issues[i], pulls[i], releases[i], repo_size[i], stars[i], forks[i], open_issues[i],
                 docker_image[index], archived[i], created_at[i], updated_at[i], docker_files_count[i], file_names[i],
                 file_paths[i], language[i], homepage[i], description[i]])
data_file.close()






