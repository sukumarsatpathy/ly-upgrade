from django import forms
from smart_selects.db_fields import ChainedForeignKey
from settings.models import State, City, Country
from .models import Training, TrainingCategory
from django.contrib.auth import get_user_model
from ckeditor.widgets import CKEditorWidget
from django.utils.translation import gettext_lazy as _

class DateInput(forms.DateInput):
    input_type = 'date'


class AddTrainingForm(forms.ModelForm):
    description = forms.CharField(widget=CKEditorWidget(attrs={'cols': 80, 'rows': 30}))
    state = ChainedForeignKey(State, chained_field="country", chained_model_field="country", show_all=False,
                              auto_choose=True, null=True)
    city = ChainedForeignKey(City, chained_field="state", chained_model_field="state", show_all=False, auto_choose=True,
                             null=True)
    start_date = forms.DateField(widget=DateInput(attrs={'class': 'form-group'}))
    end_date = forms.DateField(widget=DateInput(attrs={'class': 'form-group'}))

    class Meta:
        model = Training
        fields = (
            'category_title', 'description', 'trainer_name', 'author', 'email', 'contact_no',
            'img1', 'img2', 'img3', 'img4', 'location', 'country', 'state',
            'city', 'start_date', 'end_date', 'video_url', 'video_url_1', 'video_url_2', 'video_url_3', 'video_url_4')
        widgets = {
            'category_title': forms.Select(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'trainer_name': forms.TextInput(attrs={'class': 'form-control', 'id': 'trainer-name'}),
            'author': forms.TextInput(attrs={'class': 'form-control', 'value': '', 'id': 'author', 'type': 'hidden'}),
            'email': forms.TextInput(attrs={'class': 'form-control', 'value': '', 'id': 'user-email'}),
            'contact_no': forms.TextInput(attrs={'class': 'form-control', 'value': '', 'id': 'user-contact'}),
            'video_url': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'Provide your title video URL (Optional)'}),
            'video_url_1': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'Provide your video URL 1 (Optional)'}),
            'video_url_2': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'Provide your video URL 2 (Optional)'}),
            'video_url_3': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'Provide your video URL 3 (Optional)'}),
            'video_url_4': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'Provide your video URL 4 (Optional)'}),
            'location': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Provide your training location detail'}),
        }


class EditTrainingForm(forms.ModelForm):
    description = forms.CharField(widget=CKEditorWidget(attrs={'cols': 80, 'rows': 30}))
    state = ChainedForeignKey(State, chained_field="country", chained_model_field="country", show_all=False,
                              auto_choose=True, null=True)
    city = ChainedForeignKey(City, chained_field="state", chained_model_field="state", show_all=False, auto_choose=True,
                             null=True)
    start_date = forms.DateField(widget=DateInput(attrs={'class': 'form-group'}))
    end_date = forms.DateField(widget=DateInput(attrs={'class': 'form-group'}))

    class Meta:
        model = Training
        fields = (
            'category_title', 'description', 'trainer_name', 'email', 'contact_no',
            'img1', 'img2', 'img3', 'img4', 'location', 'country', 'state', 'city',
            'start_date', 'end_date', 'video_url', 'video_url_1', 'video_url_2', 'video_url_3', 'video_url_4')
        widgets = {
            'category_title': forms.Select(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'trainer_name': forms.TextInput(attrs={'class': 'form-control', 'id': 'trainer-name'}),
            'email': forms.TextInput(attrs={'class': 'form-control', 'value': '', 'id': 'user-email'}),
            'contact_no': forms.TextInput(attrs={'class': 'form-control', 'value': '', 'id': 'user-contact'}),
            'video_url': forms.URLInput(attrs={'class': 'form-control'}),
            'video_url_1': forms.URLInput(attrs={'class': 'form-control'}),
            'video_url_2': forms.URLInput(attrs={'class': 'form-control'}),
            'video_url_3': forms.URLInput(attrs={'class': 'form-control'}),
            'video_url_4': forms.URLInput(attrs={'class': 'form-control'}),
            'location': forms.TextInput(attrs={'class': 'form-control'}),
        }


User = get_user_model()


def get_category_choices():
    cat_List = []
    cat_List.append(('0', '--------'), )
    for cat in TrainingCategory.objects.all():
        cat = (cat.id, cat.title)
        cat_List.append(cat)
    return cat_List


class UserForm(forms.Form):
    # category_title = forms.ChoiceField(widget=forms.Select(attrs={'required': 'required'}), choices=get_category_choices(), initial='0', required=True )
    state = forms.ChoiceField(widget=forms.Select())
    city = forms.ChoiceField(widget=forms.Select())
    country = forms.ChoiceField(widget=forms.Select())

 
#   def __init__(self, *args, **kwargs):
 #       super(UserForm, self).__init__(*args, **kwargs) 
  #      self.fields['country'].queryset = Country.objects.none()
   #     self.fields['state'].queryset = State.objects.none()
    #    self.fields['country'].queryset = City.objects.none()

    
class TrainingForm(forms.ModelForm):
    author_name = forms.CharField(label=_('Author Name'), required=False)

    class Meta:
        model = Training
        fields = ['category_title', 'description', 'trainer_name', 'author', 'email', 'contact_no',
                    'img1', 'img2', 'img3', 'img4', 'location', 'country', 'state', 'city', 'start_date', 'end_date',
                  'video_url', 'video_url_1', 'video_url_2', 'video_url_3', 'video_url_4']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        if user and not user.is_superuser:
            # For non-superusers, hide the author field and set the initial value
            self.fields['author'].initial = user.id
            self.fields['author'].widget = forms.HiddenInput()
        elif user and user.is_superuser:
            # For superadmins, ensure the author field uses Select2 for enhanced UI
            self.fields['author'].queryset = User.objects.all()
            self.fields['author'].widget.attrs.update({
                'class': 'form-select',
                'data-control': 'select2',
                'id': 'author-select'
            })
            self.fields['author'].required = True

        # Common attributes for all fields, excluding author field modifications for non-superusers
        common_fields = ['description', 'trainer_name', 'author', 'email', 'contact_no',
                    'img1', 'img2', 'img3', 'img4', 'location',  'start_date', 'end_date',
                  'video_url', 'video_url_1', 'video_url_2', 'video_url_3', 'video_url_4']
        for field_name in common_fields:
            if field_name in self.fields:
                self.fields[field_name].widget.attrs['class'] = 'form-control'

        for field_name in self.fields:
            if field_name in ['category_title', 'country', 'state', 'city']:
                self.fields[field_name].widget.attrs['class'] = 'form-select'
            if isinstance(self.fields[field_name].widget, forms.TextInput):
                self.fields[field_name].widget.attrs['placeholder'] = 'Provide Detail'


class TrainingEditForm(forms.ModelForm):
    class Meta:
        model = Training
        fields = ('category_title', 'description', 'trainer_name', 'author', 'email', 'contact_no',
                    'img1', 'img2', 'img3', 'img4', 'location', 'country', 'state', 'city', 'start_date', 'end_date',
                  'video_url', 'video_url_1', 'video_url_2', 'video_url_3', 'video_url_4')

    def __init__(self, *args, **kwargs):
        super(TrainingEditForm, self).__init__(*args, **kwargs)
        self.fields['category_title'].widget.attrs['class'] = 'form-select'
        self.fields['author'].widget.attrs['class'] = 'form-control'
        self.fields['trainer_name'].widget.attrs['class'] = 'form-control'
        self.fields['description'].widget.attrs['class'] = 'form-control'
        for field in self.fields:
            self.fields[field].widget.attrs['placeholder'] = 'Provide Detail'


# class TrainingAddressForm(forms.ModelForm):
#     class Meta:
#         model = TrainingAddress
#         fields = ('location', 'country', 'state', 'city')
#
#     def __init__(self, *args, **kwargs):
#         super(TrainingAddressForm, self).__init__(*args, **kwargs)
#         self.fields['location'].widget.attrs['class'] = 'form-control'
#         self.fields['country'].widget.attrs['class'] = 'form-select'
#         self.fields['country'].widget.attrs['data-control'] = 'select2'
#         self.fields['state'].widget.attrs['class'] = 'form-select'
#         self.fields['state'].queryset = State.objects.none()
#         self.fields['state'].widget.attrs['data-control'] = 'select2'
#         self.fields['city'].widget.attrs['class'] = 'form-select'
#         self.fields['city'].queryset = City.objects.none()
#         self.fields['city'].widget.attrs['data-control'] = 'select2'
#         for field in self.fields:
#             self.fields[field].widget.attrs['placeholder'] = 'Provide Detail'
#             self.fields[field].widget.attrs['data-placeholder'] = 'Select an Option'
#
#         if 'country' in self.data:
#             try:
#                 country_id = int(self.data.get('country'))
#                 self.fields['state'].queryset = State.objects.filter(country_id=country_id).order_by('name')
#             except (ValueError, TypeError):
#                 pass  # invalid input from the client; ignore and fallback to empty state queryset
#         elif self.instance.pk and self.instance.country:
#             self.fields['state'].queryset = self.instance.country.state_set.order_by('name')
#
#         if 'state' in self.data:
#             try:
#                 state_id = int(self.data.get('state'))
#                 self.fields['city'].queryset = City.objects.filter(state_id=state_id).order_by('name')
#             except (ValueError, TypeError):
#                 pass  # invalid input from the client; ignore and fallback to empty state queryset
#         elif self.instance.pk and self.instance.state:
#             self.fields['city'].queryset = self.instance.state.city_set.order_by('name')