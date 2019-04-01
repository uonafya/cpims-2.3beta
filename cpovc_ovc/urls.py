"""OVC care section urls."""
from django.conf.urls import patterns, url

# This should contain urls related to registry ONLY
urlpatterns = patterns(
    'cpovc_ovc.views',
    url(r'^$', 'ovc_home', name='ovc_home'),
    url(r'^ovc/search/$', 'ovc_search', name='ovc_search'),
    url(r'^ovc/new/(?P<id>\d+)/$',
        'ovc_register', name='ovc_register'),
    url(r'^ovc/edit/(?P<id>\d+)/$',
        'ovc_edit', name='ovc_edit'),
    url(r'^ovc/view/(?P<id>\d+)/$',
        'ovc_view', name='ovc_view'),
    url(r'^ovc/manage/$', 'ovc_manage', name='ovc_manage'),
    url(r'^hh/view/(?P<hhid>[0-9A-Za-z_\-]+)/$',
        'hh_manage', name='hh_manage'),)
