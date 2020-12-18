import os

from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'simpled.settings')
django_asgi_app = get_asgi_application()

from django.urls import path
from channels.routing import ProtocolTypeRouter, URLRouter

from chats.consumers import AsyncChatConsumer

application = ProtocolTypeRouter({
    "http": django_asgi_app,
    "websocket": URLRouter([
        path('chat/<int:course_pk>/', AsyncChatConsumer.as_asgi(), name='chat')
    ])
})