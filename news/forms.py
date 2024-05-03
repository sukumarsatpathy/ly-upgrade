from django import forms
from django.contrib.auth import get_user_model
from .models import News


User = get_user_model()


class NewsForm(forms.ModelForm):

    class Meta:
        model = News
        fields = ['title', 'description', 'image', 'location', 'meta_title', 'meta_description', 'status']

    def __init__(self, *args, **kwargs):
        super(NewsForm, self).__init__(*args, **kwargs)
        self.fields['title'].widget.attrs['class'] = 'form-control'
        self.fields['description'].widget.attrs['class'] = 'form-control'
        self.fields['image'].widget.attrs['class'] = 'form-control'
        self.fields['location'].widget.attrs['class'] = 'form-control'
        self.fields['meta_title'].widget.attrs['class'] = 'form-control'
        self.fields['meta_title'].widget.attrs['id'] = 'maxlength_mt'
        self.fields['meta_description'].widget.attrs['class'] = 'form-control'
        self.fields['meta_description'].widget.attrs['id'] = 'maxlength_md'
        self.fields['status'].widget.attrs['class'] = 'form-select'
        for field in self.fields:
            self.fields[field].widget.attrs['placeholder'] = 'Provide Detail'