import random
import string
import uuid
from datetime import timedelta
from django.utils.translation import gettext as _
from django.db import models
from django.utils import timezone
from .sender import send_otp
from django.contrib.auth.models import AbstractUser, Group, Permission

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
    def is_valid(self, receiver, request, password):
        current_time = timezone.now()
        return self.filter(
            receiver=receiver,
            request_id=request,
            password=password,
            created__lt=current_time,
            created__gt=current_time-timedelta(seconds=120),

        ).exists()

class OTPManager(models.Manager):

    def get_queryset(self):
        return OtpRequestQuerySet(self.model, self._db)

    def is_valid(self, receiver, request, password):
        return self.get_queryset().is_valid(receiver, request, password)


    def generate(self, data):
        otp = self.model(channel=data['channel'], receiver=data['receiver'])
        otp.save(using=self._db)
        send_otp(otp)
        return otp



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
    created = models.DateTimeField(auto_now_add=True, editable=False)

    objects = OTPManager()