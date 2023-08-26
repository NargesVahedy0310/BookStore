from django.urls import path
from . import views

urlpatterns = [
    path('verify-otp/', views.OTPVerificationView.as_view(), name='otp-verification'),
]
