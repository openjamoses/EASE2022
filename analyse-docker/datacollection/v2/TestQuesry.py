#from src.thesis.forough.docker.GitHub.ReturnSearchQuery import GitHub
import json
import urllib.request
import pprint


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
            print(get_tokens()[self.ct])
            reqr = urllib.request.Request(self.url)
            reqr.add_header('Authorization', 'token %s' % get_tokens()[self.ct])
            opener = urllib.request.build_opener(urllib.request.HTTPHandler(debuglevel=1))
            status_ = opener.open(reqr).getcode()
            print('request status: ', status_)
            content = opener.open(reqr).read()

            self.ct += 1
            jsonData = json.loads(content)
            #return jsonData, self.ct
        except Exception as e:
            if 'HTTP Error 404' in str(e):
                #print('yes I got the error: ', e)
                jsonData = 404
            #pass
            print(e, self.url, self.ct, )
            #self.ct += 1
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
# +extension:py+extension:ipynb %2B
#+in:file+extension:py+extension:ipynb
#url = 'https://api.github.com/repos/google/automl'
url2 = 'https://api.github.com/search/code?q=filename:docker+filename:Dockerfile'
counts = 0
count_selected = 0
#print(url2)
ct = 0
data, ct = GitHub(url2, ct).getResponse()
list_url = []
if data != None:
    #print(' total repos:', data['total_count'])
    print(data)
