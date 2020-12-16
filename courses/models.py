from datetime import date

from django.core.validators import MinValueValidator
from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from cloudinary.models import CloudinaryField

from . import services
from simpled import settings


class Course(models.Model):
    MEDIA_FOLDER = 'course_pics'

    class Languages(models.TextChoices):
        """
            Short alpha-2 code taken from ISO 639-1
        """
        RUSSIAN = 'ru', _('Russian')
        ENGLISH = 'en', _('English')
        CHINESE = 'zh', _('Chinese')
        SPANISH = 'es', _('Spanish')
        FRENCH = 'fr', _('French')

    class Categories(models.TextChoices):
        MUSIC = 'music', _('Music')
        PHOTOGRAPHY = 'photography', _('Photography')
        DESIGN = 'design', _('Design')
        ARTS = 'arts', _('Arts')
        BUSINESS = 'business', _('Business')
        LANGUAGE_LEARNING = 'language', _('Language')
        PROGRAMMING = 'programming', _('Programming')
        HEALTH = 'health', _('Health')
        SOCIAL_SCIENCE = 'social_science', _('Social science')
        ENGINEERING = 'engineering', _('Engineering')
        MATHEMATICS = 'math', _('Mathematics')

    image = CloudinaryField(_('image'), folder=MEDIA_FOLDER, default=services.get_default_course_image,
                            validators=[services.validate_course_image])
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                                related_name='created_courses', related_query_name='created_course')
    title = models.CharField(_('title'), max_length=100, unique=True)
    description = models.TextField(_('description'), blank=True)
    category = models.CharField(_('category'), max_length=50, choices=Categories.choices)
    language = models.CharField(_('language'), max_length=3, choices=Languages.choices)
    start_date = models.DateField(_('start date'), default=date.today)
    participants = models.ManyToManyField(settings.AUTH_USER_MODEL, through='Participation',
                                          related_name='attended_courses', related_query_name='attended_course')
    is_active = models.BooleanField(_("is active"), default=True)

    def __str__(self):
        return self.title

    def delete_solutions(self):
        for task in self.tasks.all():
            task.solutions.all().delete()

    def delete_participants(self):
        Participation.objects.filter(course_id=self.id).delete()


class Participation(models.Model):
    participant = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                                    related_name='participations', related_query_name='participation')
    course = models.ForeignKey('Course',  on_delete=models.CASCADE,
                               related_name='participations', related_query_name='participation')
    is_active = models.BooleanField(_("is active"), default=True)


class Task(models.Model):
    title = models.CharField(_('title'), max_length=100)
    description = models.TextField(_('description'))
    deadline = models.DateTimeField(_('deadline'), validators=[
        MinValueValidator(timezone.now, message='Deadline must be greater than now')
    ])
    course = models.ForeignKey('Course', on_delete=models.CASCADE, related_name='tasks')
    created = models.DateTimeField(_('created'), auto_now_add=True)
    last_modified = models.DateTimeField(_('last modified'), auto_now=True)

    class Meta:
        unique_together = ['title', 'course']

    def __str__(self):
        return self.title


class Solution(models.Model):
    FILE_FOLDER = 'solutions'

    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='solutions')
    task = models.ForeignKey('Task', on_delete=models.CASCADE, related_name='solutions')
    text = models.TextField(_('text'), null=True, blank=True)
    file = CloudinaryField(_('file'), folder=FILE_FOLDER, resource_type='raw', null=True, blank=True)
    last_modified = models.DateTimeField(_('last modified'), auto_now=True)

    class Meta:
        unique_together = ['owner', 'task']

    def __str__(self):
        return f'{self.task} - {self.owner}'
