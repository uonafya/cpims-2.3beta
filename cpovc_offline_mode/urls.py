"""OVC care section urls."""
from django.conf.urls import patterns, url

# This should contain urls related to registry ONLY
urlpatterns = patterns(
    'cpovc_offline_mode.views',
    url(r'^templates/$', 'templates', name='templates'),
    url(r'^data/$', 'fetch_data', name='fetch_data'),
    url(r'^test/$', 'offline_mode_test', name='offline_mode_test'),
)
