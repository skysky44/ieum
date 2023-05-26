
# from .models import 
# Create your views here.
from django.shortcuts import render, redirect
from .models import Question, Result
from .forms import QuestionForm
from django.http import JsonResponse



def index(request):
    questions = Question.objects.all()
        
    context ={
        'questions' : questions,
    }


    return render(request, 'balances/index.html', context)

def create(request):
    if request.method =='POST':
        form = QuestionForm(request.POST, request.FILES)
        if form.is_valid():
            question = form.save(commit= False)
            question.user = request.user
            question.save()
        return redirect('balances:index')
    else:
        form = QuestionForm()
    context = {
        'form' : form,
    }
    return render(request, 'balances/create.html', context)


def detail(request, question_pk):
    question = Question.objects.get(pk=question_pk)
    
    context ={
        'question' : question,
    }

    return render(request, 'balances/detail.html', context)


# def answer(request, question_pk, select_answer):
#     question = Question.objects.get(pk=question_pk)
  
    
#     if request.method == 'POST':
#         if select_answer == 1:
#             pass
#         elif select_answer == 2:
#             pass
#     return redirect('question:detail', question_pk )

# def answer(request, question_pk, select_answer):
#     question = Question.objects.get(pk=question_pk)
#     user = request.user

#     if request.method == 'POST':
#         result, created = Result.objects.get_or_create(user=user)

#         # Get the user's chosen results list
#         chosen_results = result.chosen_result

#         if isinstance(chosen_results, tuple):
#             chosen_results = list(chosen_results)

#         # Append the selected answer to the list
            
#             chosen_results.append(select_answer)

#             # Update the chosen results list in the Result model
#             result.chosen_result = chosen_results
#             result.save()

#     return redirect('balances:detail', question_pk)

def answer(request, question_pk, select_answer):
    question = Question.objects.get(pk=question_pk)
    user = request.user

    if request.method == 'POST':
        result, created = Result.objects.get_or_create(user=user)

        # Get the user's chosen results dictionary
        chosen_results = result.chosen_result

        # Check if chosen_results is empty and initialize it as an empty dictionary if so
        if not chosen_results:
            chosen_results = {}

        # Append the selected answer to the dictionary
        chosen_results[str(question_pk)] = select_answer

        # Update the chosen results dictionary in the Result model
        result.chosen_result = chosen_results
        result.save()

    return redirect('balances:detail', question_pk)


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
