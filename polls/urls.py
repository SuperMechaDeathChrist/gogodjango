from django.urls import path,re_path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('get_flixhq_ep/',views.get_flixhq_ep),
    path('get_ep/<str:ep>/',views.get_ep),
    # path('get_flixhq_ep<str:aid>/<str:eid>',views.get_flixhq_ep),
    path('get_feed/',views.get_feed),
    path('test/',views.test),
    path('get_rss_feed/',views.get_rss_feed),
    path('categories/',views.categories),
    path('recent_anime/',views.recent_anime),
    path('recent_anime_dub/',views.recent_anime_dub),
    path('recent_anime_chinese/',views.recent_anime_chinese),
    path('favorite_anime/',views.favorite_anime),
    path('top_airing_anime/',views.test),
    path('favorite_series/',views.favorite_series),
    path('favorite_movies/',views.favorite_movies),
    path('addto_fav_anime/<str:aid>/',views.addto_fav_anime),
    path('addto_fav_series/<str:ctype>/<str:id>',views.addto_fav_series),
    # path('addto_fav/<str:aid>/',views.addto_fav),
    path('addto_fav/<str:aid>/',views.addto_fav_anime),
    path('addto_fav/<str:ctype>/<str:id>',views.addto_fav_series),
# polls/addto_fav/https://flixhq.to/movie/watch-i
    path('addto_fav/https://flixhq.to/<str:ctype>/<str:id>',views.addto_fav_series),
    # https://gogoanime.lu/category/berserk-2016-dub
    path('addto_fav/https://gogoanime.<str:trash>/category/<str:aid>',views.addto_fav_anime_full_url),

    path('removefrom_fav_anime/<str:aid>/',views.removefrom_fav_anime),
    path('removefrom_fav_series/<str:ctype>/<str:id>',views.removefrom_fav_series)
]