# Generated by Django 3.2.9 on 2022-03-19 10:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('homeapp', '0012_auto_20220319_1441'),
    ]

    operations = [
        migrations.AddField(
            model_name='globlevariables',
            name='deliveryCharge',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
    ]
