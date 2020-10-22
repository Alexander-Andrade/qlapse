from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy

from .models import Banner


@method_decorator(login_required, name='dispatch')
class BannerCreateView(CreateView):
    model = Banner
    template_name = 'banners/index.html'
    success_url = reverse_lazy('banner-list')
