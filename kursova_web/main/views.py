from django.shortcuts import render
from .models import MovieSchedule, Movie
from django.http import JsonResponse
from django.conf import settings

def index(request):
    now_showing_movies = Movie.objects.filter(status='now_showing')
    coming_soon_movies = Movie.objects.filter(status='coming_soon')
    context = {
        'now_showing_movies': now_showing_movies,
        'coming_soon_movies': coming_soon_movies,
    }
    return render(request, 'main/index.html', context)

def schedule(request):
    # Initial view for the schedule page, maybe fetch today's schedule
    # For now, just render the template
    return render(request, 'main/schedule.html')

def get_schedule_by_date(request):
    selected_date_str = request.GET.get('date')
    if not selected_date_str:
        return JsonResponse({'error': 'Date parameter is missing'}, status=400)

    try:
        # Assuming date is in YYYY-MM-DD format
        schedules = MovieSchedule.objects.filter(date=selected_date_str).select_related('movie')
        data = []
        for schedule_item in schedules:
            data.append({
                'movie_title': schedule_item.movie.title,
                'time': schedule_item.time.strftime('%H:%M'),
                'hall': schedule_item.hall,
                'price': str(schedule_item.price),
                'poster_url': schedule_item.movie.poster.url if schedule_item.movie.poster else settings.STATIC_URL + 'main/images/default_poster.jpg',
                'age_rating': schedule_item.movie.age_rating,
                'format': schedule_item.movie.format,
                'percentage_category': schedule_item.movie.percentage_category,
                'id': schedule_item.id
            })
        return JsonResponse({'schedules': data})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
