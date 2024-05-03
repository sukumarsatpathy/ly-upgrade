from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .models import ly2Transaction, blcTransaction, cttTransaction, indTraining, wcTransaction, prozoneTransaction


class ly2TransactionAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('id', 'course', 'full_name', 'email', 'contact', 'country', 'price', 'information', 'enrolled_date')
    list_display_links = ('course', 'full_name', 'email')
    search_fields = ('course', 'full_name', 'email', 'contact', 'country', 'information')
    readonly_fields = ('course', 'full_name', 'email', 'contact', 'address', 'city', 'state', 'country', 'postalcode', 'price', 'information', 'token')

admin.site.register(ly2Transaction, ly2TransactionAdmin)


class blcTransactionAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('id', 'course', 'full_name', 'email', 'contact', 'country', 'price', 'information', 'enrolled_date')
    list_display_links = ('course', 'full_name', 'email')
    search_fields = ('course', 'full_name', 'email', 'contact', 'country', 'information')
    readonly_fields = ('course', 'full_name', 'email', 'contact', 'address', 'city', 'state', 'country', 'postalcode', 'price', 'information', 'token')


admin.site.register(blcTransaction, blcTransactionAdmin)


class cttTransactionAdmin(admin.ModelAdmin):
    list_display = ('id', 'full_name', 'email', 'contact', 'country', 'price', 'information', 'enrolled_date')
    list_display_links = ('full_name', 'email')
    search_fields = ('full_name', 'email', 'contact', 'country', 'information')
    readonly_fields = ('full_name', 'email', 'contact', 'address', 'city', 'state', 'country', 'postalcode', 'price', 'information', 'token')


admin.site.register(cttTransaction, cttTransactionAdmin)


class indTrainingAdmin(admin.ModelAdmin):
    list_display = ('id', 'full_name', 'email', 'contact', 'enrolled_date')
    list_display_links = ('full_name', 'email')
    search_fields = ('full_name', 'email', 'contact', 'information')
    readonly_fields = ('full_name', 'email', 'contact', 'price', 'token')


admin.site.register(indTraining, indTrainingAdmin)


class wcTransactionAdmin(admin.ModelAdmin):
    list_display = ('id', 'full_name', 'email', 'contact', 'country', 'price', 'information', 'enrolled_date')
    list_display_links = ('full_name', 'email')
    search_fields = ('full_name', 'email', 'contact', 'country', 'information')
    readonly_fields = (
    'full_name', 'email', 'contact', 'address', 'city', 'state', 'country', 'postalcode', 'price',
    'information', 'token')


admin.site.register(wcTransaction, wcTransactionAdmin)


class prozoneTransactionAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('id', 'full_name', 'email', 'contact', 'country', 'price', 'subscribed_date')
    list_display_links = ('full_name', 'email')
    search_fields = ('membership_name', 'full_name', 'email', 'contact', 'country')
    readonly_fields = ('membership_name', 'start_date', 'expiry_date', 'full_name', 'email', 'contact', 'address', 'city', 'state', 'country', 'postalcode', 'price', 'token')


admin.site.register(prozoneTransaction, prozoneTransactionAdmin)