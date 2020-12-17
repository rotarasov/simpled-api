from django.urls import re_path, path

from .consumers import AsyncChatConsumer

websocket_urlpatterns = [
    path('chat/<int:course_pk>/', AsyncChatConsumer.as_asgi(), name='chat')
]