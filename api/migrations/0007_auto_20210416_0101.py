# Generated by Django 3.1.5 on 2021-04-15 22:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0006_auto_20210416_0021'),
    ]

    operations = [
        migrations.AlterField(
            model_name='client',
            name='birthdate',
            field=models.DateField(blank=True, null=True, verbose_name='Дата рождения'),
        ),
    ]