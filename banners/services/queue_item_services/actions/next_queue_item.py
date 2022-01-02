from shared.services.result import Success, Failure
from banners.services.queue_item_services.action_processors.next_queue_item_processor import NextQueueItemProcessor
from banners.services.queue_item_services.state_transitions.transit_to_processing_state import TransitToProcessingState
from banners.services.queue_item_services.state_transitions.transit_to_processed_state import TransitToProcessedState
from banners.models import QueueItemStatus


class NextQueueItem:

    def __init__(self, banner):
        self.banner = banner

    def next(self):
        if not self.banner:
            return Failure('banner is not found')

        current_item = self.banner.queue.actual().\
            filter(status=QueueItemStatus.PROCESSING).first()
        if current_item:
            result = TransitToProcessedState(current_item).call()
            if result.failed:
                return result

        next_item = self.banner.queue.actual().first()
        if not next_item:
            # empty queue
            return Success()

        result = TransitToProcessingState(next_item).call()
        if result.failed:
            return result

        return NextQueueItemProcessor(item=next_item).call()
