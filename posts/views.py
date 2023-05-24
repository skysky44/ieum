from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import PostForm, CommentForm
from .models import Post, Comment

def home(request):
    return render(request, 'home.html')

def index(request):
    posts = Post.objects.all()
    
    context = {
        'posts': posts
    }

    return render(request, 'posts/index.html', context)




# def create(request):
#     if request.method =='POST':
#         tags = request.POST.get('tags').split(',')
#         form = PostForm(request.POST, request.FILES)
#         image_form = PostImageForm(request.POST, request.FILES)
#         if form.is_valid():
#             post = form.save(commit= False)
#             post.user = request.user
#             post.save()
#             for tag in tags:
#                 post.tags.add(tag.strip())
#             for image in request.FILES.getlist('image'): 
#                 PostImage.objects.create(post=post, image=image)
#             return redirect('posts:detail', post.pk)
        
#     else:
#         form = PostForm()
#         image_form = PostImageForm()
#     context = {
#         'form' : form,
#         'image_form': image_form,
#     }
#     return render(request, 'posts/create.html', context)
@login_required
def create(request):
    if request.method =='POST':
        tags = request.POST.get('tags').split(',')
        form = PostForm(request.POST)
        # image_form = PostImageForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit= False)
            post.user = request.user
            post.save()
            
            # for image in request.FILES.getlist('image'): 
            #     PostImage.objects.create(post=post, image=image)

            for tag in tags:
                post.tags.add(tag.strip())
            return redirect('posts:detail', post.pk)
        
    else:
        form = PostForm()
    context = {
        'form' : form,
        # 'image_form': image_form,
    }
    return render(request, 'posts/create.html', context)


def detail(request, post_pk):
    post = Post.objects.get(pk=post_pk)
    comment_form = CommentForm()
    comments = post.comments.all()
    tags = post.tags.all()
    posts = Post.objects.all().order_by('like_users')
    
    context ={
        'post' : post,
        'comment_form':comment_form,
        'comments' : comments,
        'tags' : tags,
        'posts' : posts,
    }

    return render(request, 'posts/detail.html', context)


# @login_required
def update(request, post_pk):
    post = Post.objects.get(pk=post_pk)
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            tags = request.POST.get('tags').split(',')
            for tag in tags:
                post.tags.add(tag.strip())
            form.save()


            return redirect('posts:detail', post.pk)

    else:
        form = PostForm(instance=post)
    context = {
        'post' : post,
        'form' : form,
    }
    return render(request, 'posts/update.html', context)


# @login_required
def delete(request,post_pk):
    post = Post.objects.get(pk=post_pk)
    if request.user == post.user:
        post.delete()
    return redirect('posts:index')


# @login_required
def likes(request, post_pk):
    post = Post.objects.get(pk=post_pk)
    if post.like_users.filter(pk=request.user.pk).exists():
        post.like_users.remove(request.user)
    else:
        post.like_users.add(request.user)
    return redirect('posts:detail', post.pk)




def comment_create(request, post_pk):
    post = Post.objects.get(pk=post_pk)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.user = request.user
            comment.save()
            return redirect('posts:detail', post.pk)


def comment_update(request, post_pk, comment_pk):
    post = Post.objects.get(pk=post_pk)
    comment = Comment.objects.get(pk=comment_pk)
    comment_form = CommentForm(instance=comment)
    if request.user == comment.user:
        if request.method == 'POST':
            form = CommentForm(request.POST, instance=comment)
            if form.is_valid():
                form.save()
                return redirect('posts:detail', post.pk)
        else:
            form = CommentForm(instance=comment)
    context = {
        'post': post,
        'comment' : comment,
        'comment_form': comment_form,
    
    }
    return render(request, 'posts/detail.html', context)

def comment_delete(request, post_pk, comment_pk):
    comment = Comment.objects.get(pk=comment_pk)
    if request.user == comment.user:
        comment.delete()
    return redirect('posts:detail', post_pk)


# @login_required
def comment_likes(request, post_pk, comment_pk):
    comment = Comment.objects.get(pk=comment_pk)
    if comment.like_users.filter(pk=request.user.pk).exists():
        comment.like_users.remove(request.user)
    else:
        comment.like_users.add(request.user)
    return redirect('posts:detail', post_pk)




