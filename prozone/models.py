from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from embed_video.fields import EmbedVideoField
from django.template.defaultfilters import slugify
from ckeditor_uploader.fields import RichTextUploadingField


status_choices = (
    ('Published', 'Published'),
    ('Draft', 'Draft'),
)


class ProVideos(models.Model):
    title = models.CharField(_('Title'), max_length=500, unique=True)
    slug = models.SlugField(_('Slug'), max_length=500, unique=True)
    description = RichTextUploadingField(_('Description'), null=True)
    video_code = models.CharField(_('Video Code'), max_length=500, unique=True)
    views = models.IntegerField(_('Views'), default=0)
    status = models.CharField(_('Status'), max_length=15, choices=status_choices, default='Published')
    created_date = models.DateTimeField(_('Created Date'), auto_now_add=True, editable=False)
    modified_date = models.DateTimeField(_('Modified Date'), auto_now=True, editable=False)

    class Meta:
        verbose_name = 'Pro Video'
        verbose_name_plural = 'Pro Videos'
        db_table = 'prozone-videos-list'

    def __str__(self):
        return self.title

    # Auto Slug from title field
    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(ProVideos, self).save(*args, **kwargs)


class ProDiary(models.Model):
    title = models.CharField(_('Title'), max_length=500, unique=True)
    slug = models.SlugField(_('Slug'), max_length=500, unique=True)
    description = RichTextUploadingField(_('Description'), null=True)
    image = models.ImageField(_('Image'), upload_to='prozone/article/%Y/%m/%d/', blank=True, null=True)
    views = models.IntegerField(_('Views'), default=0)
    status = models.CharField(_('Status'), max_length=15, choices=status_choices, default='Published')
    created_date = models.DateTimeField(_('Created Date'), auto_now_add=True, editable=False)
    modified_date = models.DateTimeField(_('Modified Date'), auto_now=True, editable=False)

    class Meta:
        verbose_name = 'DrK\'s Pro Diary'
        verbose_name_plural = 'DrK\'s Pro Diary'
        db_table = 'prozone-drk-diary-list'

    def __str__(self):
        return self.title

    # Auto Slug from title field
    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(ProDiary, self).save(*args, **kwargs)


class ProResearch(models.Model):
    title = models.CharField(_('Title'), max_length=500, unique=True)
    slug = models.SlugField(_('Slug'), max_length=500, unique=True)
    description = RichTextUploadingField(_('Description'), null=True)
    image = models.ImageField(_('Image'), upload_to='prozone/research/%Y/%m/%d/', blank=True, null=True)
    views = models.IntegerField(_('Views'), default=0)
    status = models.CharField(_('Status'), max_length=15, choices=status_choices, default='Published')
    created_date = models.DateTimeField(_('Created Date'), auto_now_add=True, editable=False)
    modified_date = models.DateTimeField(_('Modified Date'), auto_now=True, editable=False)

    class Meta:
        verbose_name = 'Research Article'
        verbose_name_plural = 'Research Articles'
        db_table = 'prozone-research-list'

    def __str__(self):
        return self.title

    # Auto Slug from title field
    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(ProResearch, self).save(*args, **kwargs)


class ProDownloads(models.Model):
    title = models.CharField(_('Title'), max_length=250, unique=True, null=True)
    slug = models.SlugField(_('Slug'), max_length=250, unique=True, null=True)
    image = models.ImageField(_('Image'), upload_to='prozone/download/resource/%Y/%m/%d/')
    download_link = models.FileField(_('Upload File'), null=True)
    description = RichTextUploadingField(_('Description'), null=True)
    views = models.IntegerField(_('Views'), default=0)
    status = models.CharField(_('Status'), max_length=15, choices=status_choices, default='Published')
    created_date = models.DateTimeField(_('Created Date'), auto_now_add=True, editable=False)
    modified_date = models.DateTimeField(_('Modified Date'), auto_now=True, editable=False)

    class Meta:
        verbose_name = 'Pro Resource'
        verbose_name_plural = 'Pro Resources'
        db_table = 'prozone-resource-list'

    def __str__(self):
        return self.title

    # Auto Slug from title field
    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(ProDownloads, self).save(*args, **kwargs)


class ProPhotosCat(models.Model):
    title = models.CharField(_('Category Name'), max_length=255, unique=True)
    slug = models.SlugField(_('Slug'), max_length=255, unique=True)
    status = models.CharField(_('Status'), max_length=15, choices=status_choices, default='Published')
    created_date = models.DateTimeField(_('Created Date'), auto_now_add=True, editable=False)
    modified_date = models.DateTimeField(_('Modified Date'), auto_now=True, editable=False)

    class Meta:
        verbose_name = 'Photos Category'
        verbose_name_plural = 'Photos Category'
        db_table = 'prozone-photos-category-list'

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('download-photos')

    # Auto Slug from title field
    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(ProPhotosCat, self).save(*args, **kwargs)


class ProPhotos(models.Model):
    category = models.ForeignKey(ProPhotosCat, on_delete=models.CASCADE)
    title = models.CharField(_('Title'), max_length=255, unique=True, null=True)
    slug = models.SlugField(_('Slug'), max_length=255, unique=True, null=True)
    image = models.ImageField(_('Image'), upload_to='prozone/download/photos/%Y/%m/%d/')
    download_link = models.FileField(_('Upload File'), null=True)
    status = models.CharField(_('Status'), max_length=15, choices=status_choices, default='Published')
    created_date = models.DateTimeField(_('Created Date'), auto_now_add=True, editable=False)
    modified_date = models.DateTimeField(_('Modified Date'), auto_now=True, editable=False)

    class Meta:
        verbose_name = 'Photos'
        verbose_name_plural = 'Photos'
        db_table = 'prozone-download-photos-list'

    def __str__(self):
        return self.title

    # Auto Slug from title field
    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(ProPhotos, self).save(*args, **kwargs)


class ProQuotes(models.Model):
    title = models.CharField(_('Title'), max_length=255, unique=True, null=True)
    slug = models.CharField(_('Slug'), max_length=255, unique=True, null=True)
    image = models.ImageField(_('Image'), upload_to='prozone/download/quotes/%Y/%m/%d')
    download_link = models.FileField(_('Upload File'), null=True)
    status = models.CharField(_('Status'), max_length=15, choices=status_choices, default='Published')
    created_date = models.DateTimeField(_('Created Date'), auto_now_add=True, editable=False)
    modified_date = models.DateTimeField(_('Modified Date'), auto_now=True, editable=False)

    class Meta:
        verbose_name = 'Quote'
        verbose_name_plural = 'Quotes'
        db_table = 'prozone-quotes-list'

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(ProQuotes, self).save(*args, **kwargs)