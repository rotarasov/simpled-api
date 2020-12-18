from django.urls import re_path

from .consumers import AsyncChatConsumer

websocket_urlpatterns = [
    re_path('chat/<int:course_pk>/', AsyncChatConsumer.as_asgi(), name='chat')
]