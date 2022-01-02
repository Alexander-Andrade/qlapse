from banners.services.queue_item_services.state_transitions.transit_to_skipped_state import TransitToSkippedState
from banners.services.queue_item_services.action_processors.skip_queue_item_processor import SkipQueueItemProcessor
from shared.services.result import Success, Failure


class SkipItem:

    def __init__(self, banner):
        self.banner = banner

    def skip(self, ):
        if not self.banner:
            return Failure('banner is not found')

        item = self.banner.queue.actual().first()

        if not item:
            return Failure('The queue is empty')

        SkipQueueItemProcessor(item).call()
        TransitToSkippedState(item).call()

        return Success()
