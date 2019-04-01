from django import forms
from django.utils.translation import ugettext_lazy as _
from django.forms.widgets import RadioFieldRenderer
from django.utils.encoding import force_unicode
from django.utils.safestring import mark_safe
from cpovc_main.functions import get_list, get_org_units_list
from cpovc_registry.functions import get_geo_list, get_all_geo_list
from cpovc_registry.models import RegOrgUnit
from cpovc_main.models import SchoolList
# New lists
YESNO_CHOICES = (('AYES', 'Yes'), ('ANNO', 'No'))
bursary_school_type_list = (('STPR', 'Private'), ('STPU', 'Public'))
bursary_school_category_list = (('SCNA', 'National'), ('SCCT', 'County'), ('SCSC', 'Sub-County'))
bursary_school_enrolled_list = (('SEDY', 'Day'), ('SEBO', 'Boarding'), ('SESP', 'Special'))
principal_list = (('PRNC', 'Principal'), ('DPRN', 'Deputy Principal'))
chief_list = (('CHIF', 'Chief'), ('SCHF', 'Sub-Chief'))
bank_list = (('', 'Please Select'), ('1', 'Equity Bank'))
# -------------------------------- CPIMS-------------------------------------
person_type_list = get_list('person_type_id', 'Please Select')
psearch_criteria_list = get_list('psearch_criteria_type_id', 'Select Criteria')
povcsearch_criteria_list = get_list(
    'povcsearch_criteria_type_id', 'Select Criteria')
form_type_list = get_list('form_type_id', 'Please Select')
religion_type_list = get_list('religion_type_id', 'Please Select')
yesno_list = get_list('yesno_id', 'Please Select')
household_economics_list = get_list('household_economics', 'Please Select')
school_category_list = get_list('school_category_id', 'Please Select')
class_list = get_list('class_level_id', 'Please Select')
family_status_list = get_list('family_status_id', 'Please Select')
mental_condition_list = get_list('mental_condition_id', 'Please Select')
mental_subcondition_list = get_list('mental_subcondition_id', 'Please Select')
physical_condition_list = get_list('physical_condition_id', 'Please Select')
physical_subcondition_list = get_list(
    'physical_subcondition_id', 'Please Select')
other_condition_list = get_list('other_condition_id', 'Please Select')
other_subcondition_list = get_list('other_subcondition_id', 'Please Select')
perpetrator_status_list = get_list('perpetrator_status_id', 'Please Select')
sex_id_list = get_list('sex_id', 'Please Select')
relationship_type_list = get_list('relationship_type_id', 'Please Select')
case_nature_list = get_list('case_nature_id', 'Please Select')
case_category_list = get_list('case_category_id', 'Please Select')
intervention_list = get_list('intervention_id', 'Please Select')
risk_level_list = get_list('risk_level_id', 'Please Select')
event_place_list = get_list('event_place_id', 'Please Select')
referral_destination_list = get_list(
    'referral_destination_id', 'Please Select')
referral_destination_classification_list = get_list(
    'referral_destination_classification', 'Please Select')
geo_list = get_geo_list(get_all_geo_list(), 'GDIS')
referral_to_list = get_list('referral_type_id', 'Please Select')
core_item_list = get_list('core_item_id', '')
court_order_list = get_list('court_order_id', '')
residential_status_list = get_list('residential_status_id', 'Please Select')
document_type_list = get_list('document_tag_id', 'Please Select Document')
all_list = get_all_geo_list()
county_list = [('', 'Please Select')] + list(get_geo_list(all_list, 'GPRV'))
sub_county_list = [('', 'Please Select')] + \
    list(get_geo_list(all_list, 'GDIS'))
ward_list = [('', 'Please Select')] + list(get_geo_list(all_list, 'GWRD'))
institution_type_list = get_list('institution_type_id', 'Please Select')
admission_type_list = get_list('admission_type_id', 'Please Select')
# admission_reason_list = get_list('placement_reason_id', 'Please Select')
admission_reason_list = get_list('admission_reason_id', 'Please Select')
adverse_events_list = get_list('adverse_event_id', 'Please Select')
adverse_offence_list = get_list('offender_id', 'Please Select')
adverse_medical_list = get_list('new_condition_id', 'Please Select')
attendance_type_list = get_list('type_of_attendance', 'Please Select')
hospital_referral_type_list = get_list(
    'hospital_referral_type_id', 'Please Select')
discharge_type_list = get_list('discharge_type_id', 'Please Select')
# admission_class_list = get_list('admission_class_id', 'Please Select')
admission_class_list = get_list('class_level_id', 'Please Select')
vocational_training_list = get_list('vocational_training_id', 'Please Select')
service_provider_list = get_list('service_provider_id', 'Please Select')
services_list = get_list('core_item_id', 'Please Select')
court_outcome_list = get_list('court_outcome_id', 'Please Select')
application_outcome_list = get_list('application_outcome_id', 'Please Select')
courtsession_type_list = get_list('courtsession_type_id', 'Please Select')
plea_type_list = get_list('plea_type_id', 'Please Select')
case_reporter_list = get_list('case_reporter_id', 'Please Select')
placementfollowup_type_list = get_list(
    'follow_up_type_id', 'Please Select Followup Type')
alternative_family_care_type_list = get_list(
    'alternative_family_care_type_id', 'Please Select')
type_of_adoption_list = get_list('adoption_id', 'Please Select')
bursary_type_list = get_list('bursary_type_id', 'Select Bursary Type')
school_type_list = get_list('school_category_id', 'Please Select')
term_list = get_list('school_term_id', 'Select Term Awarded')
schoolout_reason_list = get_list('out_of_school_id', 'Please Select')
school_admission_type_list = get_list('school_type_id', 'Please Select')
education_level_list = get_list('class_level_id', 'Please Select')
longterm_needs_list = get_list('long_term_support_id', 'Please Select')
shortterm_needs_list = get_list('immediate_need_id', 'Please Select')
period_list = get_list('period_id', 'Please Select Unit')
parental_status_list = get_list('parental_status_id', 'Please Select')
caseoutcome_list = get_list('closure_outcome_id', 'Please Select')

#----------------------------------OLMIS-------------------------------------~
csi_grade_list = get_list('csi_grade_id', 'Please Select')
olmis_domain_list = get_list('olmis_domain_id', 'Please Select')
olmis_assessment_domain_list = get_list(
    'olmis_assessment_domain_id', 'Please Select')
olmis_service_provider_list = get_list(
    'olmis_service_provider_id', 'Please Select')
olmis_critical_events_list = get_list(
    'olmis_critical_event_id', 'Please Select')
olmis_ha5_list = get_list('olmis_ha5_id', 'Please Select')
olmis_ha6_list = get_list('olmis_ha6_id', 'Please Select')
olmis_ha7_list = get_list('olmis_ha7_id', 'Please Select')
olmis_ha8_list = get_list('olmis_ha8_id', 'Please Select')
olmis_ha9_list = get_list('olmis_ha9_id', 'Please Select')
olmis_ha10_type_list = get_list('olmis_ha10_type_id', 'Please Select')
olmis_ha10_condition_list = get_list('olmis_ha10_condition_id', 'Please Select')
olmis_ha11_list = get_list('olmis_ha11_id', 'Please Select')
olmis_ha12_list = get_list('olmis_ha12_id', 'Please Select')
olmis_ha13_list = get_list('olmis_ha13_id', 'Please Select')
olmis_ha14_list = get_list('olmis_ha14_id', 'Please Select')
olmis_ha15_list = get_list('olmis_ha15_id', 'Please Select')
olmis_ha16_list = get_list('olmis_ha16_id', 'Please Select')
olmis_ha17_list = get_list('olmis_ha17_id', 'Please Select')
olmis_ha18_list = get_list('olmis_ha18_id', 'Please Select')
olmis_ha19_list = get_list('olmis_ha19_id', 'Please Select')
olmis_ha20_list = get_list('olmis_ha20_id', 'Please Select')
olmis_ha21_list = get_list('olmis_ha21_id', 'Please Select')
olmis_ha22_list = get_list('olmis_ha22_id', 'Please Select')
olmis_ha23_list = get_list('olmis_ha23_id', 'Please Select')
olmis_ha24_list = get_list('olmis_ha24_id', 'Please Select')
olmis_ha25_list = get_list('olmis_ha25_id', 'Please Select')
olmis_ha28_list = get_list('olmis_ha28_id', 'Please Select')
olmis_ha29_list = get_list('olmis_ha29_id', 'Please Select')
olmis_ha30_list = get_list('olmis_ha30_id', 'Please Select')
olmis_ha31_list = get_list('olmis_ha31_id', 'Please Select')

class OVCSchoolForm(forms.Form):
    school_name = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': _('Name of School'),
               'class': 'form-control',
               'id': 'school_name',
               'data-parsley-required': "true",
               'data-parsley-group': 'group0'
               }))

    type_of_school = forms.ChoiceField(choices=school_type_list,
                                       initial='0',
                                       widget=forms.Select(
                                           attrs={'class': 'form-control',
                                                  'id': 'type_of_school',
                                                  'data-parsley-required': "true",
                                                  'data-parsley-group': 'group0'
                                                  }))
    school_subcounty = forms.ChoiceField(
        choices=sub_county_list,
        initial='0',
        widget=forms.Select(
            attrs={'class': 'form-control',
                   'id': 'school_subcounty',
                   'data-parsley-required': "true",
                   'data-parsley-group': "group0"}))
    school_ward = forms.ChoiceField(
        choices=ward_list, label=_('Select ward'),
        initial='',
        widget=forms.Select(
            attrs={'id': 'school_ward',
                   'class': 'form-control',
                   'data-parsley-required': "true",
                   'data-parsley-group': "group0"}))


class OVCBursaryForm(forms.Form):
    bursary_type = forms.ChoiceField(choices=bursary_type_list,
                                     initial='0',
                                     widget=forms.Select(
                                         attrs={'class': 'form-control',
                                                'id': 'bursary_type',
                                                'data-parsley-required': "true",
                                                'data-parsley-group': 'group0'
                                                }))
    disbursement_date = forms.DateField(widget=forms.TextInput(
        attrs={'placeholder': _('Disbursement Date'),
               'class': 'form-control',
               'id': 'disbursement_date',
               'data-parsley-required': "true",
               'data-parsley-group': 'group0'
               # type': 'hidden'
               }))

    amount = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': _('Amount(Ksh)'),
               'class': 'form-control',
               'id': 'amount',
               'data-parsley-required': "true",
               'data-parsley-type': "digits",
               'data-parsley-group': 'group0'
               }))

    year = forms.DateField(widget=forms.TextInput(
        attrs={'placeholder': _('Year Awarded(YYYY)'),
                           'class': 'form-control',
                           'id': 'year',
                           'data-parsley-required': "true",
                           'data-parsley-group': 'group0'
                           }))

    term = forms.ChoiceField(choices=term_list,
                             initial='0',
                             widget=forms.Select(
                                 attrs={'class': 'form-control',
                                        'id': 'term',
                                        'data-parsley-required': "true",
                                        'data-parsley-group': 'group0'
                                        }))
    person_id = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control',
               'id': 'person_id',
               'type': 'hidden'
               }))

    bursary_id = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control',
               'id': 'bursary_id',
               'type': 'hidden'}))
    operation_mode = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control',
               'id': 'operation_mode',
               'type': 'hidden'
               }))


class BackgroundDetailsForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(BackgroundDetailsForm, self).__init__(*args, **kwargs)
        # schools_list = [('', 'Please Select')] + list(SchoolList.objects.filter().values_list('school_id', 'school_name'))
        name_of_school = forms.ChoiceField(choices=(),
                                           initial='0',
                                           widget=forms.Select(
            attrs={'class': 'form-control',
                   'id': 'name_of_school',
                   'data-parsley-required': "true",
                   'data-parsley-group': 'group0'}))
        self.fields['name_of_school'] = name_of_school
    admmitted_to_school = forms.ChoiceField(choices=yesno_list,
                                            initial='0',
                                            widget=forms.Select(
                                                attrs={'class': 'form-control',
                                                       'id': 'admmitted_to_school',
                                                       'data-parsley-required': "true",
                                                       'data-parsley-group': 'group0'
                                                       }))
    not_in_school_reason = forms.ChoiceField(choices=schoolout_reason_list,
                                             initial='0',
                                             widget=forms.Select(
                                                 attrs={'class': 'form-control',
                                                        'id': 'not_in_school_reason',
                                                        'data-parsley-required': "true",
                                                        'data-parsley-group': 'group0'
                                                        }))
    admmission_type = forms.ChoiceField(choices=school_admission_type_list,
                                        initial='0',
                                        widget=forms.Select(
                                            attrs={'class': 'form-control',
                                                   'id': 'admmission_type',
                                                   'data-parsley-required': "true",
                                                   'data-parsley-group': 'group0'
                                                   }))
    admmission_class = forms.ChoiceField(choices=admission_class_list,
                                         initial='0',
                                         widget=forms.Select(
                                             attrs={'class': 'form-control',
                                                    'id': 'admmission_class',
                                                    'data-parsley-required': "true",
                                                    'data-parsley-group': 'group0'
                                                    }))
    admmission_subclass = forms.ChoiceField(choices=vocational_training_list,
                                            initial='0',
                                            widget=forms.Select(
                                                attrs={'class': 'form-control',
                                                       'id': 'admmission_subclass',
                                                       'data-parsley-required': "true",
                                                       'data-parsley-group': 'group0'
                                                       }))
    admission_date = forms.DateField(widget=forms.TextInput(
        attrs={'placeholder': _('Date Of Admission'),
               'class': 'form-control',
               'id': 'admission_date',
               'data-parsley-required': "true",
               'data-parsley-group': 'group0'
               }))
    education_comments = forms.CharField(widget=forms.Textarea(
        attrs={'placeholder': _('Education Comments'),
               'class': 'form-control',
               'id': 'education_comments',
               'data-parsley-group': 'group0',
               'rows': '2'}))
    school_name = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': _('Name of School'),
               'class': 'form-control',
               'id': 'school_name',
               'data-parsley-required': "true",
               'data-parsley-group': 'group0'
               }))

    type_of_school = forms.ChoiceField(choices=school_type_list,
                                       initial='0',
                                       widget=forms.Select(
                                           attrs={'class': 'form-control',
                                                  'id': 'type_of_school',
                                                  'data-parsley-required': "true",
                                                  'data-parsley-group': 'group0'
                                                  }))
    school_subcounty = forms.ChoiceField(
        choices=sub_county_list,
        initial='0',
        widget=forms.Select(
            attrs={'class': 'form-control',
                   'id': 'school_subcounty',
                   'data-parsley-required': "true",
                   'data-parsley-group': "group0"}))
    school_ward = forms.ChoiceField(
        choices=(), label=_('Select ward'),
        initial='',
        widget=forms.Select(
            attrs={'id': 'school_ward',
                   'class': 'form-control',
                   'data-parsley-required': "true",
                   'data-parsley-group': "group0"}))
    child_age = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control',
               'id': 'child_age',
               'type': 'hidden'
               }))


class DocumentsManager(forms.Form):
    document_type = forms.ChoiceField(choices=document_type_list,
                                      initial='0',
                                      required=True,
                                      widget=forms.Select(
                                          attrs={'class': 'form-control',
                                                 'id': 'document_type',
                                                 'data-parsley-required': 'true'})
                                      )
    document_description = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': _('Document Description'),
               'class': 'form-control',
               'id': 'document_description',
               'data-parsley-required': 'true'}))
    search_name = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': _('Enter Child Name(s)'),
               'class': 'form-control',
               'id': 'search_name',
               'data-parsley-required': 'true'}))
    file_name = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': _('File Name'),
               'class': 'form-control',
               'readonly': 'true',
               'id': 'file_name'}))
    search_criteria = forms.ChoiceField(choices=psearch_criteria_list,
                                        initial='0',
                                        required=True,
                                        widget=forms.Select(
                                            attrs={'class': 'form-control',
                                                   'id': 'search_criteria',
                                                   'data-parsley-required': 'true'})
                                        )
    person = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control',
               'id': 'person',
               'type': 'hidden',
               'data-parsley-required': "true",
               'data-parsley-group': 'group0'
               }))


class SearchForm(forms.Form):
    form_type = forms.ChoiceField(choices=form_type_list,
                                  initial='0',
                                  required=True,
                                  widget=forms.Select(
                                      attrs={'class': 'form-control',
                                             'id': 'form_type',
                                             'data-parsley-required': 'true'})
                                  )

    form_person = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': _('Enter Child Name'),
               'class': 'form-control',
               'id': 'form_person',
               'data-parsley-required': 'true'}))


class OVCSearchForm(forms.Form):
    person_type = forms.ChoiceField(choices=person_type_list,
                                    initial='0',
                                    required=True,
                                    widget=forms.Select(
                                        attrs={'class': 'form-control',
                                               'id': 'person_type',
                                               'data-parsley-required': 'true'})
                                    )

    search_name = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': _('Enter Child Name(s)'),
               'class': 'form-control',
               'id': 'search_name',
               'data-parsley-group': 'primary_',
               'data-parsley-required': 'true'}))

    search_criteria = forms.ChoiceField(choices=psearch_criteria_list,
                                        initial='0',
                                        required=True,
                                        widget=forms.Select(
                                            attrs={'class': 'form-control',
                                                   'id': 'search_criteria',
                                                   # 'readonly':'true',
                                                   'data-parsley-required': 'true'})
                                        )

    form_type_search = forms.ChoiceField(choices=form_type_list,
                                         initial='0',
                                         required=True,
                                         widget=forms.Select(
                                             attrs={'class': 'form-control',
                                                    'id': 'form_type_search',
                                                    'data-parsley-required': 'true'})
                                         )


class ResidentialFollowupForm(forms.Form):
    casecategorys = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control',
               'id': 'casecategorys',
               'type': 'hidden'
               #'data-parsley-required': "true",
               #'data-parsley-group': 'group0'
               }))
    person = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control',
               'id': 'person',
               'type': 'hidden'
               #'data-parsley-required': "true",
               #'data-parsley-group': 'group0'
               }))
    child_age = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control',
               'id': 'child_age',
               'type': 'hidden'
               }))
    placement_id = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control',
               'id': 'placement_id',
               'type': 'hidden'
               }))
    placementfollowup_id = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control',
               'id': 'placementfollowup_id',
               'type': 'hidden'
               }))
    placementfollowup_type = forms.ChoiceField(choices=placementfollowup_type_list,
                                               initial='0',
                                               widget=forms.Select(
                                                   attrs={'class': 'form-control',
                                                          'id': 'placementfollowup_type'
                                                          }))
    placementfollowup_date = forms.DateField(widget=forms.TextInput(
        attrs={'placeholder': _('Date Of Followup'),
               'class': 'form-control',
               'id': 'placementfollowup_date'
               }))
    placementfollowup_outcome = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': _('Outcome Of Followup'),
               'class': 'form-control',
               'id': 'placementfollowup_outcome'
               }))
    placementfollowup_details = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': _('Details Of Followup'),
               'class': 'form-control',
               'id': 'placementfollowup_details'
               }))
    adverse_events = forms.ChoiceField(choices=adverse_events_list,
                                       initial='0',
                                       widget=forms.Select(
                                           attrs={'class': 'form-control',
                                                  'id': 'adverse_events'
                                                  #'data-parsley-required': "true",
                                                  #'data-parsley-group': 'group0'
                                                  }))
    adverse_event_date = forms.DateField(widget=forms.TextInput(
        attrs={'placeholder': _('Date Of Adverse Event'),
               'class': 'form-control',
               'id': 'adverse_event_date'
               #'data-parsley-required': "true",
               #'data-parsley-group': 'group0'
               }))
    adverse_medical_events = forms.ChoiceField(choices=adverse_medical_list,
                                               initial='0',
                                               widget=forms.SelectMultiple(
                                                   attrs={'class': 'form-control',
                                                          'id': 'adverse_medical_events'
                                                          #'data-parsley-required': "true",
                                                          #'data-parsley-group': 'group0'
                                                          }))
    attendance_type = forms.ChoiceField(choices=attendance_type_list,
                                        initial='0',
                                        widget=forms.Select(
                                            attrs={'class': 'form-control',
                                                   'id': 'attendance_type'
                                                   #'data-parsley-required': "true",
                                                   #'data-parsley-group': 'group0'
                                                   }))
    hospital_referral_type = forms.ChoiceField(choices=hospital_referral_type_list,
                                               initial='0',
                                               widget=forms.Select(
                                                   attrs={'class': 'form-control',
                                                          'id': 'hospital_referral_type'
                                                          #'data-parsley-required': "true",
                                                          #'data-parsley-group': 'group0'
                                                          }))
    adverse_offences = forms.ChoiceField(choices=adverse_offence_list,
                                         initial='0',
                                         widget=forms.SelectMultiple(
                                             attrs={'class': 'form-control',
                                                    'id': 'adverse_offences'
                                                    #'data-parsley-required': "true",
                                                    #'data-parsley-group': 'group0'
                                                    }))
    discharge_date = forms.DateField(widget=forms.TextInput(
        attrs={'placeholder': _('Date Of Discharge'),
               'class': 'form-control',
               'id': 'discharge_date'
               #'data-parsley-required': "true",
               #'data-parsley-group': 'group0'
               }))
    expected_return_date = forms.DateField(widget=forms.TextInput(
        attrs={'placeholder': _('Expected Return Date'),
               'class': 'form-control',
               'id': 'expected_return_date'
               #'data-parsley-required': "true",
               #'data-parsley-group': 'group0'
               }))
    actual_return_date = forms.DateField(widget=forms.TextInput(
        attrs={'placeholder': _('Actual Return Date'),
               'class': 'form-control',
               'id': 'actual_return_date'
               #'data-parsley-required': "true",
               #'data-parsley-group': 'group0'
               }))
    discharge_type = forms.ChoiceField(choices=discharge_type_list,
                                       initial='0',
                                       widget=forms.Select(
                                           attrs={'class': 'form-control',
                                                  'id': 'discharge_type'
                                                  #'data-parsley-required': "true",
                                                  #'data-parsley-group': 'group0'
                                                  }))

    def __init__(self, *args, **kwargs):
        super(ResidentialFollowupForm, self).__init__(*args, **kwargs)
        # schools_list = [('', 'Please Select')] + list(SchoolList.objects
        # .filter().values_list('school_id', 'school_name'))
        org_unit_ids = ['TICC', 'TICA', 'TICH', 'TIRS', 'TIRC', 'TIBI',
                        'TNRC', 'TNSA', 'TNSI', 'TNCI', 'TNRH', 'TNRC',
                        'TNRR', 'TNAP', 'TNRS', 'TNRB']
        org_units_list = [('', 'Please Select')] + list(RegOrgUnit.objects.filter(
            org_unit_type_id__in=org_unit_ids).values_list('id', 'org_unit_name'))
        discharge_destination = forms.ChoiceField(choices=org_units_list,
                                                  initial='0',
                                                  widget=forms.Select(
                                                      attrs={'class': 'form-control',
                                                             'id': 'discharge_destination'}))
        self.fields['name_of_school'] = name_of_school

    discharge_reason = forms.CharField(widget=forms.Textarea(
        attrs={'placeholder': _('Discharge Reason'),
               'class': 'form-control',
               'id': 'discharge_reason',
               #'data-parsley-required': "true",
               #'data-parsley-group': 'group0',
               'rows': '2'}))
    discharge_comments = forms.CharField(widget=forms.Textarea(
        attrs={'placeholder': _('Discharge Comments'),
               'class': 'form-control',
               'id': 'discharge_comments',
               #'data-parsley-required': "true",
               #'data-parsley-group': 'group0',
               'rows': '2'}))
    admmitted_to_school = forms.ChoiceField(choices=yesno_list,
                                            initial='0',
                                            widget=forms.Select(
                                                attrs={'class': 'form-control',
                                                       'id': 'admmitted_to_school'
                                                       #'data-parsley-required': "true",
                                                       #'data-parsley-group': 'group0'
                                                       }))

    def __init__(self, *args, **kwargs):
        super(ResidentialFollowupForm, self).__init__(*args, **kwargs)
        # schools_list = [('', 'Please Select')] + list(SchoolList.objects.filter().values_list('school_id', 'school_name'))
        name_of_school = forms.ChoiceField(choices=(),
                                           initial='0',
                                           widget=forms.Select(
            attrs={'class': 'form-control',
                   'id': 'name_of_school'
                   # 'data-parsley-required': "true",
                   # 'data-parsley-group': 'group0'
                   }))
        self.fields['name_of_school'] = name_of_school

    school_name = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': _('Name of School'),
               'class': 'form-control',
               'id': 'school_name'
               }))

    type_of_school = forms.ChoiceField(choices=school_type_list,
                                       initial='0',
                                       widget=forms.Select(
                                           attrs={'class': 'form-control',
                                                  'id': 'type_of_school'
                                                  }))
    school_subcounty = forms.ChoiceField(
        choices=sub_county_list,
        initial='0',
        widget=forms.Select(
            attrs={'class': 'form-control',
                   'id': 'school_subcounty'}))
    school_ward = forms.ChoiceField(
        choices=ward_list, label=_('Select ward'),
        initial='',
        widget=forms.Select(
            attrs={'id': 'school_ward',
                   'class': 'form-control'}))

    not_in_school_reason = forms.ChoiceField(choices=schoolout_reason_list,
                                             initial='0',
                                             widget=forms.Select(
                                                 attrs={'class': 'form-control',
                                                        'id': 'not_in_school_reason'
                                                        # 'data-parsley-required': "true",
                                                        # 'data-parsley-group': 'group0'
                                                        }))
    admmission_type = forms.ChoiceField(choices=school_admission_type_list,
                                        initial='0',
                                        widget=forms.Select(
                                            attrs={'class': 'form-control',
                                                   'id': 'admmission_type'
                                                   # 'data-parsley-required': "true",
                                                   # 'data-parsley-group': 'group0'
                                                   }))

    admmission_class = forms.ChoiceField(choices=admission_class_list,
                                         initial='0',
                                         widget=forms.SelectMultiple(
                                             attrs={'class': 'form-control',
                                                    'id': 'admmission_class'
                                                    #'data-parsley-required': "true",
                                                    #'data-parsley-group': 'group0'
                                                    }))
    admmission_subclass = forms.ChoiceField(choices=vocational_training_list,
                                            initial='0',
                                            widget=forms.Select(
                                                attrs={'class': 'form-control',
                                                       'id': 'admmission_subclass'
                                                       #'data-parsley-required': "true",
                                                       #'data-parsley-group': 'group0'
                                                       }))
    admmission_subclass_other = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': _('Other Vocational'),
               'class': 'form-control',
               'id': 'admmission_subclass_other'}))
    admmission_to_school_date = forms.DateField(widget=forms.TextInput(
        attrs={'placeholder': _('Date Of Admission'),
               'class': 'form-control',
               'id': 'admmission_to_school_date'
               #'data-parsley-required': "true",
               #'data-parsley-group': 'group0'
               }))
    education_comments = forms.CharField(widget=forms.Textarea(
        attrs={'placeholder': _('Education Comments'),
               'class': 'form-control',
               'id': 'education_comments',
               #'data-parsley-required': "true",
               #'data-parsley-group': 'group0',
               'rows': '2'}))

    # Court Session
    case_event_id_court = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control',
               'id': 'case_event_id_court',
               'type': 'hidden'
               }))
    court_outcome = forms.ChoiceField(choices=court_outcome_list,
                                      initial='0',
                                      widget=forms.Select(
                                          attrs={'class': 'form-control',
                                                 'id': 'court_outcome'
                                                 }))
    application_outcome = forms.ChoiceField(choices=application_outcome_list,
                                            initial='0',
                                            widget=forms.Select(
                                                attrs={'class': 'form-control',
                                                       'id': 'application_outcome'
                                                       }))
    next_hearing_date = forms.DateField(widget=forms.TextInput(
        attrs={'placeholder': _('Next Hearing Date'),
               'class': 'form-control',
               'id': 'next_hearing_date'
               # type': 'hidden'
               }))
    next_mention_date = forms.DateField(widget=forms.TextInput(
        attrs={'placeholder': _('Next Mention Date'),
               'class': 'form-control',
               'id': 'next_mention_date'
               # type': 'hidden'
               }))
    court_session_case = forms.ChoiceField(initial='0',
                                           widget=forms.Select(
                                               attrs={'class': 'form-control',
                                                      'id': 'court_session_case'
                                                      }))
    court_session_type = forms.ChoiceField(initial='0',
                                           choices=courtsession_type_list,
                                           widget=forms.Select(
                                               attrs={'class': 'form-control',
                                                      'id': 'court_session_type'
                                                      }))
    plea_taken = forms.ChoiceField(initial='0',
                                   choices=plea_type_list,
                                   widget=forms.Select(
                                       attrs={'class': 'form-control',
                                              'id': 'plea_taken'
                                              }))
    date_of_court_event = forms.DateField(widget=forms.TextInput(
        attrs={'placeholder': _('Date Of Court Session'),
               'class': 'form-control',
               'id': 'date_of_court_event'
               }))
    court_order = forms.ChoiceField(choices=court_order_list,
                                    initial='0',
                                    widget=forms.SelectMultiple(
                                        attrs={'class': 'form-control',
                                               'id': 'court_order'
                                               }))
    court_notes = forms.CharField(widget=forms.Textarea(
        attrs={'placeholder': _('Notes'),
               'class': 'form-control',
               'rows': '2',
               'id': 'court_notes'}))
    workforce_member_court = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': _('Workforce Member/SCCO Name'),
               'class': 'form-control',
               'id': 'workforce_member_court'}))


class ResidentialForm(forms.Form):
    # OVCCaseEventPlacement
    def __init__(self, *args, **kwargs):
        super(ResidentialForm, self).__init__(*args, **kwargs)

        org_unit_ids = ['TICC', 'TICA', 'TICH', 'TIRS', 'TIRC', 'TIBI', 'TNRC']
        org_unit_ids0 = ['TNSA', 'TNSI', 'TNCI', 'TNRH', 'TNRC', 'TNRR']
        org_unit_ids.extend(org_unit_ids0)
        org_units_list = [('', 'Please Select')] + list(RegOrgUnit.objects.filter(
            org_unit_type_id__in=org_unit_ids).values_list('id', 'org_unit_name'))

        residential_institution_name = forms.ChoiceField(choices=org_units_list,
                                                         initial='0',
                                                         widget=forms.Select(
                                                             attrs={'class': 'form-control',
                                                                    'id': 'residential_institution_name',
                                                                    'data-parsley-required': "true",
                                                                    'data-parsley-group': 'group1'
                                                                    }))
        self.fields[
            'residential_institution_name'] = residential_institution_name

        transfer_from = forms.ChoiceField(choices=org_units_list,
                                          initial='0',
                                          widget=forms.Select(
                                              attrs={'class': 'form-control',
                                                     'id': 'transfer_from',
                                                     'data-parsley-required': "true",
                                                     'data-parsley-group': 'group1'
                                                     }))
        self.fields['transfer_from'] = transfer_from

    placement_type = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control',
               'id': 'placement_type',
               'type': 'hidden'
               }))
    person_id = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control',
               'id': 'person_id',
               'type': 'hidden'
               }))
    child_firstname = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': _('FirstName'),
               'class': 'form-control',
               'id': 'child_firstname',
               'data-parsley-required': "true",
               'data-parsley-group': 'group0'
               }))
    child_lastname = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': _('LastName'),
               'class': 'form-control',
               'id': 'child_lastname',
               # 'data-parsley-required': "true",
               'data-parsley-group': 'group0'
               }))
    child_surname = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': _('Surname'),
               'class': 'form-control',
               'id': 'child_surname',
               'data-parsley-required': "true",
               'data-parsley-group': 'group0'
               }))
    child_gender = forms.ChoiceField(choices=sex_id_list,
                                     initial='0',
                                     widget=forms.Select(
                                         attrs={'class': 'form-control',
                                                'id': 'child_gender',
                                                'data-parsley-required': "true",
                                                'data-parsley-group': 'group0'
                                                }))
    child_dob = forms.DateField(widget=forms.TextInput(
        attrs={'placeholder': _('Date Of Birth'),
               'class': 'form-control',
               'id': 'child_dob',
               'data-parsley-required': "true",
               'data-parsley-group': 'group0'
               }))

    case_category = forms.ChoiceField(initial='0',
                                      widget=forms.Select(
                                          attrs={'class': 'form-control',
                                                 'id': 'case_category',
                                                 # 'data-parsley-required': "true",
                                                 'data-parsley-group': 'group1'
                                                 }))

    residential_institution_type = forms.ChoiceField(choices=institution_type_list,
                                                     initial='0',
                                                     widget=forms.Select(
                                                         attrs={'class': 'form-control',
                                                                'id': 'residential_institution_type',
                                                                'data-parsley-required': "true",
                                                                'data-parsley-group': 'group1'
                                                                }))

    admission_date = forms.DateField(widget=forms.TextInput(
        attrs={'placeholder': _('Date Of Admission'),
               'class': 'form-control',
               'id': 'admission_date',
               'data-parsley-required': "true",
               'data-parsley-group': 'group1'
               # type': 'hidden'
               }))
    admission_type = forms.ChoiceField(choices=admission_type_list,
                                       initial='0',
                                       widget=forms.Select(
                                           attrs={'class': 'form-control',
                                                  'id': 'admission_type',
                                                  'data-parsley-required': "true",
                                                  'data-parsley-group': 'group1'
                                                  }))
    admission_reason = forms.ChoiceField(choices=admission_reason_list,
                                         initial='0',
                                         widget=forms.Select(
                                             attrs={'class': 'form-control',
                                                    'id': 'admission_reason',
                                                    'data-parsley-required': "true",
                                                    'data-parsley-group': 'group1'
                                                    }))
    holding_period = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': _('Holding Period(days)'),
               'class': 'form-control',
               'id': 'holding_period',
               'data-parsley-required': "true",
               'data-parsley-type': "digits",
               'data-parsley-group': 'group2'
               }))
    """
    current_residential_status = forms.ChoiceField(choices=residential_status_list,
                                                   initial='0',
                                                   widget=forms.Select(
                                                       attrs={'class': 'form-control',
                                                              'id': 'current_residential_status'
                                                              }))
    """
    has_court_committal_order = forms.ChoiceField(choices=yesno_list,
                                                  initial='0',
                                                  widget=forms.Select(
                                                      attrs={'class': 'form-control',
                                                             'id': 'has_court_committal_order',
                                                             'data-parsley-required': "true",
                                                             'data-parsley-group': 'group2'
                                                             }))
    court_order_number = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': _('Court Order Number'),
               'class': 'form-control',
               'id': 'court_order_number',
               'data-parsley-required': "true",
               'data-parsley-group': 'group2'
               }))
    court_order_issue_date = forms.DateField(widget=forms.TextInput(
        attrs={'placeholder': _('Date Of Court Order'),
               'class': 'form-control',
               'id': 'court_order_issue_date',
               'data-parsley-required': "true",
               'data-parsley-group': 'group2'
               # type': 'hidden'
               }))
    committing_court = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': _('Committing Court'),
               'class': 'form-control',
               'id': 'committing_court',
               'data-parsley-required': "true",
               'data-parsley-group': 'group2'
               }))
    committing_period_units = forms.ChoiceField(choices=period_list,
                                                initial='0',
                                                widget=forms.Select(
                                                    attrs={'class': 'form-control',
                                                           'id': 'committing_period_units',
                                                           'data-parsley-required': "true",
                                                           'data-parsley-group': 'group2'
                                                           }))
    committing_period = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': _('Committing Period(Days/Weeks/Months/Years'),
               'class': 'form-control',
               'id': 'committing_period',
               'data-parsley-required': "true",
               'data-parsley-type': "digits",
               'data-parsley-group': 'group2'
               }))
    ob_number = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': _('OB Number'),
               'class': 'form-control',
               'id': 'ob_number',
               'data-parsley-required': "true",
               'data-parsley-group': 'group2'
               }))
    free_for_adoption = forms.ChoiceField(choices=yesno_list,
                                          initial='0',
                                          widget=forms.Select(
                                              attrs={'class': 'form-control',
                                                     'id': 'free_for_adoption',
                                                     # 'data-parsley-required': "true",
                                                     'data-parsley-group': 'group2'
                                                     }))
    workforce_member_plcmnt = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': _('Workforce Member/SCCO Name'),
               'class': 'form-control',
               'id': 'workforce_member_plcmnt',
               'data-parsley-required': "true",
               'data-parsley-group': 'group2'}))
    placement_notes = forms.CharField(widget=forms.Textarea(
        attrs={'placeholder': _('Notes'),
               'class': 'form-control',
               'rows': '2',
               'id': 'placement_notes',
               #'data-parsley-required': "true",
               'data-parsley-group': 'group2'}))
    user_id = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control',
               'id': 'user_id',
               'type': 'hidden'
               }))


class ResidentialSearchForm(forms.Form):
    person_type = forms.ChoiceField(choices=person_type_list,
                                    initial='0',
                                    required=True,
                                    widget=forms.Select(
                                        attrs={'class': 'form-control',
                                               'id': 'person_type',
                                               'data-parsley-required': 'true'})
                                    )

    search_name = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': _('Enter Child Name(s)'),
               'class': 'form-control',
               'id': 'search_name',
               'data-parsley-group': 'primary_',
               'data-parsley-required': 'true'}))

    search_criteria = forms.ChoiceField(choices=psearch_criteria_list,
                                        initial='0',
                                        required=True,
                                        widget=forms.Select(
                                            attrs={'class': 'form-control',
                                                   'id': 'search_criteria',
                                                   # 'readonly':'true',
                                                   'data-parsley-required': 'true'})
                                        )

    form_type_search = forms.ChoiceField(choices=form_type_list,
                                         initial='0',
                                         required=True,
                                         widget=forms.Select(
                                             attrs={'class': 'form-control',
                                                    'id': 'form_type_search',
                                                    'data-parsley-required': 'true'})
                                         )


class OVC_FT3hForm(forms.Form):
    # Logged in User
    user_id = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control',
               'id': 'user_id',
               'type': 'hidden'
               }))

    # Reporter
    is_self_reporter = forms.CharField(
        widget=forms.CheckboxInput(
            attrs={'class': 'form-control', 'id': 'is_self_reporter'}))
    date_case_opened = forms.DateField(widget=forms.TextInput(
        attrs={'placeholder': _('Date Of Case Opening'),
               'class': 'form-control',
               'id': 'date_case_opened',
               'data-parsley-required': "true",
               'data-parsley-group': "group0"
               }))
    case_reporter = forms.ChoiceField(
        choices=case_reporter_list,
        initial='0',
        widget=forms.Select(
            attrs={'class': 'form-control',
                   'id': 'case_reporter',
                   'data-parsley-required': "true",
                   'data-parsley-group': "group0"
                   }))
    court_name = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': _('Court Name'),
               'class': 'form-control',
               'id': 'court_name',
               'data-parsley-required': "true",
               'data-parsley-group': "group0"}))
    court_number = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': _('Court/File Number'),
               'class': 'form-control',
               'id': 'court_number',
               'data-parsley-required': "true",
               'data-parsley-group': "group0"}))
    police_station = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': _('Police Station'),
               'class': 'form-control',
               'id': 'police_station',
               'data-parsley-required': "true",
               'data-parsley-group': "group0"}))
    ob_number = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': _('OB Number'),
               'class': 'form-control',
               'id': 'ob_number',
               'data-parsley-required': "true",
               'data-parsley-group': "group0"}))
    case_reporter_first_name = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': _('First Name'),
               'class': 'form-control',
               'id': 'case_reporter_first_name',
               'data-parsley-required': "true",
               'data-parsley-group': "group0"}))
    case_reporter_other_names = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': _('Middle Names'),
               'class': 'form-control',
               'id': 'case_reporter_other_names',
               'data-parsley-group': "group0"}))
    case_reporter_surname = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': _('Surname'),
               'class': 'form-control',
               'id': 'case_reporter_surname',
               'data-parsley-required': "true",
               'data-parsley-group': "group0"}))
    case_reporter_contacts = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': _('Reporter PhoneNumber'),
               'class': 'form-control',
               'id': 'case_reporter_contacts',
               'data-parsley-pattern': '/^[0-9\+]{1,}[0-9\-]{3,15}$/',
               #'data-parsley-required': "true",
               'data-parsley-group': "group0"}))
    case_reporter_relationship_to_child = forms.ChoiceField(
        choices=relationship_type_list,
        initial='0',
        widget=forms.Select(
            attrs={'class': 'form-control',
                   'id': 'case_reporter_relationship_to_child',
                   'data-parsley-required': "true",
                   'data-parsley-group': "group0"
                   }))
    report_subcounty = forms.ChoiceField(
        choices=sub_county_list,
        initial='0',
        widget=forms.Select(
            attrs={'class': 'form-control',
                   'id': 'report_subcounty',
                   'data-parsley-required': "true",
                   'data-parsley-group': "group0"}))
    report_ward = forms.ChoiceField(
        choices=ward_list, label=_('Select ward'),
        initial='',
        widget=forms.Select(
            attrs={'id': 'report_ward',
                   'class': 'form-control',
                   #'data-parsley-required': "true",
                   'data-parsley-group': "group0"}))
    report_village = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': _('Village/Estate'),
               'class': 'form-control',
               'id': 'report_village',
               'data-parsley-group': "group0"}))

    def __init__(self, *args, **kwargs):
        super(OVC_FT3hForm, self).__init__(*args, **kwargs)
        org_units_list___ = get_org_units_list('Please Select Unit')

        report_orgunit = forms.ChoiceField(
            choices=org_units_list___, label=_('Select orgunit'),
            initial='0',
            widget=forms.Select(
                attrs={'id': 'report_orgunit',
                       'class': 'form-control',
                       'data-parsley-required': "true",
                       'data-parsley-group': "group0"}))
        self.fields['report_orgunit'] = report_orgunit
    occurence_county = forms.ChoiceField(
        choices=county_list,
        initial='',
        widget=forms.Select(
            attrs={'class': 'form-control',
                   'id': 'occurence_county',
                   'data-parsley-required': "true",
                   'data-parsley-group': "group0"}))
    occurence_subcounty = forms.ChoiceField(
        choices=sub_county_list,
        initial='',
        widget=forms.Select(
            attrs={'class': 'form-control',
                   'id': 'occurence_subcounty',
                   'data-parsley-required': "true",
                   'data-parsley-group': "group0"}))
    occurence_ward = forms.ChoiceField(
        choices=ward_list, label=_('Select ward'),
        initial='',
        widget=forms.Select(
            attrs={'id': 'occurence_ward',
                   'class': 'form-control',
                   #'data-parsley-required': "true",
                   'data-parsley-group': "group0"}))
    occurence_village = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': _('Village/Estate'),
               'class': 'form-control',
               'id': 'occurence_village',
               'data-parsley-group': "group0"}))

    # About Child Info
    person = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control',
               'id': 'person',
               'type': 'hidden',
               'data-parsley-required': "true",
               'data-parsley-group': 'group0'
               }))
    case_id = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control',
               'id': 'uuid',
               'type': 'hidden',
               'data-parsley-required': "true",
               'data-parsley-group': 'group0'
               }))
    case_category_id = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control',
               'id': 'uuid',
               'type': 'hidden',
               'data-parsley-required': "true",
               'data-parsley-group': 'group0'
               }))

    friends = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': _('Enter Friends and press ENTER'),
               'class': 'form-control',
               'id': 'friends',
               'type': 'hidden',
               'data-parsley-group': 'group1'}))
    hobbies = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': _('Enter Hobbies and press ENTER'),
               'class': 'form-control',
               'id': 'hobbies',
               'type': 'hidden',
               'data-parsley-group': 'group1'}))
    case_grouping_id = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control',
               'id': 'person',
               'type': 'hidden',
               'data-parsley-group': 'group0'
               }))
    row_id = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control',
               'id': 'row_id',
               'type': 'hidden',
               'data-parsley-required': "true",
               'data-parsley-group': 'group0'
               }))

    # Household Info
    household_economics = forms.ChoiceField(choices=household_economics_list,
                                            initial='0',
                                            required=True,
                                            widget=forms.Select(
                                                attrs={'class': 'form-control',
                                                       'id': 'household_economics',
                                                       'data-parsley-required': "true",
                                                       'data-parsley-group': 'group1'})
                                            )
    family_status = forms.ChoiceField(choices=family_status_list,
                                      initial='0',
                                      required=True,
                                      widget=forms.SelectMultiple(
                                          attrs={'class': 'form-control',
                                                 'id': 'family_status',
                                                 'data-parsley-required': "true",
                                                 'data-parsley-group': 'group1'})
                                      )

    # Medical Info
    mental_condition = forms.ChoiceField(choices=mental_condition_list,
                                         initial='0',
                                         required=True,
                                         widget=forms.Select(
                                             attrs={'class': 'form-control',
                                                    'id': 'mental_condition',
                                                    'data-parsley-required': "true",
                                                    'data-parsley-group': 'group2'})
                                         )
    mental_subcondition = forms.ChoiceField(choices=mental_subcondition_list,
                                            initial='0',
                                            required=True,
                                            widget=forms.SelectMultiple(
                                                attrs={'class': 'form-control',
                                                       'id': 'mental_subcondition',
                                                       #'data-parsley-required': "true",
                                                       'data-parsley-group': 'group2'})
                                            )
    physical_condition = forms.ChoiceField(choices=physical_condition_list,
                                           initial='0',
                                           required=True,
                                           widget=forms.Select(
                                               attrs={'class': 'form-control',
                                                      'id': 'physical_condition',
                                                      'data-parsley-required': "true",
                                                      'data-parsley-group': 'group2'})
                                           )
    physical_subcondition = forms.ChoiceField(choices=physical_subcondition_list,
                                              initial='0',
                                              required=True,
                                              widget=forms.SelectMultiple(
                                                  attrs={'class': 'form-control',
                                                         'id': 'physical_subcondition',
                                                         #'data-parsley-required': "true",
                                                         'data-parsley-group': 'group2'})
                                              )
    other_condition = forms.ChoiceField(choices=other_condition_list,
                                        initial='0',
                                        required=True,
                                        widget=forms.Select(
                                            attrs={'class': 'form-control',
                                                   'id': 'other_condition',
                                                   'data-parsley-required': "true",
                                                   'data-parsley-group': 'group2'})
                                        )
    other_subcondition = forms.ChoiceField(choices=other_subcondition_list,
                                           initial='0',
                                           required=True,
                                           widget=forms.SelectMultiple(
                                               attrs={'class': 'form-control',
                                                      'id': 'other_subcondition',
                                                      #'data-parsley-required': "true",
                                                      'data-parsley-group': 'group2'})
                                           )

    # Case Data - OVCCaseRecord Model
    serial_number = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': _('Case Serial Number'),
               'class': 'form-control',
               'id': 'serial_number',
               'data-parsley-required': "true",
               'data-parsley-group': 'group3'}))
    perpetrator_status = forms.ChoiceField(choices=perpetrator_status_list,
                                           initial='0',
                                           required=True,
                                           widget=forms.Select(
                                               attrs={'class': 'form-control',
                                                      'id': 'perpetrator_status',
                                                      'data-parsley-required': "true",
                                                      'data-parsley-group': 'group3'})
                                           )
    perpetrator_first_name = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': _('First Name'),
               'class': 'form-control',
               'id': 'perpetrator_first_name',
               'data-parsley-required': "true",
               'data-parsley-group': "group3"}))
    perpetrator_other_names = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': _('Middle Name'),
               'class': 'form-control',
               'id': 'perpetrator_other_names',
               'data-parsley-group': "group3"}))
    perpetrator_surname = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': _('Surname'),
               'class': 'form-control',
               'id': 'perpetrator_surname',
               'data-parsley-required': "true",
               'data-parsley-group': "group3"}))

    perpetrator_relationship = forms.ChoiceField(choices=relationship_type_list,
                                                 initial='0',
                                                 widget=forms.Select(
                                                     attrs={'class': 'form-control',
                                                            'id': 'perpetrator_relationship',
                                                            'data-parsley-required': "true",
                                                            'data-parsley-group': "group3"
                                                            }))
    place_of_event = forms.ChoiceField(choices=event_place_list,
                                       initial='0',
                                       widget=forms.Select(
                                           attrs={'class': 'form-control',
                                                  'id': 'place_of_event'
                                                  #'data-parsley-required': "true",
                                                  #'data-parsley-group': "group3"
                                                  }))
    case_nature = forms.ChoiceField(choices=case_nature_list,
                                    initial='0',
                                    widget=forms.Select(
                                        attrs={'class': 'form-control',
                                               'id': 'case_nature'
                                               #'data-parsley-required': "true",
                                               #'data-parsley-group': "group3"
                                               }))
    risk_level = forms.ChoiceField(choices=risk_level_list,
                                   initial='0',
                                   widget=forms.Select(
                                       attrs={'class': 'form-control',
                                              'id': 'risk_level',
                                              'data-parsley-required': "true",
                                              'data-parsley-group': "group3"
                                              }))
    immediate_needs = forms.ChoiceField(choices=shortterm_needs_list,
                                        initial='0',
                                        required=True,
                                        widget=forms.SelectMultiple(
                                            attrs={  # 'class': 'form-control',
                                                'id': 'immediate_needs',
                                                #'data-parsley-required': "true",
                                                'data-parsley-group': 'group3'})
                                        )
    future_needs = forms.ChoiceField(choices=longterm_needs_list,
                                     initial='0',
                                     required=True,
                                     widget=forms.SelectMultiple(
                                         attrs={'class': 'form-control',
                                                'id': 'future_needs',
                                                #'data-parsley-required': "true",
                                                'data-parsley-group': 'group3'})
                                     )
    case_remarks = forms.CharField(widget=forms.Textarea(
        attrs={'placeholder': _('Case Remarks'),
               'class': 'form-control',
               'id': 'case_remarks',
               'rows': '3',
               'data-parsley-group': "group3"}))

    # Refferals
    refferal_present = forms.ChoiceField(choices=yesno_list,
                                         widget=forms.Select(
                                             attrs={'class': 'form-control',
                                                    'id': 'refferal_present',
                                                    'data-parsley-required': "true",
                                                    'data-parsley-group': "group3"}))
    refferal_destination_type = forms.ChoiceField(choices=referral_destination_list,
                                                  initial='0',
                                                  widget=forms.Select(
                                                      attrs={'class': 'form-control',
                                                             'id': 'refferal_destination_type'
                                                             }))
    # refferal_destination_description = forms.CharField(widget=forms.TextInput(
    #    attrs={'placeholder': _('Specify'),
    #           'class': 'form-control',
    #           'id': 'refferal_destination_description'}))
    refferal_destination_description = forms.ChoiceField(choices=referral_destination_classification_list,
                                                         initial='0',
                                                         widget=forms.Select(
                                                             attrs={'class': 'form-control',
                                                                    'id': 'refferal_destination_description'
                                                                    }))
    refferal_reason = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': _('Referral Reason'),
               'class': 'form-control',
               'id': 'refferal_reason'}))
    refferal_to = forms.ChoiceField(choices=referral_to_list,
                                    initial='0',
                                    widget=forms.Select(
                                        attrs={'class': 'form-control',
                                               'id': 'refferal_to'
                                               }))
    summon_issued = forms.ChoiceField(choices=yesno_list,
                                      initial='0',
                                      widget=forms.Select(
                                          attrs={'class': 'form-control',
                                                 'id': 'summon_issued',
                                                 'data-parsley-required': "true",
                                                 'data-parsley-group': "group3"
                                                 }))
    date_of_summon = forms.DateField(widget=forms.TextInput(
        attrs={'placeholder': _('Date Of Summon'),
               'class': 'form-control',
               'id': 'date_of_summon',
               'data-parsley-required': "true",
               'data-parsley-group': "group3"
               }))

    date_of_event = forms.DateField(widget=forms.TextInput(
        attrs={'placeholder': _('Date'),
               'class': 'form-control',
               'id': 'date_of_event',
               #'data-parsley-required': "true",
               'data-parsley-group': "group3"
               }))
    case_category = forms.ChoiceField(choices=case_category_list,
                                      initial='0',
                                      widget=forms.Select(
                                          attrs={'class': 'form-control',
                                                 'id': 'case_category',
                                                 #'multiple': 'multiple',
                                                 #'data-parsley-required': "true",
                                                 'data-parsley-group': "group3"
                                                 }))
    case_subcategory = forms.MultipleChoiceField(choices=(),
                                                 initial='',
                                                 widget=forms.SelectMultiple(
        attrs={'class': 'form-control',
               'id': 'case_subcategory',
               #'multiple': 'multiple',
               #'data-parsley-required': "true",
               'data-parsley-group': "group3"
               }))
    case_category_list = forms.CharField(widget=forms.TextInput(
        attrs={'id': 'case_category_list',
               'type': 'hidden'
               }))
    referralactors_list = forms.CharField(widget=forms.TextInput(
        attrs={'id': 'referralactors_list',
               'type': 'hidden'
               }))
    clone_ids_list = forms.CharField(widget=forms.TextInput(
        attrs={'id': 'clone_ids_list',
               'type': 'hidden'
               }))
    intervention = forms.ChoiceField(choices=intervention_list,
                                     initial='0',
                                     widget=forms.SelectMultiple(
                                         attrs={'class': 'form-control',
                                                'id': 'intervention',
                                                'multiple': 'multiple',
                                                #'data-parsley-required': "true",
                                                'data-parsley-group': "group3"
                                                }))


class OVC_CaseEventForm(forms.Form):
    service_provided_case = forms.ChoiceField(choices=case_category_list,
                                              initial='0',
                                              widget=forms.Select(
                                                  attrs={'class': 'form-control',
                                                         'id': 'service_provided_case'
                                                         }))
    place_of_service = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': _('Place of Service'),
               'class': 'form-control',
               'id': 'place_of_service'}))
    court_session_case = forms.ChoiceField(initial='0',
                                           widget=forms.Select(
                                               attrs={'class': 'form-control',
                                                      'id': 'court_session_case'
                                                      }))
    placement_case = forms.ChoiceField(initial='0',
                                       widget=forms.Select(
                                           attrs={'class': 'form-control',
                                                  'id': 'placement_case'
                                                  }))
    refferal_case = forms.ChoiceField(initial='0',
                                      widget=forms.Select(
                                          attrs={'class': 'form-control',
                                                 'id': 'refferal_case'
                                                 }))
    # Case ID
    case_id = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control',
               'id': 'case_id',
               'type': 'hidden'
               }))
    # Case Event ID
    case_event_id = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control',
               'id': 'case_event_id',
               'type': 'hidden'}))

    case_event_id_svc = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control',
               'id': 'case_event_id_svc',
               'type': 'hidden'
               }))
    case_event_id_court = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control',
               'id': 'case_event_id_court',
               'type': 'hidden'
               }))
    case_event_id_plcmt = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control',
               'id': 'case_event_id_plcmt',
               'type': 'hidden'
               }))
    case_event_id_summon = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control',
               'id': 'case_event_id_summon',
               'type': 'hidden'
               }))
    case_event_id_closure = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control',
               'id': 'case_event_id_closure',
               'type': 'hidden'
               }))
    case_event_type = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control',
               'id': 'case_event_type',
               'type': 'hidden'
               }))
    operation_mode = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control',
               'id': 'operation_mode',
               'type': 'hidden'
               }))

    # OVCCaseEventServices
    workforce_member_svc = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': _('Workforce Member/SCCO Name'),
               'class': 'form-control',
               'id': 'workforce_member_svc', }))
    workforce_member_court = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': _('Workforce Member/SCCO Name'),
               'class': 'form-control',
               'id': 'workforce_member_court'}))
    workforce_member_plcmnt = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': _('Workforce Member/SCCO Name'),
               'class': 'form-control',
               'id': 'workforce_member_plcmnt'}))
    date_of_referral_event = forms.DateField(widget=forms.TextInput(
        attrs={'placeholder': _('Date Completed'),
               'class': 'form-control',
               'name': 'date_of_referral_event',
               'id': 'date_of_referral_event'
               }))
    date_of_court_event = forms.DateField(widget=forms.TextInput(
        attrs={'placeholder': _('Date Of Court Session'),
               'class': 'form-control',
               'id': 'date_of_court_event'
               }))
    date_of_encounter_event = forms.DateField(widget=forms.TextInput(
        attrs={'placeholder': _('Date of Service'),
               'class': 'form-control',
               'id': 'date_of_encounter_event'
               }))
    date_of_placement_event = forms.DateField(widget=forms.TextInput(
        attrs={'placeholder': _('Date Of Placement'),
               'class': 'form-control',
               'id': 'date_of_placement_event'
               }))

    court_notes = forms.CharField(widget=forms.Textarea(
        attrs={'placeholder': _('Notes'),
               'class': 'form-control',
               'rows': '2',
               'id': 'court_notes'}))
    encounter_notes = forms.CharField(widget=forms.Textarea(
        attrs={'placeholder': _('Notes'),
               'class': 'form-control',
               'rows': '2',
               'id': 'encounter_notes'}))
    placement_notes = forms.CharField(widget=forms.Textarea(
        attrs={'placeholder': _('Notes'),
               'class': 'form-control',
               'rows': '2',
               'id': 'placement_notes'}))
    service_provided = forms.ChoiceField(choices=services_list,
                                         initial='0',
                                         widget=forms.Select(
                                             attrs={'class': 'form-control',
                                                    'id': 'service_provided'
                                                    }))
    service_provider = forms.ChoiceField(choices=service_provider_list,
                                         initial='0',
                                         widget=forms.Select(
                                             attrs={'class': 'form-control',
                                                    'id': 'service_provider'
                                                    }))
    service_provided_list = forms.CharField(widget=forms.TextInput(
        attrs={'type': 'hidden',
               'id': 'service_provided_list'}))
    refferals_made = forms.ChoiceField(choices=referral_to_list,
                                       initial='0',
                                       widget=forms.Select(
                                           attrs={'class': 'form-control',
                                                  'id': 'refferals_made'
                                                  }))
    refferals_actor = forms.ChoiceField(choices=referral_destination_list,
                                        initial='0',
                                        widget=forms.Select(
                                            attrs={'class': 'form-control',
                                                   'id': 'refferals_actor'
                                                   }))
    """
    refferals_actor_specify = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': _('Specify'),
               'class': 'form-control',
               'id': 'refferals_actor_specify'}))
    """
    refferals_actor_specify = forms.ChoiceField(choices=referral_destination_classification_list,
                                                initial='0',
                                                widget=forms.Select(
                                                    attrs={'class': 'form-control',
                                                           'id': 'refferals_actor_specify'
                                                           }))
    refferals_completed = forms.ChoiceField(choices=referral_to_list,
                                            initial='0',
                                            widget=forms.Select(
                                                attrs={'class': 'form-control',
                                                       'id': 'refferals_completed'
                                                       }))

    # OVCCaseEventCourt
    court_file_number = forms.CharField(widget=forms.Textarea(
        attrs={'placeholder': _('Notes'),
               'class': 'form-control',
               'id': 'court_file_number'}))
    court_outcome = forms.ChoiceField(choices=court_outcome_list,
                                      initial='0',
                                      widget=forms.Select(
                                          attrs={'class': 'form-control',
                                                 'id': 'court_outcome'
                                                 }))
    application_outcome = forms.ChoiceField(choices=application_outcome_list,
                                            initial='0',
                                            widget=forms.Select(
                                                attrs={'class': 'form-control',
                                                       'id': 'application_outcome'
                                                       }))
    court_session_type = forms.ChoiceField(initial='0',
                                           choices=courtsession_type_list,
                                           widget=forms.Select(
                                               attrs={'class': 'form-control',
                                                      'id': 'court_session_type'
                                                      }))
    plea_taken = forms.ChoiceField(initial='0',
                                   choices=plea_type_list,
                                   widget=forms.Select(
                                       attrs={'class': 'form-control',
                                              'id': 'plea_taken'
                                              }))
    next_hearing_date = forms.DateField(widget=forms.TextInput(
        attrs={'placeholder': _('Next Hearing Date'),
               'class': 'form-control',
               'id': 'next_hearing_date'
               # type': 'hidden'
               }))
    next_mention_date = forms.DateField(widget=forms.TextInput(
        attrs={'placeholder': _('Next Mention Date'),
               'class': 'form-control',
               'id': 'next_mention_date'
               # type': 'hidden'
               }))
    court_order = forms.ChoiceField(choices=court_order_list,
                                    initial='0',
                                    widget=forms.SelectMultiple(
                                        attrs={'class': 'form-control',
                                               'id': 'court_order'
                                               }))
    case_event_id_summon = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control',
               'id': 'case_event_id_summon',
               'type': 'hidden'
               }))
    honoured = forms.ChoiceField(choices=yesno_list,
                                 initial='0',
                                 widget=forms.Select(
                                     attrs={'class': 'form-control',
                                            'id': 'honoured'
                                            }))
    visit_date = forms.DateField(widget=forms.TextInput(
        attrs={'placeholder': _('Visit Date'),
               'class': 'form-control',
               'id': 'visit_date'
               }))
    honoured_date = forms.DateField(widget=forms.TextInput(
        attrs={'placeholder': _('Date Of Visit'),
               'class': 'form-control',
               'id': 'honoured_date'
               }))
    summon_date = forms.DateField(widget=forms.TextInput(
        attrs={'placeholder': _('Date Of Next Summon'),
               'class': 'form-control',
               'id': 'summon_date'
               }))
    summon_note = forms.CharField(widget=forms.Textarea(
        attrs={'placeholder': _('Summon Notes'),
               'class': 'form-control',
               'rows': '2',
               'id': 'summon_note'}))
    reported_date = forms.DateField(widget=forms.TextInput(
        attrs={'class': 'form-control',
               'id': 'reported_date',
               'type': 'hidden'
               }))

    # OVCCaseEventPlacement
    def __init__(self, *args, **kwargs):
        super(OVC_CaseEventForm, self).__init__(*args, **kwargs)
        org_unit_ids = ['TICC', 'TICA', 'TICH', 'TIRS', 'TIRC', 'TIBI']
        org_units_list = [('', 'Please Select')] + list(RegOrgUnit.objects.filter(
            org_unit_type_id__in=org_unit_ids).values_list('id', 'org_unit_name'))
        residential_institution = forms.ChoiceField(choices=org_units_list,
                                                    initial='0',
                                                    widget=forms.Select(
                                                        attrs={'class': 'form-control',
                                                               'id': 'residential_institution'}))
        self.fields['residential_institution'] = residential_institution

    current_residential_status = forms.ChoiceField(choices=residential_status_list,
                                                   initial='0',
                                                   widget=forms.Select(
                                                       attrs={'class': 'form-control',
                                                              'id': 'current_residential_status'
                                                              }))
    has_court_committal_order = forms.ChoiceField(choices=yesno_list,
                                                  initial='0',
                                                  widget=forms.Select(
                                                      attrs={'class': 'form-control',
                                                             'id': 'has_court_committal_order'
                                                             }))
    free_for_adoption = forms.ChoiceField(choices=yesno_list,
                                          initial='0',
                                          widget=forms.Select(
                                              attrs={'class': 'form-control',
                                                     'id': 'free_for_adoption'
                                                     }))
    admission_date = forms.DateField(widget=forms.TextInput(
        attrs={'placeholder': _('Date Of Admission'),
               'class': 'form-control',
               'id': 'admission_date'
               }))
    departure_date = forms.DateField(widget=forms.TextInput(
        attrs={'placeholder': _('Date Of Departure'),
               'class': 'form-control',
               'id': 'departure_date'
               # type': 'hidden'
               }))

    # OVCCaseEventClosure
    case_status = forms.ChoiceField(choices=yesno_list,
                                    initial='0',
                                    widget=forms.Select(
                                        attrs={'class': 'form-control',
                                               'id': 'case_status'
                                               }))
    case_outcome = forms.ChoiceField(choices=caseoutcome_list,
                                     initial='0',
                                     widget=forms.Select(
                                         attrs={'class': 'form-control',
                                                'id': 'case_outcome'
                                                }))

    def __init__(self, *args, **kwargs):
        super(OVC_CaseEventForm, self).__init__(*args, **kwargs)
        # org_unit_ids = ['TNSA', 'TNSI', 'TNCI', 'TNRH', 'TNRC', 'TNRR']
        # org_units_list = [('', 'Please Select')] + list(RegOrgUnit.objects.filter(org_unit_type_id__in=org_unit_ids).values_list('id', 'org_unit_name'))
        org_units_list = [('', 'Please Select')] + \
            list(RegOrgUnit.objects.all().values_list('id', 'org_unit_name'))
        transfered_to = forms.ChoiceField(choices=org_units_list,
                                          initial='0',
                                          widget=forms.Select(
                                              attrs={'class': 'form-control',
                                                     'id': 'transfered_to'}))
        self.fields['transfered_to'] = transfered_to

    date_of_case_closure = forms.DateField(widget=forms.TextInput(
        attrs={'placeholder': _('Date Of Outcome'),
               'class': 'form-control',
               'id': 'date_of_case_closure'
               }))
    case_closure_notes = forms.CharField(widget=forms.Textarea(
        attrs={'placeholder': _('Case Closure Notes'),
               'class': 'form-control',
               'id': 'case_closure_notes',
               'rows': '2'
               }))
    intervention = forms.ChoiceField(choices=intervention_list,
                                     initial='0',
                                     widget=forms.Select(
                                         attrs={'class': 'form-control',
                                                'id': 'intervention'
                                                }))
    intervention_list = forms.CharField(widget=forms.TextInput(
        attrs={'type': 'hidden',
               'id': 'intervention_list'}))
    case_closure_case = forms.ChoiceField(initial='0',
                                          widget=forms.Select(
                                              attrs={'class': 'form-control',
                                                     'id': 'case_closure_case'
                                                     }))


class OVC_FTFCForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(OVC_FTFCForm, self).__init__(*args, **kwargs)
        adopting_agency_list = [('', 'Please Select')] + list(RegOrgUnit.objects.filter(
            org_unit_type_id='TNSA').values_list('id', 'org_unit_name'))
        adopting_agency = forms.ChoiceField(choices=adopting_agency_list,
                                            initial='0',
                                            widget=forms.Select(
                                                attrs={'class': 'form-control',
                                                       'id': 'adopting_agency',
                                                       'data-parsley-required': "true",
                                                       'data-parsley-group': "group0"}))
        self.fields['adopting_agency'] = adopting_agency

        org_unit_ids__ = ['TNGP', 'TNGD']
        children_office_list = [('', 'Please Select')] + list(RegOrgUnit.objects.filter(
            org_unit_type_id__in=org_unit_ids__).values_list('id', 'org_unit_name'))
        children_office = forms.ChoiceField(choices=children_office_list,
                                            initial='0',
                                            widget=forms.Select(
                                                attrs={'class': 'form-control',
                                                       'id': 'children_office',
                                                       'data-parsley-required': "true",
                                                       'data-parsley-group': "group0"}))
        self.fields['children_office'] = children_office

        # org_unit_ids___ = ['TICC']
        org_unit_ids___ = ['TNSA', 'TNSI', 'TNCI', 'TNRH', 'TNRC', 'TNRR']
        familycare_institutions_list = [('', 'Please Select')] + list(RegOrgUnit.objects.filter(
            org_unit_type_id__in=org_unit_ids___).values_list('id', 'org_unit_name'))

        residential_institution_name = forms.ChoiceField(choices=familycare_institutions_list,
                                                         initial='0',
                                                         widget=forms.Select(
                                                             attrs={'class': 'form-control',
                                                                    'id': 'residential_institution_name',
                                                                    'data-parsley-required': "true",
                                                                    'data-parsley-group': 'group0'
                                                                    }))
        self.fields[
            'residential_institution_name'] = residential_institution_name

        # org_unit_ids____ = ['TNSA', 'TNSI', 'TNCI', 'TNRH', 'TNRC', 'TNRR']
        fostered_from_list = [('', 'Please Select')] + list(RegOrgUnit.objects.filter(
            org_unit_type_id__in=org_unit_ids___).values_list('id', 'org_unit_name'))

        fostered_from = forms.ChoiceField(choices=fostered_from_list,
                                          initial='0',
                                          widget=forms.Select(
                                              attrs={'class': 'form-control',
                                                     'id': 'fostered_from',
                                                     'data-parsley-required': "true",
                                                     'data-parsley-group': 'group0'
                                                     }))
        self.fields['fostered_from'] = fostered_from

    contact_person = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': _('Contact Person (Phone)'),
               'class': 'form-control',
               'id': 'contact_person',
               'data-parsley-required': "true",
               'data-parsley-group': "group0"}))

    type_of_care = forms.ChoiceField(choices=alternative_family_care_type_list,
                                     initial='0',
                                     widget=forms.Select(
                                         attrs={'class': 'form-control',
                                                'id': 'type_of_care',
                                                'data-parsley-required': "true",
                                                'data-parsley-group': "group0"
                                                }))

    adoption_subcounty = forms.ChoiceField(choices=sub_county_list,
                                           initial='0',
                                           widget=forms.Select(
                                               attrs={'class': 'form-control',
                                                      'id': 'adoption_subcounty',
                                                      'data-parsley-required': "true",
                                                      'data-parsley-group': "group0"
                                                      }))
    adoption_country = forms.ChoiceField(choices=(),
                                         initial='0',
                                         widget=forms.Select(
        attrs={'class': 'form-control',
               'id': 'adoption_country',
               'data-parsley-required': "true",
               'data-parsley-group': "group0"
               }))
    court_name = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': _('Court Name'),
               'class': 'form-control',
               'id': 'court_name',
               'data-parsley-required': "true",
               'data-parsley-group': "group0"}))
    court_file_number = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': _('Court File Number'),
               'class': 'form-control',
               'id': 'court_file_number',
               'data-parsley-required': "true",
               'data-parsley-group': "group0"}))
    certificate_number = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': _('P&C/Certificate Number'),
               'class': 'form-control',
               'id': 'certificate_number',
               'data-parsley-required': "true",
               'data-parsley-group': "group0"
               }))
    date_of_certificate_expiry = forms.DateField(widget=forms.TextInput(
        attrs={'placeholder': _('Date of Certificate Expiry'),
               'class': 'form-control',
               'id': 'date_of_certificate_expiry',
               'data-parsley-required': "true",
               'data-parsley-group': "group0"
               }))
    type_of_adoption = forms.ChoiceField(choices=type_of_adoption_list,
                                         initial='0',
                                         widget=forms.Select(
                                             attrs={'class': 'form-control',
                                                    'id': 'type_of_adoption',
                                                    'data-parsley-required': "true",
                                                    'data-parsley-group': "group0"
                                                    }))
    date_of_adoption = forms.DateField(widget=forms.TextInput(
        attrs={'placeholder': _('Date'),
               'class': 'form-control',
               'id': 'date_of_adoption',
               'data-parsley-required': "true",
               'data-parsley-group': "group0"
               }))
    parental_status = forms.ChoiceField(choices=parental_status_list,
                                        initial='0',
                                        widget=forms.Select(
                                            attrs={'class': 'form-control',
                                                   'id': 'parental_status',
                                                   'data-parsley-required': "true",
                                                   'data-parsley-group': "group0"
                                                   }))
    adopting_mother_firstname = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': _('FirstName'),
               'class': 'form-control',
               'id': 'adopting_mother_firstname',
               'data-parsley-required': "true",
               'data-parsley-group': "group0"
               }))
    adopting_mother_othernames = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': _('Other Names'),
               'class': 'form-control',
               'id': 'adopting_mother_othernames',
               'data-parsley-group': "group0"
               }))
    adopting_mother_surname = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': _('Surname'),
               'class': 'form-control',
               'id': 'adopting_mother_surname',
               'data-parsley-required': "true",
               'data-parsley-group': "group0"
               }))
    adopting_mother_idnumber = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': _('ID/Passport Number'),
               'class': 'form-control',
               'id': 'adopting_mother_idnumber',
               'data-parsley-group': "group0"
               }))
    adopting_mother_contacts = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': _('Contacts'),
               'class': 'form-control',
               'id': 'adopting_mother_contacts',
               'data-parsley-group': "group0"
               }))
    adopting_father_firstname = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': _('FirstName'),
               'class': 'form-control',
               'id': 'adopting_father_firstname',
               'data-parsley-required': "true",
               'data-parsley-group': "group0"
               }))
    adopting_father_othernames = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': _('Other Names'),
               'class': 'form-control',
               'id': 'adopting_father_othernames',
               'data-parsley-group': "group0"
               }))
    adopting_father_surname = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': _('Surname'),
               'class': 'form-control',
               'id': 'adopting_father_surname',
               'data-parsley-required': "true",
               'data-parsley-group': "group0"
               }))
    adopting_father_idnumber = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': _('ID/Passport Number'),
               'class': 'form-control',
               'id': 'adopting_father_idnumber',
               'data-parsley-group': "group0"
               }))
    adopting_father_contacts = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': _('Contacts'),
               'class': 'form-control',
               'id': 'adopting_father_contacts',
               'data-parsley-group': "group0"
               }))
    adoption_remarks = forms.CharField(widget=forms.Textarea(
        attrs={'placeholder': _('Remarks'),
               'class': 'form-control',
               'id': 'adoption_remarks',
               'rows': 3,
               'data-parsley-group': "group0"
               }))


# Demo API
class OVCSchoolForm(forms.Form):
    school_name = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': _('Name of School'),
               'class': 'form-control',
               'id': 'school_name',
               'data-parsley-required': "true",
               'data-parsley-group': 'group0'
               }))

    type_of_school = forms.ChoiceField(choices=school_type_list,
                                       initial='0',
                                       widget=forms.Select(
                                           attrs={'class': 'form-control',
                                                  'id': 'type_of_school',
                                                  'data-parsley-required': "true",
                                                  'data-parsley-group': 'group0'
                                                  }))
    school_subcounty = forms.ChoiceField(
        choices=sub_county_list,
        initial='0',
        widget=forms.Select(
            attrs={'class': 'form-control',
                   'id': 'school_subcounty',
                   'data-parsley-required': "true",
                   'data-parsley-group': "group0"}))
    school_ward = forms.ChoiceField(
        choices=ward_list, label=_('Select ward'),
        initial='',
        widget=forms.Select(
            attrs={'id': 'school_ward',
                   'class': 'form-control',
                   'data-parsley-required': "true",
                   'data-parsley-group': "group0"}))


#------------------------------------------- OVCCare -----------------------------------------------#
class OVCCareSearchForm(forms.Form):
    search_name = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': _('Enter Child / Household'),
               'class': 'form-control',
               'id': 'search_name',
               'data-parsley-group': 'primary_',
               'data-parsley-required': 'true'}))

    search_criteria = forms.ChoiceField(choices=povcsearch_criteria_list,
                                        initial='0',
                                        required=True,
                                        widget=forms.Select(
                                            attrs={'class': 'form-control',
                                                   'id': 'search_criteria',
                                                   # 'readonly':'true',
                                                   'data-parsley-required': 'true'})
                                        )
    """
    ovc_form_type = forms.ChoiceField(choices=ovc_form_type_list,
                                      initial='0',
                                      required=True,
                                      widget=forms.Select(
                                          attrs={'class': 'form-control input-sm',
                                                 'id': 'ovc_form_type',
                                                 'data-parsley-required': 'true'})
                                      )
    """


class OVCCsiForm(forms.Form):
    ## CSI FORM ##
    food_security = forms.ChoiceField(choices=csi_grade_list,
                                      initial='0',
                                      required=True,
                                      widget=forms.Select(
                                          attrs={'class': 'form-control',
                                                 'id': 'food_security',
                                                 'data-parsley-required': 'true',
                                                 'data-parsley-group': 'group0'})
                                      )
    nutrition_growth = forms.ChoiceField(choices=csi_grade_list,
                                         initial='0',
                                         required=True,
                                         widget=forms.Select(
                                             attrs={'class': 'form-control',
                                                    'id': 'nutrition_growth',
                                                    'data-parsley-required': 'true',
                                                    'data-parsley-group': 'group0'})
                                         )
    wellness = forms.ChoiceField(choices=csi_grade_list,
                                 initial='0',
                                 required=True,
                                 widget=forms.Select(
                                     attrs={'class': 'form-control',
                                            'id': 'wellness',
                                            'data-parsley-required': 'true',
                                            'data-parsley-group': 'group0'})
                                 )
    healthcare_services = forms.ChoiceField(choices=csi_grade_list,
                                            initial='0',
                                            required=True,
                                            widget=forms.Select(
                                                attrs={'class': 'form-control',
                                                       'id': 'healthcare_services',
                                                       'data-parsley-required': 'true',
                                                       'data-parsley-group': 'group0'})
                                            )
    shelter = forms.ChoiceField(choices=csi_grade_list,
                                initial='0',
                                required=True,
                                widget=forms.Select(
                                    attrs={'class': 'form-control',
                                                    'id': 'shelter',
                                                    'data-parsley-required': 'true',
                                                    'data-parsley-group': 'group0'})
                                )
    care = forms.ChoiceField(choices=csi_grade_list,
                             initial='0',
                             required=True,
                             widget=forms.Select(
                                 attrs={'class': 'form-control',
                                        'id': 'care',
                                        'data-parsley-required': 'true',
                                        'data-parsley-group': 'group0'})
                             )
    abuse_exploitation = forms.ChoiceField(choices=csi_grade_list,
                                           initial='0',
                                           required=True,
                                           widget=forms.Select(
                                               attrs={'class': 'form-control',
                                                      'id': 'abuse_exploitation',
                                                      'data-parsley-required': 'true',
                                                      'data-parsley-group': 'group0'})
                                           )
    legal_protection = forms.ChoiceField(choices=csi_grade_list,
                                         initial='0',
                                         required=True,
                                         widget=forms.Select(
                                             attrs={'class': 'form-control',
                                                    'id': 'legal_protection',
                                                    'data-parsley-required': 'true',
                                                    'data-parsley-group': 'group0'})
                                         )
    emotional_health = forms.ChoiceField(choices=csi_grade_list,
                                         initial='0',
                                         required=True,
                                         widget=forms.Select(
                                             attrs={'class': 'form-control',
                                                    'id': 'emotional_health',
                                                    'data-parsley-required': 'true',
                                                    'data-parsley-group': 'group0'})
                                         )
    social_behaviour = forms.ChoiceField(choices=csi_grade_list,
                                         initial='0',
                                         required=True,
                                         widget=forms.Select(
                                             attrs={'class': 'form-control',
                                                    'id': 'social_behaviour',
                                                    'data-parsley-required': 'true',
                                                    'data-parsley-group': 'group0'})
                                         )
    perfomance = forms.ChoiceField(choices=csi_grade_list,
                                   initial='0',
                                   required=True,
                                   widget=forms.Select(
                                       attrs={'class': 'form-control',
                                              'id': 'perfomance',
                                                    'data-parsley-required': 'true',
                                                    'data-parsley-group': 'group0'})
                                   )
    education_work = forms.ChoiceField(choices=csi_grade_list,
                                       initial='0',
                                       required=True,
                                       widget=forms.Select(
                                           attrs={'class': 'form-control',
                                                  'id': 'education_work',
                                                  'data-parsley-required': 'true',
                                                  'data-parsley-group': 'group0'})
                                       )
    household_strengthening = forms.ChoiceField(choices=csi_grade_list,
                                                initial='0',
                                                required=True,
                                                widget=forms.Select(
                                                    attrs={'class': 'form-control',
                                                           'id': 'household_strengthening',
                                                           'data-parsley-required': 'true',
                                                           'data-parsley-group': 'group0'})
                                                )
    ## OLMIS SERVICES ##
    olmis_domain = forms.ChoiceField(choices=olmis_domain_list,
                                     initial='0',
                                     required=True,
                                     widget=forms.Select(
                                             attrs={'class': 'form-control',
                                                    'id': 'olmis_domain'})
                                     )
    olmis_subdomain = forms.ChoiceField(choices=olmis_domain_list,
                                        initial='0',
                                        required=True,
                                        widget=forms.Select(
                                            attrs={'class': 'form-control',
                                                   'id': 'olmis_subdomain'})
                                        )
    olmis_service = forms.MultipleChoiceField(choices=(),
                                              initial='',
                                              widget=forms.Select(
        attrs={'class': 'form-control',
               'id': 'olmis_service'
               }))
    olmis_service_provider = forms.ChoiceField(choices=olmis_service_provider_list,
                                               initial='0',
                                               required=True,
                                               widget=forms.Select(
                                                   attrs={'class': 'form-control',
                                                          'id': 'olmis_service_provider'})
                                               )
    olmis_service_date = forms.DateField(widget=forms.TextInput(
        attrs={'placeholder': _('Date Of Service'),
               'class': 'form-control',
               'id': 'olmis_service_date'
               }))
    olmis_place_of_service = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': _('Place of Service'),
               'class': 'form-control',
               'id': 'olmis_place_of_service'}))
    olmis_service_provided_list = forms.CharField(widget=forms.TextInput(
        attrs={'type': 'hidden',
               'id': 'olmis_service_provided_list'}))

    ## OLMIS PRIORITIES ##
    olmis_priority_domain = forms.ChoiceField(choices=olmis_domain_list,
                                              initial='0',
                                              widget=forms.Select(
                                                  attrs={'class': 'form-control',
                                                         'id': 'olmis_priority_domain'})
                                              )
    olmis_priority_service = forms.ChoiceField(choices=(),
                                               initial='',
                                               widget=forms.SelectMultiple(
        attrs={'class': 'form-control',
               'id': 'olmis_priority_service'
               }))
    olmis_priority_service_provided_list = forms.CharField(widget=forms.TextInput(
        attrs={'type': 'hidden',
               'id': 'olmis_priority_service_provided_list'}))
    date_of_csi = forms.DateField(widget=forms.TextInput(
        attrs={'placeholder': _('Date Of CSI'),
               'class': 'form-control',
               'name': 'date_of_csi',
               'id': 'date_of_csi',
               'data-parsley-required': "true",
               'data-parsley-group': 'group2'
               }))
    person = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control',
               'id': 'person',
               'type': 'hidden',
               'data-parsley-required': "true",
               'data-parsley-group': 'group0'
               }))


class OVCF1AForm(forms.Form):
    olmis_assessment_domain = forms.ChoiceField(choices=olmis_assessment_domain_list,
                                                initial='0',
                                                widget=forms.Select(
                                                    attrs={'class': 'form-control',
                                                           'id': 'olmis_assessment_domain'})
                                                )
    olmis_assessment_coreservice = forms.ChoiceField(choices=(),
                                                     initial='0',
                                                     widget=forms.Select(
        attrs={'class': 'form-control',
               'id': 'olmis_assessment_coreservice'})
    )
    olmis_assessment_coreservice_status = forms.ChoiceField(choices=(),
                                                            initial='0',
                                                            widget=forms.SelectMultiple(
        attrs={'class': 'form-control',
               'id': 'olmis_assessment_coreservice_status'})
    )
    olmis_assessment_provided_list = forms.CharField(widget=forms.TextInput(
        attrs={'type': 'hidden',
               'id': 'olmis_assessment_provided_list'}))

    ## OLMIS SERVICES ##
    olmis_domain = forms.ChoiceField(choices=olmis_domain_list,
                                     initial='0',
                                     required=True,
                                     widget=forms.Select(
                                             attrs={'class': 'form-control',
                                                    'id': 'olmis_domain'})
                                     )
    olmis_subdomain = forms.ChoiceField(choices=olmis_domain_list,
                                        initial='0',
                                        required=True,
                                        widget=forms.Select(
                                            attrs={'class': 'form-control',
                                                   'id': 'olmis_subdomain'})
                                        )
    olmis_service = forms.ChoiceField(choices=(),
                                              initial='',
                                              widget=forms.SelectMultiple(
        attrs={'class': 'form-control',
               'id': 'olmis_service'
               }))
    olmis_service_provider = forms.ChoiceField(choices=olmis_service_provider_list,
                                               initial='0',
                                               required=True,
                                               widget=forms.Select(
                                                   attrs={'class': 'form-control',
                                                          'id': 'olmis_service_provider'})
                                               )
    olmis_service_date = forms.DateField(widget=forms.TextInput(
        attrs={'placeholder': _('Date Of Service'),
               'class': 'form-control',
               'id': 'olmis_service_date'
               }))
    olmis_place_of_service = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': _('Place of Service'),
               'class': 'form-control',
               'id': 'olmis_place_of_service'}))
    olmis_service_provided_list = forms.CharField(widget=forms.TextInput(
        attrs={'type': 'hidden',
               'id': 'olmis_service_provided_list'}))
    ## OLMIS PRIORITIES ##
    olmis_priority_domain = forms.ChoiceField(choices=olmis_domain_list,
                                              initial='0',
                                              widget=forms.Select(
                                                  attrs={'class': 'form-control',
                                                         'id': 'olmis_priority_domain'})
                                              )
    olmis_priority_service = forms.MultipleChoiceField(choices=(),
                                                       initial='',
                                                       widget=forms.SelectMultiple(
        attrs={'class': 'form-control',
               'id': 'olmis_priority_service'
               }))
    olmis_priority_service_provided_list = forms.CharField(widget=forms.TextInput(
        attrs={'type': 'hidden',
               'id': 'olmis_priority_service_provided_list'}))
    olmis_priority_health = forms.ChoiceField(choices=(),
                                              initial='0',
                                              widget=forms.SelectMultiple(
        attrs={'class': 'form-control',
               'id': 'olmis_priority_health',
               'data-parsley-required': "true",
               'data-parsley-group': 'group2'})
    )
    olmis_priority_shelter = forms.ChoiceField(choices=(),
                                               initial='0',
                                               widget=forms.SelectMultiple(
        attrs={'class': 'form-control',
               'id': 'olmis_priority_shelter',
               'data-parsley-required': "true",
               'data-parsley-group': 'group2'})
    )
    olmis_priority_education = forms.ChoiceField(choices=(),
                                                 initial='0',
                                                 widget=forms.SelectMultiple(
        attrs={'class': 'form-control',
               'id': 'olmis_priority_education',
               'data-parsley-required': "true",
               'data-parsley-group': 'group2'})
    )
    olmis_priority_protection = forms.ChoiceField(choices=(),
                                                  initial='0',
                                                  widget=forms.SelectMultiple(
        attrs={'class': 'form-control',
               'id': 'olmis_priority_protection',
               'data-parsley-required': "true",
               'data-parsley-group': 'group2'})
    )
    olmis_priority_pss = forms.ChoiceField(choices=(),
                                           initial='0',
                                           widget=forms.SelectMultiple(
        attrs={'class': 'form-control',
               'id': 'olmis_priority_pss',
               'data-parsley-required': "true",
               'data-parsley-group': 'group2'})
    )
    olmis_priority_hes = forms.ChoiceField(choices=(),
                                           initial='0',
                                           widget=forms.SelectMultiple(
        attrs={
            #'class': 'form-control',
            'id': 'olmis_priority_hes',
            'data-parsley-required': "true",
            'data-parsley-group': 'group2'})
    )
    ## OLMIS CRITICAL EVENTS ##
    olmis_critical_event = forms.ChoiceField(choices=olmis_critical_events_list,
                                             initial='0',
                                             widget=forms.SelectMultiple(
                                                 attrs={'class': 'form-control',
                                                        'id': 'olmis_critical_event'
                                                        #'data-parsley-required': "true",
                                                        #'data-parsley-group': 'group3'
                                                        })
                                             )

    date_of_assessment = forms.DateField(widget=forms.TextInput(
        attrs={'placeholder': _('Date of Event'),
               'class': 'form-control',
               'name': 'date_of_assessment',
               'id': 'date_of_assessment'
               #'data-parsley-required': "true",
               #'data-parsley-group': 'group3'
               }))
    date_of_service = forms.DateField(widget=forms.TextInput(
        attrs={'placeholder': _('Date of Event'),
               'class': 'form-control',
               'name': 'date_of_service',
               'id': 'date_of_service'
               #'data-parsley-required': "true",
               #'data-parsley-group': 'group3'
               }))
    date_of_cevent = forms.DateField(widget=forms.TextInput(
        attrs={'placeholder': _('Date of Event'),
               'class': 'form-control',
               'name': 'date_of_cevent',
               'id': 'date_of_cevent'
               #'data-parsley-required': "true",
               #'data-parsley-group': 'group3'
               }))
    date_of_priority = forms.DateField(widget=forms.TextInput(
        attrs={'placeholder': _('Date of Event'),
               'class': 'form-control',
               'name': 'date_of_priority',
               'id': 'date_of_priority'
               #'data-parsley-required': "true",
               #'data-parsley-group': 'group3'
               }))
    person = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control',
               'id': 'person',
               'type': 'hidden'
               #'data-parsley-required': "true",
               #'data-parsley-group': 'group3'
               }))
    caretaker_id = forms.CharField(widget=forms.HiddenInput(
        attrs={'id': 'caretaker_id'}))


class OVCHHVAForm(forms.Form):
    # Household Individuals
    hhva_ha1_male = forms.CharField(widget=forms.TextInput(
        attrs={
            'placeholder': _('Male'),
            'class': 'form-control',
            'id': 'hhva_ha1_male',
            'data-parsley-type': "digits",
            'data-parsley-required': "true",
            'data-parsley-group': 'group0'})
    )
    hhva_ha1_female = forms.CharField(widget=forms.TextInput(
        attrs={
            'placeholder': _('Female'),
            'class': 'form-control',
            'id': 'hhva_ha1_female',
            'data-parsley-type': "digits",
            'data-parsley-required': "true",
            'data-parsley-group': 'group0'})
    )
    hhva_ha2_male = forms.CharField(widget=forms.TextInput(
        attrs={
            'placeholder': _('Male'),
            'class': 'form-control',
            'id': 'hhva_ha2_male',
            'data-parsley-type': "digits",
            'data-parsley-required': "true",
            'data-parsley-group': 'group0'})
    )
    hhva_ha2_female = forms.CharField(widget=forms.TextInput(
        attrs={
            'placeholder': _('Female'),
            'class': 'form-control',
            'id': 'hhva_ha2_female',
            'data-parsley-type': "digits",
            'data-parsley-required': "true",
            'data-parsley-group': 'group0'})
    )
    hhva_ha3_male = forms.CharField(widget=forms.TextInput(
        attrs={
            'placeholder': _('Male'),
            'class': 'form-control',
            'id': 'hhva_ha3_male',
            'data-parsley-type': "digits",
            'data-parsley-required': "true",
            'data-parsley-group': 'group0'})
    )
    hhva_ha3_female = forms.CharField(widget=forms.TextInput(
        attrs={
            'placeholder': _('Female'),
            'class': 'form-control',
            'id': 'hhva_ha3_female',
            'data-parsley-type': "digits",
            'data-parsley-required': "true",
            'data-parsley-group': 'group0'})
    )
    hhva_ha4_male = forms.CharField(widget=forms.TextInput(
        attrs={
            'placeholder': _('Male'),
            'class': 'form-control',
            'id': 'hhva_ha4_male',
            'data-parsley-type': "digits",
            'data-parsley-required': "true",
            'data-parsley-group': 'group0'})
    )
    hhva_ha4_female = forms.CharField(widget=forms.TextInput(
        attrs={
            'placeholder': _('Female'),
            'class': 'form-control',
            'id': 'hhva_ha4_female',
            'data-parsley-type': "digits",
            'data-parsley-required': "true",
            'data-parsley-group': 'group0'})
    )

    # Water Sanitation and Hygiene
    hhva_ha5 = forms.ChoiceField(choices=olmis_ha5_list,
                                 initial='0',
                                 widget=forms.Select(
                                     attrs={'class': 'form-control',
                                            'id': 'hhva_ha5',
                                            'data-parsley-required': "true",
                                            'data-parsley-group': 'group1'})
                                 )
    hhva_ha6 = forms.ChoiceField(choices=olmis_ha6_list,
                                 initial='0',
                                 widget=forms.SelectMultiple(
                                     attrs={'class': 'form-control',
                                            'id': 'hhva_ha6',
                                            'data-parsley-required': "true",
                                            'data-parsley-group': 'group1'})
                                 )
    hhva_ha7 = forms.ChoiceField(choices=olmis_ha7_list,
                                 initial='0',
                                 widget=forms.Select(
                                     attrs={'class': 'form-control',
                                            'id': 'hhva_ha7',
                                            'data-parsley-required': "true",
                                            'data-parsley-group': 'group1'})
                                 )
    hhva_ha8 = forms.ChoiceField(choices=olmis_ha8_list,
                                 initial='0',
                                 widget=forms.Select(
                                     attrs={'class': 'form-control',
                                            'id': 'hhva_ha8',
                                            'data-parsley-required': "true",
                                            'data-parsley-group': 'group1'})
                                 )

    # Shelter and Care
    hhva_ha9 = forms.ChoiceField(choices=olmis_ha9_list,
                                 initial='0',
                                 widget=forms.Select(
                                     attrs={'class': 'form-control',
                                            'id': 'hhva_ha9',
                                            'data-parsley-required': "true",
                                            'data-parsley-group': 'group2'})
                                 )
    hhva_ha10_type = forms.ChoiceField(choices=olmis_ha10_type_list,
                                       initial='0',
                                       widget=forms.Select(
                                           attrs={'class': 'form-control',
                                                  'id': 'hhva_ha10_type'})
                                       )
    hhva_ha10_number = forms.CharField(widget=forms.TextInput(
        attrs={
            'placeholder': _('Number'),
            'class': 'form-control',
            'id': 'hhva_ha10_number',
            'data-parsley-type': "digits"})
    )
    hhva_ha10_condition = forms.ChoiceField(choices=olmis_ha10_condition_list,
                                            initial='0',
                                            widget=forms.Select(
                                                attrs={'class': 'form-control',
                                                       'id': 'hhva_ha10_condition'})
                                            )
    hhva_wash_list = forms.CharField(widget=forms.TextInput(
        attrs={'type': 'hidden',
               'id': 'hhva_wash_list'}))

    # Food Security and Nutrition
    hhva_ha11 = forms.ChoiceField(choices=olmis_ha11_list,
                                  initial='0',
                                  widget=forms.Select(
                                      attrs={'class': 'form-control',
                                             'id': 'hhva_ha11',
                                             'data-parsley-required': "true",
                                             'data-parsley-group': 'group3'})
                                  )
    hhva_ha12 = forms.ChoiceField(choices=olmis_ha12_list,
                                  initial='0',
                                  widget=forms.Select(
                                      attrs={'class': 'form-control',
                                             'id': 'hhva_ha12',
                                             'data-parsley-required': "true",
                                             'data-parsley-group': 'group3'})
                                  )

    # Household Income & Property
    hhva_ha13 = forms.ChoiceField(choices=olmis_ha13_list,
                                  initial='0',
                                  widget=forms.Select(
                                      attrs={'class': 'form-control',
                                             'id': 'hhva_ha13',
                                             'data-parsley-required': "true",
                                             'data-parsley-group': 'group4'})
                                  )
    hhva_ha14 = forms.ChoiceField(choices=olmis_ha14_list,
                                  initial='0',
                                  widget=forms.Select(
                                      attrs={'class': 'form-control',
                                             'id': 'hhva_ha14',
                                             'data-parsley-required': "true",
                                             'data-parsley-group': 'group4'})
                                  )
    hhva_ha15_asset = forms.ChoiceField(choices=olmis_ha15_list,
                                        initial='0',
                                        widget=forms.Select(
                                            attrs={'class': 'form-control',
                                                   'id': 'hhva_ha15_asset'})
                                        )
    hhva_ha15_number = forms.CharField(widget=forms.TextInput(
        attrs={
            'placeholder': _('Number'),
            'class': 'form-control',
            'id': 'hhva_ha15_number',
            'data-parsley-type': "digits"})
    )
    hhva_ha15_size = forms.CharField(widget=forms.TextInput(
        attrs={
            'placeholder': _('Size'),
            'class': 'form-control',
            'id': 'hhva_ha15_size',
            'data-parsley-type': "digits"})
    )
    hhva_asset_list = forms.CharField(widget=forms.TextInput(
        attrs={'type': 'hidden',
               'id': 'hhva_asset_list'}))
    hhva_ha16 = forms.ChoiceField(choices=olmis_ha16_list,
                                  initial='0',
                                  widget=forms.Select(
                                      attrs={'class': 'form-control',
                                             'id': 'hhva_ha16',
                                             'data-parsley-required': "true",
                                             'data-parsley-group': 'group4'})
                                  )
    hhva_ha17 = forms.ChoiceField(choices=olmis_ha17_list,
                                  initial='0',
                                  widget=forms.Select(
                                      attrs={'class': 'form-control',
                                             'id': 'hhva_ha17',
                                             'data-parsley-required': "true",
                                             'data-parsley-group': 'group4'})
                                  )
    hhva_ha18 = forms.ChoiceField(choices=olmis_ha18_list,
                                  initial='0',
                                  widget=forms.Select(
                                      attrs={'class': 'form-control',
                                             'id': 'hhva_ha18',
                                             'data-parsley-required': "true",
                                             'data-parsley-group': 'group4'})
                                  )
    hhva_ha19 = forms.ChoiceField(choices=olmis_ha19_list,
                                  initial='0',
                                  widget=forms.Select(
                                      attrs={'class': 'form-control',
                                             'id': 'hhva_ha19',
                                             'data-parsley-required': "true",
                                             'data-parsley-group': 'group4'})
                                  )
    hhva_ha20 = forms.ChoiceField(choices=olmis_ha20_list,
                                  initial='0',
                                  widget=forms.Select(
                                      attrs={'class': 'form-control',
                                             'id': 'hhva_ha20',
                                             'data-parsley-required': "true",
                                             'data-parsley-group': 'group4'})
                                  )
    hhva_ha21 = forms.ChoiceField(choices=olmis_ha21_list,
                                  initial='0',
                                  widget=forms.SelectMultiple(
                                      attrs={'class': 'form-control',
                                             'id': 'hhva_ha21',
                                             'data-parsley-required': "true",
                                             'data-parsley-group': 'group4'})
                                  )

    # Health Services and Health Seeking Behaviours
    hhva_ha22 = forms.ChoiceField(choices=olmis_ha22_list,
                                  initial='0',
                                  widget=forms.SelectMultiple(
                                      attrs={'class': 'form-control',
                                             'id': 'hhva_ha22',
                                             'data-parsley-required': "true",
                                             'data-parsley-group': 'group5'})
                                  )
    hhva_ha23 = forms.ChoiceField(choices=olmis_ha23_list,
                                  initial='0',
                                  widget=forms.Select(
                                      attrs={'class': 'form-control',
                                             'id': 'hhva_ha23',
                                             'data-parsley-required': "true",
                                             'data-parsley-group': 'group5'})
                                  )
    hhva_ha24 = forms.ChoiceField(choices=olmis_ha24_list,
                                  initial='0',
                                  widget=forms.Select(
                                      attrs={'class': 'form-control',
                                             'id': 'hhva_ha24',
                                             'data-parsley-required': "true",
                                             'data-parsley-group': 'group5'})
                                  )
    hhva_ha25 = forms.ChoiceField(choices=olmis_ha25_list,
                                  initial='0',
                                  widget=forms.Select(
                                      attrs={'class': 'form-control',
                                             'id': 'hhva_ha25',
                                             'data-parsley-required': "true",
                                             'data-parsley-group': 'group5'})
                                  )
    hhva_ha26_male = forms.CharField(widget=forms.TextInput(
        attrs={
            'placeholder': _('Male'),
            'class': 'form-control',
            'id': 'hhva_ha26_male',
            'data-parsley-type': "digits",
            'data-parsley-required': "true",
            'data-parsley-group': 'group5'})
    )
    hhva_ha26_female = forms.CharField(widget=forms.TextInput(
        attrs={
            'placeholder': _('Female'),
            'class': 'form-control',
            'id': 'hhva_ha26_female',
            'data-parsley-type': "digits",
            'data-parsley-required': "true",
            'data-parsley-group': 'group5'})
    )
    hhva_ha27_male = forms.CharField(widget=forms.TextInput(
        attrs={
            'placeholder': _('Male'),
            'class': 'form-control',
            'id': 'hhva_ha27_male',
            'data-parsley-type': "digits",
            'data-parsley-required': "true",
            'data-parsley-group': 'group5'})
    )
    hhva_ha27_female = forms.CharField(widget=forms.TextInput(
        attrs={
            'placeholder': _('Female'),
            'class': 'form-control',
            'id': 'hhva_ha27_female',
            'data-parsley-type': "digits",
            'data-parsley-required': "true",
            'data-parsley-group': 'group5'})
    )

    # Protection
    hhva_ha28 = forms.ChoiceField(choices=olmis_ha28_list,
                                  initial='0',
                                  widget=forms.SelectMultiple(
                                      attrs={'class': 'form-control',
                                             'id': 'hhva_ha28',
                                             'data-parsley-required': "true",
                                             'data-parsley-group': 'group6'})
                                  )

    # Other Services
    hhva_ha29 = forms.ChoiceField(choices=olmis_ha29_list,
                                  initial='0',
                                  widget=forms.SelectMultiple(
                                      attrs={'class': 'form-control',
                                             'id': 'hhva_ha29',
                                             'data-parsley-required': "true",
                                             'data-parsley-group': 'group7'})
                                  )
    hhva_ha30 = forms.ChoiceField(choices=olmis_ha30_list,
                                  initial='0',
                                  widget=forms.SelectMultiple(
                                      attrs={'class': 'form-control',
                                             'id': 'hhva_ha30',
                                             'data-parsley-required': "true",
                                             'data-parsley-group': 'group7'})
                                  )

    # Household Priorities
    hhva_ha31 = forms.ChoiceField(choices=olmis_ha31_list,
                                  initial='0',
                                  widget=forms.SelectMultiple(
                                      attrs={'class': 'form-control',
                                             'id': 'hhva_ha31',
                                             'data-parsley-required': "true",
                                             'data-parsley-group': 'group8'})
                                  )
    date_of_hhva = forms.DateField(widget=forms.TextInput(
        attrs={'placeholder': _('Date Of HHVA'),
               'class': 'form-control',
               'name': 'date_of_hhva',
               'id': 'date_of_hhva',
               'data-parsley-required': "true",
               'data-parsley-group': 'group0'
               }))
    person = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control',
               'id': 'person',
               'type': 'hidden'
               }))
    household_id = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control',
               'id': 'household_id',
               'type': 'hidden'
               }))


class RadioCustomRenderer(RadioFieldRenderer):
    """Custom radio button renderer class."""

    def render(self):
        """Renderer override method."""
        return mark_safe(u'%s' % u'\n'.join(
            [u'%s' % force_unicode(w) for w in self]))


class GOKBursaryForm(forms.Form):
    # Household Individuals
    kcpe_marks = forms.CharField(widget=forms.TextInput(
        attrs={
            'placeholder': _('KCPE Marks'),
            'class': 'form-control',
            'id': 'kcpe_marks',
            'data-parsley-type': "digits",
            'data-parsley-required': "true",
            'data-parsley-group': 'group1'})
    )
    child_county = forms.ChoiceField(
        choices=county_list,
        initial='0',
        widget=forms.Select(
            attrs={'class': 'form-control',
                   'data-parsley-required': "true",
                   'data-parsley-group': "group1"}))
    child_constituency = forms.ChoiceField(
        choices=sub_county_list,
        initial='0',
        widget=forms.Select(
            attrs={'class': 'form-control',
                   'data-parsley-required': "true",
                   'data-parsley-group': "group1"}))

    # Page - 1
    child_location = forms.CharField(widget=forms.TextInput(
        attrs={
            'placeholder': _('Location'),
            'class': 'form-control',
            'data-parsley-group': 'group1'})
    )
    child_sub_county = forms.CharField(widget=forms.TextInput(
        attrs={
            'placeholder': _('Sub-County'),
            'class': 'form-control',
            'data-parsley-group': 'group1'})
    )
    child_sub_location = forms.CharField(widget=forms.TextInput(
        attrs={
            'placeholder': _('Sub-Location'),
            'class': 'form-control',
            'data-parsley-group': 'group1'})
    )
    child_village = forms.CharField(widget=forms.TextInput(
        attrs={
            'placeholder': _('Village'),
            'class': 'form-control',
            'data-parsley-required': "true",
            'data-parsley-group': 'group1'})
    )
    nearest_school = forms.CharField(widget=forms.TextInput(
        attrs={
            'placeholder': _('School Name'),
            'class': 'form-control',
            'data-parsley-group': 'group1'})
    )
    nearest_worship = forms.CharField(widget=forms.TextInput(
        attrs={
            'placeholder': _('Church / Mosque'),
            'class': 'form-control',
            'data-parsley-group': 'group1'})
    )
    school_name = forms.CharField(widget=forms.TextInput(
        attrs={
            'placeholder': _('School Name'),
            'class': 'form-control',
            'data-parsley-group': 'group1'})
    )
    school_class = forms.CharField(widget=forms.TextInput(
        attrs={
            'placeholder': _('School Class'),
            'class': 'form-control',
            'data-parsley-group': 'group1'})
    )
    in_school = forms.ChoiceField(
        choices=YESNO_CHOICES,
        widget=forms.RadioSelect(
            renderer=RadioCustomRenderer,
            attrs={'data-parsley-required': 'true',
                   'data-parsley-errors-container': "#in_school_error"})
    )

    pri_school_name = forms.CharField(widget=forms.TextInput(
        attrs={
            'placeholder': _('Primary School Name'),
            'class': 'form-control',
            'data-parsley-group': 'group1'})
    )

    father_name = forms.CharField(widget=forms.TextInput(
        attrs={
            'placeholder': _('Father Name'),
            'class': 'form-control',
            'data-parsley-group': 'group1'})
    )
    mother_name = forms.CharField(widget=forms.TextInput(
        attrs={
            'placeholder': _('Mother Name'),
            'class': 'form-control',
            'data-parsley-group': 'group1'})
    )
    guardian_name = forms.CharField(widget=forms.TextInput(
        attrs={
            'placeholder': _('Guardian Name'),
            'class': 'form-control',
            'data-parsley-group': 'group1'})
    )

    father_contact = forms.CharField(widget=forms.TextInput(
        attrs={
            'placeholder': _('Father Phone'),
            'class': 'form-control',
            'data-parsley-group': 'group1'})
    )
    
    father_alive = forms.ChoiceField(
        choices=YESNO_CHOICES,
        widget=forms.RadioSelect(
            renderer=RadioCustomRenderer,
            attrs={'data-parsley-required': 'true',
                   'data-parsley-errors-container': "#father_alive_error"}))
    mother_contact = forms.CharField(widget=forms.TextInput(
        attrs={
            'placeholder': _('Mother Phone'),
            'class': 'form-control',
            'data-parsley-group': 'group1'})
    )
   
    guardian_contact = forms.CharField(widget=forms.TextInput(
        attrs={
            'placeholder': _('Guardian Phone'),
            'class': 'form-control',
            'data-parsley-group': 'group1'})
    )
    guardian_occupation = forms.CharField(widget=forms.TextInput(
        attrs={
            'placeholder': _('Guardian Contact'),
            'class': 'form-control',
            'data-parsley-group': 'group1'})
    )
    
    mother_alive = forms.ChoiceField(
        choices=YESNO_CHOICES,
        widget=forms.RadioSelect(
            renderer=RadioCustomRenderer,
            attrs={'data-parsley-required': 'true',
                   'data-parsley-errors-container': "#mother_alive_error"}))

    guardian_relation = forms.CharField(widget=forms.TextInput(
        attrs={
            'placeholder': _('Guardian relation'),
            'class': 'form-control',
            'data-parsley-group': 'group1'})
    )
    living_with = forms.ChoiceField(
        choices=YESNO_CHOICES,
        widget=forms.RadioSelect(
            renderer=RadioCustomRenderer,
            attrs={'data-parsley-required': 'true',
                   'data-parsley-errors-container': "#living_with_error"}))

    father_ill = forms.ChoiceField(
        choices=YESNO_CHOICES,
        widget=forms.RadioSelect(
            renderer=RadioCustomRenderer,
            attrs={'data-parsley-required': 'true',
                   'data-parsley-errors-container': "#father_ill_error"}))

    mother_ill = forms.ChoiceField(
        choices=YESNO_CHOICES,
        widget=forms.RadioSelect(
            renderer=RadioCustomRenderer,
            attrs={'data-parsley-required': 'true',
                   'data-parsley-errors-container': "#mother_ill_error"}))
    father_illness = forms.CharField(widget=forms.TextInput(
        attrs={
            'placeholder': _('Father Illness'),
            'class': 'form-control',
            'data-parsley-group': 'group1'})
    )
    mother_illness = forms.CharField(widget=forms.TextInput(
        attrs={
            'placeholder': _('Mother Illness'),
            'class': 'form-control',
            'data-parsley-group': 'group1'})
    )

    father_disabled = forms.ChoiceField(
        choices=YESNO_CHOICES,
        widget=forms.RadioSelect(
            renderer=RadioCustomRenderer,
            attrs={'data-parsley-required': 'true',
                   'data-parsley-errors-container': "#father_disabled_error"}))
    mother_disabled = forms.ChoiceField(
        choices=YESNO_CHOICES,
        widget=forms.RadioSelect(
            renderer=RadioCustomRenderer,
            attrs={'data-parsley-required': 'true',
                   'data-parsley-errors-container': "#mother_disabled_error"}))
    father_disability = forms.CharField(widget=forms.TextInput(
        attrs={
            'placeholder': _('Father Disability'),
            'class': 'form-control',
            'data-parsley-group': 'group1'})
    )
    mother_disability = forms.CharField(widget=forms.TextInput(
        attrs={
            'placeholder': _('Mother Disability'),
            'class': 'form-control',
            'data-parsley-group': 'group1'})
    )

    father_occupation = forms.CharField(widget=forms.TextInput(
        attrs={
            'placeholder': _('Father Occupation'),
            'class': 'form-control',
            'data-parsley-required': "true",
            'data-parsley-group': 'group1'})
    )
    father_pension = forms.ChoiceField(
        choices=YESNO_CHOICES,
        widget=forms.RadioSelect(
            renderer=RadioCustomRenderer,
            attrs={'data-parsley-required': 'true',
                   'data-parsley-errors-container': "#father_pension_error"}))
    mother_occupation = forms.CharField(widget=forms.TextInput(
        attrs={
            'placeholder': _('Mother Occupation'),
            'class': 'form-control',
            'data-parsley-required': "true",
            'data-parsley-group': 'group1'})
    )
    mother_pension = forms.ChoiceField(
        choices=YESNO_CHOICES,
        widget=forms.RadioSelect(
            renderer=RadioCustomRenderer,
            attrs={'data-parsley-required': 'true',
                   'data-parsley-errors-container': "#mother_pension_error"}))
    fees_amount = forms.CharField(widget=forms.TextInput(
        attrs={
            'placeholder': _('Fees Amount'),
            'class': 'form-control',
            'data-parsley-type': "digits",
            'data-parsley-required': "true",
            'data-parsley-group': 'group1'})
    )
    balance_amount = forms.CharField(widget=forms.TextInput(
        attrs={
            'placeholder': _('Balance Amount'),
            'class': 'form-control',
            'data-parsley-type': "digits",
            'data-parsley-required': "true",
            'data-parsley-group': 'group1'})
    )
    school_name = forms.CharField(widget=forms.TextInput(
        attrs={
            'placeholder': _('School Name.'),
            'class': 'form-control',
            'data-parsley-required': "true",
            'data-parsley-group': 'group1'})
    )
    principal_name = forms.CharField(widget=forms.TextInput(
        attrs={
            'placeholder': _('Principal Name.'),
            'class': 'form-control',
            'data-parsley-required': "true",
            'data-parsley-group': 'group1'})
    )
    school_phone = forms.CharField(widget=forms.TextInput(
        attrs={
            'placeholder': _('Phone No.'),
            'class': 'form-control',
            'data-parsley-group': 'group1'})
    )
    school_email = forms.CharField(widget=forms.TextInput(
        attrs={
            'placeholder': _('Email.'),
            'class': 'form-control',
            'data-parsley-group': 'group1'})
    )
    school_county = forms.ChoiceField(
        choices=county_list,
        initial='0',
        widget=forms.Select(
            attrs={'class': 'form-control',
                   'data-parsley-required': "true",
                   'data-parsley-group': "group1"}))
    school_constituency = forms.ChoiceField(
        choices=sub_county_list,
        initial='0',
        widget=forms.Select(
            attrs={'class': 'form-control',
                   'data-parsley-required': "true",
                   'data-parsley-group': "group1"}))

    school_location = forms.CharField(widget=forms.TextInput(
        attrs={
            'placeholder': _('Location'),
            'class': 'form-control',
            'data-parsley-group': 'group1'})
    )
    school_sub_county = forms.CharField(widget=forms.TextInput(
        attrs={
            'placeholder': _('Sub-County'),
            'class': 'form-control',
            'data-parsley-group': 'group1'})
    )
    school_sub_location = forms.CharField(widget=forms.TextInput(
        attrs={
            'placeholder': _('Sub-Location'),
            'class': 'form-control',
            'data-parsley-group': 'group1'})
    )
    school_village = forms.CharField(widget=forms.TextInput(
        attrs={
            'placeholder': _('Village'),
            'class': 'form-control',
            'data-parsley-group': 'group1'})
    )
    
    school_address = forms.CharField(widget=forms.Textarea(
        attrs={'rows': '3', 'class': 'form-control'}))

    school_type = forms.ChoiceField(
        choices=bursary_school_type_list,
        widget=forms.RadioSelect(
            renderer=RadioCustomRenderer,
            attrs={'data-parsley-required': 'true',
                   'data-parsley-errors-container': "#school_type_error"}))
    school_category = forms.ChoiceField(
        choices=bursary_school_category_list,
        widget=forms.RadioSelect(
            renderer=RadioCustomRenderer,
            attrs={'data-parsley-required': 'true',
                   'data-parsley-errors-container': "#school_category_error"}))
    school_enrolled = forms.ChoiceField(
        choices=bursary_school_enrolled_list,
        widget=forms.RadioSelect(
            renderer=RadioCustomRenderer,
            attrs={'data-parsley-required': 'true',
                   'data-parsley-errors-container': "#school_enrolled_error"}))

    bank = forms.ChoiceField(
      choices=bank_list,
      initial='0',
      widget=forms.Select(attrs={'class': 'form-control'}))

    bank_branch = forms.CharField(widget=forms.TextInput(
        attrs={
            'placeholder': _('Bank Branch'),
            'class': 'form-control',
            'data-parsley-required': "true",
            'data-parsley-group': 'group1'})
    )
    bank_account = forms.CharField(widget=forms.TextInput(
        attrs={
            'placeholder': _('Account Number.'),
            'class': 'form-control',
            'data-parsley-required': "true",
            'data-parsley-group': 'group1'})
    )
    approved_csac = forms.ChoiceField(
        choices=YESNO_CHOICES,
        widget=forms.RadioSelect(
            renderer=RadioCustomRenderer,
            attrs={'data-parsley-required': 'true',
                   'data-parsley-errors-container': "#approved_csac_error"}))
    approved_amount = forms.CharField(widget=forms.TextInput(
        attrs={
            'placeholder': _('Approved Amount'),
            'class': 'form-control',
            'data-parsley-type': "digits",
            'data-parsley-required': "true",
            'data-parsley-group': 'group1'})
    )
    signed_scco = forms.ChoiceField(
        choices=YESNO_CHOICES,
        widget=forms.RadioSelect(
            renderer=RadioCustomRenderer,
            attrs={'data-parsley-required': 'true',
                   'data-parsley-errors-container': "#signed_scco_error"}))
    signed_csac = forms.ChoiceField(
        choices=YESNO_CHOICES,
        widget=forms.RadioSelect(
            renderer=RadioCustomRenderer,
            attrs={'data-parsley-required': 'true',
                   'data-parsley-errors-container': "#signed_csac_error"}))
    date_signed_scco = forms.CharField(widget=forms.TextInput(
        attrs={
            'placeholder': _('Date Signed'),
            'class': 'form-control',
            'data-parsley-required': "true",
            'data-parsley-group': 'group1'})
    )
    date_signed_csac = forms.CharField(widget=forms.TextInput(
        attrs={
            'placeholder': _('Date Signed'),
            'class': 'form-control',
            'data-parsley-required': "true",
            'data-parsley-group': 'group1'})
    )
    school_reason = forms.CharField(widget=forms.Textarea(
        attrs={'rows': '3', 'class': 'form-control'}))

    recommend_principal = forms.ChoiceField(
        choices=principal_list,
        widget=forms.RadioSelect(
            renderer=RadioCustomRenderer,
            attrs={'data-parsley-required': 'true',
                   'data-parsley-errors-container': "#recommend_principal_error"}))

    recommend_chief = forms.ChoiceField(
        choices=chief_list,
        widget=forms.RadioSelect(
            renderer=RadioCustomRenderer,
            attrs={'data-parsley-required': 'true',
                   'data-parsley-errors-container': "#recommend_chief_error"}))

    recommend_principal_date = forms.CharField(widget=forms.TextInput(
        attrs={
            'placeholder': _('Date Recommended'),
            'class': 'form-control',
            'data-parsley-required': "true",
            'data-parsley-group': 'group1'})
    )
    recommend_chief_date = forms.CharField(widget=forms.TextInput(
        attrs={
            'placeholder': _('Date Recommended'),
            'class': 'form-control',
            'data-parsley-required': "true",
            'data-parsley-group': 'group1'})
    )
    chief_telephone = forms.CharField(widget=forms.TextInput(
        attrs={
            'placeholder': _('Telephone No'),
            'class': 'form-control',
            'data-parsley-group': 'group1'})
    )
    scco_name = forms.CharField(widget=forms.TextInput(
        attrs={
            'placeholder': _('SCCO Name'),
            'class': 'form-control',
            'data-parsley-required': "true",
            'data-parsley-group': 'group1'})
    )
    csac_chair_name = forms.CharField(widget=forms.TextInput(
        attrs={
            'placeholder': _('CSAC Chair Name'),
            'class': 'form-control',
            'data-parsley-required': "true",
            'data-parsley-group': 'group1'})
    )
    application_date = forms.CharField(widget=forms.TextInput(
        attrs={
            'placeholder': _('Date of Application'),
            'class': 'form-control',
            'data-parsley-required': "true",
            'data-parsley-group': 'group1'})
    )
