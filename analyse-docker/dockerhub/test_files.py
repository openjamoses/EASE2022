import json
import os

import pathlib

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
def remove_files_in_directory(file_path):
    total_empty = 0
    for (dirpath, dirnames, filenames) in os.walk(file_path):
        for dir_ in dirnames:
            if len(os.listdir(os.path.join(dirpath, dir_))) == 0:
                #print (os.path.join(dirpath, dir_))
                total_empty += 1
        for file_ in filenames:
            file_complete_path = os.path.join(dirpath, file_)
            level_ = len(str(file_complete_path).replace(file_path, '').split('/'))
            file_extension = '' #pathlib.Path(file_complete_path).suffix
            extens_2 = pathlib.Path(file_complete_path).suffixes
            if len(extens_2) == 1:
                file_extension = extens_2[0]
            elif len(extens_2) > 1:
                file_extension = extens_2[0]
                for ext_ in range(1,len(extens_2)):
                    file_extension += '.'+str(ext_)

            #print (level_,file_extension, len(dirnames), file_complete_path)
                    # FileManagement.remove_clone(log_)
                    # os.remove(file_path+'/'+str(file_))


path = '/Volumes/Cisco/Fall2021/Devops/Final-project/Docker/Downloads/tensorflow/tensorflow:0.10.0-gpu/test'

print(ROOT_DIR)

'''with open(path + '/manifest.json') as f:
    json_data = json.load(f)
config_digest = str(json_data['config']['digest']).split(':')[1]
print ('Config digest: ', config_digest)
for file_ in os.listdir(path):
    if not 'manifest.json' in str(file_):
        print ('   --- ', file_, len(str(file_)))
        if str(file_) == config_digest:
            print ('   this is the config digest: ', file_)'''
#remove_files_in_directory(path)