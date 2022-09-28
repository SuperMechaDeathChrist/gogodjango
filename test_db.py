import requests
requests.packages.urllib3.util.connection.HAS_IPV6 = False
import db_flixhq
# import db
import time
from cryptography.fernet import Fernet
key=b'wnuSKeQm1WLsf0qtmWVyoknqEhvrNXqj1RKewiwJFDE='
encMessage=b'gAAAAABi7tt3uuCl4P2d_m1JpvKUZuTBK7SMGuJqlJVRTIhsFhUFjLCe_kf2veI7iWNuEZpT2jCYhJE7MBhV990S4fu4iS81zpb29e41MAleVgIdZT6xSe5y6kcfTzkM_MW81n9cU08O'
fernet = Fernet(key)
gittoken = fernet.decrypt(encMessage).decode()

gitrepo="SuperMechaDeathChrist/gogodjango"

# dbo=db_flixhq.github_download(token=gittoken,repo=gitrepo,do_save=True)
# db_flixhq.printdb()
# #dbo=db.github_download(token=gittoken,repo=gitrepo,do_save=True)

# for k in dbo:
# 	if k:
		# db_flixhq_all.add(k,dbo[k])
# 		print(k,dbo[k]['response']['episodes'])
# 		# print(k,dbo[k]['response']['episodes'])
# 		# print('\n'*10)
# 		# http://192.168.0.34:3000/polls/addto_fav
# 		# r=requests.get('http://192.168.0.34:3000/polls/addto_fav/'+k)
# 		# print(r.text)
# 		print(k,dbo[k]['response']['episodes'][0])

# import pickle
# from db_flixhq import CaseInsensitiveDict
# dbo=pickle.load(open('db_flixhq - Copy.dat','rb'))
# for k in dbo:
# 	if k:
# 		print(k,dbo[k]['response']['episodes'][0])

# import db_query

# db_query.wipe()
# dbo=db_query.load()
# dbo['series']={}
# dbo['animes']={}
# db_query.github_save(dbo,gittoken,gitrepo)

# dbo=db_query.github_download(gittoken,gitrepo)
# print(dbo)

# import db_history

# # db_history.wipe()
# # dbo=db_history.load()
# # dbo['series']={}
# # dbo['animes']={}
# # db_history.github_save(dbo,gittoken,gitrepo)

# dbo=db_history.github_download(gittoken,gitrepo)
# # print(dbo)
# db_history.printdb()
# k,v=db_history.search('kgt2ba9u4zy')
# print(k)
# db_history.github_remove(k,gittoken,gitrepo)
# db_history.printdb()

# for k in dbo:
# 	print(k)

# db_history.github_remove(k,token=gittoken,repo=gitrepo)

# import db_yt_queue

# db_yt_queue.wipe()
# dbo=db_yt_queue.load()
# db_yt_queue.github_save(dbo,gittoken,gitrepo)

# dbo=db_yt_queue.github_download(gittoken,gitrepo)
# for k in dbo:
# 	if k:
# 		print(k,dbo[k])
# db_yt_queue.printdb()v






# import db_yt_channels as db
# # db_yt_channels.wipe()
# db.wipe()
# yt_channels={
#     'vinesauce':'UCzORJV8l3FWY4cFO8ot-F2w',
#     'RedLetterMedia':'UCrTNhL_yO3tPTdQ5XgmmWjA',
#     'Cinemassacre':'UC0M0rxSz3IF0CsSour1iWmw',
#     'FanboyFlicks':'UCpsjEC4PlHmhM84yX5Y3rrg',
#     'Internet Comment Etiquette with Erik':'UCyWDmyZRjrGHeKF-ofFsT5Q',
#     'Boy boy':'UC_S45UpAYVuc0fYEcHN9BVQ',
#     'I did a thing':'UCJLZe_NoiG0hT7QCX_9vmqw',
#     'H3 Pocdast':'UCLtREJY21xRfCuEKvdki1Kw',
#     'HasanAbi':'UCtoaZpBnrd0lhycxYJ4MNOQ',
#     'Channel 5 with Andrew Callaghan':'UC-AQKm7HUNMmxjdS371MSwg',
#     'Hasanabi Moments':'UCobue-_fUPSIwdWULdE3MbQ',
#     'Stoned Gremlin Productions':'UCIO689mgXeuzH4M5NS7wZwg',
#     'Ryan George':'UCh9IfI45mmk59eDvSWtuuhQ',
#     'Pitch Meeting':'UC9Kq-yEt1iYsbUzNOoIRK0g',
#     'El Pulso De La República':'UCK0_zBeybLuyXbOcHp7wmJA',
#     'Wisecrack':'UC6-ymYjG0SU0jUWnWh9ZzEQ',
#     'Screen Junkies':'UCOpcACMWblDls9Z6GERVi1A',
#     'Steve Reviews':'UCqERpXggAprNW8QT_WO1N5Q',
#     'Cold Ones':'UCfbnTUxUech4P1XgYUwYuKA',
#     }



# import db_flixhq_all
# db_flixhq_all.printdb()

# # print(db_flixhq_all.load()['']['saved'],time.time(),(time.time()-db_flixhq_all.load()['']['saved']))

# # import db_flixhq_home
# # db_flixhq_home.wipe()

# dbo=db_flixhq_all.load()
# for k in dbo:
# 	if k:
# 		if not 'response' in dbo[k]:
# 			dbo[k]={'response':dbo[k]}

# db_flixhq_all.github_save(dbo,gittoken,gitrepo)

import db_flixhq_home

dbo=db_flixhq_home.github_download(gittoken,gitrepo)
# dbo=db_flixhq_home.load()
for k in dbo:
	print(k)
print(dbo[''])
# dbo[''].pop('sha',None)
# db_flixhq_home.save(dbo)
# db_flixhq_home.printdb()

# db_flixhq_home.github_save(dbo,gittoken,gitrepo)