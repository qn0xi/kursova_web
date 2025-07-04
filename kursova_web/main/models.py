from django.db import models

# Create your models here.
class Movie(models.Model):
    STATUS_CHOICES = [
        ('now_showing', 'Зараз в кінотеатрах'),
        ('coming_soon', 'Скоро у прокаті'),
    ]

    title = models.CharField('Назва', max_length=100)
    movie = models.TextField('Опис')
    poster = models.ImageField('Постер', upload_to='movie_posters/', blank=True, null=True)
    age_rating = models.CharField('Віковий рейтинг', max_length=10, blank=True, null=True)
    format = models.CharField('Формат', max_length=10, blank=True, null=True)
    percentage_category = models.CharField('Категорія %', max_length=10, blank=True, null=True)
    duration_minutes = models.IntegerField('Тривалість (хв)', blank=True, null=True)
    status = models.CharField('Статус', max_length=20, choices=STATUS_CHOICES, default='now_showing')
    genres = models.CharField('Жанри', max_length=255, blank=True, null=True)
    actors = models.TextField('У головних ролях', blank=True, null=True)
    publisher = models.CharField('Виробництво', max_length=100, blank=True, null=True)
    trailer_url = models.URLField('Посилання на трейлер (YouTube)', blank=True, null=True)
    display_on_website = models.BooleanField('Відображати на сайті', default=True)

    def __str__(self):
        return self.title
    
    

class MovieSchedule(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    date = models.DateField('Дата', null=True, blank=True)
    time = models.TimeField('Час', null=True, blank=True)
    hall = models.CharField('Зал', max_length=50, null=True, blank=True)
    price = models.DecimalField('Ціна квитків', max_digits=6, decimal_places=2, default=200.00, null=True, blank=True)
    vip_price = models.DecimalField('Ціна VIP квитків', max_digits=6, decimal_places=2, default=350.00, null=True, blank=True)
    
    class Meta:
        ordering = ['date', 'time']
    
    def __str__(self):
        return f"{self.movie.title} - {self.date} {self.time}"

class PurchasedSeat(models.Model):
    session = models.ForeignKey(MovieSchedule, on_delete=models.CASCADE, related_name='purchased_seats')
    row = models.IntegerField()
    seat = models.IntegerField()
    seat_type = models.CharField(max_length=20, default='Звичайне місце')
    price_at_purchase = models.DecimalField('Ціна на момент покупки', max_digits=6, decimal_places=2, null=True, blank=True)
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    purchased_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('session', 'row', 'seat')

    def __str__(self):
        return f"Session {self.session.id}: Row {self.row}, Seat {self.seat} ({self.seat_type})"

    def delete(self, *args, **kwargs):
        movie = self.session.movie
        user = self.user
        super().delete(*args, **kwargs)

        remaining_purchases = PurchasedSeat.objects.filter(user=user, session__movie=movie).count()
        
        if remaining_purchases == 0:
            Rating.objects.filter(user=user, movie=movie).delete()
            print(f"[DEBUG] Deleted rating for movie {movie.title} for user {user.username} as no purchased seats remain.")
        else:
            print(f"[DEBUG] User {user.username} still has {remaining_purchases} purchased seats for movie {movie.title}. Rating not deleted.")

class Rating(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='ratings')
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    rating = models.IntegerField(choices=[(i, str(i)) for i in range(1, 6)])
    rated_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('movie', 'user')

    def __str__(self):
        return f"{self.movie.title} - {self.user.username} - {self.rating}"

class FeedbackMessage(models.Model):
    name = models.CharField('Ім\'я', max_length=100)
    email = models.EmailField('Email')
    subject = models.CharField('Тема', max_length=200)
    message = models.TextField('Повідомлення')
    submitted_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Повідомлення зворотнього зв\'язку'
        verbose_name_plural = 'Повідомлення зворотнього зв\'язку'
        ordering = ['-submitted_at']

    def __str__(self):
        return f"Feedback from {self.name} ({self.email}) - {self.subject}"
