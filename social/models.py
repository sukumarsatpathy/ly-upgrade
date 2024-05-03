import uuid
from django.db import models
from django.utils.translation import gettext_lazy as _
from accounts.models import Account


status_choices = (
    ('Published', 'Published'),
    ('Reported', 'Reported'),
)


class Feeds(models.Model):
    feeds = models.TextField(_('Feeds'))
    image = models.ImageField(_('Image'), upload_to='social/feeds/%Y/%m/%d/', null=True, blank=True)
    user = models.ForeignKey(Account, on_delete=models.CASCADE, null=True)
    views = models.IntegerField(_('Views'), default=0)
    status = models.CharField(_('Status'), max_length=15, choices=status_choices, default='Published')
    created_date = models.DateTimeField(_('Created Date'), auto_now_add=True, editable=False)

    class Meta:
        verbose_name = 'Feed'
        verbose_name_plural = 'Feeds'
        db_table = 'feeds-list'

    def __str__(self):
        return f'{self.user.full_name}- feed'