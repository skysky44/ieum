from django.urls import path
from . import views

app_name ='paints'

urlpatterns = [
    path('',views.index, name = 'index'),
    path('create/',views.create, name='create'),
    path('<int:paint_pk>/',views.detail, name='detail'),
    path('<int:paint_pk>/update/', views.update , name='update'),
    path('<int:paint_pk>/profile_update/', views.profile_update , name='profile_update'),
    path('<int:paint_pk>/delete/',views.delete, name='delete'),
    # path('<int:paint_pk>/likes/', views.likes, name='likes'),
    path('<int:paint_pk>/like_users/', views.like_users, name='like_users'),
    # path('save_image/<int:paint_pk>/', views.save_image, name='save_image'),
]