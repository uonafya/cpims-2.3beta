"""URLs for authentication module."""
from django.conf.urls import patterns, url

# This should contain urls related to auth app ONLY
urlpatterns = patterns('cpovc_auth.views',
                       url(r'^$', 'home'),
                       url(r'^register/$', 'register'),
                       url(r'^ping/$', 'user_ping', name='user_ping'),
                       url(r'^roles/$', 'roles_home', name='roles_home'),
                       url(r'^roles/edit/(?P<user_id>\d+)/$', 'roles_edit',
                           name='roles_edit'),
                       )
