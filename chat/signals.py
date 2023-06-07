from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Message

@receiver(post_save, sender=Message)
def process_new_message(sender, instance, created, **kwargs):
    if created:
        # 여기에 새로운 메시지가 생성되었을 때 수행할 작업을 추가하세요.
        pass