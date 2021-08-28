from django.db import models
from shared.validators.phone_validator import phone_regex_validator
from django.utils.translation import gettext_lazy as _
from positions.fields import PositionField
from django_enumfield import enum
from django.core.validators import MinValueValidator


class QueueItemStatus(enum.Enum):
    QUEUED = 1
    PROCESSING = 2
    PROCESSED = 3
    SKIPPED = 4


class QueueItemSource(enum.Enum):
    TWILIO = 1
    TELEGRAM = 2


class QueueItemQuerySet(models.QuerySet):
    def actual(self):
        return self.filter(past=False)

    def past(self):
        return self.filter(past=True)


class QueueItem(models.Model):
    objects = QueueItemQuerySet().as_manager()
    banner = models.ForeignKey('banners.Banner', on_delete=models.CASCADE,
                               related_name='queue')
    phone_number = models.CharField(_('phone'),
                                    validators=[phone_regex_validator],
                                    max_length=17)

    status = enum.EnumField(QueueItemStatus,
                            default=QueueItemStatus.QUEUED)
    source = enum.EnumField(QueueItemSource,
                            default=QueueItemSource.TWILIO)
    telegram_chat_id = models.BigIntegerField(null=True,
                                              validators=[MinValueValidator(0)])
    past = models.BooleanField(null=False, default=False)
    position = PositionField(collection=('banner', 'past'))

    processing_started_at = models.DateTimeField(null=True)
    processing_ended_at = models.DateTimeField(null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('position',)
        base_manager_name = 'objects'

    def __str__(self):
        return self.phone_number
