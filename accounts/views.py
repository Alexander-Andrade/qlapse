from django.shortcuts import render
from django.urls import reverse
from .models import CustomUser
import pdb
from django.views.generic.edit import CreateView
from .forms import CustomUserCreationForm
from django.urls import reverse_lazy


class CustomUserCreate(CreateView):
    model = CustomUser
    template_name = 'accounts/registration.html'
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('payments:add_payment_method')
