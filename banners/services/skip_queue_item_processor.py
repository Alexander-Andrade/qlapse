from banners.models import QueueItemSource
from ..services import telegram_services, twilio_services


class SkipQueueItemProcessor:
    PROCESSORS = {
        QueueItemSource.TWILIO: twilio_services.HandleSkippedQueueItem,
        QueueItemSource.TELEGRAM: telegram_services.HandleSkippedQueueItem
    }

    def __init__(self, item):
        self.item = item

    def call(self):
        return self.PROCESSORS[self.item.source](self.item).call()
