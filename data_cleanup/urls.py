"""Data cleanup section urls."""
from django.contrib.auth.decorators import login_required
from django.conf.urls import patterns, url

from .views import DataQualityView
# This should contain urls related to registry ONLY
urlpatterns = patterns(
    'data_cleanup.views',
    url(r'^filter/$', login_required(DataQualityView.as_view()), name='data_cleanup')
)