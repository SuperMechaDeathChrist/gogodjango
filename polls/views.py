from django.shortcuts import render,redirect
from django.urls import reverse
import requests as rq
import threading
# Create your views here.
from django.http import HttpResponse
import json
import re
import random
import unicodedata
import rklpy_lib as rk
import traceback

from xml.dom import minidom

# import imdb
# ia = imdb.Cinemagoer()

import sys
sys.path.append('../')
import db
import db_flixhq
from db import CaseInsensitiveDict

apiurl='https://gogo4rokuapi.herokuapp.com'
apiconsu='https://rokuconsumet.herokuapp.com'

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
        stream_url=streamj['sources'][0]['file']

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
        <categoryLeaf title="DUB" description="" feed="{dj}/polls/recent_anime_dub/"/>
        <categoryLeaf title="CHINESE" description="" feed="{dj}/polls/recent_anime_dub/"/>
    </category>
    
    <category title="Favorites" description="Series/movies" sd_img="pkg:/images/Favorites.png" hd_img="pkg:/images/Favorites.png">
        <categoryLeaf title="Favorite Animes" description="" feed="{dj}/polls/favorite_anime/"/>
        <categoryLeaf title="Favorite Series" description="" feed="{dj}/polls/favorite_series/"/>
    </category>
 </categories>
'''
    return HttpResponse(ans,content_type='text/xml')

def recent_gogo(dj,rtype='/recent-release'):
    # dj=request.build_absolute_uri().replace(request.path,'')
    root = minidom.Document()
    feed = root.createElement('feed')
    # rss.setAttribute('xmlns:media',"http://search.yahoo.com/mrss/") 
    # rss.setAttribute('version','2.0')
    root.appendChild(feed)
    # addto(root,feed,'resultLength','4')
    r=rq.get(apiurl+rtype)
    rj=r.json()
    for a in rj:
        title=rk.titlexml(a['animeTitle'])
        desc='Epidose '+a['episodeNum']
        url=dj+'/polls/get_ep/'+a['episodeId']
        thumbnail=a['animeImg']

        # item=root.createElement('item',attr)
        item=addto(root,feed,'item',attr=dict(
            sdImg=thumbnail,
            hdImg=thumbnail
            ))

        addto(root,item,'title',desc+' - '+title)
        addto(root,item,'contentId',a['episodeId'])
        addto(root,item,'contentType','Episode')
        addto(root,item,'contentQuality','HD')
        addto(root,item,'streamFormat','hls')
        media=root.createElement('media')
        item.appendChild(media)
        addto(root,media,'streamUrl',url)
        addto(root,item,'synopsis',desc)
        addto(root,item,'genres',a['subOrDub'])



    xml_str = root.toprettyxml(indent ="  ") 
    # return HttpResponse(xml_str,content_type='text/xml')
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
        if db.isin(aid):
            #print(aid)
            a=aids[aid]['response']
            # print(a)
        else:
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
        media=addto(root,item,'media')
        addto(root,media,'streamUrl',base_url+'test')
        season=addto(root,media,'season',None)
        addto(root,item,'synopsis',
            a['synopsis']
            )
        addto(root,item,'genres',['SUB','DUB'][bool(aid[-3:].lower()=='dub')])

        for e in reversed(a['episodesList']):
            addto(root,season,'episode',attr=dict(
                title='Episode '+e['episodeNum'],
                # text='Episode '+e['episodeNum'],
                url=base_url+e['episodeId']
                ))
    xml_str = root.toprettyxml(indent ="  ") 
    return HttpResponse(xml_str,content_type='text/xml')

def get_anime(request,aid):
    dj=request.build_absolute_uri().replace(request.path,'')
    base_url=dj+'/polls/get_ep/'
    root = minidom.Document()
    feed = root.createElement('feed')
    root.appendChild(feed)


    xml_str = root.toprettyxml(indent ="  ") 
    return HttpResponse(xml_str,content_type='text/xml')

def update_fav_anime():
    print('+'*20)
    print('updating fav anime')
    print('+'*20)
    # aids=db.load()
    aids=db.github_download(gittoken,gitrepo,do_save=True)
    if len(aids)<2:
        aids=['accel-world-dub',
            'overlord-iv']
    for aid in aids:
        if not aid:
            continue
        if '/category/' in aid:
            aid=aid.split('/category/')[-1]
        r=rq.get(apiurl+'/anime-details/'+aid)
        a=r.json()        

        # title=rk.titlexml(a['animeTitle'])
        # thumbnail=a['animeImg']
        db.add(aid,dict(
            response=a,
            ))
    db.github_save(db.load(),gittoken,gitrepo)

def update_fav_series():
    print('+'*20)
    print('updating fav series')
    print('+'*20)
    aids=db_flixhq.github_download(gittoken,gitrepo,do_save=True)
    if len(aids)<2:
        aids=[
        'tv/watch-love-death-and-robots-42148'
        ]
    for aid in aids:
        if not aid:
            continue
        r=rq.get(apiconsu+'/movies/flixhq/info'+pathargs(id=aid))
        a=r.json()

        # ia.search_movie(a['title'])
        db_flixhq.add(aid,dict(
            response=a,
            ))
    db_flixhq.github_save(db_flixhq.load(),gittoken,gitrepo)


def addto_fav_anime(request,aid):
    try:
        if not aid:
            raise ValueError
        r=rq.get(apiurl+'/anime-details/'+aid)
        a=r.json()
        # db.add(aid,
        #     dict(response=a)
        #     )
        db.github_add(aid,dict(response=a),gittoken,gitrepo)

        if request:
            return HttpResponse("Success: added "+aid)
        else:
            print("Success: added "+aid)

    except:
        if request:
            return HttpResponse("Failiure: not added "+aid)
        else:
            print("Failiure: not added "+aid)
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
        if request: return HttpResponse("Success: added "+aid)
    except:
        traceback.print_exc()
        if request: return HttpResponse("Failiure: not added "+aid)
def removefrom_fav_anime(request,aid):
    if db.github_remove(aid,gittoken,gitrepo):
        if request: return HttpResponse("Success: removed "+aid)
    else:
        if request: return HttpResponse("Failiure: not removed "+aid)
def removefrom_fav_series(request,ctype,id):
    aid=ctype+'/'+id
    if db_flixhq.github_remove(aid,gittoken,gitrepo):
        if request: return HttpResponse("Success: removed "+aid)
    else:
        if request: return HttpResponse("Failiure: not removed "+aid)

def get_flixhq_ep(request):
    eid=request.GET.get('eid', None)
    aid=request.GET.get('aid', None)
    if eid and aid:
        # ?eid=939832&aid=tv%2Fwatch-love-death-and-robots-42148
        eid=request.GET.get('eid', None)
        aid=request.GET.get('aid', None)
        # print(eid)
        # print(aid)
        er=rq.get(apiconsu+'/movies/flixhq/watch'+pathargs(episodeId=eid,server='vidcloud',mediaId=aid))
        erj=er.json()
        stream_url=erj['sources'][0]['url']

        return redirect(stream_url,permanent=True)
    else:
        url='http://commondatastorage.googleapis.com/gtv-videos-bucket/sample/BigBuckBunny.mp4'
        return redirect(url,permanent=True)



    return HttpResponse(request.path)

def favorite_series(request):
    dj=request.build_absolute_uri().replace(request.path,'')
    base_url=dj+'/polls/get_flixhq_ep/'
    
    aids=db_flixhq.load()

    root = minidom.Document()
    feed = root.createElement('feed')
    root.appendChild(feed)

    for aid in aids:
        print(aid)

    for aid in aids:
        if not aid:
            continue
        if db_flixhq.isin(aid):
            #print(aid)
            a=aids[aid]['response']
            # print(a)
        else:
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
        season=addto(root,media,'season',None)
        addto(root,item,'synopsis',
            ''
            )
        addto(root,item,'genres',', '.join(a['genres']))

        for e in a['episodes']:
            addto(root,season,'episode',attr=dict(
                # title='S'+str(e['season']).rjust(2,'0')+'E'+str(e['number']).rjust(2,'0'),
                title='S'+str(e['season']).rjust(2,'0')+e['title'],
                url=base_url+pathargs(eid=e['id'],aid=aid)
                ))
    xml_str = root.toprettyxml(indent ="  ") 
    return HttpResponse(xml_str,content_type='text/xml')

# db.wipe()
# update_fav_anime()
# addto_fav_anime(None,'bastard-ankoku-no-hakaishin-ona-dub')
# db.printdb()