# Generated by Django 5.2.1 on 2025-05-29 17:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_movie_poster'),
    ]

    operations = [
        migrations.AddField(
            model_name='movie',
            name='age_rating',
            field=models.CharField(blank=True, max_length=10, null=True, verbose_name='Віковий рейтинг'),
        ),
        migrations.AddField(
            model_name='movie',
            name='format',
            field=models.CharField(blank=True, max_length=10, null=True, verbose_name='Формат'),
        ),
        migrations.AddField(
            model_name='movie',
            name='percentage_category',
            field=models.CharField(blank=True, max_length=10, null=True, verbose_name='Категорія %'),
        ),
    ]
