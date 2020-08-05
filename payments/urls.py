from django.urls import path
from . import views

app_name = 'payments'

urlpatterns = [
    path('add_payment_method/', views.AddPaymentMethodView.as_view(), name='add_payment_method')
]
