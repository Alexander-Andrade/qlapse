from banners.models import Banner, BannerTelegram
from banners.services.queue_item_services.estimate_waiting_time import EstimateWaitingTime
from banners.templatetags.queue_filters import waiting_time_formatter
from shared.services.result import Success, Failure
from telebot import types


class StartCommandHandler:
    def __init__(self, bot, message):
        self.bot = bot
        self.message = message

    def call(self):
        banner_id = self.message.text.split()[1]
        banner = Banner.objects.filter(pk=banner_id).first()

        if not banner:
            return self.error_msg_and_failure('the banner is not found')

        banner_telegram = BannerTelegram.objects.\
            filter(banner=banner, chat_id=self.message.chat.id).first()
        if banner_telegram:
            return self.error_msg_and_failure('You are already in the queue')

        BannerTelegram.objects.create(banner=banner, chat_id=self.message.chat.id)

        markup = types.ReplyKeyboardMarkup(row_width=1, one_time_keyboard=True)
        send_mobile_number_btn = types.KeyboardButton('share contact & get in line',
                                                      request_contact=True)
        markup.add(send_mobile_number_btn)
        time_estimation = EstimateWaitingTime(banner=banner).call()
        queue_msg = f"There are {banner.queue.actual().count()} in front of you. " \
                    f"Waiting time estimation: " \
                    f"{waiting_time_formatter(time_estimation)}"
        self.bot.send_message(self.message.chat.id, queue_msg,
                              reply_markup=markup)

        return Success()

    def error_msg_and_failure(self, failure_msg):
        self.bot.send_message(self.message.chat.id, failure_msg)
        return Failure(failure_msg)
