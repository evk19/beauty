# Generated by Django 3.1.5 on 2021-04-14 09:20

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_auto_20210112_1921'),
    ]

    operations = [
        migrations.AlterField(
            model_name='car',
            name='licensePlate',
            field=models.CharField(max_length=9, validators=[django.core.validators.RegexValidator('^[АВЕКМНОРСТУХ]\\d{3}(?<!000)[АВЕКМНОРСТУХ]{2}\\d{2,3}$', 'Пример номера: А123ВЕ456')], verbose_name='Номер авто'),
        ),
        migrations.AlterField(
            model_name='discount',
            name='promoCode',
            field=models.CharField(max_length=6, unique=True, validators=[django.core.validators.RegexValidator('^[A-Z0-9]*$', 'Можно использовать буквы A-Z и цифры 0-9')], verbose_name='Промокод'),
        ),
        migrations.AlterField(
            model_name='driver',
            name='driverLicense',
            field=models.CharField(max_length=100, unique=True, validators=[django.core.validators.RegexValidator('^[A-Z](?:\\d[- ]*){14}$', 'Пример водительских прав: D6101-40706-60905')], verbose_name='Водительские права'),
        ),
        migrations.AlterField(
            model_name='order',
            name='destinationHouse',
            field=models.IntegerField(default=1, validators=[django.core.validators.MinValueValidator(1)], verbose_name='Дом'),
        ),
        migrations.AlterField(
            model_name='order',
            name='entrance',
            field=models.IntegerField(default=1, validators=[django.core.validators.MinValueValidator(1)], verbose_name='Подъезд'),
        ),
        migrations.AlterField(
            model_name='order',
            name='house',
            field=models.IntegerField(default=1, validators=[django.core.validators.MinValueValidator(1)], verbose_name='Дом'),
        ),
    ]
