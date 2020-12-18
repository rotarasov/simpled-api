import os

import django
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter

from chats.routing import websocket_urlpatterns

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'simpled.settings')

django.setup()

http_application = get_asgi_application()

application = ProtocolTypeRouter({
    "http": http_application,
    "websocket": URLRouter(websocket_urlpatterns)
})
