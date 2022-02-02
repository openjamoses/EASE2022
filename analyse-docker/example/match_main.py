import csv

import pandas as pd
import os
import time

from dockerhub.dockerimage import DockerImages
from example.analyse_dockerfile import run_main
from utils.Git import Git
from parser.file_contents import FileManagement

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
def main():
    repo_target_path_root = ROOT_DIR+"/outputs/clones"
    df_topic = pd.read_csv('../purpose.csv')
    Repos = df_topic.Repo.values.tolist()
    manual_topic = df_topic.manual_topic.values.tolist()
    purple_category_weight = df_topic.purple_category_weight.values.tolist()
    docker_image = df_topic.docker_image.values.tolist()

    df_topic = pd.read_csv('../filtered.csv')
    Repos2 = df_topic.repos.values.tolist()


    if not os.path.exists(ROOT_DIR+'/outputs'):
        os.makedirs(ROOT_DIR+'/outputs')
    if not os.path.exists(ROOT_DIR+'/outputs/logs'):
        os.makedirs(ROOT_DIR+'/outputs/logs')
    if not os.path.exists(ROOT_DIR+'/outputs/clones'):
        os.makedirs(ROOT_DIR+'/outputs/clones')
    if not os.path.exists(ROOT_DIR+'/outputs/csv'):
        os.makedirs(ROOT_DIR+'/outputs/csv')
    data_file = open(ROOT_DIR+'/outputs/csv' + '/tags_matching.csv', mode='w', newline='', encoding='utf-8')
    data_writer = csv.writer(data_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    data_writer.writerow(['repos','topic', 'total_dockerfiles', 'matching_image','all_images', 'dockerfiles','notags','base_images','purpose','purpose_weight', 'docker_compose','compose_versions','compose_services','compose_networks','compose_volume','compose_env', 'other_dockerfiles'])

    for index in range(0, len(Repos)): #264
        if Repos[index] in Repos2:
            repo = Repos[index]
            #if repo in ['numenta/nupic', 'wkentaro/labelme']:
            print(index, repo)
            repository_url = "https://github.com/" + repo + ".git"
            repo_name = repo.split('/')[1]
            if not os.path.exists(ROOT_DIR+'/outputs/logs/'+str(repo).split('/')[0]):
                os.makedirs(ROOT_DIR+'/outputs/logs/'+str(repo).split('/')[0])
            if not os.path.exists(ROOT_DIR+'/outputs/logs/'+str(repo)):
                os.makedirs(ROOT_DIR+'/outputs/logs/'+str(repo))
            log_repo_root_path = ROOT_DIR+'/outputs/logs/'+str(repo)
            if not os.path.exists(log_repo_root_path+'/hub'):
                os.makedirs(log_repo_root_path+'/hub')
            list_images = []
            image_ = docker_image[index].strip()
            split_image = image_.split(', ')
            for image in split_image:
                # print(i,len(image), image)
                list_images.append(image)

            dockerImage = DockerImages(log_repo_root_path+'/hub')
            dockerImage.get_info_images(list_images)
            images_tags = []
            tags_dict = dockerImage.images_tags
            for tag in tags_dict.keys():
                images_tags.append(tag)
            log_tags_path = log_repo_root_path+'/gh_tags.txt'# + repo_name+'_'+str(index)+ '.txt'
            repo_root = ROOT_DIR+'/outputs/clones/'+repo_name
            if not os.path.exists(repo_root):
                code = Git.clone_git_repository(url=repository_url, target_path=repo_target_path_root)
            else:
                code = 0
            if code == 0:
                Git.git_fetch_tags(repo_root)
                logs = Git.git_fetch_tags_sorts(repo_root, log_tags_path)
                tag_list = []
                tag_date_list = []
                with open(log_tags_path, "w") as text_file:
                    text_file.write(logs)

                for line in logs.split('\n'):
                    if len(line) > 0:
                        split_line = line.strip().split(' ')
                        tag = split_line[0]
                        tag = tag.replace('refs/tags/', '')
                        date = split_line[1]+' '+split_line[2]+ ' '+split_line[3]+' ' +split_line[4]+ ' '+split_line[5]
                        #print (tag, date)
                        tag_list.append(tag)
                        tag_date_list.append(date)
                print ('  ----total tags found: ', len(tag_list))
                '''if len(tag_list) > 0:
                    for tag_id in range((len(tag_list))):
                        tag = tag_list[tag_id]
                        print ('     ---- now analysing: ', tag_id, tag)
                        Git.git_checkout(repo_root, tag)
                        os.chdir(ROOT_DIR)
                        total_dockerfiles, all_dockerfiles, dict_matching,  other_docker_relatedfiles = run_main(repo_root, repo, tag,tags_dict,log_repo_root_path, save_version=1, save_image=True)
    
                        data_writer.writerow(
                            [repo, tag, total_dockerfiles, dict_matching, tags_dict, all_dockerfiles, len(other_docker_relatedfiles)])
                else:'''
                total_dockerfiles, all_dockerfiles, dict_matching, dict_base_images, dict_purpose_all, other_docker_relatedfiles, dict_compose_image, dict_compose_network, dict_compose_volume_counts, dict_compose_environment_counts, dict_compose_versions =\
                    run_main(repo_root, repo, 'latest', tags_dict,log_repo_root_path, save_version=1, save_image=True)
                #data_writer.writerow(
                #        [repo, 'latest', total_dockerfiles, dict_matching, tags_dict, all_dockerfiles,
                #         len(other_docker_relatedfiles)])

                data_writer.writerow(
                    [repo,manual_topic[index], total_dockerfiles, dict_matching, tags_dict, all_dockerfiles, len(images_tags), dict_base_images, dict_purpose_all, purple_category_weight[index],
                     len(dict_compose_versions.keys()), dict_compose_versions, dict_compose_image, dict_compose_network, dict_compose_volume_counts,
                     dict_compose_environment_counts, len(other_docker_relatedfiles)])

                # Remove the clone project after completing analysis
                FileManagement.remove_clone(repo_root)
            time.sleep(5)
        #os.rename(repo_path, repo_path2)
if __name__ == '__main__':
    main()