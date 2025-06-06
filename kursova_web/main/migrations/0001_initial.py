# Generated by Django 5.2.1 on 2025-05-24 19:40

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Movie',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, verbose_name='Назва')),
                ('movie', models.TextField(verbose_name='Опис')),
            ],
        ),
        migrations.CreateModel(
            name='MovieSchedule',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('time', models.TimeField()),
                ('hall', models.CharField(max_length=50)),
                ('price', models.DecimalField(decimal_places=2, max_digits=6)),
                ('movie', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.movie')),
            ],
            options={
                'ordering': ['date', 'time'],
            },
        ),
    ]
