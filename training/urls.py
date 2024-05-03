from django.urls import path
from . import views
from .views import AddTrainingView, ListTrainingView, EditTrainingView, DeleteTrainingView, FinderTrainingView

urlpatterns = [
    path('', ListTrainingView.as_view(), name='list-training'),
    path('add/', AddTrainingView.as_view(), name='add-training'),
    path('<int:pk>/edit', EditTrainingView.as_view(), name='edit-training'),
    path('<int:pk>/delete', DeleteTrainingView.as_view(), name='delete-training'),
    path('find-trainings-worldwide/', views.FinderTrainingView, name='find-training'),
    path('<int:pk>/', views.TrainingDetailsView, name='training-detail'),
    path('ajax/load-countries/training', views.load_countries, name='load_country_training'),  # <-- this one here
    path('load_state/training', views.load_state, name='load_state_training'),
    path('load_city/category/training', views.load_cites, name='load_city_category_training'),

    path('add/', views.trainingAddView, name='trainingAdd'), # Create
    path('list/', views.trainingListView, name='trainingList'), # Read
    path('edit/<int:pk>', views.trainingEditView, name='trainingEdit'),  # Update
    path('delete/<int:pk>', views.trainingDeleteView, name='trainingDelete'),  # Update
]
