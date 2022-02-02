import os
from pathlib import Path
import csv
import pandas as pd
import subprocess

def _info(info_path, doker_image):
    doker_image_str = ''
    if '/' in str(doker_image):
        doker_image_str = str(doker_image).replace('/', '_')
    if ':' in doker_image_str:
        doker_image_str = str(doker_image_str).replace(':', '_')
    log_info = info_path + '/' + doker_image_str + '.log'
    # process_command = 'docker search ' + keyword + ' > ' + log_
    process_command = "skopeo inspect docker://" + doker_image + " > " + log_info

    p = subprocess.Popen(process_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    output = ""
    for line in p.stdout.readlines():
        output = output + str(line) + '\n'
    retval = p.wait()
    if retval == 0:
        print("Inspecting docker Image {} successful!".format(doker_image))
    else:
        print("Docker Inspect Error for Image {}!".format(doker_image))
        print(output)
    return retval


path_output = '/Volumes/Cisco/Summer2022/Docker/Dataset/repos/combined/'
path = '/Volumes/Cisco/Summer2022/Docker/Dataset/repos/'
data_file = open(path_output + 'combined_ml_docker_repositories_final_filtered2.csv', mode='w', newline='',
                              encoding='utf-8')
data_writer = csv.writer(data_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
data_writer.writerow(['Repos','ML_Related','both','manual_topic', 'topic', 'commits', 'contributors', 'issues','pulls', 'releases','repo_size','stars','forks','open_issues','archived','docker_images','latest_image','inspect_status','sort_inspect','created_at', 'updated_at','docker_files_count', 'file_names', 'file_paths','language','homepage', 'description'])
data_df = pd.read_excel(open(path_output + 'combined_initial_ml_docker_repositories.xlsx', 'rb'),  engine="openpyxl", sheet_name='images')

#data_df = pd.read_csv(path + 'ml_docker_repositories.csv')
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
docker_image = data_df.docker_images.values.tolist()
manual_topic = data_df.manual_topic.values.tolist()

inspect_path = '/Volumes/Cisco/Summer2022/Docker/Dataset/repos/combined/docker-inspect/'

repos_data = {}
for i in range(123, len(Repos)):
    if not 'remove' in str(manual_topic[i]):
        info_path = inspect_path+Repos[i]
        if not os.path.exists(info_path):
            Path(info_path).mkdir(parents=True, exist_ok=True)
        try:
            #print(repos[i])
            list_images = []
            list_images_latest = []
            inspect_status = []
            index = Repos.index(Repos[i])
            image_ = docker_image[index].strip()
            split_image = image_.split(', ')
            sort_inspct = 0
            for image in split_image:
                list_images.append(image)
                image_str = image
                if not ':' in str(image_str):
                    image_str = str(image)+':latest'
                status = 1
                #status = _info(info_path, image_str)
                sort_inspct += status
                list_images_latest.append(image_str)
                inspect_status.append(status)
            if sort_inspct > 0:
                sort_inspct = 1
            #print(i, repos[i], split_image)
            print(i, Repos[i], len(list_images))
            data_writer.writerow(
                [Repos[i], ML_Related[i], both[i], manual_topic[i], topic[i], commits[i], contributors[i], issues[i], pulls[i],
                 releases[i], repo_size[i], stars[i], forks[i], open_issues[i], archived[i], docker_image[i], list_images_latest,
                 inspect_status,sort_inspct, created_at[i], updated_at[i], docker_files_count[i], file_names[i], file_paths[i],
                 language[i], homepage[i], description[i]])
        except Exception as e:
            print('Error writing reading repos: ', e)
        #repos_data[Repos[i]] = list_images
        # print('Total images: ', len(list_images))
data_file.close()