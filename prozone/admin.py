from django.contrib import admin
from django.db import models
from django.utils.html import format_html
from .models import ProDiary, ProVideos, ProDownloads, ProPhotos, ProQuotes, ProResearch, ProPhotosCat


class ProVideosAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'created_date', 'modified_date', 'views')
    list_display_links = ('id', 'title')

    fieldsets = [
        ('Prozone Video Details', {
            'fields': ['title', 'slug', 'description', 'video_code', 'views']}),
    ]
    prepopulated_fields = {'slug': ('title',), }
    search_fields = ('title', 'url')


admin.site.register(ProVideos, ProVideosAdmin)


class ProDiaryAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'created_date', 'modified_date', 'views')
    list_display_links = ('id', 'title')

    fieldsets = [
        ('Prozone Article Details', {
            'fields': [ 'title', 'slug', 'description', 'image', 'views']}),
    ]
    prepopulated_fields = {'slug': ('title',), }
    search_fields = ('title',)


admin.site.register(ProDiary, ProDiaryAdmin)


class ProResearchAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'created_date', 'modified_date', 'views')
    list_display_links = ('id', 'title')

    fieldsets = [
        ('Prozone Research Details', {
            'fields': [ 'title', 'slug', 'description', 'image', 'views']}),
    ]
    prepopulated_fields = {'slug': ('title',), }
    search_fields = ('title',)


admin.site.register(ProResearch, ProResearchAdmin)


class ProDownloadsAdmin(admin.ModelAdmin):
    pass

    def thumbnail(self, object):
        return format_html('<img src="{}" width="40" />'.format(object.image.url))

    list_display = ('id', 'thumbnail', 'title', 'created_date', 'modified_date',  'views')
    list_display_links = ('id', 'title')
    search_fields = ('title',)
    prepopulated_fields = {'slug': ('title',), }
    fieldsets = [
        ('Prozone Download Details', {
            'fields': ['title', 'slug', 'image', 'download_link', 'description', 'views']}),
    ]


admin.site.register(ProDownloads, ProDownloadsAdmin)


class ProPhotosCatAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'created_date', 'modified_date')
    list_display_links = ('id', 'title')
    prepopulated_fields = {'slug': ('title',), }
    search_fields = ('title',)
    fieldsets = [
        ('Prozone Category Details', {
            'fields': ['title', 'slug']}),
    ]


admin.site.register(ProPhotosCat, ProPhotosCatAdmin)


class ProPhotosAdmin(admin.ModelAdmin):
    pass

    def thumbnail(self, object):
        return format_html('<img src="{}" width="40" />'.format(object.image.url))

    list_display = ('id', 'thumbnail', 'category', 'title', 'created_date', 'modified_date')
    list_display_links = ('id', 'title')
    prepopulated_fields = {'slug': ('title',), }
    search_fields = ('title',)
    fieldsets = [
        ('Prozone Download Details', {
            'fields': ['category', 'title', 'slug', 'image', 'download_link']}),
    ]


admin.site.register(ProPhotos, ProPhotosAdmin)


class ProQuotesAdmin(admin.ModelAdmin):
    pass

    def thumbnail(self, object):
        return format_html('<img src="{}" width="40" />'.format(object.image.url))

    list_display = ('id', 'thumbnail', 'title', 'created_date', 'modified_date')
    list_display_links = ('id', 'title')
    prepopulated_fields = {'slug': ('title',), }
    search_fields = ('title',)
    fieldsets = [
        ('Prozone Download Details', {
            'fields': ['title', 'slug', 'image', 'download_link']}),
    ]


admin.site.register(ProQuotes, ProQuotesAdmin)