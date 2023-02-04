import json
from django.utils import timezone
from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
# from chat.models import OrderChatHistory
# from order.models import Order


class ChatConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        self.user = self.scope['user']
        self.id = self.scope['url_route']['kwargs']['session_id']
        self.room_group_name = 'chat_{}'.format(self.id)
        # join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        # accept connection
        await self.accept()

    async def disconnect(self, close_code):
        # leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        now = timezone.now()
        avatar_url = '/static/images/common/avatar.svg.png'
        if self.user.avatar:
            avatar_url = self.user.avatar.url
        # send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'user': self.user.username,
                'avatar_url': avatar_url,
                'datetime': now.isoformat(),
                'sudo_identity': self.user.username
            }
        )
        # order = await self._get_order()
        # await self._create_chat(order, message, now)

    # @database_sync_to_async
    # def _get_order(self):
    #     return Order.objects.get(id=self.id)

    # receive message from room group
    async def chat_message(self, event):
        # Send message to WebSocket
        await self.send(text_data=json.dumps(event))

    # @database_sync_to_async
    # def _create_chat(self, order, message, timestamp):
    #     chat = OrderChatHistory.objects.create(
    #         order=order,
    #         user=self.user,
    #         message=message,
    #         timestamp=timestamp
    #     )
    #     chat.save()
