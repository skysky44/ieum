from django.urls import path
from . import views

app_name ='balances'

urlpatterns = [
    # path('', views.index, name='balances_index'),
    # path('create/',views.create, name='create'),
    # path('balance_game/',views.balance_game_view, name='balance'),
    # path('<int:post_pk>/',views.detail, name='detail'),
    # path('<int:post_pk>/update/', views.update , name='update'),

    path('',views.index, name = 'index'),
    path('create/',views.create, name='create'),
    path('<int:question_pk>/',views.detail, name='detail'),
    path('<int:question_pk>/answer/<int:select_answer>/', views.answer, name='answer'),
    # path('<int:question_pk>/update/', views.update , name='update'),
    # path('<int:question_pk>/delete/',views.delete, name='delete'),
]
