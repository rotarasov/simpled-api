from django.db import models
from django.utils.translation import ugettext_lazy as _
from cloudinary import api
from cloudinary.models import CloudinaryField


from simpled import settings

# TODO: create post delete hook to delete picture from cloudinary
# TODO add default for creator field to match current authorized user
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
        LANGUAGE_LEARNING = 'language_learning', _('Language learning')
        PROGRAMMING = 'programming', _('Programming')
        HEALTH = 'health', _('Health')
        SOCIAL_SCIENCE = 'social_science', _('Social science')
        ENGINEERING = 'engineering', _('Engineering')
        MATHEMATICS = 'math', _('Mathematics')


    if settings.DEBUG:
        image = models.ImageField(_('image'), upload_to=MEDIA_FOLDER, default=f'{MEDIA_FOLDER}/default.png')

    else:
        image = CloudinaryField(_('image'), folder=MEDIA_FOLDER)

    creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                                related_name='created_courses', related_query_name='created_course')
    title = models.CharField(_('title'), max_length=100, unique=True)
    description = models.TextField(_('description'), blank=True)
    category = models.CharField(_('category'), max_length=50, choices=Categories.choices)
    language = models.CharField(_('language'), max_length=3, choices=Languages.choices)
    start_date = models.DateField(_('start date'), auto_now_add=True)
    participants = models.ManyToManyField(settings.AUTH_USER_MODEL, db_table='participation',
                                          related_name='attended_courses', related_query_name='attended_course')

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.image:
            result = api.resource(f'{self.MEDIA_FOLDER}/default')
            self.image = f'v{result["version"]}/{result["public_id"]}'


# class Task(models.Model):
#
#     title = models.CharField(_('title'), max_length=100)
#     description = None
#     course = models.ForeignKey('Course', on_delete=models.CASCADE)
#
#     def __str__(self):
#         return self.title

