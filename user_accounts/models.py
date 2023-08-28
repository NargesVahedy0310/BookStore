import random
import string
import uuid
from datetime import timedelta
from django.utils.translation import gettext as _
from django.db import models
from django.utils import timezone
from .sender import SMSBreaker
from django.contrib.auth.models import AbstractUser, Group, Permission, User
from rest_framework.authtoken.models import Token

class User(AbstractUser):
    groups = models.ManyToManyField(Group, related_name='user_accounts_users', blank=True, verbose_name=_('groups'))
    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name=_('user permissions'),
        blank=True,
        related_name='user_accounts_users',
        help_text=_('Specific permissions for this user.'),
    )

class OtpRequestQuerySet(models.QuerySet):
    def is_valid(self, receiver, request, password, first_name, last_name, pass_one, pass_two):
        current_time = timezone.now()
        return self.filter(
            receiver=receiver,
            request_id=request,
            password=password,
            first_name=first_name,
            last_name=last_name,
            pass_one=pass_one,
            pass_two=pass_two,
            created__lt=current_time,
            created__gt=current_time-timedelta(seconds=120),

        ).exists()

class OTPManager(models.Manager):

    def get_queryset(self):
        return OtpRequestQuerySet(self.model, self._db)

    def is_valid(self, receiver, request, password, first_name, last_name, pass_one, pass_two):
        return self.get_queryset().is_valid(receiver, request, password, first_name, last_name, pass_one, pass_two)

    
    
    def generate(self, data):
        otp = self.model(channel=data['channel'], receiver=data['receiver'],
                        first_name=data['first_name'], last_name=data['last_name'],
                        pass_one=data['pass_one'], pass_two=data['pass_two'])
        otp.save(using=self._db)
        sms_breaker = SMSBreaker()
    
        try:
            sms_breaker.send_sms(otp)
        except Exception as e:
            print(f"Failed to send SMS: {e}")
    
        return otp
    @property
    def sms_breaker(self):
        return SMSBreaker()



def generate_otp():
    rand = random.SystemRandom()
    digits = rand.choices(string.digits, k=4)
    return ''.join(digits)


class OTPRequest(models.Model):
    class OtpChannel(models.TextChoices):
        PHONE = 'Phone'

    request_id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    channel = models.CharField(max_length=10, choices=OtpChannel.choices, default=OtpChannel.PHONE)
    receiver = models.CharField(max_length=50)
    password = models.CharField(max_length=4, default=generate_otp)
    token = models.OneToOneField(Token, on_delete=models.CASCADE, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True, editable=False)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    pass_one = models.CharField(max_length=15)
    pass_two = models.CharField(max_length=15)

    objects = OTPManager()
    

# class Accounnt(models.Model):
#     class Membership_type(models.TextChoices):
#         SPECIAL = 'ویژه'
#         SIMPLE = 'ساده'
#     class Number_day(models.IntegerField):
#         SPECIAL = 31
#         DEFAULT = 0
#
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     membership_type = models.CharField(max_length=10, choices=Membership_type.choices, default=Membership_type.SINCER)
#     number_day = models.IntegerField(default=0)
#     date_time = models.DateTimeField()
#     Membership_validity_date = models.DateField()
#
#     @property
#     def username(self):
#         return self.user.username
#
#     @property
#     def first_name(self):
#         return self.user.first_name
#
#     @property
#     def last_name(self):
#         return self.user.last_name
