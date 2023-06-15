
# from .models import 
# Create your views here.
from django.shortcuts import render, redirect
from .models import Question, Result
from .forms import QuestionForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model

@login_required
def index(request):
    if request.user.is_superuser:
        questions = Question.objects.all()
            
        context ={
            'questions' : questions,
        }
        return render(request, 'balances/index.html', context)
    else:
        return redirect('posts:index')
    
def create(request):
    if request.user.is_superuser:
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
    else:
        return redirect('balances:index')

@login_required
def detail(request, question_pk):
    question = Question.objects.get(pk=question_pk)
    total = Question.objects.all().count()
    last = Question.objects.last()   
    context ={
        'question' : question,
        'last' : last,
        'total' : total,
    }
    return render(request, 'balances/detail.html', context)

@login_required
def answer(request, question_pk, select_answer):
    question = Question.objects.get(pk=question_pk)
    user = request.user
    User = get_user_model()

    if request.method == 'POST':
        result, created = Result.objects.get_or_create(user=user)
        user_score = user.score

        # Get the user's chosen results dictionary
        chosen_results = result.chosen_result

        # Check if chosen_results is empty and initialize it as an empty dictionary if so
        if not chosen_results:
            chosen_results = {}

        # Append the selected answer to the dictionary
        chosen_results[str(question_pk)] = select_answer

        # Update the chosen_results field in the Result model
        result.chosen_result = chosen_results
        result.save()

        # 유저의 워드 딕셔너리 만들기
        word_list = result.word
        if not word_list:
            word_list = {}
        
        # 워드 값이 있는 경우에만 딕셔너리 만들어주기
        if question.word1 != "" and question.word2 != "":

            if select_answer == 1:
                selected_word = question.word1
            elif select_answer == 2:
                selected_word = question.word2
            # Split the selected_word by comma (or any other delimiter you prefer)
            selected_words = selected_word.split(',')

            # Append the selected words to the list
            word_list[str(question_pk)] = selected_words
            # word_list.extend(selected_words)

            # Update the word list in the Result model
            result.word = word_list
            result.save()
        # 점수 매기기
        if question_pk <= 18:
            if question_pk == 6 or question_pk == 7 or question_pk == 9 or question_pk == 10:
                pass
            else:
                # 질문 번호가 홀수인지 짝수인지 확인
                if question_pk % 2 == 1:
                    # 홀수 번호의 질문에서 답변 1을 선택한 경우 10점 감점 F가 1번
                    if select_answer == 1:
                        user_score -= 10
                if question_pk % 2 == 0:
                    # 짝수 번호의 질문에서 답변 2을 선택한 경우 10점 감점 F가 2번
                    if select_answer == 2:
                        user_score -= 10
            # Result 모델의 score 필드 업데이트
            user.score = user_score
            user.save()
        # question_pk가 13인 경우에 user_score 필드 업데이트
        if question_pk == 21:
            if user_score >= 60:
                user.taste = 'T'
            else:
                user.taste = 'F'
            user.save()
    return redirect('balances:detail', question_pk)

@login_required
def update(request, question_pk):
    question = Question.objects.get(pk=question_pk)
    if request.user.is_superuser:
        if request.method == 'POST':
            form = QuestionForm(request.POST, request.FILES, instance=question)
            if form.is_valid():
                form.save()
                return redirect('balances:detail', question_pk)
        else:
            form = QuestionForm(instance=question)

        context = {
            'question' : question,
            'form' : form,
        }
        return render(request, 'balances/update.html', context)
    else:
        return redirect('balances:index')

# def delete(request,question_pk):
#     question = Question.objects.get(pk=question_pk)
#     if request.user.is_superuser:
#         question.delete()
#     return redirect('balances:index')
    
