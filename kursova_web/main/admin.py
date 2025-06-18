from django.contrib import admin
from .models import Movie, MovieSchedule, PurchasedSeat, FeedbackMessage

class MovieScheduleInline(admin.TabularInline):
    model = MovieSchedule
    extra = 1
    fields = ['date', 'time', 'hall', 'price', 'vip_price']

class MovieAdmin(admin.ModelAdmin):
    list_display = ('title', 'status', 'genres', 'age_rating', 'format', 'percentage_category', 'duration_minutes', 'display_on_website')
    fields = ('title', 'movie', 'genres', 'poster', 'age_rating', 'format', 'percentage_category', 'duration_minutes', 'status', 'actors', 'publisher', 'trailer_url', 'display_on_website')
    inlines = [MovieScheduleInline]

admin.site.register(Movie, MovieAdmin)
admin.site.register(PurchasedSeat)
admin.site.register(FeedbackMessage)