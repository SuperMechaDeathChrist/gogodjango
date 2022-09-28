import os
import requests as rq
rq.packages.urllib3.util.connection.HAS_IPV6 = False
from bs4 import BeautifulSoup
headers = {"User-Agent": "Mozilla/5.0 (X11; CrOS x86_64 12871.102.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.141 Safari/537.36"}


if os.path.exists('flixhq_home.html'):
	with open('flixhq_home.html','r',encoding='utf-8') as fid:
		bs=BeautifulSoup(fid.read(),features='lxml')
else:
	r=rq.get('https://flixhq.to/home')
	with open('flixhq_home.html','w',encoding='utf-8') as fid:
		fid.write(r.text)
	bs = BeautifulSoup(r.text,features='lxml')


for sect in bs.find_all('section',{'class':'block_area block_area_home section-id-01'}):
	sect_title=sect.find_all('h2',{'class':'cat-heading'})[0].text
	if sect_title=='Coming Soon':
		continue
	print(sect_title)

	for a in sect.find_all('div', {"class": "flw-item"}):
	    print('-'*20)
	    det=a.find_all('h3',{'class':'film-name'})[0].find_all('a')[0]
	    

	    sub=' '.join([fdi.text for fdi in a.find_all('span',{'class':'fdi-item'})])
	    
	    img=a.find_all('img')[0]
	    # print(det['href'].lstrip('/'))
	    # print(det['title'])
	    # print(sub)
	    # print(img['data-src'])
	    
	    # print(a.text)


# import db_flixhq_all


# db_flixhq_all.wipe()