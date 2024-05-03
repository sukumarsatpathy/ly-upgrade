import uuid
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.template.defaultfilters import slugify
from accounts.models import Account
from ckeditor_uploader.fields import RichTextUploadingField


status_choices = (
    ('Published', 'Published'),
    ('Draft', 'Draft'),
    ('Review', 'Review'),
    ('Rejected', 'Rejected'),
)


class News(models.Model):
    title = models.CharField(_("Title"), max_length=255, null=True)
    slug = models.SlugField(_('Slug'), max_length=255, null=True)
    description = RichTextUploadingField(_('Description'))
    image = models.ImageField(_('Image'), upload_to='news/%Y/%m/%d/', null=True, blank=True)
    location = models.CharField(_('Location'), max_length=255, null=True)
    views = models.IntegerField(_('Views'), default=0)
    meta_title = models.CharField(_('Meta Title'), max_length=60, null=True, blank=True)
    meta_description = models.CharField(_('Meta Description'), max_length=160, null=True, blank=True)
    status = models.CharField(_('Status'), max_length=15, choices=status_choices, default='Published')
    created_date = models.DateTimeField(_('Created Date'), auto_now_add=True, editable=False)
    modified_date = models.DateTimeField(_('Modified Date'), auto_now=True, editable=False)

    class Meta:
        verbose_name = 'News'
        verbose_name_plural = 'News'
        db_table = 'news-list'

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.slug = f'{slugify(self.title)}-{str(uuid.uuid4())[:8]}'
        super(News, self).save(*args, **kwargs)