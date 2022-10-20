import sys
sys.path.append('../')
from django.shortcuts import render,redirect
from django.urls import reverse
# import requests as rq
import requests
requests.packages.urllib3.util.connection.HAS_IPV6 = False
rq=requests.Session()
rq.headers.update({'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_2) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1309.0 Safari/537.17'})


import threading
from vtt_to_srt import str_vtt_to_srt
# Create your views here.
from django.http import HttpResponse, JsonResponse
import json
import re
import time
import random
import unicodedata
import rklpy_lib as rk
import traceback
import youtube_dl

from api.settings import last_query,series_ep_cache,last_watched_cache
from bs4 import BeautifulSoup
from xml.dom import minidom
import pytube
# import imdb
# ia = imdb.Cinemagoer()
import db
import db_flixhq
import db_query
import db_history
import db_yt_queue
import db_flixhq_all
import db_flixhq_home
from db import CaseInsensitiveDict

apiurl='https://gogo4rokuapi.herokuapp.com'
#apiconsu='https://rokuconsumet.herokuapp.com'
# apiconsu='https://consumet-api.herokuapp.com'
apiconsu='https://api.consumet.org'


from cryptography.fernet import Fernet
key=b'wnuSKeQm1WLsf0qtmWVyoknqEhvrNXqj1RKewiwJFDE='
encMessage=b'gAAAAABi7tt3uuCl4P2d_m1JpvKUZuTBK7SMGuJqlJVRTIhsFhUFjLCe_kf2veI7iWNuEZpT2jCYhJE7MBhV990S4fu4iS81zpb29e41MAleVgIdZT6xSe5y6kcfTzkM_MW81n9cU08O'
fernet = Fernet(key)
gittoken = fernet.decrypt(encMessage).decode()

gitrepo="SuperMechaDeathChrist/gogodjango"
#

# last_query=db_query.github_download(gittoken,gitrepo)


def pathargs(**d):
    ans='?'
    for k in d:
        ans+=k+'='+requests.utils.quote(d[k],safe='')+'&'
    return ans.strip('&')

def addto(root,parent,element,value=None,attr=''):
    el=root.createElement(element)
    if not attr:
        if value:
            el.appendChild(root.createTextNode(value))
    else:
        if type(attr)==str:
            el.setAttribute(attr,value)
        elif type(attr)==dict:
            for k in attr:
                if k=='text':
                    el.appendChild(root.createTextNode(attr[k]))
                else:
                    el.setAttribute(k,attr[k])
                # print(k,attr[k])
    parent.appendChild(el)
    return el

def randstr(n=6,s='QWERTYUIOPASDFGHJKLZXCVBNM'):
    ans=''
    ls=len(s)-1
    for c in range(n):
        ans+=s[random.randint(0,ls)]
    return ans

def strip_accents(s):
   return ''.join(c for c in unicodedata.normalize('NFD', s)
                  if unicodedata.category(c) != 'Mn')

def fill_movie(title='Title',thumbnail="https://www.fdd.cl/wp-content/uploads/2017/09/Test.jpg",
    url='http://commondatastorage.googleapis.com/gtv-videos-bucket/sample/BigBuckBunny.mp4',
    videoType='MP4',
    quality="HD",
    shortDescription="Short description.",
    id=randstr(),
    genres=["NA"],
    tags=["anime"],

    ):
    v=locals()
    v.pop('url',None)
    v.pop('quality',None)
    v.pop('videoType',None)
    v['content']={
    'captions':[],
    'videos':[dict(url=url,quality=quality,videoType=videoType)]
    }
    
    v['title']=rk.titlexml(title)
    return v

def fill_series(title='Title',thumbnail="https://www.fdd.cl/wp-content/uploads/2017/09/Test.jpg",
    base_url='',
    videoType='MP4',
    quality="HD",
    shortDescription="Short description.",
    id=randstr(),
    genres=["NA"],
    tags=["anime"],
    totalEpisodes=0
    ):
    v=locals()
    v.pop('base_url',None)
    v.pop('quality',None)
    v.pop('videoType',None)
    v['title']=rk.titlexml(title)
    v['shortDescription']=rk.xmltext(shortDescription)
    # v['content']={
    # 'captions':[],
    # 'videos':[dict(url=url,quality=quality,videoType=videoType)]
    # }
    v['seasons']=[{"seasonNumber":1,
                        "episodes":[]}]
    for i in range(1,int(totalEpisodes)+1):
        e={
        'id':v['id']+'-episode-'+str(i),
        'title':'Episode '+str(i),
        "episodeNumber":i,
        'shortDescription':'---',
        'thumbnail':thumbnail,
        'content':{
        'captions':[],
        'videos':[dict(url=base_url+'-episode-'+str(i),quality=quality,videoType=videoType)]
        }

        }
        v['seasons'][0]['episodes'].append(e)
    return v
def fill_anime(a,id=randstr(),base_url='',videoType='MP4'):
    '''
{'animeTitle': 'Accel World (Dub)', 
'type': 'TV Series', 'releasedDate': '2012', 'status': 'Completed', 
'genres': ['Action', 'Game', 'Romance', 'School', 'Sci-Fi', 'Shounen'], 
'otherNames': 'Accelerated World, アクセル・ワールド', 
'synopsis': 'The year is 2046. Haruyuki Arita is a young boy who finds himself on the lowest social rungs of his school. Ashamed of his miserable life, Haruyuki can only cope by indulging in virtual games. But that all changes when Kuroyukihime, the most popular girl in school, introduces him to a mysterious program called Brain Burst and a virtual reality called the Accel World.', 
'animeImg': 'https://gogocdn.net/cover/accel-world-dub.jpg', 
'totalEpisodes': '24', 
'episodesList': [
    {'episodeId': 'accel-world-dub-episode-24', 'episodeNum': '24', 'episodeUrl': 'https://gogoanime.film//accel-world-dub-episode-24'}, 
    {'episodeId': 'accel-world-dub-episode-23', 'episodeNum': '23', 'episodeUrl': 'https://gogoanime.film//accel-world-dub-episode-23'}, {'episodeId': 'accel-world-dub-episode-22', 'episodeNum': '22', 'episodeUrl': 'https://gogoanime.film//accel-world-dub-episode-22'}, {'episodeId': 'accel-world-dub-episode-21', 'episodeNum': '21', 'episodeUrl': 'https://gogoanime.film//accel-world-dub-episode-21'}, {'episodeId': 'accel-world-dub-episode-20', 'episodeNum': '20', 'episodeUrl': 'https://gogoanime.film//accel-world-dub-episode-20'}, {'episodeId': 'accel-world-dub-episode-19', 'episodeNum': '19', 'episodeUrl': 'https://gogoanime.film//accel-world-dub-episode-19'}, {'episodeId': 'accel-world-dub-episode-18', 'episodeNum': '18', 'episodeUrl': 'https://gogoanime.film//accel-world-dub-episode-18'}, {'episodeId': 'accel-world-dub-episode-17', 'episodeNum': '17', 'episodeUrl': 'https://gogoanime.film//accel-world-dub-episode-17'}, {'episodeId': 'accel-world-dub-episode-16', 'episodeNum': '16', 'episodeUrl': 'https://gogoanime.film//accel-world-dub-episode-16'}, {'episodeId': 'accel-world-dub-episode-15', 'episodeNum': '15', 'episodeUrl': 'https://gogoanime.film//accel-world-dub-episode-15'}, {'episodeId': 'accel-world-dub-episode-14', 'episodeNum': '14', 'episodeUrl': 'https://gogoanime.film//accel-world-dub-episode-14'}, {'episodeId': 'accel-world-dub-episode-13', 'episodeNum': '13', 'episodeUrl': 'https://gogoanime.film//accel-world-dub-episode-13'}, {'episodeId': 'accel-world-dub-episode-12', 'episodeNum': '12', 'episodeUrl': 'https://gogoanime.film//accel-world-dub-episode-12'}, {'episodeId': 'accel-world-dub-episode-11', 'episodeNum': '11', 'episodeUrl': 'https://gogoanime.film//accel-world-dub-episode-11'}, {'episodeId': 'accel-world-dub-episode-10', 'episodeNum': '10', 'episodeUrl': 'https://gogoanime.film//accel-world-dub-episode-10'}, {'episodeId': 'accel-world-dub-episode-9', 'episodeNum': '9', 'episodeUrl': 'https://gogoanime.film//accel-world-dub-episode-9'}, {'episodeId': 'accel-world-dub-episode-8', 'episodeNum': '8', 'episodeUrl': 'https://gogoanime.film//accel-world-dub-episode-8'}, {'episodeId': 'accel-world-dub-episode-7', 'episodeNum': '7', 'episodeUrl': 'https://gogoanime.film//accel-world-dub-episode-7'}, {'episodeId': 'accel-world-dub-episode-6', 'episodeNum': '6', 'episodeUrl': 'https://gogoanime.film//accel-world-dub-episode-6'}, {'episodeId': 'accel-world-dub-episode-5', 'episodeNum': '5', 'episodeUrl': 'https://gogoanime.film//accel-world-dub-episode-5'}, {'episodeId': 'accel-world-dub-episode-4', 'episodeNum': '4', 'episodeUrl': 'https://gogoanime.film//accel-world-dub-episode-4'}, {'episodeId': 'accel-world-dub-episode-3', 'episodeNum': '3', 'episodeUrl': 'https://gogoanime.film//accel-world-dub-episode-3'}, {'episodeId': 'accel-world-dub-episode-2', 'episodeNum': '2', 'episodeUrl': 'https://gogoanime.film//accel-world-dub-episode-2'}, {'episodeId': 'accel-world-dub-episode-1', 'episodeNum': '1', 'episodeUrl': 'https://gogoanime.film//accel-world-dub-episode-1'}]}
    '''
    ans=dict(
        title=a['animeTitle'],
        id=id,
        thumbnail=a['animeImg'],
        shortDescription=a['synopsis'],
        genres=[['SUB','DUB'][bool(id[-3:]=='dub')]],
        tags=["series"],
        seasons=[{"seasonNumber":1,'episodes':[]}]
        )
    for e in reversed(a['episodesList']):
        ans['seasons'][0]['episodes'].append({
            'id':e['episodeId'],
            'title':'Episode '+e['episodeNum'],
            'episodeNumber':e['episodeNum'],
            'shortDescription':'',
            'thumbnail':a['animeImg'],
            'content':{
            'captions':[],
            'videos':[
                {
                'quality':'HD',
                'videoType':videoType,
                'url':base_url+e['episodeId']
                }
            ]
            }
            })

    return ans

def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")
  
def _down_query_response(curl,aid,dbid):
    global last_query
    # last_query=db_query.github_download(gittoken,)
    #
    try:
        # curl=apiconsu+'/movies/flixhq/info'+pathargs(id=aid)
        # print(curl)
        r=rq.get(curl)
        a=r.json()
        last_query[dbid][aid]=dict(response=a)
        print(curl)
    except:
        traceback.print_exc()

def search_fav_series(request):
    sort='False'
    view='all'
    if request.method == 'GET': # If the form is submitted
        ts=[]
        st=[]
        cs=[]
        fs=[]
        nfs=[]
        lens=[]
        # streams=[]
        aids=db_flixhq.load()
        sort=request.GET.get('sort', None)
        sort='False' if not sort else sort
        
        view=request.GET.get('view', None)
        view='all' if not view else view

        if sort=='False':
            do=aids
        else:
            do=sorted(aids)
        for aid in do:
            if aid:
                if view=='series' and aid[0:2]!='tv':
                    continue
                elif view=='movies' and aid[0:2]=='tv':
                    continue

                qi=aids[aid]['response']
                # print(aid,qi)
                ts.append(qi['title'])
                st.append('['+qi['releaseDate']+']')
                cs.append(qi['image'])
                fs.append('../addto_fav/'+qi['id'])
                nfs.append('../removefrom_fav/'+qi['id'])
                lens.append('')
                # streams.append('../get_ep_flixhq/'+qi['id'])

                # last_query['animes'][qi['id']]=False
                # threading.Thread(target=_down_query_response,args=(
                #     apiurl+'/anime-details/'+qi['id'],
                #     qi['id'],
                #     'animes',
                #     )).start()
    context ={
        'smode':'Fav Series',
        'sort':sort,
        'view':view,
        'list':zip(ts,st,cs,fs,nfs,lens),
    }
    return render(request, "favs.html",context)
def view(request):
    dj=request.build_absolute_uri().replace(request.path,'').split('?')[0]
    if request.method == 'GET': # If the form is submitted
        f=request.GET.get('f', r"")
        aid=f.split('addto_fav/')[-1]
        if 'tv/' or 'movie/' in aid:
            try:
                dbo=db_flixhq.load()
                a=dbo[aid]['response']
            except:
                r=rq.get(apiconsu+'/movies/flixhq/info'+pathargs(id=aid))
                a=r.json()
            base_url=dj+'/polls/get_flixhq_ep/'
            title=a['title']
            cover=a['image']
            epstream=[]
            eptit=[]
            if 'tv/' == aid[:3]:
                for e in a['episodes']:
                    url_args=pathargs(eid=e['id'],aid=aid)
                    epstream.append(base_url+url_args)
                    eptit.append('S'+str(e['season']).rjust(2,'0')+e['title'])
                    # addto(root,season,'episode',attr=dict(
                    # title='S'+str(e['season']).rjust(2,'0')+e['title'],
                    # url=base_url+url_args,
                    # subs=dj+'/polls/get_flixhq_sub/'+url_args
                    # ))
            else:
                e=a['episodes'][0]
                url_args=pathargs(eid=e['id'],aid=aid)
                
                # url_args=pathargs(episodeId=e['id'],server='vidcloud',mediaId=aid)
                # er=rq.get(apiconsu+'/movies/flixhq/watch'+url_args)
                # erj=er.json()
                # stream_url=erj['sources'][0]['url']
                # epstream.append(stream_url)

                epstream.append(base_url+url_args)
                
                
                eptit.append(a['title'])
    context={'title':title,'cover':cover,'episodes':zip(epstream,eptit),'eplen':len(eptit)}
    return render(request,'view.html',context)
def search_fav_anime(request):
    sort='False'
    view=None
    if request.method == 'GET': # If the form is submitted
        ts=[]
        st=[]
        cs=[]
        fs=[]
        nfs=[]
        lens=[]
        aids=db.load()
        sort=request.GET.get('sort', None)
        sort='False' if not sort else sort
        
        view=request.GET.get('view', None)
        view='all' if not view else view

        if sort=='False':
            do=aids
        else:
            do=sorted(aids)
        for aid in do:
            if aid:
                # if view=='series' and aid[0:2]!='tv':
                #     continue
                # elif view=='movies' and aid[0:2]=='tv':
                #     continue

                qi=aids[aid]['response']
                # print(qi)
                if view=='all':
                    ts.append(qi['animeTitle'])
                    st.append('['+qi['status']+']')
                    cs.append(qi['animeImg'])
                    fs.append('../addto_fav/'+aid)
                    nfs.append('../removefrom_fav/'+aid)
                elif view=='Dub':
                    if not '(Dub)' in qi['animeTitle']:
                        continue
                    ts.append(qi['animeTitle'])
                    st.append('['+qi['status']+']')
                    cs.append(qi['animeImg'])
                    fs.append('../addto_fav/'+aid)
                    nfs.append('../removefrom_fav/'+aid)
                elif view=='Sub':
                    if '(Dub)' in qi['animeTitle']:
                        continue
                    ts.append(qi['animeTitle'])
                    st.append('['+qi['status']+']')
                    cs.append(qi['animeImg'])
                    fs.append('../addto_fav/'+aid)
                    nfs.append('../removefrom_fav/'+aid)
                lens.append('')
                # ts.append(qi['title'])
                # st.append('['+qi['releaseDate']+']')
                # cs.append(qi['image'])
                # fs.append('../addto_fav/'+qi['id'])
                # nfs.append('../removefrom_fav/'+qi['id'])

                # last_query['animes'][qi['id']]=False
                # threading.Thread(target=_down_query_response,args=(
                #     apiurl+'/anime-details/'+qi['id'],
                #     qi['id'],
                #     'animes',
                #     )).start()
    context ={
        'smode':'Fav Anime',
        'sort':sort,
        'view':view,
        'list':zip(ts,st,cs,fs,nfs,lens),
    }
    return render(request, "favs.html",context)

def search_anime(request):
    global last_query
    # last_query=db_query.github_download(gittoken,gitrepo)
    # create a dictionary to pass
    # data to the template
    last_query['animes']={}
    search_query=''
    if request.method == 'GET': # If the form is submitted
        search_query = request.GET.get('search_box', None)
        an={}
        ts=[]
        st=[]
        cs=[]
        fs=[]
        nfs=[]
        lens=[]
        if search_query:
            print(search_query)
            # queryurl=apiurl+'/search'+pathargs(keyw=search_query)
            queryurl=apiconsu+'/anime/gogoanime/'+requests.utils.quote(search_query,safe='')
            # print(queryurl)
            q=rq.get(queryurl)
            qj=q.json()
            # dj=request.build_absolute_uri().replace(request.path,'')
            # if '?' in dj:
            #     dj=dj.split('?')[0]
            # base_url=dj+'/polls/'
            if 'results' in qj:
                for qi in qj['results']:
                    # ts.append(qi['animeTitle'])
                    # st.append('['+qi['status']+']')
                    # cs.append(qi['animeImg'])
                    # fs.append('../addto_fav/'+qi['animeId'])
                    # nfs.append('../removefrom_fav/'+qi['animeId'])
                    print(qi)

                    ts.append(qi['title'])
                    st.append('['+qi['releaseDate']+']')
                    cs.append(qi['image'])
                    fs.append('../addto_fav/'+qi['id'])
                    nfs.append('../removefrom_fav/'+qi['id'])
                    lens.append('')

                    last_query['animes'][qi['id']]=False
                    threading.Thread(target=_down_query_response,args=(
                        apiurl+'/anime-details/'+qi['id'],
                        qi['id'],
                        'animes',
                        )).start()
                threading.Thread(target=db_query.github_save,args=(last_query,gittoken,gitrepo)).start()


    context ={
        #"data":"Gfg is the best",
        'nrslts':len(ts),
        'smode':'Search Anime',
        'lastq':search_query,
        'list':zip(ts,st,cs,fs,nfs,lens),
    }

    # return response with template and context
    # return render(request, "geeks.html", context)
    # print(last_query['animes'])
    return render(request, "search.html",context)
invidious_inst=['https://invidious.snopyta.org','https://vid.puffyan.us','https://inv.riverside.rocks','https://invidious.esmailelbob.xyz','https://invidious.namazso.eu','https://yt.artemislena.eu']
def search_youtube(request):
    # global last_query
    # last_query['animes']={}
    search_query=''
    if request.method == 'GET': # If the form is submitted
        search_query = request.GET.get('search_box', None)
        an={}
        ts=[]
        st=[]
        cs=[]
        fs=[]
        nfs=[]
        lens=[]
        if search_query:
            print(search_query)
            mode=('pytube','invidious')[1]
            for i in range(5):
                try:
                    if mode=='pytube':
                        ans=pytube.Search(search_query)
                        for yv in ans.results:
                            # print(yv.video_id)
                            vid=yv.video_id
                            thumb=f'https://i.ytimg.com/vi/{vid}/hqdefault.jpg'
                            ts.append(yv.title)
                            st.append(yv.author)
                            cs.append(thumb)
                            fs.append('../addto_yt_queue/'+vid)
                            nfs.append('../removefrom_yt_queue/'+vid)
                        break
                    elif mode=='invidious':
                        
                # https://vid.puffyan.us//api/v1/search?q=ghost&fields=title,author,publishedText
                # for i in range(5):
                        inst=invidious_inst[random.randint(0,len(invidious_inst))-1]
                        url=f'{inst}/api/v1/search?q='+requests.utils.quote(search_query,safe='')+'&'+'fields=title,videoId,author,publishedText,lengthSeconds'
                        print(url)
                    # try:
                        r=rq.get(url)
                        rj=r.json()
                        for yv in rj:
                            if 'author' in yv and not 'videoId' in yv:
                                continue
                            # print(yv)
                            vid=yv['videoId']
                            thumb=f'https://i.ytimg.com/vi/{vid}/hqdefault.jpg'
                            ts.append(yv['title'])
                            st.append(yv['author']+' | '+yv['publishedText'])
                            cs.append(thumb)
                            fs.append('../addto_yt_queue/'+vid)
                            nfs.append('../removefrom_yt_queue/'+vid)
                            leni=short_h_m_s(yv['lengthSeconds'])
                            lens.append(leni)
                        break
                except:
                    mode='pytube' if mode=='invidious' else 'invidious'
                    traceback.print_exc()
                    time.sleep(1.5)

                # threading.Thread(target=db_query.github_save,args=(last_query,gittoken,gitrepo)).start()


    context ={
        'nrslts':len(ts),
        'smode':'Search YouTube',
        'lastq':search_query,
        'list':zip(ts,st,cs,fs,nfs,lens),
    }
    return render(request, "search.html",context)

def short_h_m_s(secs):
    s=time.strftime('%H:%M:%S', time.gmtime(secs))
    s=s.lstrip('0').lstrip(':').lstrip('0')
    return s if s[0]!=':' else '0'+s

def search_series(request):
    global last_query
    # create a dictionary to pass
    # data to the template
    search_query=''
    last_query['series']={}
    if request.method == 'GET': # If the form is submitted
        search_query = request.GET.get('search_box', None)
        an={}
        ts=[]
        st=[]
        cs=[]
        fs=[]
        nfs=[]
        lens=[]
        if search_query:
            print(search_query)
            # queryurl=apiurl+'/search'+pathargs(keyw=search_query)
            queryurl=apiconsu+'/movies/flixhq/'+requests.utils.quote(search_query,safe='')
            print(queryurl)
            q=rq.get(queryurl)
            qj=q.json()
            # dj=request.build_absolute_uri().replace(request.path,'')
            # if '?' in dj:
            #     dj=dj.split('?')[0]
            # base_url=dj+'/polls/'
            if 'results' in qj:
                for qi in qj['results']:
                    # an.append({'title':qi['animeTitle'],'img':qi["animeImg"]})
                    # an[qi['animeTitle']+'\n'+qi['status']]=qi["animeImg"]
                    ts.append(qi['title'])
                    if 'releaseDate' in qi:
                        st.append('['+qi['type']+' - '+qi['releaseDate']+']')
                    else:
                        st.append('['+qi['type']+']')
                    cs.append(qi['image'])
                    fs.append('../addto_fav/'+qi['id'])
                    nfs.append('../removefrom_fav/'+qi['id'])
                    lens.append('')

                    last_query['series'][qi['id']]=False
                    threading.Thread(target=_down_query_response,args=(
                        apiconsu+'/movies/flixhq/info'+pathargs(id=qi['id']),
                        qi['id'],
                        'series',
                        )).start()

                threading.Thread(target=db_query.github_save,args=(last_query,gittoken,gitrepo)).start()




    context ={
        #"data":"Gfg is the best",
        'smode':'Search Movies/TV',
        'nrslts':len(ts),
        'lastq':search_query,
        'list':zip(ts,st,cs,fs,nfs,lens),
    }
    # return response with template and context
    # return render(request, "geeks.html", context)
    return render(request, "search.html",context)    

def get_ep(request,ep):
    #http://127.0.0.1:8000/polls/get_ep/test/
    if ep =='test':
        # url='https://animepisode.com/the-rising-of-the-shield-hero-season-2-episode-11-english-dubbed/'
        # url='https://pub9.animeout.com/series/00RAPIDBOT/Eighty%20Six/[AnimeOut]%2086%20-%20Eighty%20Six%20-%2001%201080pp%20[1B13598F][1080pp][SubsPlease][RapidBot].mkv'
        # 'https://pub9.animeout.com/series/Ongoing/Eighty%20Six/[AnimeOut]%2086%20-%20Eighty%20Six%20-%2007%20720pp%20[1ED825C3][SubsPlease][RapidBot].mkv'
        # url='https://pub9.animeout.com/series/00RAPIDBOT/Berserk/[AnimeOut]%20Berserk%2001%201080pp%20Blu-ray%2010bit%20Dual%20Audio[50BCB14B][1080pp][NoobSubs][RapidBot].mkv'
        url='http://commondatastorage.googleapis.com/gtv-videos-bucket/sample/BigBuckBunny.mp4'
        print(url)
        # dl='https://www.4shared.com/web/embed/file/B9Y6LpO8ea'
        # response = redirect(url,permanent=True)
        return redirect(url,permanent=True)
    else:
        # epn=ep.split('-')[-1]
        # aid=ep.replace('-episode-'+epn,'')
        
        tail=re.findall(r'-episode-[\d-]+',ep)[0]
        aid=ep.replace(tail,'')
        epn=tail.replace('-episode-','')

        stream_r=rq.get(apiurl+'/vidcdn/watch/'+ep)
        streamj=stream_r.json()
        if not 'error' in streamj:
            stream_url=streamj['sources'][0]['file']
        else:
            # epn=ep.split('-')[-1]
            # aid=ep.replace('-episode-'+epn,'')
            aids=db.load()
            try:
                a=aids[aid]['response']
            except:
                r=rq.get(apiurl+'/anime-details/'+aid)
                a=r.json()
            for e in a['episodesList']:
                # nepn=e['episodeId'].split('-')[-1]
                tail=re.findall(r'-episode-[\d-]+',e['episodeId'])[0]
                nepn=tail.replace('-episode-','')
                if nepn==epn:
                    stream_r=rq.get(apiurl+'/vidcdn/watch/'+e['episodeId'])
                    streamj=stream_r.json()
                    stream_url=streamj['sources'][0]['file']
                    break

        threading.Thread(target=db_history.github_add,args=(aid,dict(source='gogo',episode=ep),gittoken,gitrepo,)).start()
        return redirect(stream_url,permanent=True)


    return HttpResponse(ep)

def get_feed(request):
    feed={
    "providerName":"Roku Recommends",
    "language":"en-US",
    "lastUpdated":"2017-04-20T02:01:00+02:00",
    'RECENT RELEASE':[],
    'DUB':[],
    'CHINESE':[]
    }
    dj=request.build_absolute_uri().replace(request.path,'')

    r=rq.get(apiurl+"/recent-release")
    rj=r.json()
    for a in rj:
        '''
        {'animeId': 'jashin-chan-dropkick-x', 'episodeId': 'jashin-chan-dropkick-x-episode-3', 
        'animeTitle': 'Jashin-chan Dropkick X', 'episodeNum': '3', 'subOrDub': 'SUB', 
        'animeImg': 'https://gogocdn.net/cover/jashin-chan-dropkick-x.png', 
        'episodeUrl': 'https://gogoanime.film///jashin-chan-dropkick-x-episode-3'}
        '''
        feed['RECENT RELEASE'].append(
            fill_movie(title=a['animeTitle'],id=a['episodeId'],thumbnail=a['animeImg'],genres=[a['subOrDub']],
                url=dj+'/polls/get_ep/'+a['episodeId'],
                shortDescription='Episode '+a['episodeNum']
                )
            )

    r=rq.get(apiurl+"/recent-release?type=2")
    rj=r.json()
    for a in rj:
        feed['DUB'].append(
            fill_movie(title=a['animeTitle'],id=a['episodeId'],thumbnail=a['animeImg'],genres=[a['subOrDub']],
                url=dj+'/polls/get_ep/'+a['episodeId'],
                shortDescription='Episode '+a['episodeNum']
                )
            )

    r=rq.get(apiurl+"/recent-release?type=3")
    rj=r.json()
    for a in rj:
        feed['CHINESE'].append(
            fill_movie(title=a['animeTitle'],id=a['episodeId'],thumbnail=a['animeImg'],genres=[a['subOrDub']],
                url=dj+'/polls/get_ep/'+a['episodeId'],
                shortDescription='Episode '+a['episodeNum']
                )
            )

    feed['series']=[]

    aids=db.load()
#     aids='''overlord-iv
# accel-world-dub
#     '''.replace('\n',' ').replace('  ',' ').split()
    for aid in aids:
        if '/category/' in aid:
            aid=aid.split('/category/')[-1]
        if aid:
            r=rq.get(apiurl+'/anime-details/'+aid)
            rj=r.json()
            print('\n')
            print(rj)
            if not 'error' in rj:
                feed['series'].append(
                    # fill_series(title=rj['animeTitle'],id=aid,totalEpisodes=rj['totalEpisodes'],
                    # shortDescription=rj['synopsis'],
                    # base_url=dj+'/polls/get_ep/'+aid,
                    # thumbnail=rj['animeImg'],
                    # genres=[['SUB','DUB'][bool(aid[-3:]=='dub')]]
                    # )

                    fill_anime(rj,id=aid,base_url=dj+'/polls/get_ep/')
                    )
            else:
                # print(rj)
                pass
    return HttpResponse(json.dumps(feed,indent=4))

def get_rss_feed(request):
    with open(r'C:\c\Python_projects\anime_site\anime.rss', 'r',encoding='utf-8') as fid:
        ans=fid.read()
    return HttpResponse(ans)

def update_last_query():
    global last_query
    last_query=db_query.github_download(gittoken,gitrepo)

yt_channels={
    'vinesauce':'UCzORJV8l3FWY4cFO8ot-F2w',
    'RedLetterMedia':'UCrTNhL_yO3tPTdQ5XgmmWjA',
    'Cinemassacre':'UC0M0rxSz3IF0CsSour1iWmw',
    'FanboyFlicks':'UCpsjEC4PlHmhM84yX5Y3rrg',
    'Internet Comment Etiquette with Erik':'UCyWDmyZRjrGHeKF-ofFsT5Q',
    'Boy boy':'UC_S45UpAYVuc0fYEcHN9BVQ',
    'I did a thing':'UCJLZe_NoiG0hT7QCX_9vmqw',
    'H3 Pocdast':'UCLtREJY21xRfCuEKvdki1Kw',
    'Channel 5 with Andrew Callaghan':'UC-AQKm7HUNMmxjdS371MSwg',
    'HasanAbi':'UCtoaZpBnrd0lhycxYJ4MNOQ',
    'Daily Dose of HasanAbi':'UCqsq-k2LLwJ-UM77pLrEbHw',
    'Hasanabi Moments':'UCobue-_fUPSIwdWULdE3MbQ',
    'HasanAbi Industries':'UCz2n05fvYYoVTrhq1ZUnyHA',
    'Hasanabi Reactlord':'UCBwbwVWMGEQSzJ0T7-YwtHA',
    'Hasanabi Enterprise':'UCMmJp0vS2hX8Tgc1xcSELpg',
    'Hasan Reactions':'UC1hW1iEFDsW-6V0zC8jqVQA',
    'Hasanabi Productions':'UCBBQ9PIs8ARguuwVJZowGIg',
    'Joel Haver':'UCVIFCOJwv3emlVmBbPCZrvw',
    'Stoned Gremlin Productions':'UCIO689mgXeuzH4M5NS7wZwg',
    'Ryan George':'UCh9IfI45mmk59eDvSWtuuhQ',
    'Pitch Meeting':'UC9Kq-yEt1iYsbUzNOoIRK0g',
    'El Pulso De La República':'UCK0_zBeybLuyXbOcHp7wmJA',
    'Grupo Fórmula':'UCzmd9Aj2wmPggWZJpLdBB8Q',
    'Wisecrack':'UC6-ymYjG0SU0jUWnWh9ZzEQ',
    'Screen Junkies':'UCOpcACMWblDls9Z6GERVi1A',
    'Steve Reviews':'UCqERpXggAprNW8QT_WO1N5Q',
    'TVSins':'UCe4bOvc1mYxFcQ5xPb9Zmow',
    'riserecords':'UCxnS0WDBVfBnTP2e97DYDSA',
    'Eclipse Records':'UC6Qasp2KPxCeiwDtFrvpOGA',
    'Century Media Records':'UCnK9PxMozTYs8ELOvgMNKFA',
    'Cold Ones':'UCfbnTUxUech4P1XgYUwYuKA',
    'Vargskelethor Uncut: Full Joel Streams':'UCRNCUBq676nUhXyy8AJzD5w',
    'Vargskelethor Joel: Mini Highlights':'UC1O1dhQcJQTycjcoeTSiuuw',
    'Vargskelethor Joel':'UCllm3HivMERwu2x2Sjz5EIg',
    'Vinesauce: The Full Sauce':'UC2_IYqb1Tc_8Azh7rByedPA',
    'RevScarecrow: After Hours':'UCSNF0FG_I8NboKf0H7Xn1CQ',
    'Revscarecrow: Vinesauce Rev':'UC_qjBu445WM4dulK392K6ww',
    'Billiam':'UCcHBw_Rs56RFcisYAOlFfmQ',
    'Jordan Fringe':'UCJKE87wqkVvbP2hUJcAKJNw',
    'Funny Or Die':'UCzS3-65Y91JhOxFiM7j6grg',
    'Michael Reeves':'UCtHaxi4GTYDpJgMSGy7AeSw',
    'HasanAbi Fix':'UClZj4-rsMlX2BqwG7I7wQLA',
    'The Problem With Jon Stewart':'UC5HJaVyYgo7WPCvIBchRBzQ',
    'penguinz0':'UCq6VFHwMzcMXbuKyG7SQYIg',
    'SaberSpark':'UCeGGpOehPGG7vQMUVc7tG8Q',
    'Cofeezilla':'UCFQMnBA3CS502aghlcr0_aw',
    'Kitboga':'UCm22FAXZMw1BaWeFszZxUKw',
    'Ink Master':'UCzrh2s9Vu9wUBf2Y2iIYcgA',
    'Jeremy Jahns':'UC7v3-2K1N84V67IF-WTRG-Q',
    'JoshDub':'UC9DWJ33CMvIseLlyx6hyRnA',
    'Zorman World':'UCu9DFMTm98z_sXyoDLSbc2w',
    'My Thoughts Will Probably Offend You':'UCbR-GzksKvEc1dgqvMG1QtQ',
    'Observe':'UCzMvqwt21xqm7Fg5Uo3lsRQ',
    'Phelan Porteous':'UCUp4yFAjgOA11a4h568vnrA',
    'Philip DeFranco':'UClFSU9_bUb4Rc6OYfTt5SPw',
    'radiOvni':'UCphRaBOm68qyxK2rNiEmDhQ',
    'Some More News':'UCvlj0IzjSnNoduQF0l3VGng',
    'TheWizWiki':'UClh9mrZULUGRQf-2oqPnPaw',
    'WatchMojo':'UCaWd5_7JhbQBe4dknZhsHJg',
    'CollegeHumor':'UCPDXXXJj9nax0fr0Wfc048g',
    'Aamon Animations':'UCo4au6lRX4-_gIczBneEZWA',
    'Alien\'s Guide':'UCu6DDGoV21YhwSb5iWbriAw',
    'Cynical Reviews':'UC1DCPS2j-o0bvfIilkc8RSw',
    'Darkar Company Studios':'UCmyIMuo8zRYgLshDff0vLuw',
    'Elvis The Alien':'UChc-m3saf8K2oJHDSsnsj_A',
    'Grimmjack':'UC23jPAIN8bbs7zphtB-JdLQ',
    'UpIsNotJump':'UCFLwN7vRu8M057qJF8TsBaA',
    'Vivziepop':'UCzfyYtgvkx5mLy8nlLlayYg',
    'Your Narrator':'UChfYPe-r_5EMHbBMT-YuYsA',
    'Napalm Records':'UCG7AaCh_CiG6pq_rRDNw72A',
    'Marty Music':'UCmnlTWVJysjWPFiZhQ5uudg',
    'Scotty Kilmer':'UCuxpxCCevIlF-k-K5YU8XPA',
    'Metal Blade Records':'UCSldglor1t-5E-Gy2eBdMrA',
    'Emergency Awesome':'UCDiFRMQWpcp8_KD4vwIVicw',
    'Latinus_us':'UC-FVhfqCwhzpJ4DTJOMMofA',
    'LastWeekTonight':'UC3XTzVzaHQEd30rQbuvCtTQ',
    'Matthew Kiichichaos Heafy':'UCJ05pLKdBCcZpaQlixNlZAg',
    'JonTronShow':'UCdJdEguB1F1CiYe7OEi3SBg',
    'darkTunes Music Group':'UCuCYsYBaq3j0gM4wWo82LkQ',
    'NUMBSKULLS':'UCZSCvpp33elIQdn52NRaJ0Q',
    'Adult Swim':'UCgPClNr5VSYC3syrDUIlzLw',
    'CinnamonToastKen':'UCepq9z9ovYGxhNrvf6VMSjg',
    'The Daily Show with Trevor Noah':'UCwWhs_6x42TyRM4Wstoq8HA',
    'münecat':'UCqNpjt_UcMPgm_9gphZgHYA',
    'enchufetv':'UCoGDh1Xa3kUCpok24JN5DKA',
    'Nuclear Blast Records':'UCoxg3Kml41wE3IPq-PC-LQw',
    'Frontiers Music srl':'UCBLAoqCQyz6a0OvwXWzKZag',
    'Sumerian Records':'UCAtlZO9a52JIhQRyXDRLaZQ',
    'Channel Awesome':'UCiH828EtgQjTyNIMH6YiOSw',
    'Avatar Metal':'UCyaPf0E-PRRZH3UvvxNPeEw',
    'Eclipse Records':'UC6Qasp2KPxCeiwDtFrvpOGA',
    'AngryJoeShow':'UCsgv2QHkT2ljEixyulzOnUQ',
    'El Hank':'UCo17PdEv0S3AZWclXwrLdXg',
    'Better Noise Music':'UCqh8RdUfSR9lGyasBhM_bjA',
    'Screen Rant':'UC2iUwfYi_1FCGGqhOUNx-iA',
    'Lolweapon':'UCw2KIu_oU6qHYOnL7QQ3NUw',
    'Fandom Games':'UCf6J9yokPS0ys456jvjLBGQ',
    'Andy Guitar':'UC9cvVvlvr-qBssphm1EdYGQ',
    'Comedy Central':'UCUsN5ZwHx2kILm84-jPDeXw',
    'Cinematic Excrement':'UCStzEOk2Pfftjy2f2sHjflg',
    'Movie Files':'UCqD7CXlHe1jNemKzFjkOUlQ',

    }


def categories(request):

    x=threading.Thread(target=update_fav_anime)
    x.start()
    y=threading.Thread(target=update_fav_series)
    y.start()
    threading.Thread(target=update_last_query).start()

    # with open(r"C:\c\Python_projects\anime_site\api\polls\categories.xml", 'r',encoding='utf-8') as fid:
    #     ans=fid.read()
    dj=request.build_absolute_uri().replace(request.path,'')

    threading.Thread(target=update_feed_flixhq_home).start()
    # threading.Thread(target=rq.get,args=(dj+'/polls/update_feed_flixhq_home',)).start()

    ans=f'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<categories>

    <!-- banner_ad: optional element which displays an at the top level category screen -->
    <banner_ad sd_img="https://devtools.web.roku.com/videoplayer/images/missing.png" hd_img="https://devtools.web.roku.com/videoplayer/images/missing.png"/>

    <category title="Gogoanime" description="Anime" sd_img="pkg:/images/gogoanime.jpg" hd_img="pkg:/images/gogoanime.jpg">
        <categoryLeaf title="-Recent release-" description="" feed="{dj}/polls/recent_anime/"/>
        <categoryLeaf title="Top airing" description="" feed="{dj}/polls/top_airing_anime/"/>
        <categoryLeaf title="DUB" description="" feed="{dj}/polls/recent_anime_dub/"/>
        <categoryLeaf title="CHINESE" description="" feed="{dj}/polls/recent_anime_chinese/"/>
    </category>
    <category title="FlixHQ" description="Free Movies and Series" sd_img="pkg:/images/flixhq.jpg" hd_img="pkg:/images/flixhq.jpg">
        <categoryLeaf title="Trending" description="" feed="{dj}/polls/flixhq_trending/"/>
        <categoryLeaf title="Latest Movies" description="" feed="{dj}/polls/flixhq_latest_movies/"/>
        <categoryLeaf title="Latest Series" description="" feed="{dj}/polls/flixhq_latest_series/"/>
    </category>
    <category title="Favorite Movies and TV" description="Series/movies" sd_img="pkg:/images/Movies_TV.png" hd_img="pkg:/images/Movies_TV.png">
        <categoryLeaf title="Favorite Movies" description="" feed="{dj}/polls/favorite_movies/"/>
        <categoryLeaf title="Favorite Series" description="" feed="{dj}/polls/favorite_series/"/>
        <categoryLeaf title="Last watched episodes" description="" feed="{dj}/polls/history_series/"/>
    </category>
    <category title="Favorite Animes" description="Animes/OVAs/Anime movies" sd_img="pkg:/images/Favorite_anime" hd_img="pkg:/images/Favorite_anime.png">
        <categoryLeaf title="Favorite Animes" description="" feed="{dj}/polls/favorite_anime/"/>
        <categoryLeaf title="Last watched" description="" feed="{dj}/polls/history_anime/"/>
    </category>
    <category title="Search" description="https://rb.gy/8bz69s" sd_img="pkg:/images/qrsearch.png" hd_img="pkg:/images/qrsearch.png">
        <categoryLeaf title="Last searched series" description="" feed="{dj}/polls/last_query_series/"/>
        <categoryLeaf title="Last searched animes" description="" feed="{dj}/polls/last_query_animes/"/>
    </category>
    <category title="YouTube" description="" sd_img="pkg:/images/YouTube.png" hd_img="pkg:/images/YouTube.png">
        <categoryLeaf title="Queue" description="" feed="{dj}/polls/feed_yt_queue/"/>
        <categoryLeaf title="History" description="" feed="{dj}/polls/history_youtube/"/>
    </category>'''
    # ans+='''
    # <category title="YouTube Channels" description="" sd_img="pkg:/images/YouTube.png" hd_img="pkg:/images/YouTube.png">'''
    cpack=''
    i=0

    for ci in sorted(yt_channels,key=lambda i: i[0].lower()):
        cid=yt_channels[ci]
        cpack+=f'''
        <categoryLeaf title="{ci}" description="" feed="{dj}/polls/feed_yt_channel/?cid={cid}"/>'''
        i+=1
        if i==1:
            letteri=ci[0].upper()
        elif i==11:
            i=0
            letterf=ci[0].upper()
            ans+=f'''
    <category title="YouTube Channels {letteri}-{letterf}" description="" sd_img="pkg:/images/YouTube.png" hd_img="pkg:/images/YouTube.png">'''
            ans+=cpack+'''
    </category>'''
            cpack=''

    if i<10:
        letterf=ci[0].upper()
        ans+=f'''
    <category title="YouTube Channels {letteri}-{letterf}" description="" sd_img="pkg:/images/YouTube.png" hd_img="pkg:/images/YouTube.png">'''
        ans+=cpack+'''
    </category>'''
    ans+=f'''
</categories>
'''
    return HttpResponse(ans,content_type='text/xml')

def feed_yt_channel(request):
    if request:
        dj=request.build_absolute_uri().replace(request.path,'')
    else:
        dj=''
    if '?' in dj:
        dj=dj.split('?')[0]
    base_url=dj+'/polls/get_yt_stream/'
    # aids=db_yt_queue.load()

    root = minidom.Document()
    feed = root.createElement('feed')
    root.appendChild(feed)

    cid=request.GET.get('cid', None)
    # try:
    #     cid=yt_channels[cid]
    # except:
    #     pass
    

    fields='?fields=author,authorId,authorThumbnails,description,subCount,latestVideos'
    # inst='https://vid.puffyan.us/api/v1'
    inst=invidious_inst[random.randint(0,len(invidious_inst))-1]
    headers = {"User-Agent": "Mozilla/5.0 (X11; CrOS x86_64 12871.102.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.141 Safari/537.36"}

    url=inst+'/api/v1/channels/'+cid+fields
    # print(url)
    rj=rq.get(url,headers=headers).json()

    for a in rj['latestVideos']:

    # for aid in aids:
        # if not aid:
            # continue
        # try:
        #     a=aids[aid]['response']
        # except:
        #     yv=pytube.YouTube('?v='+aid)
            # a=yv.vid_info['videoDetails']
        # title=rk.titlexml(a['title']).replace('&quot;','"')
        title=a['title']
        thumbnail='https://i.ytimg.com/vi/'+a['videoId']+'/hqdefault.jpg'

        item=addto(root,feed,'item',attr=dict(
            sdImg=thumbnail,
            hdImg=thumbnail
            ))

        addto(root,item,'title',title)
        addto(root,item,'contentId',a['videoId'])
        addto(root,item,'contentType','Episode')
        addto(root,item,'contentQuality','HD')
        addto(root,item,'streamFormat','mp4')
        media=addto(root,item,'media')
        url_args=pathargs(aid=a['videoId'])
        addto(root,media,'streamUrl',base_url+url_args)
        # desc=a['shortDescription']
        desc=a['publishedText']+'\n'+'Duration: '+ short_h_m_s(a['lengthSeconds'])+'\n'+format(a['viewCount'],',')+str(' views ')

        addto(root,item,'synopsis',
            desc
            )
        try:
            addto(root,item,'genres',a['author'])
        except:
            addto(root,item,'genres','')

    xml_str = root.toprettyxml(indent ="  ",encoding='UTF-8',standalone='yes') 
    return HttpResponse(xml_str,content_type='text/xml')

def recent_gogo(dj,rtype='/recent-release'):
    r=rq.get(apiurl+rtype)
    rj=r.json()

    base_url=dj+'/polls/get_ep/'

    root = minidom.Document()
    feed = root.createElement('feed')
    root.appendChild(feed)
    for a in rj:
        title=rk.titlexml(a['animeTitle'])
        desc='Episode '+a['episodeNum']
        url=dj+'/polls/get_ep/'+a['episodeId']
        thumbnail=a['animeImg']
        item=addto(root,feed,'item',attr=dict(
            sdImg=thumbnail,
            hdImg=thumbnail
            ))

        addto(root,item,'title',desc+' - '+title)
        addto(root,item,'contentId',a['episodeId'])
        addto(root,item,'contentType','Episode')
        addto(root,item,'contentQuality','HD')
        addto(root,item,'streamFormat','hls')
        addto(root,item,'synopsis',desc)
        addto(root,item,'genres',a['subOrDub'])
        
        media=addto(root,item,'media')
        addto(root,media,'streamUrl',base_url+'test')
        season=addto(root,media,'season',None)
        # for e in reversed(a['episodesList']):
        for e in get_anime_episode_list(a):
            addto(root,season,'episode',attr=dict(
                title='Episode '+e['episodeNum'],
                url=base_url+e['episodeId']
                ))

    xml_str = root.toprettyxml(indent ="  ",encoding='UTF-8',standalone='yes')
    return xml_str

def recent_anime(request):
    dj=request.build_absolute_uri().replace(request.path,'')
    return HttpResponse(recent_gogo(dj,rtype='/recent-release'),content_type='text/xml')

def recent_anime_dub(request):
    dj=request.build_absolute_uri().replace(request.path,'')
    return HttpResponse(recent_gogo(dj,rtype='/recent-release?type=2'),content_type='text/xml')
def recent_anime_chinese(request):
    dj=request.build_absolute_uri().replace(request.path,'')
    return HttpResponse(recent_gogo(dj,rtype='/recent-release?type=3'),content_type='text/xml')

def get_anime_episode_list(rj):
    if 'episodesList' in rj:
        return rj['episodesList']
    elif 'latestEp' in rj:
        lep=int(rj['latestEp'].split()[-1])
        return ({'episodeNum':str(i),'episodeId':rj['animeId']+'-episode-'+str(i)} for i in range(lep,0,-1))
    elif "episodeNum" in rj:
        lep=int(rj['episodeNum'])
        return ({'episodeNum':str(i),'episodeId':rj['animeId']+'-episode-'+str(i)} for i in range(lep,0,-1))

        # return ({} )

def test(request):
    # https://gogo4rokuapi.herokuapp.com
    dj=request.build_absolute_uri().replace(request.path,'')
    base_url=dj+'/polls/get_ep/'
    rtype='/top-airing'
    r=rq.get(apiurl+rtype)
    rj=r.json()
    # return HttpResponse('test')
    # return JsonResponse(rj)

    root = minidom.Document()
    feed = root.createElement('feed')
    root.appendChild(feed)
    for a in rj:
        title=rk.titlexml(a['animeTitle'])
        # desc='Epidose '+a['episodeNum']
        desc=a['latestEp']
        url=dj+'/polls/get_ep/test'
        thumbnail=a['animeImg']
        item=addto(root,feed,'item',attr=dict(
            sdImg=thumbnail,
            hdImg=thumbnail
            ))

        addto(root,item,'title',desc+' - '+title)
        addto(root,item,'contentId',a['animeId']+'-'+a['latestEp'].lower().replace(' ','-'))
        addto(root,item,'contentType','Episode')
        addto(root,item,'contentQuality','HD')
        addto(root,item,'streamFormat','hls')
        addto(root,item,'synopsis',desc)
        addto(root,item,'genres',', '.join(a['genres']))
        
        media=addto(root,item,'media')
        addto(root,media,'streamUrl',base_url+'test')
        season=addto(root,media,'season',None)
        # for e in reversed(a['episodesList']):
        for e in get_anime_episode_list(a):
            addto(root,season,'episode',attr=dict(
                title='Episode '+e['episodeNum'],
                url=base_url+e['episodeId']
                ))

    xml_str = root.toprettyxml(indent ="  ",encoding='UTF-8',standalone='yes')
    return HttpResponse(xml_str,content_type='text/xml')

def favorite_anime(request):
    dj=request.build_absolute_uri().replace(request.path,'')
    base_url=dj+'/polls/get_ep/'

    aids=db.load()

    root = minidom.Document()
    feed = root.createElement('feed')
    root.appendChild(feed)

    for aid in aids:
        if not aid:
            continue
        if '/category/' in aid:
            aid=aid.split('/category/')[-1]
        try:
        # if db.isin(aid):
            a=aids[aid]['response']
        except:
        # else:
            r=rq.get(apiurl+'/anime-details/'+aid)
            a=r.json()

        title=rk.titlexml(a['animeTitle'])
        thumbnail=a['animeImg']

        item=addto(root,feed,'item',attr=dict(
            sdImg=thumbnail,
            hdImg=thumbnail
            ))

        addto(root,item,'title',title)
        addto(root,item,'contentId',aid)
        addto(root,item,'contentType','Season')
        addto(root,item,'contentQuality','HD')
        addto(root,item,'streamFormat','hls')
        addto(root,item,'synopsis',a['synopsis'])
        addto(root,item,'genres',['SUB','DUB'][bool(aid[-3:].lower()=='dub')])

        media=addto(root,item,'media')
        addto(root,media,'streamUrl',base_url+'test')
        season=addto(root,media,'season',None)
        for e in reversed(a['episodesList']):
            addto(root,season,'episode',attr=dict(
                title='Episode '+e['episodeNum'],
                # text='Episode '+e['episodeNum'],
                url=base_url+e['episodeId']
                ))
    xml_str = root.toprettyxml(indent ="  ",encoding='UTF-8',standalone='yes')
    return HttpResponse(xml_str,content_type='text/xml')


def last_query_animes(request):
    global last_query
    dj=request.build_absolute_uri().replace(request.path,'')
    base_url=dj+'/polls/get_ep/'

    aids=db.load()

    root = minidom.Document()
    feed = root.createElement('feed')
    root.appendChild(feed)

    for aid in last_query['animes']:
        if not aid:
            continue
        if '/category/' in aid:
            aid=aid.split('/category/')[-1]
        try:
        # if db.isin(aid):
            a=aids[aid]['response']
        except:
            try:
                a=last_query['animes'][aid]['response']
            except:
                r=rq.get(apiurl+'/anime-details/'+aid)
                a=r.json()


        title=rk.titlexml(a['animeTitle'])
        thumbnail=a['animeImg']

        item=addto(root,feed,'item',attr=dict(
            sdImg=thumbnail,
            hdImg=thumbnail
            ))

        addto(root,item,'title',title)
        addto(root,item,'contentId',aid)
        addto(root,item,'contentType','Season')
        addto(root,item,'contentQuality','HD')
        addto(root,item,'streamFormat','hls')
        addto(root,item,'synopsis',a['synopsis'])
        addto(root,item,'genres',['SUB','DUB'][bool(aid[-3:].lower()=='dub')])

        media=addto(root,item,'media')
        addto(root,media,'streamUrl',base_url+'test')
        season=addto(root,media,'season',None)
        for e in reversed(a['episodesList']):
            addto(root,season,'episode',attr=dict(
                title='Episode '+e['episodeNum'],
                # text='Episode '+e['episodeNum'],
                url=base_url+e['episodeId']
                ))
    xml_str = root.toprettyxml(indent ="  ",encoding='UTF-8',standalone='yes')
    return HttpResponse(xml_str,content_type='text/xml')



def get_anime(request,aid):
    dj=request.build_absolute_uri().replace(request.path,'')
    base_url=dj+'/polls/get_ep/'
    root = minidom.Document()
    feed = root.createElement('feed')
    root.appendChild(feed)


    xml_str = root.toprettyxml(indent ="  ",encoding='UTF-8',standalone='yes') 
    return HttpResponse(xml_str,content_type='text/xml')

series_results={}
anime_results={}
dbo_all={}
def _down_response(curl,aid,dbid,do_save=False):
    global series_results,anime_results,dbo_all
    #
    try:
        # curl=apiconsu+'/movies/flixhq/info'+pathargs(id=aid)
        # print(curl)
        r=rq.get(curl)
        a=r.json()

        if dbid=='flixhq':
            if 'title' in a:
                series_results[aid]=dict(response=a)
                # if do_save:
                #     dbo_all[aid]=dict(response=a)
        elif dbid=='gogoanime':
            anime_results[aid]=dict(response=a)
        print(curl)
    except:
        print(curl)
        print(r.text)
        traceback.print_exc()



def update_fav_anime():
    global anime_results
    print('+'*20)
    print('updating fav anime')
    print('+'*20)
    # aids=db.load()
    aids=db.github_download(gittoken,gitrepo,do_save=True)
    # if len(aids)<2:
    #     aids=['accel-world-dub',
    #         'overlord-iv']
    ts=[]
    for aid in aids:
        if not aid:
            continue
        if '/category/' in aid:
            aid=aid.split('/category/')[-1]
        if aids[aid]['response']['status']=='Ongoing':
            # def ti():
            if True:
                # curl=apiurl+'/anime-details/'+aid
                # r=rq.get(curl)
                # a=r.json()        
                # db.add(aid,dict(
                #     response=a,
                #     ))
                # print(curl)
                ts.append(threading.Thread(target=_down_response,args=(apiurl+'/anime-details/'+aid,aid,'gogoanime',)))
                ts[-1].start()
    for tti in ts:
        tti.join()
    for k in anime_results:
        db.add(k,anime_results[k])
    db.github_save(db.load(),gittoken,gitrepo)
    print('db updated to github')
    anime_results={}
def update_fav_series():
    global series_results,dbo_all
    print('+'*20)
    print('updating fav series')
    print('+'*20)
    aids=db_flixhq.github_download(gittoken,gitrepo,do_save=True)
    dbo_all=db_flixhq_all.load()
    recent_home=bool(abs(time.time()-dbo_all['']['saved'])/60<30)
    # if len(aids)<2:
    #     aids=[
    #     'tv/watch-love-death-and-robots-42148'
    #     ]
    series_results=dbo_all
    ts=[]
    for aid in aids:
        if not aid:
            continue
        try:
            if aid[0:6]=='movie/':
                continue
        except:
            pass
        # def ti():
        if True:
            # try:
            #     curl=apiconsu+'/movies/flixhq/info'+pathargs(id=aid)
            #     r=rq.get(curl)
            #     a=r.json()
            #     db_flixhq.add(aid,dict(
            #         response=a,
            #         ))
            #     print(curl)
            # except:
            #     traceback.print_exc()
        # ti()
            if recent_home and aid in dbo_all:
                ts.append(threading.Thread(target=_down_response,args=(apiconsu+'/movies/flixhq/info'+pathargs(id=aid),aid,'flixhq',)))
                ts[-1].start()
            elif not recent_home and not aid in dbo_all:
                ts.append(threading.Thread(target=_down_response,args=(apiconsu+'/movies/flixhq/info'+pathargs(id=aid),aid,'flixhq',)))
                ts[-1].start()
    for tti in ts:
        tti.join()

    for k in series_results:
        dbo_all[k]=series_results[k]
        if k in aids:
            aids[k]=series_results[k]
        # db_flixhq.add(k,series_results[k])
    db_flixhq.github_save(aids,gittoken,gitrepo)
    if dbo_all:
        db_flixhq_all.github_save(dbo_all,gittoken,gitrepo)
    print('db_flixhq updated to github')
    series_results={}

def addto_fav_anime_full_url(request,trash,aid):
    return addto_fav_anime(request,aid)
def removefrom_fav_anime_full_url(request,trash,aid):
    return removefrom_fav_anime(request,aid)

def addto_fav_anime(request,aid):
    try:
        if not aid:
            raise ValueError
        if len(aid)>6 and aid[0:6]=='watch-' and aid[-1].isnumeric():
            raise ValueError
        r=rq.get(apiurl+'/anime-details/'+aid)
        a=r.json()
        # db.add(aid,
        #     dict(response=a)
        #     )
        if 'error' in a:
            raise ValueError
        # db.github_add(aid,dict(response=a),gittoken,gitrepo)
        threading.Thread(target=db.github_add,args=(aid,dict(response=a),gittoken,gitrepo,)).start()
        # db.github_add(aid,dict(response=a),gittoken,gitrepo)

        if request:
            # return HttpResponse("Success: added "+aid)
            return HttpResponse(_html_added('Success!','added',aid))
        else:
            print("Success: added "+aid)
            return True,aid

    except:
        if request:
            # return HttpResponse("Failiure: not added "+aid)
            return HttpResponse(_html_added('Failiure!','not added',aid))
        else:
            print("Failiure: not added "+aid)
            return False, aid

def addto_yt_queue(request,aid):
    try:
        if not aid:
            raise ValueError
        
        # db.github_add(aid,dict(response=a),gittoken,gitrepo)
        yv=pytube.YouTube('?v='+aid)

        a=yv.vid_info['videoDetails']

        threading.Thread(target=db_yt_queue.github_add,args=(aid,dict(response=a),gittoken,gitrepo,)).start()
        # db.github_add(aid,dict(response=a),gittoken,gitrepo)

        if request:
            # return HttpResponse("Success: added "+aid)
            return HttpResponse(_html_added('Success!','added',a['title']))
        else:
            print("Success: added "+aid)
            return True,aid

    except:
        if request:
            # return HttpResponse("Failiure: not added "+aid)
            return HttpResponse(_html_added('Failiure!','not added',aid))
        else:
            print("Failiure: not added "+aid)
            return False, aid


def _html_added(ans,added,aid,urlback=''):
    # urlback='../../search'
    urlback=''
    s='''
<html>
<body text="#ffffff" style=" background-color: black;">
<head>
    <meta charset = "utf-8">
    <title>GeeksforGeeks Example</title>

    <!--CSS Code-->
    <style media = "screen">
        body {
            background: orange;
            overflow: hidden;
            color: white;
        }
        .GeeksForGeeks {
            text-align: center;
            background: #282923;
            font-size: 3.5vw;
            position: absolute;
            top: 1%;
            left: 1%;
            right: 1%;
        }
    </style>
</head>
 <div class = "GeeksForGeeks">
    '''
    # s+='Power up command sent to '+aid+'!<br>'
    # ans='Success!' if success else 'Failiure!'
    if 'added' in added:
        added='<span style="background-color: #1D7948; color: white; ">'+added+'</span>'
        tofav=' to favorites.'
    else:
        added='<span style="background-color: #B12020; color: white; ">'+added+'</span>'
        tofav=' from favorites.'

    if not 'r' in ans:
        ans='<span style="background-color: #1D7948; color: white; ">'+ans+'</span>'
    else:
        ans='<span style="background-color: #B12020; color: white; ">'+ans+'</span>'


    s+=ans+':<br>'+added+' '+aid+tofav
    #ans=send_magic_packet_git_dummy(pc)
    s+='<br>'
    # if ans=='Success!':
    #     s+='Check TeamViewer and wait for the computer to log on.<br>'
    s+='<br>Returning in 2 seconds...'
    s+='</div>'
    if urlback:
        s+='<meta http-equiv="refresh" content="3;url='+urlback+'" />'
    else:
        s+=r'''<script language="JavaScript" type="text/javascript">
    setTimeout("window.history.go(-1)",2000);
</script>
    '''
    s+='</body></html>'

    return s

def addto_fav_series(request,ctype,id):
    try:
        if not ctype or not id:
            raise ValueError
        aid=ctype+'/'+id
        # print('<>'*30)
        # print(aid)
        r=rq.get(apiconsu+'/movies/flixhq/info'+pathargs(id=aid))
        a=r.json()
        # db_flixhq.add(aid,dict(
        #     response=a,
        #     ))
        # print('<>'*30)
        # print(type(a),'a')
        # print(gittoken,gitrepo)
        # db_flixhq.github_add(aid,dict(response=a),gittoken,gitrepo)
        threading.Thread(target=db_flixhq.github_add,args=(aid,dict(response=a),gittoken,gitrepo,)).start()
        # if request: return HttpResponse("Success: added "+aid)
        if request: return HttpResponse(_html_added('Success!','added',aid))
    except:
        traceback.print_exc()
        # if request: return HttpResponse("Failiure: not added "+aid)
        if request: return HttpResponse(_html_added('Failiure!','not added',aid))
def removefrom_fav_anime(request,aid):
    dj=request.build_absolute_uri().replace(request.path,'')
    # print(dj)
    if '?' in dj:
        dj=dj.split('?')[0]
    # print(dj)
    if db.github_remove(aid,gittoken,gitrepo):
        # if request: return HttpResponse("Success: removed "+aid)
        if request: return HttpResponse(_html_added('Success!','removed',aid,dj+'/polls/search_fav_anime'))
    else:
        # if request: return HttpResponse("Failiure: not removed "+aid)
        if request: return HttpResponse(_html_added('Failiure!','not removed',aid,dj+'/polls/search_fav_anime'))
def removefrom_fav_series(request,ctype,id):
    aid=ctype+'/'+id
    dj=request.build_absolute_uri().replace(request.path,'')
    if '?' in dj:
        dj=dj.split('?')[0]
    if db_flixhq.github_remove(aid,gittoken,gitrepo):
        # if request: return HttpResponse("Success: removed "+aid)
        if request: return HttpResponse(_html_added('Success!','removed',aid,dj+'/polls/search_fav_series'))
    else:
        # if request: return HttpResponse("Failiure: not removed "+aid)
        if request: return HttpResponse(_html_added('Failiure!','not removed',aid,dj+'/polls/search_fav_series'))

def removefrom_yt_queue(request,aid):
    dj=request.build_absolute_uri().replace(request.path,'')
    if '?' in dj:
        dj=dj.split('?')[0]
    try:
        if db_yt_queue.github_remove(aid,gittoken,gitrepo):
            # if request: return HttpResponse("Success: removed "+aid)
            if request: return HttpResponse(_html_added('Success!','removed',aid,dj+'/polls/view_yt_queue/'))
        else:
            # if request: return HttpResponse("Failiure: not removed "+aid)
            if request: return HttpResponse(_html_added('Failiure!','not removed',aid,dj+'/polls/view_yt_queue/'))
    except:
        return HttpResponse(_html_added('Failiure!','not removed',aid,dj+'/polls/view_yt_queue/'))

def get_flixhq_ep(request):
    global series_ep_cache
    eid=request.GET.get('eid', None)
    aid=request.GET.get('aid', None)

    if eid and aid:
        # ?eid=939832&aid=tv%2Fwatch-love-death-and-robots-42148
        # ?episodeId=939832&mediaId=tv%2Fwatch-love-death-and-robots-42148&server='vidcloud'
        eid=request.GET.get('eid', None)
        aid=request.GET.get('aid', None)
        # print(eid)
        # print(aid)
        if '"' in aid:
            aid=aid.split('"')[0]
        aid=aid.rstrip('<')

        for iserver in ('vidcloud','upcloud','mixdrop'):

            try:
                url_args=pathargs(episodeId=eid,server=iserver,mediaId=aid)
                url=apiconsu+'/movies/flixhq/watch'+url_args
                print(aid)
                print(url)
                er=rq.get(url)
                erj=er.json()
                stream_url=erj['sources'][0]['url']
                validurl=True
            except:
                validurl=False

            try:
                raise NotImplementedError
                ans=erj['subtitles'][0]['url']
                for sub in erj['subtitles']:
                    # print(sub)
                    if 'eng' in sub['lang'].lower()[0:4]:
                        ans=sub['url']
                        break
                vtt=rq.get(ans)
                ans=str_vtt_to_srt(vtt.text)
                series_ep_cache[url_args]=ans
            except:
                series_ep_cache[url_args]=''

            if validurl:
                break
        if validurl:
            threading.Thread(target=db_history.github_add,args=(aid,dict(source='flixhq',episode=eid),gittoken,gitrepo,)).start()
        return redirect(stream_url,permanent=True)
    else:
        url='http://commondatastorage.googleapis.com/gtv-videos-bucket/sample/BigBuckBunny.mp4'
        return redirect(url,permanent=True)

    return HttpResponse(request.path)

def get_flixhq_sub(request):
    global series_ep_cache
    eid=request.GET.get('eid', None)
    aid=request.GET.get('aid', None)
    if eid and aid:
        # ?eid=939832&aid=tv%2Fwatch-love-death-and-robots-42148
        # eid=request.GET.get('eid', None)
        # aid=request.GET.get('aid', None)
        # print(eid)
        # print(aid)

        url_args=pathargs(episodeId=eid,server='vidcloud',mediaId=aid)

        if url_args in series_ep_cache:
            # return redirect(series_ep_cache[url_args],permanent=True)
            return HttpResponse(series_ep_cache[url_args])

        er=rq.get(apiconsu+'/movies/flixhq/watch'+url_args)
        erj=er.json()
        stream_url=erj['sources'][0]['url']

        try:            
            ans=erj['subtitles'][0]['url']
            for sub in erj['subtitles']:
                # print(sub)
                
                if 'eng' in sub['lang'].lower()[0:4]:
                    ans=sub['url']
                    break
            vtt=rq.get(ans)
            ans=str_vtt_to_srt(vtt.text)
            series_ep_cache[url_args]=ans
        except:
            series_ep_cache[url_args]=''

        # return redirect(stream_url,permanent=True)
        if series_ep_cache[url_args]:
            # return redirect(series_ep_cache[url_args],permanent=True)
            return HttpResponse(series_ep_cache[url_args])
        else:
            return HttpResponse(request.path)
    else:
        ans="https://cc.1clickcdn.ru/05/61/05617ecfaaf725ef9a7bec67913a532b/eng-2.vtt"
        vtt=rq.get(ans)
        ans=str_vtt_to_srt(vtt.text)
        # return redirect(ans,permanent=True)
        return HttpResponse(ans)

    return HttpResponse(request.path)


def favorite_series(request):
    if request:
        dj=request.build_absolute_uri().replace(request.path,'')
    else:
        dj=''
    base_url=dj+'/polls/get_flixhq_ep/'
    
    aids=db_flixhq.load()

    root = minidom.Document()
    feed = root.createElement('feed')
    root.appendChild(feed)

    for aid in aids:
        if not aid or aid[0:2]!='tv':
            continue
        # print(aid)
        # if db_flixhq.isin(aid):
        try:
            #print(aid)
            a=aids[aid]['response']
            # print(a)
        except:
        # else:
            r=rq.get(apiconsu+'/movies/flixhq/info'+pathargs(id=aid))
            a=r.json()

        title=rk.titlexml(a['title'])
        thumbnail=a['image']

        item=addto(root,feed,'item',attr=dict(
            sdImg=thumbnail,
            hdImg=thumbnail
            ))

        addto(root,item,'title',title)
        addto(root,item,'contentId',aid)
        addto(root,item,'contentType','Season')
        addto(root,item,'contentQuality','HD')
        addto(root,item,'streamFormat','hls')
        media=addto(root,item,'media')
        addto(root,media,'streamUrl',base_url)
        addto(root,media,'subtitleUrl',dj+'/polls/get_flixhq_sub/')
        season=addto(root,media,'season',None)
        addto(root,item,'synopsis',
            ''
            )
        addto(root,item,'genres',', '.join(a['genres']))

        for e in a['episodes']:
            url_args=pathargs(eid=e['id'],aid=aid)
            addto(root,season,'episode',attr=dict(
                # title='S'+str(e['season']).rjust(2,'0')+'E'+str(e['number']).rjust(2,'0'),
                title='S'+str(e['season']).rjust(2,'0')+e['title'],
                url=base_url+url_args,
                subs=dj+'/polls/get_flixhq_sub/'+url_args
                ))
    xml_str = root.toprettyxml(indent ="  ",encoding='UTF-8',standalone='yes') 
    return HttpResponse(xml_str,content_type='text/xml')

def favorite_movies(request):
    if request:
        dj=request.build_absolute_uri().replace(request.path,'')
    else:
        dj=''
    base_url=dj+'/polls/get_flixhq_ep/'
    
    aids=db_flixhq.load()

    root = minidom.Document()
    feed = root.createElement('feed')
    root.appendChild(feed)

    for aid in aids:
        if not aid or aid[0:2]=='tv':
            continue
        # print(aid)
        # if db_flixhq.isin(aid):
        try:
            #print(aid)
            a=aids[aid]['response']
            # print(a)
        except:
            r=rq.get(apiconsu+'/movies/flixhq/info'+pathargs(id=aid))
            a=r.json()        
        title=rk.titlexml(a['title'])
        thumbnail=a['image']

        item=addto(root,feed,'item',attr=dict(
            sdImg=thumbnail,
            hdImg=thumbnail
            ))

        addto(root,item,'title',title)
        addto(root,item,'contentId',aid)
        addto(root,item,'contentType','Episode')
        addto(root,item,'contentQuality','HD')
        addto(root,item,'streamFormat','hls')
        media=addto(root,item,'media')
        url_args=pathargs(eid=a['episodes'][0]['id'],aid=aid)
        addto(root,media,'streamUrl',base_url+url_args)
        addto(root,media,'subtitleUrl',dj+'/polls/get_flixhq_sub/'+url_args)
        # season=addto(root,media,'season',None)
        desc='Released: '+a['releaseDate']

        addto(root,item,'synopsis',
            desc
            )
        addto(root,item,'genres',', '.join(a['genres']))

        # for e in a['episodes']:
        #     addto(root,season,'episode',attr=dict(
        #         # title='S'+str(e['season']).rjust(2,'0')+'E'+str(e['number']).rjust(2,'0'),
        #         title='S'+str(e['season']).rjust(2,'0')+e['title'],
        #         url=base_url+pathargs(eid=e['id'],aid=aid)
        #         ))
    xml_str = root.toprettyxml(indent ="  ",encoding='UTF-8',standalone='yes') 
    return HttpResponse(xml_str,content_type='text/xml')

def get_yt_stream(request,):
    aid=request.GET.get('aid', None)
    isqueue=request.GET.get('queue',None)

    if aid:
        print(aid)
        try:
            stream_url=''
            if not stream_url:
                yv=pytube.YouTube('https://www.youtube.com/watch?v='+aid)
                for st in yv.streams.filter(file_extension='mp4',progressive=True):
                    if st.mime_type=='video/mp4':
                        stream_url=st.url
            if not stream_url:
                raise FileNotFoundError
        except:
            # traceback.print_exc()
            try:
                try:
                    inst=invidious_inst[random.randint(0,len(invidious_inst))-1]
                    r=rq.get(f'{inst}/api/v1/videos/{aid}?fields=formatStreams')
                    rj=r.json()
                except:
                    time.sleep(1.5)
                    while True:
                        ninst=invidious_inst[random.randint(0,len(invidious_inst))-1]
                        if ninst==inst:
                            continue
                        else:
                            inst=ninst
                            break
                    r=rq.get(f'{inst}/api/v1/videos/{aid}?fields=formatStreams')
                    rj=r.json()
                for st in rj['formatStreams']:
                    if 'video/mp4' in st['type']:
                        stream_url= st['url']
            except:
                traceback.print_exc()
                if not stream_url:
                    # localhost:3000/polls/get_yt_stream/?aid=Q6Ue8YIKhFc
                    # ydl_opts = {'format':'bestvideo[height<=1080,ext=mp4]'}
                    ydl_opts={}
                    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                        info = ydl.extract_info(
                            'https://www.youtube.com/watch?v='+aid, download=False)
                        for st in info['formats']:
                            # print(st)
                            if st['format_note']:
                                # res=int(st['format_note'].replace('p',''))
                                if st['ext']=='mp4' and st['asr']:
                                    stream_url= st['url']
        if stream_url:
            threading.Thread(target=db_history.github_add,args=(aid,dict(source='youtube',episode=aid),gittoken,gitrepo,)).start()
            if isqueue:
                threading.Thread(target=db_yt_queue.github_remove,args=(aid,gittoken,gitrepo,)).start()
        return redirect(stream_url,permanent=True)
    else:
        return HttpResponse('Error')

def feed_yt_queue(request):
    if request:
        dj=request.build_absolute_uri().replace(request.path,'')
    else:
        dj=''
    base_url=dj+'/polls/get_yt_stream/'
    
    aids=db_yt_queue.load()

    root = minidom.Document()
    feed = root.createElement('feed')
    root.appendChild(feed)

    for aid in aids:
        if not aid:
            continue
        try:
            a=aids[aid]['response']
        except:
            yv=pytube.YouTube('?v='+aid)
            a=yv.vid_info['videoDetails']
        # title=rk.titlexml(a['title']).replace('&quot;','"')
        title=a['title']
        thumbnail='https://i.ytimg.com/vi/'+a['videoId']+'/hqdefault.jpg'

        item=addto(root,feed,'item',attr=dict(
            sdImg=thumbnail,
            hdImg=thumbnail
            ))

        addto(root,item,'title',title)
        addto(root,item,'contentId',aid)
        addto(root,item,'contentType','Episode')
        addto(root,item,'contentQuality','HD')
        addto(root,item,'streamFormat','mp4')
        media=addto(root,item,'media')
        url_args=pathargs(aid=a['videoId'],queue='1')
        addto(root,media,'streamUrl',base_url+url_args)
        desc=a['shortDescription']

        addto(root,item,'synopsis',
            desc
            )
        try:
            addto(root,item,'genres',', '.join(a['keywords']))
        except:
            addto(root,item,'genres','')

    xml_str = root.toprettyxml(indent ="  ",encoding='UTF-8',standalone='yes') 
    return HttpResponse(xml_str,content_type='text/xml')


def last_query_series(request):
    # global last_query
    if request:
        dj=request.build_absolute_uri().replace(request.path,'')
    else:
        dj=''
    base_url=dj+'/polls/get_flixhq_ep/'
    
    aids=db_flixhq.load()

    root = minidom.Document()
    feed = root.createElement('feed')
    root.appendChild(feed)

    for aid in last_query['series']:
        if not aid:
            continue
        istv=True if aid[0:2]=='tv' else False
        # print(aid)
        # if db_flixhq.isin(aid):
        try:
            #print(aid)
            a=aids[aid]['response']
            # print(a)
        except:
            try:
                a=last_query['series'][aid]['response']
            except:
                r=rq.get(apiconsu+'/movies/flixhq/info'+pathargs(id=aid))
                a=r.json()

        if istv:
            title=rk.titlexml(a['title'])
            thumbnail=a['image']

            item=addto(root,feed,'item',attr=dict(
                sdImg=thumbnail,
                hdImg=thumbnail
                ))

            addto(root,item,'title',title)
            addto(root,item,'contentId',aid)
            addto(root,item,'contentType','Season')
            addto(root,item,'contentQuality','HD')
            addto(root,item,'streamFormat','hls')
            media=addto(root,item,'media')
            addto(root,media,'streamUrl',base_url)
            addto(root,media,'subtitleUrl',dj+'/polls/get_flixhq_sub/')
            season=addto(root,media,'season',None)
            addto(root,item,'synopsis',
                ''
                )
            addto(root,item,'genres',', '.join(a['genres']))

            for e in a['episodes']:
                url_args=pathargs(eid=e['id'],aid=aid)
                addto(root,season,'episode',attr=dict(
                    # title='S'+str(e['season']).rjust(2,'0')+'E'+str(e['number']).rjust(2,'0'),
                    title='S'+str(e['season']).rjust(2,'0')+e['title'],
                    url=base_url+url_args,
                    subs=dj+'/polls/get_flixhq_sub/'+url_args
                    ))
        else:
            continue
            title=rk.titlexml(a['title'])
            thumbnail=a['image']

            item=addto(root,feed,'item',attr=dict(
                sdImg=thumbnail,
                hdImg=thumbnail
                ))

            addto(root,item,'title',title)
            addto(root,item,'contentId',aid)
            addto(root,item,'contentType','Episode')
            addto(root,item,'contentQuality','HD')
            addto(root,item,'streamFormat','hls')
            media=addto(root,item,'media')
            url_args=pathargs(eid=a['episodes'][0]['id'],aid=aid)
            addto(root,media,'streamUrl',base_url+url_args)
            addto(root,media,'subtitleUrl',dj+'/polls/get_flixhq_sub/'+url_args)
            # season=addto(root,media,'season',None)
            desc='Released: '+a['releaseDate']

            addto(root,item,'synopsis',
                desc
                )
            addto(root,item,'genres',', '.join(a['genres']))

    xml_str = root.toprettyxml(indent ="  ",encoding='UTF-8',standalone='yes') 
    return HttpResponse(xml_str,content_type='text/xml')
def history_anime(request):
    dj=request.build_absolute_uri().replace(request.path,'')
    base_url=dj+'/polls/get_ep/'


    dbo=db_history.github_download(gittoken,gitrepo)
    aids=db_flixhq.load()
    
    root = minidom.Document()
    feed = root.createElement('feed')
    root.appendChild(feed)
    
    ii=0
    for aid in reversed(dbo):
        if not aid:
            continue
        if dbo[aid]['source']!='gogo':
            continue
        ii+=1
        # if ii>30:
        #     dbo.pop(aid,None)
        try:
            a=aids[aid]['response']
        except:
            r=rq.get(apiurl+'/anime-details/'+aid)
            a=r.json()

            if 'error' in a:
                continue

        epid=dbo[aid]['episode']
        # epn=epid.split('-')[-1]
        
        tail=re.findall(r'-episode-[\d-]+',epid)[0]
        epn=tail.replace('-episode-','')

        title=rk.titlexml(a['animeTitle'])+' - Episode '+epn
        thumbnail=a['animeImg']

        item=addto(root,feed,'item',attr=dict(
            sdImg=thumbnail,
            hdImg=thumbnail
            ))

        addto(root,item,'title',title)
        addto(root,item,'contentId',aid+'+'+epid)
        addto(root,item,'contentType','Season')
        addto(root,item,'contentQuality','HD')
        addto(root,item,'streamFormat','hls')
        addto(root,item,'synopsis',a['synopsis'])
        addto(root,item,'genres',['SUB','DUB'][bool(aid[-3:].lower()=='dub')])

        media=addto(root,item,'media')
        addto(root,media,'streamUrl',base_url+'test')
        season=addto(root,media,'season',None)

        
        donow=False
        for e in reversed(a['episodesList']):
            if e['episodeId']==epid and donow==False:
                donow=True
            if donow:
                addto(root,season,'episode',attr=dict(
                    title='Episode '+e['episodeNum'],
                    url=base_url+e['episodeId']
                    ))
    xml_str = root.toprettyxml(indent ="  ",encoding='UTF-8',standalone='yes')
    return HttpResponse(xml_str,content_type='text/xml')
def history_series(request):
    dj=request.build_absolute_uri().replace(request.path,'')
    base_url=dj+'/polls/get_flixhq_ep/'

    
    dbo=db_history.github_download(gittoken,gitrepo)
    aids=db_flixhq_all.load()
    
    root = minidom.Document()
    feed = root.createElement('feed')
    root.appendChild(feed)
    do_gsave=False
    
    ii=0
    for aid in reversed(dbo):
        if not aid:
            continue
        if dbo[aid]['source']!='flixhq':
            continue
        istv=True if aid[0:2]=='tv' else False

        ii+=1
        # if ii>30:
        #     dbo.pop(aid,None)
        try:
            a=aids[aid]['response']
        except:
            r=rq.get(apiurl+'/anime-details/'+aid)
            a=r.json()

        epid=dbo[aid]['episode']

        if istv:
            ii+=1
            if 'error' in a:
                a=rq.get(apiconsu+'/movies/flixhq/info'+pathargs(id=aid)).json()
                aids[aid]={'response':a}
                do_gsave=True
            title=rk.titlexml(a['title'])

            thumbnail=a['image']

            item=addto(root,feed,'item',attr=dict(
                sdImg=thumbnail,
                hdImg=thumbnail
                ))

            addto(root,item,'contentId',aid+'+'+epid)
            addto(root,item,'contentType','Season')
            addto(root,item,'contentQuality','HD')
            addto(root,item,'streamFormat','hls')
            media=addto(root,item,'media')
            addto(root,media,'streamUrl',base_url)
            addto(root,media,'subtitleUrl',dj+'/polls/get_flixhq_sub/')
            season=addto(root,media,'season',None)
            addto(root,item,'synopsis',
                ''
                )
            addto(root,item,'genres',', '.join(a['genres']))

            donow=False
            for e in a['episodes']:
                if e['id']==epid and donow==False:
                    eptitle='S'+str(e['season']).rjust(2,'0')+e['title']
                    addto(root,item,'title',title+' - '+eptitle)
                    donow=True
                if donow:
                    url_args=pathargs(eid=e['id'],aid=aid)
                    addto(root,season,'episode',attr=dict(
                        # title='S'+str(e['season']).rjust(2,'0')+'E'+str(e['number']).rjust(2,'0'),
                        title='S'+str(e['season']).rjust(2,'0')+e['title'],
                        url=base_url+url_args,
                        subs=dj+'/polls/get_flixhq_sub/'+url_args
                        ))
        else:
            continue
            title=rk.titlexml(a['title'])
            thumbnail=a['image']

            item=addto(root,feed,'item',attr=dict(
                sdImg=thumbnail,
                hdImg=thumbnail
                ))

            addto(root,item,'title',title)
            addto(root,item,'contentId',aid)
            addto(root,item,'contentType','Episode')
            addto(root,item,'contentQuality','HD')
            addto(root,item,'streamFormat','hls')
            media=addto(root,item,'media')
            url_args=pathargs(eid=a['episodes'][0]['id'],aid=aid)
            addto(root,media,'streamUrl',base_url+url_args)
            addto(root,media,'subtitleUrl',dj+'/polls/get_flixhq_sub/'+url_args)
            # season=addto(root,media,'season',None)
            desc='Released: '+a['releaseDate']

            addto(root,item,'synopsis',
                desc
                )
            addto(root,item,'genres',', '.join(a['genres']))

    xml_str = root.toprettyxml(indent ="  ",encoding='UTF-8',standalone='yes')
    if do_gsave:
        threading.Thread(target=db_flixhq_all.github_save,args=(aids,gittoken,gitrepo)).start()
    return HttpResponse(xml_str,content_type='text/xml')

def view_yt_queue(request):
    sort='False'
    view=None
    if request.method == 'GET': # If the form is submitted
        ts=[]
        st=[]
        cs=[]
        fs=[]
        nfs=[]
        lens=[]
        aids=db_yt_queue.load()
        sort=request.GET.get('sort', None)
        sort='False' if not sort else sort
        
        view=request.GET.get('view', None)
        view='all' if not view else view

        if sort=='False':
            do=aids
        else:
            # do=sorted(aids)
            titles=[]
            for vid in aids:
                if vid:
                    titles.append((aids[vid]['response']['title'].lower(),vid))
                do=[]
                for t in sorted(titles):
                    do.append(t[1])
            # do={k: v for k, v in sorted(aids.items(), key=lambda item: item[1]['response']['title'].lower())}
        for aid in do:
            if aid:
                # if view=='series' and aid[0:2]!='tv':
                #     continue
                # elif view=='movies' and aid[0:2]=='tv':
                #     continue

                qi=aids[aid]['response']
                # print(qi)
                ts.append(qi['title'])
                st.append(qi['author'])
                thumb='https://i.ytimg.com/vi/'+qi['videoId']+'/hqdefault.jpg'
                cs.append(thumb)
                fs.append('')
                nfs.append('../removefrom_yt_queue/'+qi['videoId'])
                lens.append(short_h_m_s(int(qi['lengthSeconds'])))
                
    context ={
        'smode':'YouTube Queue',
        'sort':sort,
        'view':view,
        'list':zip(ts,st,cs,fs,nfs,lens),
    }
    return render(request, "favs.html",context)

def history_youtube(request):
    dj=request.build_absolute_uri().replace(request.path,'')
    base_url=dj+'/polls/get_yt_stream/'


    dbo=db_history.github_download(gittoken,gitrepo)
    aids=db_yt_queue.load()
    
    root = minidom.Document()
    feed = root.createElement('feed')
    root.appendChild(feed)
    
    ii=0
    for aid in reversed(dbo):
        if not aid:
            continue
        if dbo[aid]['source']!='youtube':
            continue
        ii+=1
        if ii>60:
            # dbo.pop(aid,None)
            break
        try:
            a=aids[aid]['response']
        except:
            yv=pytube.YouTube('?v='+dbo[aid]['episode'])
            try:
                a=yv.vid_info['videoDetails']
            except:
                # yv.bypass_age_gate()
                a=yv.vid_info['videoDetails']

            
        title=a['title']
        thumbnail='https://i.ytimg.com/vi/'+a['videoId']+'/hqdefault.jpg'

        item=addto(root,feed,'item',attr=dict(
            sdImg=thumbnail,
            hdImg=thumbnail
            ))

        addto(root,item,'title',title)
        addto(root,item,'contentId',aid)
        addto(root,item,'contentType','Episode')
        addto(root,item,'contentQuality','HD')
        addto(root,item,'streamFormat','mp4')
        media=addto(root,item,'media')
        url_args=pathargs(aid=a['videoId'])
        addto(root,media,'streamUrl',base_url+url_args)
        desc=a['shortDescription']

        addto(root,item,'synopsis',
            desc
            )
        try:
            addto(root,item,'genres',', '.join(a['keywords']))
        except:
            addto(root,item,'genres','')

    xml_str = root.toprettyxml(indent ="  ",encoding='UTF-8',standalone='yes')
    return HttpResponse(xml_str,content_type='text/xml')


threading.Thread(target=update_last_query).start()

def schedule_once(target,args=(),dt=0):
    def delayed_fun():
        time.sleep(dt)
        target(*args)
    threading.Thread(target=delayed_fun).start()


def launch_channel(request):
    roku='http://192.168.0.42:8060'
    # http://$ROKU_DEV_TARGET:8060/keypress/home
    # rq.post(roku+'/keypress/home')
    # rq.post(roku+'/keypress/home')
    # rq.post(roku+'/launch/dev')
    # schedule_once(rq.post,args=(roku+'/launch/dev',),dt=2)

    urlback=''
    s='''
<html>
<body text="#ffffff" style=" background-color: black;">
<head>
    <meta charset = "utf-8">
    <title>GeeksforGeeks Example</title>

    <!--CSS Code-->
    <style media = "screen">
        body {
            background: orange;
            overflow: hidden;
            color: white;
        }
        .GeeksForGeeks {
            text-align: center;
            background: #282923;
            font-size: 3.5vw;
            position: absolute;
            top: 1%;
            left: 1%;
            right: 1%;
        }
    </style>
</head>
 <div class = "GeeksForGeeks">
    '''
    # if ans=='Success!':
    #     s+='Check TeamViewer and wait for the computer to log on.<br>'
    # s+=url
    s+='<br>Returning...'
    s+='</div>'
    if urlback:
        s+='<meta http-equiv="refresh" content="3;url='+urlback+'" />'
    else:
        s+=r'''<script language="JavaScript" type="text/javascript">
    let xhr = new XMLHttpRequest();
    xhr.open("POST", "http://192.168.0.42:8060/keypress/home");
    xhr.send();

    let xhr2 = new XMLHttpRequest();
    xhr2.open("POST", "http://192.168.0.42:8060/keypress/home");
    setTimeout("xhr2.send()",500);

    let xhr3 = new XMLHttpRequest();
    xhr3.open("POST", "http://192.168.0.42:8060/launch/dev");
    setTimeout("xhr3.send()",1000);

    setTimeout("window.history.go(-1)",1500);

</script>
    '''
    s+='</body></html>'

    # return s
    return HttpResponse(s)



def tflixreq(url,result,index):
    print('started:',url)
    r=rq.get(url)
    rj=r.json()

    if 'error' in rj:
        time.sleep(.7)
        r=rq.get(url)
        rj=r.json()


    result[index] = rj
    print('finished:',url)

flixhome_update_finished=[True]
threads={}
def update_feed_flixhq_home(request=None):
    global threads

    if not flixhome_update_finished[0]:
        return
    flixhome_update_finished[0]=False
    
    # dbh=db_flixhq_home.load()
    db_flixhq_home.wipe()
    dbh=db_flixhq_home.load()
    db_flixhq_home.github_save(dbh,gittoken,gitrepo)

    #dbo=db_flixhq_all.github_download(gittoken,gitrepo)
    db_flixhq_all.wipe()
    dbo=db_flixhq_all.load()

    

    do_save=bool(abs(time.time()-dbo['']['saved'])/60>30)
    do_save=True
    print((time.time()-dbo['']['saved'])/60)
    dboo=dbo.copy()
    headers = {"User-Agent": "Mozilla/5.0 (X11; CrOS x86_64 12871.102.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.141 Safari/537.36"}
    r=rq.get('https://flixhq.to/home')
    bs = BeautifulSoup(r.text.replace('block_area block_area_home section-id-01','block_area block_area_home section-id-02'),features='lxml')
    for sect in bs.find_all('section',{'class':'block_area block_area_home section-id-02'}):
        sect_title=sect.find_all('h2',{'class':'cat-heading'})[0].text
        if sect_title=='Coming Soon':
            continue
        print(sect_title)
        
        sect_vids={}
        result={}
        threads={}

        for a in sect.find_all('div', {"class": "flw-item"}):
            # print('-'*20)
            det=a.find_all('h3',{'class':'film-name'})[0].find_all('a')[0]
            aid=det['href'].lstrip('/')
            # print(bool(aid in dbo),aid)
            try:
                #print(apiconsu+'/movies/flixhq/info'+pathargs(id=aid))
                if aid[0:6]=='movie/' and not aid in dbo:
                    #print(aid,'---------')
                    threads[aid]=threading.Thread(target=tflixreq, args=(apiconsu+'/movies/flixhq/info'+pathargs(id=aid), result, aid,))
                    threads[aid].start()
                    # r=rq.get(apiconsu+'/movies/flixhq/info'+pathargs(id=aid))
                    # rj=r.json()
                    # print(rj)
                    # if not 'error' in rj:
                    #     dbo[aid]={'response':rj}
                elif aid[0:6]=='movie/':
                    pass
                else:
                    if do_save or not aid in dbo:
                        #print(aid,'---------')
                        threads[aid]=threading.Thread(target=tflixreq, args=(apiconsu+'/movies/flixhq/info'+pathargs(id=aid), result, aid,))
                        threads[aid].start()
                        # r=rq.get(apiconsu+'/movies/flixhq/info'+pathargs(id=aid))
                        # rj=r.json()
                        # if not 'error' in rj:
                        #     dbo[aid]={'response':rj}

            except:
                traceback.print_exc()
            time.sleep(.3)
            
            # sect_vids[aid]=dbo[aid]

            # try:
            #     sect_vids[aid]=dbo[aid]
            # except:
            #     pass
            
            # print(det['href'].lstrip('/'))
            # print(det['title'])

            # sub=' '.join([fdi.text for fdi in a.find_all('span',{'class':'fdi-item'})])
            # print(sub)
            # img=a.find_all('img')[0]
            # print(img['data-src'])
        #print(threads)
        for aid in threads:
            threads[aid].join()

        for aid in result:
            rj=result[aid]
            if not 'error' in rj:
                dbo[aid]={'response':rj}
                sect_vids[aid]=dbo[aid]
                # try:
                    
                # except:
                #     pass

        dbh[sect_title.lower().strip()]=sect_vids

    if dboo!=dbo:
        print('updating db_flixhq_all')
        # db_flixhq_all.github_save(dbo,gittoken,gitrepo)
        threading.Thread(target=db_flixhq_all.github_save,args=(dbo,gittoken,gitrepo)).start()
    
    db_flixhq_home.save(dbh)
    flixhome_update_finished[0]=True

    threading.Thread(target=db_flixhq_home.github_save,args=(dbh,gittoken,gitrepo)).start()
    if request:
        return HttpResponse('db_flixhq_home updated!')
    else:
        print('db_flixhq_home updated!')



def flixhq_trending(request):
    while not flixhome_update_finished[0]:
        time.sleep(.3)

    if request:
        dj=request.build_absolute_uri().replace(request.path,'')
    else:
        dj=''

    dbo=db_flixhq_home.load()['trending']

    base_url=dj+'/polls/get_flixhq_ep/'
    root = minidom.Document()
    feed = root.createElement('feed')
    root.appendChild(feed)
    
    for aid in dbo:
        if not aid:
            continue
        istv=True if aid[0:2]=='tv' else False
        #print(aid)
        # print(dbo[aid].keys())
        a=dbo[aid]['response']

        if istv:
            title=rk.titlexml(a['title'])
            thumbnail=a['image']

            item=addto(root,feed,'item',attr=dict(
                sdImg=thumbnail,
                hdImg=thumbnail
                ))

            addto(root,item,'title',title)
            addto(root,item,'contentId',aid)
            addto(root,item,'contentType','Season')
            addto(root,item,'contentQuality','HD')
            addto(root,item,'streamFormat','hls')
            media=addto(root,item,'media')
            addto(root,media,'streamUrl',base_url)
            addto(root,media,'subtitleUrl',dj+'/polls/get_flixhq_sub/')
            season=addto(root,media,'season',None)
            addto(root,item,'synopsis',
                ''
                )
            addto(root,item,'genres',', '.join(a['genres']))

            for e in a['episodes']:
                url_args=pathargs(eid=e['id'],aid=aid)
                addto(root,season,'episode',attr=dict(
                    # title='S'+str(e['season']).rjust(2,'0')+'E'+str(e['number']).rjust(2,'0'),
                    title='S'+str(e['season']).rjust(2,'0')+e['title'],
                    url=base_url+url_args,
                    subs=dj+'/polls/get_flixhq_sub/'+url_args
                    ))
        else:
            title=rk.titlexml(a['title'])
            thumbnail=a['image']

            item=addto(root,feed,'item',attr=dict(
                sdImg=thumbnail,
                hdImg=thumbnail
                ))

            addto(root,item,'title',title)
            addto(root,item,'contentId',aid)
            addto(root,item,'contentType','Episode')
            addto(root,item,'contentQuality','HD')
            addto(root,item,'streamFormat','hls')
            media=addto(root,item,'media')
            url_args=pathargs(eid=a['episodes'][0]['id'],aid=aid)
            addto(root,media,'streamUrl',base_url+url_args)
            addto(root,media,'subtitleUrl',dj+'/polls/get_flixhq_sub/'+url_args)
            # season=addto(root,media,'season',None)
            desc='Released: '+a['releaseDate']

            addto(root,item,'synopsis',
                desc
                )
            addto(root,item,'genres',', '.join(a['genres']))

    xml_str = root.toprettyxml(indent ="  ",encoding='UTF-8',standalone='yes') 
    return HttpResponse(xml_str,content_type='text/xml')

def flixhq_latest_series(request):
    while not flixhome_update_finished[0]:
        time.sleep(.3)

    if request:
        dj=request.build_absolute_uri().replace(request.path,'')
    else:
        dj=''

    dbo=db_flixhq_home.load()['latest tv shows']
    #print(dbo.keys())
    base_url=dj+'/polls/get_flixhq_ep/'
    root = minidom.Document()
    feed = root.createElement('feed')
    root.appendChild(feed)

    
    for aid in dbo:
        if not aid:
            continue
        istv=True if aid[0:2]=='tv' else False
        #print(aid)
        #print(dbo[aid].keys())
        a=dbo[aid]['response']

        if istv:
            title=rk.titlexml(a['title'])
            thumbnail=a['image']

            item=addto(root,feed,'item',attr=dict(
                sdImg=thumbnail,
                hdImg=thumbnail
                ))

            addto(root,item,'title',title)
            addto(root,item,'contentId',aid)
            addto(root,item,'contentType','Season')
            addto(root,item,'contentQuality','HD')
            addto(root,item,'streamFormat','hls')
            media=addto(root,item,'media')
            addto(root,media,'streamUrl',base_url)
            addto(root,media,'subtitleUrl',dj+'/polls/get_flixhq_sub/')
            season=addto(root,media,'season',None)
            addto(root,item,'synopsis',
                ''
                )
            addto(root,item,'genres',', '.join(a['genres']))

            for e in a['episodes']:
                url_args=pathargs(eid=e['id'],aid=aid)
                addto(root,season,'episode',attr=dict(
                    # title='S'+str(e['season']).rjust(2,'0')+'E'+str(e['number']).rjust(2,'0'),
                    title='S'+str(e['season']).rjust(2,'0')+e['title'],
                    url=base_url+url_args,
                    subs=dj+'/polls/get_flixhq_sub/'+url_args
                    ))
        else:
            title=rk.titlexml(a['title'])
            thumbnail=a['image']

            item=addto(root,feed,'item',attr=dict(
                sdImg=thumbnail,
                hdImg=thumbnail
                ))

            addto(root,item,'title',title)
            addto(root,item,'contentId',aid)
            addto(root,item,'contentType','Episode')
            addto(root,item,'contentQuality','HD')
            addto(root,item,'streamFormat','hls')
            media=addto(root,item,'media')
            url_args=pathargs(eid=a['episodes'][0]['id'],aid=aid)
            addto(root,media,'streamUrl',base_url+url_args)
            addto(root,media,'subtitleUrl',dj+'/polls/get_flixhq_sub/'+url_args)
            # season=addto(root,media,'season',None)
            desc='Released: '+a['releaseDate']

            addto(root,item,'synopsis',
                desc
                )
            addto(root,item,'genres',', '.join(a['genres']))

    xml_str = root.toprettyxml(indent ="  ",encoding='UTF-8',standalone='yes') 
    return HttpResponse(xml_str,content_type='text/xml')

def flixhq_latest_movies(request):
    while not flixhome_update_finished[0]:
        time.sleep(.3)

    if request:
        dj=request.build_absolute_uri().replace(request.path,'')
    else:
        dj=''

    dbo=db_flixhq_home.load()['latest movies']
    #print(dbo.keys())
    base_url=dj+'/polls/get_flixhq_ep/'
    root = minidom.Document()
    feed = root.createElement('feed')
    root.appendChild(feed)
    
    for aid in dbo:
        if not aid:
            continue
        istv=True if aid[0:2]=='tv' else False
        #print(aid)
        #print(dbo[aid].keys())
        a=dbo[aid]['response']

        if istv:
            title=rk.titlexml(a['title'])
            thumbnail=a['image']

            item=addto(root,feed,'item',attr=dict(
                sdImg=thumbnail,
                hdImg=thumbnail
                ))

            addto(root,item,'title',title)
            addto(root,item,'contentId',aid)
            addto(root,item,'contentType','Season')
            addto(root,item,'contentQuality','HD')
            addto(root,item,'streamFormat','hls')
            media=addto(root,item,'media')
            addto(root,media,'streamUrl',base_url)
            addto(root,media,'subtitleUrl',dj+'/polls/get_flixhq_sub/')
            season=addto(root,media,'season',None)
            addto(root,item,'synopsis',
                ''
                )
            addto(root,item,'genres',', '.join(a['genres']))

            for e in a['episodes']:
                url_args=pathargs(eid=e['id'],aid=aid)
                addto(root,season,'episode',attr=dict(
                    # title='S'+str(e['season']).rjust(2,'0')+'E'+str(e['number']).rjust(2,'0'),
                    title='S'+str(e['season']).rjust(2,'0')+e['title'],
                    url=base_url+url_args,
                    subs=dj+'/polls/get_flixhq_sub/'+url_args
                    ))
        else:
            title=rk.titlexml(a['title'])
            thumbnail=a['image']

            item=addto(root,feed,'item',attr=dict(
                sdImg=thumbnail,
                hdImg=thumbnail
                ))

            addto(root,item,'title',title)
            addto(root,item,'contentId',aid)
            addto(root,item,'contentType','Episode')
            addto(root,item,'contentQuality','HD')
            addto(root,item,'streamFormat','hls')
            media=addto(root,item,'media')
            url_args=pathargs(eid=a['episodes'][0]['id'],aid=aid)
            addto(root,media,'streamUrl',base_url+url_args)
            addto(root,media,'subtitleUrl',dj+'/polls/get_flixhq_sub/'+url_args)
            # season=addto(root,media,'season',None)
            desc='Released: '+a['releaseDate']

            addto(root,item,'synopsis',
                desc
                )
            addto(root,item,'genres',', '.join(a['genres']))

    xml_str = root.toprettyxml(indent ="  ",encoding='UTF-8',standalone='yes') 
    return HttpResponse(xml_str,content_type='text/xml')

# threading.Thread(target=update_feed_flixhq_home).start()