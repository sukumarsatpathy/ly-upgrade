import uuid
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from accounts.models import Account


class AccountToken(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    self_token = models.UUIDField(_('Self Token Number'), default=uuid.uuid4, editable=False)
    parent_token = models.CharField(_('Parent Token Number'), max_length=100, null=True)
    created_date = models.DateTimeField(_('Created Date'), auto_now_add=True)

    class Meta:
        verbose_name = 'Account Token'
        verbose_name_plural = 'Account Tokens'
        db_table = 'tokens-account'

    def __str__(self):
        return self.user.full_name


class LeaderUniqueToken(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    amount = models.IntegerField()
    quantity = models.IntegerField()
    count = models.IntegerField(_('Registration Count'), default=0)
    token = models.UUIDField(_('Self Token Number'), default=uuid.uuid4)
    created_date = models.DateTimeField(default=timezone.now)
    status = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'Leader Registration'
        verbose_name_plural = 'Leader Registration'
        db_table = 'tokens-leader-registration'

    def __str__(self):
        return self.token


class TeacherUniqueToken(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    amount = models.IntegerField()
    quantity = models.IntegerField()
    count = models.IntegerField(_('Registration Count'), default=0)
    token = models.UUIDField(_('Self Token Number'), default=uuid.uuid4)
    created_date = models.DateTimeField(default=timezone.now)

    class Meta:
        verbose_name = 'Teacher Registration'
        verbose_name_plural = 'Teacher Registration'
        db_table = 'tokens-teacher-registration'

    def __str__(self):
        return self.token