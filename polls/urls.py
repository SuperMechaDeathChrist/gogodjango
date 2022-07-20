from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('get_ep/<str:ep>/',views.get_ep),
    path('get_feed/',views.get_feed)
]