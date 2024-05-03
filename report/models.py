from django.db import models
from django.utils.translation import gettext_lazy as _

category_choices = (
    ('Contact', 'Contact'),
    ('LY2', 'LY2'),
    ('Basic Learning Course', 'Basic Learning Course'),
    ('Leader Training', 'Leader Training'),
    ('Teacher Training', 'Teacher Training'),
    ('School', 'School'),
    ('Business', 'Business'),
    ('Special Needs', 'Special Needs'),
    ('Profile Enquiry', 'Profile Enquiry'),
)


class Contact(models.Model):
    category = models.CharField(_('Category'), max_length=100, choices=category_choices, null=True)
    full_name = models.CharField(_('Full Name'), max_length=100, null=True)
    email = models.CharField(_('Email'), max_length=100, null=True)
    contact = models.CharField(_('Contact'), max_length=15, null=True)
    country = models.CharField(_('Country'), max_length=100, null=True)
    message = models.TextField(_('Description'))
    created = models.DateTimeField(_('Created Date'), auto_now=True)

    class Meta:
        verbose_name = 'Contact Us'
        verbose_name_plural = 'Contact Us'
        db_table = 'report-contact-lists'

    def __str__(self):
        return self.full_name


class InfoBooklet(models.Model):
    full_name = models.CharField(_('Full Name'), max_length=100, null=True)
    email = models.CharField(_('Email'), max_length=100, null=True)
    country = models.CharField(_('Country'), max_length=100, null=True)
    downloaded = models.DateTimeField(_('Download Date'), auto_now=True)

    class Meta:
        verbose_name = 'Info Booklet'
        verbose_name_plural = 'Info Booklet'
        db_table = 'report-info-booklet'

    def __str__(self):
        return self.full_name


class TrainerProfileEnquiry(models.Model):
    full_name = models.CharField(_('Full Name'), max_length=100, null=True)
    email = models.CharField(_('Email'), max_length=100, null=True)
    contact = models.CharField(_('Contact'), max_length=15, null=True)
    country = models.CharField(_('Country'), max_length=100, null=True)
    message = models.TextField(_('Description'))
    created = models.DateTimeField(_('Created Date'), auto_now=True)

    class Meta:
        verbose_name = 'Trainer Profile Enquiry'
        verbose_name_plural = 'Trainer Profile Enquiry'
        db_table = 'report-trainer-profile-enquiry'

    def __str__(self):
        return self.full_name


tour_category_list = (
    ('Jaipur', 'Jaipur'),
    ('Thane-Navi-Mumbai', 'Thane-Navi-Mumbai'),
    ('Mumbai', 'Mumbai'),
)


class LYTourEnquiry(models.Model):
    full_name = models.CharField(_('Full Name'), max_length=200, null=True)
    email = models.CharField(_('Email'), max_length=200, null=True)
    contact = models.CharField(_('Contact'), max_length=15, null=True)
    category = models.CharField(_('Category'), max_length=20, null=True, default='Jaipur')
    created = models.DateTimeField(_('Created Date'), auto_now=True)

    class Meta:
        verbose_name = 'LY Tour Enquiry'
        verbose_name_plural = 'LY Tour Enquiry'
        db_table = 'report-ly-tour-enquiry'

    def __str__(self):
        return self.full_name


class ZoomLCEnquiry(models.Model):
    full_name = models.CharField(_('Full Name'), max_length=200, null=True)
    email = models.CharField(_('Email'), max_length=200, null=True)
    contact = models.CharField(_('Contact'), max_length=15, null=True)
    occupation = models.CharField(_('Occupation'), max_length=255, null=True)
    country = models.CharField(_('Country'), max_length=15, null=True)
    token = models.CharField(_('Token'), max_length=100, null=True)
    created = models.DateTimeField(_('Created Date'), auto_now=True)

    class Meta:
        verbose_name = 'Zoom LC Enquiry'
        verbose_name_plural = 'Zoom LC Enquiry'
        db_table = 'report-zoom-lc-enquiry'

    def __str__(self):
        return self.full_name


class SpiritualRetreat(models.Model):
    month = models.CharField(_('Retreat Month'), max_length=255, null=True)
    name = models.CharField(_('Full Name'), max_length=200, null=True)
    email = models.CharField(_('Email'), max_length=200, null=True)
    whatsapp = models.CharField(_('Contact'), max_length=15, null=True)
    location = models.CharField(_('Location'), max_length=255, null=True)
    info = models.TextField(_('Information'), null=True)
    accommodation = models.TextField(_('Accommodation'), null=True)
    comments = models.TextField(_('Comments'), null=True)
    token = models.TextField(_('Token'), null=True)
    whatsapp_status = models.BooleanField(_("WhatsApp Status"), default=False, null=True)
    email_status = models.BooleanField(_("Email Status"), default=False, null=True)
    submitted_date = models.DateTimeField(_('Submitted Date'), auto_now=True)

    class Meta:
        verbose_name = 'Spiritual Retreat'
        verbose_name_plural = 'Spiritual Retreat'
        db_table = 'report-spiritual-retreat-registration'

    def __str__(self):
        return self.name