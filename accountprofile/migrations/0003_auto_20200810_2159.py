# Generated by Django 3.1 on 2020-08-10 20:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accountprofile', '0002_auto_20200809_1729'),
    ]

    operations = [
        migrations.AlterField(
            model_name='package',
            name='price',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=12),
        ),
    ]
