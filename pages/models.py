from django.db import models
from datetime import datetime
from django.urls import reverse
from django.template.defaultfilters import slugify
from django.utils.translation import gettext_lazy as _
from ckeditor_uploader.fields import RichTextUploadingField

status_choices = (
    ('Published', 'Published'),
    ('Draft', 'Draft'),
)


class GetInvolved(models.Model):
    title = models.CharField(_('Title'), max_length=100, unique=True)
    description = models.CharField(_('Description'), max_length=255, null=True)
    image = models.ImageField(_('Image'), upload_to='getinvolved/%Y/%m/%d/')
    btn_name = models.CharField(_('Button Name'), max_length=20, blank=True, null=True)
    url = models.URLField(_('Link URL'), max_length=200)
    status = models.CharField(_('Status'), max_length=15, choices=status_choices, default='Published')
    created_date = models.DateTimeField(_('Created Date'), auto_now_add=True, editable=False)
    modified_date = models.DateTimeField(_('Modified Date'), auto_now=True, editable=False)

    class Meta:
        verbose_name = 'Get Involved'
        verbose_name_plural = 'Get Involved'
        db_table = 'pages-get-involved'

    def __str__(self):
        return self.title


class Diary(models.Model):
    title = models.CharField(_('Title'), max_length=500, unique=True, null=True)
    slug = models.SlugField(_('Slug'), max_length=500, unique=True)
    description = RichTextUploadingField(_('Description'), null=True)
    image = models.ImageField(_('Image'), upload_to='diary/%Y/%m/%d/', help_text="326x244", null=True)
    created_date = models.DateTimeField(_('Created Date'), auto_now_add=True, editable=False)
    modified_date = models.DateTimeField(_('Modified Date'), auto_now=True, editable=False)
    views = models.IntegerField(_('Views'), default=0)
    status = models.CharField(_('Status'), max_length=15, choices=status_choices, default='Published')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Dairy'
        verbose_name_plural = 'Dairies'
        db_table = 'pages-diary'

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Diary, self).save(*args, **kwargs)


class laughterBlogsCat(models.Model):
    title = models.CharField(_('Category Name'), max_length=255, unique=True)
    slug = models.SlugField(_('Slug'), max_length=255, unique=True)
    created_date = models.DateTimeField(_('Created Date'), auto_now_add=True, editable=False)
    modified_date = models.DateTimeField(_('Modified Date'), auto_now=True, editable=False)

    class Meta:
        verbose_name = 'Laughter Blog Category'
        verbose_name_plural = 'Laughter Blog Category'
        db_table = 'pages-laughter-blog-category-list'

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('laughter-blogs')

    # Auto Slug from title field
    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(laughterBlogsCat, self).save(*args, **kwargs)


class laughterBlogs(models.Model):
    category = models.ForeignKey(laughterBlogsCat, on_delete=models.CASCADE)
    title = models.CharField(_('Title'), max_length=255, unique=True, null=True)
    slug = models.SlugField(_('Slug'), max_length=255, unique=True, null=True)
    description = RichTextUploadingField(_('Description'))
    image = models.ImageField(_('Image'), upload_to='laughterBlogs/%Y/%m/%d/')
    views = models.IntegerField(_('Views'), default=0, null=True, blank=True)
    meta_title = models.CharField(_('Meta Title'), max_length=60, null=True)
    meta_description = models.CharField(_('Meta Description'), max_length=158, null=True)
    meta_keywords = models.CharField(_('Meta Keywords'), max_length=500, null=True, help_text='Word separated by commas')
    status = models.CharField(_('Status'), max_length=15, choices=status_choices, default='Published')
    created_date = models.DateTimeField(_('Created Date'), auto_now_add=True, editable=False)
    modified_date = models.DateTimeField(_('Modified Date'), auto_now=True, editable=False)

    class Meta:
        verbose_name = 'Laughter Blog'
        verbose_name_plural = 'Laughter Blogs'
        db_table = 'pages-laughter-blog-list'

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('laughter-blogs-detail')

    # Auto Slug from title field
    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(laughterBlogs, self).save(*args, **kwargs)


class generalResearch(models.Model):
    title = models.CharField(_('Title'), max_length=500, unique=True)
    slug = models.SlugField(_('Slug'), max_length=500, unique=True)
    description = RichTextUploadingField(_('Description'), null=True)
    image = models.ImageField(_('Image'), upload_to='general/research/%Y/%m/%d/', blank=True, null=True)
    views = models.IntegerField(_('Views'), default=0)
    meta_title = models.CharField(_('Meta Title'), max_length=60, null=True)
    meta_description = models.CharField(_('Meta Description'), max_length=158, null=True)
    meta_keywords = models.CharField(_('Meta Keywords'), max_length=500, null=True, help_text='Word separated by commas')
    created_date = models.DateTimeField(_('Created Date'), auto_now_add=True, editable=False)
    modified_date = models.DateTimeField(_('Modified Date'), auto_now=True, editable=False)
    status = models.CharField(_('Status'), max_length=15, choices=status_choices, default='Published')

    class Meta:
        verbose_name = 'Research Articles on LY'
        verbose_name_plural = 'Research Articles on LY'
        db_table = 'pages-research-list'

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('research-article-detail')

    # Auto Slug from title field
    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(generalResearch, self).save(*args, **kwargs)