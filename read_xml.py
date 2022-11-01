from lxml import etree
from io import StringIO, BytesIO
import re
from datetime import datetime


def time_ago(time=False):
    """
    Get a datetime object or a int() Epoch timestamp and return a
    pretty string like 'an hour ago', 'Yesterday', '3 months ago',
    'just now', etc
    Modified from: http://stackoverflow.com/a/1551394/141084
    """
    now = datetime.utcnow()
    if type(time) is int:
        diff = now - datetime.fromtimestamp(time)
    elif type(time) is float:
          diff = now - datetime.fromtimestamp(time)
    elif isinstance(time,datetime):
        diff = now - time
    elif not time:
        diff = now - now
    else:
        raise ValueError('invalid date %s of type %s' % (time, type(time)))
    second_diff = diff.seconds
    day_diff = diff.days
    # day_diff=round(day_diff)

    if day_diff < 0:
        return ''

    if day_diff == 0:
        if second_diff < 10:
            return "just now"
        if second_diff < 60:
            return str(second_diff) + " seconds ago"
        if second_diff < 120:
            return  "a minute ago"
        if second_diff < 3600:
            return str( second_diff / 60 ) + " minutes ago"
        if second_diff < 7200:
            return "an hour ago"
        if second_diff < 86400:
            return str( second_diff / 3600 ) + " hours ago"
    if day_diff == 1:
        return "Yesterday"
    if day_diff < 7:
        # return str(day_diff) + " days ago"
        return str(int(round(day_diff,1))) + " days ago"
    if day_diff < 31:
        # return str(day_diff/7) + " weeks ago"
        # return str(int(round(day_diff/7,1))) + " weeks ago"
        ans=int(round(day_diff/7,1))
        if ans>1:
            return str(ans) + " weeks ago"
        else:
            return str(ans) + " week ago"
    if day_diff < 365:
        # return str(day_diff/30) + " months ago"
        # return str(int(round(day_diff/30,1))) + " months ago"
        ans=int(round(day_diff/30,1))
        if ans>1:
            return str(ans) + " months ago"
        else:
            return str(ans) + " month ago"
    # return str(day_diff/365) + " years ago"
    ans=int(round(day_diff/365,1))
    if ans>1:
        return str(ans) + " years ago"
    else:
        return str(ans) + " year ago"

def remove_tag(tag,s):
    return s.replace(f'<{tag}>','').replace(f'</{tag}>','').strip()

# with open('videos.xml',encoding='utf-8') as fid:
#   # xml=fid.read()
#   # tree = etree.parse(StringIO(fid))
#   # tree=etree.fromstring(fid.read())
#   s=fid.read()

# print(s)
# ans=re.findall(r'<entry>.*</entry>',s)
# pat=r'(?<=<entry>)[\n]+.+?(?=/)'

URL_REGEX=r'https?:[^\n^"^\?]*'
# vids={}

def read_yt_xml_channel_feed(s):

    vids=[]



    entry0=False
    author=''
    for l in s.splitlines():
        # print(l)
        if entry0:
            if '<yt:videoId>' in l:
                # url=re.findall(URL_REGEX,l)[0]
                # vids[-1]['videoId']=url.replace('https://www.youtube.com/v/','')
                
                # ['lengthSeconds']
                vids.append({'videoId':remove_tag('yt:videoId',l)})

            elif '<title>' in l:
                vids[-1]['title']=remove_tag('title',l)
                vids[-1]['lengthSeconds']=0
                # vids[-1]['publishedText']=''
                vids[-1]['author']=author
            # list(vids)[-1]
            # vids[-1]=t
            # vids[t]=0
            # vids.append({'title':t})
            elif '<published>' in l:
                pub=remove_tag('published',l)
                y,m,dd=pub.split('-')
                d,hh=dd.split('T')
                h,mi,ss,zz=hh.split(':')
                dt = datetime(int(y), int(m), int(d), int(h), int(mi))
                # print(dt)
                # print(time_ago(dt.timestamp()))
                vids[-1]['publishedText']=time_ago(dt.timestamp())

            elif '<media:statistics' in l:
                views=re.findall(r'[0-9]+',l)[0]
                vids[-1]['viewCount']=int(views)

        else:
            if '<title>' in l:
                author=remove_tag('title',l)
            elif '<entry>' in l:
                entry0=True



    # print(vids)
    return vids
    # print(tree.getroot())