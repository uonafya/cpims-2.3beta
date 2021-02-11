"""Urls for Settings."""
from django.conf.urls import patterns, url

# This should contain urls related to settings ONLY
urlpatterns = patterns(
    'cpovc_manage.views',
    url(r'^$', 'manage_home', name='manage_home'),
    url(r'^travel/$', 'home_travel', name='home_travel'),
    url(r'^integration/$', 'integration_home', name='integration_home'),
    url(r'^travel/edit/(?P<id>\d+)/$', 'edit_travel', name='edit_travel'),
    url(r'^travel/view/(?P<id>\d+)/$', 'view_travel', name='view_travel'),
    url(r'^travel/pdf/(?P<id>\d+)/$', 'travel_report', name='travel_report'),
)
