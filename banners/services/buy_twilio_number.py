from twilio.rest import Client
from django.conf import settings
import twilio
from shared.services.result import Success, Failure


class BuyTwilioNumber:
    COUNTRY_CODE = 'US'
    AVAILABLE_PHONE_NUMBERS_LIMIT = 1

    def __init__(self):
        self.__set_twilio_client()

    def buy(self):
        phone_number_result = self.__get_us_phone_number()

        if phone_number_result.failed:
            return phone_number_result

        capabilities_result = \
            self.__check_number_capabilities(phone_number_result.result)

        if capabilities_result.failed:
            return capabilities_result

        return self.__buy_phone_number(phone_number_result.result.phone_number)

    def __get_us_phone_number(self):
        try:
            phone_numbers = \
                self.client.available_phone_numbers(self.COUNTRY_CODE).\
                local.list(limit=self.AVAILABLE_PHONE_NUMBERS_LIMIT)
        except twilio.base.exceptions.TwilioException as e:
            return Failure(e['message'])

        return Success(phone_numbers[0])

    def __check_number_capabilities(self, phone_number_info):
        if not phone_number_info.capabilities['SMS'] is False:
            return Success()
        return Failure('There is no sms capability')

    def __buy_phone_number(self, phone_number):
        try:
            bought_number_info = self.client.incoming_phone_numbers.\
                create(
                    phone_number=phone_number,
                    voice_url=settings.TWILIO_BANNER_CALL_CALLBACK_URL,
                    voice_method='POST'
                )
        except twilio.base.exceptions.TwilioRestException as e:
            return Failure(e.msg)

        return Success(bought_number_info.phone_number)

    def __set_twilio_client(self):
        self.client = Client(settings.TWILIO_ACCOUNT_SID,
                             settings.TWILIO_ACCOUNT_TOKEN)
