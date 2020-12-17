from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncJsonWebsocketConsumer

from courses.models import Course


class ChatConsumer(AsyncJsonWebsocketConsumer):
    @database_sync_to_async
    def check_course_exists(self, course_pk):
        return Course.objects.filter(pk=course_pk).exists()

    async def connect(self):
        course_pk = self.scope['url_route']['kwargs']['course_pk']

        if self.check_course_exists(course_pk):
            self.chat_name = course_pk
            self.channel_layer.group