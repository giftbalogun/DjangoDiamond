# Generated by Django 3.1 on 2023-02-01 17:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('diamond', '0021_auto_20200818_1454'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='referral_code',
            field=models.CharField(default='ZSRGZ', max_length=6),
        ),
    ]
