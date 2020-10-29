import cloudinary

from . import config
from . import django as settings

def config_media_storage():
    if settings.DEBUG:
        cloudinary.config(
            cloud_name=config.env.str('CLOUDINARY_CLOUD_NAME'),
            api_key = config.env.str('CLOUDINARY_API_KEY'),
            api_secret=config.env.str('CLOUDINARY_API_SECRET')
        )