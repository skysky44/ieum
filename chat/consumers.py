import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models import Message
from django.contrib.auth import get_user_model

# 
class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        name = [ord(char) for char in self.room_name]
        b = ''
        for a in name:
            b += str(a)
        
        self.room_group_name = f'chat{b}'

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
    
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        user_id = self.scope["user"].id
        user = await self.get_user(user_id)

        message_obj = await self.save_message(user, message)

        user_obj = await self.get_user(user_id)
        user_profile_image = user_obj.image.url if user_obj.image else None
        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message_obj.content,
                'user': message_obj.user.username,
                'user_profile_image' : user_profile_image,
            } 
        )

    @database_sync_to_async
    def get_user(self, user_id):
        return get_user_model().objects.get(id=user_id)

    @database_sync_to_async
    def save_message(self, user, message):
        room_owner = Message.objects.filter(room=self.room_name, is_owner=True).first()
        is_owner = not bool(room_owner) or room_owner.user == user

        message_obj = Message.objects.create(user=user, content=message, room=self.room_name, is_owner=is_owner)

        if is_owner and not room_owner:
            message_obj.is_owner = True
            message_obj.save()

        return message_obj

    async def chat_message(self, event):
        message = event['message']
        user = event['user']
        user_profile_image = event['user_profile_image']
        # image = event['image']
        # Send message to WebSocket
        # 메시지를 WebSocket으로 전송합니다. 사용자 이름과 프로필 사진을 포함하여 보냅니다.
        await self.send(text_data=json.dumps({
            'type': 'chat.message',
            'message': message,
            'user': user,
            'user_profile_image': user_profile_image,
        }))

    
