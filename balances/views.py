from django.shortcuts import render
# from .models import 
# Create your views here.


def index(request):

    return render(request, 'index.html')


# def create(request):
#     if request.method =='POST':
#         form = PostForm(request.POST)
#         if form.is_valid():
#             post = form.save(commit= False)
#             post.user = request.user
#             post.save()
            
#             for tag in tags:
#                 post.tags.add(tag.strip())
#             return redirect('posts:detail', post.pk)
        
#     else:
#         form = PostForm()
#     context = {
#         'form' : form,
#         # 'image_form': image_form,
#     }
#     return render(request, 'posts/create.html', context)


# def detail(request, post_pk):
#     post = Post.objects.get(pk=post_pk)
#     comment_form = CommentForm()
#     comments = post.comments.all()
#     tags = post.tags.all()
#     posts = Post.objects.all().order_by('like_users')
    
#     context ={
#         'post' : post,
#         'comment_form':comment_form,
#         'comments' : comments,
#         'tags' : tags,
#         'posts' : posts,
#     }

#     return render(request, 'posts/detail.html', context)


# # @login_required
# def update(request, post_pk):
#     post = Post.objects.get(pk=post_pk)
#     if request.method == 'POST':
#         form = PostForm(request.POST, request.FILES, instance=post)
#         if form.is_valid():
#             tags = request.POST.get('tags').split(',')
#             for tag in tags:
#                 post.tags.add(tag.strip())
#             form.save()


#             return redirect('posts:detail', post.pk)

#     else:
#         form = PostForm(instance=post)
#     context = {
#         'post' : post,
#         'form' : form,
#     }
#     return render(request, 'posts/update.html', context)


# # @login_required
# def delete(request,post_pk):
#     post = Post.objects.get(pk=post_pk)
#     if request.user == post.user:
#         post.delete()
#     return redirect('posts:index')
