from django.urls import path
from . import views

app_name ='posts'

urlpatterns = [
    path('',views.index, name = 'index'),
    path('create/',views.create, name='create'),
    path('<int:post_pk>/',views.detail, name='detail'),
    path('<int:post_pk>/update/', views.update , name='update'),
    path('<int:post_pk>/delete/',views.delete, name='delete'),
    path('<int:post_pk>/likes/', views.likes, name='likes'),
    path('<int:post_pk>/comments_create/', views.comment_create, name='comment_create'),
    path('<int:post_pk>/comments/<int:comment_pk>/comment_update/', views.comment_update, name='comment_update'),
    path('<int:post_pk>/comments/<int:comment_pk>/comment_delete/', views.comment_delete, name='comment_delete'),
    path('<int:post_pk>/comments/<int:comment_pk>/comment_likes/', views.comment_likes, name='comment_likes'),
    
    # 저는 이만 밥먹으러 가겠습니다 -미영-
]
