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
from django.http import HttpResponseBadRequest
# from . import search_spotify

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
    music = Track.objects.all()
    if request.method == 'GET':
        query = request.GET.get('q')  # GET 파라미터에서 'q' 값을 가져옵니다.

        if query:
            tracks = search_spotify(query)  # 검색 기능 사용
            context = {
                'person': person,
                'tracks': tracks,
                'music' : music,
            }
            return render(request, 'accounts/profile.html', context)

    context = {
        'person': person,
        'music' : music,
    }
    return render(request, 'accounts/profile.html', context)


# def profile(request, username):
#     User = get_user_model()
#     person = User.objects.get(username=username)
#     context = {
#         'person': person,
#     }
#     return render(request, 'accounts/profile.html', context)    


from pprint import pprint
# music = []


tracks = {}
def search_spotify(request):
    global tracks
    if request.method == 'GET':
        query = request.GET.get('q')

        if query:
            tracks = search(query)  # 검색 기능 사용
            
            # pprint(tracks)
            # print("================================")
            # music = tracks
            # pprint(tracks)
            # for m in tracks:
            #     print("------------")
            #     pprint(m)
                # if "3q2987XcSbQpQIiLmD6z4T" == m['id']:
                #         print("------------")
                #         pprint(m)
                # elif "4Htjh6MSRQoPhdz41Pb9PS" == m['album']['id']:

            # for track in tracks:
            #     Track.objects.create(
            #         title=track['name'],
            #         artist=track['artists'][0]['name'],
            #         album=track['album']['name'],
            #         image_url=track['album']['images'][0]['url'],
            #         preview_url=track['preview_url']
            #     )
            context = {
                'tracks': tracks,
            }
            return render(request, 'accounts/profile.html', context)
        return render(request, 'accounts/profile.html')


# 복붙

def save_track(request):
    global tracks
    if request.method == 'POST':
        selected_tracks = request.POST.getlist('selected_tracks[]')
        # print(tracks)
        # print(selected_tracks)
    music = Track.objects.filter(user_id=request.user.id)
    if music is not None:
        # if request.user == music.user_id:
        music.delete()
    
    for track_id in selected_tracks:
        for track in tracks:
            if track_id == track['id']:
                Track.objects.create(
                    title=track['name'],
                    artist=track['artists'][0]['name'],
                    album=track['album']['name'],
                    image_url=track['album']['images'][0]['url'],
                    preview_url=track['preview_url'],
                    user = request.user
                )
        return redirect('accounts:profile', username=request.user.username)
    else:
        return HttpResponseBadRequest("Invalid request method.")
        # try:
        #     track_id = int(track_id)
        #     Track.objects.create(
        #         title=track['name'],
        #         artist=track['artists'][0]['name'],
        #         album=track['album']['name'],
        #         image_url=track['album']['images'][0]['url'],
        #         preview_url=track['preview_url']
        #     )
        #     track = Track.objects.get(pk=track_id)
        #     # print(track_id)
        #     user_profile = request.user.profile
        #     user_profile.saved_tracks.add(track)
        # except (ValueError, Track.DoesNotExist):
        #     # print('1')
        #     pass




        # for track_id in selected_tracks:
            # try:
            # track = Track.objects.get(id=track_id)
            # Track 모델에 저장
            # saved_track = Track(
            #     title=track.title,
            #     artist=track.artist,
            #     album=track.album,
            #     image_url=track.image_url,
            #     preview_url=track.preview_url
            # )
            # saved_track.save()
            # except Track.DoesNotExist:
            #     print('1')
            #     pass

# def search_spotify(request):
#     if request.method == 'GET':
#         query = request.GET.get('q')

#         if query:
#             tracks = search(query)  # 검색 기능 사용
            # pprint(tracks)
            # print("================================")
            # music = tracks
            # pprint(tracks)
            # for m in tracks:
            #     print("------------")
            #     pprint(m)
                # if "3q2987XcSbQpQIiLmD6z4T" == m['id']:
                #         print("------------")
                #         pprint(m)
                # elif "4Htjh6MSRQoPhdz41Pb9PS" == m['album']['id']:
        #     for track in tracks:
        #         Track.objects.create(
        #             title=track['name'],
        #             artist=track['artists'][0]['name'],
        #             album=track['album']['name'],
        #             image_url=track['album']['images'][0]['url'],
        #             preview_url=track['preview_url']
        #         )
        #     context = {
        #         'tracks': tracks,
        #     }
        #     return render(request, 'accounts/profile.html', context)
        # return render(request, 'accounts/profile.html')

import os
from django.conf import settings

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

# def search2(track_id):

#     def get_access_token():
#         token_url = 'https://accounts.spotify.com/api/token'
#         auth = (client_id, client_secret)
#         payload = {'grant_type': 'client_credentials'}
#         response = requests.post(token_url, data=payload, auth=auth)

#         if response.status_code == 200:
#             token_data = response.json()
#             access_token = token_data['access_token']
#             return access_token
#         else:
#             raise Exception('Failed to retrieve access token from Spotify.')

#     def search2(track_id):
#         search_url = 'https://api.spotify.com/v1/search'
#         headers = {'Authorization': f'Bearer {get_access_token()}'}
#         params = {'q': f'track:{track_id}', 'type': 'track'}

#         response = requests.get(search_url, headers=headers, params=params)

#         if response.status_code == 200:
#             search_results = response.json()
#             tracks = search_results['tracks']['items']
#             return tracks
#         else:
#             raise Exception('Failed to search tracks on Spotify.')

#     tracks = search2(track_id)
#     return tracks


User = get_user_model()
def set_profile_music(request, track_id):
    # Get the currently logged-in user
    user = request.user

    # Retrieve the user instance
    user_instance = get_object_or_404(User, username=user.username)

    # Set the selected track as the profile music
    user_instance.profile_music = track_id
    user_instance.save()

    # Display a success message
    messages.success(request, '프로필 뮤직이 설정되었습니다.')

    # Redirect to the profile page
    return redirect('accounts:profile', username=user.username)


# def save_track(request):
#     # track_id를 사용하여 Track 모델에서 해당 음원을 가져옵니다.
#     if request.method == 'POST':
#         track_id = request.POST.get('track_id')
#         track = Track.objects.get(pk=track_id)  # track_id를 사용하여 음원 객체를 가져옴


#     # 현재 로그인된 사용자의 프로필에 음원을 저장합니다.
#     user_profile = request.user.profile  # 사용자의 프로필 가져오기
#     user_profile.saved_tracks.add(track)  # 음원을 저장하는 관계 필드에 추가

#     # 프로필 페이지로 리디렉션합니다.
#     return redirect('accounts:profile', username=request.user.username)



# def save_track(request):
#     if request.method == 'POST':
#         selected_tracks = request.POST.getlist('selected_tracks[]')
#         print(selected_tracks)
        # for track_id in selected_tracks:
            # try:
            # track = Track.objects.get(id=track_id)
            # Track 모델에 저장
            # saved_track = Track(
            #     title=track.title,
            #     artist=track.artist,
            #     album=track.album,
            #     image_url=track.image_url,
            #     preview_url=track.preview_url
            # )
            # saved_track.save()
            # except Track.DoesNotExist:
            #     print('1')
            #     pass

    #     return redirect('accounts:profile', username=request.user.username)
    # else:
    #     return HttpResponseBadRequest("Invalid request method.")
    

            # track_id = int(selected_tracks)
        # # track_id = selected_tracks
        # track = Track.objects.get(pk=track_id)
        # print(track_id)
        # user_profile = request.user.profile
        # user_profile.saved_tracks.add(track)
        
        # print(music)
        # print(selected_tracks)
        # for track_id in selected_tracks:
        #     try:
        #         track_id = int(track_id)
        #         # track = search2(track_id) 
        #         # Track.objects.create(
        #         #     title=track['name'],
        #         #     artist=track['artists'][0]['name'],
        #         #     album=track['album']['name'],
        #         #     image_url=track['album']['images'][0]['url'],
        #         #     preview_url=track['preview_url']
        #         # )
        #         track = Track.objects.get(pk=track_id)
        #         # print(track_id)
        #         user_profile = request.user.profile
        #         user_profile.saved_tracks.add(track)
        #     except (ValueError, Track.DoesNotExist):
        #         # print('1')
        #         pass