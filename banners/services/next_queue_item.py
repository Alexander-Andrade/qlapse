from django.conf import settings
from shared.services.result import Success, Failure
from banners.models import *
from twilio.rest import Client
import twilio


class NextQueueItem:

    def __init__(self, banner):
        self.banner = banner
        self.client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_ACCOUNT_TOKEN)

    def next(self):
        if not self.banner:
            return Failure('banner is not found')

        current_item = self.banner.queue.filter(status=QueueItemStatus.PROCESSING).first()
        if current_item:
            current_item.delete()

        next_item = self.banner.queue.first()

        if not next_item:
            # empty queue
            return Success()

        next_item.status = QueueItemStatus.PROCESSING
        next_item.save()

        return self.__send_sms(item=next_item)

    def __send_sms(self, item):
        try:
            self.client.messages.create(
                body=f"Your turn",
                from_=self.banner.phone_number,
                to=item.phone_number
            )
            return Success(item)
        except twilio.base.exceptions.TwilioException as e:
            return Failure(e['message'])
