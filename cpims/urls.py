"""
cpims URL Configuration.

Other urls are import
Put here only urls not specific to app
"""
from django.conf.urls import include, url
from django.contrib import admin
from cpovc_auth import urls as auth_urls
from cpovc_registry import urls as registry_urls
from cpovc_forms import urls as forms_urls
from cpovc_reports import urls as reports_urls
from cpovc_gis import urls as gis_urls
from cpovc_api import urls as api_urls
from cpovc_ovc import urls as ovc_urls
from cpovc_settings import urls as settings_urls
from django.contrib.auth.views import (
    password_reset_done, password_change, password_change_done)
from cpovc_auth.views import password_reset
from django.views.generic import TemplateView

from cpovc_access.forms import StrictPasswordChangeForm


urlpatterns = [
    url(r'^admin/', include(admin.site.urls), name='admin'),
    # url(r'^$', 'cpovc_auth.views.log_in', name='home'),
    url(r'^$', 'cpims.views.home', name='home'),
    url(r'^accounts/request/$', 'cpims.views.access', name='access'),
    url(r'^accounts/terms/(?P<id>\d+)/$', 'cpovc_access.views.terms',
        name='terms'),
    url(r'^login/$', 'cpovc_auth.views.log_in', name='login'),
    url(r'^logout/$', 'cpovc_auth.views.log_out', name='logout'),
    url(r'^register/$', 'cpovc_auth.views.register', name='register'),
    url(r'^auth/', include(auth_urls)),
    url(r'^registry/', include(registry_urls)),
    url(r'^forms/', include(forms_urls)),
    url(r'^reports/', include(reports_urls)),
    url(r'^gis/', include(gis_urls)),
    url(r'^api/', include(api_urls)),
    url(r'^ovcare/', include(ovc_urls)),
    url(r'^settings/', include(settings_urls)),
    url(r'^accounts/login/$', 'cpovc_auth.views.log_in', name='login'),
    url(r'^accounts/password/reset/$', password_reset,
        {'template_name': 'registration/password_reset.html'},
        name='password_reset'),
    url(r'^accounts/password/reset/done/$', password_reset_done,
        {'template_name': 'registration/password_reset_done.html'},
        name='password_reset_done'),
    url(r'^accounts/reset/confirm/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>.+)/$',
        'cpovc_auth.views.reset_confirm', name='password_reset_confirm'),
    url(r'^reset/$', 'cpovc_auth.views.reset', name='reset'),
    url(r'^accounts/password/change/$', password_change,
        {'post_change_redirect': '/accounts/password/change/done/',
         'template_name': 'registration/password_change.html',
         'password_change_form': StrictPasswordChangeForm},
        name='password_change'),
    url(r'^accounts/password/change/done/$', password_change_done,
        {'template_name': 'registration/password_change_done.html'}),
    url(r'^F57665A859FE7CFCDB6C8935196374AD\.txt$',
        TemplateView.as_view(template_name='comodo.txt',
                             content_type='text/plain')),
    url(r'^robots\.txt$', TemplateView.as_view(template_name='robots.txt',
                                               content_type='text/plain'))]

handler400 = 'cpims.views.handler_400'
handler404 = 'cpims.views.handler_404'
handler500 = 'cpims.views.handler_500'

admin.site.site_header = 'CPIMS Administration'
admin.site.site_title = 'CPIMS administration'
admin.site.index_title = 'CPIMS admin'
