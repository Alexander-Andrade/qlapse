from banners.models import QueueItem, Banner
from django.conf import settings
from shared.services.result import Success, Failure
from twilio.rest import Client
import twilio


class RegisterInQueue:

    def __init__(self, client_phone_number, banner_phone_number):
        self.client_phone_number = client_phone_number
        self.banner_phone_number = banner_phone_number
        self.client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_ACCOUNT_TOKEN)

    def register(self):
        banner = Banner.objects.get(phone_number=self.banner_phone_number)

        if not banner:
            return Failure('banner is not found')

        queue_size = banner.queue.count()
        queue_item = banner.queue.create(phone_number=self.client_phone_number)

        try:
            self.client.messages.create(
                body=f"You are in Queue. There are {queue_size} in front of you.",
                from_=self.banner_phone_number,
                to=self.client_phone_number
            )
        except twilio.base.exceptions.TwilioException as e:
            return Failure(e['message'])

        return Success(queue_item)
