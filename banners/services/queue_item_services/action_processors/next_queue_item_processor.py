from banners.models import QueueItemSource
from banners.services.queue_item_services import telegram_services, twilio_services


class NextQueueItemProcessor:
    PROCESSORS = {
        QueueItemSource.TWILIO: twilio_services.NotifyNextPersonInLine,
        QueueItemSource.TELEGRAM: telegram_services.NotifyNextPersonInLine
    }

    def __init__(self, item):
        self.item = item

    def call(self):
        return self.PROCESSORS[self.item.source](self.item).call()
