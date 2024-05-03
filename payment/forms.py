from django import forms
from .models import ly2Transaction, blcTransaction, cttTransaction, indTraining, wcTransaction


class LY2Form(forms.ModelForm):
    class Meta:
        model = ly2Transaction
        fields = ['full_name', 'email', 'address', 'city', 'state', 'country', 'postalcode', 'price', 'contact', 'information']


class blcForm(forms.ModelForm):
    class Meta:
        model = blcTransaction
        fields = ['course', 'full_name', 'email', 'address', 'city', 'state', 'country', 'postalcode', 'price', 'contact', 'information']


class cttForm(forms.ModelForm):
    class Meta:
        model = cttTransaction
        fields = ['full_name', 'email', 'address', 'city', 'state', 'country', 'postalcode', 'price', 'contact', 'information']


class blcIndForm(forms.ModelForm):
    class Meta:
        model = indTraining
        fields = ['full_name', 'email', 'price', 'contact', 'token', 'instamojo_response']


class wcForm(forms.ModelForm):
    class Meta:
        model = wcTransaction
        fields = ['full_name', 'email', 'address', 'city', 'state', 'country', 'postalcode', 'price', 'contact', 'information']

