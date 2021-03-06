# Generated by Django 3.2.9 on 2022-03-17 21:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('homeapp', '0005_temporaryorderstoretable'),
    ]

    operations = [
        migrations.CreateModel(
            name='userPaymentTable',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('userId', models.CharField(blank=True, default='', max_length=50)),
                ('cardNumber', models.CharField(blank=True, default='', max_length=50)),
                ('cardHolderName', models.CharField(blank=True, default='', max_length=50)),
                ('expiryDate', models.CharField(blank=True, default='', max_length=50)),
            ],
        ),
        migrations.AddField(
            model_name='usertable',
            name='accountList',
            field=models.CharField(blank=True, default='', max_length=500),
        ),
    ]
