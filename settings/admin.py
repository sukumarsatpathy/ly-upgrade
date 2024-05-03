from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
# from core.resources import CountryResource, StateResource, CityResource
from .models import (WebSettings, MailServer, StripeGateway, RazorPayGateway, Country, State, City, Twilio, Services,
                     Banners, FAQ, Changelog, Membership)


admin.site.register(WebSettings)
admin.site.register(MailServer)
admin.site.register(StripeGateway)
admin.site.register(RazorPayGateway)
admin.site.register(Services)
admin.site.register(Banners)
admin.site.register(FAQ)
admin.site.register(Changelog)


@admin.register(Country)
class CountryAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('id', 'name', 'iso3', 'iso2', 'numeric_code', 'phone_code', 'modified')
    list_display_links = ('id', 'name', 'numeric_code', 'iso2', 'iso3')
    search_fields = ('name',)
    # resource_class = CountryResource


@admin.register(State)
class StateAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('id', 'name', 'country', 'state_code', 'latitude', 'longitude', 'modified')
    list_display_links = ('id', 'name', 'country', 'state_code', 'latitude', 'longitude')
    search_fields = ('name',)
    # resource_class = StateResource


@admin.register(City)
class CityAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('id', 'name', 'country', 'state', 'latitude', 'longitude')
    list_display_links = ('id', 'name', 'country', 'state', 'latitude', 'longitude')
    search_fields = ('name',)
    # resource_class = CityResource


@admin.register(Twilio)
class TwilioAdmin(admin.ModelAdmin):
    list_display = ('id', 'accountSID', 'authToken', 'phoneNumber', 'status', 'modified')
    list_display_links = ('id', 'accountSID', 'authToken', 'phoneNumber', 'status', 'modified')
    search_fields = ('accountSID',)

class MembershipAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',), }
    list_display = ('id', 'title', 'type', 'price', 'duration')
    list_display_links = ('id', 'title', 'type', 'price')
    search_fields = ('title', 'type', 'duration')


admin.site.register(Membership, MembershipAdmin)