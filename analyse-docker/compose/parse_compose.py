from yaml import load, dump
try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper
with open("docker-compose.yml", 'r') as ymlfile:
    data = load(ymlfile, Loader=Loader)
    #docker_config = yaml.load(ymlfile)
    for key, val in data.items():
        print(key, val)
    print('******\n')
    for key, val in data['services'].items():
        print(key, val)
#print(data)