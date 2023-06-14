from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm, CustomUserChangeForm, CustomAuthenticationForm, CustomPasswordChangeForm, ResultForm
from django.contrib.auth import get_user_model
import requests
from django.contrib import messages
from .models import Track
import os
from django.conf import settings
from django.http import HttpResponseBadRequest
from django.http import JsonResponse
from posts.models import Post, PostReport, CommentReport, Fortune
from django.core.files.base import ContentFile
import urllib.request
import tempfile
from django.core.exceptions import ObjectDoesNotExist
from balances.models import Result
from datetime import date
from .models import User

# Create your views here.
def balances(request):
    return render(request, 'accounts/balances.html')

def login(request):
    if request.user.is_authenticated:
        return redirect('posts:index')

    
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, request.POST)
        username = request.POST.get('username')
        user = get_user_model()
        users = user.objects.all()
        a = []
        for i in users:
            a.append(i.username)
        if form.is_valid():
            auth_login(request, form.get_user())
            user1 = User.objects.get(username=username)
            user_pk = user1.pk
            hiword_1 = Result.objects.filter(pk=user_pk)
            if hiword_1.exists():
                return redirect('posts:index')
            else:
                return redirect('accounts:balances')

            
        else:
            for i in a:
                if username in a:
                    context = {
                        'error' : '⛔ 이메일 인증하세요.',
                        'form': form,
                        }
                    return render(request, 'accounts/login.html', context)
                elif username not in a:
                    context = {
                        'error' : '⛔ 회원정보가 존재하지 않습니다.',
                        'form' : form,
                        }
                    return render(request, 'accounts/login.html', context)
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

# 이메일 인증 관련
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.core.mail import EmailMessage
from django.utils.encoding import force_bytes, force_text
from .tokens import account_activation_token
from django.contrib import auth

def complete_signup(request):
    return render(request, 'accounts/complete_signup.html')

def signup(request):
    if request.user.is_authenticated:
        return redirect('posts:index')

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST, files=request.FILES)
        # print(form)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = True 
            # user.is_active = False 
            user.save()
            current_site = get_current_site(request) 
            message = render_to_string('accounts/activation_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            mail_title = "계정 활성화 확인 이메일"
            mail_to = request.POST["email"]
            email = EmailMessage(mail_title, message, to=[mail_to])
            email.send()
            auth_login(request, user)
            return redirect('accounts:complete_signup')
    else:
        form = CustomUserCreationForm()
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

# 중복 이메일 체크

def check_email(request):
    email = request.POST.get('email', '')
    User = get_user_model()
    users_with_email = User.objects.filter(email=email)
    available = not users_with_email.exists()

    return JsonResponse({'available': available})


# 계정 활성화 함수(토큰을 통해 인증)
def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExsit):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        auth.login(request, user)
        return redirect("home")
    else:
        context = {
            'error' : '계정 활성화 오류'
        }

        return render(request, 'accounts/email_error.html', context)


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

    return distance

def profile(request, username):
    User = get_user_model()
    person = get_object_or_404(User, username=username)
    user_id = person.id
    post_count = Post.objects.filter(user=person).count()
    music = Track.objects.filter(user_id=user_id)
    post_reports = PostReport.objects.order_by('post_id', 'title')
    comment_reports = CommentReport.objects.order_by('comment_id', 'title') 
    word_form = ResultForm(user=request.user)
    
    try:
        fortunes = Fortune.objects.get(user_id=user_id)
        # fortunes = Fortune.objects.filter(user_id=user_id)
    except ObjectDoesNotExist:
        fortunes = None

    # 자기소개 표시
    introductions_list = []
    sign = ["[","]","'",","]
    word = ""
    len_word = len(person.introductions)
    for i in range(len_word):
        if person.introductions[i] == "," or i == len_word - 1:
            introductions_list.append(word)
            word = ""
        elif person.introductions[i] not in sign:
            word += person.introductions[i]
    
    # 밸런스 단어 받기
    if person.words:
        word_list = []
        word2 = ""
        len_word2 = len(person.words)
        for j in range(len_word2):
            if j == len_word2 - 1:
                word2 += person.words[j]
                word_list.append(word2)
            elif person.words[j] == ",":
                word_list.append(word2)
                word2 = ""
            else:
                word2 += person.words[j]
    else:
        word_list = []

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
        'post_reports' : post_reports,
        'comment_reports' : comment_reports,
        'fortunes' : fortunes,
        'word_list' : word_list,
        'fortune_today' : date.today(),
        'word_form' : word_form,

    }
    return render(request, 'accounts/profile.html', context)



@login_required
def follow(request, user_pk):
    # person = get_object_or_404(User, pk=user_pk)
    User = get_user_model()
    person  = User.objects.get(pk=user_pk)
    if person != request.user:
        if request.user in person.followers.all():
            person.followers.remove(request.user)
            is_followed = False
        else:
            person.followers.add(request.user)
            is_followed = True
        followers_list = []
        for follower in person.followers.all():
            if follower.image:
                followers_list.append({'username': follower.username, 'pk': follower.pk, 'image': follower.image.url})
            else:
                followers_list.append({'username': follower.username, 'pk': follower.pk})
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

# 밸런스 게임에서 할당 된 워드를 폼으로 받기 위한 코드
def word_create(request):
    user = request.user
    if request.method == 'POST':
        word_form = ResultForm(request.POST, user=user)
        if word_form.is_valid():
            words = word_form.cleaned_data['words']
            
            # Update the User model with the selected words
            user.words = ','.join(words)
            user.save()
            
            return redirect('accounts:profile', user.username)
    else:
        word_form = ResultForm(user=user)