from django.urls import path
from . import views

urlpatterns = [
    path('auth-log/', views.OTPVerificationView.as_view(), name='otp-verification'),
]
