from django.utils import timezone

from shared.services.result import Success, Failure
from .next_queue_item_processor import NextQueueItemProcessor
from ..models import QueueItemStatus


class NextQueueItem:

    def __init__(self, banner):
        self.banner = banner

    def next(self):
        if not self.banner:
            return Failure('banner is not found')

        current_item = self.banner.queue.actual().\
            filter(status=QueueItemStatus.PROCESSING).first()
        if current_item:
            current_item.past = True
            current_item.processing_ended_at = timezone.now()
            current_item.status = QueueItemStatus.PROCESSED
            current_item.save()

        next_item = self.banner.queue.actual().first()

        if not next_item:
            # empty queue
            return Success()

        next_item.status = QueueItemStatus.PROCESSING
        next_item.processing_started_at = timezone.now()
        next_item.save()

        return NextQueueItemProcessor(item=next_item).call()
