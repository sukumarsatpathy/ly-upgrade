import uuid
from django.db import models
from django.urls import reverse
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


class Testimonial(models.Model):
    title = models.CharField(_("Title"), max_length=255, null=True)
    slug = models.SlugField(_('Slug'), max_length=255, null=True)
    description = RichTextUploadingField(_('Description'))
    image = models.ImageField(_('Image'), upload_to='testimonials/%Y/%m/%d/', null=True)
    location = models.CharField(_('Location'), max_length=255, null=True)
    publisher = models.CharField(_("Publisher Name"), max_length=255, null=True, blank=True)
    author = models.ForeignKey(Account, on_delete=models.CASCADE, null=True)
    views = models.IntegerField(_('Views'), default=0)
    meta_title = models.CharField(_('Meta Title'), max_length=60, null=True, blank=True)
    meta_description = models.CharField(_('Meta Description'), max_length=160, null=True, blank=True)
    status = models.CharField(_('Status'), max_length=15, choices=status_choices, default='Published')
    created_date = models.DateTimeField(_('Created Date'), auto_now_add=True, editable=False)
    modified_date = models.DateTimeField(_('Modified Date'), auto_now=True, editable=False)

    class Meta:
        verbose_name = 'Testimonial'
        verbose_name_plural = 'Testimonials'
        db_table = 'testimonial'

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.slug = f'{slugify(self.title)}-{str(uuid.uuid4())[:8]}'
        super(Testimonial, self).save(*args, **kwargs)