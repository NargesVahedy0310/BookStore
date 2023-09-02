from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User, OTPRequest,sms_breaker_status
# Register your models here.

admin.site.register(OTPRequest)
admin.site.register(sms_breaker_status)

@admin.register(User)
class AppUserAdmin(UserAdmin):
    pass