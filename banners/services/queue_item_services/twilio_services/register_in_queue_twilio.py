from functools import cached_property

from banners.models import Banner
from django.conf import settings

from banners.services.queue_item_services.waiting_time.estimate_waiting_time import EstimateWaitingTime
from banners.templatetags.queue_filters import waiting_time_formatter
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
        if not self.banner:
            return self.error_msg_and_failure('The banner is not found')

        if self.find_queue_item():
            return self.error_msg_and_failure('You are already in the queue')

        self.queue_item

        sms_result = self.sms(
            body=f"You are in the queue. There are {self.queue_size - 1} in front of you. "
                 f"Waiting time estimation: {self.formatted_time_estimation}"
        )
        if sms_result.failed:
            return sms_result

        return Success(self.queue_item)

    @cached_property
    def formatted_time_estimation(self):
        return waiting_time_formatter(self.time_estimation)

    @cached_property
    def time_estimation(self):
        return EstimateWaitingTime(banner=self.banner, queue_item=self.queue_item).call()

    @cached_property
    def queue_item(self):
        return self.banner.queue.create(phone_number=self.client_phone_number)

    @cached_property
    def queue_size(self):
        return self.banner.queue.actual().count()

    def find_queue_item(self):
        return self.banner.queue.actual().filter(phone_number=self.client_phone_number).first()

    @cached_property
    def banner(self):
        return Banner.objects.filter(phone_number=self.banner_phone_number).first()

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
