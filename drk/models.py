from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

class UpcomingEvents(models.Model):
    title = models.CharField(_('Title'), max_length=255, null=True)
    description = models.TextField(_('Description'), null=True)
    startDate = models.DateTimeField(_('Start Date'), null=True)
    duration = models.CharField(_('Duration'), max_length=100, null=True)
    timing = models.CharField(_('Timing'), max_length=100, null=True)
    language = models.CharField(_('Language'), max_length=100, null=True)
    btnText = models.CharField(_('Button Text'), max_length=50, null=True)
    btnURL = models.URLField(_('Button URL'), null=True)
    btnBgColor = models.CharField(_('Button Color'), max_length=50, null=True)
    image = models.ImageField(_('Image'), upload_to='upcomingEvents/%Y/%m/%d/', null=True)
    is_daily = models.BooleanField(_('Is Daily?'), default=False)
    is_active = models.BooleanField(_('Is Active'), default=True)
    created_date = models.DateTimeField(_('Created Date'), default=timezone.now, editable=False)
    modified_date = models.DateTimeField(_('Modified Date'), auto_now=True, editable=False)

    class Meta:
        verbose_name = 'Upcoming Event'
        verbose_name_plural = 'Upcoming Events'
        db_table = 'drk_upcoming_events'

    def __str__(self):
        return self.title

    def days_left(self):
        if self.is_daily:
            return "Daily event"
        if self.startDate:
            today = timezone.localtime(timezone.now()).date()
            start_date = timezone.localtime(self.startDate).date()
            delta = start_date - today
            if delta.days < 0:
                return "Event completed"
            else:
                return "{} days left".format(delta.days)

        return None