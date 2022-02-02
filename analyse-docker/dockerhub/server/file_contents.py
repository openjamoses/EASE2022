import os
import shutil
import subprocess


class FileManagement:
    @staticmethod
    def list_project_docker_files(directory):
        directory = os.path.abspath(directory)
        list_of_files = list()
        for (dirpath, dirnames, filenames) in os.walk(directory):
            docker_files = list()
            for file in filenames:
                if file.endswith('Dockerfile'):
                    docker_files.append(os.path.join(dirpath, file))
            list_of_files.extend(docker_files)
        return list_of_files

    @staticmethod
    def read_file_source(file):
        try:
            source = open(file, "r")
            return source.read()
        except Exception:
            raise SystemExit("The file doesn't exist or it isn't a Dockerfile ...")

    @staticmethod
    def get_file_contents(files):
        dict_file_contents = {}
        for file in files:
            try:
                source = open(file, "r").read()

                dict_file_contents[file] = source
            except Exception:
                raise SystemExit("The file doesn't exist or it isn't a Dockerfile...")

            #docker_parser = Parser()

            #docker_parser.content = source.read()
            #result.extend(docker_parser.json)
        return dict_file_contents
    @staticmethod
    def remove_clone(repo_root):
        ## Try to remove tree; if failed show an error using try...except on screen
        try:
            shutil.rmtree(repo_root)
        except OSError as e:
            print ("Error: %s - %s." % (e.filename, e.strerror))
    @staticmethod
    def extract_layer_tarfar(image_file_path, docker_layer_tarfile):
        os.chdir(image_file_path)
        command_str = 'tar -xvzf {} --directory ./{}_temp'.format(docker_layer_tarfile,  docker_layer_tarfile)
        p = subprocess.Popen(command_str, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        output = ""
        for line in p.stdout.readlines():
            output = output + str(line) + '\n'
        retval = p.wait()
        if retval == 0:
            print("Layer tarfile extracted and saved successfully!")
        else:
            print("Error in tarfile extraction for {}!".format(docker_layer_tarfile))
            #print(output)
        return retval
        pass