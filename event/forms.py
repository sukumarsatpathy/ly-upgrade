from django import forms
from smart_selects.db_fields import ChainedForeignKey
from ckeditor.widgets import CKEditorWidget
from settings.models import Country, State, City
from .models import Event


class DateInput(forms.DateInput):
    input_type = 'date'


class AddEventForm(forms.ModelForm):
    description = forms.CharField(widget=CKEditorWidget(attrs={'cols': 80, 'rows': 30}))
    state = ChainedForeignKey(State, chained_field="country", chained_model_field="country", show_all=False,
                              auto_choose=True, null=True)
    city = ChainedForeignKey(City, chained_field="state", chained_model_field="state", show_all=False, auto_choose=True,
                             null=True)
    start_date = forms.DateField(widget=DateInput())
    end_date = forms.DateField(widget=DateInput())

    class Meta:
        model = Event
        fields = (
            'category', 'description', 'organiser_name', 'author', 'email', 'contact_no', 'location',
            'country', 'state', 'city', 'start_date', 'end_date', 'website_url', 'img1', 'img2', 'video1', 'video2')
        widgets = {
            'category': forms.Select(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'organiser_name': forms.TextInput(attrs={'class': 'form-control', 'id': 'organiser-name'}),
            'author': forms.TextInput(attrs={'class': 'form-control', 'value': '', 'id': 'author', 'type': 'hidden'}),
            'email': forms.TextInput(attrs={'class': 'form-control', 'value': '', 'id': 'user-email'}),
            'contact_no': forms.TextInput(attrs={'class': 'form-control', 'value': '', 'placeholder': 'Provide your Contact Number (Optional)' }),
            'location': forms.TextInput(attrs={'class': 'form-control'}),
            'website_url': forms.URLInput(attrs={'class': 'form-control', 'value': '', 'id': 'user-website'}),
            'video1': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'Provide your video link 1 (Optional)'}),
            'video2': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'Provide your video link 2 (Optional)'}),
        }


class EditEventForm(forms.ModelForm):
    description = forms.CharField(widget=CKEditorWidget(attrs={'cols': 80, 'rows': 30}))
    state = ChainedForeignKey(State, chained_field="country", chained_model_field="country", show_all=False,
                              auto_choose=True, null=True)
    city = ChainedForeignKey(City, chained_field="state", chained_model_field="state", show_all=False, auto_choose=True,
                             null=True)
    start_date = forms.DateField(widget=DateInput(attrs={'class': 'fc-datepicker'}))
    end_date = forms.DateField(widget=DateInput(attrs={'class': 'fc-datepicker'}))

    class Meta:
        model = Event
        fields = (
            'category', 'description', 'organiser_name', 'email', 'contact_no', 'website_url', 'location',
            'country', 'state', 'city', 'start_date', 'end_date', 'img1', 'img2', 'video1', 'video2')
        widgets = {
            'category': forms.Select(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'organiser_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.TextInput(attrs={'class': 'form-control'}),
            'contact_no': forms.TextInput(attrs={'class': 'form-control', 'value': '', 'placeholder': 'Provide your Contact Number (Optional)' }),
            'location': forms.TextInput(attrs={'class': 'form-control'}),
            'website_url': forms.URLInput(attrs={'class': 'form-control'}),
            'video1': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'Provide your video link 1 (Optional)'}),
            'video2': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'Provide your video link 2 (Optional)'}),
        }


class EventFinderForm(forms.ModelForm):

    category= forms.ChoiceField(widget = forms.Select(), 
                 choices = ([
     ('--', '--------'), 
     ('Free Public Seminar', 'Free Public Seminar'),
     ('Workshop', 'Workshop'),
     ('Conference', 'Conference'),
     ('World Laughter Day', 'World Laughter Day'), ]), initial='--', required = True)
    state =  forms.ChoiceField(widget = forms.Select())
    city =  forms.ChoiceField(widget = forms.Select())
    country =  forms.ChoiceField(widget = forms.Select()) 
   
    # def __init__(self, *args, **kwargs):
    #     super(EventFinderForm, self).__init__(*args, **kwargs) 
    #     self.fields['country'].queryset = Country.objects.none()
    #     self.fields['state'].queryset = State.objects.none()
    #     self.fields['city'].queryset = City.objects.none()

 
    class Meta:
    
        model = Event
        fields = ('category','country','state', 'city')
