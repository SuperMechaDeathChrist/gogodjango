from django.shortcuts import render,redirect
from django.http import HttpResponse, JsonResponse
def redirect(request):
	dj=request.build_absolute_uri()
	# print(dj)
	# return redirect('https://gogdjango.herokuapp.com/polls/search/')
	s=f'<meta http-equiv="refresh" content=".1; URL={dj}polls/search/" />'
	return HttpResponse(s)