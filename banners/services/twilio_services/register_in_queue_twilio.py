from banners.models import Banner
from django.conf import settings
from shared.services.result import Success, Failure
from twilio.rest import Client
import twilio


class RegisterInQueueTwilio:

    def __init__(self, client_phone_number, banner_phone_number):
        self.client_phone_number = client_phone_number
        self.banner_phone_number = banner_phone_number
        self.client = Client(settings.TWILIO_ACCOUNT_SID,
                             settings.TWILIO_ACCOUNT_TOKEN)

    def register(self):
        banner = Banner.objects.\
            filter(phone_number=self.banner_phone_number).first()

        if not banner:
            return self.error_msg_and_failure('The banner is not found')

        queue_item = banner.queue.\
            filter(phone_number=self.client_phone_number).first()
        if queue_item:
            return self.error_msg_and_failure('You are already in the queue')

        queue_size = banner.queue.count()
        queue_item = banner.queue.create(phone_number=self.client_phone_number)

        sms_result = self.sms(
            body=f"You are in the queue. There are {queue_size} in front of you."
        )
        if sms_result.failed:
            return sms_result

        return Success(queue_item)

    def sms(self, body):
        try:
            self.client.messages.create(
                body=body,
                from_=self.banner_phone_number,
                to=self.client_phone_number
            )
            return Success()
        except twilio.base.exceptions.TwilioException as e:
            return Failure(e['message'])

    def error_msg_and_failure(self, failure_msg):
        self.sms(body=failure_msg)
        return Failure(failure_msg)
