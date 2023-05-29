from django.urls import path
from . import views

app_name = 'my_messages'

urlpatterns = [
    path('compose/', views.compose_message, name='compose_message'),
    path('inbox/', views.inbox, name='inbox'),
    path('message/<int:message_id>/', views.view_message, name='view_message'),
    path('message/<int:message_id>/mark_as_read/', views.mark_as_read, name='mark_as_read'),
    path('message/<int:message_id>/delete/', views.delete_message, name='delete_message'),
]
