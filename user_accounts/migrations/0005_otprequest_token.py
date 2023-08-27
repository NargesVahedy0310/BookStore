# Generated by Django 4.2.4 on 2023-08-27 23:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('authtoken', '0003_tokenproxy'),
        ('user_accounts', '0004_alter_otprequest_first_name_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='otprequest',
            name='token',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='authtoken.token'),
        ),
    ]