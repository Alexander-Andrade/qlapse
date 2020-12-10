from django.urls import path
from django.contrib.auth.views import LogoutView
from . import views

app_name = 'accounts'

urlpatterns = [
    path('signup/', views.CustomUserCreate.as_view(), name='signup'),
    path("logout/", LogoutView.as_view(), name="logout")
]
