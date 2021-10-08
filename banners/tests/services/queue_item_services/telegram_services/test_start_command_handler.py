from django.test import TestCase
from unittest.mock import patch, Mock

from banners.services import StartCommandHandler
from banners.tests.factories.banner_telegrams import BannerTelegramFactory
from banners.tests.factories.banners import BannerFactory
from banners.tests.factories.queue_items import QueueItemFactory
from shared.services.result import Success


class TestStartCommandHandler(TestCase):
    def setUp(self):
        self.banner = BannerFactory()

    @patch('telebot.TeleBot')
    def test_banner_not_found(self, telebot_class):
        message = Mock()
        message.chat.id = 1
        message.text = "/start 150"

        bot = telebot_class()
        result = StartCommandHandler(bot=bot, message=message).call()
        self.assertEqual(result.error, 'the banner is not found')

        self.assertTrue(telebot_class().send_message.called)

        self.assertEqual(
            telebot_class().send_message.call_args[0],
            (1, 'the banner is not found')
        )

    @patch('telebot.TeleBot')
    def test_double_queue_join(self, telebot_class):
        message = Mock()
        message.chat.id = 1
        message.text = f"/start {self.banner.id}"
        bot = telebot_class()
        BannerTelegramFactory(banner=self.banner, chat_id=message.chat.id)

        result = StartCommandHandler(bot=bot, message=message).call()

        self.assertEqual(result.error, 'You are already in the queue')

        self.assertEqual(
            telebot_class().send_message.call_args[0],
            (1, 'You are already in the queue')
        )

    @patch('telebot.TeleBot')
    def test_text_back_to_user(self, telebot_class):
        message = Mock()
        message.chat.id = 1
        message.text = f"/start {self.banner.id}"
        bot = telebot_class()

        QueueItemFactory(banner=self.banner)

        result = StartCommandHandler(bot=bot, message=message).call()

        self.assertIsInstance(result, Success)

        self.assertEqual(
            telebot_class().send_message.call_args[0],
            (1, "There are 1 in front of you. Waiting time estimation: ∞")
        )
