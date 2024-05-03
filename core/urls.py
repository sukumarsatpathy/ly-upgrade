from django.contrib import admin
from django.shortcuts import redirect
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    path('', include('pages.urls')),
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('dashboard/', lambda request: redirect('dashboard', permanent=True)),
    path('training/', include('training.urls')),
    path('event/', include('event.urls')),
    path('tokens/', include('tokens.urls')),
    path('settings/', include('settings.urls')),
    path('subscription/', include('subscription.urls')),
    path('testimonial/', include('testimonial.urls')),
    path('news/', include('news.urls')),
    path('social/', include('social.urls')),
    path('prozone/', include('prozone.urls')),
    path('club/', include('club.urls')),
    path('report/', include('report.urls')),
    path('payment/', include('payment.urls')),
    path('drk/', include('drk.urls')),

    path('ckeditor/', include('ckeditor_uploader.urls')),
    path("__debug__/", include("debug_toolbar.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
