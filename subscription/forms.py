from django import forms
from django.contrib.auth import get_user_model
from .models import Subscription

User = get_user_model()


class SubscriptionForm(forms.ModelForm):
    class Meta:
        model = Subscription
        fields = ['user', 'membership', 'startDate', 'endDate', 'status']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(SubscriptionForm, self).__init__(*args, **kwargs)

        if self.instance and self.instance.pk:
            self.fields['user'].disabled = True  # Disable user field for existing instances

        if user and user.is_superuser:
            # For superadmins, ensure the author field uses Select2 for enhanced UI
            self.fields['author'].queryset = User.objects.all()
            self.fields['author'].widget.attrs.update({
                'class': 'form-select',
                'data-control': 'select2',
                'id': 'author-select'
            })
            self.fields['author'].required = True

        self.fields['startDate'].widget.attrs.update(
            {'id': 'startDate', 'class': 'form-control datetimepicker-input', 'data-target': '#startDate'})
        self.fields['endDate'].widget.attrs.update(
            {'id': 'endDate', 'class': 'form-control datetimepicker-input', 'data-target': '#endDate'})

        for field_name in self.fields:
            if field_name in ['user', 'membership', 'status']:
                self.fields[field_name].widget.attrs['class'] = 'form-select'
                self.fields[field_name].widget.attrs['data-control'] = 'select2'
            if isinstance(self.fields[field_name].widget, forms.TextInput):
                self.fields[field_name].widget.attrs['placeholder'] = 'Provide Detail'