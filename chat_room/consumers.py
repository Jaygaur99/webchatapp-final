import json
from channels.generic.websocket import AsyncWebsocketConsumer
from .models import Message
from django.contrib.auth import get_user_model
from channels.db import database_sync_to_async

class ChatConsumer(AsyncWebsocketConsumer):
    User = get_user_model()

    async def connect(self):
        # Layer is to be created
        self.username = self.scope['url_route']['kwargs']['username']
        self.from_user = int(self.scope['url_route']['kwargs']['from_user'])
        self.to_user = int(self.scope['url_route']['kwargs']['to_user'])
        # print(self.username, self.from_user, self.to_user)
        await self.channel_layer.group_add(self.username, self.channel_name)
        await self.accept()

    async def disconnect(self):
        await self.channel_layer.group_discard(self.email_name, self.channel_name)

    @database_sync_to_async
    def save_to_db(self, message):
        Message(
            from_user=self.User.objects.get(id=self.from_user),
            to_user=self.User.objects.get(id=self.to_user),
            chat_identifier=self.username,
            content=message
        ).save()

    async def receive(self, text_data):
        test_data_json = json.loads(text_data)
        message = test_data_json['message']
        # await sync_to_async(ChatModel(room_no=self.room_name, message=message).save())
        await self.save_to_db(message)
        await self.channel_layer.group_send(self.username, {
            'type' : 'send_back',
            'message': message,
        })
    
    async def send_back(self, event):
        message = event['message']
        await self.send(text_data=json.dumps({
            'message': message.split(":")[1],
            'user': message.split(":")[0] 
        }))
    

    # @&@%@ -> :