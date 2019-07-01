from django.urls import path , include
from . import views

urlpatterns = [
    path('', views.index , name = 'index'),
    #   User Authentication
    path('account/login/' , views.login_user , name = 'login'),
    path('account/logout/' , views.logout_user , name = 'logout'),
    path('account/signup/' , views.signup_user , name = 'signup'),
    #   Album List
    path('browse/' , views.browse , name = 'browse'),
    path('browse/<int:page_no>/' , views.browse , name = 'browse'),
    #   Album Page
    path('album/<int:album_id>/' , views.album , name = 'album'),
    path('videoId/<str:songname>/' , views.videoId , name = 'videoId'),
    #   Favourites Add
    path('favourite_add/<str:songid>/' , views.favourite_add , name='favourite_add'),
    path('favourite/' , views.favourite , name='favourite'),
    #   Bot API Response
    path('botResponse/' , views.botResponse , name='botResponse'),
]