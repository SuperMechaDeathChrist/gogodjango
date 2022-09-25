dbpath='db_yt_channels.dat'
import pickle
from github import Github
import unicodedata
from difflib import get_close_matches, ndiff
from difflib import SequenceMatcher
import os
import time
from datetime import datetime




def strip_accents(s):
   return ''.join(c for c in unicodedata.normalize('NFD', s)
                  if unicodedata.category(c) != 'Mn')
# globals()['CaseInsensitiveDict']=None
class CaseInsensitiveDict(dict):

    @classmethod
    def _k(cls, key):
        return key.lower() if isinstance(key, str) else key

    def __init__(self, *args, **kwargs):
        super(CaseInsensitiveDict, self).__init__(*args, **kwargs)
        self._convert_keys()

    def __getitem__(self, key):
        return super(CaseInsensitiveDict, self).__getitem__(self.__class__._k(key))

    def __setitem__(self, key, value):
        super(CaseInsensitiveDict, self).__setitem__(
            self.__class__._k(key), value)

    def __delitem__(self, key):
        return super(CaseInsensitiveDict, self).__delitem__(self.__class__._k(key))

    def __contains__(self, key):
        return super(CaseInsensitiveDict, self).__contains__(self.__class__._k(key))

    def has_key(self, key):
        return super(CaseInsensitiveDict, self).has_key(self.__class__._k(key))

    def pop(self, key, *args, **kwargs):
        return super(CaseInsensitiveDict, self).pop(self.__class__._k(key), *args, **kwargs)

    def get(self, key, *args, **kwargs):
        return super(CaseInsensitiveDict, self).get(self.__class__._k(key), *args, **kwargs)

    def setdefault(self, key, *args, **kwargs):
        return super(CaseInsensitiveDict, self).setdefault(self.__class__._k(key), *args, **kwargs)

    def update(self, E={}, **F):
        super(CaseInsensitiveDict, self).update(self.__class__(E))
        super(CaseInsensitiveDict, self).update(self.__class__(**F))

    def _convert_keys(self):
        for k in list(self.keys()):
            v = super(CaseInsensitiveDict, self).pop(k)
            self.__setitem__(k, v)

# global CaseInsensitiveDict

def load():
    return pickle.load(open(dbpath,'rb'))

def github_download(token,repo,do_save=True):
    g = Github(token)
    try:
        repo = g.get_repo(repo)
    except:
        return
    contents = repo.get_contents(dbpath)
    s=contents.decoded_content
    dbo=pickle.loads(s)
    dbo['']['sha']=contents.sha
    if do_save:
        save(dbo)
    return dbo
def github_get_sha(token,repo):
    try:
        return load()['']['sha']
    except:
        g = Github(token)
        try:
            repo = g.get_repo(repo)
        except:
            return ''
        contents = repo.get_contents(dbpath)
        return contents.sha

def github_save(dbo,token,repo):
    dbo['']['saved']=time.time()
    g = Github(token)
    try:
        repo = g.get_repo(repo)
    except:
        repo=None

    try:
        ans=repo.update_file(dbpath,str(datetime.now()),pickle.dumps(dbo),github_get_sha(token,repo))
    except:
        try:
            ans=repo.create_file(dbpath, str(datetime.now()), pickle.dumps(dbo))
        except:
            contents = repo.get_contents(dbpath)
            ans=repo.update_file(dbpath,str(datetime.now()),pickle.dumps(dbo),contents.sha)
    dbo['']['sha']=ans['commit'].sha
    save(dbo)
def github_add(key,value,token,repo):
    dbo=github_download(token,repo,do_save=False)
    dbo.pop(key,None)
    dbo[key]=value
    # dbo['']['edited']=time.time()
    # save(dbo)
    github_save(dbo,token,repo)

def github_remove(key,token,repo):
    dbo=github_download(token,repo,do_save=False)
    try:
        dbo.pop(key)
        github_save(dbo,token,repo)
        return dbo
    except:
        return None

def printdb(exclude=()):

    dbo=load()
    print('+'*20)
    print('{')
    for key in dbo:
        # print('-'*20)
        if exclude:
            if type(exclude)==str:
                exclude=exclude.split()
            for e in exclude:
                # del dbo[key][e]
                if e in dbo[key]:
                    dbo[key].pop(e,None)
                pass
        print('-'*20)
        print('>>',key,':',dbo[key])
    print('}')
    print('+'*20)

def save(dbo):
    # dbo=load()
    # dbo['']['saved']=time.time()
    pickle.dump(dbo,open(dbpath,'wb'))

def add(key,value):
    dbo=load()
    dbo.pop(key,None)
    dbo[key]=value
    # dbo['']['edited']=time.time()
    save(dbo)

def remove(key):
    dbo=load()
    try:
        dbo.pop(key)
        save(dbo)
        return dbo
    except:
        return None
def isin(key,strip_accent=False):
    if strip_accents:
        key=strip_accents(key)
    return bool(key in load())

def wipe():
    dbo=CaseInsensitiveDict()
    dbo['']={'edited':time.time(),'saved':time.time()}
    save(dbo)

def _reset_time_meta_():
    dbo=load()
    dbo['']={'edited':time.time(),'saved':time.time()}
    save(dbo)    

# # printdb()
# add('hell',[-1,2,3])
# printdb()
# # remove('hell')
# wipe()
# printdb()
# print(isin('Héll'))

# an=pickle.load(open('home.dat','rb'))
# for a in an['Recent Releases']:
#   # print(a['title'],a['source'])
#   add(a['title'],a['source'])

# printdb()
# wipe()
def search(s):
    dbo=load()
    dx_max=-1
    closest=''
    for a in dbo:
        dx=SequenceMatcher(None,s,a).ratio()
        # errors=[li for li in ndiff(s, a) if li[0] != ' ']
        # ne=len(errors)
        # print(a,dx)
        if dx>dx_max:
            closest=a
            dx_max=dx
        if dx==1:
            break

    # print('x'*20)
    # print(closest)
    return closest,dbo[closest]

if not os.path.exists(dbpath):
    wipe()