from django.utils import timezone

from banners.models import QueueItemStatus
from banners.services.queue_item_services.waiting_time.convolve_waiting_time import ConvolveWaitingTime
from banners.services.queue_item_services.validators.queue_item_validator import QueueItemValidator
from shared.services.result import Success, Failure


class TransitToProcessedState:
    TRANSITION_FROM_STATES = [QueueItemStatus.PROCESSING]

    def __init__(self, queue_item):
        self.queue_item = queue_item

    def call(self):
        if not self.is_transition_allowed():
            return Failure(f"Queue item with {self.queue_item.state} state can"
                           f" not be transfered to {QueueItemStatus.PROCESSED} state")

        self.queue_item.past = True
        self.queue_item.position = -1
        self.queue_item.processing_ended_at = timezone.now()
        self.queue_item.status = QueueItemStatus.PROCESSED
        self.queue_item.waiting_time_estimation = \
            ConvolveWaitingTime(queue_item=self.queue_item).call()
        result = QueueItemValidator(self.queue_item).call()
        if result.failed:
            return result
        self.queue_item.save()
        return Success(self.queue_item)

    def is_transition_allowed(self):
        return self.queue_item.status in self.TRANSITION_FROM_STATES
