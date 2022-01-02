from banners.models import QueueItemStatus, QueueItemSource
from shared.services.result import Success, Failure
from django.core.exceptions import ValidationError


class QueueItemValidator:
    def __init__(self, queue_item):
        self.queue_item = queue_item

    def call(self):
        result = self.validate_processed_item()
        if result.failed:
            return result

        result = self.validate_telegram_item()
        if result.failed:
            return result

        try:
            self.queue_item.full_clean()
        except ValidationError as e:
            return Failure(str(e))

        return Success()

    def validate_processed_item(self):
        if self.queue_item.status != QueueItemStatus.PROCESSED:
            return Success()
        if self.queue_item.processing_ended_at is None:
            return Failure('processing_ended_at should be present')

        if self.queue_item.waiting_time_estimation is None:
            return Failure('waiting_time_estimation should be present')

        return Success()

    def validate_telegram_item(self):
        if self.queue_item.source != QueueItemSource.TELEGRAM:
            return Success()

        if self.queue_item.telegram_chat_id is None:
            return Failure('telegram_chat_id cannot be blank')

        return Success()
