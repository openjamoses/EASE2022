#!/usr/bin/env python
# if running in py3, change the shebang, drop the next import for readability (it does no harm in py3)
from __future__ import print_function   # py2 compatibility
import subprocess
import os
import csv
import json
import numpy as np
from datetime import datetime
import pathlib
import time
from pathlib import Path
from file_contents import FileManagement
from collections import defaultdict
import hashlib
import os
import sys


def chunk_reader(fobj, chunk_size=1024):
    """Generator that reads a file in chunks of bytes"""
    while True:
        chunk = fobj.read(chunk_size)
        if not chunk:
            return
        yield chunk


def get_hash(filename, first_chunk_only=False, hash=hashlib.sha1):
    hashobj = hash()
    file_object = open(filename, 'rb')

    if first_chunk_only:
        hashobj.update(file_object.read(1024))
    else:
        for chunk in chunk_reader(file_object):
            hashobj.update(chunk)
    hashed = hashobj.digest()

    file_object.close()
    return hashed


def check_for_duplicates(path, hashes_by_size, hashes_on_1k, hashes_full,hashes_file_size, hashes_layers, layername):
    #hashes_by_size = defaultdict(list)  # dict of size_in_bytes: [full_path_to_file1, full_path_to_file2, ]
    #hashes_on_1k = defaultdict(list)  # dict of (hash1k, size_in_bytes): [full_path_to_file1, full_path_to_file2, ]
    #hashes_full = {}   # dict of full_file_hash: full_path_to_file_string

    #for path in paths:
    for dirpath, dirnames, filenames in os.walk(path):
        # get all files that have the same size - they are the collision candidates
        for filename in filenames:
            full_path = os.path.join(dirpath, filename)
            try:
                # if the target is a symlink (soft one), this will
                # dereference it - change the value to the actual target file
                full_path = os.path.realpath(full_path)
                file_size = os.path.getsize(full_path)
                hashes_by_size[file_size].append(full_path)

            except (OSError,):
                # not accessible (permissions, etc) - pass on
                continue


    # For all files with the same file size, get their hash on the 1st 1024 bytes only
    for size_in_bytes, files in hashes_by_size.items():
        if len(files) < 2:
            continue    # this file size is unique, no need to spend CPU cycles on it

        for filename in files:
            try:
                small_hash = get_hash(filename, first_chunk_only=True)
                # the key is the hash on the first 1024 bytes plus the size - to
                # avoid collisions on equal hashes in the first part of the file
                # credits to @Futal for the optimization
                hashes_on_1k[(small_hash, size_in_bytes)].append(filename)
                if filename in hashes_layers.keys():
                    hashes_layers[filename].append(layername)
                else:
                    hashes_layers[filename] = [layername]
                if filename in hashes_file_size.keys():
                    hashes_file_size[filename].append(size_in_bytes)
                else:
                    hashes_file_size[filename] = [size_in_bytes]
            except (OSError,):
                # the file access might've changed till the exec point got here
                continue



class Downloader:
    def __init__(self, root_path=os.getcwd(), layer_path=os.getcwd(), repo=None, image_name='all'):
        self.root_path = root_path
        self.repo = repo
        #if not os.path.exists(self.root_path + '/details'):
        #    os.makedirs(self.root_path + '/details')
        self.csv_path = layer_path #self.root_path + '/details'
        #dt_string = datetime.now().strftime("%Y-%m-%d")
        mode = 'w'
        if os.path.exists(self.csv_path + '/Manifest_details.csv'):
            mode = 'a+'

        self.data_file_manifest = open(self.csv_path + '/Manifest_details.csv',
                                  mode=mode, newline='',
                                  encoding='utf-8')
        self.data_writer_manifest = csv.writer(self.data_file_manifest, delimiter=',', quotechar='"',
                                               quoting=csv.QUOTE_MINIMAL)


        ## config info
        self.data_file_config = open(self.csv_path + '/Manifest_Config_info.csv',
                                mode=mode, newline='',
                                encoding='utf-8')
        self.data_writer_config = csv.writer(self.data_file_config, delimiter=',', quotechar='"',
                                             quoting=csv.QUOTE_MINIMAL)
        self.data_file_history = open(self.csv_path + '/Manifest_History.csv',
                                 mode=mode, newline='',
                                 encoding='utf-8')
        self.data_writer_history = csv.writer(self.data_file_history, delimiter=',', quotechar='"',
                                              quoting=csv.QUOTE_MINIMAL)
        # self.data_file_duplicate = open(self.csv_path + '/posible_duplicate{}.csv'.format(run_version),
        #                              mode=mode, newline='',
        #                              encoding='utf-8')
        # self.data_writer_duplicate = csv.writer(self.data_file_duplicate, delimiter=',', quotechar='"',
        #                                      quoting=csv.QUOTE_MINIMAL)

        path_details = self.csv_path + '/details/'+str(self.repo)
        if not os.path.exists(path_details):
            Path(path_details).mkdir(parents=True, exist_ok=True)
        #if not os.path.exists(self.csv_path + '/details'):
        #    os.makedirs(self.csv_path + '/details')
        mode2 = 'w'
        if os.path.exists(path_details + '/Image_layers_info_{}.csv'.format(image_name)):
            mode2 = 'a+'

        self.data_file_layers_info = open(path_details + '/Image_layers_info_{}.csv'.format(image_name), mode=mode2, newline='',
                                 encoding='utf-8')
        self.data_writer_layers_info = csv.writer(self.data_file_layers_info, delimiter=',', quotechar='"',
                                              quoting=csv.QUOTE_MINIMAL)

        self.data_file_layers_info_summary = open(self.csv_path + '/Image_layers_info_summary.csv', mode=mode, newline='',
                                     encoding='utf-8')
        self.data_writer_layers_info_summary = csv.writer(self.data_file_layers_info_summary, delimiter=',', quotechar='"',
                                                  quoting=csv.QUOTE_MINIMAL)

        # self.data_file_duplicate = open(self.csv_path + '/posible_duplicate{}.csv'.format(run_version),
        #                                mode=mode, newline='',
        #                                encoding='utf-8')
        # self.data_writer_duplicate = csv.writer(self.data_file_duplicate, delimiter=',', quotechar='"',
        #                                        quoting=csv.QUOTE_MINIMAL)
        if mode == 'w':
            self.data_writer_manifest.writerow(
                ['Image', 'RepoTag', 'schemaVersion', 'mediaType', 'config_mediaType', 'config_size', 'config_digest',
                 'layers_mediaType', 'layers_size', 'layers_digest'])

            self.data_writer_config.writerow(
                ['Image', 'RepoTag', 'config_mediaType', 'config_size', 'config_digest',
                 'architecture', 'os', 'created', 'config_hostname', 'config_domain',
                 'config_User', 'config_env_count', 'Env', 'Cmd', 'ArgsEscaped', 'Image_shaa', 'Volumes', 'WorkingDir',
                 'Entrypoint', 'OnBuild', 'Labels', 'maintainer', 'container', 'cont_hostname', 'cont_domain',
                 'cont_User',
                 'cont_env_count', 'cont_Env', 'cont_Cmd', 'cont_Image_shaa', 'cont_Volumes', 'cont_WorkingDir',
                 'cont_Entrypoint',
                 'cont_OnBuild', 'cont_Labels', 'cont_maintainer', 'rootfs_layers_count', 'rootfs_layers', 'history'])

            self.data_writer_history.writerow(['Image', 'RepoTag', 'config_size', 'config_digest', 'created', 'created_by', 'empty_layer', 'comments'])

            # self.data_writer_duplicate.writerow(
            #    ['Image', 'RepoTag', 'filename', 'duplicate', 'size', 'digest_name', 'digest_total', 'unique_digest'])

            self.data_writer_layers_info_summary.writerow(
            ['Image', 'RepoTag', 'layer_digest', 'total_files', 'total_directory','total_empty_dirs', 'file_type', 'file_type_counts', 'avg_level', 'median_level', 'max_level', 'min_level', '', 'avg_size', 'median_size', 'max_size', 'min_size'])
        if mode2 == 'w':
            self.data_writer_layers_info.writerow(
                ['Image', 'RepoTag', 'layer_digest', 'file_name', 'file_path', 'file_size', 'extension', 'level'])

    def download_manifest_groups(self, image_):
        #for image_, tag_list in image_tags.items():
            #for tag in tag_list:

        tag = str(image_).split(':')[-1]
        image_ = str(image_).split(':')[0]
        docker_image_ = image_+':'+str(tag)
        config_file = 'unknown'
        if '/' in image_:
            if not os.path.exists(self.root_path+'/'+str(image_).split('/')[0]):
                os.makedirs(self.root_path+'/'+str(image_).split('/')[0])
            if not os.path.exists(self.root_path+'/'+str(image_)):
                os.makedirs(self.root_path+'/'+str(image_))
        else:
            if not os.path.exists(self.root_path+'/'+str(image_)):
                os.makedirs(self.root_path+'/'+str(image_))
        image_dir = self.root_path + '/' + str(image_)+'/'+str(tag)
        #print('inside downloader x1', docker_image_)
        if not os.path.exists(image_dir):
            os.makedirs(image_dir)
            self._download(docker_image_, image_dir)
        #print('inside downloader x2', docker_image_)
        try:
            if os.path.exists(image_dir + '/manifest.json'):
                with open(image_dir + '/manifest.json') as f:
                    json_data = json.load(f)
                config_mediaType = json_data['config']['mediaType']
                config_size = json_data['config']['size']
                config_digest = json_data['config']['digest']
                for layer_obj in json_data['layers']:
                    row = [image_, tag, json_data['schemaVersion'], json_data['mediaType'],
                           json_data['config']['mediaType'],
                           json_data['config']['size'], json_data['config']['digest'],
                           layer_obj['mediaType'], layer_obj['size'], layer_obj['digest']]
                    self.data_writer_manifest.writerow(row)

                ### Configurations:
                config_file = str(config_digest).split(':')[1]
                if os.path.exists(image_dir + '/' + config_file):
                    with open(image_dir + '/' + config_file) as f:
                        json_data = json.load(f)
                    print(' ---- config found successfull!: ')

                    env_count_config = 0
                    env_count_cont = 0
                    try:
                        env_count_config = len(json_data['config']['Env'])
                    except:
                        pass
                    try:
                        env_count_cont = len(json_data['container_config']['Env'])
                    except:
                        pass
                    layers_str = ''
                    layers_count = 0
                    try:
                        for layer in json_data['rootfs']['diff_ids']:
                            layers_str += str(layer) + '/'
                            layers_count += 1
                    except:
                        pass
                    #print(' config son_data: ', json_data)

                    config_label = json_data['config']['Labels']
                    container_config_label = ''
                    try:
                        container_config_label = json_data['container_config']['Labels']
                    except:
                        pass

                    config_maintainer = ''
                    container_config_maintainer = ''
                    if config_label != None:
                        try:
                            config_maintainer = json_data['config']['Labels']['maintainer']
                        except:
                            pass
                    if container_config_label != None:
                        try:
                            container_config_maintainer = json_data['container_config']['Labels']['maintainer']
                        except:
                            pass
                    ArgsEscaped = ''
                    try:
                        ArgsEscaped = json_data['config']['ArgsEscaped']
                    except:
                        pass
                    container = ''
                    Hostname = ''; Domainname = ''; User = ''; Env = ''; Cmd = ''; Image = ''; Volumes = ''; WorkingDir = ''; Entrypoint = ''; OnBuild = ''; Labels = '';
                    try:
                        container = json_data['container']
                        Hostname = json_data['container_config']['Hostname']
                        Domainname = json_data['container_config']['Domainname']
                        User = json_data['container_config']['User']
                        Env = json_data['container_config']['Env']
                        Cmd = json_data['container_config']['Cmd']
                        Image = json_data['container_config']['Image']
                        Volumes = json_data['container_config']['Volumes']
                        WorkingDir = json_data['container_config']['WorkingDir']
                        Entrypoint = json_data['container_config']['Entrypoint']
                        OnBuild = json_data['container_config']['OnBuild']
                        Labels = json_data['container_config']['Labels']
                    except:
                        pass
                    Hostname_conf = ''; Domainname_conf = ''; User_conf = ''; Env_conf = ''; Cmd_conf = '';Image_conf = ''; Volumes_conf=''; WorkingDir_conf = ''; Entrypoint_conf=''; OnBuild_conf='';
                    try:
                        Hostname_conf = json_data['config']['Hostname']
                        Domainname_conf = json_data['config']['Domainname']
                        User_conf = json_data['config']['User']
                        Env_conf = json_data['config']['Env']
                        Cmd_conf = json_data['config']['Cmd']
                        Image_conf = json_data['config']['Image']
                        Volumes_conf = json_data['config']['Volumes']
                        WorkingDir_conf = json_data['config']['WorkingDir']
                        Entrypoint_conf = json_data['config']['Entrypoint']
                        OnBuild_conf = json_data['config']['OnBuild']
                    except:
                        pass
                    row = [image_, tag, config_mediaType, config_size, config_digest,
                           json_data['architecture'], json_data['os'], json_data['created'],
                           Hostname_conf, Domainname_conf,
                           User_conf, env_count_config, Env_conf,
                           Cmd_conf, ArgsEscaped,
                           Image_conf, Volumes_conf,
                           WorkingDir_conf, Entrypoint_conf,
                           OnBuild_conf, config_label,
                           config_maintainer, container,
                           Hostname, Domainname, User, env_count_cont, Env, Cmd, Image,
                           Volumes, WorkingDir, Entrypoint, Labels, container_config_maintainer,
                           layers_str, layers_str, len(json_data['history'])]
                    self.data_writer_config.writerow(row)
                    #print(' --- history obj: ', history_obj)
                    for history_obj in json_data['history']:
                        created_by = ''
                        empty_layer = ''
                        comment = ''
                        try:
                            created_by = history_obj['created_by']
                        except:
                            pass
                        try:
                            empty_layer = history_obj['empty_layer']
                        except:
                            pass
                        try:
                            comment = history_obj['comment']
                        except:
                            pass
                        row_history = [image_, tag,config_size, config_digest, history_obj['created'], created_by, empty_layer, comment]
                        self.data_writer_history.writerow(row_history)

                else:
                    print(' config not found: ')

            else:
                print('  error manifest was not found..!', image_dir + '/manifest.json')

        except Exception as e:
            print('Manifest or config error: ', e)


        self.analyse_layers_(image_, tag, image_dir, config_file)
        self.data_file_manifest.close()
        self.data_file_config.close()
        self.data_file_history.close()
        self.data_file_layers_info.close()
        self.data_file_layers_info_summary.close()
    def _check_images_tags_downloaded(self, image_, image_tags):
        list_tags_ = []
        for tag in image_tags:
            docker_image = image_+':'+str(tag)
            if not os.path.exists(self.root_path + '/' + str(docker_image)):
                list_tags_.append(tag)
        return list_tags_
    def download_manifest_single(self, image_, image_tags):
        for tag in image_tags:
            docker_image = image_+':'+str(tag)
            if '/' in docker_image:
                if not os.path.exists(self.root_path+'/'+str(docker_image).split('/')[0]):
                    os.makedirs(self.root_path+'/'+str(docker_image).split('/')[0])
            if not os.path.exists(self.root_path + '/' + str(docker_image)):
                os.makedirs(self.root_path + '/' + str(docker_image))
            image_dir = self.root_path + '/' + str(docker_image)
            self._download(docker_image, image_dir)
    def _download(self, image, image_dir):
        process_command = "skopeo copy docker://"+image+" dir:"+format(image_dir)
        p = subprocess.Popen(process_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        output = ""
        for line in p.stdout.readlines():
            output = output + str(line) + '\n'
        retval = p.wait()
        if retval == 0:
            print("Image download Success for {}!".format(image))
        else:
            print("Image download Error for {}!".format(image))
            print(output)
        return retval
    def analyse_layers_(self, image_, tag, image_file_path, config_file):
        # hashes_by_size = defaultdict(list)  # dict of size_in_bytes: [full_path_to_file1, full_path_to_file2, ]
        # hashes_on_1k = defaultdict(list)  # dict of (hash1k, size_in_bytes): [full_path_to_file1, full_path_to_file2, ]
        # hashes_full = {}  # dict of full_file_hash: full_path_to_file_string
        # hashes_layers = {}
        # hashes_file_size = {}
        for layer_name in os.listdir(image_file_path):
            if len(layer_name) == 64 and str(layer_name) != config_file:
                if not os.path.exists(image_file_path+'/'+str(layer_name)+'_temp'):
                    os.makedirs(image_file_path+'/'+str(layer_name)+'_temp')
                extracted_path = image_file_path+'/'+str(layer_name)+'_temp'
                FileManagement.extract_layer_tarfar(image_file_path=image_file_path, docker_layer_tarfile=layer_name)
                total_empty = 0
                total_dirs = 0
                total_files = 0
                dict_extension_ = {}
                dict_extension_size = {}
                dict_extension_level = {}
                for (dirpath, dirnames, filenames) in os.walk(extracted_path):
                    for dir_ in dirnames:
                        total_dirs += 1
                        if len(os.listdir(os.path.join(dirpath, dir_))) == 0:
                            # print (os.path.join(dirpath, dir_))
                            total_empty += 1

                    for file_ in filenames:
                        total_files += 1
                        file_complete_path = os.path.join(dirpath, file_)
                        file_levels = len(str(file_complete_path).replace(extracted_path, '').split('/'))
                        file_size = 0
                        if os.path.exists(file_complete_path):
                            file_size = os.path.getsize(file_complete_path)
                        file_extension = ''  # pathlib.Path(file_complete_path).suffix
                        extens_2 = pathlib.Path(file_complete_path).suffixes


                        if len(extens_2) == 0:
                            save_extension = 'none'
                        else:
                            save_extension = str(extens_2[0])
                            if save_extension.isnumeric():
                                save_extension = 'none'
                        if save_extension in dict_extension_.keys():
                            dict_extension_[save_extension] += 1
                            val_size = dict_extension_size.get(save_extension)
                            val_size.append(file_size)
                            dict_extension_size[save_extension] = val_size

                            val_level = dict_extension_level.get(save_extension)
                            val_level.append(file_levels - 1)
                            dict_extension_level[save_extension] = val_level

                        else:
                            dict_extension_[save_extension] = 1
                            dict_extension_size[save_extension] = [file_size]
                            dict_extension_level[save_extension] = [file_levels - 1]

                        if len(extens_2) == 1:
                            file_extension = save_extension #extens_2[0]
                        elif len(extens_2) > 1:
                            file_extension = save_extension #extens_2[0]

                            for ext_ in range(1, len(extens_2)):
                                file_extension += '.' + str(ext_)
                        else:
                            file_extension = save_extension

                        self.data_writer_layers_info.writerow(
                            [image_, tag, layer_name, file_, str(file_complete_path).replace(extracted_path, ''), file_size, file_extension,
                             file_levels-1])
                for key, val in dict_extension_.items():
                    self.data_writer_layers_info_summary.writerow(
                        [image_, tag, layer_name, total_files, total_dirs,total_empty, key,
                         val, np.mean(dict_extension_level.get(key)), np.median(dict_extension_level.get(key)), np.max(dict_extension_level.get(key)), np.min(dict_extension_level.get(key)), '', np.mean(dict_extension_size.get(key)),
                         np.median(dict_extension_size.get(key)), np.max(dict_extension_size.get(key)), np.min(dict_extension_size.get(key))])
                # check posible duplicates here
                # since_1 = time.time()
                # print(' ----- going to calculate the posible duplicate:')
                # #TODO: https://stackoverflow.com/questions/748675/finding-duplicate-files-and-removing-them
                # check_for_duplicates(extracted_path, hashes_by_size, hashes_on_1k, hashes_full, hashes_file_size, hashes_layers, layer_name)
                # time_elapsed_1 = time.time() - since_1
                #
                # print(' ----- finished calculate the posible duplicate in {:.0f}m {:.0f}s:'.format(time_elapsed_1 // 60, time_elapsed_1 % 60))
                #
                FileManagement.remove_clone(extracted_path)

                #FileManagement.remove_clone(image_file_path+'/'+str(layer_name))
                os.remove(image_file_path+'/'+str(layer_name))
        # For all files with the hash on the 1st 1024 bytes, get their hash on the full file - collisions will be duplicates
        '''for __, files_list in hashes_on_1k.items():
            if len(files_list) < 2:
                continue  # this hash of fist 1k file bytes is unique, no need to spend cpy cycles on it

            for filename in files_list:
                try:
                    full_hash = get_hash(filename, first_chunk_only=False)
                    duplicate = hashes_full.get(full_hash)
                    filesize = ''
                    try:
                        filesize = np.mean(hashes_file_size.get(filename))
                    except:
                        pass
                    layers_duplicate = hashes_layers.get(filename)
                    if duplicate:
                        print("Duplicate found: {} and {}".format(filename, duplicate))
                        self.data_writer_duplicate.writerow(
                            [image_, tag, filename, duplicate,filesize, set(layers_duplicate), len(layers_duplicate),
                             len(set(layers_duplicate))])
                    else:
                        hashes_full[full_hash] = filename
                except (OSError,):
                    # the file access might've changed till the exec point got here
                    continue'''

    def remove_files_in_directory(self, file_path, config_file):
        for (dirpath, dirnames, filenames) in os.walk(file_path):
            for file_ in filenames:
                if not 'manifest.json' in str(file_) or not config_file in str(file_):
                    if os.path.exists(file_path+'/'+str(file_)):
                        pass
                        #FileManagement.remove_clone(log_)
                        #os.remove(file_path+'/'+str(file_))
