from django.shortcuts import redirect, render, get_object_or_404
from .services.banner_creator import BannerCreator
from .services.next_queue_item import NextQueueItem
from .services.skip_item import SkipItem
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import ListView
from .models import Banner, QueueItem
from twilio.twiml.voice_response import VoiceResponse, Say
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from .services.register_in_queue import RegisterInQueue


@method_decorator(login_required, name='dispatch')
class BannersListView(ListView):
    model = Banner
    template_name = 'banners/index.html'
    context_object_name = 'banners'

    def get_queryset(self):
        queryset = super(BannersListView, self).get_queryset()
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


@login_required
def queue(request, banner_id):
    banner = get_object_or_404(Banner, pk=banner_id)
    context = {'banner': banner, 'queue_items': banner.queue.all()}

    return render(request, 'banners/queue.html', context)


@login_required
def next_queue_item(request, banner_id):
    banner = Banner.objects.filter(id=banner_id).first()
    next_item_result = NextQueueItem(banner=banner).next()

    # TODO redirect to the queue page


@login_required
def skip_queue_item(request, banner_id):
    banner = Banner.objects.filter(id=banner_id).first()
    next_item_result = SkipItem(banner=banner).skip()

    # TODO redirect to the queue page
