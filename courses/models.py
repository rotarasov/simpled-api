from django.db import models
from django.utils.translation import ugettext_lazy as _

from simpled import settings

# TODO add category
class Course(models.Model):
    class Languages(models.TextChoices):
        """
            Short alpha-2 code taken from ISO 639-1
        """
        Russian = 'ru', _('Russian')
        English = 'en', _('English')
        Chinese = 'zh', _('Chinese')
        Spanish = 'es', _('Spanish')
        French = 'fr', _('French')

    class Categories(models.TextChoices):
        pass

    image = models.ImageField(_('image'), upload_to='course_pics', default='default.png')
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                                related_name='created_courses', related_query_name='created_course')
    title = models.CharField(_('title'), max_length=100, unique=True)
    description = models.TextField(_('description'), blank=True)
    category = models.CharField(_('category'), max_length=20, choices=Categories.choices)
    language = models.CharField(_('language'), max_length=3, choices=Languages.choices)
    start_date = models.DateField(_('start date'), auto_now_add=True)
    participants = models.ManyToManyField(settings.AUTH_USER_MODEL, db_table='participation',
                                          related_name='attended_courses', related_query_name='attended_course')

    def __str__(self):
        return self.title


# class Task(models.Model):
#
#     title = models.CharField(_('title'), max_length=100)
#     description = None
#     course = models.ForeignKey('Course', on_delete=models.CASCADE)
#
#     def __str__(self):
#         return self.title

