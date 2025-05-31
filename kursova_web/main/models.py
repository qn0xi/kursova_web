from django.db import models

# Create your models here.
class Movie(models.Model):
    STATUS_CHOICES = [
        ('now_showing', 'Зараз в кінотеатрах'),
        ('coming_soon', 'Скоро у прокаті'),
    ]

    title = models.CharField('Назва', max_length=100)
    movie = models.TextField('Опис')
    poster = models.ImageField(upload_to='movie_posters/', blank=True, null=True)
    age_rating = models.CharField('Віковий рейтинг', max_length=10, blank=True, null=True)
    format = models.CharField('Формат', max_length=10, blank=True, null=True)
    percentage_category = models.CharField('Категорія %', max_length=10, blank=True, null=True)
    status = models.CharField('Статус', max_length=20, choices=STATUS_CHOICES, default='now_showing')
    genres = models.CharField('Жанри', max_length=255, blank=True, null=True)

    def __str__(self):
        return self.title
    
    

class MovieSchedule(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    date = models.DateField()
    time = models.TimeField()
    hall = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    
    class Meta:
        ordering = ['date', 'time']
    
    def __str__(self):
        return f"{self.movie.title} - {self.date} {self.time}"
