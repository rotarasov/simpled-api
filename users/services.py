from cloudinary import api
from cloudinary.exceptions import NotFound
from cloudinary.models import CloudinaryResource
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError


def get_default_user_image() -> str:
    User = get_user_model()
    result = api.resource(f'{User.MEDIA_FOLDER}/default')
    return f'{result["resource_type"]}/{result["type"]}/v{result["version"]}/{result["public_id"]}'


def validate_user_image(value: CloudinaryResource) -> CloudinaryResource:
    try:
        api.resource(value.public_id)
    except NotFound:
        raise ValidationError('Incorrect public id or image is not uploaded on media server')
    return value


def get_users_for_video_chat_display():
    User = get_user_model()
    return User.objects.only('first_name', 'last_name').all()
