from django import forms
from django.contrib.auth import get_user_model
from image_cropping import ImageCropField, ImageRatioField
from subscription.models import Subscription
from tokens.models import LeaderUniqueToken, TeacherUniqueToken
from settings.models import State, City

User = get_user_model()

services = (
    ('Certified Leader Training', 'Certified Leader Training'),
    ('Certified Teacher Training', 'Certified Teacher Training'),
    ('Social Laughter Clubs', 'Social Laughter Clubs'),
    ('Free Public Seminars', 'Free Public Seminars'),
    ('Corporate Programs', 'Corporate Programs'),
    ('Senior Center Session', 'Senior Center Session'),
    ('Special Need Groups', 'Special Need Groups'),
)


class EditProfileForm(forms.ModelForm):
    profile_pic = ImageCropField(blank=True, upload_to='members/%Y/%m/%d/')
    pp_cropped = ImageRatioField('profile_pic', '300x300', size_warning=True)

    class Meta:
        model = User
        fields = (
            'first_name', 'last_name', 'email', 'contact_number', 'trained_by', 'services', 'user_type', 'profile_pic',
            'country', 'state', 'city', 'description', 'website_url', 'facebook_url', 'youtube_url', 'linkedin_url',
            'video_url_1', 'video_url_2', 'video_url_3', 'video_url_4', 'basic_learning_course',
            'certified_leader_training', 'certified_teacher_training', 'is_masked'
        )

    def __init__(self, *args, **kwargs):
        super(EditProfileForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs['class'] = 'form-control'
        self.fields['last_name'].widget.attrs['class'] = 'form-control'
        self.fields['email'].widget.attrs['class'] = 'form-control'
        self.fields['contact_number'].widget.attrs['class'] = 'form-control'
        self.fields['trained_by'].widget.attrs['class'] = 'form-control'
        self.fields['services'].widget.attrs['class'] = 'form-control'
        self.fields['user_type'].widget.attrs['class'] = 'form-select'
        self.fields['user_type'].widget.attrs['data-control'] = 'select2'
        self.fields['country'].widget.attrs['class'] = 'form-select'
        self.fields['country'].widget.attrs['data-control'] = 'select2'
        self.fields['state'].widget.attrs['class'] = 'form-select'
        self.fields['state'].queryset = State.objects.none()
        self.fields['state'].widget.attrs['data-control'] = 'select2'
        self.fields['city'].widget.attrs['class'] = 'form-select'
        self.fields['city'].queryset = City.objects.none()
        self.fields['city'].widget.attrs['data-control'] = 'select2'
        self.fields['description'].widget.attrs['class'] = 'form-control'
        self.fields['website_url'].widget.attrs['class'] = 'form-control'
        self.fields['facebook_url'].widget.attrs['class'] = 'form-control'
        self.fields['youtube_url'].widget.attrs['class'] = 'form-control'
        self.fields['linkedin_url'].widget.attrs['class'] = 'form-control'
        self.fields['video_url_1'].widget.attrs['class'] = 'form-control'
        self.fields['video_url_2'].widget.attrs['class'] = 'form-control'
        self.fields['video_url_3'].widget.attrs['class'] = 'form-control'
        self.fields['video_url_4'].widget.attrs['class'] = 'form-control'
        self.fields['basic_learning_course'].widget.attrs['class'] = 'form-control'
        self.fields['certified_leader_training'].widget.attrs['class'] = 'form-control'
        self.fields['certified_teacher_training'].widget.attrs['class'] = 'form-control'
        self.fields['is_masked'].widget.attrs['class'] = 'form-check'
        for field in self.fields:
            self.fields[field].widget.attrs['placeholder'] = 'Provide Detail'
            self.fields[field].widget.attrs['data-placeholder'] = 'Select an option'

        if 'country' in self.data:
            try:
                country_id = int(self.data.get('country'))
                self.fields['state'].queryset = State.objects.filter(country_id=country_id).order_by('name')
            except (ValueError, TypeError):
                pass  # invalid input from the client; ignore and fallback to empty state queryset
        elif self.instance.pk and self.instance.country:
            self.fields['state'].queryset = self.instance.country.state_set.order_by('name')

        if 'state' in self.data:
            try:
                state_id = int(self.data.get('state'))
                self.fields['city'].queryset = City.objects.filter(state_id=state_id).order_by('name')
            except (ValueError, TypeError):
                pass  # invalid input from the client; ignore and fallback to empty state queryset
        elif self.instance.pk and self.instance.state:
            self.fields['city'].queryset = self.instance.state.city_set.order_by('name')


class UserMembershipForm(forms.ModelForm):
    class Meta:
        model = Subscription
        fields = ['user', 'membership', 'startDate', 'endDate', 'status']

    def clean(self):
        return self.cleaned_data


class SelfLeaderCreationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Enter Your Password', 'class': 'form-control'}))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Retype Your Password', 'class': 'form-control'}))

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'password']

    def clean(self):
        cleaned_data = super(SelfLeaderCreationForm, self).clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')
        if password != confirm_password:
            raise forms.ValidationError("Password does not match!")

    def __init__(self, *args, **kwargs):
        super(SelfLeaderCreationForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs['placeholder'] = 'Enter First Name'
        self.fields['last_name'].widget.attrs['placeholder'] = 'Enter Last Name'
        self.fields['email'].widget.attrs['placeholder'] = 'Enter Email Address'
        self.fields['email'].widget.attrs['style'] = 'text-transform:lowercase;'
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control form-control-lg'


class LeaderUniqueTokenForm(forms.ModelForm):
    class Meta:
        model = LeaderUniqueToken
        fields = ['user', 'amount', 'quantity', 'token']


class TeacherUniqueTokenForm(forms.ModelForm):
    class Meta:
        model = TeacherUniqueToken
        fields = ['user', 'amount', 'quantity', 'token']


class SelfTeacherCreationForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ['email',]

    # def clean(self):
    #     cleaned_data = super(SelfTeacherCreationForm, self).clean()
    #     password = cleaned_data.get('password')
    #     confirm_password = cleaned_data.get('confirm_password')
    #     if password != confirm_password:
    #         raise forms.ValidationError("Password does not match!")

    def __init__(self, *args, **kwargs):
        super(SelfTeacherCreationForm, self).__init__(*args, **kwargs)
        self.fields['email'].widget.attrs['placeholder'] = 'Enter Email Address'
        self.fields['email'].widget.attrs['style'] = 'text-transform:lowercase;'
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control form-control-lg'