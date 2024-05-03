from django.urls import path
from django.shortcuts import redirect
from . import views


urlpatterns = [
    path('feeds/', views.feedsView, name='feeds'),
    # path('logout/', views.logout, name='logout'),
    # path('dashboard/', views.dashboard, name='dashboard'),
    #
    # # User Management
    # path('list/', views.userListView, name='userList'), # Read
    # path('add/', views.userAddView, name='userAdd'), # Create
    # path('view/<int:pk>', views.userView, name='userView'), # View
    # path('edit/<int:pk>', views.userEditView, name='userEdit'), # Update
    # path('delete/<int:pk>', views.userDeleteView, name='userDelete'), # Delete
]