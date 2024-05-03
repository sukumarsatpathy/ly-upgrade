from accounts.models import Category
from django import forms
from smart_selects.db_fields import ChainedForeignKey
from ckeditor.widgets import CKEditorWidget
from settings.models import Country, State, City
from .models import Club, ClubCategory


class ClubForm(forms.ModelForm):
    description = forms.CharField(widget=CKEditorWidget(attrs={'cols': 80, 'rows': 30}))
    state = ChainedForeignKey(State, chained_field="country", chained_model_field="country", show_all=False,
                              auto_choose=True, null=True)
    city = ChainedForeignKey(City, chained_field="state", chained_model_field="state", show_all=False, auto_choose=True,
                             null=True)

    class Meta:
        model = Club
        fields = (
            'category_title', 'title', 'description', 'email', 'frequency', 'author', 'contact_no',
            'contact_name', 'location', 'country', 'state', 'city', 'image1', 'image2', 'video1', 'video2')
        widgets = {
            'category_title': forms.Select(attrs={'class': 'form-control'}),
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'email': forms.TextInput(attrs={'class': 'form-control', 'value': '', 'id': 'user-email'}),
            'frequency': forms.TextInput(attrs={'class': 'form-control'}),
            'author': forms.TextInput(attrs={'class': 'form-control', 'value': '', 'id': 'author', 'type': 'hidden'}),
            'contact_no': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Provide your contact number (Optional)'}),
            'contact_name': forms.TextInput(attrs={'class': 'form-control', 'id': 'user-fullname'}),
            'location': forms.TextInput(attrs={'class': 'form-control'}),
            'video1': forms.URLInput(attrs={'class': 'form-control', 'value': ''}),
            'video2': forms.URLInput(attrs={'class': 'form-control', 'value': ''}),
        }


def get_category_choices():
    cat_List = []
    cat_List.append(('0', '--------'),)
    for cat in ClubCategory.objects.all():
        cat = (cat.id, cat.title)
        cat_List.append(cat)
    return cat_List


class ClubFinderForm(forms.Form):
    # category_title = forms.ChoiceField(widget=forms.Select(), choices=get_category_choices(), initial='0', required=True )
    state = forms.ChoiceField(widget=forms.Select())
    city = forms.ChoiceField(widget=forms.Select())
    country = forms.ChoiceField(widget=forms.Select())

    def __init__(self, *args, **kwargs):
        super(ClubFinderForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Club
        fields = ('category_title', 'country', 'state', 'city')
