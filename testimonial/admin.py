from django.contrib import admin
from .models import Testimonial
from django.utils.html import format_html
from import_export.admin import ImportExportModelAdmin
from core.resources import testimonialResource


class TestimonialAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    def thumbnail(self, object):
        return format_html('<img src="{}" width="30" "/>'.format(object.image.url))
    thumbnail.short_description = 'Testimonial Image'
    list_display = ('id', 'thumbnail', 'title', 'author', 'location', 'status', 'modified_date', 'views')
    list_display_links = ('id', 'thumbnail', 'title', 'author', 'location')
    list_editable =('status',)
    # autocomplete_fields = ('author',)
    search_fields = ('title', 'location', 'location')
    prepopulated_fields = {'slug': ('title',), }
    resource_class = testimonialResource

    fieldsets = [
        ('Basic Details', {'fields': ['title', 'slug', 'description', 'image', 'publisher', 'location', 'author', 'status']}),
        ('SEO Details', {'fields': ['meta_title', 'meta_description']}),
    ]


admin.site.register(Testimonial, TestimonialAdmin)