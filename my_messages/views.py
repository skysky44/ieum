from django.shortcuts import render, get_object_or_404, redirect
from .models import Message
from .forms import ComposeMessageForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages

@login_required
def compose_message(request):
    if request.method == 'POST':
        form = ComposeMessageForm(request.POST, user=request.user)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = request.user
            message.save()
            return redirect('my_messages:inbox')
    else:
        form = ComposeMessageForm(user=request.user)
    return render(request, 'my_messages/compose.html', {'form': form})

def inbox(request):
    received_messages = Message.objects.filter(receiver=request.user).order_by('-timestamp')
    sent_messages = Message.objects.filter(sender=request.user).order_by('-timestamp')
    return render(request, 'my_messages/inbox.html', {'received_messages': received_messages, 'sent_messages': sent_messages})

def view_message(request, message_id):
    message = get_object_or_404(Message, id=message_id)
    if request.user == message.receiver:
        message.is_read = True
        message.save()
    if request.method == 'POST':
        form = ComposeMessageForm(request.POST)
        if form.is_valid():
            reply = form.save(commit=False)
            reply.sender = request.user
            reply.receiver = message.sender
            reply.save()
            return redirect('my_messages:inbox')
    else:
        initial_data = {
            'content': f"Re: {message.content}",
            'receiver': message.sender,
        }
        form = ComposeMessageForm(initial=initial_data)
    return render(request, 'my_messages/view.html', {'message': message, 'form': form})

def mark_as_read(request, message_id):
    message = get_object_or_404(Message, id=message_id)
    if request.user == message.receiver:
        message.is_read = True
        message.save()
    return redirect('my_messages:inbox')

def delete_message(request, message_id):
    message = get_object_or_404(Message, id=message_id)
    if request.user == message.sender and not message.is_read:
        message.delete()
    return redirect('my_messages:inbox')