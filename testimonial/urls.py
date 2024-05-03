from django.urls import path
from . import views

urlpatterns = [
    path('', views.testimonial, name='testimonial'), # Front
    path('add/', views.testimonialAddView, name='testimonialAdd'), # Create
    path('list/', views.testimonialListView, name='testimonialList'), # Read
    path('edit/<int:pk>', views.testimonialEditView, name='testimonialEdit'),  # Update
    path('delete/<int:pk>', views.testimonialDeleteView, name='testimonialDelete'),  # Update
    path('d:<str:slug>/', views.testimonial_detail, name='testimonial_detail'), # Front
]