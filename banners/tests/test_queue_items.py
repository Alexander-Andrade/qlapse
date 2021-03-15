from django.test import TestCase, Client
from banners.models import Banner, QueueItem, QueueItemStatus, QueueItemSource
from banners.models import BannerTelegram
from django.test.client import RequestFactory
from banners.views import next_queue_item, skip_queue_item, queue
from unittest.mock import patch
from django.contrib.auth import get_user_model
from django.core.files import File
from django.test import override_settings
import tempfile
from django.urls import reverse

User = get_user_model()


class NextQueueItemTwilio(TestCase):
    @override_settings(MEDIA_ROOT=tempfile.gettempdir())
    def setUp(self):
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

        next_queue_item(self.request, self.banner.id)

        self.assertFalse(QueueItem.objects.filter(id=self.queue_item1.id).exists())

    @patch('twilio.rest.Client.messages')
    def test_sms_sent_to_next_item(self, twilio_client_class):
        next_queue_item(self.request, self.banner.id)

        self.assertTrue(twilio_client_class.create.called)
        self.assertEqual(twilio_client_class.create.call_args[1]['from_'],
                         self.banner.phone_number)
        self.assertEqual(twilio_client_class.create.call_args[1]['to'],
                         self.queue_item1.phone_number)
        self.assertEqual(twilio_client_class.create.call_args[1]['body'],
                         'Your turn')

    @patch('twilio.rest.Client.messages')
    def test_next_item_status_changed(self, twilio_client_class):
        next_queue_item(self.request, self.banner.id)

        self.queue_item1.refresh_from_db()
        self.assertEqual(self.queue_item1.status, QueueItemStatus.PROCESSING)

    @patch('twilio.rest.Client.messages')
    def test_returns_queue_redirect(self, twilio_client_class):
        response = next_queue_item(self.request, self.banner.id)
        response.client = Client()

        self.assertRedirects(
            response,
            reverse('banners:queue', kwargs={'banner_id': self.banner.id}),
            target_status_code=302
        )


class NextQueueItemTelegram(TestCase):
    @override_settings(MEDIA_ROOT=tempfile.gettempdir())
    def setUp(self):
        user = User.objects.create_user(email='normal@user.com',
                                        password='foo',
                                        phone_number='+375293969579')

        self.banner = Banner.objects.create(
            upload=File(tempfile.NamedTemporaryFile(suffix='.pdf')),
            user=user,
            phone_number='+375293969579'
        )

        self.queue_item1 = self.banner.queue.create(
            phone_number='+375445677421',
            source=QueueItemSource.TELEGRAM,
            telegram_chat_id=1
        )

        BannerTelegram.objects.create(
            banner=self.banner, chat_id=self.queue_item1.telegram_chat_id
        )

        self.queue_item2 = self.banner.queue.create(
            phone_number='+375445677422',
            source=QueueItemSource.TELEGRAM,
            telegram_chat_id=2
        )

        BannerTelegram.objects.create(
            banner=self.banner, chat_id=self.queue_item2.telegram_chat_id
        )

        self.request_factory = RequestFactory()
        self.request = self.request_factory.\
            post(reverse("banners:next_queue_item",
                         kwargs={'banner_id': self.banner.id}))
        self.request.user = user

    @patch('telebot.TeleBot')
    @patch('telebot.types.ReplyKeyboardRemove')
    def test_message_sent_to_next_item(self, reply_class, bot_class):
        next_queue_item(self.request, self.banner.id)

        bot_class().send_message.assert_called_once_with(
            self.queue_item1.telegram_chat_id,
            'Your turn',
            reply_markup=reply_class()
        )

    @patch('telebot.TeleBot')
    def test_banner_telegram_object_deleted(self, bot_class):
        next_queue_item(self.request, self.banner.id)

        self.assertFalse(
            BannerTelegram.objects.filter(
                banner=self.banner,
                chat_id=self.queue_item1.telegram_chat_id
            )
        )

    @patch('telebot.TeleBot')
    def test_returns_queue_redirect(self, bot_class):
        response = next_queue_item(self.request, self.banner.id)
        response.client = Client()

        self.assertRedirects(
            response,
            reverse('banners:queue', kwargs={'banner_id': self.banner.id}),
            target_status_code=302
        )


class SkipQueueItem(TestCase):
    @override_settings(MEDIA_ROOT=tempfile.gettempdir())
    def setUp(self):
        User = get_user_model()
        user = User.objects.create_user(email='normal@user.com',
                                        password='foo',
                                        phone_number='+375293969579')

        self.banner = Banner.objects.create(
            upload=File(tempfile.NamedTemporaryFile(suffix='.pdf')),
            user=user,
            phone_number='+375293969579'
        )

        self.request_factory = RequestFactory()
        self.request = self.request_factory.\
            post(reverse("banners:next_queue_item",
                         kwargs={'banner_id': self.banner.id}))
        self.request.user = user

    def test_next_item_skipped(self):
        queue_item1 = self.banner.queue.create(
            phone_number='+375445677421')
        queue_item2 = self.banner.queue.create(
            phone_number='+375445877422')

        skip_queue_item(self.request, self.banner.id)

        self.assertFalse(
            self.banner.queue.filter(id=queue_item1.id).exists()
        )
        self.assertTrue(
            self.banner.queue.filter(id=queue_item2.id).exists()
        )

    @patch('django.contrib.messages.error')
    def test_failure_message_on_empty_queue(self, messages_error):
        skip_queue_item(self.request, self.banner.id)

        messages_error.assert_called_once_with(
            self.request, 'The queue is empty'
        )

    @patch('django.contrib.messages.error')
    def test_redirect_with_empty_queue(self, messages_error):
        response = skip_queue_item(self.request, self.banner.id)
        response.client = Client()

        self.assertRedirects(
            response,
            reverse('banners:queue', kwargs={'banner_id': self.banner.id}),
            target_status_code=302
        )

    def test_returns_queue_redirect(self):
        self.banner.queue.create(
            phone_number='+375445677421'
        )

        response = skip_queue_item(self.request, self.banner.id)
        response.client = Client()

        self.assertRedirects(
            response,
            reverse('banners:queue', kwargs={'banner_id': self.banner.id}),
            target_status_code=302
        )

    def test_banner_telegram_deleted(self):
        queue_item1 = self.banner.queue.create(
            phone_number='+375445677421',
            source=QueueItemSource.TELEGRAM,
            telegram_chat_id=2
        )
        BannerTelegram.objects.create(
            banner=self.banner, chat_id=queue_item1.telegram_chat_id
        )

        skip_queue_item(self.request, self.banner.id)

        self.assertFalse(
            BannerTelegram.objects.filter(
                banner=self.banner,
                chat_id=queue_item1.telegram_chat_id
            )
        )


class Queue(TestCase):
    @override_settings(MEDIA_ROOT=tempfile.gettempdir())
    def setUp(self):
        user = User.objects.create_user(email='normal@user.com',
                                        password='foo',
                                        phone_number='+375293969579')

        self.banner = Banner.objects.create(
            upload=File(tempfile.NamedTemporaryFile(suffix='.pdf')),
            user=user,
            phone_number='+375293969579'
        )

        self.queue_item1 = self.banner.queue.create(
            phone_number='+375445677421'
        )

        self.client = Client()
        self.client.login(username='normal@user.com',
                          password='foo')

    def test_queue_rendered(self):
        response = self.client.get(
            reverse('banners:queue', kwargs={'banner_id': self.banner.id})
        )

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'banners/queue.html')
        self.assertContains(response, self.queue_item1.phone_number)


class QueueEntrypoint(TestCase):
    @override_settings(MEDIA_ROOT=tempfile.gettempdir())
    def setUp(self):
        user = User.objects.create_user(email='normal@user.com',
                                        password='foo',
                                        phone_number='+375293969579')

        self.banner = Banner.objects.create(
            upload=File(tempfile.NamedTemporaryFile(suffix='.pdf')),
            user=user,
            phone_number='+375293969579'
        )

        self.queue_item1 = self.banner.queue.create(
            phone_number='+375445677421'
        )

        self.client = Client()

    def test_queue_entrypoint_rendered(self):
        response = self.client.get(
            reverse('banners:queue_entrypoint',
                    kwargs={'banner_id': self.banner.id})
        )

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'banners/queue_entrypoint.html')
        self.assertContains(response, self.banner.phone_number)
