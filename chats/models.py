from django.db import models
from django.utils.translation import ugettext_lazy as _

from simpled import settings


class Message(models.Model):
    course = models.ForeignKey('courses.Course', on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='messages')
    text = models.CharField(_('text'), max_length=512)
    timestamp = models.DateTimeField(_('timestamp'), auto_now_add=True)

    class Meta:
        ordering = ('timestamp',)
