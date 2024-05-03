from django import forms
from django.contrib.auth import get_user_model
from .models import Testimonial


User = get_user_model()


class TestimonialForm(forms.ModelForm):

    class Meta:
        model = Testimonial
        fields = ['title', 'description', 'image', 'location', 'publisher', 'meta_title', 'meta_description', 'status', 'author']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Provide Details'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Provide Details'}),
            'image': forms.FileInput(attrs={'class': 'form-control'}),
            'location': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Provide Details'}),
            'publisher': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Provide Details'}),
            'meta_title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Provide Details', 'id': 'maxlength_mt'}),
            'meta_description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Provide Details', 'id': 'maxlength_md'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
            'author': forms.Select(attrs={'class': 'form-select'}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(TestimonialForm, self).__init__(*args, **kwargs)

        # Conditionally display 'status' field only for superusers
        if not user.is_superuser:
            self.fields.pop('status', None)

        # Set initial values for 'publisher' and 'location' for non-superusers on creation
        if not self.instance.pk and not user.is_superuser:
            self.fields['publisher'].initial = user.get_full_name()
            self.fields['location'].initial = user.profile.country if hasattr(user, 'profile') else ''

        # For superusers, ensure all fields are left as is (potentially blank for some)
        if user and user.is_superuser:
            self.fields['author'].queryset = User.objects.all()
            # Ensure initial value is set correctly when editing
            if self.instance and self.instance.pk and self.instance.author_id:
                # Directly setting the initial value to the author's ID
                self.fields['author'].initial = self.instance.author_id
            self.fields['author'].required = True
            self.fields['publisher'].required = True  # As an example, adjust based on your model
            self.fields['location'].required = True
            self.fields['status'].required = False
            # No need to pre-populate fields for superusers

        # For regular users, pre-populate publisher and location
        elif user and not user.is_superuser:
            self.fields['publisher'].initial = user.get_full_name()
            # Assuming the user has a related profile with a country attribute
            if hasattr(user, 'UserAddress') and user.UserAddress.country:
                self.fields['location'].initial = user.UserAddress.country.name
            # Hide or disable the author field if you want to set it automatically to the logged-in user
            if 'author' in self.fields:
                self.fields['author'].initial = user.id
                self.fields['author'].widget = forms.HiddenInput()