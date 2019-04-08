"""Forms for Reports section of CPIMS."""
from django import forms
from cpovc_registry.functions import (
    get_all_geo_list, get_geo_list, get_specific_orgs)
from cpovc_main.functions import get_org_units_list

from .functions import create_year_list, get_clusters


all_list = get_all_geo_list()
county_list = get_geo_list(all_list, 'GPRV', 'Please Select County')
sub_county_list = get_geo_list(all_list, 'GDIS', 'Please Select Sub-county')
'''
document_type = get_list('document_type_id', 'Select report/document type')
'''
document_type = (('DSCE', 'Social enquiry'), ('DSUM', 'Summons'))
report_types = (('', 'Select type'), ('M', 'Monthly'),
                ('Q', 'Quarterly'), ('Y', 'Yearly'))

report_types_others = (('', 'Select type'), ('M', 'Monthly'),
                       ('Q', 'Quarterly'), ('Y', 'Yearly'), ('O', 'Others'))

report_types_datim = (('', 'Select type'), ('S', 'Semi Annual'),
                      ('Y', 'Annual'))

report_types_other = (('', 'Select type'), ('S', 'Semi Annual'),
                      ('Y', 'Annual'), ('O', 'Other'))

report_vars = (('', 'Select Variable'), (1, 'Organisation Unit'),
               (2, 'Institution Register'))
# (3, 'Case category'))
inst_vars = (('', 'Select Type'),
             ('TNCI', 'Charitable Children Institution'),
             ('TNSI', 'Statutory Institution'))

usg_reports = (('', 'Select Report'), (1, 'DATIM'),
               (2, 'Services by Domain (PEPFAR Summary)'),
               (3, 'Key Performance Indicator'),
               (4, 'CHV monthly RR'),
               (5, 'List of OVC not served'),
               (6, 'PEPFAR Summary'),
               (7, 'Registration by CHV'),
               (8, 'Beneficiary list'),
               (9, 'Form1A summary'),
               (10, 'Needs vs Served by domain'),
               (11, 'Form1B summary'),
               (12, 'List of OVC served'),
               (13, 'Master List'),
               (14, 'List of OVC Assessed'),
               (15, 'Priority List'))
report_period = ()

YEAR_CHOICES = create_year_list()
YEAR_ICHOICES = create_year_list(i_report=True)


class CaseLoad(forms.Form):
    """Class for case load reports forms."""

    def __init__(self, user, *args, **kwargs):
        """Constructor for override especially on fly data."""
        self.user = user
        super(CaseLoad, self).__init__(*args, **kwargs)
        org_units = get_specific_orgs(self.user.reg_person_id)
        org_inst = get_specific_orgs(self.user.reg_person_id, 1)
        # clusters
        cluster_list = get_clusters(self.user, "Please Select Cluster")
        if user.is_superuser:
            org_units = get_org_units_list('Please select Unit')
            inst_types = ['TNRH', 'TNRB', 'TNRR', 'TNRS', 'TNAP', 'TNRC']
            org_inst = get_org_units_list('Please select Unit', inst_types)
        org_unit = forms.ChoiceField(
            choices=org_units,
            initial='',
            widget=forms.Select(
                attrs={'class': 'form-control',
                       'autofocus': 'true'}))
        self.fields['org_unit'] = org_unit

        org_inst = forms.ChoiceField(
            choices=org_inst,
            initial='',
            widget=forms.Select(
                attrs={'class': 'form-control',
                       'autofocus': 'true',
                       'id': 'id_org_unit'}))
        self.fields['org_inst'] = org_inst

        cluster = forms.ChoiceField(
            choices=cluster_list,
            widget=forms.Select(
                attrs={'class': 'form-control',
                       'data-parsley-required': 'false',
                       'autofocus': 'true'}))
        self.fields['cluster'] = cluster

    county = forms.ChoiceField(
        choices=county_list,
        initial='',
        widget=forms.Select(
            attrs={'class': 'form-control',
                   'data-parsley-required': 'true',
                   'data-parsley-errors-container': "#county_error",
                   'id': 'county'}))
    sub_county = forms.ChoiceField(
        choices=sub_county_list,
        initial='',
        widget=forms.Select(
            attrs={'class': 'form-control',
                   'data-parsley-required': 'true',
                   'data-parsley-errors-container': "#sub_county_error",
                   'id': 'sub_county'}))

    document_type = forms.ChoiceField(
        choices=document_type,
        initial='',
        widget=forms.Select(
            attrs={'class': 'form-control',
                   'data-parsley-required': 'true',
                   'autofocus': 'true'}))

    report_type = forms.ChoiceField(
        choices=report_types,
        initial='',
        widget=forms.Select(
            attrs={'class': 'form-control',
                   'data-parsley-required': 'true',
                   'autofocus': 'true'}))

    report_type_datim = forms.ChoiceField(
        choices=report_types_datim,
        initial='',
        widget=forms.Select(
            attrs={'class': 'form-control',
                   'id': 'id_report_type',
                   'data-parsley-required': 'true',
                   'autofocus': 'true'}))

    report_type_other = forms.ChoiceField(
        choices=report_types_other,
        initial='',
        widget=forms.Select(
            attrs={'class': 'form-control',
                   'id': 'id_report_type',
                   'data-parsley-required': 'true',
                   'autofocus': 'true'}))

    report_type_others = forms.ChoiceField(
        choices=report_types_others,
        initial='',
        widget=forms.Select(
            attrs={'class': 'form-control',
                   'id': 'id_report_type',
                   'data-parsley-required': 'true',
                   'autofocus': 'true'}))

    report_year = forms.ChoiceField(
        choices=YEAR_CHOICES,
        initial='',
        widget=forms.Select(
            attrs={'class': 'form-control',
                   'data-parsley-required': 'true',
                   'autofocus': 'true'}))

    report_years = forms.ChoiceField(
        choices=YEAR_ICHOICES,
        initial='',
        widget=forms.Select(
            attrs={'class': 'form-control',
                   'data-parsley-required': 'true',
                   'autofocus': 'true', 'id': 'report_year'}))

    report_period = forms.ChoiceField(
        choices=report_period,
        initial='',
        widget=forms.Select(
            attrs={'class': 'form-control',
                   'data-parsley-required': 'true',
                   'autofocus': 'true'}))

    child = forms.IntegerField(widget=forms.TextInput(
        attrs={'class': 'form-control',
               'data-parsley-required': 'true',
               'id': 'child_id'}))

    report_from_date = forms.CharField(
        widget=forms.TextInput(
            attrs={'class': 'form-control',
                   'data-parsley-required': 'true',
                   'id': 'from_date'}))

    report_to_date = forms.CharField(
        widget=forms.TextInput(
            attrs={'class': 'form-control',
                   'data-parsley-required': 'true',
                   'id': 'to_date'}))

    cpims_child = forms.CharField(widget=forms.HiddenInput(
        attrs={'id': 'cpims_child_id'}))

    report_id = forms.CharField(widget=forms.HiddenInput(
        attrs={'id': 'report_id'}))

    report_vars = forms.ChoiceField(
        choices=report_vars,
        widget=forms.Select(
            attrs={'class': 'form-control',
                   'data-parsley-required': 'true',
                   'autofocus': 'true'}))

    institution_type = forms.ChoiceField(
        choices=inst_vars,
        widget=forms.Select(
            attrs={'class': 'form-control',
                   'data-parsley-required': 'true',
                   'autofocus': 'true'}))

    org_type = forms.ChoiceField(
        choices=(),
        widget=forms.Select(
            attrs={'class': 'form-control',
                   'data-parsley-required': 'false',
                   'autofocus': 'true'}))

    report_ovc = forms.ChoiceField(
        choices=usg_reports,
        widget=forms.Select(
            attrs={'class': 'form-control',
                   'data-parsley-required': 'true',
                   'autofocus': 'true'}))


class ClusterForm(forms.Form):
    """Class for case load reports forms."""

    def __init__(self, user, *args, **kwargs):
        """Override method especially for dynamic lookup data."""
        self.user = user
        super(ClusterForm, self).__init__(*args, **kwargs)
        org_units_list = get_specific_orgs(self.user.reg_person_id)

        if user.is_superuser:
            org_units_list = get_org_units_list('Please select Unit')

        cbo_unit_id = forms.MultipleChoiceField(
            choices=org_units_list,
            initial='',
            widget=forms.SelectMultiple(
                attrs={'class': 'form-control',
                       'data-parsley-required': 'true',
                       'id': 'cbo'}))

        self.fields['cbo'] = cbo_unit_id

    cluster = forms.CharField(
        widget=forms.TextInput(
            attrs={'class': 'form-control',
                   'data-parsley-required': 'true',
                   'id': 'cluster'}))
