from django.urls import path
from . import views

app_name = 'stripe_payments'

urlpatterns = [
    path('config/', views.config),
    path('create-checkout-session/', views.create_checkout_session),
]
