from django.urls import path
from django.shortcuts import redirect
from . import views

urlpatterns = [
    path('', lambda request: redirect('dashboard', permanent=True)),  # /profile -> redirects to Dashboard
    path('webSettings/', views.webSettingsView, name='webSettings'),
    path('mailServer/', views.mailServerView, name='mailServer'),
    path('stripeGateway/', views.stripeGatewayView, name='stripeGatewayView'),
    path('razorPayGateway/', views.razorPayGatewayView, name='razorPayGatewayView'),
    path('messagingAPI/', views.messagingAPIView, name='messagingAPI'),

    # Changelog
    path('changlog/', views.changeLogView, name='changeLogView'),

    # Country
    path('countryList/', views.countryView, name='countryList'), # Read
    path('countryAdd/', views.countryAddView, name='countryAdd'), # Create
    path('countryUpdate/<int:pk>', views.countryUpdateView, name='countryUpdate'), # Update

    # State
    path('stateList/', views.stateListView, name='stateList'), # Read
    path('stateAdd/', views.stateAddView, name='stateAdd'), # Create
    path('stateUpdate/<int:pk>', views.stateUpdateView, name='stateUpdate'), # Update

    # City
    path('cityList/', views.cityListView, name='cityList'), # Read
    path('cityAdd/', views.cityAddView, name='cityAdd'), # Create
    path('cityUpdate/<int:pk>', views.cityUpdateView, name='cityUpdate'), # Update

    # Membership
    path('membership/', views.membershipListView, name='membershipList'), # Read
    path('membership/add/', views.membershipAddView, name='membershipAdd'), # Create
    path('membership/edit/<int:pk>', views.membershipUpdateView, name='membershipUpdate'), # Update
    path('membership/delete/<int:pk>', views.membershipDeleteView, name='membershipDelete'), # Delete

    # Dropdown List
    path('add_service/', views.add_service, name='add_service'),
]