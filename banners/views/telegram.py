from django.views.decorators.csrf import csrf_exempt
from django.views import View
from django.utils.decorators import method_decorator
import json
import telebot
from django.conf import settings
from django.http import JsonResponse
import logging
from ..services import RegisterInQueueTelegram, StartCommandHandler, CalcPeopleAhead

bot = telebot.TeleBot(settings.TELEGRAM_QUEUE_BOT_TOKEN)
logger = logging.getLogger(__name__)


@method_decorator(csrf_exempt, name='dispatch')
class TelegramQueueWebhookView(View):
    def post(self, request, *args, **kwargs):
        body = json.loads(request.body)
        logger.error(body)
        update = telebot.types.Update.de_json(body)
        bot.process_new_updates([update])
        return JsonResponse({"ok": ""})


# https://t.me/QlapseBot?start=17
# deep linking https://core.telegram.org/bots#deep-linking
@bot.message_handler(commands=['start'])
def show_send_mobile_button(message):
    StartCommandHandler(message=message, bot=bot).call()


@bot.message_handler(content_types=['contact'])
def phone_number_acquired(message):
    RegisterInQueueTelegram(message=message, bot=bot).register()


@bot.message_handler(commands=['check'])
def calc_people_ahead(message):
    CalcPeopleAhead(message=message, bot=bot).call()
