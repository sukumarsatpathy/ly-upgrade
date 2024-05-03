
from django.contrib import admin
from .models import Training, TrainingCategory
from django.db import models
from django.utils.html import format_html
from image_cropping import ImageCroppingMixin
from import_export.admin import ImportExportModelAdmin


class TrainingAdmin(admin.ModelAdmin):
    list_display = ('id', 'category_title', 'trainer_name', 'country', 'state', 'city', 'start_date', 'end_date', 'modified_date', 'created_date', 'views', 'status')
    list_display_links = ('id', 'category_title', 'trainer_name',)
    search_fields = ('category_title', 'trainer_name')
    autocomplete_fields = ['author', ]
    fieldsets = [
        ('Basic Details', {'fields': ['category_title', 'description', 'start_date', 'end_date']}),
        ('Location Details', {'fields': ['location', 'country', 'state', 'city']}),
        ('Contact Details', {'fields': ['trainer_name', 'email', 'contact_no', 'author']}),
        ('Image and Videos', {'fields': ['img1', 'img2', 'img3', 'img4', 'video_url', 'video_url_1', 'video_url_2', 'video_url_3', 'video_url_4', 'status']}),
    ]


admin.site.register(Training, TrainingAdmin)


class TrainingCategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'title')
    list_display_links = ('id', 'title')
    search_fields = ('title',)


admin.site.register(TrainingCategory, TrainingCategoryAdmin)
