from django.shortcuts import render, get_object_or_404, redirect
from .models import MovieSchedule, Movie, PurchasedSeat
from django.http import JsonResponse
from django.conf import settings
from decimal import Decimal
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate, logout
from .forms import UserRegisterForm, UserLoginForm
from django.contrib import messages
from django.utils import timezone
from django.views.decorators.http import require_POST
from django.core.mail import EmailMessage
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.models import User
from django.db.models import Count, Sum
import json
import qrcode
import io
import base64
from email.mime.image import MIMEImage

def index(request):
    now_showing_movies = Movie.objects.filter(status='now_showing', display_on_website=True)[:5]
    coming_soon_movies = Movie.objects.filter(status='coming_soon', display_on_website=True)
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

    purchased_seats_coords = set((ps.row, ps.seat) for ps in PurchasedSeat.objects.filter(session=session))

    hall_rows = 5  # Example: 5 rows
    seats_per_row = 10 # Example: 10 seats per row
    vip_row_index = 4 # 0-indexed, so row 5 is index 4

    hall_seats_data = []
    for r in range(1, hall_rows + 1):
        row_seats = []
        for s in range(1, seats_per_row + 1):
            is_vip = (r - 1) == vip_row_index # Check if current row is the VIP row
            is_taken = (r, s) in purchased_seats_coords
            seat_info = {
                'row': r,
                'seat_num': s,
                'is_vip': is_vip,
                'is_taken': is_taken,
                'price': str(vip_price if is_vip else regular_price) # Pass prices as strings
            }
            row_seats.append(seat_info)
        hall_seats_data.append(row_seats)

    context = {
        'session': session,
        'movie': movie,
        'regular_price': regular_price,
        'vip_price': vip_price,
        'hall_seats_data': hall_seats_data, # Pass pre-processed seat data
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
        schedules = MovieSchedule.objects.filter(date=selected_date_str, movie__display_on_website=True).select_related('movie')
        data = []
        for schedule_item in schedules:
            data.append({
                'movie_title': schedule_item.movie.title,
                'time': schedule_item.time.strftime('%H:%M'),
                'hall': schedule_item.hall,
                'price': str(schedule_item.price),
                'poster_url': schedule_item.movie.poster.url if schedule_item.movie.poster else settings.STATIC_URL + 'main/images/default_poster.jpg',
                'age_rating': f"{schedule_item.movie.age_rating}+" if schedule_item.movie.age_rating else None,
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
            messages.success(request, f'Новий обліковий запис створено: {user.username}')
            return redirect('/')
        else:
            # Removed global error messages as they are now displayed per field in the template
            pass # No explicit action needed here as errors are handled by form rendering
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
                messages.info(request, f"Ви увійшли як {username}")
                return redirect('/')
            else:
                messages.error(request, "Невірне ім'я користувача або пароль.")
        else:
            messages.error(request, "Невірне ім'я користувача або пароль.")
    form = UserLoginForm()
    return render(request, 'registration/login.html', {'form': form})

def user_logout(request):
    logout(request)
    messages.info(request, "Ви успішно вийшли з акаунту")
    return redirect('/')

def movie_gallery(request):
    movies = Movie.objects.filter(display_on_website=True)
    return render(request, 'main/movie_gallery.html', {'movies': movies})

def movie_details(request, movie_id):
    movie = get_object_or_404(Movie, pk=movie_id, display_on_website=True)
    
    # Fetch all future sessions for the movie, ordered by date and time
    sessions = MovieSchedule.objects.filter(movie=movie, date__gte=timezone.now().date()).order_by('date', 'time')
    session_data = []
    for session in sessions:
        session_data.append({
            'id': session.id,
            'date': session.date.strftime('%Y-%m-%d'),
            'time': session.time.strftime('%H:%M'),
            'hall': session.hall,
            'price': str(session.price),
            'vip_price': str(session.vip_price),
        })

    data = {
        'title': movie.title,
        'movie': movie.movie, # Description field is named 'movie' in the model
        'poster': movie.poster.url if movie.poster else settings.STATIC_URL + 'images/no_poster.jpg',
        'age_rating': f"{movie.age_rating}+" if movie.age_rating else None,
        'format': movie.format,
        'duration_minutes': movie.duration_minutes,
        'genres': movie.genres,
        'actors': movie.actors,
        'publisher': movie.publisher,
        'trailer_url': movie.trailer_url,
        'status_display': movie.get_status_display(),
        'sessions': session_data, # Add session data here
    }
    return JsonResponse(data)

@require_POST
@login_required
def purchase_tickets(request, session_id):
    user = request.user
    session = get_object_or_404(MovieSchedule, pk=session_id)
    try:
        data = json.loads(request.body)
        seats_data = data.get('seats', [])
        if not seats_data:
            return JsonResponse({'error': 'No seats selected.'}, status=400)

        # Remove debugging: Print raw seats_data
        # print(f"Raw seats_data from frontend: {seats_data}")
        # print(f"Type of seats_data: {type(seats_data)}")

        qr_codes_html = ""

        msg = EmailMessage(
            subject="Дякуємо за покупку квитків!",
            body="", # Will be set as html_content later
            from_email=None, # Use DEFAULT_FROM_EMAIL from settings
            to=[user.email]
        )
        msg.content_subtype = "html"

        for i, seat_info in enumerate(seats_data):
            # Remove debugging prints
            # print(f"Processing seat_info ({i}): {seat_info}")
            # print(f"Type of seat_info ({i}): {type(seat_info)}")
            
            # Simplified extraction, assuming seat_info is always a dict from frontend
            row = int(seat_info['row'])
            seat_num_from_frontend = int(seat_info['seat']) # Use seat from frontend
            seat_type = seat_info.get('type', 'Звичайне місце')

            if PurchasedSeat.objects.filter(session=session, row=row, seat=seat_num_from_frontend).exists():
                return JsonResponse({'error': f'Місце Ряд {row}, Місце {seat_num_from_frontend} вже зайняте.'}, status=400)

            # Create PurchasedSeat instance
            purchased_seat = PurchasedSeat.objects.create(
                session=session,
                row=row,
                seat=seat_num_from_frontend, # Use seat from frontend
                seat_type=seat_type,
                user=user
            )

            # Prepare data for QR code
            qr_data = f"SessionID:{session.id}|Movie:{session.movie.title}|Date:{session.date}|Time:{session.time}|Hall:{session.hall}|Row:{row}|Seat:{seat_num_from_frontend}|Type:{seat_type}|PurchaseID:{purchased_seat.id}"

            # Generate QR code
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=10,
                border=4,
            )
            qr.add_data(qr_data)
            qr.make(fit=True)

            img = qr.make_image(fill_color="black", back_color="white")
            
            # Save QR code to a BytesIO object
            buffer = io.BytesIO()
            img.save(buffer, format="PNG")
            buffer.seek(0) # Rewind to the beginning of the buffer

            # Create unique Content-ID for each image
            image_cid = f'qr_code_{purchased_seat.id}'
            
            # Attach the QR code image as an inline attachment
            qr_image = MIMEImage(buffer.getvalue())
            qr_image.add_header('Content-ID', f'<{image_cid}>')
            msg.attach(qr_image)

            qr_codes_html += f"""
                <p><strong>Ряд:</strong> {row}, <strong>Місце:</strong> {seat_num_from_frontend}, <strong>Тип:</strong> {seat_type}</p>
                <img src="cid:{image_cid}" alt="QR Code for Seat {row}-{seat_num_from_frontend}" style="width:150px;height:150px;"><br/><br/>
            """
        
        html_content = f"""
            <html>
            <body>
                <p>Привіт, {user.username}!</p>
                <p>Дякуємо за покупку квитків у кінотеатрі "Галактика".</p>
                <p>Ваші квитки на фільм <strong>"{session.movie.title}"</strong> ({session.date.strftime('%d.%m.%Y')} о {session.time.strftime('%H:%M')}, Зал №{session.hall}):</p>
                {qr_codes_html}
                <p>Будь ласка, покажіть ці QR-коди при вході на сеанс.</p>
                <p>З повагою,<br/>Команда кінотеатру "Галактика"</p>
            </body>
            </html>
        """
        
        # Plain text alternative for email clients that don't display HTML
        text_content = f"""Дякуємо за покупку, {user.username}!
Ваші місця:
{' '.join([f'Ряд {info["row"]}, Місце {info["seat"]}, {info["type"]}' for info in seats_data])}

Будь ласка, покажіть QR-коди (у HTML-версії листа) при вході на сеанс."""

        msg.body = html_content
        msg.send()

        return JsonResponse({'success': True})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@staff_member_required
def admin_statistics(request):
    # Filter schedules and purchased seats to only include current/future dates
    today = timezone.now().date()

    total_movies = Movie.objects.count()
    total_schedules = MovieSchedule.objects.filter(date__gte=today).count()
    total_purchased_seats = PurchasedSeat.objects.filter(session__date__gte=today).count()

    # Calculate Total Revenue Generated from purchased tickets for current/future sessions
    total_revenue_obj = PurchasedSeat.objects.filter(session__date__gte=today).aggregate(total_sum=Sum('session__price'))
    total_revenue = total_revenue_obj['total_sum'] if total_revenue_obj['total_sum'] is not None else Decimal('0.00')

    # More complex stats could involve aggregations, e.g., most popular movie
    # Example: Most popular movie based on purchased seats for future sessions
    popular_movie = Movie.objects.filter(
        movieschedule__date__gte=today,
        status='now_showing', # Filter for movies currently showing
        display_on_website=True # Ensure it's displayed on the website
    ).annotate(
        num_purchased_seats=Count('movieschedule__purchased_seats')
    ).order_by('-num_purchased_seats').first()

    total_registered_users = User.objects.filter(is_staff=False).count()

    context = {
        'total_movies': total_movies,
        'total_schedules': total_schedules,
        'total_purchased_seats': total_purchased_seats,
        'total_revenue': total_revenue,
        'popular_movie': popular_movie,
        'total_registered_users': total_registered_users,
    }
    return render(request, 'main/admin_statistics.html', context)
