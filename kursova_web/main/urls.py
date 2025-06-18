from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.index, name='home'),
    path('contacts/', views.contacts, name='contacts'),
    path('feedback/', views.feedback, name='feedback'),
    path('prices/', views.prices, name='prices'),
    path('about-us/', views.about_us, name='about_us'),
    path('schedule/', views.schedule, name='schedule'),
    path('schedule/<int:session_id>/select_seats/', views.select_seats, name='select_seats'),
    path('schedule/by-date/', views.get_schedule_by_date, name='get_schedule_by_date'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('movies/', views.movie_gallery, name='movie_gallery'),
    path('movies/details/<int:movie_id>/', views.movie_details, name='movie_details'),
    path('schedule/<int:session_id>/purchase/', views.purchase_tickets, name='purchase_tickets'),
    path('admin_statistics/', views.admin_statistics, name='admin_statistics'),
    path('purchase_history/', views.purchase_history, name='purchase_history'),
    path('submit_rating/', views.submit_rating, name='submit_rating'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)