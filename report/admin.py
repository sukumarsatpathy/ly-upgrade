from django.contrib import admin
from .models import Contact, InfoBooklet, LYTourEnquiry, ZoomLCEnquiry, SpiritualRetreat
from import_export.admin import ImportExportModelAdmin


class ContactAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('id', 'category', 'full_name', 'email', 'contact', 'country', 'created')
    list_display_links = ('category', 'full_name', 'email')
    search_fields = ('category', 'full_name', 'email', 'contact', 'country')
    readonly_fields = ('category', 'full_name', 'email', 'contact', 'country', 'message', 'created')

    # This will help you to disable add functionality
    def has_add_permission(self, request):
        return False

    # This will help you to disable delete functionality
    def has_delete_permission(self, request, obj=None):
        return False

    # This will help you to disable change functionality
    # def has_change_permission(self, request, obj=None):
    #     return False


admin.site.register(Contact, ContactAdmin)


class InfoBookletAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('id', 'full_name', 'email', 'country', 'downloaded')
    list_display_links = ('full_name', 'email')
    search_fields = ('full_name', 'email', 'country')

    # This will help you to disable add functionality
    def has_add_permission(self, request):
        return False

    # This will help you to disable delete functionality
    def has_delete_permission(self, request, obj=None):
        return False

    # This will help you to disable change functionality
    # def has_change_permission(self, request, obj=None):
    #     return False


admin.site.register(InfoBooklet, InfoBookletAdmin)


class LYTourEnquiryAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('id', 'category', 'full_name', 'email', 'contact', 'created')
    list_display_links = ('full_name', 'email')
    search_fields = ('category', 'full_name', 'email', 'contact')
    readonly_fields = ('category', 'full_name', 'email', 'contact', 'created')
    # resource_class = LYTourEnquiryResource # DB Export
    # This will help you to disable add functionality
    def has_add_permission(self, request):
        return False

    # This will help you to disable delete functionality
    def has_delete_permission(self, request, obj=None):
        return False

    # This will help you to disable change functionality
    # def has_change_permission(self, request, obj=None):
    #     return False


admin.site.register(LYTourEnquiry, LYTourEnquiryAdmin)


class ZoomLCEnquiryAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('id', 'full_name', 'email', 'contact', 'occupation', 'country', 'created')
    list_display_links = ('full_name', 'email', 'occupation', 'country')
    search_fields = ('full_name', 'email', 'contact', 'country', 'token')
    readonly_fields = ('full_name', 'email', 'contact', 'occupation', 'country', 'token', 'created')
    # resource_class = ZLCEnquiryResource # DB Export
    # This will help you to disable add functionality
    def has_add_permission(self, request):
        return False

    # This will help you to disable delete functionality
    def has_delete_permission(self, request, obj=None):
        return False

    # This will help you to disable change functionality
    # def has_change_permission(self, request, obj=None):
    #     return False


admin.site.register(ZoomLCEnquiry, ZoomLCEnquiryAdmin)


class SpiritualRetreatAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'whatsapp', 'accommodation', 'whatsapp_status', 'email_status', 'submitted_date')
    list_display_links = ('name', 'whatsapp', 'accommodation')
    search_fields = ('name', 'email', 'whatsapp', 'location', 'token')
    readonly_fields = ('name', 'email', 'whatsapp', 'location', 'accommodation', 'comments', 'token', 'submitted_date')
    # resource_class = spiritualRetreatResource # DB Export
    # This will help you to disable add functionality
    def has_add_permission(self, request):
        return True

    # This will help you to disable delete functionality
    def has_delete_permission(self, request, obj=None):
        return False

    # This will help you to disable change functionality
    def has_change_permission(self, request, obj=None):
        return False

admin.site.register(SpiritualRetreat, SpiritualRetreatAdmin)