from django.urls import path
from . import views

app_name ='balances'

urlpatterns = [
    path('', views.index, name='balances_index'),
    # path('create/',views.create, name='create'),
    # path('<int:post_pk>/',views.detail, name='detail'),
    # path('<int:post_pk>/update/', views.update , name='update'),
]
