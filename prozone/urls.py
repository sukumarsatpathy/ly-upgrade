from django.urls import path
from .import views

urlpatterns = [
    path('', views.prozoneLanding, name='prozone'),

    path('drk-pro-diary/', views.prodiaryList, name='drk-pro-diary'),# Frontend
    path('drk-pro-diary/<str:slug>/', views.prodiarydetail, name='drk-pro-diary-detail'),# Frontend
    path('drk-pro-diary/list', views.proDiaryListView, name='proDiaryList'), #Admin
    path('drk-pro-diary/add', views.proDiaryAddView, name='proDiaryAdd'), #Admin
    path('drk-pro-diary/edit/<str:slug>', views.proDiaryEditView, name='proDiaryEdit'), #Admin
    path('drk-pro-diary/delete/<str:slug>', views.proDiaryDeleteView, name='proDiaryDelete'), #Admin

    path('research-articles/', views.proresearchList, name='pro-research-articles'), #Frontend
    path('research-articles/<str:slug>/', views.proresearchdetail, name='pro-research-articles-detail'), #Frontend
    path('research-articles/list', views.raListView, name='raList'), #Admin
    path('research-articles/add', views.raAddView, name='raAdd'), #Admin
    path('research-articles/edit/<str:slug>', views.raEditView, name='raEdit'), #Admin
    path('research-articles/delete/<str:slug>', views.raDeleteView, name='raDelete'), #Admin

    path('watch-videos/', views.videoList, name='watch-pro-videos'),#Frontend
    path('watch-videos/list', views.videosListView, name='videosList'), #Admin
    path('watch-videos/add', views.videosAddView, name='videosAdd'), #Admin
    path('watch-videos/edit/<str:slug>', views.videosEditView, name='videosEdit'), #Admin
    path('watch-videos/delete/<str:slug>', views.videosDeleteView, name='videosDelete'), #Admin

    path('download-resources/', views.downloadList, name='download-resources'),#Frontend
    path('download-resources/list', views.resourcesListView, name='resourcesList'), #Admin
    path('download-resources/add', views.resourcesAddView, name='resourcesAdd'), #Admin
    path('download-resources/edit/<str:slug>', views.resourcesEditView, name='resourcesEdit'), #Admin
    path('download-resources/delete/<str:slug>', views.resourcesDeleteView, name='resourcesDelete'), #Admin

    path('download-photos/', views.downloadPhotosList, name='download-photos'),
    path('download-photos/c:<str:cat_slug>', views.downloadCatPhotosList, name='download-cat-photos'),
    path('download-photos/list', views.photosListView, name='photosList'), #Admin
    path('download-photos/add', views.photosAddView, name='photosAdd'), #Admin
    path('download-photos/edit/<str:slug>', views.photosEditView, name='photosEdit'), #Admin
    path('download-photos/delete/<str:slug>', views.photosDeleteView, name='photosDelete'), #Admin

    path('download-quotes/', views.downloadQuoteList, name='download-quotes'),
    path('download-quotes/list', views.quotesListView, name='quotesList'), #Admin
    path('download-quotes/add', views.quotesAddView, name='quotesAdd'), #Admin
    path('download-quotes/edit/<str:slug>', views.quotesEditView, name='quotesEdit'), #Admin
    path('download-quotes/delete/<str:slug>', views.quotesDeleteView, name='quotesDelete'), #Admin


    #Dropdown
    path('add-category/', views.addCategory, name='add-category'),
]