# coding: utf-8
"""Kinds of validators."""

import re

from django.utils.translation import ugettext_lazy as _
from django.core.validators import BaseValidator, RegexValidator

class UnicodeMinWidthValidator(BaseValidator):

    """Unicode min-width validator."""

    def compare(self, a, b):
        return a < b

    def clean(self, x):
        return len(x.encode('utf-8'))

    message = _(
        'Ensure this value has at least %(limit_value)d character '
        '(it has %(show_value)d).',
        'Ensure this value has at least %(limit_value)d characters '
        '(it has %(show_value)d).',
        'limit_value'
    )
    code = 'min_unicode_length'


class UnicodeMaxWidthValidator(BaseValidator):

    """Unicode max-width validator."""

    def compare(self, a, b):
        return a > b

    def clean(self, x):
        return len(x.encode('utf-8'))

    message = _(
        'Ensure this value has at least %(limit_value)d character '
        '(it has %(show_value)d).',
        'Ensure this value has at least %(limit_value)d characters '
        '(it has %(show_value)d).',
        'limit_value'
    )
    code = 'max_unicode_length'


class PasswordValidator(RegexValidator):

    """Password validator."""

    regex = re.compile(r'^[a-zA-Z0-9@#$%^&*]{6,16}')
    message = _('enter a valid password.')
