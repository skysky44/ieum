from django.urls import path
from . import views

app_name = 'my_messages'

urlpatterns = [
    path('compose/', views.compose_message, name='compose_message'),
    path('compose/<str:username>', views.compose_message_to_user, name='compose_message_to_user'),
    path('inbox/received/', views.received_messages, name='received_messages'),
    path('inbox/sent/', views.sent_messages, name='sent_messages'),
    path('message/<int:message_id>/', views.view_message, name='view_message'),
    path('message/<int:message_id>/mark_as_read/', views.mark_as_read, name='mark_as_read'),
    path('message/<int:message_id>/delete/', views.delete_message, name='delete_message'),
]
