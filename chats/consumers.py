from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncJsonWebsocketConsumer

from courses.models import Course
from .models import Message


class AsyncChatConsumer(AsyncJsonWebsocketConsumer):
    @database_sync_to_async
    def check_course_exists(self, course_pk):
        return Course.objects.filter(pk=course_pk).exists()

    async def connect(self):
        course_pk = self.scope['url_route']['course_pk']

        if self.check_course_exists(course_pk):
            self.chat_name = f'chat_{course_pk}'
            await self.channel_layer.group_add(self.chat_name, self.channel_name)

        else:
            await self.close()

