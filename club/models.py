from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from smart_selects.db_fields import ChainedForeignKey
from ckeditor_uploader.fields import RichTextUploadingField
from django.contrib.auth import get_user_model
from embed_video.fields import EmbedVideoField
from settings.models import Country, State, City

User = get_user_model()


class ClubCategory(models.Model):
    title = models.CharField(_('Category Name'), max_length=250)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'
        db_table = 'club-category'


class Club(models.Model):
    category_title = models.ForeignKey(ClubCategory, on_delete=models.CASCADE)
    title = models.CharField(_('Title'), max_length=255)
    description = RichTextUploadingField(_('Description'))
    email = models.EmailField(_('Contact Email'), max_length=200)
    frequency = models.CharField(_('Meeting Frequency'), max_length=200)
    country = models.ForeignKey(Country, on_delete=models.SET_NULL, null=True, blank=True)
    state = ChainedForeignKey(State, chained_field="country", chained_model_field="country", show_all=False, auto_choose=True, null=True)
    city = ChainedForeignKey(City, chained_field="state", chained_model_field="state", show_all=False, auto_choose=True, null=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    location = models.CharField(_('Location'), max_length=200)
    contact_name = models.CharField(_('Contact Person'), max_length=200, null=True)
    contact_no = models.CharField(_('Contact Number'), max_length=15, null=True, blank=True)
    image1 = models.ImageField(_('Club Image 1'), upload_to='club/%Y/%m/%d/', blank=True, null=True)
    image2 = models.ImageField(_('Club Image 2'), upload_to='club/%Y/%m/%d/', blank=True, null=True)
    video1 = EmbedVideoField(_('Club Video 1'), blank=True, null=True)
    video2 = EmbedVideoField(_('Club Video 2'), blank=True, null=True)
    views = models.IntegerField(_('Views'), default=0)
    created_date = models.DateTimeField(_('Created Date'), auto_now_add=True, editable=False)
    modified_date = models.DateTimeField(_('Modified Date'), auto_now=True, editable=False)

    class Meta:
        verbose_name = 'Laughter Club'
        verbose_name_plural = 'Laughter Clubs'
        db_table = 'laughter_club'

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('list-club')
