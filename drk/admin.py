from django.contrib import admin
from .models import UpcomingEvents
from django.utils.html import format_html
from image_cropping import ImageCroppingMixin
from import_export.admin import ImportExportModelAdmin

class UpcomingEventsAdmin(ImportExportModelAdmin, ImageCroppingMixin, admin.ModelAdmin):
    list_display = (
        'id', 'title', 'startDate','duration', 'language', 'created_date', 'modified_date')
    list_display_links = ('id', 'title')
    search_fields = ('title', 'duration', 'language')
    fieldsets = [
        ('Basic Details', {'fields': ['title', 'description', 'startDate', 'duration', 'timing', 'language']}),
        ('Image Details',  {'fields': ('image',)}),
        ('Button Details',  {'fields': ('btnText', 'btnURL', 'btnBgColor', 'is_active', 'is_daily')}),
    ]


admin.site.register(UpcomingEvents, UpcomingEventsAdmin)