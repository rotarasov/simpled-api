from cloudinary import api
from cloudinary.exceptions import NotFound
from cloudinary.models import CloudinaryResource
from django.core.exceptions import ValidationError


def get_default_course_image() -> str:
    from .models import Course

    result = api.resource(f'{Course.MEDIA_FOLDER}/default')
    return f'{result["resource_type"]}/{result["type"]}/v{result["version"]}/{result["public_id"]}'


def validate_course_image(value: CloudinaryResource) -> CloudinaryResource:
    try:
        api.resource(value.public_id)
        return value
    except NotFound:
        raise ValidationError('Incorrect public id or image is not uploaded on media server')
