from django.test import TestCase
from .services.banner_creator import BannerCreator
from banners.models import *
import vcr
from django.test.client import RequestFactory
from banners.views import twilio_on_banner_call_webhook, next_queue_item, skip_queue_item
from unittest.mock import patch
from django.contrib.auth import get_user_model
from django.core.files import File
from django.test import override_settings
import tempfile
from django.urls import reverse
import sys


class BannerCreatorTest(TestCase):
    def setUp(self):
        User = get_user_model()
        self.user = User.objects.\
            create_user(email='test@gmail.com', phone_number="+375293969579", password='password')

    @vcr.use_cassette('banners/tests/cassettes/banner_creator_create.yaml')
    def test_create(self):
        creation_result = BannerCreator(user=self.user).create()
        self.assertIsInstance(creation_result.result, Banner)


class TwilioOnBannerCallWebhook(TestCase):
    @override_settings(MEDIA_ROOT=tempfile.gettempdir())
    def setUp(self):
        self.request_factory = RequestFactory()
        self.banner_number = '+16175551212'
        self.client_number = '+16173251789'
        self.request_data = { 'CallSid': 'callsid', 'AccountSid': 'ACXXXX', 'From': self.client_number,
                                              'To': self.banner_number, 'CallStatus': 'ringing' }
        self.request = self.request_factory.post('/banners/twilio_on_banner_call_webhook', self.request_data)
        User = get_user_model()
        user = User.objects.create_user(email='normal@user.com', password='foo', phone_number='+375293969579')

        self.banner = Banner.objects.create(
            upload=File(tempfile.NamedTemporaryFile(suffix='.pdf')),
            user=user,
            phone_number=self.banner_number
        )

    @override_settings(MEDIA_ROOT=tempfile.gettempdir())
    @patch('twilio.rest.Client.messages')
    def test_twilml_response(self, twilio_client_class):
        response = twilio_on_banner_call_webhook(self.request)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "You are added to the queue")

    @override_settings(MEDIA_ROOT=tempfile.gettempdir())
    @patch('twilio.rest.Client.messages')
    def test_queue_item_created(self, twilio_client_class):
        response = twilio_on_banner_call_webhook(self.request)
        queue_item = QueueItem.objects.filter(phone_number=self.client_number)
        self.assertTrue(queue_item.exists())
        self.assertEqual(queue_item[0].banner, self.banner)

    @override_settings(MEDIA_ROOT=tempfile.gettempdir())
    @patch('twilio.rest.Client.messages')
    def test_sms(self, twilio_client_class):
        response = twilio_on_banner_call_webhook(self.request)

        self.assertTrue(twilio_client_class.create.called)
        self.assertEqual(twilio_client_class.create.call_args[1]['from_'], self.banner_number)
        self.assertEqual(twilio_client_class.create.call_args[1]['to'], self.client_number)
        self.assertEqual(twilio_client_class.create.call_args[1]['body'], 'You are in Queue. There are 0 in front of you.')


class NextQueueItem(TestCase):
    @override_settings(MEDIA_ROOT=tempfile.gettempdir())
    def setUp(self):
        User = get_user_model()
        user = User.objects.create_user(email='normal@user.com', password='foo', phone_number='+375293969579')

        self.banner = Banner.objects.create(
            upload=File(tempfile.NamedTemporaryFile(suffix='.pdf')),
            user=user,
            phone_number='+375293969579'
        )

        self.queue_item1 = self.banner.queue.create(phone_number='+375445677421')

        self.queue_item2 = self.banner.queue.create(phone_number='+375445677422')

        self.request_factory = RequestFactory()
        self.request = self.request_factory.\
            post(reverse("banners:next_queue_item", kwargs={'banner_id': self.banner.id}))
        self.request.user = user

    @patch('twilio.rest.Client.messages')
    def test_removes_first_queue_element_if_it_has_processing_status(self, twilio_client_class):
        self.queue_item1.status = QueueItemStatus.PROCESSING
        self.queue_item1.save()

        response = next_queue_item(self.request, self.banner.id)

        self.assertFalse(QueueItem.objects.filter(id=self.queue_item1.id).exists())

    @patch('twilio.rest.Client.messages')
    def test_sms_sent_to_next_item(self, twilio_client_class):
        response = next_queue_item(self.request, self.banner.id)

        self.assertTrue(twilio_client_class.create.called)
        self.assertEqual(twilio_client_class.create.call_args[1]['from_'], self.banner.phone_number)
        self.assertEqual(twilio_client_class.create.call_args[1]['to'], self.queue_item1.phone_number)
        self.assertEqual(twilio_client_class.create.call_args[1]['body'], 'Your turn')

    @patch('twilio.rest.Client.messages')
    def test_next_item_status_changed(self, twilio_client_class):
        response = next_queue_item(self.request, self.banner.id)

        self.queue_item1.refresh_from_db()
        self.assertEqual(self.queue_item1.status, QueueItemStatus.PROCESSING)


class SkipQueueItem(TestCase):
    @override_settings(MEDIA_ROOT=tempfile.gettempdir())
    def setUp(self):
        User = get_user_model()
        user = User.objects.create_user(email='normal@user.com', password='foo', phone_number='+375293969579')

        self.banner = Banner.objects.create(
            upload=File(tempfile.NamedTemporaryFile(suffix='.pdf')),
            user=user,
            phone_number='+375293969579'
        )

        self.request_factory = RequestFactory()
        self.request = self.request_factory.\
            post(reverse("banners:next_queue_item", kwargs={'banner_id': self.banner.id}))
        self.request.user = user

    def test_next_item_skipped(self):
        self.queue_item1 = self.banner.queue.create(phone_number='+375445677421')
        self.queue_item2 = self.banner.queue.create(phone_number='+375445677422')

        response = skip_queue_item(self.request, self.banner.id)

        self.assertFalse(QueueItem.objects.filter(id=self.queue_item1.id).exists())

    def test_empty_queue_nothing_skipped(self):
        try:
            response = skip_queue_item(self.request, self.banner.id)
        except:
            e = sys.exc_info()[0]
            self.fail(f'exception where raised, when queue is empty:')
