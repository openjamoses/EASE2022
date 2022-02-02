import csv
import pandas as pd
import math
import time
import random
#from src.quantum.codeanalyser.v2.TOKENS import get_tokens
import urllib.request
import json

def get_tokens():
    tokens = []
    return tokens
class GitHub:
    def __init__(self, url, ct):
        self.ct = ct
        self.url = url
    def getResponse(self):
        jsonData = None
        try:
            if self.ct == len(get_tokens()):
                self.ct = 0
            reqr = urllib.request.Request(self.url)
            reqr.add_header('Authorization', 'token %s' % get_tokens()[self.ct])
            opener = urllib.request.build_opener(urllib.request.HTTPHandler(debuglevel=1))
            content = opener.open(reqr).read()
            self.ct += 1
            jsonData = json.loads(content)
            #return jsonData, self.ct
        except Exception as e:
            #pass
            print(e, self.ct)
            #if not 'HTTP Error 403:' in str(e):
            #    jsonData = 'Error'
        return jsonData, self.ct
    def url_header(self):
        jsonData = None
        try:
            if self.ct == len(get_tokens()):
                self.ct = 0
            reqr = urllib.request.Request(self.url)
            reqr.add_header('Accept', 'application/vnd.github.mercy-preview+json')
            reqr.add_header('Authorization', 'token %s' % get_tokens()[self.ct])
            opener = urllib.request.build_opener(urllib.request.HTTPHandler(debuglevel=1))
            content = opener.open(reqr).read()
            self.ct += 1
            jsonData = json.loads(content)
            return jsonData, self.ct
        except Exception as e:
            pass
            #print(e)
        return jsonData, self.ct

class GitHubMeta:
    def __init__(self, repo, ct):
        self.ct = ct
        self.repo = repo
    def repos_contrib_counts_(self):
        p = 1
        total_contrib = 0
        while True:
            url2 = 'https://api.github.com/repos/'+self.repo+'/contributors?page='+str(p)+'&per_page=100'
            contrib_arrays, self.ct = GitHub(url2, self.ct).getResponse()
            p += 1
            if contrib_arrays != None:
                if len(contrib_arrays) == 0:
                    break
                total_contrib += len(contrib_arrays)
            else:
                break
        return total_contrib, self.ct
    def repos_pr_counts_(self):
        p = 1
        total_contrib = 0
        while True:
            url2 = 'https://api.github.com/repos/'+self.repo+'/pulls?state=all&page='+str(p)+'&per_page=100&'
            contrib_arrays, self.ct = GitHub(url2, self.ct).getResponse()
            p += 1
            if contrib_arrays != None:
                if len(contrib_arrays) == 0:
                    break
                total_contrib += len(contrib_arrays)
                if total_contrib % 500 == 0:
                    print(' ---- pr: ', total_contrib)
            else:
                break
        return total_contrib, self.ct
    def repos_issues_counts_(self):
        p = 1
        total_contrib = 0
        while True:
            url2 = 'https://api.github.com/repos/'+self.repo+'/issues?state=all&page='+str(p)+'&per_page=100'
            contrib_arrays, self.ct = GitHub(url2, self.ct).getResponse()
            p += 1
            if contrib_arrays != None:
                if len(contrib_arrays) == 0:
                    break
                total_contrib += len(contrib_arrays)
                if total_contrib%500 == 0:
                    print(' ---- issues: ', total_contrib)
            else:
                break
        return total_contrib, self.ct
    def repos_commits_counts_(self):
        p = 1
        total_contrib = 0
        while True:
            url2 = 'https://api.github.com/repos/'+self.repo+'/commits?page='+str(p)+'&per_page=100'
            contrib_arrays, self.ct = GitHub(url2, self.ct).getResponse()
            p += 1
            if contrib_arrays != None:
                if len(contrib_arrays) == 0:
                    break
                total_contrib += len(contrib_arrays)
                if total_contrib%500 == 0:
                    print(' ---- commits: ', total_contrib)
            else:
                break
        return total_contrib, self.ct
    def repos_releases_counts_(self):
        p = 1
        total_contrib = 0
        while True:
            url2 = 'https://api.github.com/repos/'+self.repo+'/releases?page='+str(p)+'&per_page=100'
            contrib_arrays, self.ct = GitHub(url2, self.ct).getResponse()
            p += 1
            if contrib_arrays != None:
                if len(contrib_arrays) == 0:
                    break
                total_contrib += len(contrib_arrays)
                if total_contrib%500 == 0:
                    print(' ---- releases: ', total_contrib)
            else:
                break
        return total_contrib, self.ct

def __generate_search_query(topic, ct, list_url, stars_from=0, stars_to = None, expected_stars=None, cm_stars=0, list_searches_used=[]):
    #print(' -- Just called the recursion with: stars_from:{}, stars_to:{}, expected_stars:{}, cm_stars:{}'.format(stars_from, stars_to, expected_stars, cm_stars))
    flag_ = 0
    if stars_from != None and stars_to == None:
        stars = ':>={}'.format(stars_from)
        flag_ = 1
    else:
        if str(stars_from) + '/' + str(stars_to) in list_searches_used:
            stars_to += 1
        list_searches_used.append(str(stars_from)+'/'+str(stars_to))
        stars = ':{}..{}'.format(stars_from, stars_to)
        flag_ = 3
    url = 'https://api.github.com/search/repositories?q=' + topic + '+stars' + stars + '+forks:>=10+fork:false&sort=forks&order=desc'
    #url = 'https://api.github.com/search/code?q=' + config + '+in:file+stars'+stars+'+language:python+extension:py'

    # url = 'https://api.github.com/search/repositories?q=' + config + '+stars'+stars+'+forks:>=50+fork:false&sort=forks&order=desc'
    #print(url)
    data, ct = GitHub(url, ct).getResponse()

    if data != None:
        if data['total_count'] >= 700 and data['total_count'] <= 1000:
            list_url.append(url)
            cm_stars += data['total_count']
            #if cm_stars >= expected_stars:
            #    list_url.append(url)
            #elif cm_stars < expected_stars:
            #    list_url.append(url)
            #
            print(expected_stars, cm_stars)
            if cm_stars < expected_stars:
                if expected_stars-cm_stars <= 1000:
                    stars_from = stars_to+1
                    stars_to = None
                elif expected_stars-cm_stars > 1000 and expected_stars-cm_stars <= 5000:
                    stars_from = stars_to+1
                    stars_to += 50
                elif expected_stars - cm_stars > 5000:
                    stars_from = stars_to+1
                    stars_to += 20
                #print('Recursive with ', stars_from, stars_to)
                __generate_search_query(topic, ct, list_url=list_url, stars_from=stars_from, stars_to=stars_to,
                                            expected_stars=expected_stars,
                                            cm_stars=cm_stars,list_searches_used=list_searches_used)


        elif data['total_count'] < 700 and (cm_stars+data['total_count']) < expected_stars:
            #print("Looping in: ", expected_stars, cm_stars)
            if stars_to == None:
                stars_to = stars_from + 100
            else:
                #stars_to += round((stars_to + stars_from) / 2)
                if str(stars_from) + '/' + str(stars_to) in list_searches_used:
                    stars_to += random.randint(stars_from, stars_to)
                else:
                    stars_to += round((stars_to + stars_from) / 2)
            #stars_to += 100
            #print("Recursion less: ", stars_from, stars_to)
            __generate_search_query(topic, ct, list_url=list_url, stars_from=stars_from, stars_to=stars_to,
                                    expected_stars=expected_stars,
                                    cm_stars=cm_stars,list_searches_used=list_searches_used)
        elif data['total_count'] < 700 and (cm_stars+data['total_count']) >= expected_stars:
            #print("Looping out: ",expected_stars, cm_stars+data['total_count'])
            list_url.append(url)

        else:
            if flag_ == 1:
                if data['total_count'] >= 2000:
                    step_stars = 200

                else:
                    step_stars = 250
                stars_to = step_stars
                __generate_search_query(topic, ct, list_url=list_url, stars_from=stars_from, stars_to=stars_to,
                                        expected_stars=expected_stars,
                                        cm_stars=cm_stars,list_searches_used=list_searches_used)
            elif flag_ == 3:
                if str(stars_from) + '/' + str(stars_to) in list_searches_used:
                    stars_to = random.randint(stars_from, stars_to)
                else:
                    stars_to = round((stars_to + stars_from) / 2)
                #print("recusion greater: ", stars_from, stars_to)
                __generate_search_query(topic, ct, list_url=list_url, stars_from=stars_from, stars_to=stars_to,
                                        expected_stars=expected_stars,
                                        cm_stars=cm_stars,list_searches_used=list_searches_used)
    else:
        time.sleep(10)
        __generate_search_query(topic, ct, list_url=list_url, stars_from=stars_from, stars_to=stars_to,
                                expected_stars=expected_stars,
                                cm_stars=cm_stars,list_searches_used=list_searches_used)

def get_data(url, ct):
    while True:
        data, ct = GitHub(url, ct).getResponse()
        if data != None:
            break
        time.sleep(15)
    return data, ct
def main():
    path_output = '/Volumes/Cisco/Fall2021/Devops/Final-project/GitHub/Repositories/'
    data_file = open(path_output + 'Repos_ml_docker_metrics-final-v44.csv', mode='w', newline='',
                                  encoding='utf-8')
    data_writer = csv.writer(data_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    data_writer.writerow(['Repos', 'topic', 'commits', 'contributors', 'issues','pulls', 'releases','size','stars','forks','open_issues','archived','created_at', 'updated_at','docker_files_count', 'file_names', 'file_paths','language','homepage', 'description'])

    proj_list = []
    suggested_topics = [#'tensorflow','torch', 'serving','cnn','mlflow','mlops', 'rnn','keras','mxnet', 'cntk','sklearn',  'machine-learning', 'deep-learning', 'reinforcement-learning',  'artificial-intelligence', 'computer-vision', 'image-processing','neural-network', 'image-classification', 'convolutional-neural-networks', 'object-detection',
           'machine-intelligence', 'deep-neural-network', 'docker ml']

    data_df = pd.read_csv(path_output + 'Repos_ml_docker_metrics-final-v3.csv')
    Repos = data_df.Repos.values.tolist()
    for repo in Repos:
        proj_list.append(repo)
    total_expected_everything = 0
    #for word in suggested_topics:
    #url = 'https://api.github.com/search/topics?q='+word
    ct = 0
    #github = GitHub(url, ct)
    #json_data, ct = github.url_header()  # gitHub.readUrl(get_tokens()[0])
    #if json_data != None:
    #    print(word,json_data['total_count'])
    for topic in suggested_topics: #json_data['items']:
        #topic = obj_['name']
        counts = 0
        count_selected = 0
        #url3 = 'https://api.github.com/search/code?q=filename:docker+filename:Dockerfile'

        url2 = 'https://api.github.com/search/repositories?q=' + topic + '+stars:>=2+forks:>=10+fork:false&sort=forks&order=desc'

        print(url2)
        data, ct = get_data(url2, ct) #GitHub(url2, ct).getResponse()
        list_url = []
        if data != None:
            print(topic, ' total repos:', data['total_count'])
            total_expected_everything += data['total_count']
            if data['total_count'] <= 1000:
                list_url.append(url2)
            else:
                __generate_search_query(topic, ct, list_url=list_url, stars_from=2, stars_to=None,
                                        expected_stars=data['total_count'], cm_stars=0)
        print("Total urls: {}".format(len(list_url)), list_url)
        for url_ in list_url:
            print(url_)

            unique_list = []
            pages_ = 1
            x_flag = 0
            while True:
                url = url_+'&page={}&per_page=100'.format(pages_)
                #print(url2)
                data, ct = get_data(url, ct)
                #data, ct = GitHub(url2, ct).getResponse()
                if data != None:
                    if len(data['items']) == 0:
                        x_flag = 1
                        print("breaking here!!")
                        break
                    print("         ---- Page {}, total items: {}".format(pages_, len(data['items'])))
                    for obj in data['items']:
                        counts += 1
                        flag = 0
                        #for ignore_ in list_ignore:
                        #    if  ignore_ in str(obj['full_name']).lower() or  ignore_ in str(obj['description']).lower():
                        #        flag += 1
                        #if flag == 0:
                        #print('         ------- ', '{}/{}'.format(counts,count_selected) , obj['full_name'] )
                        if not obj['full_name'] in proj_list:
                            '''if obj['full_name'] in dict_repos_topics.keys():
                                val_ = dict_repos_topics.get(obj['full_name'])
                                val_.append(topic)
                                dict_repos_topics[obj['full_name']] = val_
                            else:
                                dict_repos_topics[obj['full_name']] = [topic]'''

                            count_selected += 1

                            ## Search for docker files here!!!
                            total_count = 0
                            docker_flag = 0
                            names_str = ''
                            paths_str = ''
                            url3 = 'https://api.github.com/search/code?q=filename:docker+filename:Dockerfile+repo:{}'.format(obj['full_name'])
                            data_docker, ct = get_data(url3, ct) #GitHub(url3, ct).getResponse()
                            if data_docker != None:
                                total_count = data_docker['total_count']
                                if total_count > 0:
                                    docker_flag = 1
                                for item_obj in data_docker['items']:
                                    name = item_obj['name']
                                    path = item_obj['path']
                                    names_str += name+'; '
                                    paths_str += path+'; '
                            if total_count > 0:
                                proj_list.append(obj['full_name'])
                                unique_list.append(obj['full_name'])
                                issues, ct = GitHubMeta(obj['full_name'], ct).repos_issues_counts_()
                                pr, ct = GitHubMeta(obj['full_name'], ct).repos_pr_counts_()
                                contrib, ct = GitHubMeta(obj['full_name'], ct).repos_contrib_counts_()
                                release, ct = GitHubMeta(obj['full_name'], ct).repos_releases_counts_()
                                commits, ct = GitHubMeta(obj['full_name'], ct).repos_commits_counts_()
                                data_writer.writerow(
                                    [obj['full_name'], topic, commits, contrib, issues, pr, release, obj['size'],
                                     obj['stargazers_count'], obj['forks'], obj['open_issues'], obj['archived'], obj['created_at'], obj['updated_at'], total_count,names_str, paths_str, obj['language'],
                                     obj['homepage'], obj['description']])
                pages_ += 1
                print('      ----- We are on page: ', pages_, ' now!')
                time.sleep(5)
                if pages_ == 11:
                    break
            print("      ----- Summary total results: {}, total unique docker {}, unique added docker {}".format(total_expected_everything, len(proj_list), len(unique_list)))
if __name__ == '__main__':
    main()
