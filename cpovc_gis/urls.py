"""Urls for GIS."""
from django.conf.urls import patterns, url

# This should contain urls related to GIS Module ONLY
urlpatterns = patterns(
    'cpovc_gis.views',
    url(r'^$', 'gis_home', name='gis_home'),
    url(r'^data/$', 'gis_data', name='gis_data'),)
