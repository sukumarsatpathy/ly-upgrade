from django.db import models
from django.urls import reverse
from image_cropping import ImageRatioField
from smart_selects.db_fields import ChainedForeignKey
from django.utils.translation import gettext_lazy as _
from datetime import datetime
from accounts.models import Account
from settings.models import Country, State, City
from embed_video.fields import EmbedVideoField
from ckeditor_uploader.fields import RichTextUploadingField


class TrainingCategory(models.Model):
    title = models.CharField(_('Category Name'), max_length=250)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'
        db_table = 'training-category'


class Training(models.Model):
    category_title = models.ForeignKey(TrainingCategory, on_delete=models.CASCADE)
    description = RichTextUploadingField(_('Description'))
    img1 = models.ImageField(_('Sidebar Image 1'), upload_to='trainings/%Y/%m/%d/', blank=True, null=True)
    img2 = models.ImageField(_('Sidebar Image 2'), upload_to='trainings/%Y/%m/%d/', blank=True, null=True)
    img3 = models.ImageField(_('Sidebar Image 3'), upload_to='trainings/%Y/%m/%d/', blank=True, null=True)
    img4 = models.ImageField(_('Sidebar Image 4'), upload_to='trainings/%Y/%m/%d/', blank=True, null=True)
    cropped_img1 = ImageRatioField('img1', '345x230', size_warning=True)
    cropped_img2 = ImageRatioField('img2', '345x230', size_warning=True)
    cropped_img3 = ImageRatioField('img3', '345x230', size_warning=True)
    cropped_img4 = ImageRatioField('img4', '345x230', size_warning=True)
    trainer_name = models.CharField(_('Trainer Name'), max_length=200, null=True)
    author = models.ForeignKey(Account, on_delete=models.CASCADE)
    email = models.EmailField(_('Email'), max_length=200)
    contact_no = models.CharField(_('Contact No'), max_length=15)
    video_url = EmbedVideoField(_('Title Video'), blank=True, null=True)
    video_url_1 = EmbedVideoField(_('Sidebar Video 1'), blank=True, null=True)
    video_url_2 = EmbedVideoField(_('Sidebar Video 2'), blank=True, null=True)
    video_url_3 = EmbedVideoField(_('Sidebar Video 3'), blank=True, null=True)
    video_url_4 = EmbedVideoField(_('Sidebar Video 4'), blank=True, null=True)
    location = models.CharField(_('Venue Details'), max_length=200, blank=True, null=True)
    country = models.ForeignKey(Country, on_delete=models.SET_NULL, null=True, blank=True)
    state = ChainedForeignKey(State, chained_field="country", chained_model_field="country", show_all=False, auto_choose=True, null=True)
    city = ChainedForeignKey(City, chained_field="state", chained_model_field="state", show_all=False, auto_choose=True, null=True)
    start_date = models.DateField(_('Start Date'), editable=True)
    end_date = models.DateField(_('End Date'), editable=True)
    created_date = models.DateTimeField(_('Created Date'), default=datetime.now, editable=False)
    modified_date = models.DateTimeField(_('Modified Date'), auto_now=True, editable=False)
    views = models.IntegerField(_('Views'), default=0)
    status = models.BooleanField(_('Status'), default=True)

    class Meta:
        verbose_name = 'Training'
        verbose_name_plural = 'Trainings'
        db_table = 'training'

    def __str__(self):
        return str(self.trainer_name)

    def get_absolute_url(self):
        return reverse('list-training')
