from django.urls import path
from . import views

app_name = 'banners'

urlpatterns = [
    path('', views.BookingListView.as_view(), name="index"),
    path('create', views.create, name='create'),
    path('twilio_on_banner_call_webhook', views.twilio_on_banner_call_webhook, name='twilio_on_banner_call_webhook')
]
