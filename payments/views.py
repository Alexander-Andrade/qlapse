from django.shortcuts import render
from django.views.generic.base import TemplateView


class AddPaymentMethodView(TemplateView):
    template_name = 'payments/add_payment_method.html'
