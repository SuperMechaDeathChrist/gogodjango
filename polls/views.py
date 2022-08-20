import sys
sys.path.append('../')
from django.shortcuts import render,redirect
from django.urls import reverse
import requests as rq
import threading
from vtt_to_srt import str_vtt_to_srt
# Create your views here.
from django.http import HttpResponse, JsonResponse
import json
import re
import random
import unicodedata
import rklpy_lib as rk
import traceback

from api.settings import last_query,series_ep_cache

from xml.dom import minidom

# import imdb
# ia = imdb.Cinemagoer()
import db
import db_flixhq
from db import CaseInsensitiveDict

apiurl='https://gogo4rokuapi.herokuapp.com'
# apiconsu='https://rokuconsumet.herokuapp.com'
apiconsu='https://consumet-api.herokuapp.com'

from cryptography.fernet import Fernet
key=b'wnuSKeQm1WLsf0qtmWVyoknqEhvrNXqj1RKewiwJFDE='
encMessage=b'gAAAAABi7tt3uuCl4P2d_m1JpvKUZuTBK7SMGuJqlJVRTIhsFhUFjLCe_kf2veI7iWNuEZpT2jCYhJE7MBhV990S4fu4iS81zpb29e41MAleVgIdZT6xSe5y6kcfTzkM_MW81n9cU08O'
fernet = Fernet(key)
gittoken = fernet.decrypt(encMessage).decode()

gitrepo="SuperMechaDeathChrist/gogodjango"
#

def pathargs(**d):
    ans='?'
    for k in d:
        ans+=k+'='+rq.utils.quote(d[k],safe='')+'&'
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
                ts.append(qi['title'])
                st.append('['+qi['releaseDate']+']')
                cs.append(qi['image'])
                fs.append('../addto_fav/'+qi['id'])
                nfs.append('../removefrom_fav/'+qi['id'])

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
        'list':zip(ts,st,cs,fs,nfs),
    }
    return render(request, "favs.html",context)
def search_fav_anime(request):
    sort='False'
    view=None
    if request.method == 'GET': # If the form is submitted
        ts=[]
        st=[]
        cs=[]
        fs=[]
        nfs=[]
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
        'list':zip(ts,st,cs,fs,nfs),
    }
    return render(request, "favs.html",context)

def search_anime(request):
    global last_query
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
        if search_query:
            print(search_query)
            # queryurl=apiurl+'/search'+pathargs(keyw=search_query)
            queryurl=apiconsu+'/anime/gogoanime/'+rq.utils.quote(search_query,safe='')
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

                    ts.append(qi['title'])
                    st.append('['+qi['releaseDate']+']')
                    cs.append(qi['image'])
                    fs.append('../addto_fav/'+qi['id'])
                    nfs.append('../removefrom_fav/'+qi['id'])

                    last_query['animes'][qi['id']]=False
                    threading.Thread(target=_down_query_response,args=(
                        apiurl+'/anime-details/'+qi['id'],
                        qi['id'],
                        'animes',
                        )).start()




    context ={
        #"data":"Gfg is the best",
        'nrslts':len(ts),
        'smode':'Search Anime',
        'lastq':search_query,
        'list':zip(ts,st,cs,fs,nfs),
    }

    # return response with template and context
    # return render(request, "geeks.html", context)
    # print(last_query['animes'])
    return render(request, "search.html",context)

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
        if search_query:
            print(search_query)
            # queryurl=apiurl+'/search'+pathargs(keyw=search_query)
            queryurl=apiconsu+'/movies/flixhq/'+rq.utils.quote(search_query,safe='')
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

                    last_query['series'][qi['id']]=False
                    threading.Thread(target=_down_query_response,args=(
                        apiconsu+'/movies/flixhq/info'+pathargs(id=qi['id']),
                        qi['id'],
                        'series',
                        )).start()




    context ={
        #"data":"Gfg is the best",
        'smode':'Search Movies/TV',
        'nrslts':len(ts),
        'lastq':search_query,
        'list':zip(ts,st,cs,fs,nfs),
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
        stream_r=rq.get(apiurl+'/vidcdn/watch/'+ep)
        streamj=stream_r.json()
        if not 'error' in streamj:
            stream_url=streamj['sources'][0]['file']
        else:
            epn=ep.split('-')[-1]
            aid=ep.replace('-episode-'+epn,'')
            aids=db.load()
            try:
                a=aids[aid]['response']
            except:
                r=rq.get(apiurl+'/anime-details/'+aid)
                a=r.json()
            for e in a['episodesList']:
                nepn=e['episodeId'].split('-')[-1]
                if nepn==epn:
                    stream_r=rq.get(apiurl+'/vidcdn/watch/'+e['episodeId'])
                    streamj=stream_r.json()
                    stream_url=streamj['sources'][0]['file']
                    break

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

    aids=[
    'accel-world-dub',
    'overlord-iv',
    'https://gogoanime.lu/category/dungeon-ni-deai-wo-motomeru-no-wa-machigatteiru-darou-ka-iv',
    'high-school-dxd-dub',#12
    'https://gogoanime.gg/category/high-school-dxd-new-dub',#13
    'https://gogoanime.gg/category/high-school-dxd-born-dub',#15
    'high-school-dxd-hero-dub',#18
    'https://gogoanime.gg/category/high-school-dxd-specials-ova',
    'https://gogoanime.gg/category/high-school-dxd-specials',
    'https://gogoanime.gg/category/highschool-dxd-born-specials'
    'https://gogoanime.gg/category/highschool-dxd-born-yomigaerarenai-pheonix'
    



    ]
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


def categories(request):
    x=threading.Thread(target=update_fav_anime)
    x.start()
    y=threading.Thread(target=update_fav_series)
    y.start()
    # with open(r"C:\c\Python_projects\anime_site\api\polls\categories.xml", 'r',encoding='utf-8') as fid:
    #     ans=fid.read()
    dj=request.build_absolute_uri().replace(request.path,'')
    ans=f'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<categories>

      <!-- banner_ad: optional element which displays an at the top level category screen -->
      <banner_ad sd_img="https://devtools.web.roku.com/videoplayer/images/missing.png" hd_img="https://devtools.web.roku.com/videoplayer/images/missing.png"/>

     <category title="Anime" description="Gogoanime" sd_img="pkg:/images/gogoanime.jpg" hd_img="pkg:/images/gogoanime.jpg">
        <categoryLeaf title="-Recent release-" description="" feed="{dj}/polls/recent_anime/"/>
        <categoryLeaf title="Top airing" description="" feed="{dj}/polls/top_airing_anime/"/>
        <categoryLeaf title="DUB" description="" feed="{dj}/polls/recent_anime_dub/"/>
        <categoryLeaf title="CHINESE" description="" feed="{dj}/polls/recent_anime_chinese/"/>
    </category>
    
    <category title="Favorite Movies and TV" description="Series/movies" sd_img="pkg:/images/Favorites.png" hd_img="pkg:/images/Favorites.png">
        <categoryLeaf title="Favorite Movies" description="" feed="{dj}/polls/favorite_movies/"/>
        <categoryLeaf title="Favorite Series" description="" feed="{dj}/polls/favorite_series/"/>
    </category>
    <category title="Favorite Animes" description="Animes/OVAs/Anime movies" sd_img="pkg:/images/Favorite_anime" hd_img="pkg:/images/Favorite_anime.png">
        <categoryLeaf title="Favorite Animes" description="" feed="{dj}/polls/favorite_anime/"/>
    </category>
    <category title="Search" description="https://rb.gy/8bz69s" sd_img="pkg:/images/qrsearch.png" hd_img="pkg:/images/qrsearch.png">
        <categoryLeaf title="Last searched series" description="" feed="{dj}/polls/last_query_series/"/>
        <categoryLeaf title="Last searched animes" description="" feed="{dj}/polls/last_query_animes/"/>
    </category>
 </categories>
'''
    return HttpResponse(ans,content_type='text/xml')

def recent_gogo(dj,rtype='/recent-release'):
    r=rq.get(apiurl+rtype)
    rj=r.json()

    base_url=dj+'/polls/get_ep/'

    root = minidom.Document()
    feed = root.createElement('feed')
    root.appendChild(feed)
    for a in rj:
        title=rk.titlexml(a['animeTitle'])
        desc='Epidose '+a['episodeNum']
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
def _down_response(curl,aid,dbid):
    global series_results,anime_results
    #
    try:
        # curl=apiconsu+'/movies/flixhq/info'+pathargs(id=aid)
        # print(curl)
        r=rq.get(curl)
        a=r.json()

        if dbid=='flixhq':
            series_results[aid]=dict(response=a)
        elif dbid=='gogoanime':
            anime_results[aid]=dict(response=a)
        print(curl)
    except:
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
    global series_results
    print('+'*20)
    print('updating fav series')
    print('+'*20)
    aids=db_flixhq.github_download(gittoken,gitrepo,do_save=True)
    # if len(aids)<2:
    #     aids=[
    #     'tv/watch-love-death-and-robots-42148'
    #     ]

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
            ts.append(threading.Thread(target=_down_response,args=(apiconsu+'/movies/flixhq/info'+pathargs(id=aid),aid,'flixhq',)))
            ts[-1].start()
    for tti in ts:
        tti.join()

    for k in series_results:
        db_flixhq.add(k,series_results[k])
    db_flixhq.github_save(db_flixhq.load(),gittoken,gitrepo)
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
        db.github_add(aid,dict(response=a),gittoken,gitrepo)

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

# def addto_fav(request,aid):
#     if not aid:
#         raise ValueError

def _html_added(ans,added,aid,urlback='../../search'):
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
    s+='<br>Returning in 3 seconds...'
    s+='</div>'
    #s+='<meta http-equiv="refresh" content="4;url='+urlback+'" />'
    s+=r'''<script language="JavaScript" type="text/javascript">
        setTimeout("window.history.go(-1)",3000);
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
        db_flixhq.github_add(aid,dict(response=a),gittoken,gitrepo)
        # if request: return HttpResponse("Success: added "+aid)
        if request: return HttpResponse(_html_added('Success!','added',aid))
    except:
        traceback.print_exc()
        # if request: return HttpResponse("Failiure: not added "+aid)
        if request: return HttpResponse(_html_added('Failiure!','not added',aid))
def removefrom_fav_anime(request,aid):
    if db.github_remove(aid,gittoken,gitrepo):
        # if request: return HttpResponse("Success: removed "+aid)
        if request: return HttpResponse(_html_added('Success!','removed',aid))
    else:
        # if request: return HttpResponse("Failiure: not removed "+aid)
        if request: return HttpResponse(_html_added('Failiure!','not removed',aid))
def removefrom_fav_series(request,ctype,id):
    aid=ctype+'/'+id
    if db_flixhq.github_remove(aid,gittoken,gitrepo):
        # if request: return HttpResponse("Success: removed "+aid)
        if request: return HttpResponse(_html_added('Success!','removed',aid))
    else:
        # if request: return HttpResponse("Failiure: not removed "+aid)
        if request: return HttpResponse(_html_added('Failiure!','not removed',aid))

def get_flixhq_ep(request):
    global series_ep_cache
    eid=request.GET.get('eid', None)
    aid=request.GET.get('aid', None)
    if eid and aid:
        # ?eid=939832&aid=tv%2Fwatch-love-death-and-robots-42148
        eid=request.GET.get('eid', None)
        aid=request.GET.get('aid', None)
        # print(eid)
        # print(aid)

        url_args=pathargs(episodeId=eid,server='vidcloud',mediaId=aid)

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


def last_query_series(request):
    global last_query
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

# db.wipe()
# update_fav_anime()
# addto_fav_anime(None,'bastard-ankoku-no-hakaishin-ona-dub')
# db.printdb()