# Generated by Django 3.1 on 2020-08-10 21:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accountprofile', '0003_auto_20200810_2159'),
    ]

    operations = [
        migrations.AlterField(
            model_name='package',
            name='price',
            field=models.IntegerField(),
        ),
    ]
