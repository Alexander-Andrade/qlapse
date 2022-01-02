from common.utils import fake_phone_number
from django.conf import settings

from shared.services.result import Success
from .buy_twilio_number import BuyTwilioNumber


class BuyOrFakePhoneNumber:
    def __init__(self, fake_banner_number=settings.FAKE_BANNER_PHONE_NUMBERS):
        self.fake_banner_number = fake_banner_number

    def call(self):
        if self.fake_banner_number:
            return Success(fake_phone_number())
        else:
            return BuyTwilioNumber().buy()
