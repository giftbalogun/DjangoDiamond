# Generated by Django 3.1 on 2020-08-18 13:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('diamond', '0018_auto_20200813_1956'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='referree',
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='referral_code',
            field=models.CharField(default='WNVQT', max_length=6),
        ),
    ]
