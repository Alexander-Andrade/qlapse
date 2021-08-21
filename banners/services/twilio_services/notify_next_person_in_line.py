from django.conf import settings
from twilio.rest import Client
from shared.services.result import Success, Failure
import twilio


class NotifyNextPersonInLine:
    def __init__(self, item):
        self.client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_ACCOUNT_TOKEN)
        self.item = item

    def call(self):
        try:
            self.client.messages.create(
                body=f"Your turn",
                from_=self.item.banner.phone_number,
                to=self.item.phone_number
            )
            return Success(self.item)
        except twilio.base.exceptions.TwilioException as e:
            return Failure(e.msg)
