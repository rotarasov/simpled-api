import re

from cloudinary import config as media_storage
from urllib.parse import urlparse

from . import configuration


def config_media_storage(**options):
    netloc = urlparse(configuration.env.str('CLOUDINARY_URL')).netloc
    api_key, api_secret, cloud_name = re.split('[@:]', netloc)
    media_storage(cloud_name=cloud_name,api_key=api_key, api_secret=api_secret, **options)
