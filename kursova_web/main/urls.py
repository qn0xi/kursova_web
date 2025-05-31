from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('schedule/', views.schedule, name='schedule'),
    path('schedule/by-date/', views.get_schedule_by_date, name='get_schedule_by_date'),
]