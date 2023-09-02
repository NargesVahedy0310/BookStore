from django.urls import path, include
from . import views

urlpatterns = [
    path('auth-log/', views.OTPVerificationView.as_view(), name='otp-verification'),
    path('profile/', views.UserProfileView.as_view(), name='user-profile'),
    
]



