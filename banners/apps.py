from django.apps import AppConfig
import telebot
from django.conf import settings
import time


class BannersConfig(AppConfig):
    name = 'banners'

    def ready(self):
        if settings.DEBUG:
            bot = telebot.TeleBot(settings.TELEGRAM_QUEUE_BOT_TOKEN)
            bot.remove_webhook()
            time.sleep(settings.TELEGRAM_API_INTERVAL)
            bot.set_webhook(url=settings.TELEGRAM_QUEUE_BOT_WEBHOOK_URL)
