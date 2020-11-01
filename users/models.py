from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import ugettext_lazy as _
from cloudinary.models import CloudinaryField
from cloudinary import api

from .managers import UserManager

# TODO: create added courses and erolled courses foreign keys

def image_default():
    result = api.resource(f'{User.MEDIA_FOLDER}/default')
    return f'{result["resource_type"]}/{result["type"]}/v{result["version"]}/{result["public_id"]}'

class User(AbstractUser):
    MEDIA_FOLDER = 'profile_pics'

    image = CloudinaryField(_('profile image'), folder=MEDIA_FOLDER, default=image_default)
    username = None
    email = models.EmailField(_('email address'), unique=True)
    bio = models.TextField(_('biography'), blank=True)
    first_name = models.CharField(_('first name'), max_length=32)
    last_name = models.CharField(_('last name'), max_length=32)
    points = models.PositiveIntegerField(_('points'), default=0)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    objects = UserManager()

    def __str__(self):
        return self.email

    def get_added_courses(self):
        from courses.models import Course

        return list(Course.objects.filter(creator_id=self.id))

    def get_enrolled_courses(self):
        from courses.models import Course

        return list(Course.objects.filter(participants__in=[self.id]))