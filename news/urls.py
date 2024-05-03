from django.urls import path
from . import views

urlpatterns = [
    path('', views.news, name='news'), # Create
    path('add/', views.newsAddView, name='newsAdd'), # Create
    path('list/', views.newsListView, name='newsList'), # Read
    path('edit/<int:pk>', views.newsEditView, name='newsEdit'),  # Update
    path('delete/<int:pk>', views.newsDeletetView, name='newsDelete'),  # Update
]