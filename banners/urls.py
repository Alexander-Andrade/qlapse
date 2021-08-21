from django.urls import path, re_path
from . import views

app_name = 'banners'

urlpatterns = [
    path('', views.BannersListView.as_view(), name="index"),
    path('create', views.create, name='create'),
    path('twilio_on_banner_call_webhook', views.twilio_on_banner_call_webhook, name='twilio_on_banner_call_webhook'),
    path('<int:banner_id>/queue', views.queue, name='queue'),
    path('<int:banner_id>/queue/next', views.next_queue_item, name='next_queue_item'),
    path('<int:banner_id>/queue/skip', views.skip_queue_item, name='skip_queue_item'),
    path('telegram_queue_webhook', views.TelegramQueueWebhookView.as_view(), name='telegram_queue_webhook'),
    path('<int:banner_id>/queue_entrypoint', views.queue_entrypoint, name='queue_entrypoint')
]
