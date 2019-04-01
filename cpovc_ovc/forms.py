"""OVC Registration forms."""
from django import forms
from django.utils.translation import ugettext_lazy as _
from cpovc_main.functions import get_list, get_org_units_list

search_criteria_list = (('', 'Select Criteria'), ('1', 'Names'),
                        ('2', 'HouseHold'), ('3', 'CHV'), ('4', 'CBO'),
                        ('5', 'Caregiver'))

immunization_list = get_list('immunization_status_id', 'Please Select')

person_type_list = get_list('person_type_id', 'Please Select Type')
school_level_list = get_list('school_level_id', 'Please Select Level')
hiv_status_list = get_list('hiv_status_id', 'Please Select HIV Status')
alive_status_list = get_list('yesno_id', '')
art_status_list = get_list('art_status_id', 'Please Select Status')
ovc_form_type_list = get_list('ovc_form_type_id', 'Please Select')
eligibility_list = get_list('eligibility_criteria_id', '')
death_cause_list = get_list('death_cause_id', 'Please Select Cause of Death')
exit_list = get_list('exit_reason_id', 'Please Select one')
admission_list = get_list('school_type_id', 'Please Select one')

health_unit_list = get_org_units_list(
    default_txt='Select Unit', org_types=['HFGU'])


class OVCSearchForm(forms.Form):
    """Search registry form."""

    search_name = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': _('Search . . .'),
               'class': 'form-control',
               'id': 'search_name',
               'data-parsley-minlength': '3',
               'data-parsley-required': 'true'}))

    search_criteria = forms.ChoiceField(
        choices=search_criteria_list,
        initial='0',
        required=True,
        widget=forms.Select(
            attrs={'class': 'form-control',
                   'data-parsley-required': "true",
                   'id': 'search_criteria'}))

    person_exited = forms.CharField(
        required=False,
        widget=forms.CheckboxInput(
            attrs={'id': 'person_exited'}))

    form_type = forms.ChoiceField(
        choices=ovc_form_type_list,
        initial='0',
        widget=forms.Select(
            attrs={'class': 'form-control',
                   'id': 'form_type'}))


class OVCRegistrationForm(forms.Form):
    """OVC registration form."""

    def __init__(self, guids, *args, **kwargs):
        """Override methods."""
        super(OVCRegistrationForm, self).__init__(*args, **kwargs)
        pids = guids['guids']
        kids = guids['chids']
        # Guardians
        for i in pids:
            gid = 'gstatus_%s' % str(i)
            aid = 'astatus_%s' % str(i)
            cid = 'cstatus_%s' % str(i)
            gstatus = forms.ChoiceField(
                choices=hiv_status_list,
                initial='0',
                widget=forms.Select(
                    attrs={'class': 'form-control', 'id': gid,
                           'data-parsley-required': "true"}))
            astatus = forms.ChoiceField(
                choices=alive_status_list,
                initial='AYES',
                widget=forms.Select(
                    attrs={'class': 'form-control alive', 'id': aid,
                           'data-parsley-required': "true"}))
            cstatus = forms.ChoiceField(
                choices=death_cause_list,
                initial='AYES',
                widget=forms.Select(
                    attrs={'class': 'form-control alive', 'id': cid}))
            self.fields[gid] = gstatus
            self.fields[aid] = astatus
            self.fields[cid] = cstatus
        # Siblings
        for i in kids:
            gid = 'sgstatus_%s' % str(i)
            aid = 'sastatus_%s' % str(i)
            sgstatus = forms.ChoiceField(
                choices=hiv_status_list,
                initial='0',
                widget=forms.Select(
                    attrs={'class': 'form-control', 'id': gid,
                           'data-parsley-required': "true"}))
            sastatus = forms.ChoiceField(
                choices=alive_status_list,
                initial='AYES',
                widget=forms.Select(
                    attrs={'class': 'form-control', 'id': aid,
                           'data-parsley-required': "true"}))
            self.fields[gid] = sgstatus
            self.fields[aid] = sastatus

    reg_date = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control',
               'id': 'reg_date',
               'data-parsley-required': "true"}))

    exit_date = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control',
               'id': 'exit_date',
               'data-parsley-required': "true"}))

    has_bcert = forms.CharField(
        widget=forms.CheckboxInput(
            attrs={'class': 'form-control',
                   'id': 'has_bcert'}))

    is_exited = forms.CharField(
        widget=forms.CheckboxInput(
            attrs={'class': 'form-control',
                   'id': 'is_exited'}))

    bcert_no = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control',
               'id': 'bcert_no'}))

    ncpwd_no = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control',
               'id': 'ncpwd_no'}))

    disb = forms.CharField(
        widget=forms.CheckboxInput(
            attrs={'class': 'form-control',
                   'id': 'disb'}))

    cbo_uid = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control',
               'initial': '00001',
               'id': 'cbo_uid',
               'data-parsley-required': "true"}))

    cbo_uid_check = forms.CharField(widget=forms.HiddenInput(
        attrs={'class': 'form-control',
               'initial': '00001',
               'id': 'cbo_uid_check'}))

    cbo_id = forms.CharField(widget=forms.HiddenInput(
        attrs={'class': 'form-control',
               'id': 'cbo_id'}))

    immunization = forms.ChoiceField(
        choices=immunization_list,
        initial='0',
        required=True,
        widget=forms.Select(
            attrs={'class': 'form-control',
                   'data-parsley-required': "true",
                   'id': 'immunization'}))

    eligibility = forms.MultipleChoiceField(
        choices=eligibility_list,
        initial='0',
        required=True,
        widget=forms.SelectMultiple(
            attrs={'class': 'form-control',
                   'data-parsley-required': "true",
                   'id': 'eligibility'}))

    exit_reason = forms.ChoiceField(
        choices=exit_list,
        initial='0',
        required=True,
        widget=forms.Select(
            attrs={'class': 'form-control',
                   'id': 'exit_reason'}))

    ovc_exit_reason = forms.ChoiceField(
        choices=exit_list,
        initial='0',
        required=True,
        widget=forms.Select(
            attrs={'class': 'form-control',
                   'id': 'ovc_exit_reason'}))

    hiv_status = forms.ChoiceField(
        choices=hiv_status_list,
        initial='0',
        required=True,
        widget=forms.Select(
            attrs={'class': 'form-control',
                   'data-parsley-required': "true",
                   'id': 'hiv_status'}))

    school_level = forms.ChoiceField(
        choices=school_level_list,
        initial='0',
        required=True,
        widget=forms.Select(
            attrs={'class': 'form-control',
                   'data-parsley-required': "true",
                   'id': 'school_level'}))

    facility = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control',
               'data-parsley-required': "true",
               'placeholder': 'Start typing then select',
               'id': 'facility'}))

    school_name = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control',
               'placeholder': 'Start typing then select',
               'id': 'school_name'}))

    art_status = forms.ChoiceField(
        choices=art_status_list,
        initial='0',
        required=True,
        widget=forms.Select(
            attrs={'class': 'form-control',
                   'data-parsley-required': "true",
                   'id': 'art_status'}))

    link_date = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control',
               'id': 'link_date'}))

    ccc_number = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control',
               'id': 'ccc_number'}))

    facility_id = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control',
               'readonly': 'readonly',
               'id': 'facility_id'}))

    school_id = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control',
               'readonly': 'readonly',
               'id': 'school_id'}))

    admission_type = forms.ChoiceField(
        choices=admission_list,
        initial='0',
        required=True,
        widget=forms.Select(
            attrs={'class': 'form-control',
                   'id': 'admission_type'}))

    school_class = forms.ChoiceField(
        choices=(),
        initial='0',
        required=True,
        widget=forms.Select(
            attrs={'class': 'form-control',
                   'id': 'school_class'}))

    exit_org_name = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control',
               'placeholder': 'Organization name exiting to',
               'id': 'exit_org_name'}))
