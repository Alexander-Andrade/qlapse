from functools import cached_property

from banners.models import Banner, BannerTelegram
from banners.services.queue_item_services.waiting_time.estimate_waiting_time import EstimateWaitingTime
from banners.templatetags.queue_filters import waiting_time_formatter
from shared.services.result import Success, Failure
from telebot import types


class StartCommandHandler:
    def __init__(self, bot, message):
        self.bot = bot
        self.message = message

    def call(self):
        if not self.banner:
            return self.error_msg_and_failure('the banner is not found')

        banner_telegram_result = self.filter_or_create_banner_telegram()
        if banner_telegram_result.failed:
            return banner_telegram_result

        self.send_bot_message()

        return Success()

    def send_bot_message(self):
        markup = types.ReplyKeyboardMarkup(row_width=1, one_time_keyboard=True)
        send_mobile_number_btn = types.KeyboardButton('share contact & get in line',
                                                      request_contact=True)
        markup.add(send_mobile_number_btn)
        queue_msg = f"There are {self.queue_size} in front of you. " \
                    f"Waiting time estimation: " \
                    f"{self.formatted_time_estimation}"
        self.bot.send_message(self.message.chat.id, queue_msg,reply_markup=markup)

    @cached_property
    def queue_size(self):
        return self.banner.queue.actual().count()

    @cached_property
    def formatted_time_estimation(self):
        return waiting_time_formatter(self.time_estimation)

    @cached_property
    def time_estimation(self):
        return EstimateWaitingTime(banner=self.banner).call()

    @cached_property
    def banner(self):
        return Banner.objects.filter(pk=self.banner_id).first()

    def filter_or_create_banner_telegram(self):
        banner_telegram = BannerTelegram.objects.filter(banner=self.banner,
                                                        chat_id=self.message.chat.id).first()

        if banner_telegram:
            return self.error_msg_and_failure('You are already in the queue')

        banner_telegram = BannerTelegram.objects.create(banner=self.banner, chat_id=self.message.chat.id)
        return Success(banner_telegram)

    @property
    def banner_id(self):
        return self.message.text.split()[1]

    def error_msg_and_failure(self, failure_msg):
        self.bot.send_message(self.message.chat.id, failure_msg)
        return Failure(failure_msg)
