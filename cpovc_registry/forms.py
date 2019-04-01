"""Forms for Registry sections of CPIMS."""
from django import forms
from django.utils.translation import ugettext_lazy as _
from django.forms.widgets import RadioFieldRenderer
from django.utils.encoding import force_unicode
from django.utils.safestring import mark_safe

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout
from .functions import (
    get_org_units, get_all_geo_list, get_geo_list, get_specific_orgs,
    get_user_geos, get_chvs)
from cpovc_main.functions import get_list, get_org_units_list
from .models import RegPerson

from cpovc_main.country import OCOUNTRIES
from cpovc_access.forms import StrictSetPasswordForm


my_list = []
for country in OCOUNTRIES:
    my_list.append((country, OCOUNTRIES[country]))
country_list = list(my_list)


person_type_list = get_list('person_type_id', 'Please Select')
org_unit_type_list = get_list('org_unit_type_id', 'Please Select')
relationship_type_list = get_list('relationship_type_id', 'Please Select')
external_id_list = get_list('identifier_type_id', 'Please Select')
cadre_type_list = get_list('cadre_type_id', 'Please Select')
sex_id_list = get_list('sex_id', 'Please Select')
psearch_criteria_list = get_list('psearch_criteria_type_id', 'Select Criteria')
org_units_list = get_org_units_list('Please select Unit')
classes_list = get_list('class_level_id', 'Please Select')

all_list = get_all_geo_list()
county_list = get_geo_list(all_list, 'GPRV')
sub_county_list = get_geo_list(all_list, 'GDIS')
ward_list = get_geo_list(all_list, 'GWRD')


YESNO_CHOICES = get_list('yesno_id')

# org_unit_type_id
reg_list = get_list('organisation_type_id', 'Select unit type')
reg_type = get_list('identifier_type_id', 'Select registration type',
                    'Organisational unit ID - external')

org_units = get_org_units()


class RegistrationSearchForm(forms.Form):
    """Search registry form."""

    person_type = forms.ChoiceField(
        choices=person_type_list,
        initial='0',
        required=True,
        widget=forms.Select(
            attrs={'class': 'form-control',
                   'id': 'person_type',
                   'data-parsley-required': 'true'}))

    search_name = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': _('Search . . .'),
               'class': 'form-control',
               'id': 'search_name',
               'data-parsley-group': 'primary',
               'data-parsley-required': 'true'}))

    search_criteria = forms.ChoiceField(
        choices=psearch_criteria_list,
        initial='0',
        required=True,
        widget=forms.Select(
            attrs={'class': 'form-control',
                   'id': 'search_criteria',
                   'data-parsley-required': 'true'}))
    person_deceased = forms.CharField(
        required=False,
        widget=forms.CheckboxInput(
            attrs={'id': 'person_deceased'}))


class RadioCustomRenderer(RadioFieldRenderer):
    """Custom radio button renderer class."""

    def render(self):
        """Renderer override method."""
        return mark_safe(u'%s' % u'\n'.join(
            [u'%s' % force_unicode(w) for w in self]))


class RegistrationForm(forms.Form):
    """Registration for class."""

    def __init__(self, user, *args, **kwargs):
        """Override method especially for dynamic lookup data."""
        self.user = user
        super(RegistrationForm, self).__init__(*args, **kwargs)
        org_units_list = get_specific_orgs(self.user.reg_person_id)
        chv_list = get_chvs(self.user.reg_person_id)
        if user.is_superuser:
            org_units_list = get_org_units_list('Please select Unit')
        org_unit_id = forms.ChoiceField(
            choices=org_units_list,
            initial='',
            widget=forms.Select(
                attrs={'class': 'form-control',
                       'id': 'org_unit_id'}))
        cbo_unit_id = forms.ChoiceField(
            choices=org_units_list,
            initial='',
            widget=forms.Select(
                attrs={'class': 'form-control',
                       'id': 'cbo_unit_id'}))
        chv_unit_id = forms.ChoiceField(
            choices=chv_list,
            initial='',
            widget=forms.Select(
                attrs={'class': 'form-control',
                       'id': 'chv_unit_id'}))
        self.fields['org_unit_id'] = org_unit_id
        self.fields['cbo_unit_id'] = cbo_unit_id
        self.fields['chv_unit_id'] = chv_unit_id
        self.chvs = chv_list

        # All working in selections need to be tied to currently logged in user
        user_geos = get_user_geos(self.user)
        print user_geos
        county_filter = [] if user.is_superuser else user_geos['counties']
        scounty_filter = [] if user.is_superuser else user_geos['sub_counties']
        ward_filter = [] if user.is_superuser else user_geos['wards']
        county_list = get_geo_list(all_list, 'GPRV', user_filter=county_filter)
        sub_county_list = get_geo_list(
            all_list, 'GDIS', user_filter=scounty_filter)
        ward_list = get_geo_list(all_list, 'GWRD', user_filter=ward_filter)

        working_in_county = forms.MultipleChoiceField(
            choices=county_list,
            initial='',
            widget=forms.SelectMultiple(
                attrs={'class': 'form-control',
                       'id': 'working_in_county'}))
        self.fields['working_in_county'] = working_in_county

        working_in_subcounty = forms.MultipleChoiceField(
            choices=sub_county_list,
            initial='',
            widget=forms.SelectMultiple(
                attrs={'class': 'form-control',
                       'id': 'working_in_subcounty',
                       'data-parsley-required': 'true'}))
        self.fields['working_in_subcounty'] = working_in_subcounty

        working_in_ward = forms.MultipleChoiceField(
            choices=ward_list, label=_('Select ward'),
            initial='',
            widget=forms.SelectMultiple(
                attrs={'id': 'working_in_ward',
                       'class': 'form-control'}))
        self.fields['working_in_ward'] = working_in_ward

    tribes = get_list('tribe_category_id', 'Please Select')
    religions = get_list('religion_type_id', 'Please Select')

    county_list_wb = get_geo_list(all_list, 'GPRV', True)
    sub_county_list_wb = get_geo_list(all_list, 'GDIS', True)
    ward_list_wb = get_geo_list(all_list, 'GWRD', True)

    REGION_CHOICES = ((0, 'National'), (1, 'County'), (2, 'Sub County'))

    working_in_region = forms.ChoiceField(
        choices=REGION_CHOICES,
        widget=forms.RadioSelect(
            renderer=RadioCustomRenderer,
            attrs={'id': 'working_in_region',
                   'data-parsley-required': 'true',
                   'class': 'working_region',
                   'data-parsley-errors-container': "#type_error"}))

    person_type = forms.ChoiceField(
        choices=person_type_list,
        initial='0',
        widget=forms.Select(
            attrs={'class': 'form-control',
                   'autofocus': 'false',
                   'id': 'person_type',
                   'data-parsley-required': 'true'}))

    is_caregiver = forms.CharField(
        widget=forms.CheckboxInput(
            attrs={'autofocus': 'false'}))

    no_adult_caregiver = forms.CharField(
        widget=forms.CheckboxInput(
            attrs={'autofocus': 'false'}))

    child_services = forms.ChoiceField(
        choices=YESNO_CHOICES,
        widget=forms.RadioSelect(
            renderer=RadioCustomRenderer,
            attrs={'id': 'child_services',
                   'data-parsley-required': 'true',
                   'data-parsley-errors-container': "#services_error"}))

    child_ovc = forms.ChoiceField(
        choices=YESNO_CHOICES,
        widget=forms.RadioSelect(
            renderer=RadioCustomRenderer,
            attrs={'id': 'child_ovc',
                   'data-parsley-required': 'true',
                   'data-parsley-errors-container': "#child_ovc_error"}))

    unit_parent = forms.ChoiceField(
        choices=YESNO_CHOICES,
        widget=forms.RadioSelect(
            renderer=RadioCustomRenderer,
            attrs={'autofocus': 'false'}))

    unit_reg_assistant = forms.ChoiceField(
        choices=YESNO_CHOICES,
        widget=forms.RadioSelect(
            renderer=RadioCustomRenderer,
            attrs={'autofocus': 'false'}))

    title_type = forms.ChoiceField(
        choices=(),
        initial='',
        widget=forms.Select(
            attrs={'class': 'form-control',
                   'id': 'title_type'}))

    cadre_type = forms.ChoiceField(
        choices=cadre_type_list,
        initial='0',
        widget=forms.Select(
            attrs={'class': 'form-control',
                   'id': 'cadre_type'}))

    first_name = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': _('First Name'),
               'class': 'form-control',
               'id': 'first_name',
               'data-parsley-required': "true"}))
    other_names = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': _('Other Names'),
               'class': 'form-control',
               'id': 'other_names'}))
    surname = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': _('Surname'),
               'class': 'form-control',
               'id': 'surname',
               'data-parsley-required': "true"}))
    sex_id = forms.ChoiceField(
        choices=sex_id_list,
        widget=forms.Select(
            attrs={'placeholder': _('Sex'),
                   'class': 'form-control',
                   'id': 'sex_id',
                   'data-parsley-required': "true"}))
    des_phone_number = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': _('07XXXXXXXX'),
               'class': 'form-control',
               'id': 'des_phone_number',
               'data-parsley-maxlength': '10',
               'data-parsley-pattern': '/^[0-9\+]{1,}[0-9\-]{3,12}$/'}))
    other_phone_number = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': _('07XXXXXXXX'),
               'class': 'form-control',
               'id': 'other_phone_number',
               'data-parsley-maxlength': '10',
               'data-parsley-pattern': '/^[0-9\+]{1,}[0-9\-]{3,12}$/'}))
    email = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': _('Email Address'),
               'class': 'form-control',
               'id': 'email',
               'data-parsley-type': 'email'}))
    physical_address = forms.CharField(widget=forms.Textarea(
        attrs={'rows': '3', 'class': 'form-control'}))

    living_in_county = forms.ChoiceField(
        choices=county_list_wb,
        initial='',
        widget=forms.Select(
            attrs={'class': 'form-control',
                   'id': 'living_in_county'}))

    living_in_subcounty = forms.ChoiceField(
        choices=sub_county_list_wb,
        initial='',
        widget=forms.Select(
            attrs={'class': 'form-control',
                   'id': 'living_in_subcounty'}))

    living_in_ward = forms.ChoiceField(
        choices=ward_list_wb, label=_('Select ward'),
        initial='',
        widget=forms.Select(
            attrs={'id': 'living_in_ward',
                   'class': 'form-control'}))

    national_id = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': _('National ID'),
               'class': 'form-control',
               'id': 'national_id'}))
    staff_id = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': _('Staff Number'),
               'class': 'form-control',
               'id': 'staff_id'}))
    workforce_id = forms.IntegerField(widget=forms.TextInput(
        attrs={'placeholder': _('Workforce ID'),
               'class': 'form-control',
               'id': 'workforce_id'}))
    beneficiary_id = forms.IntegerField(widget=forms.TextInput(
        attrs={'placeholder': _('Beneficiary ID'),
               'class': 'form-control',
               'id': 'beneficiary_id'}))
    birth_reg_id = forms.IntegerField(widget=forms.TextInput(
        attrs={'placeholder': _('Birth Reg ID'),
               'class': 'form-control',
               'id': 'birth_reg_id'}))
    given_name = forms.IntegerField(widget=forms.TextInput(
        attrs={'placeholder': _('Given name'),
               'class': 'form-control'}))
    caregiver_id = forms.IntegerField(widget=forms.TextInput(
        attrs={'placeholder': _('Caregiver National ID/Name/CPIMS ID'),
               'class': 'form-control',
               'id': 'caregiver_id'}))
    caregiver_idno = forms.IntegerField(widget=forms.TextInput(
        attrs={'placeholder': _('National ID'),
               'class': 'form-control',
               'id': 'caregiver_idno'}))
    caregiver_tel = forms.IntegerField(widget=forms.TextInput(
        attrs={'placeholder': _('Cellphone Number'),
               'class': 'form-control',
               'id': 'caregiver_tel'}))
    relationship_type_id = forms.ChoiceField(
        choices=relationship_type_list,
        initial='0',
        widget=forms.Select(
            attrs={'class': 'form-control',
                   'id': 'relationship_type_id'}))
    date_of_birth = forms.DateField(widget=forms.DateInput(
        attrs={'placeholder': _('Date Of Birth'),
               'class': 'form-control',
               'id': 'date_of_birth',
               'data-parsley-required': 'true'
               }))
    date_of_death = forms.DateField(widget=forms.DateInput(
        attrs={'placeholder': _('Date Of Death'),
               'class': 'form-control',
               'id': 'date_of_death'}))

    caregiver_cpims_id = forms.CharField(widget=forms.HiddenInput(
        attrs={'id': 'caregiver_cpims_id'}))

    sibling_cpims_id = forms.CharField(widget=forms.HiddenInput(
        attrs={'id': 'sibling_cpims_id'}))

    is_cpims_sibling = forms.CharField(
        widget=forms.CheckboxInput(
            attrs={'autofocus': 'false'}))

    sibling_id = forms.IntegerField(widget=forms.TextInput(
        attrs={'placeholder': _('Birth Registration ID/Name/CPIMS ID'),
               'class': 'form-control',
               'id': 'cpims_child_id'}))

    sibling_firstname = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': _('First name'),
               'class': 'form-control'}))

    sibling_surname = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': _('Surname'),
               'class': 'form-control'}))

    sibling_othernames = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': _('Other names'),
               'class': 'form-control'}))

    sibling_dob = forms.DateField(widget=forms.DateInput(
        attrs={'placeholder': _('Sibling Date Of Birth'),
               'class': 'form-control',
               'id': 'sibling_dob'}))

    sibling_gender = forms.ChoiceField(
        choices=sex_id_list,
        widget=forms.Select(
            attrs={'class': 'form-control',
                   'id': 'sibling_gender_id'}))

    sibling_class = forms.ChoiceField(
        choices=classes_list,
        widget=forms.Select(
            attrs={'class': 'form-control',
                   'id': 'sibling_class_id'}))

    sibling_remark = forms.CharField(widget=forms.Textarea(
        attrs={'rows': '3', 'class': 'form-control'}))

    audit_workforce = forms.IntegerField(widget=forms.TextInput(
        attrs={'placeholder': _('Workforce ID / Name'),
               'class': 'form-control',
               'data-parsley-required': 'true',
               'id': 'audit_workforce_id'}))

    workforce_id = forms.CharField(widget=forms.HiddenInput(
        attrs={'id': 'workforce_id'}))

    audit_date = forms.DateField(widget=forms.DateInput(
        attrs={'class': 'form-control',
               'data-parsley-required': 'true',
               'id': 'audit_date'}))

    org_unit_primary = forms.CharField(widget=forms.HiddenInput(
        attrs={'id': 'org_unit_primary'}))

    person_id = forms.CharField(widget=forms.HiddenInput(
        attrs={'id': 'person_id'}))

    orgs_selected = forms.CharField(widget=forms.TextInput(
        attrs={'readonly': 'readonly',
               'data-parsley-required-message': (
                   'Please add atleast one Organisation unit to the grid'),
               'class': 'form-control'}))

    tribe = forms.ChoiceField(
        choices=tribes,
        initial='',
        widget=forms.Select(
            attrs={'class': 'form-control'}))

    religion = forms.ChoiceField(
        choices=religions,
        initial='',
        widget=forms.Select(
            attrs={'class': 'form-control'}))

    is_cpims_caregiver = forms.CharField(
        widget=forms.CheckboxInput(
            attrs={'autofocus': 'false'}))

    caregiver_firstname = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': _('First name'),
               'class': 'form-control'}))

    caregiver_surname = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': _('Surname'),
               'class': 'form-control'}))

    caregiver_othernames = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': _('Other names'),
               'class': 'form-control'}))

    caregiver_dob = forms.DateField(widget=forms.DateInput(
        attrs={'placeholder': _('Caregiver Date Of Birth'),
               'class': 'form-control',
               'id': 'caregiver_dob'}))

    caregiver_gender = forms.ChoiceField(
        choices=sex_id_list,
        widget=forms.Select(
            attrs={'class': 'form-control',
                   'id': 'caregiver_gender_id'}))

    country = forms.ChoiceField(
        choices=country_list,
        widget=forms.Select(
            attrs={'class': 'form-control',
                   'id': 'country_id'}))

    class Meta:
        """Override model class."""

        model = RegPerson


class LoginForm(forms.Form):
    """Login form class for the log in page."""

    username = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': _('Username'), 'class': 'form-control input-lg',
               'autofocus': 'false'}),
        error_messages={'required': 'Please enter your username.',
                        'invalid': 'Please enter a valid username.'})
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={'placeholder': _('Password'), 'class': 'form-control input-lg',
               'autofocus': 'false'}),
        error_messages={'required': 'Please enter your password.',
                        'invalid': 'Please enter a valid password.'},)

    def clean_username(self):
        """Method to clean username."""
        username = self.cleaned_data['username']
        if not username:
            raise forms.ValidationError("Please enter your username.")
        return username

    def clean_password(self):
        """Method to clean password."""
        password = self.cleaned_data['password']
        if not password:
            raise forms.ValidationError("Please enter your password.")
        return password


class NewUser(StrictSetPasswordForm):
    """Class for new user creation pages from existing persons."""

    person_id = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': _('Person ID'),
               'class': 'form-control',
               'id': 'person_id',
               'autofocus': 'false',
               'type': 'hidden',
               'data-parsley-required': "true"}))

    username = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': _('Username'),
               'class': 'form-control',
               'id': 'username',
               'autofocus': 'false',
               'data-parsley-required': "true"}))
    password1 = forms.CharField(widget=forms.PasswordInput(
        attrs={'placeholder': _('Password'),
               'class': 'form-control',
               'id': 'password1',
               'data-parsley-required': "true"}))
    password2 = forms.CharField(widget=forms.PasswordInput(
        attrs={'placeholder': _('Password(Again)'),
               'class': 'form-control',
               'id': 'password2',
               'data-parsley-required': "true"}))


class FormRegistry(forms.Form):
    """Org units registry search."""

    reg_list = get_list('organisation_type_id', 'All Types')
    org_category = forms.ChoiceField(
        choices=reg_list,
        initial='0',
        required=False,
        widget=forms.Select(
            attrs={'class': 'form-control'}))
    org_type = forms.ChoiceField(
        choices=(),
        initial='0',
        required=False,
        widget=forms.Select(
            attrs={'class': 'form-control'}))

    handle_ovc = forms.ChoiceField(
        choices=YESNO_CHOICES,
        widget=forms.RadioSelect(
            renderer=RadioCustomRenderer,
            attrs={'id': 'handle_ovc',
                   'data-parsley-required': 'true',
                   'data-parsley-group': 'primary1',
                   'data-parsley-errors-container': "#handle_ovc_error"}))
    org_unit_name = forms.CharField(
        required=False,
        widget=forms.TextInput(
            attrs={'placeholder': _('Organisation unit'),
                   'class': 'form-control',
                   'autofocus': 'false', 'data-parsley-group': 'primary'}))
    org_closed = forms.CharField(
        required=False,
        widget=forms.CheckboxInput(
            attrs={'autofocus': 'false'}))


class FormRegistryNew(forms.Form):
    """Class for handling all persons registry."""

    def __init__(self, user, *args, **kwargs):
        """Constructor for override especially on the fly data."""
        self.user = user
        super(FormRegistryNew, self).__init__(*args, **kwargs)
        org_units = get_specific_orgs(self.user.reg_person_id)
        if user.is_superuser:
            org_units = org_units_list
        parent_org_unit = forms.ChoiceField(
            choices=org_units,
            initial='',
            widget=forms.Select(
                attrs={'class': 'form-control',
                       'autofocus': 'false',
                       'data-parsley-group': 'primary1',
                       'data-parsley-required': 'true'}))
        self.fields['parent_org_unit'] = parent_org_unit

    org_unit_category = forms.ChoiceField(
        choices=reg_list,
        initial='0',
        widget=forms.Select(
            attrs={'class': 'form-control',
                   'autofocus': 'false',
                   'data-parsley-required': 'true',
                   'data-parsley-group': 'primary1'}))

    org_unit_type = forms.ChoiceField(
        choices=(('', 'Select sub-type'),),
        initial='0',
        widget=forms.Select(
            attrs={'class': 'form-control',
                   'autofocus': 'false',
                   'data-parsley-required': 'true',
                   'data-parsley-group': 'primary1'}))

    handle_ovc = forms.ChoiceField(
        choices=YESNO_CHOICES,
        widget=forms.RadioSelect(
            renderer=RadioCustomRenderer,
            attrs={'id': 'handle_ovc',
                   'data-parsley-required': 'true',
                   'data-parsley-group': 'primary1',
                   'data-parsley-errors-container': "#handle_ovc_error"}))

    org_reg_type = forms.ChoiceField(
        choices=reg_type,
        initial='0',
        widget=forms.Select(
            attrs={'class': 'form-control',
                   'data-parsley-group': 'primary1'}))
    org_unit_name = forms.CharField(
        widget=forms.TextInput(
            attrs={'placeholder': _('Unit name'),
                   'class': 'form-control',
                   'autofocus': 'false',
                   'data-parsley-checkunit': "true",
                   'data-parsley-required': "true",
                   'data-parsley-trigger': 'input',
                   'data-parsley-group': 'primary'}))
    reg_date = forms.CharField(
        required=False,
        widget=forms.TextInput(
            attrs={'placeholder': _('Select date'),
                   'class': 'form-control',
                   'data-parsley-notfuturedate': "dd-M-yy",
                   'id': 'datepicker',
                   'data-parsley-group': 'primary'}))
    legal_reg_number = forms.CharField(
        widget=forms.TextInput(
            attrs={'placeholder': _('Registration No.'),
                   'class': 'form-control',
                   'autofocus': 'false',
                   'data-parsley-group': 'primary1'}))
    county = forms.MultipleChoiceField(
        choices=county_list,
        label=_('Select County'),
        required=False,
        widget=forms.SelectMultiple(
            attrs={'rows': '6',
                   'data-parsley-multiple': 'multiple'}))
    sub_county = forms.MultipleChoiceField(
        choices=sub_county_list,
        label=_('Select sub-county'),
        required=False,
        widget=forms.SelectMultiple(
            attrs={'rows': '6',
                   'data-parsley-group': 'primary2',
                   'data-parsley-chkcounty': '#id_org_unit_type',
                   'data-parsley-validate-if-empty': "true",
                   'data-parsley-errors-container': "#county_error",
                   'data-parsley-multiple': 'multiple'}))
    ward = forms.MultipleChoiceField(
        choices=ward_list, label=_('Select ward'),
        required=False, widget=forms.SelectMultiple(
            attrs={'rows': '6', 'data-parsley-multiple': 'multiple'}))
    parent_org_units = forms.ChoiceField(
        choices=org_units,
        initial='',
        widget=forms.Select(
            attrs={'class': 'form-control',
                   'autofocus': 'false',
                   'data-parsley-group': 'primary1'}))
    close_date = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': _('Select date'),
               'class': 'form-control',
               'autofocus': 'false',
               'data-parsley-notfuturedate': "dd-M-yy",
               'id': 'editdate',
               'readonly': 'readonly'}))


class FormContact(forms.Form):
    """Contact form generator from items in database."""

    contacts = get_list('contact_detail_type_id')
    helper = FormHelper()
    helper.form_tag = False
    helper.label_class = 'control-label col-md-4 col-sm-4'
    helper.field_class = 'col-md-6 col-sm-6'
    helper.layout = Layout()

    def __init__(self, *args, **kwargs):
        """Override for Contact data given all values are from db."""
        txt_box = ['CPOA', 'CPHA']
        attrs = {'class': 'form-control'}
        super(FormContact, self).__init__(*args, **kwargs)
        for i, contact in enumerate(self.contacts):
            contact_key = contact[0]
            contact_name = contact[1]
            v_name, v_check = 'data-parsley-required', "false"
            if 'email' in contact_name.lower():
                v_name, v_check = 'data-parsley-type', "email"
            elif 'number' in contact_name.lower():
                v_name, v_check = 'data-parsley-type', "number"
            else:
                if 'data-parsley-type' in attrs:
                    del(attrs['data-parsley-type'])
                if 'data-parsley-min' in attrs:
                    del(attrs['data-parsley-min'])
                if 'data-parsley-max' in attrs:
                    del(attrs['data-parsley-max'])
            # validations params
            attrs[v_name] = v_check
            is_designate = 'designated' in contact_name.lower()
            is_physical = 'physical' in contact_name.lower()
            is_person = 'person' in contact_name.lower()
            if is_designate or is_physical or is_person:
                is_required = True
                attrs['data-parsley-required'] = "true"
                attrs['data-parsley-group'] = "primary3"
                # del(attrs['data-parsley-type'])
            else:
                is_required = False
                if 'data-parsley-required' in attrs:
                    del(attrs['data-parsley-required'])
                if 'latitude'in contact_name.lower():
                    attrs['data-parsley-type'] = "number"
                    attrs['data-parsley-min'] = "-4"
                    attrs['data-parsley-max'] = "4"
                elif 'longitude'in contact_name.lower():
                    attrs['data-parsley-type'] = "number"
                    attrs['data-parsley-min'] = "31"
                    attrs['data-parsley-max'] = "41"
                else:
                    if 'data-parsley-group' in attrs:
                        del(attrs['data-parsley-group'])
                    if 'data-parsley-min' in attrs:
                        del(attrs['data-parsley-min'])
                    if 'data-parsley-max' in attrs:
                        del(attrs['data-parsley-max'])
            tool_text = self.do_tooltips(contact_name, is_required)
            cont_name = contact_name + tool_text
            form_char = forms.CharField(label=cont_name,
                                        required=is_required,
                                        widget=forms.TextInput(
                                            attrs=attrs))
            attrs['rows'] = '3'
            form_text = forms.CharField(label=cont_name,
                                        required=is_required,
                                        widget=forms.Textarea(
                                            attrs=attrs))
            form_type = form_text if str(contact_key) in txt_box else form_char
            if contact_key != 'CPHD':
                self.fields['contact_%s' % contact_key] = form_type

    def do_tooltips(self, data, is_required):
        """Method for creating tooltips."""
        tool_req = '' if is_required else ' not'
        if data.lower() == 'latitude':
            data = 'Latitude (max +4 for North and min -4 for South)'
        if data.lower() == 'longitude':
            data = 'Longitude (min 31 for East and max 41 for West)'
        label = ('<span><a href="#" data-toggle="tooltip" title="%s is%s '
                 'mandatory."><i class="fa fa-info-circle fa-lg">'
                 '</i></a></span>') % (data, tool_req)
        return label

    def extra_contacts(self):
        """Method for extracting dynamically generated contact fields."""
        for name, value in self.cleaned_data.items():
            if name.startswith('contact'):
                field_name = name.replace('contact_', '')
                # field_label = self.fields[name].label
                yield (field_name, value)
