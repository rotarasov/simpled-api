import json

from django.db import models
from django.utils.translation import ugettext_lazy as _

from simpled.settings import BASE_DIR

# TODO add category and language choices
class Course(models.Model):
    class Categories(models.TextChoices):
        pass

    class Languages(models.TextChoices):
        pass

    title = models.CharField(_('title'), max_length=100, unique=True)
    description = models.TextField(_('description'), blank=True)
    category = models.CharField(_('category'), choices=Categories.choices)
    language = models.CharField(_('language'), choices=Languages.choices)

    # @classmethod
    # def get_all_categories(self):
    #     path = BASE_DIR('choices.json')
    #     choices = json.load(path)
    #     return []