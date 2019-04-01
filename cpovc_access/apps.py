"""Accessp app with password policies."""
from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class AccessAppConfig(AppConfig):
    """Password policies."""

    name = 'cpovc_access'
    verbose_name = _('Password Policy')
