import os

from django.core.asgi import get_asgi_application


if os.environ.get('LOCAL_DEVELOPMENT'):
    settings_path = 'simpled.local_settings'
else:
    settings_path = 'simpled.production_settings'


os.environ.setdefault('DJANGO_SETTINGS_MODULE', settings_path)

application = get_asgi_application()
