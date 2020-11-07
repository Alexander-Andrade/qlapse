from django.shortcuts import redirect, render
from .services.banner_creator import BannerCreator
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import ListView
from .models import Banner


@method_decorator(login_required, name='dispatch')
class BookingListView(ListView):
    model = Banner
    template_name = 'banners/index.html'
    context_object_name = 'banners'


@login_required
def create(request):
    if request.method == 'POST':
        creation_result = BannerCreator(user=request.user).create()

        if creation_result.succeed:
            return redirect('banners:index')
        else:
            return render(request, 'banners/index.html', {'error': creation_result.error})
