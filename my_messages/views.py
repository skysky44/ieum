from django.shortcuts import render, get_object_or_404, redirect
from .models import Message
from accounts.models import User
from .forms import ComposeMessageForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator

# 메시지 보내기
@login_required
def compose_message(request):
    if request.method == 'POST':
        form = ComposeMessageForm(request.POST, user=request.user)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = request.user
            message.save()
            return redirect('my_messages:sent_messages')
    else:
        form = ComposeMessageForm(user=request.user)
    return render(request, 'my_messages/compose.html', {'form': form})

@login_required
def compose_message_to_user(request, username):
    person = get_object_or_404(User, username=username)
    if request.method == 'POST':
        form = ComposeMessageForm(request.POST, user=request.user)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = request.user
            message.receiver = person
            message.save()
            return redirect('my_messages:sent_messages')
    else:
        initial_data = {'receiver': person}
        form = ComposeMessageForm(initial=initial_data, user=request.user)
    return render(request, 'my_messages/compose_to_user.html', {'form': form, 'person': person})


# 메시지 받기
@login_required
def received_messages(request):
    received_messages = Message.objects.filter(receiver=request.user).order_by('-timestamp')
    page = request.GET.get('page', '1')
    per_page = 5
    paginator = Paginator(received_messages, per_page)
    page_obj = paginator.get_page(page)
    is_read_messages = Message.objects.filter(receiver=request.user, is_read=False).count()


    return render(request, 'my_messages/received_messages.html', {'received_messages': received_messages, 'received_messages': page_obj, 'is_read_messages': is_read_messages})

@login_required
def sent_messages(request):
    sent_messages = Message.objects.filter(sender=request.user).order_by('-timestamp')
    page = request.GET.get('page', '1')
    per_page = 5
    paginator = Paginator(sent_messages, per_page)
    page_obj = paginator.get_page(page)
    return render(request, 'my_messages/sent_messages.html', {'sent_messages': sent_messages, 'sent_messages': page_obj,})


def view_message(request, message_id):
    param = request.GET.get('param')
    message = get_object_or_404(Message, id=message_id)


    if request.user == message.receiver:
        message.is_read = True
        User.my_is_read = True
        message.save()
    
    if request.method == 'POST':
        form = ComposeMessageForm(request.POST)
        if form.is_valid():
            reply = form.save(commit=False)
            reply.sender = request.user
            reply.receiver = message.sender
            reply.save()
            return redirect('my_messages:received_messages')
    else:
        initial_data = {
            'receiver': message.sender,
        }
        form = ComposeMessageForm(initial=initial_data)
    
    if param == '1':
        return render(request, 'my_messages/received_view.html', {'message': message, 'form': form})

    elif param == '2':
        return render(request, 'my_messages/sent_view.html', {'message': message, 'form': form})


def mark_as_read(request, message_id):
    message = get_object_or_404(Message, id=message_id)
    if request.user == message.receiver:
        message.is_read = True
        User.my_is_read = True
        message.save()
        
    return redirect('my_messages:received_messages')

def delete_message(request, message_id):
    message = get_object_or_404(Message, id=message_id)
    if request.user == message.sender and not message.is_read:
        message.delete()
    return redirect('my_messages:received_messages')

@login_required
def delete_message(request, message_id):
    message = get_object_or_404(Message, id=message_id)
    if request.user == message.receiver or request.user == message.sender:
        message.delete()
        messages.success(request, '쪽지가 삭제되었습니다.')
    return redirect('my_messages:received_messages')
