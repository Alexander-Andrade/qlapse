from django.urls import path
from . import views

app_name = 'banners'

urlpatterns = [
    path('create', views.BannerCreateView.as_view(), name='create'),
]
