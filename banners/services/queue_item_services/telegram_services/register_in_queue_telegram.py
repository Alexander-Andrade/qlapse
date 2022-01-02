from functools import cached_property

from banners.models import Banner, QueueItemSource, BannerTelegram
from banners.services.queue_item_services.waiting_time.estimate_waiting_time import EstimateWaitingTime
from banners.templatetags.queue_filters import waiting_time_formatter
from shared.services.result import Success, Failure
from telebot import types


class RegisterInQueueTelegram:
    def __init__(self, bot, message):
        self.bot = bot
        self.message = message

    def register(self):
        if not self.banner_telegram:
            return self.error_msg_and_failure(f"unknown banner for the chat id: {self.message.chat.id}")

        if not self.banner:
            return self.error_msg_and_failure('banner not found')

        self.send_bot_message()

        return Success(self.queue_item)

    @cached_property
    def queue_msg(self):
        return f"You are in Queue. There are {self.queue_size} in front of you." \
               f"Waiting time estimation: {waiting_time_formatter(self.time_estimation)}"

    def send_bot_message(self):
        markup = types.ReplyKeyboardMarkup(row_width=1)
        queue_length_btn = types.KeyboardButton('/check queue length')
        markup.add(queue_length_btn)
        self.bot.send_message(self.message.chat.id, self.queue_msg,
                              reply_markup=markup)

    @cached_property
    def time_estimation(self):
        return EstimateWaitingTime(banner=self.banner, queue_item=self.queue_item).call()

    @cached_property
    def queue_item(self):
        return self.banner.queue.create(
            phone_number=self.message.contact.phone_number,
            source=QueueItemSource.TELEGRAM,
            telegram_chat_id=self.message.chat.id
        )

    @cached_property
    def queue_size(self):
        return self.banner.queue.actual().count()

    @cached_property
    def banner(self):
        return Banner.objects.filter(pk=self.banner_telegram.banner_id).first()

    @cached_property
    def banner_telegram(self):
        return BannerTelegram.objects.filter(chat_id=self.message.chat.id).first()

    def error_msg_and_failure(self, failure_msg):
        self.bot.send_message(self.message.chat.id, failure_msg)
        return Failure(failure_msg)
