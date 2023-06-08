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
import os
from django.conf import settings
from django.http import HttpResponseBadRequest
from django.http import JsonResponse
from posts.models import Post
from django.core.files.base import ContentFile
import urllib.request
import tempfile


# Create your views here.
def login(request):
    if request.user.is_authenticated:
        return redirect('posts:index')
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
            user = form.save(commit=False)
            user.save()
            return redirect('accounts:profile', request.user.username)
    else:
        form = CustomUserChangeForm(instance=request.user)
    context = {
        'form': form,
    }

    return render(request, 'accounts/update.html', context)

@login_required
def delete(request):
    request.user.delete()
    return redirect('posts:index')


def signup(request):
    # my_sentence = []
    if request.user.is_authenticated:
        return redirect('posts:index')

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST, files=request.FILES)
        # print(form)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()
            auth_login(request, user)
            # my_sentence = request.POST.getlist('tag')
            return redirect('posts:index')
    else:
        form = CustomUserCreationForm()
        # my_sentence = request.POST.getlist('tag')
    context = {
        'form': form,
    }
    return render(request, 'accounts/signup.html', context)

# 중복 아이디 체크

def check_username(request):
    username = request.POST.get('username', '')
    print(username)
    User = get_user_model()
    try:
        User.objects.get(username=username)
        available = False
    except User.DoesNotExist:
        available = True

    return JsonResponse({'available': available})

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

# 거리 계산 api
import math
import requests

def haversine_distance(lon1, lat1, lon2, lat2):
    lon1, lat1, lon2, lat2 = map(math.radians, [lon1, lat1, lon2, lat2])

    dlon = lon2 - lon1
    dlat = lat2 - lat1

    a = math.sin(dlat/2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    r = 6371  # 지구의 반지름 (단위: km)

    distance = r * c
    distance = int(distance * 10) / 10  # 소수점 첫 번째 자리까지 버림
    return distance


def calculate_distance(address1, address2):
    url = 'https://dapi.kakao.com/v2/local/search/address.json'
    headers = {
        'Authorization': 'KakaoAK ' + settings.KAKAO_API_KEY
    }
    
    params = {
        'query': address1
    }
    response = requests.get(url, headers=headers, params=params)
    result1 = response.json()

    params = {
        'query': address2
    }
    response = requests.get(url, headers=headers, params=params)
    result2 = response.json()

    if 'documents' in result1 and result1['documents']:
        point1 = result1['documents'][0]['address']
    else:
        # 주소 검색 결과가 없는 경우 처리
        point1 = {
            'x': '126.97843',
            'y': '37.56668',
            'address_name': '서울특별시 중구 서소문동 37-9'
        }

    if 'documents' in result2 and result2['documents']:
        point2 = result2['documents'][0]['address']
    else:
        # 주소 검색 결과가 없는 경우 처리
        point2 = {
            'x': '126.97843',
            'y': '37.56668',
            'address_name': '서울특별시 중구 서소문동 37-9'
        }
    
    url = 'https://dapi.kakao.com/v2/local/geo/transcoord.json'
    params = {
        'x': point1['x'],
        'y': point1['y'],
        'output_coord': 'WGS84'
    }
    response = requests.get(url, headers=headers, params=params)
    result1 = response.json()

    params = {
        'x': point2['x'],
        'y': point2['y'],
        'output_coord': 'WGS84'
    }
    response = requests.get(url, headers=headers, params=params)
    result2 = response.json()

    if 'documents' in result1 and result1['documents'] and 'documents' in result2 and result2['documents']:
        distance = haversine_distance(result1['documents'][0]['x'], result1['documents'][0]['y'], result2['documents'][0]['x'], result2['documents'][0]['y'])
    else:
        # 유효한 좌표를 가져오지 못한 경우, 기본 거리를 0으로 설정
        distance = 0
    print(distance)

    return distance



def profile(request, username):
    User = get_user_model()
    person = get_object_or_404(User, username=username)
    user_id = person.id
    post_count = Post.objects.filter(user=person).count()
    music = Track.objects.filter(user_id=user_id)
    # introductions = request.person.get('introductions').split(',')
    # for intro in person.introductions:
    #     print(intro)
    # introductions_list = [intro.strip("'") for intro in person.introductions]
    introductions_list = []
    sign = ["[","]","'",","]
    word = ""
    # print(person.introductions)
    for introduction in person.introductions:
        if introduction == ",":
                introductions_list.append(word)
                word = ""
        if introduction not in sign:
            word += introduction
            
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

    if request.user.is_authenticated:
        current_user = request.user
        distance = calculate_distance(person.region, current_user.region)
    else:
        distance = None
        
    context = {
        'introductions_list' : introductions_list,
        'person': person,
        'music': music,
        'username': username,
        'distance': distance,
        'post_count': post_count,
        'introductions_list': introductions_list,

    }
    return render(request, 'accounts/profile.html', context)



@login_required
def follow(request, user_pk):
    person = get_object_or_404(User, pk=user_pk)

    if person != request.user:
        if person.followers.filter(pk=request.user.pk).exists():
            person.followers.remove(request.user)
            is_followed = False
        else:
            person.followers.add(request.user)
            is_followed = True

        followers_list = [{'username': follower.username, 'image_url': follower.image.url} for follower in person.followers.all()]
        # followings_list = [{'username': following.username, 'image_url': following.image.url} for following in person.followings.all()]

        context = {
            'is_followed': is_followed,
            'followings_count': person.followings.count(),
            'followers_count': person.followers.count(),
            # 'followings_list': followings_list,
            'followers_list': followers_list,
        }

        return JsonResponse(context)

    return JsonResponse({'error': 'You cannot follow yourself.'}, status=400)


tracks = {}
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



def save_track(request):
    global tracks
    if request.method == 'POST':
        selected_tracks = request.POST.getlist('selected_tracks[]')

    music = Track.objects.filter(user_id=request.user.id)
    if music.exists():
        for track in music:
            if request.user == track.user:
                if track.image:  
                    image_path = os.path.join(settings.MEDIA_ROOT, str(track.image))
                    if os.path.isfile(image_path):
                        os.remove(image_path)
                        music.delete()
                track.delete()

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
        if music.image:  
            image_path = os.path.join(settings.MEDIA_ROOT, str(music.image))
            if os.path.isfile(image_path):
                os.remove(image_path)
        music.delete()
    return redirect('accounts:profile',username=request.user.username)


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


