from django.utils import timezone
from django.db import models
from django.utils.translation import gettext_lazy as _
from accounts.models import Account
from settings.models import Membership


membership_choices = (
    ('free', 'Free'),
    ('paid', 'Paid'),
    ('complimentary', 'Complimentary'),
)

status_choices = (
    ('Active', 'Active'),
    ('Expired', 'Expired'),
)


class Subscription(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE, null=True)
    membership = models.ForeignKey(Membership, on_delete=models.SET_NULL, null=True)
    startDate = models.DateTimeField(_('Start Date'), null=True, blank=True)
    endDate = models.DateTimeField(_('Expiry Date'), null=True, blank=True)
    token = models.TextField(_('Token'), max_length=100, null=True, blank=True)
    status = models.CharField(_('Status'), max_length=50, choices=status_choices, default='Active')

    class Meta:
        verbose_name = 'Subscription'
        verbose_name_plural = 'Subscriptions'
        db_table = 'subscriptions-list'

    def __str__(self):
        return self.membership.title

    def save(self, *args, **kwargs):
        now = timezone.now()
        if now > self.endDate:
            self.status = 'Expired'
        else:
            self.status = 'Active'
        super(Subscription, self).save(*args, **kwargs)