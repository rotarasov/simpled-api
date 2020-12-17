from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncJsonWebsocketConsumer

from courses.models import Course
from .models import Message


class AsyncChatConsumer(AsyncJsonWebsocketConsumer):
    @database_sync_to_async
    def check_course_exists(self, course_pk):
        return Course.objects.filter(pk=course_pk).exists()

    @database_sync_to_async
    def save_message(self, message):
        Message.objects.create(course_id=self.course_id,
                               sender_id=message['sender_id'],
                               text=message['text'],
                               timestamp=message['timestamp'])

    async def connect(self):
        course_id = self.scope['url_route']['course_pk']

        if await self.check_course_exists(course_id):
            self.course_id = course_id
            self.chat_name = f'chat_{course_id}'
            await self.channel_layer.group_add(self.chat_name, self.channel_name)

        else:
            await self.close()

    async def receive_json(self, content, **kwargs):
        await self.save_message(content)
        await self.channel_layer.group_send(self.chat_name, {
            'type': 'chat.message',
            'sender_id': content['sender_id'],
            'full_name': content['full_name'],
            'text': content['text'],
            'timestamp': content['timestamp']
        })

    async def chat_message(self, event):
        return await self.send_json({
            'sender_id': event['sender_id'],
            'full_name': event['full_name'],
            'timestamp': event['timestamp'],
            'text': event['text']
        })
