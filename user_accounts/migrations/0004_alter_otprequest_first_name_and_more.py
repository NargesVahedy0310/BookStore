# Generated by Django 4.2.4 on 2023-08-27 08:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_accounts', '0003_otprequest_first_name_otprequest_last_name_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='otprequest',
            name='first_name',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='otprequest',
            name='last_name',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='otprequest',
            name='pass_one',
            field=models.CharField(max_length=15),
        ),
        migrations.AlterField(
            model_name='otprequest',
            name='pass_two',
            field=models.CharField(max_length=15),
        ),
    ]
