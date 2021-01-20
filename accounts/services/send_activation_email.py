from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.utils.encoding import force_bytes
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse


class SendActivationEmail:
    def __init__(self, user, request):
        self.user = user
        self.request = request
        self.current_site = get_current_site(self.request)

    def plain_message(self):
        return render_to_string('accounts/activate_mail.text', {
                'user': self.user,
                'activation_url': self.activation_url(),
            })

    def html_message(self):
        return render_to_string('accounts/activate_mail.html', {
                'user': self.user,
                'activation_url': self.activation_url(),
            })

    def uid(self):
        return urlsafe_base64_encode(force_bytes(self.user.pk))

    def token(self):
        return default_token_generator.make_token(self.user)

    def scheme(self):
        return self.request.scheme

    def domain(self):
        return self.current_site.domain

    def activation_url(self):
        path = reverse('accounts:activate',
                       kwargs={'uidb64': self.uid(), 'token': self.token()})
        return f"{self.scheme()}://{self.domain()}{path}"

    def send(self):
        send_mail(
            'Activate your Qlapse account.',
            self.plain_message(),
            'hello@qlapse.com',
            [self.user.email],
            html_message=self.html_message()
        )

