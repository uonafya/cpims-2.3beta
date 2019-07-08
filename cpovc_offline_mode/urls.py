"""OVC care section urls."""
from django.conf.urls import patterns, url

# This should contain urls related to registry ONLY
urlpatterns = patterns(
	'cpovc_offline_mode.views',
	url(r'^$', 'fetch_forms', name='fetch_forms'),
	url(r'^data/(?P<id>\d+)/$', 'fetch_data', name='fetch_data'),
	url(r'^test/$', 'offline_mode_test', name='offline_mode_test'),
)
