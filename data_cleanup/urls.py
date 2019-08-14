"""Data cleanup section urls."""
from django.contrib.auth.decorators import login_required
from django.conf.urls import patterns, url

from .views import DataQualityView, CasePlanDataQualityView

urlpatterns = patterns(
    'data_cleanup.views',
    url(r'^filter/$', login_required(
        DataQualityView.as_view()), name='data_cleanup'),
    url(r'^filter/case_plan$', login_required(
        CasePlanDataQualityView.as_view()), name='data_cleanup_case_plan')
)
