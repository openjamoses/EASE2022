import pandas as pd
import subprocess
import os
import csv
import json
from datetime import datetime
import time
class DockerImages:
    def __init__(self, info_path):
        self.info_path = info_path
        self.total_images = 0
        self.image_stars = {}
        self.images_tags = {}
        self.images_layers = {}
        self.images_env = {}
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

    def get_info_images(self, image_list):
        for docker_image in image_list:
            print('Started inspecting image - {}'.format(docker_image))
            log_info = self._info(self.info_path, docker_image)
            try:
                with open(log_info) as f:
                    json_data = json.load(f)
                #print(json_data)
                self.images_tags[docker_image] = json_data['RepoTags']
                self.images_layers[docker_image] = json_data['Layers']
                self.images_env[docker_image] = json_data['Env']
            except Exception as e:
                print("Error while inspecting the docker image: ", docker_image, e)

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
            #print(output)
        return log_info

    def _remove_path(self, path):
        if self.save_log == False:
            if os.path.exists(path):
                os.remove(path)