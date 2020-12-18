import os

from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'simpled.settings')
django_asgi_app = get_asgi_application()

from django.conf.urls import url
from channels.routing import ProtocolTypeRouter, URLRouter

from chats.consumers import AsyncChatConsumer

application = ProtocolTypeRouter({
    "http": django_asgi_app,
    "websocket": URLRouter([
        url(r"^wss/chat/(?P<course_pk>[0-9]+)/$", AsyncChatConsumer.as_asgi(), name='chat')
    ])
})