import os

from django.core.asgi import get_asgi_application
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter

from chats.routing import websocket_urlpatterns

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'simpled.settings')

application = get_asgi_application()
# application = ProtocolTypeRouter({
#     "http": get_asgi_application(),
#     "websocket": URLRouter(websocket_urlpatterns)
# })
