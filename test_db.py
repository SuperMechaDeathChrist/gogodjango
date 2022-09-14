# import requests
import db_flixhq
# import db

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

import db_history

# # db_history.wipe()
# # dbo=db_history.load()
# # dbo['series']={}
# # dbo['animes']={}
# # db_history.github_save(dbo,gittoken,gitrepo)

dbo=db_history.github_download(gittoken,gitrepo)
# # print(dbo)
# db_history.printdb()
# k,v=db_history.search('kgt2ba9u4zy')
# print(k)
# db_history.github_remove(k,gittoken,gitrepo)
db_history.printdb()

for k in dbo:
	print(k)

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