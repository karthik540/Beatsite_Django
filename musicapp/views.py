from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth import authenticate, login , logout
from .models import CustomUser
import requests , json , pprint
from .image_url_fetcher import fetch_url

# Create your views here.

def index(request):
    return render(request , 'index.html')

def login_user(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = CustomUser.objects.get(email = email)

        if user is not None:
            if user.check_password(password):
                if user.is_active:
                    login(request , user)
                    return JsonResponse({'flag' : 1})
    return JsonResponse({'flag' : 0})

def logout_user(request):
    logout(request)
    return JsonResponse({'flag' : 1})

def signup_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        email = request.POST['email']

        user = CustomUser()
        user.username = username
        user.set_password(password)
        user.email = email
        user.save()

        user = CustomUser.objects.get(email = email)
        if user is not None:
            login(request , user)
            return JsonResponse({'flag' : 1})
    return JsonResponse({'flag' : 0})

def browse(request , page_no = 1):
    album_list = []
    page_limit = 12                  #Page Limit Setting Variable
    
    url_request = 'http://api.musixmatch.com/ws/1.1/chart.tracks.get?apikey=3d136bab70652b62413441c2a2880831&chart_name=top&page=' + str(page_no) + '&page_size=' + str(page_limit) + '&country=in&f_has_lyrics=1'
    r = requests.get(url_request)
    json_data = json.loads(r.text)
    
    for track in json_data['message']['body']['track_list']:
        url = fetch_url(str(track['track']['album_name']) , str(track['track']['artist_name']))
        single_album_list = {
            'album_id' : track['track']['album_id'],
            'album_name' : track['track']['album_name'] , 
            'artist_name' : track['track']['artist_name'],
            'image_url': url
        }
        album_list.append(single_album_list)
    #pprint.pprint(album_list)


    data = {
        'flag' : 1,
        'album_list' : album_list,
        'page_no' : page_no
    }
    return render(request , 'browse.html' , context= data)

def album(request , album_id):
    track_list = []
    url_request = 'http://api.musixmatch.com/ws/1.1/album.tracks.get?apikey=3d136bab70652b62413441c2a2880831&album_id=' + str(album_id) + '&page=1&page_size=20'
    r = requests.get(url_request)
    json_data = json.loads(r.text)

    counter = 1
    for track in json_data['message']['body']['track_list']:
        songname = track['track']['track_name']
        """
        Youtube video Fetcher

        <iframe width="560" height="315" src="https://www.youtube.com/embed/GWH_k6S7YQU" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>

        l = "https://www.googleapis.com/youtube/v3/search?part=id&q="+ str(songname) +"&type=video&key=AIzaSyBtN6nKC7Jaai3hIWlumCQgrtkBZcmWq4U"
        p = requests.get(l)
        j_objs = json.loads(p.text)
        pprint.pprint(j_objs)
        video_id = j_objs['items'][0]['id']['videoId']
        print(video_id)

        """

        single_track = {
            'index' : counter ,
            'track_id' : track['track']['track_id'],
            'track_name' : track['track']['track_name'], 
            'track_rating' : track['track']['track_rating'],
            #'video_id' : video_id
        }
        track_list.append(single_track)
        counter = counter + 1
    for track in json_data['message']['body']['track_list']:
        url = fetch_url(str(track['track']['album_name']) , str(track['track']['artist_name']))
        if not track['track']['primary_genres']['music_genre_list']:
            genre = "Unknown"
        else:
            genre = track['track']['primary_genres']['music_genre_list'][0]['music_genre']['music_genre_name']
        album_info = {
            'album_name' : track['track']['album_name'],
            'artist_name' : track['track']['artist_name'],
            'album_url' : url ,
            'genre' : genre
        }
        break
    #pprint.pprint(json_data['message']['body']['track_list'])
    data = {
        'flag' : 1,
        'album_info': album_info , 
        'track_list' : track_list
    }
    return render(request , 'album.html' , context= data)

def videoId(request , songname):
    songname = songname.replace(" " , "_")
    #print(songname)
    l = "https://www.googleapis.com/youtube/v3/search?part=id&q="+ str(songname) +"&type=video&key=AIzaSyBtN6nKC7Jaai3hIWlumCQgrtkBZcmWq4U"
    p = requests.get(l)
    j_objs = json.loads(p.text)
    pprint.pprint(j_objs)
    video_id = j_objs['items'][0]['id']['videoId']
    return JsonResponse({'video_id' : video_id})

