# Generated by Django 3.2.9 on 2022-02-12 19:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('homeapp', '0002_productstableprimary_isactive'),
    ]

    operations = [
        migrations.RenameField(
            model_name='productstableprimary',
            old_name='subCategory',
            new_name='searchTitle',
        ),
        migrations.AddField(
            model_name='productstableprimary',
            name='subCategory1',
            field=models.CharField(blank=True, default='', max_length=50),
        ),
        migrations.AddField(
            model_name='productstableprimary',
            name='subCategory2',
            field=models.CharField(blank=True, default='', max_length=50),
        ),
    ]
