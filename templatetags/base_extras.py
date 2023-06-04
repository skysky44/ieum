# from django import template
# from my_messages.models import Message

# register = template.Library()

# @register.filter
# def is_read_count(user):
#     is_read_messages = Message.objects.filter(receiver=user, is_read=False).count()
#     return is_read_messages
