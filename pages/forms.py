from django import forms
from . models import GetInvolved, Diary, laughterBlogsCat, laughterBlogs, generalResearch
from django.contrib.auth import get_user_model

User = get_user_model()

class GetInvolvedForm(forms.ModelForm):

    class Meta:
        model = GetInvolved
        fields = ['title', 'description', 'image', 'btn_name', 'url', 'status']

    def __init__(self, *args, **kwargs):
        super(GetInvolvedForm, self).__init__(*args, **kwargs)
        self.fields['title'].widget.attrs['class'] = 'form-control'
        self.fields['description'].widget.attrs['class'] = 'form-control'
        self.fields['image'].widget.attrs['class'] = 'form-control'
        self.fields['btn_name'].widget.attrs['class'] = 'form-control'
        self.fields['url'].widget.attrs['class'] = 'form-control'
        self.fields['status'].widget.attrs['class'] = 'form-select'
        self.fields['status'].widget.attrs['data-control'] = 'select2'
        for field in self.fields:
            self.fields[field].widget.attrs['placeholder'] = 'Provide Detail'


class DiaryForm(forms.ModelForm):

    class Meta:
        model = Diary
        fields = ['title', 'description', 'image', 'status']

    def __init__(self, *args, **kwargs):
        super(DiaryForm, self).__init__(*args, **kwargs)
        self.fields['title'].widget.attrs['class'] = 'form-control'
        self.fields['description'].widget.attrs['class'] = 'form-control'
        self.fields['image'].widget.attrs['class'] = 'form-control'
        self.fields['status'].widget.attrs['class'] = 'form-select'
        for field in self.fields:
            self.fields[field].widget.attrs['placeholder'] = 'Provide Detail'

class BlogsForm(forms.ModelForm):

    class Meta:
        model = laughterBlogs
        fields = ['category', 'title', 'description', 'image', 'meta_title', 'meta_description', 'meta_keywords', 'status']

    def __init__(self, *args, **kwargs):
        super(BlogsForm, self).__init__(*args, **kwargs)
        self.fields['category'].widget.attrs['class'] = 'form-select'
        self.fields['category'].widget.attrs['data-control'] = 'select2'
        self.fields['category'].queryset = laughterBlogsCat.objects.all() | laughterBlogsCat.objects.none()
        self.fields['category'].widget.choices = [('add_new', 'Add Now')] + list(self.fields['category'].widget.choices)
        self.fields['title'].widget.attrs['class'] = 'form-control'
        self.fields['description'].widget.attrs['class'] = 'form-control'
        self.fields['image'].widget.attrs['class'] = 'form-control'
        self.fields['meta_title'].widget.attrs['class'] = 'form-control'
        self.fields['meta_description'].widget.attrs['class'] = 'form-control'
        self.fields['meta_keywords'].widget.attrs['class'] = 'form-control'
        self.fields['status'].widget.attrs['class'] = 'form-select'
        for field in self.fields:
            self.fields[field].widget.attrs['placeholder'] = 'Provide Detail'


class gResearchForm(forms.ModelForm):
    class Meta:
        model = generalResearch
        fields = ['title', 'description', 'image', 'status']

    def __init__(self, *args, **kwargs):
        super(gResearchForm, self).__init__(*args, **kwargs)
        self.fields['title'].widget.attrs['class'] = 'form-control'
        self.fields['description'].widget.attrs['class'] = 'form-control'
        self.fields['image'].widget.attrs['class'] = 'form-control'
        self.fields['status'].widget.attrs['class'] = 'form-select'
        for field in self.fields:
            self.fields[field].widget.attrs['placeholder'] = 'Provide Detail'


class UserForm(forms.Form):
    user_type = forms.ChoiceField(
        widget=forms.Select(),
        choices=[
            ('--', '--------'),
            ('Certified Leader', 'Certified Leader'),
            ('Certified Teacher', 'Certified Teacher'),
            ('Certified Master Trainer', 'Certified Master Trainer'),
        ],
        initial='--',
        required=True
    )
    country = forms.ChoiceField(widget=forms.Select(), choices=[('', 'Select Country')], required=False)
    state = forms.ChoiceField(widget=forms.Select(), choices=[('', 'Select State')], required=False)
    city = forms.ChoiceField(widget=forms.Select(), choices=[('', 'Select City')], required=False)
