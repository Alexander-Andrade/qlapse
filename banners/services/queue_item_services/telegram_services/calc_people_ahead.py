from functools import cached_property

from banners.models import Banner, QueueItemSource, BannerTelegram
from shared.services.result import Success, Failure
from telebot import types


class CalcPeopleAhead:
    def __init__(self, message, bot):
        self.message = message
        self.bot = bot

    def call(self):
        if not self.banner_telegram:
            return self.error_msg_and_failure(
                f"unknown banner for the chat id: {self.message.chat.id}"
            )

        if not self.banner:
            return self.error_msg_and_failure(
                'banner not found'
            )

        if not self.queue_item:
            return self.error_msg_and_failure(
                'queue item not found'
            )

        self.send_message_to_bot()

        return Success(self.queue_item)

    @cached_property
    def banner_telegram(self):
        return BannerTelegram.objects.filter(chat_id=self.message.chat.id).first()

    @cached_property
    def banner(self):
        return Banner.objects.filter(pk=self.banner_telegram.banner_id).first()

    @cached_property
    def queue_item(self):
        return self.banner.queue.actual().filter(telegram_chat_id=self.message.chat.id).first()

    @cached_property
    def people_ahead_count(self):
        return self.banner.queue.actual().filter(position__lt=self.queue_item.position).count()

    def send_message_to_bot(self):
        queue_msg = f"There are {self.people_ahead_count} in front of you."

        markup = types.ReplyKeyboardMarkup(row_width=1)
        queue_length_btn = types.KeyboardButton('/check queue length')
        markup.add(queue_length_btn)
        self.bot.send_message(self.message.chat.id, queue_msg,
                              reply_markup=markup)

    def error_msg_and_failure(self, failure_msg):
        self.bot.send_message(self.message.chat.id, failure_msg)
        return Failure(failure_msg)
