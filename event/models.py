from django.db import models
from django.urls import reverse
from image_cropping import ImageRatioField
from smart_selects.db_fields import ChainedForeignKey
from django.utils.translation import gettext_lazy as _
from datetime import datetime
from ckeditor_uploader.fields import RichTextUploadingField
from accounts.models import Account
from settings.models import Country, State, City
from django.template.defaultfilters import slugify
from embed_video.fields import EmbedVideoField


event_category = (
    ('Free Public Seminar', 'Free Public Seminar'),
    ('Workshop', 'Workshop'),
    ('Conference', 'Conference'),
    ('World Laughter Day', 'World Laughter Day'),
)


class Event(models.Model):
    category = models.CharField(_('Category'), choices=event_category, default='free', max_length=30)
    description = RichTextUploadingField(_('Description'))
    organiser_name = models.CharField(_('Organiser Name'), max_length=200)
    author = models.ForeignKey(Account, on_delete=models.CASCADE)
    email = models.EmailField(_('Email'), max_length=200)
    contact_no = models.CharField(_('Contact No'), max_length=15, blank=True, null=True)
    location = models.CharField(_('Location'), max_length=200)
    country = models.ForeignKey(Country, on_delete=models.SET_NULL, null=True, blank=True)
    state = ChainedForeignKey(State, chained_field="country", chained_model_field="country", show_all=False, auto_choose=True, null=True)
    city = ChainedForeignKey(City, chained_field="state", chained_model_field="state", show_all=False, auto_choose=True,null=True)
    start_date = models.DateField(_('Start Date'), editable=True)
    end_date = models.DateField(_('End Date'), editable=True)
    website_url = models.URLField(_('Website URL'), max_length=200, null=True, blank=True)
    img1 = models.ImageField(_('Event Image 1'), upload_to='events/%Y/%m/%d/', blank=True, null=True)
    img2 = models.ImageField(_('Event Image 2'), upload_to='events/%Y/%m/%d/', blank=True, null=True)
    video1 = EmbedVideoField(_('Event Video 1'), blank=True, null=True)
    video2 = EmbedVideoField(_('Event Video 2'), blank=True, null=True)
    created_date = models.DateTimeField(_('Created Date'), default=datetime.now, editable=False)
    modified_date = models.DateTimeField(_('Modified Date'), auto_now=True, editable=False)
    views = models.IntegerField(_('Views'), default=0)

    class Meta:
        verbose_name = 'Event'
        verbose_name_plural = 'Events'
        db_table = 'events'

    def __str__(self):
        return self.category

    def get_absolute_url(self):
        return reverse('list-event')


wld_cat = (
    ('Banner','Banner'),
    ('Blue Background Logo','Blue Background Logo'),
    ('Message','Message'),
    ('Round Logo','Round Logo'),
)


class worldLaughterDay(models.Model):
    category = models.CharField(_('Category'), max_length=200, choices=wld_cat, default='Banner')
    title = models.CharField(_('Title'), max_length=255, null=True)
    image = models.ImageField(_('Image URL'), upload_to='wld/jpg/%Y/%m/%d/', null=True)
    pdf = models.FileField(_('PDF URL'), upload_to='wld/pdf/%Y/%m/%d/', null=True)
    created_date = models.DateTimeField(_('Created Date'), default=datetime.now, editable=False)
    modified_date = models.DateTimeField(_('Modified Date'), auto_now=True, editable=False)

    class Meta:
        verbose_name = 'WLD'
        verbose_name_plural = 'WLD'
        db_table = 'world-laughter-day'

    def __str__(self):
        return self.title