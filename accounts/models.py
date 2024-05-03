from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.utils.translation import gettext_lazy as _
from image_cropping import ImageRatioField
from settings.models import Country, State, City
from embed_video.fields import EmbedVideoField
from ckeditor_uploader.fields import RichTextUploadingField


class Category(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self) -> str:
        return self.name


class CustomUserManager(BaseUserManager):
    """Define a model manager for User model with no username field."""

    def _create_user(self, email, password=None, **extra_fields):
        """Create and save a User with the given email and password."""
        if not email:
            raise ValueError('Provide a correct email Address')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password=None, **extra_fields):
        """Create and save a SuperUser with the given email and password."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


membership_status = (
    ('active', 'Active'),
    ('expired', 'Expired'),
)

designation_choices = (
    ('General User', 'General User'),
    ('Certified Leader', 'Certified Leader'),
    ('Certified Teacher', 'Certified Teacher'),
    ('Certified Master Trainer', 'Certified Master Trainer'),
)


class Account(AbstractUser):
    username = None
    email = models.EmailField(_('Email'), max_length=255, unique=True)
    first_name = models.CharField(_('First Name'), max_length=100, null=True)
    last_name = models.CharField(_('Last Name'), max_length=100, null=True)
    contact_number = models.CharField(_('Contact Number'), max_length=30, null=True, blank=True)
    trained_by = models.CharField(_('Trainer Name'), max_length=200, null=True)
    services = models.CharField(_('Services Offered'), max_length=500, null=True)
    user_type = models.CharField(_('User Type'), choices=designation_choices, default='General User', max_length=100)
    country = models.ForeignKey(Country, on_delete=models.SET_NULL, null=True)
    state = models.ForeignKey(State, on_delete=models.SET_NULL, null=True)
    city = models.ForeignKey(City, on_delete=models.SET_NULL, null=True)
    profile_pic = models.ImageField(_('Profile Picture'), upload_to='members/%Y/%m/%d/', default='members/default.png')
    pp_cropped = ImageRatioField('profile_pic', '300x300', free_crop=True)
    description = RichTextUploadingField(_(' Description'), null=True)
    basic_learning_course = models.URLField(_('Basic Learning Course URL'), max_length=200, null=True, blank=True)
    certified_leader_training = models.URLField(_('Certified Leader Training URL'), max_length=200, null=True, blank=True)
    certified_teacher_training = models.URLField(_('Certified Teacher Training URL'), max_length=200, null=True, blank=True)

    website_url = models.CharField(_('Website URL'), max_length=200, null=True, blank=True)
    facebook_url = models.CharField(_('Facebook URL'), max_length=200, null=True, blank=True)
    youtube_url = models.CharField(_('Youtube URL'), max_length=200, null=True, blank=True)
    linkedin_url = models.CharField(_('LinkedIn URL'), max_length=200, null=True, blank=True)
    video_url_1 = EmbedVideoField(_('Bottom Video 1'), blank=True, null=True)
    video_url_2 = EmbedVideoField(_('Bottom Video 2'), blank=True, null=True)
    video_url_3 = EmbedVideoField(_('Bottom Video 3'), blank=True, null=True)
    video_url_4 = EmbedVideoField(_('Bottom Video 4'), blank=True, null=True)

    token = models.CharField(_('Token Number'), max_length=100, null=True, blank=True)
    views = models.IntegerField(_('Views'), default=0)

    is_ambassador = models.BooleanField(default=False)
    is_masked = models.BooleanField(default=False)
    active = models.BooleanField(default=True)
    staff = models.BooleanField(default=False)
    admin = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def full_name(self):
        return f'{self.first_name} {self.last_name}'

    def __str__(self):              # __unicode__ on Python 2
        return self.email

    objects = CustomUserManager()

    def get_reg_num(self):
        print(self.country)
        print(self.country.phone_code)
        print(self.first_name)
        print(self.last_name)
        if self.country and self.country.phone_code and self.first_name and self.last_name:
            country_code = self.country.phone_code
            user_initials = f"{self.first_name[0].upper()}{self.last_name[0].upper()}"
            return f"LY-00{country_code}-{user_initials}-{self.pk}"
        else:
            return None