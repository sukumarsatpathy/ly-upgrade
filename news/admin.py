from django.contrib import admin
from .models import News
from django.utils.html import format_html
from import_export.admin import ImportExportModelAdmin


class NewsAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    def thumbnail(self, object):
        return format_html('<img src="{}" width="30" "/>'.format(object.image.url))
    thumbnail.short_description = 'News Image'
    list_display = ('id', 'thumbnail', 'title', 'location', 'status', 'modified_date', 'views')
    list_display_links = ('id', 'thumbnail', 'title', 'location')
    list_editable =('status',)
    search_fields = ('title', 'location', 'location')
    prepopulated_fields = {'slug': ('title',), }

    fieldsets = [
        ('Basic Details', {'fields': ['title', 'slug', 'description', 'image', 'location', 'status']}),
        ('SEO Details', {'fields': ['meta_title', 'meta_description']}),
    ]


admin.site.register(News, NewsAdmin)