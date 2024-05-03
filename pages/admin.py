from django.contrib import admin
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _
from .models import GetInvolved, Diary, laughterBlogs, laughterBlogsCat, generalResearch


class GetInvolvedAdmin(admin.ModelAdmin):
    def thumbnail(self, object):
        return format_html('<img src="{}" width="30" "/>'.format(object.image.url))

    list_display = ('id', 'thumbnail', 'title', 'url', 'status', 'created_date')
    list_display_links = ('id', 'thumbnail', 'title', 'url')
    fieldsets = [
        ('Basic Details', {'fields': ['title', 'description', 'image', 'btn_name', 'url', 'status']}),
    ]
    search_fields = ('title', 'url')


admin.site.register(GetInvolved, GetInvolvedAdmin)


class DiaryAdmin(admin.ModelAdmin):
    def thumbnail(self, object):
        return format_html('<img src="{}" width="40" />'.format(object.image.url))

    thumbnail.short_description = 'Image'

    list_display = ('id', 'thumbnail', 'title', 'modified_date', 'views')
    list_display_links = ('id', 'title')
    fieldsets = [
        (_('Basic Details'), {'fields': ['title', 'slug', 'description', 'image', 'views']}),
    ]
    search_fields = ('title',)
    prepopulated_fields = {'slug': ('title',), }


admin.site.register(Diary, DiaryAdmin)


class laughterBlogsCatAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'created_date', 'modified_date')
    list_display_links = ('id', 'title')
    prepopulated_fields = {'slug': ('title',), }
    search_fields = ('title',)
    fieldsets = [
        ('Prozone Category Details', {
            'fields': ['title', 'slug']}),
    ]


admin.site.register(laughterBlogsCat, laughterBlogsCatAdmin)


class laughterBlogsAdmin(admin.ModelAdmin):
    pass

    def thumbnail(self, object):
        return format_html('<img src="{}" width="40" />'.format(object.image.url))

    list_display = ('id', 'thumbnail', 'category', 'title', 'created_date', 'modified_date')
    list_display_links = ('id', 'title')
    prepopulated_fields = {'slug': ('title',), }
    search_fields = ('title',)
    fieldsets = [
        ('Laughter Blog Details', {'fields': ['category', 'title', 'slug', 'description', 'image', 'views']}),
        ('SEO Details', {'fields': ['meta_title', 'meta_description', 'meta_keywords']}),
    ]


admin.site.register(laughterBlogs, laughterBlogsAdmin)


class generalResearchAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'created_date', 'modified_date', 'views')
    list_display_links = ('id', 'title')

    fieldsets = [
        ('Prozone Research Details', {
            'fields': [ 'title', 'slug', 'description', 'image', 'views']}),
        ('SEO Details', {'fields': ['meta_title', 'meta_description', 'meta_keywords']}),
    ]
    prepopulated_fields = {'slug': ('title',), }
    search_fields = ('title',)


admin.site.register(generalResearch, generalResearchAdmin)