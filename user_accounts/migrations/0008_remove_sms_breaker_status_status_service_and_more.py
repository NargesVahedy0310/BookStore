# Generated by Django 4.2.4 on 2023-09-02 18:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_accounts', '0007_sms_breaker_status'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='sms_breaker_status',
            name='status_service',
        ),
        migrations.AddField(
            model_name='sms_breaker_status',
            name='title_service',
            field=models.CharField(choices=[('Kavenegar', 'Kavenegar'), ('Signal', 'Signal')], default='Kavenegar', max_length=25),
        ),
    ]