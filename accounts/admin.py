from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from image_cropping import ImageCroppingMixin
from django.contrib.auth.models import Group
from accounts.models import Account
from tokens.models import LeaderUniqueToken, TeacherUniqueToken
from subscription.models import Subscription
from import_export.admin import ImportExportModelAdmin


class Subscriptioninline(admin.TabularInline):
    model = Subscription
    extra = 1


class CustomUserAdmin(ImportExportModelAdmin, ImageCroppingMixin, BaseUserAdmin):
    inlines = [
               Subscriptioninline
    ]
    list_display = (
        'id', 'first_name', 'last_name', 'email', 'user_type', 'country', 'last_login', 'views', 'active', 'is_masked')
    list_display_links = ('id', 'first_name', 'last_name', 'email')
    search_fields = ('id', 'first_name', 'last_name', 'email', 'user_type', 'token')
    ordering = ('id',)
    readonly_fields = ('token',)
    # resource_class = CustomUserResource # Export DB
    fieldsets = (
        (_('Account Details'), {'fields': ('email', 'password')}),
        (_('Personal Details'), {'fields': ('first_name', 'last_name', 'contact_number', 'profile_pic')}),
        (_('Professional Details'), {'fields': ('user_type', 'trained_by', 'services', 'other_services', 'description')}),
        (_('Address'), {'fields': ('country', 'state', 'city' )}),
        (_('Social Details'), {'fields': ('website_url', 'facebook_url', 'youtube_url', 'linkedin_url')}),
        (_('Video URLs'), {'fields': ('video_url_1', 'video_url_2', 'video_url_3', 'video_url_4')}),
        (_('Upcoming Trainings'), {'fields': ('basic_learning_course', 'certified_leader_training',
                                              'certified_teacher_training')}),
        (_('Miscellaneous Details'), {'fields': ('token', 'views', 'is_ambassador', 'is_masked', 'active', 'staff', 'admin', 'last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (_('Account Details'), {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),
        }),
        (_('Personal Details'), {'fields': ('first_name', 'last_name', 'contact_number', 'profile_pic')}),
        (_('Professional Details'), {'fields': ('user_type', 'trained_by', 'services', 'other_services', 'description')}),
        (_('Address'), {'fields': ('country', 'state', 'city')}),
        (_('Social Details'), {'fields': ('website_url', 'facebook_url', 'youtube_url', 'linkedin_url')}),
        (_('Video URLs'), {'fields': ('video_url_1', 'video_url_2', 'video_url_3', 'video_url_4')}),
        (_('Upcoming Trainings'), {'fields': ('basic_learning_course', 'certified_leader_training',
                                              'certified_teacher_training')}),
        (_('Miscellaneous Details'), {'fields': ('token', 'is_ambassador', 'is_masked', 'active', 'staff', 'admin', 'last_login', 'date_joined')}),
    )


admin.site.register(Account, CustomUserAdmin)
admin.site.unregister(Group)
