# Generated by Django 3.2.9 on 2022-03-19 09:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('homeapp', '0011_auto_20220319_0507'),
    ]

    operations = [
        migrations.AddField(
            model_name='temporaryorderstoretable',
            name='orderTotal',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
        migrations.AddField(
            model_name='temporaryorderstoretable',
            name='restAmount',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
        migrations.AddField(
            model_name='temporaryorderstoretable',
            name='tokenAmount',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
    ]
