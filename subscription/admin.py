from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .models import Subscription
from core.resources import subscriptionResource


class SubscriptionAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('id', 'user', 'membership', 'token', 'startDate', 'endDate', 'status')
    list_display_links = ('id', 'user', 'membership')
    search_fields = ('user__email', 'membership__title')
    resource_class = subscriptionResource


admin.site.register(Subscription, SubscriptionAdmin)
