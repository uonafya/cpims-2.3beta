"""Data cleanup section urls."""
from django.conf.urls import patterns, url

from .views import DataCleaUpView
# This should contain urls related to registry ONLY
urlpatterns = patterns(
    'data_cleanup.views',
    url(r'^filter/$', DataCleaUpView.as_view(), name='data_cleanup')
)