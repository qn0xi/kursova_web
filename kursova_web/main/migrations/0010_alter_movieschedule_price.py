# Generated by Django 5.2.1 on 2025-06-03 22:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0009_movieschedule_vip_price'),
    ]

    operations = [
        migrations.AlterField(
            model_name='movieschedule',
            name='price',
            field=models.DecimalField(decimal_places=2, default=200.0, max_digits=6),
        ),
    ]
