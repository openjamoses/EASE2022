import time
import random
#from src.quantum.codeanalyser.v2.TOKENS import get_tokens
import urllib.request
import json

def get_tokens():
    tokens = ["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",
              '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',
              #'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',
              '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']
    return tokens
class GitHub:
    def __init__(self, url, ct):
        self.ct = ct
        self.url = url
    def getResponse(self):
        jsonData = None
        code = 200
        try:
            if self.ct == len(get_tokens()):
                self.ct = 0
            reqr = urllib.request.Request(self.url)
            reqr.add_header('Authorization', 'token %s' % get_tokens()[self.ct])
            opener = urllib.request.build_opener(urllib.request.HTTPHandler(debuglevel=1))
            content = opener.open(reqr).read()
            self.ct += 1
            #print(content)
            jsonData = json.loads(content)
            #return jsonData, self.ct
        except Exception as e:
            #pass
            print(e, self.ct)
            if not 'HTTP Error 403:' in str(e):
                code = 404
        return jsonData, code, self.ct
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
def get_data(url, ct):
    while True:
        data, code, ct = GitHub(url, ct).getResponse()
        if data != None:
            break
        if code == 404:
            break
        time.sleep(15)
    return data, ct
class GitHubMeta:
    def __init__(self, repo, ct):
        self.ct = ct
        self.repo = repo
    def repos_contrib_counts_(self):
        p = 1
        total_contrib = 0
        while True:
            url2 = 'https://api.github.com/repos/'+self.repo+'/contributors?page='+str(p)+'&per_page=100'
            contrib_arrays, self.ct = get_data(url2, self.ct) #GitHub(url2, self.ct).getResponse()
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
            contrib_arrays, self.ct = get_data(url2, self.ct) #GitHub(url2, self.ct).getResponse()
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
            contrib_arrays, self.ct = get_data(url2, self.ct) #GitHub(url2, self.ct).getResponse()
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
            contrib_arrays, self.ct = get_data(url2, self.ct) #GitHub(url2, self.ct).getResponse()
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
            contrib_arrays, self.ct = get_data(url2, self.ct) #GitHub(url2, self.ct).getResponse()
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