"""Forms for Registry sections of CPIMS."""
from django import forms
from django.utils.translation import ugettext_lazy as _
from cpovc_main.functions import get_list

person_type_list = ()
sex_id_list = get_list('sex_id', 'Select')


class NOTTForm(forms.Form):
    """Search registry form."""

    person_type = forms.ChoiceField(
        choices=person_type_list,
        initial='0',
        required=True,
        widget=forms.Select(
            attrs={'class': 'form-control',
                   'id': 'person_type',
                   'data-parsley-required': 'true'}))

    institution_name = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': _('Institution Name'),
               'class': 'form-control',
               'id': 'institution_name',
               'data-parsley-required': 'true'}))

    country_name = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': _('Country Name'),
               'class': 'form-control',
               'id': 'country_name',
               'data-parsley-required': 'true'}))

    travel_date = forms.CharField(widget=forms.DateInput(
        attrs={'placeholder': _('Travel Date'),
               'class': 'form-control',
               'id': 'travel_date',
               'data-parsley-required': 'true'}))

    return_date = forms.CharField(widget=forms.DateInput(
        attrs={'placeholder': _('Return Date'),
               'class': 'form-control',
               'id': 'return_date',
               'data-parsley-required': 'true'}))

    no_applied = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': _('No. applied'),
               'class': 'form-control',
               'id': 'no_applied',
               'data-parsley-required': 'true'}))

    no_cleared = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': _('No. cleared'),
               'class': 'form-control',
               'id': 'no_cleared',
               'data-parsley-required': 'true'}))

    no_returned = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': _('No. returned'),
               'class': 'form-control',
               'id': 'no_returned',
               'data-parsley-required': 'true'}))

    reason = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': _('Reason for Travel'),
               'class': 'form-control',
               'id': 'reason',
               'data-parsley-required': 'true'}))

    sponsor = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': _('Sponsor'),
               'class': 'form-control',
               'id': 'sponsor',
               'data-parsley-required': 'true'}))

    contacts = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': _('Contact Number'),
               'class': 'form-control',
               'id': 'contacts',
               'data-parsley-required': 'false'}))

    status = forms.CharField(
        required=False,
        widget=forms.CheckboxInput(
            attrs={'id': 'status'}))

    comments = forms.CharField(widget=forms.Textarea(
        attrs={'rows': '3',
               'id': 'comments',
               'class': 'form-control'}))


class ChaperonForm(forms.Form):
    first_name = forms.CharField(
        label='First Name',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': _('First Name')
        })
    )

    surname = forms.CharField(
        label='Surname',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': _('Surname')
        })
    )

    other_names = forms.CharField(
        label='Other Names',
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': _('Other Names')
        })
    )

    passport_no = forms.CharField(
        label='Passport No.',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': _('Passport No')
        })
    )

    sex = forms.ChoiceField(
        choices=sex_id_list,
        widget=forms.Select(
            attrs={'class': 'form-control',
                   'id': 'sex'}))

    person_id = forms.CharField(
        widget=forms.HiddenInput(
            attrs={'id': 'person_id'}))

    chaperon_id = forms.CharField(
        widget=forms.HiddenInput(
            attrs={'id': 'chaperon_id'}))


class ChildrenForm(forms.Form):
    first_name = forms.CharField(
        label='First Name',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': _('First Name')
        })
    )

    surname = forms.CharField(
        label='Surname',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': _('Surname')
        })
    )

    other_names = forms.CharField(
        label='Other Names',
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': _('Other Names')
        })
    )

    passport_no = forms.CharField(
        label='Passport No.',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': _('Passport No')
        })
    )

    sex = forms.ChoiceField(
        choices=sex_id_list,
        widget=forms.Select(
            attrs={'class': 'form-control',
                   'id': 'sex'}))

    cleared = forms.CharField(
        required=False,
        widget=forms.CheckboxInput(
            attrs={'id': 'cleared'}))

    returned = forms.CharField(
        required=False,
        widget=forms.CheckboxInput(
            attrs={'id': 'returned'}))

    person_id = forms.CharField(
        widget=forms.HiddenInput(
            attrs={'id': 'person_id'}))

    child_id = forms.CharField(
        widget=forms.HiddenInput(
            attrs={'id': 'child_id'}))
