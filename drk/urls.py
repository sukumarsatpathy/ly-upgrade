from django.urls import path
from .import views

urlpatterns = [
    path('upcoming-events/', views.upcomingEvents, name='upcomingEvents'),
]

