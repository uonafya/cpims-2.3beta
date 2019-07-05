from django.conf.urls import patterns, url

# This should contain urls related to registry ONLY
urlpatterns = patterns(
    # Forms Registry
    'cpovc_forms.views',
    url(r'^$', 'forms_home', name='forms'),
    url(r'^followups/$', 'forms_registry',
        name='forms_registry'),

    # Documents Manager
    url(r'^documents_manager/$', 'documents_manager',
        name='documents_manager'),
    url(r'^documents_manager_search/$', 'documents_manager_search',
        name='documents_manager_search'),

    # Case Record Sheet Urls
    url(r'^crs/$', 'case_record_sheet',
        name='case_record_sheet'),
    url(r'^crs/new/(?P<id>\d+)/$', 'new_case_record_sheet',
        name='new_case_record_sheet'),
    url(r'^crs/view/(?P<id>\w+)/$', 'view_case_record_sheet',
        name='view_case_record_sheet'),
    url(r'^crs/edit/(?P<id>\w+)/$', 'edit_case_record_sheet',
        name='edit_case_record_sheet'),
    url(r'^crs/delete/(?P<id>\w+)/$', 'delete_case_record_sheet',
        name='delete_case_record_sheet'),

    # Alternative Family Care Urls
    url(r'^afc/$', 'alternative_family_care',
        name='alternative_family_care'),
    url(r'^afc/new/(?P<id>\d+)/$', 'new_alternative_family_care',
        name='new_alternative_family_care'),
    url(r'^afc/edit/(?P<id>\w+)/$', 'edit_alternative_family_care',
        name='edit_alternative_family_care'),
    url(r'^afc/view/(?P<id>\w+)/$', 'view_alternative_family_care',
        name='view_alternative_family_care'),

    # Residential Placement
    url(r'^placement/save/$', 'save_placement',
        name='save_placement'),
    url(r'^placement/view/(?P<id>\w+)/$', 'view_placement',
        name='view_placement'),
    url(r'^placement/edit/(?P<id>\w+)/$', 'edit_placement',
        name='edit_placement'),
    url(r'^placement/delete/$', 'delete_placement',
        name='delete_placement'),
    url(r'^placement/$',
        'residential_placement', name='residential_placement'),
    url(r'^placement/(?P<id>\d+)/$',
        'placement', name='placement'),

    # Residential Placement FollowUp
    url(r'^placement_followup/(?P<id>\d+)/$',
        'placement_followup', name='placement_followup'),
    url(r'^save_placementfollowup/$',
        'save_placementfollowup', name='save_placementfollowup'),
    url(r'^view_placementfollowup/$',
        'view_placementfollowup', name='view_placementfollowup'),
    url(r'^edit_placementfollowup/$', 'edit_placementfollowup',
        name='edit_placementfollowup'),
    url(r'^delete_placementfollowup/$', 'delete_placementfollowup',
        name='delete_placementfollowup'),

    # Case Events (Encounters/Court Sessions/Referrals/Case
    # Closure/Summons)
    url(r'^case_events/(?P<id>\w+)/$', 'case_events',
        name='case_events'),
    # ---------------------------------------------------------
    url(r'^save_encounter/$', 'save_encounter',
        name='save_encounter'),
    url(r'^view_encounter/$', 'view_encounter',
        name='view_encounter'),
    url(r'^edit_encounter/$', 'edit_encounter',
        name='edit_encounter'),
    url(r'^delete_encounter/$', 'delete_encounter',
        name='delete_encounter'),
    # ----------------------------------------------------------
    url(r'^save_court/$', 'save_court', name='save_court'),
    url(r'^view_court/$', 'view_court',
        name='view_court'),
    url(r'^edit_court/$', 'edit_court',
        name='edit_court'),
    url(r'^delete_court/$', 'delete_court',
        name='delete_court'),
    # ----------------------------------------------------------
    url(r'^save_summon/$', 'save_summon', name='save_summon'),
    url(r'^edit_summon/$', 'edit_summon', name='edit_summon'),
    url(r'^view_summon/$', 'view_summon', name='view_summon'),
    url(r'^delete_summon/$', 'delete_summon',
        name='delete_summon'),
    # ----------------------------------------------------------
    url(r'^save_closure/$', 'save_closure', name='save_closure'),
    url(r'^edit_closure/$', 'edit_closure', name='edit_closure'),
    url(r'^view_closure/$', 'view_closure', name='view_closure'),
    url(r'^delete_closure/$', 'delete_closure', name='delete_closure'),

    # Referrals
    url(r'^delete_referral/$', 'delete_referral',
        name='delete_referral'),

    # Management Urls
    url(r'^manage_refferal/$', 'manage_refferal',
        name='manage_refferal'),
    url(r'^manage_refferal001/$', 'manage_refferal001',
        name='manage_refferal001'),
    url(r'^manage_refferal002/$', 'manage_refferal002',
        name='manage_refferal002'),
    url(r'^manage_refferal003/$', 'manage_refferal003',
        name='manage_refferal003'),
    url(r'^manage_casecategory001/$', 'manage_casecategory001',
        name='manage_casecategory001'),
    url(r'^manage_casecategory002/$', 'manage_casecategory002',
        name='manage_casecategory002'),
    url(r'^manage_casecategory003/$', 'manage_casecategory003',
        name='manage_casecategory003'),
    url(r'^manage_casecategory004/$', 'manage_casecategory004',
        name='manage_casecategory004'),
    url(r'^manage_encounters001/$', 'manage_encounters001',
        name='manage_encounters001'),
    url(r'^manage_encounters004/$', 'manage_encounters004',
        name='manage_encounters004'),
    url(r'^manage_case_events/$', 'manage_case_events',
        name='manage_case_events'),
    url(r'^manage_placementfollowup/$', 'manage_placementfollowup',
        name='manage_placementfollowup'),
    url(r'^manage_schools/$', 'manage_schools',
        name='manage_schools'),
    url(r'^manage_countries/$', 'manage_countries',
        name='manage_countries'),
    url(r'^manage_casehistory/$', 'manage_casehistory',
        name='manage_casehistory'),
    url(r'^manage_service_category/$', 'manage_service_category',
        name='manage_service_category'),
    url(r'^manage_form_type/$', 'manage_form_type',
        name='manage_form_type'),
    # ---------------------------------------------------------------
    url(r'^userorgunits_lookup/$', 'userorgunits_lookup',
        name='userorgunits_lookup'),
    url(r'^usersubcounty_lookup/$', 'usersubcounty_lookup',
        name='usersubcounty_lookup'),
    url(r'^userward_lookup/$', 'userward_lookup',
        name='userward_lookup'),
    url(r'^generate_serialnumber/$', 'generate_serialnumber',
        name='generate_serialnumber'),
    url(r'^getJsonObject001/$', 'getJsonObject001',
        name='getJsonObject001'),

    # Search Urls
    url(r'^ovc_search/$', 'ovc_search', name='ovc_search'),

    # School & Bursary Urls
    url(r'^education/$', 'background_details',
        name='background_details'),
    url(r'^education/new/(?P<id>\d+)/$',
        'new_education_info', name='new_education_info'),
    url(r'^education/edit/(?P<id>\w+)/$',
        'edit_education_info', name='edit_education_info'),
    url(r'^education/view/(?P<id>\w+)/$',
        'view_education_info', name='view_education_info'),
    url(r'^education/delete/(?P<id>\w+)/$',
        'delete_education_info', name='delete_education_info'),
    # -----------------------------------------------------------------
    url(r'^school/$',
        'new_school', name='new_school'),
    # ------------------------------------------------------------------
    url(r'^bursary/new/$',
        'new_bursary_info', name='new_bursary_info'),
    url(r'^bursary/edit/$',
        'edit_bursary_info', name='edit_bursary_info'),
    url(r'^bursary/view/$',
        'view_bursary_info', name='view_bursary_info'),
    url(r'^bursary/delete/$',
        'delete_bursary_info', name='delete_bursary_info'),
    url(r'^bursary/followup/(?P<id>\d+)/$',
        'bursary_followup', name='bursary_followup'),
    url(r'^bursary/manage/$',
        'manage_bursary', name='manage_bursary'),
    # OVC Care - CSI
    url(r'^csi/$',
        'csi', name='csi'),
    url(r'^csi/new/(?P<id>\d+)/$',
        'new_csi', name='new_csi'),
    url(r'^csi/edit/(?P<id>\w+)/$',
        'edit_csi', name='edit_csi'),
    url(r'^csi/view/(?P<id>\w+)/$',
        'view_csi', name='view_csi'),
    url(r'^csi/delete/(?P<id>\w+)/$',
        'delete_csi', name='delete_csi'),
        
    # OVC Care - Form1A
    url(r'^form1a/new/(?P<id>\d+)/$',
        'form1a_events', name='form1a_events'),
    url(r'^form1a/save/$',
        'save_form1a', name='save_form1a'),
    url(r'^form1a/update/$',
        'update_form1a', name='update_form1a'),
    url(r'^form1a/edit/(?P<id>\d+)/(?P<btn_event_type>\w+)/(?P<btn_event_pk>.+)/$',
        'edit_form1a', name='edit_form1a'),
    url(r'^form1a/view/$',
        'view_form1a', name='view_form1a'),
    url(r'^form1a/delete/(?P<id>\d+)/(?P<btn_event_type>\w+)/(?P<btn_event_pk>.+)/$',
        'delete_form1a', name='delete_form1a'),
    url(r'^form1a/delete_previous_event_entry/(?P<btn_event_type>\w+)/(?P<entry_id>.+)/$',
            'delete_previous_event_entry', name='delete_previous_event_entry'),
    url(r'^form1a/manage/$',
        'manage_form1a_events', name='manage_form1a_events'),
    # end OVC Care - Form1A

    # OVC Care - Form1B
    url(r'^form1b/new/(?P<id>\d+)/$',
        'new_form1b', name='new_form1b'),
    url(r'^form1b/delete/(?P<id>\d+)/(?P<btn_event_pk>.+)/$',
        'delete_form1b', name='delete_form1b'),
    url(r'^form1b/manage/$',
        'manage_form1b_events', name='manage_form1b_events'),
    # OVC Care - Form1B

    # OVC Care - HHVA
    url(r'^hhva/new/(?P<id>\d+)/$',
        'new_hhva', name='new_hhva'),
    url(r'^hhva/edit/(?P<id>\w+)/$',
        'edit_hhva', name='edit_hhva'),
    url(r'^hhva/view/(?P<id>\w+)/$',
        'view_hhva', name='view_hhva'),
    url(r'^hhva/delete/(?P<id>\w+)/$',
        'delete_hhva', name='delete_hhva'),
    # Presidential Bursary
    url(r'^bursary/list/(?P<id>\d+)/$',
        'list_bursary', name='list_bursary'),
    url(r'^bursary/view/(?P<id>[0-9A-Za-z_\-{32}\Z]+)/$',
        'view_bursary', name='view_bursary'),
    url(r'^bursary/new/(?P<id>\d+)/$',
        'new_bursary', name='new_bursary'),
    url(r'^bursary/edit/(?P<id>[0-9A-Za-z_\-{32}\Z]+)/$',
        'edit_bursary', name='edit_bursary'),
    url(r'^bursary/form/(?P<id>[0-9A-Za-z_\-{32}\Z]+)/$',
        'form_bursary', name='form_bursary'),
    # OVC Care - CPARA Form
    url(r'^cpara/new/(?P<id>\d+)/$',
        'new_cpara', name='new_cpara'),
    url(r'^cpara/delete/(?P<id>\d+)/(?P<btn_event_pk>.+)/$',
        'delete_cpara', name='delete_cpara'),

    # OVC Care - Case Plan Template
    url(r'^caseplan/new/(?P<id>\d+)/$',
        'case_plan_template', name='new_caseplan'),
    url(r'^caseplan/update/(?P<ovcid>\d+)/(?P<event_id>.+)/$',
        'update_caseplan', name='update_caseplan'),
    url(r'^caseplan-monitoring/new/(?P<id>\d+)/$', 'new_case_plan_monitoring', name='new_caseplan_monitoring'),

    #wellbeing Adult and Child
    url(r'^wellbeing/new/(?P<id>\d+)/$',
        'new_wellbeing', name='new_wellbeing'),
    #wellbeing Adolescent
    url(r'^wellbeingadolescent/new/(?P<id>\d+)/$',
        'new_wellbeingadolescent', name='new_wellbeingadolescent'),
    # hiv_status
    url(r'^HIVstatus/$',
        'hiv_status', name='hiv_status'),
        
    # HIV Risk Assessment Form
    url(r'^hivscreeningtool/new/(?P<id>\d+)/$',
        'new_hivscreeningtool', name='new_hivscreeningtool'),

     # HIV Risk Management Form
    url(r'^hivmanagementform/new/(?P<id>\d+)/$',
        'new_hivmanagementform', name='new_hivmanagementform'),

)
