import re
f='-search.html'
html='{% load static %}\n'
with open(f,'r',encoding='utf-8') as fid:
	s=fid.read()

# s=s.replace(r'="assets/','="{% static \'assets/')
# print(s)

# for c in s:
# regex="(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?«»""'']))"
regex=r'(="assets/[^\s]+")'
# print(s)
url = re.findall(regex,s)
for u in url:
	s=s.replace(u,'="{% static \''+u[2:-1]+'\' %}"')
# print(s)

with open(f.strip('-'),'w',encoding='utf-8') as fid:
	fid.write(html+s)