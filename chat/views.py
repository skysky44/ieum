from django.shortcuts import render
from .models import Message

def index(request):
    messages = Message.objects.all()
    rooms = []
    for message in messages:
        rooms.append(message.room)
    context = {
        'rooms': set(rooms),
    }

    return render(request, 'chat/index.html', context)

def room(request, room_name):
    messages = Message.objects.filter(room=room_name)
    context = {
        'room_name': room_name,
        'messages': messages,
    }
    return render(request, 'chat/room.html', context)