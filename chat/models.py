# Create your models here.
from django.db import models
from django.conf import settings


class Message(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    room = models.CharField(max_length=100)
    is_owner = models.BooleanField(default=False)  # 방장 여부를 나타내는 필드

    def __str__(self):
        return f'{self.user.username}: {self.content}'

    def delete_room(self):
        if self.is_owner:
            # 방장인 경우 방의 모든 메시지 삭제
            Message.objects.filter(room=self.room).delete()
            # 또는 다른 로직을 수행할 수 있습니다.
        else:
            # 방장이 아닌 경우 처리 로직을 정의하세요
            pass
        
# 채팅방 삭제 > 메시지 삭제