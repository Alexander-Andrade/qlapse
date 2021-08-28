from django.test import TestCase
from django.test.client import RequestFactory
from unittest.mock import patch

from banners.tests.factories.banners import BannerFactory
from banners.views import twilio_on_banner_call_webhook
from banners.models import QueueItem


class TwilioOnBannerCallWebhook(TestCase):
    def setUp(self):
        self.request_factory = RequestFactory()
        self.banner_number = '+16175551212'
        self.client_number = '+16173251789'
        self.request_data = { 'CallSid': 'callsid', 'AccountSid': 'ACXXXX', 'From': self.client_number,
                                              'To': self.banner_number, 'CallStatus': 'ringing' }
        self.request = self.request_factory.post('/banners/twilio_on_banner_call_webhook', self.request_data)
        self.banner = BannerFactory(phone_number=self.banner_number)

    @patch('twilio.rest.Client.messages')
    def test_twilml_response(self, twilio_client_class):
        response = twilio_on_banner_call_webhook(self.request)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "You are added to the queue")

    @patch('twilio.rest.Client.messages')
    def test_queue_item_created(self, twilio_client_class):
        twilio_on_banner_call_webhook(self.request)
        queue_item = QueueItem.objects.filter(phone_number=self.client_number)
        self.assertTrue(queue_item.exists())
        self.assertEqual(queue_item[0].banner, self.banner)

    @patch('twilio.rest.Client.messages')
    def test_sms(self, twilio_client_class):
        twilio_on_banner_call_webhook(self.request)

        self.assertTrue(twilio_client_class.create.called)
        self.assertEqual(twilio_client_class.create.call_args[1]['from_'], self.banner_number)
        self.assertEqual(twilio_client_class.create.call_args[1]['to'], self.client_number)
        self.assertEqual(
            twilio_client_class.create.call_args[1]['body'],
            'You are in the queue. There are 0 in front of you.'
        )
