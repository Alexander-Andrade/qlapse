from banners.models import Banner, QueueItemSource, BannerTelegram
from shared.services.result import Success, Failure
from telebot import types


class CalcPeopleAhead:
    def __init__(self, message, bot):
        self.message = message
        self.bot = bot

    def call(self):
        banner_telegram = BannerTelegram.objects. \
            filter(chat_id=self.message.chat.id).first()
        if not banner_telegram:
            return self.error_msg_and_failure(
                f"unknown banner for the chat id: {self.message.chat.id}"
            )

        banner = Banner.objects.filter(pk=banner_telegram.banner_id).first()
        if not banner:
            return self.error_msg_and_failure(
                'banner not found'
            )

        queue_item = banner.queue.actual().\
            filter(telegram_chat_id=self.message.chat.id).first()
        if not queue_item:
            return self.error_msg_and_failure(
                'queue item not found'
            )

        people_ahead = banner.queue.actual().\
            filter(position__lt=queue_item.position).count()
        queue_msg = f"There are {people_ahead} in front of you."

        markup = types.ReplyKeyboardMarkup(row_width=1)
        queue_length_btn = types.KeyboardButton('/check queue length')
        markup.add(queue_length_btn)
        self.bot.send_message(self.message.chat.id, queue_msg,
                              reply_markup=markup)

        return Success(queue_item)

    def error_msg_and_failure(self, failure_msg):
        self.bot.send_message(self.message.chat.id, failure_msg)
        return Failure(failure_msg)
