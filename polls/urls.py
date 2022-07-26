from django.urls import path,re_path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('search/', views.search_series, name='index'),
    path('search_anime/', views.search_anime, name='index'),
    path('search_fav_series/', views.search_fav_series, name='index'),
    path('search_fav_anime/', views.search_fav_anime, name='index'),
    path('search_series/', views.search_series, name='index'),
    path('search_youtube/', views.search_youtube, name='index'),

    path('get_flixhq_ep/',views.get_flixhq_ep),
    path('get_flixhq_sub/',views.get_flixhq_sub),
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

    path('last_query_animes/',views.last_query_animes),
    path('last_query_series/',views.last_query_series),
    path('history_anime/',views.history_anime),
    path('history_series/',views.history_series),

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

    path('removefrom_fav/<str:aid>/',views.removefrom_fav_anime),
    path('removefrom_fav/<str:ctype>/<str:id>',views.removefrom_fav_series),
    path('removefrom_fav/https://flixhq.to/<str:ctype>/<str:id>',views.removefrom_fav_series),
    path('removefrom_fav/https://gogoanime.<str:trash>/category/<str:aid>',views.removefrom_fav_anime_full_url),    

    path('removefrom_fav_anime/<str:aid>/',views.removefrom_fav_anime),
    path('removefrom_fav_series/<str:ctype>/<str:id>',views.removefrom_fav_series),

    path('launch_channel/',views.launch_channel),

    path('addto_yt_queue/<str:aid>/',views.addto_yt_queue),
    path('get_yt_stream/',views.get_yt_stream),
    path('feed_yt_queue/',views.feed_yt_queue),
    path('feed_yt_channel/',views.feed_yt_channel),
    path('view_yt_queue/',views.view_yt_queue),
    
    path('history_youtube/',views.history_youtube),
    path('removefrom_yt_queue/<str:aid>/',views.removefrom_yt_queue),
    path('view/',views.view),

    path('update_feed_flixhq_home',views.update_feed_flixhq_home),
    path('flixhq_trending/',views.flixhq_trending),
    path('flixhq_latest_series/',views.flixhq_latest_series),
    path('flixhq_latest_movies/',views.flixhq_latest_movies),

]

