# Generated by Django 3.2.9 on 2022-03-30 13:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('homeapp', '0018_rename_streetaddress2_useraddressbook_landmark'),
    ]

    operations = [
        migrations.RenameField(
            model_name='useraddressbook',
            old_name='streetAddress1',
            new_name='address',
        ),
    ]