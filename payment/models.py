from django.db import models
from django.utils.translation import gettext_lazy as _


class ly2Transaction(models.Model):
    course = models.CharField(_('Course'), max_length=500, null=True)
    full_name = models.CharField(_('Full Name'), max_length=500, null=True)
    email = models.EmailField(_('Email'), max_length=500, null=True)
    address = models.CharField(_('Address'), max_length=500, null=True)
    city = models.CharField(_('City'), max_length=500, null=True)
    state = models.CharField(_('State'), max_length=500, null=True)
    country = models.CharField(_('Country'), max_length=500, null=True)
    postalcode = models.CharField(_('Postal Code'), max_length=500, null=True)
    price = models.CharField(_('Price'), max_length=100, null=True)
    contact = models.CharField(_('Contact'), max_length=500, null=True)
    information = models.CharField(_('Information'), max_length=500, null=True)
    token = models.TextField(_('Token No'), null=True)
    enrolled_date = models.DateTimeField(_('Start Date'), auto_now=True)

    class Meta:
        verbose_name = 'LY2 Transaction'
        verbose_name_plural = 'LY2 Transaction'
        db_table = 'payment_ly2_transaction'

    def __str__(self):
        return self.full_name


class blcTransaction(models.Model):
    course = models.CharField(_('Course'), max_length=500, null=True)
    full_name = models.CharField(_('Full Name'), max_length=500, null=True)
    email = models.EmailField(_('Email'), max_length=500, null=True)
    address = models.CharField(_('Address'), max_length=500, null=True)
    city = models.CharField(_('City'), max_length=500, null=True)
    state = models.CharField(_('State'), max_length=500, null=True)
    country = models.CharField(_('Country'), max_length=500, null=True)
    postalcode = models.CharField(_('Postal Code'), max_length=500, null=True)
    price = models.IntegerField(_('Price'), null=True)
    contact = models.CharField(_('Contact'), max_length=500, null=True)
    information = models.CharField(_('Information'), max_length=500, null=True)
    token = models.TextField(_('Token No'), null=True)
    enrolled_date = models.DateTimeField(_('Start Date'), auto_now=True)

    class Meta:
        verbose_name = 'BLC Transaction'
        verbose_name_plural = 'BLC Transaction'
        db_table = 'payment_blc_transaction'

    def __str__(self):
        return self.full_name


class cttTransaction(models.Model):
    full_name = models.CharField(_('Full Name'), max_length=500, null=True)
    email = models.EmailField(_('Email'), max_length=500, null=True)
    address = models.CharField(_('Address'), max_length=500, null=True)
    city = models.CharField(_('City'), max_length=500, null=True)
    state = models.CharField(_('State'), max_length=500, null=True)
    country = models.CharField(_('Country'), max_length=500, null=True)
    postalcode = models.CharField(_('Postal Code'), max_length=500, null=True)
    price = models.IntegerField(_('Price'), null=True)
    contact = models.CharField(_('Contact'), max_length=500, null=True)
    information = models.CharField(_('Information'), max_length=500, null=True)
    token = models.TextField(_('Token No'), null=True)
    enrolled_date = models.DateTimeField(_('Start Date'), auto_now=True)

    class Meta:
        verbose_name = 'Teacher Training Transaction'
        verbose_name_plural = 'Teacher Training Transaction'
        db_table = 'payment_ctt_transaction'

    def __str__(self):
        return self.full_name


class indTraining(models.Model):
    full_name = models.CharField(_('Full Name'), max_length=500, null=True)
    email = models.EmailField(_('Email'), max_length=500, null=True)
    price = models.IntegerField(_('Price'), null=True)
    contact = models.CharField(_('Contact'), max_length=500, null=True)
    token = models.TextField(_('Token No'), null=True)
    instamojo_response = models.TextField(_('Instamojo Response'), null=True, blank=True)
    enrolled_date = models.DateTimeField(_('Start Date'), auto_now=True)

    class Meta:
        verbose_name = 'India Training Transaction'
        verbose_name_plural = 'India Training Transaction'
        db_table = 'payment_ind_transaction'

    def __str__(self):
        return self.full_name

PaymentStatus = (
    ('Success', 'Success'),
    ('Failure', 'Failure'),
    ('Pending', 'Pending'),
)


email_status = (
    ('Sent', 'Sent'),
    ('Pending', 'Pending'),
)

class wcTransaction(models.Model):
    full_name = models.CharField(_('Full Name'), max_length=500, null=True)
    email = models.EmailField(_('Email'), max_length=500, null=True)
    address = models.CharField(_('Address'), max_length=500, null=True)
    city = models.CharField(_('City'), max_length=500, null=True)
    state = models.CharField(_('State'), max_length=500, null=True)
    country = models.CharField(_('Country'), max_length=500, null=True)
    postalcode = models.CharField(_('Postal Code'), max_length=500, null=True)
    price = models.CharField(_('Price'), max_length=100, null=True)
    contact = models.CharField(_('Contact'), max_length=500, null=True)
    information = models.CharField(_('Information'), max_length=500, null=True)
    token = models.TextField(_('Token No'), null=True)
    enrolled_date = models.DateTimeField(_('Start Date'), auto_now=True)

    class Meta:
        verbose_name = 'World Conference Transaction'
        verbose_name_plural = 'World Conference Transaction'
        db_table = 'payment_world_conference'
    def __str__(self):
        return self.full_name


class prozoneTransaction(models.Model):
    full_name = models.CharField(_('Full Name'), max_length=500, null=True)
    email = models.EmailField(_('Email'), max_length=500, null=True)
    membership_name = models.CharField(_('Membership Name'), max_length=500, null=True)
    start_date = models.DateTimeField(_('Start Date'), null=True, blank=True)
    expiry_date = models.DateTimeField(_('Expiry Date'), null=True, blank=True)
    address = models.CharField(_('Address'), max_length=500, null=True)
    city = models.CharField(_('City'), max_length=500, null=True)
    state = models.CharField(_('State'), max_length=500, null=True)
    country = models.CharField(_('Country'), max_length=500, null=True)
    postalcode = models.CharField(_('Postal Code'), max_length=500, null=True)
    price = models.CharField(_('Price'), max_length=100, null=True)
    contact = models.CharField(_('Contact'), max_length=500, null=True)
    token = models.TextField(_('Token No'), null=True)
    subscribed_date = models.DateTimeField(_('Start Date'), auto_now=True)

    class Meta:
        verbose_name = 'Prozone Transaction'
        verbose_name_plural = 'Prozone Transaction'
        db_table = 'payment_prozone_transaction'

    def __str__(self):
        return self.full_name