from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm, CustomUserChangeForm, CustomAuthenticationForm, CustomPasswordChangeForm
from django.contrib.auth import get_user_model
import requests
from django.contrib import messages
from .models import Track
from pprint import pprint
import os
from django.conf import settings
from django.http import HttpResponseBadRequest
from django.http import JsonResponse

# Create your views here.
def login(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, request.POST)
        if form.is_valid():
            auth_login(request, form.get_user())
            return redirect('posts:index')
    
    else:
        form = CustomAuthenticationForm()
    context = {
        'form': form,
    }
    return render(request, 'accounts/login.html', context)

@login_required
def logout(request):
    if request.user.is_authenticated:
        auth_logout(request)
    return redirect('posts:index')

@login_required
def update(request):
    if request.method == 'POST':
        form = CustomUserChangeForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('accounts:profile', request.user.username)
    else:
        form = CustomUserChangeForm(instance=request.user)
    context = {
        'form':form,
    }
    
    return render(request, 'accounts/update.html', context)


def signup(request):
    # my_sentence = []
    if request.user.is_authenticated:
        return redirect('posts:index')

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST, files=request.FILES)
        # print(form)
        if form.is_valid():
            # form.save()
            user = form.save()
            auth_login(request, user)
            # my_sentence = request.POST.getlist('tag')
            return redirect('accounts:login')
    else:
        form = CustomUserCreationForm()
        my_sentence = request.POST.getlist('tag')
    context = {
        'form': form,
        # 'my_sentence':my_sentence,
    }
    return render(request, 'accounts/signup.html', context)

@login_required
def change_password(request):
    if request.method == 'POST':
        form = CustomPasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            return redirect('posts:index')
    else:
        form = CustomPasswordChangeForm(request.user)
    context = {
        'form': form,
    }
    return render(request, 'accounts/change_password.html', context)


def profile(request, username):
    User = get_user_model()
    person = get_object_or_404(User, username=username)
    user_id = person.id

    music = Track.objects.filter(user_id=user_id)

    if request.method == 'GET':
        query = request.GET.get('q')

        if query:
            tracks = search_spotify(query)
            context = {
                'person': person,
                'tracks': tracks,
                'music': music,
            }
            return render(request, 'accounts/profile.html', context)

    context = {
        'person': person,
        'music': music,
        'username': username,
    }
    return render(request, 'accounts/profile.html', context)


# def profile(request, username):
#     User = get_user_model()
#     person = get_object_or_404(User, username=username)
#     music = Track.objects.all()
#     if request.method == 'GET':
#         query = request.GET.get('q')  # GET 파라미터에서 'q' 값을 가져옵니다.

#         if query:
#             tracks = search_spotify(query)  # 검색 기능 사용
#             context = {
#                 'person': person,
#                 'tracks': tracks,
#                 'music' : music,
#             }
#             return render(request, 'accounts/profile.html', context)

#     context = {
#         'person': person,
#         'music' : music,
#     }
#     return render(request, 'accounts/profile.html', context)


tracks = {}
# def search_spotify(request):
#     global tracks
#     if request.method == 'GET':
#         query = request.GET.get('q')

#         if query:
#             tracks = search(query)  # 검색 기능 사용
#             context = {
#                 'tracks': tracks,
#             }
#             return render(request, 'accounts/profile.html', context)
#         return render(request, 'accounts/profile.html')
from django.template.loader import render_to_string

def search_spotify(request):
    global tracks
    if request.method == 'GET':
        query = request.GET.get('q')

        if query:
            tracks = search(query)  # 검색 기능 사용

            context = {
                'tracks': tracks,
            }
            return render(request, 'accounts/search_results.html', context)

    return render(request, 'accounts/search_results.html')

from django.core.files.base import ContentFile
import urllib.request
import tempfile

def save_track(request):
    global tracks
    if request.method == 'POST':
        selected_tracks = request.POST.getlist('selected_tracks[]')

    music = Track.objects.filter(user_id=request.user.id)
    if music.exists():
        music.delete()

    for track_id in selected_tracks:
        for track in tracks:
            if track_id == track['id']:
                # 이미지 URL 가져오기
                image_url = track['album']['images'][0]['url']

                # 이미지 다운로드 및 저장
                img_temp = tempfile.TemporaryFile()
                img_temp.write(urllib.request.urlopen(image_url).read())
                img_temp.seek(0)  # 파일 포인터를 처음으로 되돌림

                # Track 객체 생성 및 저장
                new_track = Track()
                new_track.title = track['name']
                new_track.artist = track['artists'][0]['name']
                new_track.album = track['album']['name']
                new_track.preview_url = track['preview_url']
                new_track.user = request.user
                new_track.image.save(f'{track_id}.jpg', ContentFile(img_temp.read()))

        return redirect('accounts:profile', username=request.user.username)
    else:
        return HttpResponseBadRequest("Invalid request method.")

def delete_track(request, track_pk):
    music = Track.objects.get(pk=track_pk)
    if request.user == music.user:
        music.delete()
    return redirect('accounts:profile',username=request.user.username)



#     global tracks
#     if request.method == 'POST':
#         selected_tracks = request.POST.getlist('selected_tracks[]')
#         # print(tracks)
#         # print(selected_tracks)
#     music = Track.objects.filter(user_id=request.user.id)
#     if music is not None:
#         # if request.user == music.user_id:
#         music.delete()
    
#     for track_id in selected_tracks:
#         for track in tracks:
#             if track_id == track['id']:
#                 Track.objects.create(
#                     title=track['name'],
#                     artist=track['artists'][0]['name'],
#                     album=track['album']['name'],
#                     image_url=track['album']['images'][0]['url'],
#                     preview_url=track['preview_url'],
#                     user = request.user
#                 )
#         return redirect('accounts:profile', username=request.user.username)
#     else:
#         return HttpResponseBadRequest("Invalid request method.")




def search(query):
    CLIENT_ID = settings.CLIENT_ID
    CLIENT_SECRET = settings.CLIENT_SECRET

    def get_access_token():
        token_url = 'https://accounts.spotify.com/api/token'
        auth = (CLIENT_ID, CLIENT_SECRET)
        payload = {'grant_type': 'client_credentials'}
        response = requests.post(token_url, data=payload, auth=auth)

        if response.status_code == 200:
            token_data = response.json()
            access_token = token_data['access_token']
            return access_token
        else:
            raise Exception('Failed to retrieve access token from Spotify.')

    def search(query):
        search_url = 'https://api.spotify.com/v1/search'
        headers = {'Authorization': f'Bearer {get_access_token()}'}
        params = {'q': query, 'type': 'track'}

        response = requests.get(search_url, headers=headers, params=params)

        if response.status_code == 200:
            search_results = response.json()
            tracks = search_results['tracks']['items']
            return tracks
        else:
            raise Exception('Failed to search tracks on Spotify.')

    tracks = search(query)
    return tracks


User = get_user_model()
def set_profile_music(request, track_id):
    user = request.user
    user_instance = get_object_or_404(User, username=user.username)
    user_instance.profile_music = track_id
    user_instance.save()

    messages.success(request, '프로필 뮤직이 설정되었습니다.')

    return redirect('accounts:profile', username=user.username)
