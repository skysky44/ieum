from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from .forms import PostForm, CommentForm, PostReportForm, CommentReportForm
from .models import Post, Comment, Fortune
from paints.models import Paint
from .models import PostTrack
import os
from django.conf import settings
from django.core.files.base import ContentFile
import urllib.request
import tempfile
import requests
from django.db.models import Count

def home(request):
    paints = Paint.objects.all().order_by('-id')[:6]
    category_class = Post.objects.filter(category='모임').order_by('-id')[:6]
    category_anonymous = Post.objects.filter(category='익명').order_by('-id')[:6]
    
    context = {
        'paints': paints,
        'category_class' : category_class,
        'category_anonymous' : category_anonymous,
    }

    return render(request, 'home.html', context)


def aboutus(request):
    return render(request, 'aboutus.html')


def index(request):
    category_class = Post.objects.filter(category='모임').order_by('-id')
    page = request.GET.get('page', '1')
    section = request.GET.get('section', None)

    if section == 'popular':
        # 좋아요가 가장 많은 순으로 분류
        category_class = category_class.annotate(num_likes=Count('like_users')).order_by('-num_likes')
    elif section == 'recent':
        # 최근 작성글 순으로 분류
        category_class = category_class.order_by('-created_at')
    elif section == 'oldest':
        # 가장 오래된 글 순으로 분류
        category_class = category_class.order_by('created_at')
    tags = Post.tags.all()
    per_page = 5
    
    paginator = Paginator(category_class, per_page)
    page_obj = paginator.get_page(page)

    total_pages = paginator.num_pages

    context = {
        'category_class': page_obj,
        'section': section,
        'total_pages': total_pages,
        # 'tags': tags,
    }

    return render(request, 'posts/index.html', context)


def anonymous(request):
    category_class = Post.objects.filter(category='익명').order_by('-id')
    page = request.GET.get('page', '1')
    section = request.GET.get('section', None)

    if section == 'popular':
        # 좋아요가 가장 많은 순으로 분류
        category_class = category_class.annotate(num_likes=Count('like_users')).order_by('-num_likes')
    elif section == 'recent':
        # 최근 작성글 순으로 분류
        category_class = category_class.order_by('-created_at')
    elif section == 'oldest':
        # 가장 오래된 글 순으로 분류
        category_class = category_class.order_by('created_at')

    per_page = 3
    paginator = Paginator(category_class, per_page)
    page_obj = paginator.get_page(page)

    total_pages = paginator.num_pages

    context = {
        'category_class': page_obj,
        'section': section,
        'total_pages': total_pages,
    }
    return render(request, 'posts/anonymous.html', context)


@login_required
def create(request):
    global tracks
    category_choices = [
        ('모임', '모임'),
        ('익명', '익명'),
    ]
    selected_tracks = request.POST.getlist('selected_tracks[]')

    if request.method =='POST':
        tags = request.POST.get('tags').split(',')
        form = PostForm(request.POST, request.FILES)
        form.fields['category'].choices = category_choices
        if form.is_valid():
            post = form.save(commit= False)
            post.user = request.user
            post.save()
            for tag in tags:
                post.tags.add(tag.strip())

            if not selected_tracks:
                return redirect('posts:index')
            else:
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
                            new_track = PostTrack()
                            new_track.post = post
                            new_track.title = track['name']
                            new_track.artist = track['artists'][0]['name']
                            new_track.album = track['album']['name']
                            new_track.preview_url = track['preview_url']
                            new_track.user = request.user
                            new_track.image.save(f'{track_id}.jpg', ContentFile(img_temp.read()))

                    return redirect('posts:index')
    else:
        form = PostForm()
    form.fields['category'].choices = category_choices    
    context = {
        'form' : form,
    }
    return render(request, 'posts/create.html', context)


@login_required
def anonymous_create(request):
    global tracks
    category_choices = [
        ('익명', '익명'),
        ('모임', '모임'),
    ]
    selected_tracks = request.POST.getlist('selected_tracks[]')


    if request.method =='POST':
        tags = request.POST.get('tags').split(',')
        form = PostForm(request.POST, request.FILES)
        form.fields['category'].choices = category_choices
        if form.is_valid():
            post = form.save(commit= False)
            post.user = request.user
            post.save()
            for tag in tags:
                post.tags.add(tag.strip())

            if not selected_tracks:
                return redirect('posts:anonymous')
            else:
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
                            new_track = PostTrack()
                            new_track.post = post
                            new_track.title = track['name']
                            new_track.artist = track['artists'][0]['name']
                            new_track.album = track['album']['name']
                            new_track.preview_url = track['preview_url']
                            new_track.user = request.user
                            new_track.image.save(f'{track_id}.jpg', ContentFile(img_temp.read()))

                    return redirect('posts:anonymous')
    else:
        form = PostForm()
    form.fields['category'].choices = category_choices    
    context = {
        'form' : form,
    }
    return render(request, 'posts/anonymous_create.html', context)



@login_required
def detail(request, post_pk):
    post = Post.objects.get(pk=post_pk)
    comment_form = CommentForm()
    comment_likes = Comment.objects.filter(post=post).annotate(num_likes=Count('like_users')).order_by('-num_likes')[:3]
    comments = post.comments.all().order_by('created_at')
    comment_latest = post.comments.all().order_by('-created_at')
    comment_forms = []
    post_report_form = PostReportForm()
    comment_report_form = CommentReportForm()
    for comment in comments:
        u_comment_form = (
            comment,
            CommentForm(instance=comment),
        )
        comment_forms.append(u_comment_form)
    tags = post.tags.all()
    posts = Post.objects.exclude(user=request.user).order_by('like_users')
    music = PostTrack.objects.filter(post=post_pk)
    context ={
        'post' : post,
        'comment_forms': comment_forms,
        'comment_form': comment_form,
        'comments' : comments,
        'comment_latest': comment_latest,
        'tags' : tags,
        'posts' : posts,
        'music' : music,
        'comment_likes' : comment_likes,
        'post_report_form' : post_report_form,
        'comment_report_form' : comment_report_form,
    }

    return render(request, 'posts/detail.html', context)

import uuid

def generate_anonymous_id():
    return str(uuid.uuid4())[:6]

@login_required
def anonymous_detail(request, post_pk):
    post = Post.objects.get(pk=post_pk)
    post_report_form = PostReportForm()
    comment_report_form = CommentReportForm()
    comment_form = CommentForm()
    comments = post.comments.all().order_by('created_at')
    comment_latest = post.comments.all().order_by('-created_at')
    comment_likes = Comment.objects.filter(post=post).annotate(num_likes=Count('like_users')).order_by('-num_likes')[:3]
    comment_forms = []
    for comment in comments:
        u_comment_form = (
            comment,
            CommentForm(instance=comment)
        )
        comment_forms.append(u_comment_form) 
    tags = post.tags.all()
    posts = Post.objects.exclude(user=request.user).order_by('like_users')
    music = PostTrack.objects.filter(post=post_pk)
    context ={
        'post' : post,
        'comment_forms': comment_forms,
        'comment_form': comment_form,
        'comment_latest' : comment_latest,
        'comments' : comments,
        'tags' : tags,
        'posts' : posts,
        'music' : music,
        'comment_likes' : comment_likes,
        'post_report_form' : post_report_form,
        'comment_report_form' : comment_report_form,
    }

    # Generate or retrieve anonymous ID for the current user
    anonymous_id = request.session.get('anonymous_id')
    if not anonymous_id:
        anonymous_id = generate_anonymous_id()
        request.session['anonymous_id'] = anonymous_id
    context['anonymous_id'] = anonymous_id
    
    return render(request, 'posts/anonymous_detail.html', context)

@login_required
def update(request, post_pk):
    category_choices = [
        ('모임', '모임'),
        ('익명', '익명'),
    ]
    post = Post.objects.get(pk=post_pk)
    music = PostTrack.objects.filter(post=post_pk)
    if request.user == post.user or request.user.is_superuser:
        if request.method == 'POST':
            selected_tracks = request.POST.getlist('selected_tracks[]')
            form = PostForm(request.POST, request.FILES, instance=post)
            form.fields['category'].choices = category_choices
            if form.is_valid():
                tags = request.POST.get('tags').split(',')
                for tag in tags:
                    post.tags.add(tag.strip())
                form.save()
            
                if not selected_tracks:
                        return redirect('posts:index')
                else:
                    if music.exists():
                        for track in music:
                            if request.user == track.user:
                                if track.image:  
                                    image_path = os.path.join(settings.MEDIA_ROOT, str(track.image))
                                    if os.path.isfile(image_path):
                                        os.remove(image_path)
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
                            new_track = PostTrack()
                            new_track.post = post
                            new_track.title = track['name']
                            new_track.artist = track['artists'][0]['name']
                            new_track.album = track['album']['name']
                            new_track.preview_url = track['preview_url']
                            new_track.user = request.user
                            new_track.image.save(f'{track_id}.jpg', ContentFile(img_temp.read()))

                return redirect('posts:detail', post.pk)

        else:
            form = PostForm(instance=post)
    else:
        return redirect('posts:detail', post.pk)
    form.fields['category'].choices = category_choices
    context = {
        'post' : post,
        'form' : form,
        'music' : music,
    }
    return render(request, 'posts/update.html', context)


@login_required
def anonymous_update(request, post_pk):
    category_choices = [
        ('모임', '모임'),
        ('익명', '익명'),
    ]
    post = Post.objects.get(pk=post_pk)
    music = PostTrack.objects.filter(post=post_pk)
    if request.user == post.user or request.user.is_superuser:
        if request.method == 'POST':
            selected_tracks = request.POST.getlist('selected_tracks[]')
            form = PostForm(request.POST, request.FILES, instance=post)
            form.fields['category'].choices = category_choices
            if form.is_valid():
                tags = request.POST.get('tags').split(',')
                for tag in tags:
                    post.tags.add(tag.strip())
                form.save()
            
                if not selected_tracks:
                        return redirect('posts:anonymous')
                else:
                    if music.exists():
                        for track in music:
                            if request.user == track.user:
                                if track.image:  
                                    image_path = os.path.join(settings.MEDIA_ROOT, str(track.image))
                                    if os.path.isfile(image_path):
                                        os.remove(image_path)
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
                            new_track = PostTrack()
                            new_track.post = post
                            new_track.title = track['name']
                            new_track.artist = track['artists'][0]['name']
                            new_track.album = track['album']['name']
                            new_track.preview_url = track['preview_url']
                            new_track.user = request.user
                            new_track.image.save(f'{track_id}.jpg', ContentFile(img_temp.read()))

                return redirect('posts:anonymous_detail', post.pk)

        else:
            form = PostForm(instance=post)
    else:
        return redirect('posts:anonymous_detail', post.pk)
    form.fields['category'].choices = category_choices
    context = {
        'post' : post,
        'form' : form,
        'music' : music,
    }
    return render(request, 'posts/anonymous_update.html', context)


@login_required
def delete(request,post_pk):
    post = Post.objects.get(pk=post_pk)
    music_queryset = PostTrack.objects.filter(post=post_pk)
    if request.user == post.user or request.user.is_superuser:
        for music in music_queryset:
            if music.image:  
                image_path = os.path.join(settings.MEDIA_ROOT, str(music.image))
                if os.path.isfile(image_path):
                    os.remove(image_path)

        post.delete()
    return redirect('posts:index')

@login_required
def anonymous_delete(request,post_pk):
    post = Post.objects.get(pk=post_pk)
    music_queryset = PostTrack.objects.filter(post=post_pk)
    if request.user == post.user:
        for music in music_queryset:
            if music.image:  
                image_path = os.path.join(settings.MEDIA_ROOT, str(music.image))
                if os.path.isfile(image_path):
                    os.remove(image_path)

        post.delete()
    return redirect('posts:anonymous')



def likes(request, post_pk):
    post = Post.objects.get(pk=post_pk)
    if post.like_users.filter(pk=request.user.pk).exists():
        post.like_users.remove(request.user)
    else:
        post.like_users.add(request.user)

    # 이전 페이지로 리디렉션
    referer = request.META.get('HTTP_REFERER') # 이전 페이지의 url을 가져옴
    if referer:
        return redirect(referer)
    
    return redirect('posts:index')

def anonymous_likes(request, post_pk):
    post = Post.objects.get(pk=post_pk)
    if post.like_users.filter(pk=request.user.pk).exists():
        post.like_users.remove(request.user)
    else:
        post.like_users.add(request.user)

    # 이전 페이지로 리디렉션
    referer = request.META.get('HTTP_REFERER') # 이전 페이지의 url을 가져옴
    if referer:
        return redirect(referer)
    
    return redirect('posts:anonymous')

@login_required
def post_report(request, post_pk):
    post = Post.objects.get(pk=post_pk)
    form = PostReportForm()
    if request.method == 'POST':
        form = PostReportForm(request.POST)
        if form.is_valid():
            post_report = form.save(commit=False)
            post_report.post = post
            post_report.user = request.user
            post_report.save()
            # 신고 당한 사람 표시
            post.user.reported = True
            post.user.save()
            post.report = True
            post.save()
            return redirect('posts:detail', post_pk)
            
    # context = {
    #     'post_report_form': form,
    #     'post_pk' : post_pk,
    # }
    # return render(request, 'posts/post_report.html', context)


def comment_create(request, post_pk):
    post = Post.objects.get(pk=post_pk)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.category = post.category  # 혹은 다른 문자열 값
            comment.user = request.user
            comment.save()
            return redirect('posts:detail', post.pk)
        
def anonymous_comment_create(request, post_pk):
    post = Post.objects.get(pk=post_pk)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.category = post.category  # 혹은 다른 문자열 값
            comment.user = request.user
            comment.save()
            return redirect('posts:anonymous_detail', post.pk)


def comment_update(request, post_pk, comment_pk):
    comment = Comment.objects.get(pk=comment_pk)
    if request.user == comment.user:
        if request.method == 'POST':
            comment_form = CommentForm(request.POST, instance=comment)
            if comment_form.is_valid():
                comment_form.save()
                return redirect('posts:detail', post_pk)
                # return JsonResponse({'status': 'success'})
        else:
            comment_form = CommentForm(instance=comment)
        context = {
            'comment_form': comment_form,
            'comment': comment,
        }
        return render(request, 'posts/detail.html', context)


def anonymous_comment_update(request, post_pk, comment_pk):
    comment = Comment.objects.get(pk=comment_pk)
    comment_form = CommentForm(request.POST, instance=comment)
    if request.user == comment.user:
        if request.method == 'POST':
            comment_form = CommentForm(request.POST, instance=comment)
            if comment_form.is_valid():
                comment_form.save()
                return redirect('posts:anonymous_detail', post_pk)
        else:
            comment_form = CommentForm(instance=comment)  # 인스턴스 설정
    context = {
        'comment_form': comment_form,
        'comment': comment,
    }
    return redirect('posts:anonymous_detail', context)

def comment_delete(request, post_pk, comment_pk):
    comment = Comment.objects.get(pk=comment_pk)
    if request.user == comment.user:
        comment.delete()
    return redirect('posts:detail', post_pk)

def anonymous_comment_delete(request, post_pk, comment_pk):
    comment = Comment.objects.get(pk=comment_pk)
    if request.user == comment.user:
        comment.delete()
    return redirect('posts:anonymous_detail', post_pk)

@login_required
def comment_report(request, post_pk, comment_pk):
    comment = Comment.objects.get(pk=comment_pk)
    form = CommentReportForm()

    if request.method == 'POST':
        form = CommentReportForm(request.POST)
        if form.is_valid():
            comment_report = form.save(commit=False)
            comment_report.comment = comment
            comment_report.user = request.user
            comment_report.save()
            # 신고 당한 사람 표시
            comment.user.reported = True
            comment.user.save()
            comment.report = True
            comment.save()
            return redirect('posts:detail', post_pk)
            
    # context = {
    #     'comment_report_form': form,
    #     'post_pk' : post_pk,
    #     'comment_pk' : comment_pk,
    # }
    # return render(request, 'posts/comment_report.html', context)

# @login_required
def comment_likes(request, post_pk, comment_pk):
    comment = Comment.objects.get(pk=comment_pk)
    if comment.like_users.filter(pk=request.user.pk).exists():
        comment.like_users.remove(request.user)
    else:
        comment.like_users.add(request.user)
    return redirect('posts:detail', post_pk)

def anonymous_comment_likes(request, post_pk, comment_pk):
    comment = Comment.objects.get(pk=comment_pk)
    if comment.like_users.filter(pk=request.user.pk).exists():
        comment.like_users.remove(request.user)
    else:
        comment.like_users.add(request.user)
    return redirect('posts:anonymous_detail', post_pk)


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
            return render(request, 'posts/search_results.html', context)

    return render(request, 'posts/create.html')


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

# 포춘쿠키
from django.utils import timezone
import random

def fortune_cookie(request):
    current_date = timezone.now().date()

    # 현재 사용자의 과거 운세가 있는지 확인 후 지우기
    user = request.user
    past_fortunes = Fortune.objects.filter(date__lt=current_date, user=user)
    past_fortunes.delete()
    # 오늘 날짜와 현재 사용자에 대한 기존 운세가 있는지 확인
    fortune = Fortune.objects.filter(date=current_date, user=user).first()

    if not fortune:
        # 새로운 운세 설정
        fortunes = [
            "오늘의 키 포인트는 미소입니다.당신은 웃는 얼굴이 매력입니다.",
            "예상치 못한 시점에 원하는 자리에 도달해 있을거예요. 이미 이만큼 왔는걸요.",
            "오늘 행운의 색은 파랑색 입니다. 쿨한 모습이 행운을 가져다줍니다.",
            "감수성이 예민한 사람이군요. 힘들 땐 잠시 멈춰 스스로를 어루만져 주세요.",
            "이해하기 힘든 사람에게 말을 걸어 보십시오. 생각지 못한 것들을 보게될거예요."
        ]
        random_fortune = random.choice(fortunes)

        # Save the new fortune in the database associated with the current user
        fortune = Fortune.objects.create(user=user, message=random_fortune, date=current_date)

    context = {'fortune': fortune}
    return redirect('accounts:profile',user.username)