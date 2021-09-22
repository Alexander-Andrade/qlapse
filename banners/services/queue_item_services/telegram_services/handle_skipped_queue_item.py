from banners.models import BannerTelegram
from shared.services.result import Success


class HandleSkippedQueueItem:
    def __init__(self, item):
        self.item = item

    def call(self):
        BannerTelegram.objects.filter(
            banner=self.item.banner, chat_id=self.item.telegram_chat_id
        ).delete()
        return Success()
