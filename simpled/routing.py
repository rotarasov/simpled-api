from django.urls import re_path
from channels.routing import ProtocolTypeRouter, URLRouter

from chats.consumers import AsyncChatConsumer

application = ProtocolTypeRouter({
    "websocket": URLRouter([
        re_path('chat/<int:course_pk>/', AsyncChatConsumer.as_asgi(), name='chat')
    ])
})