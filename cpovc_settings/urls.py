"""Urls for Settings."""
from django.conf.urls import patterns, url

# This should contain urls related to settings ONLY
urlpatterns = patterns(
    'cpovc_settings.views',
    url(r'^$', 'settings_home', name='settings_home'),
    url(r'^reports/d/(?P<file_name>[0-9_\-_A-Za-z_\._A-Za-z]+)$',
        'archived_reports', name='archived_reports'),
    url(r'^reports/r/(?P<file_name>[0-9_\-_A-Za-z_\._A-Za-z]+)$',
        'remove_reports', name='remove_reports'),
    url(r'^reports/$', 'settings_reports', name='settings_reports'),
    url(r'^facilities/$', 'settings_facilities', name='settings_facilities'),
    url(r'^schools/$', 'settings_schools', name='settings_schools'),
    url(r'^data/$', 'settings_rawdata', name='settings_rawdata'),
    url(r'^changes/$', 'change_notes', name='change_notes'),)
