from django.db import models
from django.core.validators import FileExtensionValidator
from shared.validators.phone_validator import phone_regex_validator
from django.utils.translation import gettext_lazy as _
from accounts.models import CustomUser
from enum import IntEnum
from positions.fields import PositionField


class Banner(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    phone_number = models.CharField(_('phone'), validators=[phone_regex_validator], max_length=17)
    upload = models.FileField(upload_to='banners/', validators=[FileExtensionValidator(allowed_extensions=['pdf'])])
    preview = models.ImageField(upload_to='banner_previews/', null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.phone_number


class QueueItemStatus(IntEnum):
    QUEUE = 1
    PROCESSING = 2

    @classmethod
    def choices(cls):
        return [(key.value, key.name) for key in cls]


class QueueItem(models.Model):
    banner = models.ForeignKey(Banner, on_delete=models.CASCADE, related_name='queue')
    phone_number = models.CharField(_('phone'), validators=[phone_regex_validator], max_length=17)

    status = models.IntegerField(choices=QueueItemStatus.choices(), default=QueueItemStatus.QUEUE)

    position = PositionField(collection='banner')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('position',)

    def __str__(self):
        return self.phone_number