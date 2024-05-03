from django.urls import path
from . import views
from .views import AddEventView, ListEventView, EditEventView, DeleteEventView, FinderEventView

urlpatterns = [
    path('', ListEventView.as_view(), name='list-event'),
    path('add/', AddEventView.as_view(), name='add-event'),
    path('<int:pk>/edit', EditEventView.as_view(), name='edit-event'),
    path('<int:pk>/delete', DeleteEventView.as_view(), name='delete-event'),
    path('find-events-worldwide/', views.FinderEventView, name='find-event'),
    path('<int:id>/', views.EventDetailsView, name='event-detail'),
    path('ajax/load-countries/', views.load_countries, name='load_countries_category'),
    path('load_state/category/', views.load_state, name='load_state_category'),
    path('load_city/category/', views.load_cites, name='load_city_category'),

    path('add/', views.EventDetailsView, name='eventAdd'), # Create
    path('list/', views.EventDetailsView, name='eventList'), # Read
    path('edit/<int:pk>', views.EventDetailsView, name='eventEdit'),  # Update
    path('delete/<int:pk>', views.EventDetailsView, name='eventDelete'),  # Update
]
