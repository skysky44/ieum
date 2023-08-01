from django.shortcuts import render, redirect, get_object_or_404
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
from django.http import JsonResponse

def home(request):
    paints = Paint.objects.all().order_by('-id')[:6]
    if request.user.is_authenticated:     
        if request.user.taste == 'T' :
            category_class = Post.objects.exclude(category='익명').filter(user__taste='T').order_by('-id')
            category_class = category_class.annotate(num_likes=Count('like_users')).order_by('-num_likes')[:4]
        elif request.user.taste == 'F' :
            category_class = Post.objects.exclude(category='익명').filter(user__taste='F').order_by('-id')
            category_class = category_class.annotate(num_likes=Count('like_users')).order_by('-num_likes')[:4]
        elif request.user.taste == 'N':
            category_class = Post.objects.exclude(category='익명').order_by('-id')[:4]
    else:
        category_class = Post.objects.exclude(category='익명').order_by('-id')[:4]
        

    category_anonymous = Post.objects.filter(category='익명').order_by('-id')[:4]


    # image_urls를 리스트로 변환
    for post in category_class:
        post.image_urls = post.image_urls.split(',')
    for post in category_anonymous:
        post.image_urls = post.image_urls.split(',')

    context = {
        'paints': paints,
        'category_class' : category_class,
        'category_anonymous' : category_anonymous,
    }

    return render(request, 'home.html', context)


def aboutus(request):
    return render(request, 'aboutus.html')

from django.db.models import Q
# 검색 기능
def main_search(request):
    query = request.GET.get('query')

    if query:
        meeting_posts = Post.objects.filter(
            ~Q(category__icontains='익명'),
            Q(title__icontains=query) | Q(content__icontains=query)
        )

        anonymous_posts = Post.objects.filter(
            Q(category__icontains='익명'),
            Q(title__icontains=query) | Q(content__icontains=query)
        )


    context = {
        'query': query,
        'meeting_posts': meeting_posts,
        'anonymous_posts': anonymous_posts,
    }
    return render(request, 'posts/main_search_results.html', context)


from bs4 import BeautifulSoup
def extract_image_urls(content):
    soup = BeautifulSoup(content, 'html.parser')
    image_tags = soup.find_all('img')
    image_urls = [tag['src'] for tag in image_tags]
    return image_urls


def index(request):
    if request.user.is_authenticated:
        if request.user.taste == 'T' :
            category_class = Post.objects.exclude(category='익명').filter(user__taste='T').order_by('-id')
        elif request.user.taste == 'F' :
            category_class = Post.objects.exclude(category='익명').filter(user__taste='F').order_by('-id')
        else:
            category_class = Post.objects.exclude(category='익명').order_by('-id')
    else:
        category_class = Post.objects.exclude(category='익명').order_by('-id')
    
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
    per_page = 6
    paginator = Paginator(category_class, per_page)
    page_obj = paginator.get_page(page)

    total_pages = paginator.num_pages

    for post in page_obj:
        post.image_urls = extract_image_urls(post.content)

    context = {
        'category_class': page_obj,
        'section': section,
        'total_pages': total_pages,
        'per_page' : per_page,
        'tags': tags,
        'post_image_urls': [post.image_urls for post in page_obj],
        # 'co'
    }

    return render(request, 'posts/index.html', context)

@login_required
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
    tags = Post.tags.all()
    per_page = 6
    
    paginator = Paginator(category_class, per_page)
    page_obj = paginator.get_page(page)

    total_pages = paginator.num_pages

    for post in page_obj:
        post.image_urls = extract_image_urls(post.content)

    context = {
        'category_class': page_obj,
        'section': section,
        'total_pages': total_pages,
        'tags': tags,
        'post_image_urls': [post.image_urls for post in page_obj],
    }
    return render(request, 'posts/anonymous.html', context)


@login_required
def create(request):
    global tracks
    category_choices = [
        ('맛집', '맛집'),
        ('음악', '음악'),
        ('운동', '운동'),
        ('게임', '게임'),
        ('여행', '여행'),
        ('일상', '일상'),
        ('기타', '기타'),
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
    address = ""
    if post.address:
        address = post.address
    else:
        address = ""
    
    comment_form = CommentForm()
    comment_likes = Comment.objects.filter(post=post).annotate(num_likes=Count('like_users')+1).filter(num_likes__gt=1).order_by('-num_likes')[:3]
    comments = post.comments.all().order_by('created_at')
    comment_latest = post.comments.all().order_by('-created_at')
    comment_forms = []
    post_report_form = PostReportForm()
    comment_report_form = CommentReportForm()
    if request.user.is_authenticated:
        if request.user.taste == 'T' :
            category_class = Post.objects.exclude(category='익명').filter(user__taste='T').order_by('-id')
        elif request.user.taste == 'F' :
            category_class = Post.objects.exclude(category='익명').filter(user__taste='F').order_by('-id')
    previous_post = category_class.filter(id__lt=post_pk).order_by('-id').first()
    next_post = category_class.filter(id__gt=post_pk).order_by('id').first()
    for comment in comments:
        u_comment_form = (
            comment,
            CommentForm(instance=comment),
        )
        comment_forms.append(u_comment_form)
    tags = post.tags.all()
    posts = Post.objects.exclude(user=request.user).order_by('like_users')
    music = PostTrack.objects.filter(post=post_pk)

    # 조회수 증가
    post.view_count += 1
    post.save()
    
    # image_urls를 리스트로 변환
    post.image_urls = extract_image_urls(post.content)
    # post.image_urls = post.image_urls.split(', ')


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
        'post.image_urls' : post.image_urls,
        'previous_post': previous_post,
        'next_post': next_post,
        'address':address,
    }

    return render(request, 'posts/detail.html', context)


@login_required
def anonymous_detail(request, post_pk):
    post = Post.objects.get(pk=post_pk)
    address = ""
    if post.address:
        address = post.address
    else:
        address = ""
    comment_form = CommentForm()
    comment_likes = Comment.objects.filter(post=post).annotate(num_likes=Count('like_users')+1).filter(num_likes__gt=1).order_by('-num_likes')[:3]
    comments = post.comments.all().order_by('created_at')
    comment_latest = post.comments.all().order_by('-created_at')
    comment_forms = []
    post_report_form = PostReportForm()
    comment_report_form = CommentReportForm()
    category_class = Post.objects.filter(category='익명').order_by('-id')
    previous_post = category_class.filter(id__lt=post_pk).order_by('-id').first()
    next_post = category_class.filter(id__gt=post_pk).order_by('id').first()
    for comment in comments:
        u_comment_form = (
            comment,
            CommentForm(instance=comment),
        )
        comment_forms.append(u_comment_form)
    tags = post.tags.all()
    posts = Post.objects.exclude(user=request.user).order_by('like_users')
    music = PostTrack.objects.filter(post=post_pk)

    # 조회수 증가
    post.view_count += 1
    post.save()
    
    # image_urls를 리스트로 변환
    post.image_urls = extract_image_urls(post.content)
    # post.image_urls = post.image_urls.split(', ')
    


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
        'post.image_urls' : post.image_urls,
        'previous_post': previous_post,
        'next_post': next_post,
        'address' : address,
    }

    return render(request, 'posts/anonymous_detail.html', context)


@login_required
def update(request, post_pk):
    category_choices = [
        ('맛집', '맛집'),
        ('음악', '음악'),
        ('운동', '운동'),
        ('게임', '게임'),
        ('여행', '여행'),
        ('일상', '일상'),
        ('기타', '기타'),
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
                        return redirect('posts:detail', post_pk)
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
        ('익명', '익명')
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
                        return redirect('posts:anonymous_detail', post.pk)
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
        is_liked = False
    else:
        post.like_users.add(request.user)
        is_liked = True

    # # 이전 페이지로 리디렉션
    # referer = request.META.get('HTTP_REFERER') # 이전 페이지의 url을 가져옴
    # if referer:
    #     return redirect(referer)

    context = {
        'is_liked': is_liked,
        'like_count': post.like_users.count(),
    }
    
    return JsonResponse(context)


def anonymous_likes(request, post_pk):
    post = Post.objects.get(pk=post_pk)
    if post.like_users.filter(pk=request.user.pk).exists():
        post.like_users.remove(request.user)
        is_liked = False
    else:
        post.like_users.add(request.user)
        is_liked = True

    # # 이전 페이지로 리디렉션
    # referer = request.META.get('HTTP_REFERER') # 이전 페이지의 url을 가져옴
    # if referer:
    #     return redirect(referer)

    context = {
        'is_liked': is_liked,
        'like_count': post.like_users.count(),
    }
    
    return JsonResponse(context)


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
            post_report.save()
            return redirect('posts:detail', post_pk)
            
    # context = {
    #     'post_report_form': form,
    #     'post_pk' : post_pk,
    # }
    # return render(request, 'posts/post_report.html', context)


@login_required
def anonymous_post_report(request, post_pk):
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
            post_report.save()
            return redirect('posts:anonymous_detail', post_pk)


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
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False, 'errors': form.errors})

        
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
            comment_report.save()
            return redirect('posts:detail', post_pk)
        

@login_required
def anonymous_comment_report(request, post_pk, comment_pk):
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
            comment_report.save()
            return redirect('posts:anonymous_detail', post_pk)
            
    # context = {
    #     'comment_report_form': form,
    #     'post_pk' : post_pk,
    #     'comment_pk' : comment_pk,
    # }
    # return render(request, 'posts/comment_report.html', context)

# @login_required
# def comment_likes(request, post_pk, comment_pk):
#     comment = Comment.objects.get(pk=comment_pk)
#     if comment.like_users.filter(pk=request.user.pk).exists():
#         comment.like_users.remove(request.user)
#     else:
#         comment.like_users.add(request.user)
#     return redirect('posts:detail', post_pk)


def comment_likes(request, post_pk, comment_pk):
    comment = Comment.objects.get(pk=comment_pk)
    if comment.like_users.filter(pk=request.user.pk).exists():
        comment.like_users.remove(request.user)
        liked = False
    else:
        comment.like_users.add(request.user)
        liked = True
    
    like_count = comment.like_users.count()
    
    response_data = {
        'liked': liked,
        'like_count': like_count,
    }
    
    return JsonResponse(response_data)


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

    return render(request, 'posts/search_results.html')


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
            "이해하기 힘든 사람에게 말을 걸어 보십시오. 생각지 못한 것들을 보게될거예요.",
            "상대방과의 대화를 위해서는 화려한 지식이 아니라 공감이 필요합니다.",
            "당신의 몫은 당신이 정합니다. 현재 가진 걸 바꾸고 싶다면 먼저 행동해야 합니다.",
            "오늘 행운의 색은 흰 색 입니다. 당신의 순수한 매력을 보여주세요.",
            "애정운이 좋은 시기입니다. 그 사람에게 적극적으로 다가가보세요.",
            "스스로를 낮추지 말고 본인의 장점을 찾아보세요. 당신은 생각보다 멋진 사람입니다.",
            "친구,가족에게 작은 선물을 해보세요. 행복해질거예요.",
            "다가올 내일보다 중요한 것은 지금 살고 있는 현재입니다. 미래를 위해 현재를 포기하지마세요.",
            "이번 주 행운의 아이템은 볼펜입니다.",
            "오늘은 어제보다 내일은 오늘보다 더 좋은 하루가 되겠습니다.",
            "혼자 고민하지 말고 용기내어 주변 사람들과 상의해보세요.",
            "행복의 가장 큰 위해요소는 남과 비교하는 것 입니다. 비교하지 마세요. 당신은 소중합니다.",
            "당신에게 필요한 것은 적절한 시기를 기다릴 줄 아는 여유입니다.",
            "오늘 행운의 색은 검은색 입니다. 시크한 아이템을 선택해보세요.",
            "당분간 지켜보는 것이 좋습니다. 타이밍이 중요합니다.",
            "발 밑만 보며 걷다보면예상치 못한 길로 갈 수 있습니다. 멀리 보고 진행하시길!",
            "과거에 얽매여 힘들어하지 마세요. 중요한 것은 지금 현재입니다.",
            "지루한 일상에는여행이나 새로운 경험이 도움이 됩니다.",
            "오늘 행운의 색은 노란색 입니다. 밝고 발랄한 미소가 포인트예요.",
            "힘들어도 이겨내고 앞으로 나가는 당신의 모습이 아름답습니다. 더 좋은 날이 올 거예요.",
            "작은 말이라도, 칭찬해보세요. 칭찬은 고래도 춤추게 한다잖아요.",
            "할까말까 고민되는 일이 있다면이것을 했을 때 후회할 것인가 생각해보세요.",
            "주변의 소중한 사람들에게 사랑한다고 말해보세요.",
            "그동안 모르고 있었던 재능이 발현되는 날입니다. 새로운 일도 두려워마세요.",
            "다가오는 기회가 좋은 결과를 가져오겠습니다. 과거의 좋았던 일에 미련을 갖지 마세요.",
            "오늘 행운의 색은 붉은색 입니다. 열정적인 모습을 보여주세요.",
            "즐기는 자를 이길 수 있는 사람은 없다고 했습니다. 즐거운 방법을 찾아보세요.",
            "결단력이 필요한 때 입니다. 주저하면 기회를 놓치게 됩니다.",
            "직감이 놀랍게 상승하는 때입니다. 당신의 감을 믿고 도전해보세요.",
            "타인에게 베푼 작은 호의가 큰 행운으로 돌아오겠습니다.",
            "오늘은 기분 좋게 웃으며 하루를시작하시길 바랍니다.",
            "변화를 원한다면 NO를 이야기해보세요. 너무 YES만 해오지는 않았나요?",
            "실행력이 중요한 때입니다. 머릿속에 가지고 있는 생각을 실천하세요.",
            "설레는 일이 다가오고 있습니다. 마음의 준비를 하고 기다려보세요.",
            "사람을 움직이는 힘은 입이 아니라 귀에서 나옵니다. 잘 들어보세요.",
            "곧 큰 결정을 하게 될 시기가 올 것 같습니다. 긍정적인 결과가 예상됩니다.",
            "행운지수가 상승하였습니다! 예상치 못했던 수입이 들어올 수도 있습니다.",
            "당신의 어릴 적 꿈은 무엇이었나요? 그 꿈을 잊지마세요. 당신의 삶을 순수하게 지켜줍니다.",
            "기본에 충실해야 기둥이 세워집니다. 차근 차근 벽돌을 쌓아보세요.",
            "오늘은 무엇을 하든지 잘 될 거예요. 미루지 말고 시작해보세요.",
            "작은 차이가 명품을 만듭니다. 어떤 차이를 가지고 계신가요?",
            "당신은 시간이 지날수록 빛이 나는 사람입니다.",
        ]
        random_fortune = random.choice(fortunes)

        # Save the new fortune in the database associated with the current user
        fortune = Fortune.objects.create(user=user, message=random_fortune, date=current_date)

    context = {'fortune': fortune}
    return redirect('accounts:profile',user.username)
