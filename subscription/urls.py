from django.urls import path
from . import views

urlpatterns = [
    # Admin
    path('', views.subscriptionListView, name='subscriptionList'), # Read
    path('add/', views.subscriptionAddView, name='subscriptionAdd'), # Read
    path('edit/<int:pk>/', views.subscriptionEditView, name='subscriptionEdit'), # Update
    path('delete/<int:pk>/', views.subscriptionDeleteView, name='subscriptionDelete'), # Delete
    # path('', views.membership_plan, name='subscription-plan'),
    path('renewal', views.subscriptionListView, name='membership-renewal'),
    # path('<str:slug>/checkout/', views.prozoneCheckout, name='prozone-checkout'),
    # path('charge/', views.prozoneCharge, name='prozone-charge'),
    # path('success/<str:args>', views.prozoneSuccessMsg, name='prozone-success'),
]