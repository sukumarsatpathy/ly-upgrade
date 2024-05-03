from django.urls import path
from . import views
from .views import AddClubView, EditClubView, DeleteClubView, ListClubView, FinderClubView

urlpatterns = [
    path('list/', ListClubView.as_view(), name='list-club'),
    path('add/', AddClubView.as_view(), name='add-club'),
    path('<int:pk>/edit', EditClubView.as_view(), name='edit-club'),
    path('<int:pk>/delete', DeleteClubView.as_view(), name='delete-club'),
    path('find-clubs-worldwide/', views.FinderClubView, name='find-club'),
    path('<int:pk>/', views.ClubDetailsView, name='club-detail'),
    path('ajax/load-countries/club', views.load_countries, name='load_countries_category_club'),
    path('load_state/category/club', views.load_state, name='load_state_category_club'),
    path('load_city/category/club', views.load_cites, name='load_city_category_club'),

    path('add/', views.ClubDetailsView, name='clubAdd'), # Create
    path('list/', views.ClubDetailsView, name='clubList'), # Read
    path('edit/<int:pk>', views.ClubDetailsView, name='clubEdit'),  # Update
    path('delete/<int:pk>', views.ClubDetailsView, name='clubDelete'),  # Update
]
