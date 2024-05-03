import uuid
from django.db import models
from django.template.defaultfilters import slugify
from ckeditor.fields import RichTextField
from django.utils.translation import gettext_lazy as _
from django.core.validators import RegexValidator

menu_choices = (
    ('Home', 'Home'),
    ('About Laughter Yoga', 'About Laughter Yoga'),
    ('Invite DrK', 'Invite DrK'),
    ('LY for Yoga Practitioners', 'LY for Yoga Practitioners'),
    ('LY for Seniors', 'LY for Seniors'),
    ('LY for Business', 'LY for Business'),
    ('LY for School & Colleges', 'LY for School & Colleges'),
    ('LY for Depression', 'LY for Depression'),
    ('LY for Cancer', 'LY for Cancer'),
    ('LY for Special Needs', 'LY for Special Needs'),
    ('LY Trainings', 'LY Trainings'),
    ('Online Training by DrK', 'Online Training by DrK'),
    ('LY 2.0', 'LY 2.0'),
    ('Teacher Training By DrK', 'Teacher Training By DrK'),
    ('Finder', 'Finder'),
    ('DrK Dairy', 'DrK Dairy'),
    ('Blogs', 'Blogs'),
    ('Research Articles', 'Research Articles'),
    ('News', 'News'),
    ('Testimonials', 'Testimonials'),
    ('Shop', 'Shop'),
    ('Prozone', 'Prozone'),
    ('Zoom Laughter Club', 'Zoom Laughter Club'),
    ('DrK Upcoming Events', 'DrK Upcoming Events'),
)


phone_validator = RegexValidator(r"^(\+?\d{0,4})?\s?-?\s?(\(?\d{3}\)?)\s?-?\s?(\(?\d{3}\)?)\s?-?\s?(\(?\d{4}\)?)?$",
                                 "The phone number provided is invalid")


key_type_choices = (
    ('Live', 'Live'),
    ('Test', 'Test'),
)

status_choices = (
    ('Published', 'Published'),
    ('Draft', 'Draft'),
)


email_choices = (
    ('True', 'True'),
    ('False', 'False'),
)

membership_choices = (
    ('Paid', 'Paid'),
    ('Complimentary', 'Complimentary'),
)


class WebSettings(models.Model):
    # Brand
    title = models.CharField(_('Brand Name'), max_length=255, null=True)
    slogan = models.CharField(_('Slogan'), max_length=255, null=True)
    # Logo
    logo_dark = models.ImageField(_('Logo Dark'), upload_to='settings/logo/%Y/%m/%d/')
    logo_light = models.ImageField(_('Logo Light'), upload_to='settings/logo/%Y/%m/%d/')
    favicon = models.FileField(_('Favicon'), upload_to='settings/favicon/%Y/%m/%d/')
    # Contact
    contact_email = models.EmailField(_('Contact Email'), max_length=255, null=True)
    contact_number = models.CharField(_('Contact Number'), max_length=20, validators=[phone_validator], null=True)
    contact_address = models.CharField(_('Contact Address'), max_length=500, null=True)
    # Invoice
    company_name = models.CharField(_('Registered Company Name'), max_length=500, null=True, blank=True)
    company_address = models.CharField(_('Registered Company Address'), max_length=500, null=True, blank=True)
    company_gst = models.CharField(_('Goods and Service Tax'), max_length=50, null=True, blank=True)
    # Default User
    default_user = models.ImageField(_('Default User Image'), upload_to='settings/user/%Y/%m/%d/', null=True)
    # Google reCaptcha V3
    public_key = models.CharField(_('Google reCaptcha Public Key'), max_length=255, null=True, blank=True)
    private_key = models.CharField(_('Google reCaptcha Private Key'), max_length=255, null=True, blank=True)
    # SEO
    meta_title = models.CharField(_('Meta Title'), max_length=60, null=True)
    meta_description = models.CharField(_('Meta Description'), max_length=158, null=True)
    meta_keywords = models.CharField(_('Meta Keywords'), max_length=255, null=True)

    created = models.DateTimeField(_('Created Date'), auto_now_add=True, editable=False)
    modified = models.DateTimeField(_('Modified Date'), auto_now=True, editable=False)

    class Meta:
        verbose_name = 'Web Setting'
        verbose_name_plural = 'Web Settings'
        db_table = 'settings-website'

    def __str__(self):
        return self.title


class MailServer(models.Model):
    name = models.CharField(_('SMTP From Name'), max_length=100, null=True)
    email = models.EmailField(_('SMTP From Email'), max_length=100, null=True)
    port = models.CharField(_('SMTP Port Number'), max_length=10, null=True)
    host = models.CharField(_('SMTP HOST'), max_length=50, null=True)
    host_user = models.EmailField(_('SMTP Host User'), max_length=100, null=True)
    host_password = models.CharField(_('SMTP Host Password'), max_length=100, null=True)
    use_tls = models.CharField(_('SMTP Use TLS'), max_length=5, choices=email_choices, null=True)
    use_ssl = models.CharField(_('SMTP Use SSL'), max_length=5, choices=email_choices, null=True)
    created = models.DateTimeField(_('Created Date'), auto_now_add=True, editable=False)
    modified = models.DateTimeField(_('Modified Date'), auto_now=True, editable=False)

    class Meta:
        verbose_name = 'Mail Server'
        verbose_name_plural = 'Mail Server'
        db_table = 'settings-mail-server'

    def __str__(self):
        return self.name


class StripeGateway(models.Model):
    key_type = models.CharField(_('Stripe Key Type'), max_length=10, choices=key_type_choices, null=True)
    public_key = models.CharField(_('Stripe Public Key'), max_length=255, null=True)
    secret_key = models.CharField(_('Stripe Secret Key'), max_length=255, null=True)
    status = models.CharField(_('Stripe Key Status'), max_length=10, choices=status_choices, null=True)
    created = models.DateTimeField(_('Created Date'), auto_now_add=True, editable=False)
    modified = models.DateTimeField(_('Modified Date'), auto_now=True, editable=False)

    class Meta:
        verbose_name = 'Stripe Payment Gateway'
        verbose_name_plural = 'Stripe Payment Gateway'
        db_table = 'settings-stripe-payment-gateway'

    def __str__(self):
        return str(self.id)


class RazorPayGateway(models.Model):
    key_type = models.CharField(_('RazorPay Key Type'), max_length=10, choices=key_type_choices, null=True)
    key_id = models.CharField(_('RazorPay Key Id'), max_length=255, null=True)
    key_secret = models.CharField(_('RazorPay Key Secret'), max_length=255, null=True)
    status = models.CharField(_('RazorPay Key Status'), max_length=10, choices=status_choices, null=True)
    created = models.DateTimeField(_('Created Date'), auto_now_add=True, editable=False)
    modified = models.DateTimeField(_('Modified Date'), auto_now=True, editable=False)

    class Meta:
        verbose_name = 'RazorPay Payment Gateway'
        verbose_name_plural = 'RazorPay Payment Gateway'
        db_table = 'settings-razorpay-payment-gateway'

    def __str__(self):
        return str(self.id)


class Country(models.Model):
    name = models.CharField(_('Name'), max_length=100, null=True)
    iso3 = models.CharField(_('ISO 3'), max_length=3, null=True)
    iso2 = models.CharField(_('ISO 2'), max_length=2, null=True)
    numeric_code = models.CharField(_('Numeric Code'), max_length=50, null=True)
    phone_code = models.CharField(_('Phone Code'), max_length=50, null=True)
    capital = models.CharField(_('Capital'), max_length=100, null=True)
    currency = models.CharField(_('Currency'), max_length=50, null=True)
    currency_symbol = models.CharField(_('Currency Symbol'), max_length=50, null=True)
    tld = models.CharField(_('TLD'), max_length=50, null=True)
    native = models.CharField(_('Native'), max_length=50, null=True)
    region = models.CharField(_('Region'), max_length=50, null=True)
    sub_region = models.CharField(_('Sub Region'), max_length=50, null=True, blank=True)
    timezones = models.TextField(_('Timezones'), null=True)
    latitude = models.CharField(_('Latitude'), max_length=50, null=True)
    longitude = models.CharField(_('Longitude'), max_length=50, null=True)
    emoji = models.CharField(_('Emoji'), max_length=50, null=True)
    emojiU = models.CharField(_('EmojiU'), max_length=50, null=True)
    status = models.CharField(_('Status'), max_length=10, choices=status_choices, default='Published', null=True)
    created = models.DateTimeField(_('Created Date'), auto_now_add=True, editable=False)
    modified = models.DateTimeField(_('Modified Date'), auto_now=True, editable=False)

    class Meta:
        verbose_name = 'Country'
        verbose_name_plural = 'Country'
        db_table = 'settings-country'

    def __str__(self):
        return self.name


class State(models.Model):
    name = models.CharField(_('Name'), max_length=100, null=True)
    country = models.ForeignKey(Country, on_delete=models.CASCADE, null=True)
    state_code = models.CharField(_('State Code'), max_length=50, null=True)
    type = models.CharField(_('Type'), max_length=100, null=True, blank=True)
    latitude = models.CharField(_('Latitude'), max_length=50, null=True)
    longitude = models.CharField(_('Longitude'), max_length=50, null=True)
    status = models.CharField(_('Status'), max_length=10, choices=status_choices, default='Published', null=True)
    created = models.DateTimeField(_('Created Date'), auto_now_add=True, editable=False)
    modified = models.DateTimeField(_('Modified Date'), auto_now=True, editable=False)

    class Meta:
        verbose_name = 'State'
        verbose_name_plural = 'State'
        db_table = 'settings-state'

    def __str__(self):
        return self.name


class City(models.Model):
    name = models.CharField(_('Name'), max_length=100, null=True)
    country = models.ForeignKey(Country, on_delete=models.CASCADE, null=True)
    state = models.ForeignKey(State, on_delete=models.CASCADE, null=True)
    latitude = models.CharField(_('Latitude'), max_length=50, null=True)
    longitude = models.CharField(_('Longitude'), max_length=50, null=True)
    status = models.CharField(_('Status'), max_length=10, choices=status_choices, default='Published', null=True)
    created = models.DateTimeField(_('Created Date'), auto_now_add=True, editable=False)
    modified = models.DateTimeField(_('Modified Date'), auto_now=True, editable=False)

    class Meta:
        verbose_name = 'City'
        verbose_name_plural = 'City'
        db_table = 'settings-city'

    def __str__(self):
        return self.name


class Twilio(models.Model):
    accountSID = models.CharField(_('Account SID'), max_length=100, null=True)
    authToken = models.CharField(_('Auth Token'), max_length=100, null=True)
    phoneNumber = models.CharField(_('Twilio Number'), max_length=20, null=True)
    status = models.CharField(_('Status'), max_length=10, choices=status_choices, default='Published', null=True)
    created = models.DateTimeField(_('Created Date'), auto_now_add=True, editable=False)
    modified = models.DateTimeField(_('Modified Date'), auto_now=True, editable=False)

    class Meta:
        verbose_name = 'Twilio'
        verbose_name_plural = 'Twilio'
        db_table = 'settings-twilio'

    def __str__(self):
        return self.phoneNumber


class Services(models.Model):
    title = models.CharField(_('Title'), max_length=255, null=True)
    status = models.CharField(_('Status'), max_length=10, choices=status_choices, default='Published', null=True)

    class Meta:
        verbose_name = 'Service'
        verbose_name_plural = 'Services'
        db_table = 'settings-services'

    def __str__(self):
        return self.title


class Banners(models.Model):
    category = models.CharField(_('Select Menu'), max_length=50, choices=menu_choices, null=True)
    title = models.CharField(_('Title'), max_length=255, null=True)
    image = models.ImageField(_('Banner Image'), upload_to='settings/banners/%Y/%m/%d/', null=True)
    status = models.CharField(_('Status'), max_length=10, choices=status_choices, default='Published', null=True)
    created = models.DateTimeField(_('Created Date'), auto_now_add=True, editable=False)
    modified = models.DateTimeField(_('Modified Date'), auto_now=True, editable=False)

    class Meta:
        verbose_name = 'Banner'
        verbose_name_plural = 'Banners'
        db_table = 'settings-banners'

    def __str__(self):
        return self.title


class FAQ(models.Model):
    category = models.CharField(_('Select Menu'), max_length=50, choices=menu_choices, null=True)
    question = models.TextField(_('Question'), null=True)
    answer = models.TextField(_('Answer'), null=True)
    status = models.CharField(_('Status'), max_length=10, choices=status_choices, default='Published', null=True)
    created = models.DateTimeField(_('Created Date'), auto_now_add=True, editable=False)
    modified = models.DateTimeField(_('Modified Date'), auto_now=True, editable=False)

    class Meta:
        verbose_name = 'FAQ'
        verbose_name_plural = 'FAQ'
        db_table = 'settings-faq'

    def __str__(self):
        return self.question


class Membership(models.Model):
    title = models.CharField(_('Name'), max_length=250, null=True)
    slug = models.SlugField(_('Slug'), unique=True, null=True, blank=True, allow_unicode=True)
    type = models.CharField(_('Type'), choices=membership_choices, default='free', max_length=30)
    duration = models.IntegerField(_('Duration in Days'))
    price = models.DecimalField(_('Price'), decimal_places=2, max_digits=5, default=0)
    status = models.CharField(_('Status'), max_length=15, choices=status_choices, default='Published')
    created_date = models.DateTimeField(_('Created Date'), auto_now_add=True, editable=False)
    modified_date = models.DateTimeField(_('Modified Date'), auto_now=True, editable=False)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Membership'
        verbose_name_plural = 'Membership'
        db_table = 'settings-membership'

    def save(self, *args, **kwargs):
        self.slug = f'{slugify(self.title)}-{str(uuid.uuid4())[:8]}'
        super(Membership, self).save(*args, **kwargs)


class Changelog(models.Model):
    title = models.CharField(_('Title'), max_length=255, null=True)
    description = RichTextField(_('Description'), null=True)
    status = models.CharField(_('Status'), max_length=10, choices=status_choices, default='Published', null=True)
    created = models.DateTimeField(_('Created Date'), auto_now_add=True, editable=False)
    modified = models.DateTimeField(_('Modified Date'), auto_now=True, editable=False)

    class Meta:
        verbose_name = 'Changelog'
        verbose_name_plural = 'Changelog'
        db_table = 'settings-changelog'

    def __str__(self):
        return self.title