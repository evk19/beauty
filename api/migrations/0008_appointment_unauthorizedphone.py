# Generated by Django 3.1.5 on 2021-04-15 22:34

from django.db import migrations
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0007_auto_20210416_0101'),
    ]

    operations = [
        migrations.AddField(
            model_name='appointment',
            name='unauthorizedPhone',
            field=phonenumber_field.modelfields.PhoneNumberField(blank=True, max_length=128, null=True, region=None, unique=True, verbose_name='Телефон неавторизованного клиента'),
        ),
    ]
