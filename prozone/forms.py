from django import forms
from . models import ProDiary, ProResearch, ProVideos, ProDownloads, ProPhotosCat, ProPhotos, ProQuotes


class ProDiaryForm(forms.ModelForm):

    class Meta:
        model = ProDiary
        fields = ['title', 'description', 'image', 'status']

    def __init__(self, *args, **kwargs):
        super(ProDiaryForm, self).__init__(*args, **kwargs)
        self.fields['title'].widget.attrs['class'] = 'form-control'
        self.fields['description'].widget.attrs['class'] = 'form-control'
        self.fields['image'].widget.attrs['class'] = 'form-control'
        self.fields['status'].widget.attrs['class'] = 'form-select'
        for field in self.fields:
            self.fields[field].widget.attrs['placeholder'] = 'Provide Detail'


class ProResearchForm(forms.ModelForm):
    class Meta:
        model = ProResearch
        fields = ['title', 'description', 'image', 'status']

    def __init__(self, *args, **kwargs):
        super(ProResearchForm, self).__init__(*args, **kwargs)
        self.fields['title'].widget.attrs['class'] = 'form-control'
        self.fields['description'].widget.attrs['class'] = 'form-control'
        self.fields['image'].widget.attrs['class'] = 'form-control'
        self.fields['status'].widget.attrs['class'] = 'form-select'
        for field in self.fields:
            self.fields[field].widget.attrs['placeholder'] = 'Provide Detail'


class ProVideosForm(forms.ModelForm):
    class Meta:
        model = ProVideos
        fields = ['title', 'description', 'video_code', 'status']

    def __init__(self, *args, **kwargs):
        super(ProVideosForm, self).__init__(*args, **kwargs)
        self.fields['title'].widget.attrs['class'] = 'form-control'
        self.fields['description'].widget.attrs['class'] = 'form-control'
        self.fields['video_code'].widget.attrs['class'] = 'form-control'
        self.fields['status'].widget.attrs['class'] = 'form-select'
        for field in self.fields:
            self.fields[field].widget.attrs['placeholder'] = 'Provide Detail'


class ProDownloadsForm(forms.ModelForm):
    class Meta:
        model = ProDownloads
        fields = ['title', 'description', 'image', 'download_link',  'status']

    def __init__(self, *args, **kwargs):
        super(ProDownloadsForm, self).__init__(*args, **kwargs)
        self.fields['title'].widget.attrs['class'] = 'form-control'
        self.fields['description'].widget.attrs['class'] = 'form-control'
        self.fields['image'].widget.attrs['class'] = 'form-control'
        self.fields['download_link'].widget.attrs['class'] = 'form-control'
        self.fields['status'].widget.attrs['class'] = 'form-select'
        for field in self.fields:
            self.fields[field].widget.attrs['placeholder'] = 'Provide Detail'


class ProPhotosForm(forms.ModelForm):
    class Meta:
        model = ProPhotos
        fields = ['category', 'title', 'image', 'download_link',  'status']

    def __init__(self, *args, **kwargs):
        super(ProPhotosForm, self).__init__(*args, **kwargs)
        self.fields['category'].widget.attrs['class'] = 'form-select'
        self.fields['category'].widget.attrs['data-control'] = 'select2'
        self.fields['category'].widget.attrs['style'] = 'height: 420px;'
        self.fields['category'].queryset = ProPhotosCat.objects.all() | ProPhotosCat.objects.none()
        self.fields['category'].widget.choices = [('add_new', 'Add Now')] + list(self.fields['category'].widget.choices)
        self.fields['title'].widget.attrs['class'] = 'form-control'
        self.fields['image'].widget.attrs['class'] = 'form-control'
        self.fields['download_link'].widget.attrs['class'] = 'form-control'
        self.fields['status'].widget.attrs['class'] = 'form-select'
        for field in self.fields:
            self.fields[field].widget.attrs['placeholder'] = 'Provide Detail'


class ProQuotesForm(forms.ModelForm):
    class Meta:
        model = ProQuotes
        fields = ['title', 'image', 'download_link',  'status']

    def __init__(self, *args, **kwargs):
        super(ProQuotesForm, self).__init__(*args, **kwargs)
        self.fields['title'].widget.attrs['class'] = 'form-control'
        self.fields['image'].widget.attrs['class'] = 'form-control'
        self.fields['download_link'].widget.attrs['class'] = 'form-control'
        self.fields['status'].widget.attrs['class'] = 'form-select'
        for field in self.fields:
            self.fields[field].widget.attrs['placeholder'] = 'Provide Detail'
