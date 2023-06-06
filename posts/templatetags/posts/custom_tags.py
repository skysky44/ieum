from django import template
from django.contrib.auth.models import User

register = template.Library()


@register.simple_tag
def get_unread_messages_count(user):
    received_messages = user.received_messages.filter(is_read=False)
    print(received_messages)
    count = received_messages.count()
    return count