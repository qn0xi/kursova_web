from django.urls import path
from . import views

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
]