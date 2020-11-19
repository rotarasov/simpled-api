import re

import cloudinary
from urllib.parse import urlparse

from . import config


def config_media_storage(**options):
    netloc = urlparse(config.env.str('CLOUDINARY_URL')).netloc
    api_key, api_secret, cloud_name = re.split('[@:]', netloc)
    cloudinary.config(cloud_name=cloud_name,api_key=api_key, api_secret=api_secret, **options)
