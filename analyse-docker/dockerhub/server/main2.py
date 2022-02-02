import pandas as pd
import subprocess
import os
import csv
import json
from datetime import datetime
import time
from os import walk
import time

from downloader import Downloader

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
#from downloader import Downloader


def select_tags(list_tags):
    tags_ = []
    for i in range(len(list_tags)):
        if i==0 or i==(len(list_tags)-1) or i == round((len(list_tags)/2)) or i==round(len(list_tags)*0.25) or  i==round(len(list_tags)*0.75):
            tags_.append(list_tags[i])
    return tags_
def select_tags_latest(list_tags):
    if 'latest' in list_tags:
        return 'latest'
    else:
        latest = ''
        for i in range(len(list_tags)-1, -1, -1):
            if 'latest' in list_tags[i]:
                latest = list_tags[i]
            break
        if latest == '':
            if len(list_tags) > 0:
                latest = list_tags[len(list_tags)-1]
        if latest == '':
            latest == 'latest'
        return latest

class DockerImages:
    def __init__(self, path=os.getcwd(), save_log=True, download_manifest=True):
        if not os.path.exists(path+'/csv'):
            os.makedirs(path+'/csv')
        self.csv_path = path+'/csv'
        if not os.path.exists(path+'/logs'):
            os.makedirs(path+'/logs')
        self.log_path = path+'/logs'
        self.total_images = 0
        self.image_stars = {}
        if not os.path.exists(path+'/logs/info'):
            os.makedirs(path+'/logs/info')
        self.info_path = path+'/logs/info'

        if not os.path.exists(path+'/layers'):
            os.makedirs(path+'/layers')
        self.layers_path = path+'/layers/'

        self.save_log = save_log
        self.download_manifest = download_manifest
        self.images_tags = {}
        self.images_layers = {}
        self.images_env = {}

        model = 'w'
        if not os.path.exists(self.csv_path + '/Images_Info_stats.csv'):
            self.data_file_stats = open(self.csv_path + '/Images_Info_stats.csv', mode='w',
                               newline='',
                               encoding='utf-8')
            self.data_file_tags = open(self.csv_path + '/Images_tags.csv', mode='w',
                                  newline='',
                                  encoding='utf-8')
            self.data_file_layers = open(self.csv_path + '/Images_layers.csv', mode='w',
                                    newline='',
                                    encoding='utf-8')
        else:
            model = 'a+'
            self.data_file_stats = open(self.csv_path + '/Images_Info_stats.csv', mode=model,
                                   newline='',
                                   encoding='utf-8')
            self.data_file_tags = open(self.csv_path + '/Images_tags.csv', mode=model,
                                  newline='',
                                  encoding='utf-8')
            self.data_file_layers = open(self.csv_path + '/Images_layers.csv', mode=model,
                                    newline='',
                                    encoding='utf-8')
        self.data_writer_stats = csv.writer(self.data_file_stats, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        self.data_writer_tags = csv.writer(self.data_file_tags, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        self.data_writer_layers = csv.writer(self.data_file_layers, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

        if model == 'w':
            self.data_writer_stats.writerow(['repo', 'Image', 'Name', 'Digest', 'Tags', 'Created', 'DockerVersion', 'Labels', 'Architecture', 'Os',
             'Layers', 'Env'])
            self.data_writer_tags.writerow(['repo', 'Image', 'Name', 'RepoTags'])
            self.data_writer_layers.writerow(['repo', 'Image', 'Name', 'Layers'])

    def search_all(self, keywords=[]):
        dt_string = datetime.now().strftime("%Y-%m-%d_%H.%M")
        data_file = open(self.csv_path + '/Docker_images_{}.csv'.format(dt_string), mode='w', newline='',
                         encoding='utf-8')
        data_writer = csv.writer(data_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        data_writer.writerow(['Keyword', 'Name', 'Description', 'Stars', 'IsOfficial', 'IsAutomated'])
        for keyword in keywords:
            log_ = self._search_by_keyword(keyword)
            try:
                file1 = open(log_, 'r', encoding='utf-8')
                Lines = file1.readlines()
                count = 0
                # Strips the newline character
                for line in Lines:
                    line_json = eval(line)
                    self.total_images += 1
                    data_writer.writerow(
                        [keyword, line_json['Name'], line_json['Description'], line_json['StarCount'],
                         line_json['IsOfficial'],
                         line_json['IsAutomated']])
                    if not line_json['Name'] in self.image_stars:
                        self.image_stars[line_json['Name']] = line_json['StarCount']
                    #self.image_list.append(line_json['Name'])
                file1.close()
            except Exception as e:
                print(e)

            self._remove_path(log_)
            #FileManagement.remove_clone(log_)
        data_file.close()

    def _search_by_keyword(self,keyword):

        log_ = self.log_path + '/log_' + keyword + '-{}.txt'.format(datetime.now().strftime("%Y-%m-%d-%H.%M"))
        # process_command = 'docker search ' + keyword + ' > ' + log_
        process_command = "docker search --format='{{json .}}' " + keyword + " > " + log_

        p = subprocess.Popen(process_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        output = ""
        for line in p.stdout.readlines():
            output = output + str(line) + '\n'
        retval = p.wait()
        if retval == 0:
            print("Docker search successful for keyword: {}!".format(keyword))
        else:
            print("Docker search Error for keyword {}!".format(keyword))
            print(output)
        return log_

    def get_info_images(self, repo, image_list, extraction_version=1):
        #dt_string = datetime.now().strftime("%Y-%m-%d-%H-%M")

        #for repo, image_list in repos_data.items():
        for doker_image in image_list:
            since = time.time()
            ## Only consider image with atleast 1 stars
            #print(star_)
            #if int(star_) > 0:
            print('Started inspecting image - {}'.format(doker_image))
            log_info = self._info(self.info_path, doker_image)

            #print('log info extracted: ', log_info)

            try:
                with open(log_info) as f:
                    json_data = json.load(f)
                #print(json_data)
                self.images_tags[doker_image] = json_data['RepoTags']
                self.images_layers[doker_image] = json_data['Layers']
                self.images_env[doker_image] = json_data['Env']
                count_layers = 0
                count_env = 0
                count_labels = 0
                count_tags = 0
                try:
                    count_labels = len(json_data['Labels'])
                except:
                    pass
                try:
                    count_layers = len(json_data['Layers'])
                    for layer in json_data['Layers']:
                        self.data_writer_layers.writerow([repo, doker_image, json_data['Name'], layer])
                except:
                    pass
                try:
                    count_env = len(json_data['Env'])
                except:
                    pass
                try:
                    count_tags = len(json_data['RepoTags'])
                    list_tags = []
                    for tag_ in json_data['RepoTags']:
                        self.data_writer_tags.writerow([repo,doker_image, json_data['Name'], tag_])
                        list_tags.append(tag_)
                    #if len(list_tags) <= 4:
                    #    selected_tags = list_tags
                    #else:
                    #    selected_tags = select_tags(list_tags)
                    #selected_tags = select_tags_latest(list_tags)

                    print('going to check tags now')
                    #if '/' in str(doker_image):
                    image_name = str(doker_image) #.split('/')[0]
                    if '/' in str(image_name):
                        image_name = str(image_name).replace('/', '_')
                    since = time.time()
                    downloader = Downloader(root_path=path_download, layer_path=self.layers_path,
                                            repo=repo, image_name=image_name)
                    #downloaded_tags = downloader._check_images_tags_downloaded(doker_image, selected_tags)
                    #print("Image: {}, selected {}/{}, Not downloaded previusly: {}, Tags: ".format(image_,
                    #                                                                               len(selected_tags),
                    #                                                                               len(list_tags), len(
                    #        downloaded_tags)), selected_tags, downloaded_tags)

                    #if len(downloaded_tags) > 0:
                    #print('Latest tag selected for: {} is: {}'.format(doker_image, selected_tags))
                    dict_image_tags = {}
                    #print(type(doker_image), doker_image)

                    #dict_image_tags[doker_image] = [selected_tags]
                    downloader.download_manifest_groups(doker_image)
                    time_elapsed_1 = time.time() - since
                    print(' -- completed in {:.0f}m {:.0f}s:'.format(
                        time_elapsed_1 // 60, time_elapsed_1 % 60))

                    print(' Called successfully!!!!!!')
                except Exception as e:
                    print(" Error: ", e)
                    pass

                print(len(json_data['RepoTags']))
                self.data_writer_stats.writerow(
                    [repo,doker_image, json_data['Name'], json_data['Digest'], count_tags, json_data['Created'], json_data['DockerVersion'], count_labels, json_data['Architecture'], json_data['Os'],
                     count_layers, count_env])

                #print(json_data['Digest'], json_data['Name'])

            except Exception as e:
                print(" Error overral: ", e)
            #    pass
                #print(e, 'error occyred in info!')
                #if os.path.exists(log_info):
                #    os.remove(log_info)
                #self._remove_path(log_info)
            time.sleep(5)
    def close_files(self):
        self.data_file_stats.close()
        self.data_file_tags.close()
        self.data_file_layers.close()
    def _info(self,info_path, doker_image):
        doker_image_str = ''
        if '/' in str(doker_image):
            doker_image_str = str(doker_image).replace('/', '_')
        log_info = info_path+ '/info_' + doker_image_str + '.log'
        # process_command = 'docker search ' + keyword + ' > ' + log_
        process_command = "skopeo inspect docker://"+doker_image+" > " + log_info

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
        return log_info

    def _remove_path(self, path):
        if self.save_log == False:
            if os.path.exists(path):
                os.remove(path)

#path = './images'
if not os.path.exists(ROOT_DIR+'/outputs'):
    os.makedirs(ROOT_DIR+'/outputs')
if not os.path.exists(ROOT_DIR+'/outputs/dockerhub'):
    os.makedirs(ROOT_DIR+'/outputs/dockerhub')
#if not os.path.exists('../outputs/dockerhub/dockerimages'):
#    os.makedirs('../outputs/dockerhub/dockerimages')
path_download = ROOT_DIR+'/outputs/dockerhub/downloads'
if not os.path.exists(path_download):
    os.makedirs(path_download)
path = ROOT_DIR+'/outputs/dockerhub'
#path = './'
#df_data = pd.read_excel(open(path+'Ml Docker projects-v2.xlsx', 'rb'), sheet_name='filtered-final')

#df_data = pd.read_csv('../../input.csv')
#Repos = df_data.Repos.values.tolist()
#docker_image = df_data.docker_image.values.tolist()
#path = '/Volumes/Cisco/Summer2022/Docker/Dataset/repos/combined/'
df_data = pd.read_csv('../../combine_images.csv')#tags_matching - final.csv
Repos = df_data.Repos.values.tolist()
#docker_images = df_data.docker_images.values.tolist()
latest_image = df_data.latest_image.values.tolist()
both = df_data.both.values.tolist()
manual_topic = df_data.manual_topic.values.tolist()

path_details = '/Volumes/Cisco/Summer2022/Docker/Dataset/downloads/combined/layers/'
dockerImages = DockerImages(path=path, save_log=True, download_manifest=True)

repos_data = {}
for i in range(len(Repos)): #error pull limits on index 181-235
    if not 'remove' in str(manual_topic[i]):
        try:
            #print(repos[i])
            list_images = []
            index = Repos.index(Repos[i])
            image_lst = eval(latest_image[index])
            #split_image = image_.split(', ')
            path_to_file = path_details + 'details/' + str(Repos[i])
            if not os.path.exists(path_to_file):
                for image in image_lst:
                    list_images.append(image)
                    #list_repos.append(Repos[i])
                #print(i, repos[i], split_image)
                print(i, Repos[i], len(list_images))
                dockerImages.get_info_images(Repos[i],list_images, extraction_version=1)
        except Exception as e:
            print('Error writing reading repos: ', e)
        #repos_data[Repos[i]] = list_images
        # print('Total images: ', len(list_images))
dockerImages.close_files()

