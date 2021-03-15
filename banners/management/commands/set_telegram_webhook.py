import telebot
import time
from django.core.management.base import BaseCommand
from django.conf import settings


class Command(BaseCommand):
    help = 'To use telegram bot you need to set webhook'

    def handle(self, *args, **options):
        bot = telebot.TeleBot(settings.TELEGRAM_QUEUE_BOT_TOKEN)
        if not options['no_reset']:
            bot.remove_webhook()
        time.sleep(settings.TELEGRAM_API_INTERVAL)
        bot.set_webhook(url=settings.TELEGRAM_QUEUE_BOT_WEBHOOK_URL)

    def add_arguments(self, parser):
        parser.add_argument(
            '-n',
            '--no-reset',
            action='store_true',
            default=False,
            help='Without old webhooks reset'
        )
