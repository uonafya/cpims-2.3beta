"""Accessp app with password policies."""
from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class OVCAppConfig(AppConfig):
    """Password policies."""

    name = 'cpovc_ovc'
    verbose_name = _('OVC Care')
