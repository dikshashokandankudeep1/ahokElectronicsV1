# Generated by Django 3.2.9 on 2022-03-21 12:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('homeapp', '0014_rename_deliverycharge_globlevariables_deliverychargepercentage'),
    ]

    operations = [
        migrations.RenameField(
            model_name='useraddressbook',
            old_name='companyName',
            new_name='locationType',
        ),
    ]
