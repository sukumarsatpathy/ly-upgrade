from django.contrib import admin
from .models import Event
from django.db import models
from django.utils.html import format_html
from image_cropping import ImageCroppingMixin


class EventAdmin(ImageCroppingMixin, admin.ModelAdmin):
    list_display = ('id', 'author', 'country', 'state', 'city', 'start_date', 'end_date', 'modified_date', 'created_date', 'views')
    list_display_links = ('id', 'author', 'country')
    fieldsets = [
        ('Event Basic Details', {'fields': ['category', 'description', 'start_date', 'end_date']}),
        ('Event Location Details', {'fields': ['location', 'country', 'state', 'city']}),
        ('Organizer Details', {'fields': ['organiser_name', 'author', 'email', 'contact_no', 'website_url']}),
        ('Images and Videos', {'fields': ['img1', 'img2', 'video1', 'video2']}),
    ]
    search_fields = ('title', 'author', 'country', 'state', 'city')
    autocomplete_fields = ['author', ]


admin.site.register(Event, EventAdmin)