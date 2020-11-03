from twilio.rest import Client
from django.conf import settings
import twilio
import pdb

class BuyTwilioNumber:

	def __init__(self):
		self.__set_twilio_client()

	def buy(self):
		phone_number_result = self.__get_us_phone_number()

		if 'error' in phone_number_result:
			return phone_number_result

		capabilities_result = self.__check_number_capabilities(phone_number_result['success'])

		if 'error' in capabilities_result:
			return capabilities_result

		return self.__buy_phone_number(phone_number_result['success'].phone_number)

	def __get_us_phone_number(self, limit=1):
		try:
			phone_numbers = self.client.available_phone_numbers('US').\
				local.list(limit=limit)
		except twilio.base.exceptions.TwilioException as e:
			return {'error': e.message}

		return {'success': phone_numbers[0]}

	def __check_number_capabilities(self, phone_number_info):
		if not phone_number_info.capabilities['SMS'] is False:
			return {'success': None}
		return {'error': 'There is no sms capability'}

	def __buy_phone_number(self, phone_number):
		try:
			bought_number_info = self.client.incoming_phone_numbers.\
			create(phone_number=phone_number)
		except twilio.base.exceptions.TwilioRestException as e:
			return {'error': e.message}

		return {'success': bought_number_info.phone_number}

	def __set_twilio_client(self):
		self.client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_ACCOUNT_TOKEN)
