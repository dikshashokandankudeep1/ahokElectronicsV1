# Generated by Django 3.2.9 on 2022-04-01 14:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('homeapp', '0019_rename_streetaddress1_useraddressbook_address'),
    ]

    operations = [
        migrations.AddField(
            model_name='usertable',
            name='gender',
            field=models.CharField(blank=True, default='', max_length=50),
        ),
    ]