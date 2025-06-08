from django.shortcuts import render, get_object_or_404, redirect
from .models import MovieSchedule, Movie
from django.http import JsonResponse
from django.conf import settings
from decimal import Decimal
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate, logout
from .forms import UserRegisterForm, UserLoginForm
from django.contrib import messages

def index(request):
    now_showing_movies = Movie.objects.filter(status='now_showing')
    coming_soon_movies = Movie.objects.filter(status='coming_soon')
    context = {
        'now_showing_movies': now_showing_movies,
        'coming_soon_movies': coming_soon_movies,
    }
    return render(request, 'main/index.html', context)

def contacts(request):
    return render(request, 'main/contacts.html')

def feedback(request):
    return render(request, 'main/feedback.html')

def prices(request):
    return render(request, 'main/prices.html')

def about_us(request):
    return render(request, 'main/about.html')

@login_required
def select_seats(request, session_id):
    session = get_object_or_404(MovieSchedule, pk=session_id)
    movie = session.movie
    
    regular_price = session.price if session.price is not None else Decimal('200.00')
    vip_price = session.vip_price if session.vip_price is not None else regular_price * Decimal('1.5')

    context = {
        'session': session,
        'movie': movie,
        'regular_price': regular_price,
        'vip_price': vip_price,
    }
    return render(request, 'main/seat_selection.html', context)

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

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f'New account created: {user.username}')
            return redirect('/')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"Error in {field}: {error}")
    else:
        form = UserRegisterForm()
    return render(request, 'registration/register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        form = UserLoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"You are now logged in as {username}")
                return redirect('/')
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    form = UserLoginForm()
    return render(request, 'registration/login.html', {'form': form})

def user_logout(request):
    logout(request)
    messages.info(request, "You have successfully logged out.")
    return redirect('/')
