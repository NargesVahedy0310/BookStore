# Generated by Django 4.2.4 on 2023-09-05 06:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user_accounts', '0008_remove_sms_breaker_status_status_service_and_more'),
    ]

    operations = [
        migrations.DeleteModel(
            name='sms_breaker_status',
        ),
    ]
