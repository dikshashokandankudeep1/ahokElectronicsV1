# Generated by Django 3.2.9 on 2022-03-17 22:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('homeapp', '0006_auto_20220318_0233'),
    ]

    operations = [
        migrations.AddField(
            model_name='userpaymenttable',
            name='bankName',
            field=models.CharField(blank=True, default='', max_length=50),
        ),
        migrations.AddField(
            model_name='userpaymenttable',
            name='cardIssuer',
            field=models.CharField(blank=True, default='', max_length=50),
        ),
        migrations.AddField(
            model_name='userpaymenttable',
            name='cardType',
            field=models.CharField(blank=True, default='', max_length=50),
        ),
        migrations.AddField(
            model_name='userpaymenttable',
            name='cvv',
            field=models.CharField(blank=True, default='', max_length=50),
        ),
    ]
