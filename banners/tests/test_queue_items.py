from django.test import TestCase
from banners.models import *
from django.test.client import RequestFactory
from banners.views import next_queue_item, skip_queue_item
from unittest.mock import patch
from django.contrib.auth import get_user_model
from django.core.files import File
from django.test import override_settings
import tempfile
from django.urls import reverse
import sys


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
