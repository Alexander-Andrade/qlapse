from .models import CustomUser
from django.views.generic.edit import CreateView
from .forms import CustomUserCreationForm
from django.urls import reverse_lazy
from django.db import transaction
from .services.send_activation_email import SendActivationEmail
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
from django.http import HttpResponse
from django.shortcuts import redirect
from django.views.generic.base import TemplateView


class CustomUserCreate(CreateView):
    model = CustomUser
    template_name = 'accounts/registration.html'
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('accounts:confirm_activation')

    @transaction.atomic
    def form_valid(self, form):
        response = super(CustomUserCreate, self).form_valid(form)

        self.object.is_active = False
        self.object.save()

        SendActivationEmail(user=self.object, request=self.request).send()

        return response


class ConfirmActivationView(TemplateView):
    template_name = 'accounts/confirm_activation.html'


def activate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = CustomUser._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
        user = None
    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        return redirect('payments:add_payment_method')
    else:
        return HttpResponse('Activation link is invalid!')

