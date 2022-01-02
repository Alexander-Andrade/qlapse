from banners.models import QueueItemStatus
from banners.services.queue_item_services.validators.queue_item_validator import QueueItemValidator
from shared.services.result import Failure, Success


class TransitToSkippedState:
    TRANSITION_FROM_STATES = [QueueItemStatus.QUEUED]

    def __init__(self, queue_item):
        self.queue_item = queue_item

    def call(self):
        if not self.is_transition_allowed():
            return Failure(f"Queue item with {self.queue_item.state} state can"
                           f" not be transfered to {QueueItemStatus.SKIPPED} state")

        self.queue_item.past = True
        self.queue_item.status = QueueItemStatus.SKIPPED
        result = QueueItemValidator(self.queue_item).call()
        if result.failed:
            return result
        self.queue_item.save()
        return Success(self.queue_item)

    def is_transition_allowed(self):
        return self.queue_item.status in self.TRANSITION_FROM_STATES
