from django.urls import path
from .import views

urlpatterns = [
    #path('', views.ly2Landing, name='ly2'),

    # LY2 Payment URLs
    path('ly2-charge/', views.ly2charge, name='ly2charge'),
    path('ly2-success/', views.ly2successMsg, name='ly2success'),
    # path('ly2-success/<str:args>/', views.ly2successMsg, name='ly2success'),

    # BLC Payment URLs
    path('blc-charge/', views.blccharge, name='blccharge'),
    path('online-basic-training/', views.blcsuccessMsg, name='blcsuccess'),

    # Teacher Training Payment URLs
    path('teacher-training-charge/', views.teachertcharge, name='ctttcharge'),
    path('teacher-training-success/<str:args>/', views.teachertsuccessMsg, name='cttsuccess'),


    # India Training Payment URLs
    path('blc-ind-charge/', views.indTrainingCharge, name='indTrainingCharge'),
    path('blc-ind-success/', views.blcIndsuccess, name='blcIndSuccess'),

    # Conference Payment
    path('wcSuccess/', views.wcSuccess, name='wcSuccess'),

]

