import telebot
from telebot import types
from banners.models import BannerTelegram
from django.conf import settings
from shared.services.result import Success, Failure


class NotifyNextPersonInLine:
    def __init__(self, item):
        self.item = item
        self.bot = telebot.TeleBot(settings.TELEGRAM_QUEUE_BOT_TOKEN)

    def call(self):
        markup = types.ReplyKeyboardRemove()
        self.bot.send_message(self.item.telegram_chat_id, 'Your turn',
                              reply_markup=markup)
        BannerTelegram.objects.filter(
            banner=self.item.banner, chat_id=self.item.telegram_chat_id
        ).delete()
        return Success()
