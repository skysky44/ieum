from django.urls import path
from . import views

app_name ='my_messages'

urlpatterns = [
    path('compose/', views.compose_message, name='compose_message'),
    path('inbox/', views.inbox, name='inbox'),
    path('message/<int:message_id>/', views.view_message, name='view_message'),

]
