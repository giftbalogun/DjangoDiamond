# Generated by Django 3.0.5 on 2020-08-13 02:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('diamond', '0014_auto_20200813_0849'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='referral_code',
            field=models.CharField(default='LEGEU', max_length=6),
        ),
    ]
