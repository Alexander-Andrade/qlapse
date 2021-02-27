from shared.services.result import Success, Failure
from banners.models import *
from .next_queue_item_processor import NextQueueItemProcessor


class NextQueueItem:

    def __init__(self, banner):
        self.banner = banner

    def next(self):
        if not self.banner:
            return Failure('banner is not found')

        current_item = self.banner.queue.\
            filter(status=QueueItemStatus.PROCESSING).first()
        if current_item:
            current_item.delete()

        next_item = self.banner.queue.first()

        if not next_item:
            # empty queue
            return Success()

        next_item.status = QueueItemStatus.PROCESSING
        next_item.save()

        return NextQueueItemProcessor(item=next_item).call()
