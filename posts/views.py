from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from .forms import PostForm, CommentForm
from .models import Post, Comment
from paints.models import Paint
from .models import PostTrack
import os
from django.conf import settings
from django.core.files.base import ContentFile
import urllib.request
import tempfile
import requests

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

def index(request):
    # posts = Post.objects.order_by('-pk')
    category_class = Post.objects.filter(category='모임').order_by('-id')
    page = request.GET.get('page', '1')
    tags = Post.tags.all()
    per_page = 5
    paginator = Paginator(category_class, per_page)
    page_obj = paginator.get_page(page)
    
    context = {
        'tags': tags,
        # 'posts': page_obj,
        'category_class' : page_obj,
    }

    return render(request, 'posts/index.html', context)

def anonymous(request):
    # posts = Post.objects.order_by('-pk')
    category_anonymous = Post.objects.filter(category='익명').order_by('-id')
    per_page = 5
    paginator = Paginator(category_anonymous, per_page)
    page = request.GET.get('page', '1')
    page_obj = paginator.get_page(page)
    tags = Post.tags.all()
    context ={
        'category_anonymous' : page_obj,
        'tags' : tags,
        # 'posts' : page_obj

    }
    return render(request, 'posts/anonymous.html',context)

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
    comments = post.comments.all()
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
        'comments' : comments,
        'tags' : tags,
        'posts' : posts,
        'music' : music,
    }

    return render(request, 'posts/detail.html', context)

import uuid

def generate_anonymous_id():
    return str(uuid.uuid4())[:6]

@login_required
def anonymous_detail(request, post_pk):
    post = Post.objects.get(pk=post_pk)
    comment_form = CommentForm()
    comments = post.comments.all()
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
        'comments' : comments,
        'tags' : tags,
        'posts' : posts,
        'music' : music,
    }

    # Generate or retrieve anonymous ID for the current user
    anonymous_id = request.session.get('anonymous_id')
    if not anonymous_id:
        anonymous_id = generate_anonymous_id()
        request.session['anonymous_id'] = anonymous_id
    context['anonymous_id'] = anonymous_id
    
    return render(request, 'posts/anonymous_detail.html', context)

# @login_required
# def anonymous_detail(request, post_pk):
#     post = Post.objects.get(pk=post_pk)
#     comment_form = CommentForm()
#     comments = post.comments.all()
#     tags = post.tags.all()
#     posts = Post.objects.all().order_by('like_users')
#     music = PostTrack.objects.filter(post=post_pk)
#     context ={
#         'post' : post,
#         'comment_form':comment_form,
#         'comments' : comments,
#         'tags' : tags,
#         'posts' : posts,
#         'music' : music,
#     }

#     return render(request, 'posts/anonymous_detail.html', context)


@login_required
def update(request, post_pk):
    category_choices = [
        ('모임', '모임'),
        ('익명', '익명'),
    ]
    post = Post.objects.get(pk=post_pk)
    music = PostTrack.objects.filter(post=post_pk)
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
    if request.user == post.user:
        for music in music_queryset:
            if music.image:  
                image_path = os.path.join(settings.MEDIA_ROOT, str(music.image))
                if os.path.isfile(image_path):
                    os.remove(image_path)

        post.delete()
    return redirect('posts:index')



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

# @login_required
def comment_likes(request, post_pk, comment_pk):
    comment = Comment.objects.get(pk=comment_pk)
    if comment.like_users.filter(pk=request.user.pk).exists():
        comment.like_users.remove(request.user)
    else:
        comment.like_users.add(request.user)
    return redirect('posts:detail', post_pk)


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

