"""Urls for reports."""
from django.conf.urls import patterns, url

# This should contain urls related to reports ONLY
urlpatterns = patterns(
    'cpovc_reports.views',
    url(r'^$', 'reports_home', name='reports'),
    url(r'^documents/$', 'reports_home',
        name='document_reports'),
    url(r'^(?P<id>\d+)/$', 'reports_cpims',
        name='cpims_reports'),
    url(r'^caseload/$', 'reports_caseload',
        name='caseload_reports'),
    url(r'^get_viral_load_report/$', 'get_viral_load_report',
            name='get_viral_load_report'),
    url(r'^manage/$', 'manage_reports',
        name='manage_reports'),
    url(r'^dashboard/$', 'manage_dashboard',
        name='manage_dashboard'),
    url(r'^download/(?P<file_name>[0-9A-Za-z_\.=\-\' ]+)$',
        'reports_download', name='download_reports'),
    url(r'^generate/$', 'reports_generate',
        name='generate_reports'),
    url(r'^pivot/$', 'reports_pivot',
        name='pivot_reports'),
    url(r'^data/$', 'reports_rawdata',
        name='pivot_rawdata'),
    url(r'^datim/$', 'reports_ovc_pivot',
        name='pivot_ovc_reports'),
    url(r'^datim_mer/$', 'reports_ovc_datim_mer_pivot',
        name='pivot_ovc_reports_mer'),
    url(r'^datim_mer23/$', 'reports_ovc_datim_mer23_pivot',
        name='pivot_ovc_reports_mer23'),
    url(r'^pepfar/$', 'reports_ovc_pepfar',
        name='pivot_ovc_pepfar'),
    url(r'^kpi/$', 'reports_ovc_kpi',
        name='pivot_ovc_kpi'),
    url(r'^viral_load/$', 'viral_load',
            name='viral_load'),
    url(r'^ovcdata/$', 'reports_ovc_rawdata',
        name='pivot_ovc_rawdata'),
    url(r'^download/$', 'reports_ovc_download',
        name='ovc_download'),
    url(r'^ovc/(?P<id>\d+)/$', 'reports_ovc',
        name='reports_ovc'),
    url(r'^dashboard/data/$', 'dashboard_details',
        name='dashboard_details'),
    url(r'^cluster/$', 'cluster', name='cluster'),
    url(r'^ovc/$', 'reports_ovc_list', name='reports_ovc_list'),
     url(r'^bursary/$', 'reports_bursary', name='bursary_reports'),
    )


