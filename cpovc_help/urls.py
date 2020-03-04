"""Urls for Settings."""
from django.conf.urls import patterns, url

# This should contain urls related to settings ONLY
urlpatterns = patterns(
    'cpovc_help.views',
    url(r'^downloads/$', 'help_downloads', name='help_downloads'),
    url(r'^download/(?P<name>[0-9A-Za-z_\-\.]+)$', 'doc_download', name='doc_download'),
    url(r'^faq/$', 'help_faq', name='help_faq'),
)