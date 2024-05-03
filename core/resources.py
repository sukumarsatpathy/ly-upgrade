from import_export import resources, fields  # For import_export functionality
from accounts.models import Account  # For import_export functionality
from report.models import LYTourEnquiry, Contact, InfoBooklet, SpiritualRetreat, ZoomLCEnquiry
from payment.models import blcTransaction, ly2Transaction
from subscription.models import Subscription
from testimonial.models import Testimonial


class CustomUserResource(resources.ModelResource):

    class Meta:
        model = Account
        fields = ('first_name', 'last_name', 'email', 'contact_number', 'registration_no', 'user_type',
                   'trained_by', 'country__name', 'state__name', 'city__name')


class LYTourEnquiryResource(resources.ModelResource):

    class Meta:
        model = LYTourEnquiry
        fields = ('id', 'full_name', 'email', 'contact')


class ZLCEnquiryResource(resources.ModelResource):

    class Meta:
        model = ZoomLCEnquiry
        fields = ('id', 'full_name', 'email', 'contact', 'country')


class blcTransactionResource(resources.ModelResource):

    class Meta:
        model = blcTransaction
        fields = ('course', 'full_name', 'email', 'city', 'country', 'postalcode', 'contact', 'price', 'enrolled_date')


class ly2TransactionResource(resources.ModelResource):

    class Meta:
        model = ly2Transaction
        fields = ('course', 'full_name', 'email', 'city', 'country', 'postalcode', 'contact', 'price', 'enrolled_date')


class subscriptionResource(resources.ModelResource):
    class Meta:
        model = Subscription
        fields = ('user__email', 'membership__title', 'startDate', 'endDate', 'token', 'status')
        export_order = ['user__email', 'membership__title', 'startDate', 'endDate', 'token', 'status']


class contactResource(resources.ModelResource):
    class Meta:
        model = Contact
        fields = ('category', 'full_name', 'email', 'contact', 'token', 'active')
        export_order = ['user__email', 'membership__membership_name', 'start_date', 'expiry_date', 'token', 'active']


class spiritualRetreatResource(resources.ModelResource):
    class Meta:
        model = Contact
        fields = ('id', 'name', 'email', 'whatsapp', 'location', 'info', 'accommodation', 'comment', 'token', 'whatsapp_status', 'email_status', 'submitted_date')
        export_order = ['name', 'email', 'whatsapp', 'location', 'info', 'accommodation', 'comment', 'token', 'whatsapp_status', 'email_status', 'submitted_date']



class testimonialResource(resources.ModelResource):
    class Meta:
        model = Testimonial
        fields = ('title', 'slug', 'description', 'image', 'author', 'location', 'meta_title', 'meta_description', 'views', 'status')
        export_order = ['title', 'slug', 'description', 'image', 'author', 'location', 'meta_title', 'meta_description', 'views', 'status']