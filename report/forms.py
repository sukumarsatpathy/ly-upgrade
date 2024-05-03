from django import forms
from .models import Contact, LYTourEnquiry, ZoomLCEnquiry


class ContactForm(forms.ModelForm):

    class Meta:
        model = Contact
        fields = ['full_name', 'email', 'contact', 'country', 'message']

    def __init__(self, *args, **kwargs):
        super(ContactForm, self).__init__(*args, **kwargs)
        self.fields['full_name'].widget.attrs['placeholder'] = 'Full Name'
        self.fields['email'].widget.attrs['placeholder'] = 'Email Name'
        self.fields['contact'].widget.attrs['placeholder'] = 'Contact No'
        self.fields['country'].widget.attrs['placeholder'] = 'Country Name'
        self.fields['message'].widget.attrs['placeholder'] = 'Message'
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control form-control-lg'


class InfoBookletForm(forms.ModelForm):

    class Meta:
        model = Contact
        fields = ['full_name', 'email', 'country']

    def __init__(self, *args, **kwargs):
        super(InfoBookletForm, self).__init__(*args, **kwargs)
        self.fields['full_name'].widget.attrs['placeholder'] = 'Full Name'
        self.fields['email'].widget.attrs['placeholder'] = 'Email Name'
        self.fields['country'].widget.attrs['placeholder'] = 'Country Name'
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'


class LYTourEnquiryForm(forms.ModelForm):

    class Meta:
        model = LYTourEnquiry
        fields = ['full_name', 'email', 'contact', 'category']

    def __init__(self, *args, **kwargs):
        super(LYTourEnquiryForm, self).__init__(*args, **kwargs)
        self.fields['full_name'].widget.attrs['placeholder'] = 'Full Name'
        self.fields['email'].widget.attrs['placeholder'] = 'Email Name'
        self.fields['contact'].widget.attrs['placeholder'] = 'Phone No'
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'


class ZoomLCForm(forms.ModelForm):

    class Meta:
        model = ZoomLCEnquiry
        fields = ['full_name', 'email', 'contact', 'occupation', 'country']

    def __init__(self, *args, **kwargs):
        super(ZoomLCForm, self).__init__(*args, **kwargs)
        self.fields['full_name'].widget.attrs['placeholder'] = 'Full Name'
        self.fields['email'].widget.attrs['placeholder'] = 'Email Addres'
        self.fields['contact'].widget.attrs['placeholder'] = 'Phone No'
        self.fields['occupation'].widget.attrs['placeholder'] = 'Occupation'
        self.fields['country'].widget.attrs['placeholder'] = 'Country Name'
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control form-control-lg'

    def clean_country_data(self):
        country_data = self.cleaned_data.get('country')
        if '|' not in country_data:
            raise forms.ValidationError("Invalid country data format.")
        return country_data