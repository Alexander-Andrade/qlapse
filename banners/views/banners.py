from ..services.banner_creator import BannerCreator
from django.utils.decorators import method_decorator
from django.views.generic import ListView
from django.contrib.auth.decorators import login_required
from ..models import Banner
from django.contrib import messages
from django.shortcuts import redirect
from django.conf import settings


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

        if creation_result.failed:
            messages.error(request, creation_result.error)

        return redirect('banners:index')
