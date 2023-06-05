from django.urls import path
from . import views

app_name ='posts'

urlpatterns = [
    path('',views.index, name = 'index'),
    path('anonymous/',views.anonymous, name='anonymous'),
    path('create/',views.create, name='create'),
    path('anonymous_create/',views.anonymous_create, name='anonymous_create'),
    path('<int:post_pk>/',views.detail, name='detail'),
    path('anonymous/<int:post_pk>/',views.anonymous_detail, name='anonymous_detail'),
    path('<int:post_pk>/update/', views.update , name='update'),
    path('<int:post_pk>/anonymous_update/', views.anonymous_update , name='anonymous_update'),
    path('<int:post_pk>/delete/',views.delete, name='delete'),
    path('<int:post_pk>/likes/', views.likes, name='likes'),
    path('<int:post_pk>/comments_create/', views.comment_create, name='comment_create'),
    path('<int:post_pk>/anonymous_comments_create/', views.anonymous_comment_create, name='anonymous_comment_create'),
    path('<int:post_pk>/comments/<int:comment_pk>/anonymous_comment_update/', views.anonymous_comment_update, name='anonymous_comment_update'),
    path('<int:post_pk>/comments/<int:comment_pk>/comment_update/', views.comment_update, name='comment_update'),
    path('<int:post_pk>/comments/<int:comment_pk>/comment_delete/', views.comment_delete, name='comment_delete'),
    path('<int:post_pk>/comments/<int:comment_pk>/anonymous_comment_delete/', views.anonymous_comment_delete, name='anonymous_comment_delete'),
    path('<int:post_pk>/comments/<int:comment_pk>/comment_likes/', views.comment_likes, name='comment_likes'),
    path('search/', views.search_spotify, name='search_spotify'),
    # path('save_track/', views.save_track, name='save_track'),
    # path('delete_track/<int:track_pk>/',views.delete_track, name='delete_track'),
    
    # 저는 이만 밥먹으러 가겠습니다 -미영-
]
