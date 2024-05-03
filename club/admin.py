from django.contrib import admin
from .models import Club, ClubCategory
from django.utils.html import format_html
from image_cropping import ImageCroppingMixin
from import_export.admin import ImportExportModelAdmin


class ClubAdmin(ImportExportModelAdmin, ImageCroppingMixin, admin.ModelAdmin):
    list_display = (
        'id', 'title', 'author', 'country', 'state', 'city', 'created_date',
        'modified_date', 'views')
    list_display_links = ('id', 'title', 'author', 'country')
    search_fields = ('title', 'email', 'author__email')
    autocomplete_fields = ['author', ]
    fieldsets = [
        ('Laughter Club Basic Details', {'fields': ['category_title', 'title', 'description', 'frequency']}),
        ('Laughter Club Location Details', {'fields': ['location', 'country', 'state', 'city']}),
        ('Trainer Details', {'fields': ['contact_name', 'email', 'contact_no', 'author', 'views']}),
        ('Image and Video Details',  {'fields': ('image1', 'image2', 'video1', 'video2')}),
    ]


admin.site.register(Club, ClubAdmin)


class ClubCategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'title')
    list_display_links = ('id', 'title')
    search_fields = ('title',)


admin.site.register(ClubCategory, ClubCategoryAdmin)

