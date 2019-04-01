from django import forms
from cpovc_registry.functions import (
    get_all_geo_list, get_geo_list, get_specific_orgs)
from cpovc_main.functions import get_org_units_list
from cpovc_reports.functions import get_clusters

lists_vars = (('', 'Select Report'), (1, 'Master List'),
               (2, 'Assessment List'), (3, 'Priorities List'),
               (4, 'Services List'))


class SettingsForm(forms.Form):
    """Class for Settings reports forms."""

    def __init__(self, user, *args, **kwargs):
        """Constructor for override especially on fly data."""
        self.user = user
        super(SettingsForm, self).__init__(*args, **kwargs)
        org_units = get_specific_orgs(self.user.reg_person_id)
        # clusters list
        cluster_list = get_clusters(self.user, "Please Select Cluster")
        if user.is_superuser:
            org_units = get_org_units_list('Please select Unit')

        org_unit = forms.ChoiceField(
            choices=org_units,
            initial='',
            widget=forms.Select(
                attrs={'class': 'form-control',
                       'data-parsley-required': 'false',
                       'autofocus': 'true'}))
        self.fields['org_unit'] = org_unit


        cluster = forms.ChoiceField(
            choices=cluster_list,
            widget=forms.Select(
                attrs={'class': 'form-control',
                       'data-parsley-required': 'false',
                       'autofocus': 'true'}))
        self.fields['cluster'] = cluster


    raw_data = forms.ChoiceField(
        choices=lists_vars,
        initial='',
        widget=forms.Select(
            attrs={'class': 'form-control',
                   'data-parsley-required': 'true',
                   'id': 'raw_data'}))

    report_from_date = forms.CharField(
        widget=forms.TextInput(
            attrs={'class': 'form-control',
                   'data-parsley-required': 'true',
                   'placeholder': 'Start date',
                   'id': 'report_from_date'}))

    report_to_date = forms.CharField(
        widget=forms.TextInput(
            attrs={'class': 'form-control',
                   'data-parsley-required': 'true',
                   'placeholder': 'End date',
                   'id': 'report_to_date'}))
