from django.shortcuts import render, redirect
from .models import Message
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden


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



@login_required
def room_delete(request, room_name):
    # 방장 여부 확인
    room_owner = Message.objects.filter(room=room_name, is_owner=True, user=request.user).first()
    if not room_owner:
        return HttpResponseForbidden("당신은 방장이 아닙니다.")

    # 방장인 경우 방의 모든 메시지 삭제
    Message.objects.filter(room=room_name).delete()

    return redirect('chat:index')