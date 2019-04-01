# -*- coding: utf-8 -*-
"""Common method for getting related list for dropdowns... e.t.c."""
import uuid
import datetime
import collections
import itertools
import jellyfish
import traceback
import operator
from dateutil import parser
from .models import SetupList, SetupGeography
from django.core.cache import cache
from django.core.exceptions import FieldError
from django.db.models import Q
from cpovc_registry.models import (
    RegPerson, RegPersonsGeo, RegPersonsOrgUnits, RegOrgUnit,
    RegOrgUnitGeography, RegPersonsTypes, RegPersonsExternalIds)
# Added
from cpovc_forms.models import OVCCaseCategory
from cpovc_main.models import SetupGeography, SetupList, SchoolList

organisation_id_prefix = 'U'
benficiary_id_prefix = 'B'
workforce_id_prefix = 'W'
form_id_prefix = 'F'
case_event_id_prefix = 'CE'


class Persons:
    id_int = None
    user_id = None
    workforce_id = None
    national_id = None
    first_name = ''
    other_names = ''
    surname = ''
    name = None
    sex_id = None
    sex = None
    date_of_birth = None
    date_of_death = None
    steps_ovc_number = None
    man_number = None
    ts_number = None
    sign_number = None
    roles = None
    org_units = None
    org_unit_name = None
    person_type = None
    person_type_id = None
    geo_location = None
    gdclsu_details = None
    contact = None
    registered_by_person_id = None
    direct_services = None
    

    def __init__(self, workforce_id, national_id, first_name,surname, other_names, sex_id, date_of_birth, steps_ovc_number,man_number,
                ts_number,sign_number,roles, org_units,primary_org_unit_name, person_type, gdclsu_details, contact,person_type_id, districts=None, 
                wards=None, communities=None,direct_services=None,edit_mode_hidden=None,workforce_type_change_date=None,parent_org_change_date=None,
                work_locations_change_date=None,date_of_death=None,org_data_hidden = None, primary_org_id=None, wards_string = None,
                org_units_string = None,communities_string = None):
        
        if workforce_id == fielddictionary.empty_workforce_id:
            self.user_id = 'N/A'
        else:
            self.user_id = workforce_id
        self.workforce_id = workforce_id
        self.national_id = national_id
        self.first_name = first_name
        self.surname = surname
        self.other_names = other_names
        if first_name and surname:
            self.name = first_name + ' ' + surname
        self.sex_id = sex_id
        self.date_of_birth = date_of_birth
        #self.date_of_death = date_of_death
        self.steps_ovc_number = steps_ovc_number
        self.man_number = man_number
        self.ts_number = ts_number
        self.sign_number = sign_number
        #self.registered_by_person_id = registered_by_person_id
        self.roles = roles
        self.org_units = org_units
        self.primary_org_id = primary_org_id
        self.primary_org_unit_name = primary_org_unit_name
        self.person_type = person_type
        #self.geo_location = geo_location
        self.gdclsu_details = gdclsu_details       
        self.contact = contact
        self.person_type_id = person_type_id
        self.wards_string = wards_string
        self.org_units_string = org_units_string
        self.communities_string = communities_string
        self.geo_location = {}
        self.geo_location = {'districts':districts,
                             'wards': wards,
                             'communities':communities}
        
        self.direct_services = direct_services
        self.edit_mode_hidden = edit_mode_hidden
        self.workforce_type_change_date=workforce_type_change_date
        self.parent_org_change_date=parent_org_change_date
        self.work_locations_change_date=work_locations_change_date
        self.date_of_death=date_of_death
        self.org_data_hidden = org_data_hidden
        _distrcits_wards = []
        _communities = None
        if wards:
            _distrcits_wards += wards
        if districts:
            _distrcits_wards += districts
            
        if _distrcits_wards:
            if self.geo_location['communities']:
                _communities = self.geo_location['communities']
            else:
                _communities = []
            self.locations_for_display = matches_for_display(_distrcits_wards, _communities)
        else:
            self.locations_for_display = []
        
        self.locations_unique_readable = []
        
        for loc in _distrcits_wards:
            self.locations_unique_readable.append(GeoLocation(loc).geo_name)
        
        if _communities:
            for comm in communities:
                self.locations_unique_readable.append(RegOrgUnit.objects.get(pk=comm).org_unit_name)
        
    def __unicode__(self):
        return '%s %s'% (self.first_name, self.surname)
    
    def sex(self):
        self.sex = list_provider.get_description_for_item_id(self.sex_id)
        #self.sex = list_provider.get_item_desc_for_order_and_category(self.sex_id, fielddictionary.sex)
        if not self.sex:
            return ''
        return self.sex[0]
    
    def get_locations_for_display(self):
        return self.locations_for_display

def translate_school(value):
    item_value = SchoolList.objects.get(school_id=value, is_void=False)
    return item_value.school_name

def translate_reverse_org(value):
    item_value = RegOrgUnit.objects.get(org_unit_name=value, is_void=False)
    return item_value.id
    
def translate_case(value):
    item_value = OVCCaseCategory.objects.get(case_category_id=value, is_void=False)
    return item_value.case_category

def translate_geo(value):
    item_value = SetupGeography.objects.get(area_id=value, is_void=False)
    return item_value.area_name

def translate(value):
    if value:
        item_value = SetupList.objects.filter(item_id=value, is_void=False)
        item_value = item_value[0]
        return item_value.item_description
    else:
        return value

def translate_reverse(value):
    if value:
        item_value = SetupList.objects.filter(item_description=value, is_void=False)
        item_value = item_value[0]
        return item_value.item_id
    else:
        return value

def get_description_for_item_id(item_id):
    return tuple([(l.item_description) for l in SetupList.objects.filter(item_id = item_id)])

def get_geo_list(default_txt=False):
    '''
     Get all area_id & area_name
    '''
    initial_list = {'': default_txt} if default_txt else {}
    all_list = collections.OrderedDict(initial_list)
    try:
        my_list = SetupGeography.objects.filter(
            is_void=False).order_by('area_name')
        for a_list in my_list:
            all_list[a_list.area_id] = a_list.area_name
    except Exception, e:
        error = 'Error getting list - %s' % (str(e))
        print error
        return ()
    else:
        return all_list.items

def get_vgeo_dict(area_id, default_txt=False):
    initial_list = {'': default_txt} if default_txt else {}
    all_list = collections.OrderedDict(initial_list)
    try:
        my_list = SetupGeography.objects.filter(area_id=area_id,
            is_void=False).order_by('area_name')
        for a_list in my_list:
            all_list[a_list.area_id] = a_list.area_name
    except Exception, e:
        error = 'Error getting list - %s' % (str(e))
        print error
        return ()
    else:
        return all_list.items

def get_vgeo_list(area_id):
    '''
    Get list general filtered by field_name
    '''
    try:
        queryset = SetupGeography.objects.filter(area_id=area_id, is_void=False).order_by('area_id')
        
    except Exception, e:
        error = 'Error getting whole list - %s' % (str(e))
        print error
        return None
    else:
        return queryset


def get_vorg_list(org_unit_id):
    '''
    Get list general filtered by field_name
    '''
    try:
        queryset = RegOrgUnit.objects.filter(
            id=org_unit_id, is_void=False).order_by('org_unit_name')
        # print 'OrgUnit Name: %s' %queryset.org_unit_name
    except Exception, e:
        error = 'Error getting whole list - %s' % (str(e))
        print error
        return None
    else:
        return queryset


def get_general_list(field_names=[], item_category=False):
    '''
    Get list general filtered by field_name
    '''
    try:
        queryset = SetupList.objects.filter(is_void=False).order_by(
            'the_order', 'id')
        if len(field_names) > 1:
            q_filter = Q()
            for field_name in field_names:
                q_filter |= Q(**{"field_name": field_name})
            queryset = queryset.filter(q_filter)
        else:
            queryset = queryset.filter(
                field_name=field_names[0]).order_by('the_order')
        if item_category:
            queryset = queryset.filter(
                item_category=item_category).order_by('the_order')
    except Exception, e:
        error = 'Error getting whole list - %s' % (str(e))
        print error
        return None
    else:
        return queryset


def get_list(field_name=[], default_txt=False, category=False):
    my_list = ()
    try:
        cat_id = '1' if category else '0'
        cache_key = 'set_up_list_%s_%s' % (field_name, cat_id)
        cache_list = cache.get(cache_key)
        if cache_list:
            v_list = cache_list
            print 'FROM Cache %s' % (cache_key)
        else:
            v_list = get_general_list([field_name], category)
            cache.set(cache_key, v_list, 300)
        my_list = v_list.values_list(
            'item_id', 'item_description').order_by('the_order')
        if default_txt:
            initial_list = ('', default_txt)
            final_list = [initial_list] + list(my_list)
            return final_list
    except Exception, e:
        error = 'Error getting list - %s' % (str(e))
        print error
        return my_list
    else:
        return my_list


def get_org_units_list(default_txt=False, org_types=[]):
    '''
     Get all org_unit_name + org_unit__id
    '''
    initial_list = {'': default_txt} if default_txt else {}
    all_list = collections.OrderedDict(initial_list)
    try:
        my_list = RegOrgUnit.objects.filter(
            id__gt=1, is_void=False).order_by('org_unit_name')
        for a_list in my_list:
            unit_names = '%s - %s' % (a_list.org_unit_id_vis,
                                      a_list.org_unit_name)
            unit_type = str(a_list.org_unit_type_id)
            if org_types:
                if unit_type in org_types:
                    all_list[a_list.id] = unit_names
            else:
                all_list[a_list.id] = unit_names
    except Exception, e:
        error = 'Error getting list - %s' % (str(e))
        print error
        return ()
    else:
        return all_list.items


def get_org_units_dict(default_txt=False):
    '''
     Get all org_unit_name + org_unit__id
    '''
    all_list = {}
    try:
        my_list = RegOrgUnit.objects.filter(
            is_void=False).order_by('org_unit_name')
        for a_list in my_list:
            org_name = '%s %s' % (a_list.org_unit_id_vis, a_list.org_unit_name)
            all_list[a_list.id] = org_name
    except Exception, e:
        error = 'Error getting list - %s' % (str(e))
        print error
        return ()
    else:
        return all_list


def get_dict(field_name=[], default_txt=False):
    '''
    Push the item_id and item_description into a tuple
    Instead of sorting after, ordered dict works since query
    results are already ordered from db
    '''
    # initial_list = {'': default_txt} if default_txt else {}
    # all_list = collections.OrderedDict(initial_list)
    # [{'item_id': u'TNRS', 'item_description': u'Residentia....'}
    dict_val = {}
    try:
        my_list = get_general_list(field_names=field_name)
        all_list = my_list.values('item_id', 'item_description')
        for value in all_list:
            item_id = value['item_id']
            item_details = value['item_description']
            dict_val[item_id] = item_details
    except Exception, e:
        error = 'Error getting list - %s' % (str(e))
        print error
        return {}
    else:
        return dict_val


def get_mapped(field_name=[], default_txt=False):
    '''
    Push the item_id and item_description into a tuple.
    Instead of sorting after, ordered dict works since query
    results are already ordered from db
    '''
    # initial_list = {'': default_txt} if default_txt else {}
    # all_list = collections.OrderedDict(initial_list)
    # [{'item_id': u'TNRS', 'item_description': u'Residentia....'}
    dict_val = {}
    try:
        my_list = get_general_list(field_names=field_name)
        all_list = my_list.values(
            'item_id', 'item_description', 'field_name')
        for value in all_list:
            item_id = value['item_id']
            item_details = value['item_description']
            item_field = value['field_name']
            items = {'name': item_details, 'id': item_field}
            dict_val[item_id] = items
    except Exception, e:
        error = 'Error getting list - %s' % (str(e))
        print error
        return {}
    else:
        return dict_val


def tokenize_search_string(search_string):
    if not search_string:
        return []
    return search_string.split()


def as_of_date_filter(queryset, as_of_date=None, include_died=True):
    """
    as_of_date: A date or not specified. If not specified, we assume we want
    current data (date delinked is null). If specified, when looking at
    date_delinked, date_of_death e.t.c we regard them as still linked, still
    alive e.t.c if the date delinked or date_of_death occurs after this
    parameter date.
    This function takes in any queryset and tries to use the as_of_date filter
    to carry out the above rule.
    By default we need to exclude the died, but if we have include died we have
    #show all the died. If we do not have include died BUT we have
    #as of date, we get all whose date of death came after the as_of_death.
    """
    if include_died:
        # do nothing - We have not filtered on dead or alive so everyone is
        # currently included
        pass
    else:
        # now basically DO NOT include died so we remove the died...unless the
        # as_of_date is provided then we only remove those whose date of
        # death is gt than
        if as_of_date:
            queryset = queryset.exclude(date_of_death__lt=as_of_date)
        else:
            queryset = queryset.exclude(date_of_death__isnull=False)

    if not as_of_date:
        try:
            queryset = queryset.filter(date_delinked__isnull=True)
        except FieldError:
            pass
    if as_of_date:
        try:
            queryset = queryset.exclude(date_delinked__lt=as_of_date)
        except FieldError:
            try:
                queryset = queryset.exclude(date_of_death__lt=as_of_date)
            except FieldError:
                pass

    return queryset


def order_by_relevence(wrapped_function):
    def _wrapper(*args, **kwargs):
        results = wrapped_function(*args, **kwargs)
        # we order the results by relevance
        search_string = kwargs['search_string']
        field_names = kwargs['field_names']
        diff_distances = []
        for result in results:
            # match against the concentenated fields
            field_values = [getattr(result, fname) for fname in field_names]
            field_values = itertools.ifilter(None, field_values)
            field_string = " ".join(field_values)
            # access the field names dynamically.
            diff_distance = jellyfish.jaro_distance(
                unicode(field_string.upper()),
                unicode(search_string.upper())
            )
            diff_distances.append((result, diff_distance),)
        sorted_distances = sorted(diff_distances, key=lambda x: -x[1])
        # Now return the actual sorted results not the tuples
        return [sorted_distance[0] for sorted_distance in sorted_distances]
    return _wrapper


def search_core_ids(regpersons_queryset, search_string, as_of_date=None):
    """takes a queryset of regpersons and a search string - returns a filtered
    queryset with filters acted upon core_ids"""
    core_id_fields = ['national_id', 'birth_reg_id', 'workforce_id',
                      'beneficiary_id']

    search_strings = tokenize_search_string(search_string)
    q_filter = Q()
    for search_string in search_strings:
        for field in core_id_fields:
            q_filter |= Q(**{"%s__icontains" % field: search_string})
    results = regpersons_queryset.filter(q_filter)

    results = as_of_date_filter(results, as_of_date=None)
    # redundant just for documentation
    return results


@order_by_relevence
def direct_field_search(queryset, field_names, search_string, as_of_date=None):
    """Takes a queryset and a list of field names that the search string can act
    on."""
    # Split the string in case of first name, surname e.t.c
    search_strings = tokenize_search_string(search_string)
    q_filter = Q()
    for search_string in search_strings:
        for field in field_names:
            q_filter |= Q(**{"%s__icontains" % field: search_string})
    results = queryset.filter(q_filter)

    # results = as_of_date_filter(results, as_of_date=None)
    # redundant just for documentation
    # filter already applied on regpersons
    return results


def search_geo_tags(regpersons_queryset, search_string, as_of_date=None):
    # geographical areas
    search_strings = tokenize_search_string(search_string)
    q_filter = Q()
    for search_string in search_strings:
        q_filter |= Q(**{"area_name__icontains": search_string})
    areas_matched = SetupGeography.objects.filter(q_filter)
    area_param = areas_matched.values_list("area_id")
    persons_geo = RegPersonsGeo.objects.filter(area_id__in=area_param)
    # persons_geo = as_of_date_filter(persons_geo, as_of_date=None)
    persons_param = persons_geo.values_list("person__id")
    matches = regpersons_queryset.filter(id__in=persons_param)

    return matches


def search_parent_orgs(regpersons_queryset, search_string, as_of_date=None):
    search_strings = tokenize_search_string(search_string)
    q_filter = Q()
    query_param = "org_unit_name__icontains"
    for search_string in search_strings:
        q_filter |= Q(**{query_param: search_string})
    parent_orgs_matched = RegOrgUnit.objects.filter(q_filter)
    orgs_param = parent_orgs_matched.values_list("id")
    parent_orgs_matches = RegPersonsOrgUnits.objects.filter(
        org_unit_id__in=orgs_param)
    p_param = parent_orgs_matches.values_list("person_id")
    parent_org_unit_match_persons = regpersons_queryset.filter(id__in=p_param)

    return parent_org_unit_match_persons


def filter_age(regpersons_queryset, age=None, as_of_date=None):
    # convert the age to a timedelta
    age_datetime = datetime.timedelta(365 * int(age))
    if as_of_date:
        required_year_of_birth = as_of_date - age_datetime
    else:
        required_year_of_birth = datetime.datetime.today() - age_datetime

    one_year_time_delta = datetime.timedelta(days=365)
    results = regpersons_queryset.filter(
        date_of_birth__range=[required_year_of_birth - one_year_time_delta,
                              required_year_of_birth + one_year_time_delta])

    return results


def person_type_filter(regpersons_queryset, passed_in_persons_types):
    """in_person_types: list of person types we want to search in (tbvc, tbgr,
       twvl, twne, twge), if not specified, search in all person types. if
       as_of_date provided, look at records where (date_delinked is null or
       date_delinked > as_of_date)
    """
    person_types = RegPersonsTypes.objects.filter(
        person_type_id__in=passed_in_persons_types)
    regpersons_queryset = regpersons_queryset.filter(
        id__in=person_types.values('person'))
    return regpersons_queryset


def rank_results(results_dict, required_fields, rank_order):
    """First pick out the required fields from the results dict."""
    # Choose the required items
    # Rank them and ensure no duplicates
    ranked_results = []
    for field in rank_order:
        if field in required_fields:
            try:
                field_results = results_dict[field]
                for person in field_results:
                    if person not in ranked_results:
                        ranked_results.append(person)
            except KeyError:
                pass
    return ranked_results

def load_wfc_from_id(wfc_pk,user=None,include_dead=False):
    print 'include_dead', include_dead
    if RegPerson.objects.filter(pk=wfc_pk,is_void=False).count() > 0:
        tmp_wfc = None
        if include_dead:
            tmp_wfc = RegPerson.objects.get(pk=wfc_pk,is_void=False)
        else:
            tmp_wfc = RegPerson.objects.get(pk=wfc_pk,is_void=False,date_of_death=None)
            
        if tmp_wfc:
            if tmp_wfc.workforce_id == '':
                tmp_wfc.workforce_id = 'N/A'
        roles = None
        org_units = []
        person_type = None
        geos = None
        wards=None
        districts = None
        communities = None
        contact = None 
        person_type_id = None
        org_unit_name = ''
        org_unit_id = ''

        if RegPersonsOrgUnits.objects.filter(person=tmp_wfc,date_delinked=None,is_void=False).count() > 0:
            try:
                tmp_org_unit = RegPersonsOrgUnits.objects.get(person=tmp_wfc,date_delinked=None,is_void=False)
                if tmp_org_unit:
                    #To come back here
                    org_unit_name = tmp_org_unit.org_unit.org_unit_name
                    org_unit_id = tmp_org_unit.org_unit.pk
            except:
                org_unit_name = None
                org_unit_id = None
            tmp_org_units = RegPersonsOrgUnits.objects.filter(person=tmp_wfc,is_void=False,date_delinked=None)
            if tmp_org_units:
                for org in tmp_org_units:                    
                    org_model = org.org_unit

                    """
                    ********** To add later ************  
                    tmp_yes_no = org.primary
                    yes_no_value = ''
                    if tmp_yes_no:                        
                        yes_no_value = 'Yes'
                    else:
                        yes_no_value = 'No'
                    wfc_user = None
                    has_reg_assisstant_role = "No"
                    if tmp_wfc:
                        if len(AppUser.objects.filter(reg_person=tmp_wfc))==1:
                            #print tmp_wfc.workforce_id,'Crashing workforce id'
                            #print tmp_wfc.first_name, 'first_name'
                            #print tmp_wfc.surname,'surname'
                            wfc_user = AppUser.objects.get(reg_person=tmp_wfc)
                            if wfc_user:
                                role_geos = get_user_role_geo_org(wfc_user)
                                for roles_geo in  role_geos:
                                    if roles_geo.org_unit:
                                        if roles_geo.org_unit.pk == org_model.pk and roles_geo.group.group_name=='Registration assistant':
                                            has_reg_assisstant_role="Yes"
                    """

                    org_unit = OrganisationUnit(
                                    org_id_int = org_model.pk,
                                    org_id = org_model.org_unit_id_vis,                                    
                                    org_name = org_model.org_unit_name
                                    #primary_org = yes_no_value,
                                    #hasRegAssistantRole = has_reg_assisstant_role
                                    )
                    
                    org_units.append(org_unit)
            
        if RegPersonsTypes.objects.filter(person=tmp_wfc,is_void=False,date_ended=None).count() > 0:
            person_type = RegPersonsTypes.objects.get(person=tmp_wfc,is_void=False,date_ended=None)
        person_type_desc=''
        if person_type:
            person_type_id = person_type.person_type_id
            wfc_type_tpl = list_provider.get_description_for_item_id(person_type.person_type_id)
            if(len(wfc_type_tpl) > 0):
                person_type_desc = wfc_type_tpl[0]
            
        #RegPersonsExternalIds
        """
        ********** To add later[Search by RegPersonsExternalIds] ************  
        man_id = ''
        ovc_id = ''
        ts_id = ''
        sing_id = ''
        if RegPersonsExternalIds.objects.filter(person=tmp_wfc,is_void=False).count() > 0:
            tmp_man_id = [(l.identifier) for l in RegPersonsExternalIds.objects.filter(person=tmp_wfc, identifier_type_id = fielddictionary.govt_man_number,is_void=False)]
            if(len(tmp_man_id) > 0):
                man_id = tmp_man_id[0]
                
            tmp_ovc_id = [(l.identifier) for l in RegPersonsExternalIds.objects.filter(person=tmp_wfc, identifier_type_id = fielddictionary.steps_ovc_caregiver,is_void=False)]
            if(len(tmp_ovc_id) > 0):
                ovc_id = tmp_ovc_id[0]
                
            tmp_ts_id = [(l.identifier) for l in RegPersonsExternalIds.objects.filter(person=tmp_wfc, identifier_type_id = fielddictionary.teacher_service_id,is_void=False)]
            if(len(tmp_ts_id) > 0):
                ts_id = tmp_ts_id[0]
                
            tmp_sign_id = [(l.identifier) for l in RegPersonsExternalIds.objects.filter(person=tmp_wfc, identifier_type_id = fielddictionary.police_sign_number,is_void=False)]
            if(len(tmp_sign_id) > 0):
                sing_id = tmp_sign_id[0]
                #sing_id = x[0]

        
        ********** To add later[Search by RegPersonsContact] ************  
        designated_phone = ''
        other_mobile_number = ''
        email_address = ''
        physical_address = ''
        if RegPersonsContact.objects.filter(person=tmp_wfc,is_void=False).count() > 0:
            designated_phone_tpl = [(l.contact_detail) for l in RegPersonsContact.objects.filter(person=tmp_wfc, contact_detail_type_id = fielddictionary.contact_designated_mobile_phone,is_void=False)]
            if(len(designated_phone_tpl) > 0):
                designated_phone = designated_phone_tpl[0]
                
            mobile_phone_tpl = [(l.contact_detail) for l in RegPersonsContact.objects.filter(person=tmp_wfc, contact_detail_type_id = fielddictionary.contact_mobile_phone,is_void=False)]
            if(len(mobile_phone_tpl) > 0):
                other_mobile_number = mobile_phone_tpl[0]
             
            email_address_tpl = [(l.contact_detail) for l in RegPersonsContact.objects.filter(person=tmp_wfc, contact_detail_type_id = fielddictionary.contact_email_address,is_void=False)]
            if(len(email_address_tpl) > 0):
                email_address = email_address_tpl[0]
                
            physical_address_tpl = [(l.contact_detail) for l in RegPersonsContact.objects.filter(person=tmp_wfc, contact_detail_type_id = fielddictionary.contact_physical_address,is_void=False)]
            if(len(physical_address_tpl) > 0):
                physical_address = physical_address_tpl[0]
                
        contact = Contact(designated_phone, other_mobile_number, email_address, physical_address)
        """

        geos = {}
        if RegPersonsGeo.objects.filter(person=tmp_wfc,is_void=False,date_delinked=None).count() > 0:
            m_wfc_geo = RegPersonsGeo.objects.filter(person=tmp_wfc,is_void=False,date_delinked=None)
            
            for geo in m_wfc_geo:
                areainfo = SetupGeography.objects.get(area_id=geo.area_id)
                if areainfo.area_type_id in geos:
                    geos[areainfo.area_type_id].append(areainfo.area_id)
                else:
                    geos[areainfo.area_type_id] = [areainfo.area_id]
        if geos and 'GDIS'.strip() in geos:
            districts = geos['GDIS'.strip()]
        if geos and 'GWRD'.strip() in geos:
            wards = geos['GWRD',strip()]
        
        """
        ***Not Required For Kenyan Model***
        communties = {}
        if RegPersonsGdclsu.objects.filter(person=tmp_wfc,is_void=False,date_delinked=None).count() > 0:
            communities = RegPersonsGdclsu.objects.filter(person=tmp_wfc,is_void=False,date_delinked=None).values_list('gdclsu_id', flat=True)
        """
        org_data_hidden = reconstruct_org_text(org_units)

        wfc = WorkforceMember(  
            workforce_id = tmp_wfc.workforce_id,
            national_id= tmp_wfc.national_id,
            first_name=tmp_wfc.first_name,
            surname=tmp_wfc.surname,
            other_names=tmp_wfc.other_names,
            sex_id=tmp_wfc.sex_id,
            date_of_birth=tmp_wfc.date_of_birth,
            date_of_death=tmp_wfc.date_of_death,
            steps_ovc_number=ovc_id,
            man_number=man_id,
            ts_number=ts_id,
            sign_number=sing_id,
            roles=None,
            org_units= org_units,
            org_unit_name=org_unit_name,
            person_type=person_type_desc, 
            gdclsu_details=None, 
            contact=contact,
            person_type_id=person_type_id,
            districts=districts,
            wards=wards,
            wards_string=get_obj_strings(wards,None,'ward'),
            org_units_string=get_obj_strings(org_units,org_unit_name,'org'),
            communities_string=get_obj_strings(communities,None,'community'),
            communities= communities,
            direct_services='',
            edit_mode_hidden='',
            workforce_type_change_date=None,
            parent_org_change_date=None,
            work_locations_change_date=None,
            org_data_hidden=org_data_hidden,
            org_unit_id = org_unit_id
                    )
        wfc.id_int = tmp_wfc.pk

        return wfc
    
    else:
        print 'Workforce with the ID passsed does not exists'
        #raise Exception('Workforce with the ID passsed does not exists')

def search_wfc_by_org_unit(tokens):
    #print tokens,'tokens'
    org_ids = None
    search_condition = []
    if tokens:
        #for term in tokens:
        #print term,'term'
        search_condition.append(Q(org_unit_name__icontains=tokens))

        orgs = RegOrgUnit.objects.filter(reduce(operator.or_, search_condition)).values_list('id', 'org_unit_name')
        #print orgs,'orgs'
        if orgs:
            idstosearch = []
            for id, unit_name in orgs:
                if id in idstosearch:
                    continue
                idstosearch.append(id)

            org_ids = RegPersonsOrgUnits.objects.filter(org_unit_id__in=idstosearch, is_void=False).values_list('org_unit_id', flat=True)

    return org_ids


def get_parent_area_ids(geoid, geoids=[]):
    geoids = [] + geoids
    children_ids = SetupGeography.objects.filter(parent_area_id=geoid).values_list('area_id', flat=True)
    if children_ids:
        for childid in children_ids:
            if childid in geoids:
                continue
            geoids.append(childid)
            get_parent_area_ids(childid, geoids)
    return geoids


def search_wfc_by_location(tokens):
    #Search By Living In
    loc_ids = None
    search_condition = []
    if tokens:
        #for term in tokens:
        search_condition.append(Q(area_name__icontains=tokens))

        geos = SetupGeography.objects.filter(reduce(operator.or_, search_condition)).values_list('area_id', 'area_name')
        if geos:
            idstosearch = []
            for geo_id, geo_name in geos:
                if geo_id in idstosearch:
                    continue
                idstosearch.append(geo_id)
                childrenids = get_parent_area_ids(geo_id)
                idstosearch = idstosearch + childrenids
            loc_ids = RegPersonsGeo.objects.filter(area_id__in=idstosearch).values_list('area_id', flat=True)
    return loc_ids

def search_wfcs(tokens, wfc_type,search_location=True, search_by_org_unit = False):
    result = set()
    q_list = []
    if tokens or wfc_type:
        try:
            if tokens:
                #for token in tokens:
                q_list.append(Q(first_name__icontains=tokens))
                q_list.append(Q(surname__icontains=tokens))
                q_list.append(Q(other_names__icontains=tokens))
                #q_list.append(Q(national_id__icontains=tokens))
            
            if wfc_type and tokens:
                tmp_result = RegPerson.objects.filter(reduce(operator.or_, q_list), regpersonstypes__person_type_id__icontains=wfc_type, regpersonstypes__date_ended=None, is_void=False,date_of_death=None)               
            elif wfc_type and not tokens:
                tmp_result = RegPerson.objects.filter(regpersonstypes__person_type_id__contains=wfc_type, regpersonstypes__date_ended=None,is_void=False,date_of_death=None)
            elif tokens and not wfc_type:
                tmp_result = RegPerson.objects.filter(reduce(operator.or_, q_list), regpersonstypes__date_ended=None,is_void=False,date_of_death=None)
            elif not wfc_type and not tokens:
                tmp_result = RegPerson.objects.filter(regpersonstypes__date_ended=None, is_void=False,date_of_death=None)
            
            #Add Person To Result
            for person in tmp_result:
                result.add(person)
            
            if search_location:
                loc_ids = search_wfc_by_location(tokens)
                if loc_ids:
                    locsstofetch = list(loc_ids)
                    
                    if locsstofetch:
                        if wfc_type:
                            persons_by_geo = RegPerson.objects.filter(regpersonstypes__person_type_id__icontains=wfc_type,
                                regpersonsgeo__area_id__in=locsstofetch,is_void=False,date_of_death=None)
                        else:
                            persons_by_geo = RegPerson.objects.filter(regpersonsgeo__area_id__in=locsstofetch, is_void=False,date_of_death=None)
                    if persons_by_geo:
                        for person_by_geo in persons_by_geo:
                            result.add(person_by_geo)
            
            if search_by_org_unit:
                org_unit_ids = search_wfc_by_org_unit(tokens)
                if org_unit_ids:
                    orgstofetch = list(org_unit_ids)
                    if orgstofetch:
                        if wfc_type:
                            persons_by_org_unit = RegPerson.objects.filter(
                                regpersonstypes__person_type_id__icontains=wfc_type,
                                regpersonsorgunits__org_unit_id__in=orgstofetch,
                                is_void=False, date_of_death=None)
                        else:
                            persons_by_org_unit = RegPerson.objects.filter(
                                regpersonsorgunits__org_unit_id__in=orgstofetch,
                                is_void=False, date_of_death=None)

                    if persons_by_org_unit:
                        for person_by_org_unit in persons_by_org_unit:
                            result.add(person_by_org_unit)

        except Exception as e:
            traceback.print_exc()
            raise Exception('workforce search failed - %s' % (str(e)))
    else:
        result = RegPerson.objects.filter(
            regpersonstypes__person_type_id__in=get_list(
                'person_type_id', 'All Types'),
            regpersonstypes__date_ended=None, is_void=False,
            date_of_death=None)
    return result



def get_persons_list(user, tokens, wfc_type, getJSON=False,
                     search_location=True,
                     search_wfc_by_org_unit=True):
    wfcs = []
    modelwfcs = search_wfcs(
        tokens=tokens, wfc_type=wfc_type,
        search_location=search_location,
        search_by_org_unit=search_wfc_by_org_unit)

    """
    for wfc in modelwfcs:
        try:
            wfc = load_wfc_from_id(wfc.pk,user)

            *** To check later*** [Deals with Role Allocation]
            if getJSON:
                wfc = wfc_json(wfc,user)
                wfcs.append(wfc)
            else:
                wfcs.append(wfc)

            wfcs.append(wfc)
        except Exception as e:
            traceback.print_exc()
            raise Exception('Error - Retrieving person(s) failed!')
    """

    wfcs.append(modelwfcs)

    return wfcs


def get_list_of_persons(search_string,
                        search_string_look_in=["names", "core_ids",
                                               "parent_orgs", "geo_tags"],
                        age=None, has_beneficiary_id=False,
                        has_workforce_id=False, as_of_date=None,
                        in_person_types=[], number_of_results=5,
                        include_died=True, sex=None, include_void=False,
                        search_criteria=None,
                        ):
    """
    search_string: The text the user has entered in the control. Used for
    searching among the following:
        Names

        NRC
        Birth Certificate
        Workforce ID
        Beneficiary ID
        Geographical tags

        Names of parent org units of the person
    search search_string_look_in: What field search looks in, One or more of:
        Core IDs
        Names
        Parent Org Units
    age: Match against people with +-1 year of specific age. If not specified
    do not use. If as of date provided, calculate age as of that date
        else calculate age on current date.
    sex: SMAL or SFEM - If not specified, do not filter by sex
    has_beneficiary_id: True or False or not specified - Whether we want the
    to search among persons with beneficiary ids, persons without
        beneficiary_ids or all persons regardless of whether or not they have
        the beneficiary_id
    has_work_force_id: True or False or not specified. Whether to search among
    persons with workforce ids, persons without workforce ids, or all
        persons regardless of whether or not they have a workforce id
    as_of_date: A date or not specified. If not specified, we assume we want
    current data (date delinked is null). If specified, when looking at
        date_delinked, date_of_death e.t.c we regard them as still linked,
        still alive e.t.c if the date delinked or date_of_death occurs after
        this parameter date.
    in_person_types: List of person types we want to search in (TBVC, TBGR,
        TWVL, TWNE, TWGE), if not specified, search in all person types. If
        as_of_date provided, look at records where (date_delinked is null or
        date_delinked > as_of_date)
    include_void: True or False. If unspecified we assume false. Whether to
    include records where tbl_reg_persons.void = true or not

    include_died: True or false. If unspecified we assume true. Whether to
    include persons who have died or not. Note if as_of_date provided and
    include_ died is false, look at records where (date_of_death is null)

    number_of_results: Limit to number of results to be returned. If not
    specified, assume unlimited.

    All the other filters come after that.
    """
    regpersons_queryset = as_of_date_filter(RegPerson.objects.all(),
                                            as_of_date, include_died)
    if age:
        regpersons_queryset = filter_age(regpersons_queryset, age, as_of_date)
    if in_person_types:
        regpersons_queryset = person_type_filter(regpersons_queryset,
                                                 in_person_types)
    regpersons_queryset = regpersons_queryset.filter(is_void=include_void)
    if sex:
        regpersons_queryset = regpersons_queryset.filter(sex_id__iexact=sex)
    if has_beneficiary_id:
        regpersons_queryset = regpersons_queryset.filter(
            beneficiary_id__isnull=False)
    if has_workforce_id:
        regpersons_queryset = regpersons_queryset.filter(
            workforce_id__isnull=False)

    field_names = ['first_name', 'other_names', 'surname']
    # Take care of criteria this - So useless
    name_results, core_id_results = {}, {}
    geo_tag_results, parent_orgs_results = {}, {}
    rank_order = ['names', 'core_ids', 'geo_tags', 'parent_orgs']
    if search_criteria == 'PSNM':
        name_results = direct_field_search(regpersons_queryset,
                                           field_names=field_names,
                                           search_string=search_string)
        '''
        core_id_results = search_external_ids(regpersons_queryset,
                                              search_string=search_string)
        '''
    elif search_criteria == 'PSRE':
        rank_order = ['geo_tags', 'parent_orgs', 'names', 'core_ids']
        geo_tag_results = search_geo_tags(regpersons_queryset, search_string)
    elif search_criteria == 'PSOG':
        rank_order = ['parent_orgs', 'names', 'core_ids', 'geo_tags']
        parent_orgs_results = search_parent_orgs(regpersons_queryset,
                                                 search_string)
    results_dict = {
        "names": name_results,
        "core_ids": core_id_results,
        "geo_tags": geo_tag_results,
        "parent_orgs": parent_orgs_results,
    }
    ranked_results = rank_results(results_dict, search_string_look_in,
                                  rank_order)
    return ranked_results[:number_of_results]


def search_external_ids(queryset, search_string, as_of_date=None):
    # External ids
    search_strings = tokenize_search_string(search_string)
    q_filter = Q()
    for search_string in search_strings:
        q_filter |= Q(**{"identifier__icontains": search_string})
    persons_matched = RegPersonsExternalIds.objects.filter(q_filter)
    person_param = persons_matched.values_list("person_id")
    matches = queryset.filter(id__in=person_param)

    return matches


def search_geo_org_tags(queryset, search_string, as_of_date=None):
    # geographical areas
    search_strings = tokenize_search_string(search_string)
    q_filter = Q()
    for search_string in search_strings:
        q_filter |= Q(**{"area_name__icontains": search_string})
    areas_matched = SetupGeography.objects.filter(q_filter)
    a_param = areas_matched.values_list("area_id")
    reg_org_units_geo = RegOrgUnitGeography.objects.filter(area_id__in=a_param)
    # reg_org_units_geo = as_of_date_filter(reg_org_units_geo, as_of_date=None)
    geo_param = reg_org_units_geo.values_list("org_unit__id")
    matches = queryset.filter(id__in=geo_param)

    return matches


def org_unit_type_filter(queryset, passed_in_org_types):
    for passed_in_org_type in passed_in_org_types:
        queryset = queryset.filter(org_unit_type_id=passed_in_org_type)
    return queryset


def include_closed_filter(queryset, as_of_date=None, include_closed=True):
    """include_closed: True or false. If unspecified, we assume true.
        whether to include org units which have closed or not. Not if
        as_of_date provided and include_closed is false, look at records
        where (date_closed is null or date_closed > as_of_date)"""
    if include_closed:
        pass
    else:
        if as_of_date:
            queryset = queryset.exclude(date_closed__lt=as_of_date)
        else:
            queryset = queryset.exclude(date_closed__isnull=False)
    '''
    if not as_of_date and not include_closed:
        try:
            queryset = queryset.filter(date_closed__isnull=False)
        except FieldError:
            pass
    '''
    if as_of_date:
        try:
            queryset = queryset.exclude(date_closed__lt=as_of_date)
        except FieldError:
            try:
                queryset = queryset.exclude(date_closed__lt=as_of_date)
            except FieldError:
                pass
    return queryset


def get_list_of_org_units(search_string, as_of_date=None, in_org_unit_types=[],
                          include_closed=True, include_void=False,
                          number_of_results=5,
                          search_string_look_in=['names', 'geo_tags']):
    """
    search_string: The text the user has entered in the control. Used for
    searching among the following:
        org_unit_name
        org_unit_id
        geographical_tags

    search_string_look_in: What field search looks in, One or more of:
        Names, org_id

    as_of_date: A date or not specified. If not specified, we assume we want
    current data (date delinked is null). If specified, when looking at
    date_delinked, date_of_death e.t.c we regard them as still linked, still
    alive e.t.c if the date delinked or date_of_death occurs after this
    parameter date.

    in_org_unit_types: List of org unit types we want to search in.
        If not specified, assume we want to search in all org unit
        types. Note if as_of_date is provided, look at records where
        (date_delinked is null or date_delinked > as_of_date)

    include_closed: True or false. If unspecified, we assume true.
        whether to include org units which have closed or not. Not if
        as_of_date provided and include_closed is false, look at records
        where (date_closed is null or date_closed > as_of_date)

    include_void: True or False. If unspecified we assume false. Whether to
    include records where tbl_reg_persons.void = true or not

    number_of_results: Limit to number of results to be returned. If not
    specified, assume unlimited.
    """
    queryset = include_closed_filter(RegOrgUnit.objects.all(), as_of_date,
                                     include_closed)
    if in_org_unit_types:
        # queryset = org_unit_type_filter(queryset, in_org_unit_types)
        queryset = queryset.filter(org_unit_type_id__in=in_org_unit_types)

    queryset = queryset.filter(is_void=include_void)
    # queryset = include_closed_filter(queryset, as_of_date, include_closed)

    field_names = ["org_unit_id_vis", "org_unit_name"]
    name_results = direct_field_search(queryset, field_names=field_names,
                                       search_string=search_string)

    geo_tag_results = search_geo_org_tags(queryset, search_string)

    results_dict = {
        "names": name_results,
        "geo_tags": geo_tag_results,
    }
    rank_order = ['names', 'geo_tags']
    ranked_results = rank_results(results_dict, search_string_look_in,
                                  rank_order)
    return ranked_results[:number_of_results]


def new_guid_32():
    return str(uuid.uuid1()).replace('-', '')


def workforce_id_generator(modelid):
    uniqueid = '%05d' % modelid
    checkdigit = calculate_luhn(str(uniqueid))
    return workforce_id_prefix + str(uniqueid) + str(checkdigit)


def beneficiary_id_generator(modelid):
    uniqueid = '%05d' % modelid
    checkdigit = calculate_luhn(str(uniqueid))
    return benficiary_id_prefix + str(uniqueid) + str(checkdigit)

def form_id_generator(modelid):
    uniqueid = '%05d' % modelid
    checkdigit = calculate_luhn(str(uniqueid))
    return form_id_prefix + str(uniqueid) + str(checkdigit)

def case_event_id_generator(modelid):
    uniqueid = '%05d' % modelid
    checkdigit = calculate_luhn(str(uniqueid))
    return case_event_id_prefix + str(uniqueid) + str(checkdigit)
    
def org_id_generator(modelid):
    uniqueid = '%05d' % modelid
    checkdigit = calculate_luhn(str(uniqueid))
    return organisation_id_prefix + str(uniqueid) + str(checkdigit)


def luhn_checksum(check_number):
    '''
    http://en.wikipedia.org/wiki/Luhn_algorithm
    '''
    def digits_of(n):
        return [int(d) for d in str(n)]
    digits = digits_of(check_number)
    odd_digits = digits[-1::-2]
    even_digits = digits[-2::-2]
    checksum = 0
    checksum += sum(odd_digits)
    for d in even_digits:
        checksum += sum(digits_of(d * 2))
    return checksum % 10


def is_luhn_valid(check_number):
    '''
    http://en.wikipedia.org/wiki/Luhn_algorithm
    '''
    return luhn_checksum(check_number) == 0


def calculate_luhn(partial_check_number):
    '''
    http://en.wikipedia.org/wiki/Luhn_algorithm
    '''
    check_digit = luhn_checksum(int(partial_check_number) * 10)
    return check_digit if check_digit == 0 else 10 - check_digit


def convert_date(d_string, fmt='%d-%b-%Y'):
    try:
        if isinstance(d_string, datetime.date):
            new_date = datetime.datetime.strptime(d_string, fmt)
        else:
            new_date = datetime.datetime.strptime(d_string, fmt)
    except Exception, e:
        error = 'Error converting date -%s' % (str(e))
        print error
        return d_string
    else:
        return new_date


def get_days_difference(d_event):
    '''
    get difference of provided date and today's day
    '''
    d_today = datetime.datetime.now()
    d_today = d_today.strftime("%Y-%m-%d")
    d_event = d_event.strftime("%Y-%m-%d")
    d_today = parser.parse(d_today)
    d_event = parser.parse(d_event)
    delta = d_today - d_event

    return delta.days