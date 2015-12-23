# coding: utf-8
"""PIM User Module."""

from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

from django.utils import timezone
from django.conf import settings
from django.core.validators import RegexValidator
from django.utils.translation import ugettext_lazy as _

from common.validators import UnicodeMinWidthValidator
from common.constants import (
    USER_TYPE_GUEST, USER_TYPE_NORMAL, USER_TYPE_ADMIN,
    USER_TYPE_CHOICE
)

class PimUserGroup(models.Model):

    """Pim user group. """

    group_name = models.CharField(
        _('group name'),
        validators=[
            RegexValidator(
                regex=u'^[a-zA-Z0-9_ @.\u4e00-\u9fa5]+$',
                message='name must be certain charactors',
                code='invalid_fmt_name'
            ),
            UnicodeMinWidthValidator(4)
        ],
        blank=True,
        max_length=60,
        unique=True,
    )
    date_joined = models.DateTimeField(
        _('date joined'),
        auto_now_add=True,
    )
    description = models.CharField(
        _('group description'),
        max_length=200,
        blank=True,
    )

    def __unicode__(self):
        """String representation."""
        return self.group_name

class PimUserManager(BaseUserManager):

    """Customized pim user mananger."""

    def create_user(self, username, password, email, cellphone=None, user_type=USER_TYPE_NORMAL):
        """Just a wrapper to create user."""
        if not username or not email or not password:
            return None

        user = self.model(username=username,
                          cellphone=cellphone,
                          email=email,
                          user_type=user_type)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create(self, username, password, email, cellphone=None, user_type=USER_TYPE_NORMAL):
        return self.create_user(username, password, email, cellphone, user_type)

class PimUser(AbstractBaseUser):
    username = models.CharField(
        _('username'),
        validators=[
            RegexValidator(
                regex=u'^[a-zA-Z0-9_ @.\u4e00-\u9fa5]+$',
                message='username must be certain charactors',
                code='invalid_fmt_username'
            ),
            UnicodeMinWidthValidator(4)
        ],
        max_length=30,
        unique=True
    )
    email = models.EmailField(
        _('email address'),
        max_length=254,
        unique=True,
        null=True
    )
    is_email_confirmed = models.BooleanField(
        _('email confirmation status'),
        default=False,
        blank=True
    )
    cellphone = models.CharField(
        _('cellphone'),
        validators=[
            RegexValidator(
                regex='^1[0-9]{10}$',
                message='invalid cellphone number format',
                code='invalid_fmt_cellphone'
            )
        ],
        max_length=30,
        unique=True,
        null=True,
        blank=True
    )
    group = models.CharField(
        _('group'),
        max_length=254,
        null=True,
        blank=True
    )
    date_joined = models.DateTimeField(
        _('date joined'),
        default=timezone.now,
        blank=True
    )
    is_active = models.BooleanField(
        _('whether use is enable or not'),
        default=True,
        blank=True
    )
    frozen_time = models.DateTimeField(
        _('the time user is frozen'),
        auto_now=False,
        auto_now_add=False,
        blank=True,
        null=True
    )
    user_type = models.IntegerField(
        _('user type'),
        default=USER_TYPE_NORMAL,
        choices=USER_TYPE_CHOICE,
    )

    objects = PimUserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELD = ['email']

    class Meta:

        """Define default ordering field."""

        verbose_name = _('pimuser')
        verbose_name_plural = _('pimusers')
        ordering = ('date_joined',)

    def get_full_name(self):
        """The user is identified by their username."""
        return self.username

    def get_short_name(self):
        """The user is identified by their username."""
        return self.username

    def __unicode__(self):
        """The user representation."""
        return self.username

    def has_perm(self, perm, obj=None):
        """Whether the user have a specific permission or not."""
        return True

    def has_module_perms(self, app_label):
        """Whether the user have permissions to view the app or not."""
        return True
