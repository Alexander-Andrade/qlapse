from twilio.twiml.voice_response import VoiceResponse
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from banners.services.twilio_services.register_in_queue_twilio import RegisterInQueueTwilio


@csrf_exempt
def twilio_on_banner_call_webhook(request):
    register_result = RegisterInQueueTwilio(
        client_phone_number=request.POST['From'],
        banner_phone_number=request.POST['To']
    ).register()

    response = VoiceResponse()

    if register_result.succeed:
        response.say('You are added to the queue')
    else:
        response.say('Failed to put you in the queue')

    return HttpResponse(str(response))
