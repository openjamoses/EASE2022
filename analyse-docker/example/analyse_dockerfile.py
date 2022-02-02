import argparse
import csv
import json
import operator
import os
from pathlib import Path
from analysis.Analyse import DockerImage
from analysis.DockerOptions import ImageOptions
from parser.file_contents import FileManagement
from parser.parser import Parser
from yaml import load, dump
try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper
parser = argparse.ArgumentParser()
parser.add_argument('-d', '--dir', help="search directory")
parser.add_argument('-r', '--repo', help="repo org/name")
parser.add_argument('-v', '--repoversion', help="repo version")
parser.add_argument('-t', '--testing', help="run as testing", nargs="?", const="tangent")

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

def run_main(repo_dir,repo_name, repo_version, tags_dict,log_repo_root_path, save_version=0, save_image=False):
    repo_version = str(repo_version).replace("b'",'')

    docker_files = FileManagement.list_project_docker_files(repo_dir)
    docker_compose = FileManagement.list_project_docker_compose(repo_dir)
    other_docker_relatedfiles = FileManagement.list_project_other_docker_relatedfiles(repo_dir)
    path_output = ROOT_DIR+'/outputs/csv/'
    if not os.path.exists(ROOT_DIR+'/outputs/csv'):
        os.makedirs(ROOT_DIR+'/outputs/csv')
    if not os.path.exists(path_output + 'results_instruction.csv'):
         data_file = open(path_output + 'results_instruction.csv', mode='w', newline='', encoding='utf-8')
         data_writer = csv.writer(data_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
         data_writer.writerow(
             ['repos', 'repo_version','filename','instructions', 'instructions_count'])
         ## Second file
         data_file2 = open(path_output + 'results_options.csv', mode='w', newline='', encoding='utf-8')
         data_writer2 = csv.writer(data_file2, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
         data_writer2.writerow(
             ['repos', 'repo_version', 'filename', 'option', 'option_count', 'category'])

         data_file3 = open(path_output + '/options_raw_details.csv', mode='w', newline='',
                           encoding='utf-8')
         data_writer3 = csv.writer(data_file3, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
         data_writer3.writerow(
             ['repos', 'repo_version', 'filename', 'option','total_counts', 'details'])

         data_file4 = open(path_output + '/compose_data.csv', mode='w', newline='',
                           encoding='utf-8')
         data_writer4 = csv.writer(data_file4, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
         data_writer4.writerow(
             ['repos', 'repo_version', 'filename', 'services', 'images', 'ports', 'network', 'environment', 'volume', 'depend_on'])

         data_file5 = open(path_output + '/compose_raw_details.csv', mode='w', newline='',
                           encoding='utf-8')
         data_writer5 = csv.writer(data_file5, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
         data_writer5.writerow(
             ['repos', 'repo_version', 'filename', 'raw_details'])
    else:
        data_file = open(path_output + 'results_instruction.csv', mode='a+', newline='', encoding='utf-8')
        data_writer = csv.writer(data_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        ## Second file
        data_file2 = open(path_output + 'results_options.csv', mode='a+', newline='', encoding='utf-8')
        data_writer2 = csv.writer(data_file2, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

        data_file3 = open(path_output + '/options_raw_details.csv', mode='a+', newline='',
                          encoding='utf-8')
        data_writer3 = csv.writer(data_file3, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

        data_file4 = open(path_output + '/compose_data.csv', mode='a+', newline='',
                          encoding='utf-8')
        data_writer4 = csv.writer(data_file4, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)


        data_file5 = open(path_output + '/compose_raw_details.csv', mode='a+', newline='',
                          encoding='utf-8')
        data_writer5 = csv.writer(data_file5, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

    # , repo_dir, repo_name, repo_version
    docker_image_contents = FileManagement.get_file_contents(docker_files)
    imageOptions = ImageOptions()
    parser = Parser()

    tag_image_list = []
    tag_list = []
    matching_str = ''
    for key, val in tags_dict.items():
        for val2 in val:
            tag_image_list.append(str(key)+":"+str(val2))
            tag_list.append(str(val2))
            if repo_name in str(val2):
                matching_str += repo_name+', '
    dict_matching = {}
    all_dockerfiles = set()
    total_dockerfiles = 0

    dict_base_images = {}
    dict_purpose_all = {}



    for file_, source in docker_image_contents.items():
        dockerImage = DockerImage()
        total_dockerfiles +=1
        #print (type(source))
        #print (source)
        #print(file_)
        parser.content = source
        json_data = json.loads(parser.json)
        dockerImage.analyse(json_data)
        instructions_dict = dockerImage.instructions_dict
        instructions_options_dict = dockerImage.instructions_options_dict
        options_data = dockerImage.option_data
        file_ = str(file_).replace(str(repo_dir), '')
        file_name = str(file_).split('/')[len(str(file_).split('/')) - 1]
        all_dockerfiles.add(file_)
        if 'FROM' in options_data.keys():
            dict_base_images[file_] = options_data['FROM']

        for val in tag_list:
            if val in file_:
                matching_str += tag_image_list[tag_list.index(val)]
                if val in dict_matching.keys():
                    val2 = dict_matching[val]
                    val2.append(file_)
                    dict_matching[val] = val2
                else:
                    dict_matching[val] = [file_]


        for key, val in instructions_dict.items():
            data_writer.writerow(
                [repo_name, repo_version, file_, key, val])
        dict_purpose = {}

        for key, val in instructions_options_dict.items():
            data_writer2.writerow(
                [repo_name, repo_version, file_, key, val, imageOptions.get_category(key)])
            if imageOptions.get_category(key) in dict_purpose.keys():
                dict_purpose[imageOptions.get_category(key)] += val
            else:
                dict_purpose[imageOptions.get_category(key)] = val
        sorted_d = dict(sorted(dict_purpose.items(), key=operator.itemgetter(1), reverse=True))
        dict_purpose_all[file_] = sorted_d
        for key, val in options_data.items():
            data_writer3.writerow(
                [repo_name, repo_version, file_, key, len(val), val])
        if save_image:
            if not os.path.exists(log_repo_root_path + '/'+repo_version):
                os.makedirs(log_repo_root_path + '/'+repo_version)
            docker_root_path = log_repo_root_path + '/'+repo_version
            if '/' in str(file_):
                docker_root_path = log_repo_root_path + '/' + repo_version+'/'+str(file_)[0:str(file_).rindex('/')]
            if not os.path.exists(docker_root_path):
                Path(docker_root_path).mkdir(parents=True, exist_ok=True)
            with open(docker_root_path+'/'+file_name, "w") as _file:
                _file.write(source)
    data_file.close()
    data_file2.close()
    data_file3.close()

    docker_compose_contents = FileManagement.get_file_contents(docker_compose)

    dict_compose_image = {}
    dict_compose_versions = {}
    dict_compose_network = {}
    dict_compose_volume_counts = {}
    dict_compose_environment_counts = {}
    for file_, source in docker_compose_contents.items():
        try:
            #with open("docker-compose.yml", 'r') as ymlfile:
            data = load(source, Loader=Loader)
            file_ = str(file_).replace(str(repo_dir), '')
            # docker_config = yaml.load(ymlfile)
            #for key, val in data.items():
            #    print(key, val)
            #print('******\n')
            if 'version' in data.keys():
                dict_compose_versions[file_] = data['version']
            if 'volumes' in data.keys():
                dict_compose_volume_counts[file_] = len(data['volumes'])
            if 'networks' in data.keys():
                dict_compose_network[file_] = data['networks']
            images_list = []
            for key, val in data['services'].items():
                image = ''; environment = ''; volumes = ''; ports = ''; depends_on = ''; networks = ''
                if 'image' in val.keys():
                    image = val['image']
                    images_list.append(str(key)+'; '+str(image))
                if 'environment' in val.keys():
                    environment = val['environment']
                    if str(file_) in dict_compose_environment_counts.keys():
                        dict_compose_environment_counts[str(file_)] += len(environment)
                    else:
                        dict_compose_environment_counts[str(file_)] = len(environment)
                if 'volumes' in val.keys():
                    volumes = val['volumes']

                if 'ports' in val.keys():
                    ports = val['ports']
                if 'depends_on' in val.keys():
                    depends_on = val['depends_on']
                if 'networks' in val.keys():
                    networks = val['networks']
                data_writer4.writerow(
                    [repo_name, repo_version, file_, key, image, ports, networks, environment,
                     volumes, depends_on])
            dict_compose_image[file_] = images_list
            data_writer5.writerow(
                [repo_name, repo_version, file_, data])
            file_name = str(file_).split('/')[len(str(file_).split('/')) - 1]
            if save_image:
                if not os.path.exists(log_repo_root_path + '/' + repo_version):
                    os.makedirs(log_repo_root_path + '/' + repo_version)
                docker_root_path = log_repo_root_path + '/' + repo_version
                if '/' in str(file_):
                    docker_root_path = log_repo_root_path + '/' + repo_version + '/' + str(file_)[
                                                                                       0:str(file_).rindex('/')]
                if not os.path.exists(docker_root_path):
                    Path(docker_root_path).mkdir(parents=True, exist_ok=True)
                with open(docker_root_path + '/' + file_name, "w") as _file:
                    _file.write(source)

            #print(key, val)
        except Exception as e:
            print('Error parsing compose: ', e)
    data_file4.close()
    data_file5.close()
    return total_dockerfiles, all_dockerfiles, dict_matching, dict_base_images, dict_purpose_all, other_docker_relatedfiles, dict_compose_image, dict_compose_network, dict_compose_volume_counts, dict_compose_environment_counts, dict_compose_versions
def exit_if_invalid_args(args):
    if args.dir is None or os.path.isfile(args.dir):
        raise SystemExit("ERROR: -d --dir arg should be directory.")
    if args.repo is None:
        raise SystemExit("ERROR: -r --repo arg should be repo org/name.")
    if args.repoversion is None:
        raise SystemExit("ERROR: -v --repoversion arg should be repo release version.")

if __name__ == "__main__":
    args = parser.parse_args()
    exit_if_invalid_args(args)
    repo_dir = os.path.abspath(args.dir)
    repo_name = args.repo
    repo_version = args.repoversion
    run_main(repo_dir,repo_name, repo_version)