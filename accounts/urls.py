from django.urls import path
from django.contrib.auth.views import LogoutView
from . import views

app_name = 'accounts'

urlpatterns = [
    path('signup/', views.CustomUserCreate.as_view(), name='signup'),
    path('confirm_activation/', views.ConfirmActivationView.as_view(), name='confirm_activation'),
    path('activate/<uidb64>/<token>/', views.activate, name='activate'),
    path("logout/", LogoutView.as_view(), name="logout")
]
