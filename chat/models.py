# Create your models here.
from django.db import models
from django.conf import settings


class Message(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    room = models.CharField(max_length=100)

    def __str__(self):
        return f'{self.user.username}: {self.content}'

# 채팅방 삭제 > 메시지 삭제