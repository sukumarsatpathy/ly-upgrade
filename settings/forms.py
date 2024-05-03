from django import forms
from .models import WebSettings, MailServer, StripeGateway, RazorPayGateway, Country, State, City, Twilio, Membership


class WebSettingsForm(forms.ModelForm):
    class Meta:
        model = WebSettings
        fields = ('title', 'slogan', 'logo_dark', 'logo_light', 'favicon', 'contact_email', 'contact_number',
                  'contact_address', 'company_name', 'company_address', 'company_gst', 'meta_title', 'meta_description',
                  'meta_keywords', 'default_user', 'public_key', 'private_key')

    def __init__(self, *args, **kwargs):
        super(WebSettingsForm, self).__init__(*args, **kwargs)
        self.fields['title'].widget.attrs['class'] = 'form-control'
        self.fields['slogan'].widget.attrs['class'] = 'form-control'
        self.fields['logo_dark'].widget.attrs['class'] = 'form-control'
        self.fields['logo_light'].widget.attrs['class'] = 'form-control'
        self.fields['favicon'].widget.attrs['class'] = 'form-control'
        self.fields['contact_email'].widget.attrs['class'] = 'form-control'
        self.fields['contact_number'].widget.attrs['class'] = 'form-control'
        self.fields['contact_address'].widget.attrs['class'] = 'form-control'
        self.fields['company_name'].widget.attrs['class'] = 'form-control'
        self.fields['company_address'].widget.attrs['class'] = 'form-control'
        self.fields['company_gst'].widget.attrs['class'] = 'form-control'
        self.fields['meta_title'].widget.attrs['class'] = 'form-control kt_docs_maxlength_basic'
        self.fields['meta_title'].widget.attrs['maxlength'] = '60'
        self.fields['meta_description'].widget.attrs['class'] = 'form-control kt_docs_maxlength_basic'
        self.fields['meta_description'].widget.attrs['maxlength'] = '255'
        self.fields['meta_keywords'].widget.attrs['class'] = 'form-control'
        self.fields['default_user'].widget.attrs['class'] = 'form-control'
        self.fields['public_key'].widget.attrs['class'] = 'form-control'
        self.fields['private_key'].widget.attrs['class'] = 'form-control'
        for field in self.fields:
            self.fields[field].widget.attrs['placeholder'] = 'Provide Detail'


class MailServerForm(forms.ModelForm):
    class Meta:
        model = MailServer
        fields = ('name', 'email', 'port', 'host', 'host_user', 'host_password', 'use_tls', 'use_ssl')

    def __init__(self, *args, **kwargs):
        super(MailServerForm, self).__init__(*args, **kwargs)
        self.fields['name'].widget.attrs['class'] = 'form-control'
        self.fields['email'].widget.attrs['class'] = 'form-control'
        self.fields['port'].widget.attrs['class'] = 'form-control'
        self.fields['host'].widget.attrs['class'] = 'form-control'
        self.fields['host_user'].widget.attrs['class'] = 'form-control'
        self.fields['host_password'].widget.attrs['class'] = 'form-control'
        self.fields['use_tls'].widget.attrs['class'] = 'form-select'
        self.fields['use_ssl'].widget.attrs['class'] = 'form-select'
        for field in self.fields:
            self.fields[field].widget.attrs['placeholder'] = 'Provide Detail'


class StripeGatewayForm(forms.ModelForm):
    class Meta:
        model = StripeGateway
        fields = ('key_type', 'public_key', 'secret_key', 'status')

    def __init__(self, *args, **kwargs):
        super(StripeGatewayForm, self).__init__(*args, **kwargs)
        self.fields['key_type'].widget.attrs['class'] = 'form-select'
        self.fields['public_key'].widget.attrs['class'] = 'form-control'
        self.fields['secret_key'].widget.attrs['class'] = 'form-control'
        self.fields['status'].widget.attrs['class'] = 'form-select'
        for field in self.fields:
            self.fields[field].widget.attrs['placeholder'] = 'Provide Detail'


class RazorPayGatewayForm(forms.ModelForm):
    class Meta:
        model = RazorPayGateway
        fields = ('key_type', 'key_id', 'key_secret', 'status')

    def __init__(self, *args, **kwargs):
        super(RazorPayGatewayForm, self).__init__(*args, **kwargs)
        self.fields['key_type'].widget.attrs['class'] = 'form-select'
        self.fields['key_id'].widget.attrs['class'] = 'form-control'
        self.fields['key_secret'].widget.attrs['class'] = 'form-control'
        self.fields['status'].widget.attrs['class'] = 'form-select'
        for field in self.fields:
            self.fields[field].widget.attrs['placeholder'] = 'Provide Detail'


class CountryForm(forms.ModelForm):
    class Meta:
        model = Country
        fields = ('name', 'iso3', 'iso2', 'numeric_code', 'phone_code', 'capital', 'currency', 'currency_symbol', 'tld',
                  'native', 'region', 'sub_region', 'timezones', 'latitude', 'longitude', 'emoji', 'emojiU', 'status')

    def __init__(self, *args, **kwargs):
        super(CountryForm, self).__init__(*args, **kwargs)
        self.fields['name'].widget.attrs['class'] = 'form-control'
        self.fields['iso3'].widget.attrs['class'] = 'form-control'
        self.fields['iso2'].widget.attrs['class'] = 'form-control'
        self.fields['numeric_code'].widget.attrs['class'] = 'form-control'
        self.fields['phone_code'].widget.attrs['class'] = 'form-control'
        self.fields['capital'].widget.attrs['class'] = 'form-control'
        self.fields['currency'].widget.attrs['class'] = 'form-control'
        self.fields['currency_symbol'].widget.attrs['class'] = 'form-control'
        self.fields['tld'].widget.attrs['class'] = 'form-control'
        self.fields['native'].widget.attrs['class'] = 'form-control'
        self.fields['region'].widget.attrs['class'] = 'form-control'
        self.fields['sub_region'].widget.attrs['class'] = 'form-control'
        self.fields['timezones'].widget.attrs['class'] = 'form-control'
        self.fields['latitude'].widget.attrs['class'] = 'form-control'
        self.fields['longitude'].widget.attrs['class'] = 'form-control'
        self.fields['emoji'].widget.attrs['class'] = 'form-control'
        self.fields['emojiU'].widget.attrs['class'] = 'form-control'
        self.fields['status'].widget.attrs['class'] = 'form-select'
        for field in self.fields:
            self.fields[field].widget.attrs['placeholder'] = 'Provide Detail'


class StateForm(forms.ModelForm):
    class Meta:
        model = State
        fields = ('name', 'country', 'state_code', 'type', 'latitude', 'longitude', 'status')

    def __init__(self, *args, **kwargs):
        super(StateForm, self).__init__(*args, **kwargs)
        self.fields['name'].widget.attrs['class'] = 'form-control'
        self.fields['country'].widget.attrs['class'] = 'form-select'
        self.fields['country'].widget.attrs['data-control'] = 'select2'
        self.fields['state_code'].widget.attrs['class'] = 'form-control'
        self.fields['type'].widget.attrs['class'] = 'form-control'
        self.fields['latitude'].widget.attrs['class'] = 'form-control'
        self.fields['longitude'].widget.attrs['class'] = 'form-control'
        self.fields['status'].widget.attrs['class'] = 'form-select'
        for field in self.fields:
            self.fields[field].widget.attrs['placeholder'] = 'Provide Detail'


class CityForm(forms.ModelForm):
    class Meta:
        model = City
        fields = ('name', 'state', 'country', 'latitude', 'longitude', 'status')

    def __init__(self, *args, **kwargs):
        super(CityForm, self).__init__(*args, **kwargs)
        self.fields['country'].widget.attrs['class'] = 'form-select'
        self.fields['country'].widget.attrs['data-control'] = 'select2'
        self.fields['state'].widget.attrs['class'] = 'form-select'
        self.fields['state'].queryset = State.objects.none()
        self.fields['state'].widget.attrs['data-control'] = 'select2'
        self.fields['latitude'].widget.attrs['class'] = 'form-control'
        self.fields['longitude'].widget.attrs['class'] = 'form-control'
        self.fields['name'].widget.attrs['class'] = 'form-control'
        self.fields['status'].widget.attrs['class'] = 'form-select'
        for field in self.fields:
            self.fields[field].widget.attrs['placeholder'] = 'Provide Detail'
            self.fields[field].widget.attrs['data-placeholder'] = 'Select an option'

        if 'country' in self.data:
            try:
                country_id = int(self.data.get('country'))
                self.fields['state'].queryset = State.objects.filter(country_id=country_id).order_by('name')
            except (ValueError, TypeError):
                pass  # invalid input from the client; ignore and fallback to empty state queryset
        elif self.instance.pk:
            self.fields['state'].queryset = self.instance.country.state_set.order_by('name')


class TwilioForm(forms.ModelForm):
    class Meta:
        model = Twilio
        fields = ('accountSID', 'authToken', 'phoneNumber', 'status')

    def __init__(self, *args, **kwargs):
        super(TwilioForm, self).__init__(*args, **kwargs)
        self.fields['accountSID'].widget.attrs['class'] = 'form-control'
        self.fields['authToken'].widget.attrs['class'] = 'form-control'
        self.fields['phoneNumber'].widget.attrs['class'] = 'form-control'
        self.fields['status'].widget.attrs['class'] = 'form-select'
        for field in self.fields:
            self.fields[field].widget.attrs['placeholder'] = 'Provide Detail'


class MembershipForm(forms.ModelForm):
    class Meta:
        model = Membership
        fields = ('title', 'type', 'duration', 'price', 'status')

    def __init__(self, *args, **kwargs):
        super(MembershipForm, self).__init__(*args, **kwargs)
        self.fields['title'].widget.attrs['class'] = 'form-control'
        self.fields['type'].widget.attrs['class'] = 'form-select'
        self.fields['duration'].widget.attrs['class'] = 'form-control'
        self.fields['price'].widget.attrs['class'] = 'form-control'
        self.fields['status'].widget.attrs['class'] = 'form-select'
        for field in self.fields:
            self.fields[field].widget.attrs['placeholder'] = 'Provide Detail'