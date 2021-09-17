from django.shortcuts import redirect, render, get_object_or_404
from banners.services.queue_item_services.next_queue_item import NextQueueItem
from banners.services.queue_item_services.skip_item import SkipItem
from django.contrib.auth.decorators import login_required
from ..models import Banner
from django.contrib import messages

from ..services.queue_item_services.estimate_waiting_time import EstimateWaitingTime


@login_required
def queue(request, banner_id):
    banner = get_object_or_404(Banner, pk=banner_id)
    context = {'banner': banner, 'queue_items': banner.queue.all()}

    return render(request, 'banners/queue.html', context)


@login_required
def next_queue_item(request, banner_id):
    banner = get_object_or_404(Banner, pk=banner_id)
    next_item_result = NextQueueItem(banner=banner).next()

    if next_item_result.failed:
        messages.error(request, next_item_result.error)

    return redirect('banners:queue', banner_id=banner_id)


@login_required
def skip_queue_item(request, banner_id):
    banner = get_object_or_404(Banner, pk=banner_id)
    skip_item_result = SkipItem(banner=banner).skip()

    if skip_item_result.failed:
        messages.error(request, skip_item_result.error)

    return redirect('banners:queue', banner_id=banner_id)


def queue_entrypoint(request, banner_id):
    banner = get_object_or_404(Banner, pk=banner_id)
    time_estimation = EstimateWaitingTime(banner=banner).call()
    context = {'banner': banner, 'time_estimation': time_estimation}

    return render(request, 'banners/queue_entrypoint.html', context)
