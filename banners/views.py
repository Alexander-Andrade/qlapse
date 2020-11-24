from django.shortcuts import redirect, render
from .services.banner_creator import BannerCreator
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import ListView
from .models import Banner, QueueItem, QueueItemStatus
from twilio.twiml.voice_response import VoiceResponse, Say
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from .services.register_in_queue import RegisterInQueue
from datetime import datetime


@method_decorator(login_required, name='dispatch')
class BookingListView(ListView):
    model = Banner
    template_name = 'banners/index.html'
    context_object_name = 'banners'

    def get_queryset(self):
        queryset = super(BookingListView, self).get_queryset()
        queryset = queryset.filter(user=self.request.user)
        return queryset


@login_required
def create(request):
    if request.method == 'POST':
        creation_result = BannerCreator(user=request.user).create()

        if creation_result.succeed:
            return redirect('banners:index')
        else:
            return render(request, 'banners/index.html', {'error': creation_result.error})


@csrf_exempt
def twilio_on_banner_call_webhook(request):
    register_result = RegisterInQueue(
        client_phone_number=request.POST['From'],
        banner_phone_number=request.POST['To']
    ).register()

    response = VoiceResponse()

    if register_result.succeed:
        response.say('You are added to the queue')
    else:
        response.say('Failed to put you in the queue')
    return HttpResponse(str(response))

def queue_item(request, banner_id):
    banner= Banner.objects.get(pk=id)
    queue_items = Banner.objects.all()
    items = QueueItem.objects.filter()
    current_time = datetime.now()
    context = {"queue_items": queue_items, "current_time": current_time}
    return render(request, "banners/client.html", context)

def queue(request, banner_id):
    items = QueueItem.objects.filter()
    phone_numbers = QueueItem.objects.filter()
    context = {"items": items, "phone_numbers": phone_numbers}
    return render(request, "banners/queue.html", context)


def next(request):
    pass
    # queue_item = QueueItem.objects.get(pk=id)
    # status = QueueItemStatus.PROCESSED
    # next_status = QueueItemStatus.PROCESSING
    # context = {"queue_item": queue_item}
    # return render(request, "banners/queue.html", context)

def skip(request):
    pass

