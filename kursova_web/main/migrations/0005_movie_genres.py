# Generated by Django 5.2.1 on 2025-05-29 17:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_movie_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='movie',
            name='genres',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Жанри'),
        ),
    ]
