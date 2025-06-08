from django.contrib import admin
from .models import Movie, MovieSchedule

class MovieScheduleInline(admin.TabularInline):
    model = MovieSchedule
    extra = 1  # Allows adding one extra schedule form by default
    fields = ['date', 'time', 'hall', 'price', 'vip_price']

class MovieAdmin(admin.ModelAdmin):
    list_display = ('title', 'status', 'genres', 'age_rating', 'format', 'percentage_category', 'duration_minutes')
    fields = ('title', 'movie', 'genres', 'poster', 'age_rating', 'format', 'percentage_category', 'duration_minutes', 'status', 'actors', 'publisher', 'trailer_url')
    inlines = [MovieScheduleInline]

admin.site.register(Movie, MovieAdmin)