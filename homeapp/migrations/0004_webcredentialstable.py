# Generated by Django 3.2.9 on 2022-02-14 18:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('homeapp', '0003_auto_20220213_0118'),
    ]

    operations = [
        migrations.CreateModel(
            name='webCredentialsTable',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('credentialType', models.CharField(blank=True, default='', max_length=50)),
                ('websiteUrl', models.CharField(blank=True, default='', max_length=50)),
                ('senderEmail', models.CharField(blank=True, default='', max_length=50)),
                ('password', models.CharField(blank=True, default='', max_length=50)),
            ],
        ),
    ]
