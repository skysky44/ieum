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
    # 질문 가져오기
    question = Question.objects.get(pk=question_pk)
    # 현재 사용자의 사용자 모델 값 가져오기
    user = request.user
    # User = get_user_model()

    if request.method == 'POST':
        # 현재 유저의 밸런스 결과 가져오고, 없으면 생성하기
        result, created = Result.objects.get_or_create(user=user)
        user_score = user.score # 사용자의 점수 가져오기

        # 결과의 chosen_result값만 새로운 변수에 할당
        chosen_results = result.chosen_result

        # 만약 chosen_results가 비어 있다면 빈 딕셔너리로 초기화
        if not chosen_results:
            chosen_results = {}

        # 선택한 답변을 딕셔너리에 추가(이렇게 딕셔너리로 할 경우 답을 고치게 되더라도 수정이 자동으로 가능해짐)
        chosen_results[str(question_pk)] = select_answer

        # 유저가 밸런스 게임을 한 후 Result 모델의 chosen_result 필드 업데이트
        result.chosen_result = chosen_results
        result.save()

        # 유저의 워드 딕셔너리 만들기
        word_list = result.word
        # 워드 딕셔너리가 비어있으면 딕셔너리로 만들기 위한 코드
        if not word_list:
            word_list = {}
        
        # 워드 값이 있는 경우에만 딕셔너리 만들어주기(질문의 word1과 word2가 비어 있지 않은 경우에만 처리)
        if question.word1 != "" and question.word2 != "":

            if select_answer == 1:
                selected_word = question.word1
            elif select_answer == 2:
                selected_word = question.word2
            # 선택한 단어를 쉼표로 나누기
            selected_words = selected_word.split(',')

            # 선택한 단어들을 리스트에 추가(질문pk = 내가 고른 질문의 답의 단어)
            word_list[str(question_pk)] = selected_words

            # 유저가 밸런스 게임을 답할때마다 Result 모델의 word 필드 업데이트 
            result.word = word_list
            result.save()

        # 질문 번호가 18 이하인 경우에만 점수 계산
        if question_pk <= 18:
            if question_pk == 6 or question_pk == 7 or question_pk == 9 or question_pk == 10:
                pass
            else:
                # 질문 번호가 홀수인지 짝수인지 확인
                if question_pk % 2 == 1:
                    # 홀수 번호의 질문에서 답변 1을 선택한 경우 10점 감점 (F가 1번)
                    if select_answer == 1:
                        user_score -= 10
                if question_pk % 2 == 0:
                    # 짝수 번호의 질문에서 답변 2을 선택한 경우 10점 감점 (F가 2번)
                    if select_answer == 2:
                        user_score -= 10
            # Result 모델의 score 필드 업데이트
            user.score = user_score
            user.save()
        # question_pk가 21인 경우에 user_score 필드 업데이트(21번까지 답을 다 해야만, 점수 필드를 얻을 수 있음)
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

# 밸런스 게임의 문제를 삭제하게 될 경우, 그 전에 있는 유저는 전의 질문의 값을 갖고 있기 때문에 유저를 분류 할 때 애매해짐
# 그래서 대대적인 업데이트 아닌 경우, 질문을 최대한 수정을 자제하고 삭제는 대대적인 업데이트가 아닌 경우면 사용하지 않기로 회의함 
# def delete(request,question_pk):
#     question = Question.objects.get(pk=question_pk)
#     if request.user.is_superuser:
#         question.delete()
#     return redirect('balances:index')
   
