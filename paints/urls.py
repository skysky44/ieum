from django.urls import path
from . import views

app_name ='paints'

urlpatterns = [
    path('',views.index, name = 'index'),
    path('create/',views.create, name='create'),
    path('<int:paint_pk>/',views.detail, name='detail'),
    # path('<int:paints_pk>/update/', views.update , name='update'),
    path('<int:paint_pk>/delete/',views.delete, name='delete'),
]