# -*- coding: utf-8 -*-
"""Registry views for CPIMS."""
import uuid
from datetime import datetime
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.utils import timezone
from django.shortcuts import get_object_or_404
from django.contrib import messages
from cpovc_main.functions import (
    get_list_of_org_units, get_dict, convert_date, get_list_of_persons)
from .forms import FormRegistry, FormRegistryNew, FormContact
from .models import RegOrgUnitGeography, RegPersonsAuditTrail
from .functions import (
    org_id_generator, save_contacts, save_external_ids, close_org_unit,
    save_geo_location, get_external_ids, get_geo_location, get_contacts,
    get_geo_selected, search_org_units, delete_org_unit, save_locations,
    extract_post_params, auto_suggest_person, merge_two_dicts,
    set_person_dead, delete_person, names_from_ids, remove_locations,
    save_person_extids, save_person_type, remove_person_type, save_sibling,
    save_audit_trail, create_geo_list, counties_from_aids, get_user_details,
    get_list_types, geos_from_aids, person_duplicate, copy_locations,
    unit_duplicate, get_temp, save_household, get_household, get_index_child,
    check_duplicate, search_person_ft)
from cpovc_auth.models import AppUser
from cpovc_registry.models import (
    RegOrgUnit, RegOrgUnitContact, RegPerson, RegPersonsOrgUnits,
    RegPersonsTypes, RegPersonsGuardians, RegPersonsGeo, RegPersonsExternalIds,
    RegPersonsSiblings)
from cpovc_registry.forms import (
    RegistrationForm, RegistrationSearchForm, NewUser)
from cpovc_main.functions import (
    workforce_id_generator, beneficiary_id_generator, get_org_units_dict)
from cpovc_main.models import SetupGeography
from cpovc_auth.decorators import is_allowed_groups

from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_control

from cpovc_main.country import COUNTRIES
from cpovc_ovc.models import OVCRegistration
from cpovc_ovc.functions import get_ovcdetails
from cpovc_ovc.views import ovc_register
from cpovc_forms.views import new_case_record_sheet


now = timezone.now()


@login_required(login_url='/')
@is_allowed_groups(['RGM', 'RGU', 'DSU', 'STD'])
def home(request):
    """Search page for Organisation Unit / Default page."""
    try:
        orgs = get_list_types()
        if request.method == 'POST':
            form = FormRegistry(data=request.POST)
            search_string = request.POST.get('org_unit_name')
            org_type = request.POST.get('org_type')
            org_category = request.POST.get('org_category')
            org_closed = request.POST.get('org_closed')

            closed_org = True if org_closed == 'on' else False
            unit_type = [org_type] if org_type else []
            if org_category and not org_type:
                this_orgs = orgs[org_category]
                unit_type = []
                for org in this_orgs:
                    unit_type.append(org.split(',', 1)[0])
            if search_string:
                results = get_list_of_org_units(
                    search_string=search_string,
                    include_closed=closed_org,
                    in_org_unit_types=unit_type,
                    number_of_results=50)
            else:
                results = search_org_units(unit_type, closed_org)
            items = 'result' if len(results) == 1 else 'results'
            ids = []
            for result in results:
                ids.append(result.id)
            geo_names = names_from_ids(ids)
            msg_text = 'for %s' % (search_string) if search_string else ''
            message = "Search %s returned %d %s" % (msg_text,
                                                    len(results),
                                                    items)
            check_fields = ['org_unit_type_id', 'committee_unit_type_id',
                            'adoption_unit_type_id', 'si_unit_type_id',
                            'cci_unit_type_id', 'ngo_unit_type_id',
                            'government_unit_type_id']
            val = get_dict(field_name=check_fields)
            # All existing org units
            org_units_dict = get_org_units_dict()
            vals = merge_two_dicts(val, org_units_dict)
            return render(request, 'registry/org_units_index.html',
                          {'form': form, 'results': results,
                           'geos': geo_names, 'orgs': orgs,
                           'org_category': org_type,
                           'message': message, 'vals': vals})
        form = FormRegistry()
        query = request.GET.get('q')
        if query:
            results = auto_suggest_person(request, query)
            return JsonResponse(results, content_type='application/json',
                                safe=False)
        return render(request, 'registry/org_units_index.html',
                      {'form': form, 'orgs': orgs})
    except Exception, e:
        print str(e)
        raise e


@login_required
@is_allowed_groups(['RGM', 'RGU', 'DSU'])
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def register_new(request):
    """Create page for New Organisation Unit."""
    try:
        if request.method == 'POST':
            form = FormRegistry(data=request.POST)
            cform = FormContact(data=request.POST)
            # print request.POST
            org_unit_type = request.POST.get('org_unit_type')
            org_unit_name = request.POST.get('org_unit_name')
            handle_ovc = request.POST.get('handle_ovc')
            reg_date = request.POST.get('reg_date')
            if str(reg_date):
                reg_date = convert_date(reg_date)
            else:
                reg_date = None
            handles_ovc = True if handle_ovc == 'AYES' else False
            county = request.POST.getlist('county')
            sub_county = request.POST.getlist('sub_county')
            ward = request.POST.getlist('ward')
            parent_org_unit = request.POST.get('parent_org_unit')
            if not parent_org_unit:
                parent_org_unit = None
            org_reg_type = request.POST.get('org_reg_type')
            legal_reg_number = request.POST.get('legal_reg_number')
            org_new = RegOrgUnit(org_unit_id_vis='NXXXXXX',
                                 org_unit_name=org_unit_name.upper(),
                                 org_unit_type_id=org_unit_type,
                                 date_operational=reg_date,
                                 parent_org_unit_id=parent_org_unit,
                                 created_by_id=request.user.id,
                                 handle_ovc=handles_ovc,
                                 is_void=False)
            org_new.save()
            org_unit_id = org_new.pk
            org_unit_id_vis = org_id_generator(org_unit_id)
            org_new.org_unit_id_vis = org_unit_id_vis
            org_new.save(update_fields=["org_unit_id_vis"])
            msg = 'Organisation Unit (%s) save success.' % (org_unit_name)
            messages.info(request, msg)
            # Save external ids
            if org_reg_type:
                save_external_ids(org_reg_type, legal_reg_number, org_unit_id)
            # Save geo units
            geo_locs = ward + sub_county
            if not geo_locs and county:
                geo_locs = geos_from_aids(county, area_type='GDIS')
            save_geo_location(geo_locs, org_unit_id)
            # Save contacts
            if cform.is_valid():
                for (form_id, form_value) in cform.extra_contacts():
                    if form_value:
                        save_contacts(form_id, form_value, org_unit_id)
            # Perform audit trail for new org unit
            if org_new:
                params = {}
                params['transaction_type_id'] = 'REGU'
                params['interface_id'] = 'INTW'
                params['org_unit_id'] = org_unit_id
                save_audit_trail(request, params, 'Unit')
            return HttpResponseRedirect(reverse(home))
        form = FormRegistryNew(request.user)
        cform = FormContact()
        orgs = get_list_types()
        return render(request, 'registry/org_units_new.html',
                      {'form': form, 'cform': cform, 'orgs': orgs})
    except Exception, e:
        raise e


@login_required
@is_allowed_groups(['RGM', 'RGU', 'DSU'])
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def register_edit(request, org_id):
    """Edit page for Organisation Unit with id - org_id."""
    resp = ''
    try:
        units = RegOrgUnit.objects.get(pk=org_id, is_void=False)
        unit_parent = units.parent_org_unit_id
        all_units = RegOrgUnit.objects.filter(is_void=False)
        units_html = '<option value="">Select Org unit</option>'
        for my_unit in all_units:
            u_id = my_unit.id
            u_safe_name = my_unit.org_unit_name.replace("'", "\\'")
            u_name = '%s %s' % (my_unit.org_unit_id_vis, u_safe_name)
            sel_txt = 'selected' if u_id == unit_parent else ''
            units_html += '<option value="%s" %s>%s</option>' % (
                u_id, sel_txt, u_name)
        name = units.org_unit_name
        # Geo location ids
        if units.date_closed:
            closed_msg = ("Closed Organisation unit (%s) is "
                          "not editable." % (name))
            messages.error(request, closed_msg)
            return HttpResponseRedirect(reverse(home))
        area_ids = get_geo_location(org_id)
        area_list = []
        for area_id in area_ids:
            area_list.append(area_id['area_id'])
        county_list = counties_from_aids(area_list)
        if request.method == 'POST':
            form = FormRegistry(data=request.POST)
            cform = FormContact(data=request.POST)
            edit_type = int(request.POST.get('edit_org'))
            org_unit_name = request.POST.get('org_unit_name')
            org_unit_type = request.POST.get('org_unit_type')
            handle_ovc = request.POST.get('handle_ovc')
            reg_date = request.POST.get('reg_date')
            if str(reg_date):
                reg_date = convert_date(reg_date)
            else:
                reg_date = None
            handles_ovc = True if handle_ovc == 'AYES' else False
            county = request.POST.getlist('county')
            sub_county = request.POST.getlist('sub_county')
            ward = request.POST.getlist('ward')
            if edit_type == 1:
                # This is a normal edit
                print 'Normal edit'
                # Update changed fields in main table
                units.org_unit_name = org_unit_name.upper()
                units.org_unit_type_id = org_unit_type
                units.date_operational = reg_date
                units.handle_ovc = handles_ovc
                units.save(update_fields=["org_unit_name", "org_unit_type_id",
                                          "date_operational", "handle_ovc"])
                # Update registration details
                org_reg_type = request.POST.get('org_reg_type')
                reg_number = request.POST.get('legal_reg_number')
                if org_reg_type:
                    save_external_ids(org_reg_type, reg_number, org_id)
                # Update Geo locations
                geo_locs = ward + sub_county
                if not geo_locs and county:
                    geo_locs = geos_from_aids(county, area_type='GDIS')
                save_geo_location(geo_locs, org_id, area_list)
                # Update contacts
                if cform.is_valid():
                    for (form_id, form_value) in cform.extra_contacts():
                        if form_value:
                            save_contacts(form_id, form_value, org_id)
            elif edit_type == 2:
                # This is a close with date provided
                close_date = request.POST.get('close_date')
                if close_date:
                    close_date = convert_date(close_date)
                    close_org_unit(close_date, org_id)
                resp = 'Closed with given date - %s' % (close_date)
            else:
                # This is a close without date - use today
                # Check first that is no a parent to any unit
                parent_count = RegOrgUnit.objects.filter(
                    parent_org_unit_id=org_id, is_void=False).count()
                if parent_count == 0:
                    delete_org_unit(org_id)
                    resp = 'Deleted due to error / duplicate'
                else:
                    resp = ('This unit can not be deleted as it is a parent '
                            'to other sub-units.')
            # Perform audit trail for this edit transaction
            if edit_type:
                params = {}
                params['transaction_type_id'] = 'UPDU'
                params['interface_id'] = 'INTW'
                params['org_unit_id'] = org_id
                save_audit_trail(request, params, 'Unit')
            msg = 'Organisation Unit (%s) edit success.' % (org_unit_name)
            msg += '\n%s' % (resp)
            if not edit_type:
                msg = 'Edit cancelled'
            messages.info(request, msg)
            return HttpResponseRedirect(reverse(home))
        # f = ContactForm(request.POST, initial=data)
        # f.has_changed()
        date_op, date_closed = None, None
        if units.date_operational:
            the_date = convert_date(units.date_operational, '%Y-%m-%d')
            date_op = the_date.strftime('%d-%b-%Y')
        if units.date_closed:
            close_date = convert_date(units.date_closed, '%Y-%m-%d')
            date_closed = close_date.strftime('%d-%b-%Y')
        unit_type = units.org_unit_type_id
        parent_unit = units.parent_org_unit_id
        handles_ovc = units.handle_ovc
        handle_ovc = 'AYES' if handles_ovc else 'ANNO'
        # External ids
        ext_ids = get_external_ids(org_id)
        external = {}
        if ext_ids:
            reg_type = ext_ids[0]['identifier_type_id']
            reg_number = ext_ids[0]['identifier_value']
            external['org_reg_type'] = reg_type
            external['legal_reg_number'] = reg_number
        orgs = get_list_types()
        org_cat = None
        for org in orgs:
            org_vals = orgs[org]
            for org_val in org_vals:
                if unit_type and org_val.startswith(unit_type):
                    org_cat = org
        # Final data
        data = {'org_unit_name': name, 'org_unit_type': unit_type,
                'reg_date': date_op, 'sub_county': area_list,
                'ward': area_list, 'close_date': date_closed,
                'parent_org_unit': parent_unit, 'county': county_list,
                'org_unit_category': org_cat, 'handle_ovc': handle_ovc}
        data_dict = merge_two_dicts(external, data)
        form = FormRegistryNew(request.user, data_dict)
        # Get contact details
        contacts = get_contacts(org_id)
        cform = FormContact(contacts)
        return render(request,
                      'registry/org_units_edit.html',
                      {'form': form, 'cform': cform, 'org_unit': units,
                       'org_units': all_units, 'units_html': units_html,
                       'orgs': orgs, 'unit_type': unit_type})
    except RegOrgUnit.DoesNotExist:
        form = FormRegistry()
        msg = 'Organisation Unit does not exist'
        messages.add_message(request, messages.ERROR, msg)
        return render(request, 'registry/org_units_index.html',
                      {'form': form})
    except Exception, e:
        form = FormRegistry()
        msg = 'Organisation Unit edit error - %s' % (str(e))
        print msg
        messages.add_message(request, messages.ERROR, msg)
        return render(request, 'registry/org_units_index.html',
                      {'form': form})


@login_required
@is_allowed_groups(['RGM', 'RGU', 'DSU', 'STD'])
def register_details(request, org_id):
    """
    Some default page for the home page / Dashboard.

    vals - All possible list_general used on this page
    """
    try:
        # All my filters
        check_fields = ['contact_detail_type_id', 'org_unit_type_id',
                        'identifier_type_id', 'government_unit_type_id',
                        'committee_unit_type_id', 'adoption_unit_type_id',
                        'si_unit_type_id', 'cci_unit_type_id',
                        'ngo_unit_type_id']
        db_vals = get_dict(field_name=check_fields)
        # All existing org units
        org_units_dict = get_org_units_dict()
        vals = merge_two_dicts(db_vals, org_units_dict)
        org_unit = RegOrgUnit.objects.get(pk=org_id)
        org_contact = RegOrgUnitContact.objects.filter(
            org_unit_id=org_id).order_by("-contact_detail_type_id")
        org_lat = None
        org_long = None
        for con_org in org_contact:
            con_org_type = con_org.contact_detail_type_id
            if con_org_type == "CPLT":
                org_lat = con_org.contact_detail
            if con_org_type == "CPLG":
                org_long = con_org.contact_detail
        if not org_lat and not org_long:
            org_map = {'lat': -1.290211, 'long': 36.812137}
            org_map['map'] = 'Coordinates not available - Showing head office'
        else:
            # lat: -1.290211, lng: 36.812137
            org_map = {'lat': org_lat, 'long': org_long}
            org_map['map'] = 'Coordinates (%s, %s)' % (org_lat, org_long)
        org_unit.maps = org_map
        org_unit.contacts = org_contact
        # Geo details
        inner_qs = RegOrgUnitGeography.objects.filter(
            org_unit_id=org_id).values('area_id')
        entries = SetupGeography.objects.filter(area_id__in=inner_qs)
        wards, sub_counties = [], []
        for inner_q in entries:
            area_type = inner_q.area_type_id
            area_name = inner_q.area_name
            if area_type == 'GDIS':
                sub_counties.append(area_name)
            if area_type == 'GWRD':
                wards.append(area_name)
        show_wards = ' ,'.join(wards)
        show_county = ' ,'.join(sub_counties)
        # Get units where this is parent
        child_units = RegOrgUnit.objects.filter(
            is_void=False, parent_org_unit_id=org_id).order_by("org_unit_name")
        # External ids
        ext_ids = get_external_ids(org_id)
        if ext_ids:
            reg_type = ext_ids[0]['identifier_type_id']
            reg_number = ext_ids[0]['identifier_value']
            org_unit.registration_type = reg_type
            org_unit.registration_number = reg_number
        org_unit.sub_county = show_county
        org_unit.wards = show_wards
        return render(request, 'registry/org_units_details.html',
                      {'org_details': org_unit, 'vals': vals,
                       'child_units': child_units})
    except Exception, e:
        # raise e
        error = 'Org unit view error - %s' % (str(e))
        print error
        form = FormRegistry()
        msg = 'Organisation Unit does not exist - %s' % (str(e))
        messages.add_message(request, messages.ERROR, msg)
        return render(request, 'registry/org_units_index.html',
                      {'form': form})


@login_required
@is_allowed_groups(['RGM', 'RGU', 'DSU'])
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def new_person(request):
    """
    For creating all types of persons page.

    The persons include Government, NGO, volunteer, child and
    also caregivers.
    """
    operation_msg = None
    today = datetime.now()
    todate = today.strftime('%d-%b-%Y')
    try:
        my_params = get_temp(request)
        list_types = ['person_type_id', 'title_type_id', 'ngo_title_type_id']
        person_titles = get_list_types(list_type=list_types)
        unused_titles = {'TBVC': [], 'TBGR': [], 'TWVL': []}
        titles = merge_two_dicts(person_titles, unused_titles)
        # We handle POST request
        if request.method == 'POST':
            form = RegistrationForm(request.user, data=request.POST)
            # Check duplicate first
            person_uid = request.POST.get('person_uid')
            unique_id = check_duplicate(person_uid)
            if not unique_id:
                msg = 'Duplicate records identified.'
                messages.add_message(request, messages.ERROR, msg)
                return HttpResponseRedirect(reverse(persons_search))

            # Extract Caregivers, Org Units, Siblings
            attached_cg = extract_post_params(request)
            attached_ou = extract_post_params(request, 'ou_')
            attached_sb = extract_post_params(request, 'sb_')
            designation = request.POST.get('cadre_type')
            person_type = request.POST.get('person_type')
            first_name = request.POST.get('first_name').strip()
            other_names = request.POST.get('other_names').strip()
            surname = request.POST.get('surname').strip()
            sex_id = request.POST.get('sex_id')
            des_phone_number = request.POST.get('des_phone_number').strip()
            email = request.POST.get('email').strip()
            working_in_region = request.POST.get('working_in_region')
            working_in_county = request.POST.getlist('working_in_county')
            living_in = request.POST.get('living_in_subcounty')
            working_in = request.POST.getlist('working_in_subcounty')

            living_in_ward = request.POST.get('living_in_ward')
            working_in_ward = request.POST.getlist('working_in_ward')

            is_caregiver = request.POST.get('is_caregiver')

            national_id = request.POST.get('national_id')
            staff_id = request.POST.get('staff_id')
            birth_reg_id = request.POST.get('birth_reg_id')
            caregiver_id = request.POST.get('caregiver_id')

            date_of_birth = request.POST.get('date_of_birth')
            child_services = request.POST.get('child_services')

            other_phone_no = request.POST.get('other_phone_number').strip()
            physical_address = request.POST.get('physical_address').strip()

            tribe = request.POST.get('tribe')
            religion = request.POST.get('religion')
            country = request.POST.get('country')
            given_name = request.POST.get('given_name')

            child_ovc = request.POST.get('child_ovc')

            audit_date = request.POST.get('audit_date')
            audit_workforce_id = request.POST.get('workforce_id')

            dob = convert_date(date_of_birth) if date_of_birth else None

            if not email:
                email = None

            other_names = None if not other_names else other_names.upper()

            if not des_phone_number:
                des_phone_number = None
            if des_phone_number:
                des_phone_number = des_phone_number[-9:]

            person_types = [person_type]
            if 'TBGR' != person_type and is_caregiver:
                person_types.append('TBGR')
            # Get the type of children
            if 'TBVC' in person_types:
                designation = 'COVC' if child_ovc == 'AYES' else 'CGOC'
            # Capture RegPerson Model
            person = RegPerson(
                designation=designation,
                first_name=first_name.upper(),
                other_names=other_names,
                surname=surname.upper(), sex_id=sex_id,
                des_phone_number=des_phone_number,
                email=email, date_of_birth=dob,
                created_by_id=request.user.id,
                date_of_death=None, is_void=False)

            person.save()

            reg_person_pk = int(person.pk)
            now = timezone.now()

            # Save child as OVC
            if designation == 'COVC':
                reg_date = '1900-01-01'
                cbo_id = request.POST.get('cbo_unit_id')
                chv_id = request.POST.get('chv_unit_id')
                has_bcert = True if birth_reg_id else False
                ovc = OVCRegistration(
                    person_id=reg_person_pk, registration_date=reg_date,
                    has_bcert=has_bcert, is_disabled=False, is_void=False,
                    child_cbo_id=cbo_id, child_chv_id=chv_id,
                    exit_date=None, created_at=now)
                ovc.save()
                '''
                ovc, created = OVCRegistration.objects.get_or_create(
                    person_id=reg_person_pk,
                    defaults={"registration_date": reg_date, "has_bcert": has_bcert,
                              "is_disabled": False, "is_void": False,
                              "child_cbo_id": cbo_id, "child_chv_id": chv_id,
                              "exit_date": None, "created_at": now })
                '''
            # Capture RegPersonTypes Model
            if person_types:
                save_person_type(person_types, reg_person_pk)

            # Capture attached Organisation units
            if attached_ou:
                for unid in attached_ou:
                    org_unit_id = int(unid)
                    pri_unit = attached_ou[unid]['pri']
                    reg_ass = attached_ou[unid]['reg']
                    is_pri_unit = True if pri_unit == 'AYES' else False
                    is_reg_ass = True if reg_ass == 'AYES' else False
                    RegPersonsOrgUnits(
                        person=RegPerson.objects.get(pk=int(reg_person_pk)),
                        org_unit_id=org_unit_id,
                        date_linked=now,
                        date_delinked=None,
                        primary_unit=is_pri_unit,
                        reg_assistant=is_reg_ass,
                        is_void=False).save()
            # For OVC programming Caregiver and Volunteer add cbo_id
            reg_ovc = request.session.get('reg_ovc', False)
            ovc_cbos = ['TBGR', 'TWVL']
            ovc_type = str(person_type)
            if reg_ovc and ovc_type in ovc_cbos:
                cbo_id = request.POST.get('cbo_unit_id')
                person_id = int(reg_person_pk)
                RegPersonsOrgUnits(
                    person_id=person_id, org_unit_id=cbo_id,
                    date_linked=now, date_delinked=None, primary_unit=True,
                    reg_assistant=False, is_void=False).save()

            # Capture RegPersonsGeo Model
            area_ids = {}
            if living_in:
                area_ids[living_in] = 'GLTL'
            if living_in_ward:
                area_ids[living_in_ward] = 'GLTL'
            # Working in is a list so handle differently
            create_geo_list(area_ids, working_in)
            create_geo_list(area_ids, working_in_ward)

            # This is to handle Roles National/County/Sub-county
            region_role_id = int(working_in_region) if working_in_region else 0
            if region_role_id == 1:
                create_geo_list(area_ids, working_in_county)
                scids = geos_from_aids(working_in_county, area_type='GDIS')
                create_geo_list(area_ids, scids)
            elif region_role_id == 2:
                # Working in values are multi so handle differently
                create_geo_list(area_ids, working_in)
                create_geo_list(area_ids, working_in_ward)

            save_locations(area_ids, int(reg_person_pk))
            # Households data
            sib_ids, hh_members = [], []
            # Capture Siblings
            if attached_sb:
                pers_id = int(reg_person_pk)
                sib_ids = save_sibling(request, attached_sb, pers_id)

            # Capture RegPersonsGuardians Model
            if attached_cg:
                for ccid_id in attached_cg:
                    is_adult = attached_cg[ccid_id]['adult']
                    cgid = attached_cg[ccid_id]['cpid']
                    caregiver_id = int(cgid) if cgid.isnumeric() else 0
                    relationship = attached_cg[ccid_id]['ctype']
                    child_headed = True if is_adult == 'No' else False
                    RegPersonsGuardians(
                        child_person_id=reg_person_pk,
                        guardian_person_id=caregiver_id,
                        relationship=relationship,
                        date_linked=now,
                        date_delinked=None,
                        child_headed=child_headed,
                        is_void=False).save()
                    hh_members.append(caregiver_id)
            # Create house hold
            for sib_id in sib_ids:
                hh_members.append(sib_id)
            save_household(reg_person_pk, hh_members)
            # Capture RegPersonsExternalIds Model
            workforce_id, beneficiary_id = None, None
            identifier_types = {}

            if child_services:
                print 'Create WF', child_services
                if child_services == 'AYES':
                    workforce_id = workforce_id_generator(reg_person_pk)
            if 'TBGR' in person_types:
                    beneficiary_id = beneficiary_id_generator(reg_person_pk)
            if national_id:
                identifier_types['INTL'] = national_id
            if staff_id:
                identifier_types['IMAN'] = staff_id
            if workforce_id:
                identifier_types['IWKF'] = workforce_id
            if beneficiary_id:
                identifier_types['ISCG'] = beneficiary_id
            if birth_reg_id:
                identifier_types['ISOV'] = birth_reg_id
            if other_phone_no:
                identifier_types['CPHM'] = other_phone_no
            if physical_address:
                identifier_types['CPHA'] = physical_address
            if tribe and person_type == 'TBVC':
                identifier_types['ITRB'] = tribe
            if religion and person_type == 'TBVC':
                identifier_types['IREL'] = religion
            if country and person_type == 'TBVC':
                    identifier_types['ICOU'] = country
            if given_name and person_type == 'TBVC':
                    identifier_types['IGNM'] = given_name

            save_person_extids(identifier_types, int(reg_person_pk))

            # Perform audit trail here for all
            if person_type:
                params = {}
                params['transaction_type_id'] = 'REGS'
                params['interface_id'] = 'INTW'
                params['date_recorded_paper'] = audit_date
                params['paper_person_id'] = audit_workforce_id
                params['person_id'] = int(reg_person_pk)
                save_audit_trail(request, params)
            # Master Table update
            if unique_id:
                unique_id.person_type = person_type
                unique_id.person_id = int(reg_person_pk)
                unique_id.system_id = 'XXXX'
                unique_id.save(
                    update_fields=["person_type", "person_id", "system_id"])

            operation_msg = 'Person (%s) save success.' % first_name.upper()
            messages.add_message(request, messages.INFO, operation_msg)
            if child_ovc == 'AYES':
                ovc_url = reverse(ovc_register, kwargs={'id': reg_person_pk})
                return HttpResponseRedirect(ovc_url)
            elif 'TBVC' in person_types and child_ovc != 'AYES':
                csr_url = reverse(new_case_record_sheet,
                                  kwargs={'id': reg_person_pk})
                return HttpResponseRedirect(csr_url)
            return HttpResponseRedirect(
                '%s?id=%d' % (reverse(persons_search), reg_person_pk))
        else:
            # Not request.POST
            chvs = RegistrationForm(request.user)
            chvs = len(chvs.chvs)
            person_uid = uuid.uuid4
            form = RegistrationForm(request.user, data=my_params)
            return render(request, 'registry/person_new.html',
                          {'form': form, 'titles': titles, 'todate': todate,
                           'chvs': chvs, 'person_uid': person_uid},)

    except Exception, e:
        operation_msg = 'Error occured when saving person -  %s' % (str(e))
        print operation_msg
        form = RegistrationSearchForm()
        messages.add_message(request, messages.ERROR, operation_msg)
        return render(request, 'registry/person_search.html',
                      {'form': form},)


@login_required
@is_allowed_groups(['RGM', 'RGU', 'DSU', 'STD'])
def persons_search(request):
    """For persons search results page - put on data grid."""
    result = None
    person_type = None
    app_user = {}
    try:
        form = RegistrationSearchForm()
        check_fields = ['sex_id', 'cadre_type_id', 'person_type_id',
                        'relationship_type_id', 'identifier_type_id']
        vals = get_dict(field_name=check_fields)
        if request.method == 'POST':
            form = RegistrationSearchForm(data=request.POST)
            if form.is_valid():
                person_type = form.cleaned_data['person_type']
                search_string = form.cleaned_data['search_name'].strip()
                person_deceased = form.cleaned_data['person_deceased']
                search_criteria = form.cleaned_data['search_criteria']

                include_dead = True if person_deceased == 'True' else False
                type_of_person = [person_type] if person_type else []

                """
                resultsets = get_persons_list(
                    user=request.user, tokens=search_string,
                    wfc_type=wfc_type, search_location=search_location,
                    search_wfc_by_org_unit=search_wfc_by_org_unit)
                """
                if search_criteria == 'PSNM':
                    results = search_person_ft(request, search_string,
                                               person_type, include_dead)
                    # print res
                else:
                    results = get_list_of_persons(
                        search_string=search_string, number_of_results=100000,
                        in_person_types=type_of_person,
                        include_died=include_dead,
                        search_criteria=search_criteria)

                # Alternative for removing select query inside a for loop
                ids = []
                for result in results:
                    ids.append(result.pk)
                geo_names = names_from_ids(ids, registry='persons')
                org_names = names_from_ids(ids, registry='person_orgs')
                p_types = names_from_ids(ids, registry='person_types')

                print 'orgs', org_names

                # Person accounts
                accounts = AppUser.objects.all().values('id', 'reg_person_id')
                for account in accounts:
                    account_id = 'U%s' % (account['id'])
                    app_user[account['reg_person_id']] = account_id
                return render(request, 'registry/person_search.html',
                              {'form': form, 'results': results,
                               'vals': vals, 'person_type': person_type,
                               'app_user': app_user, 'geos': geo_names,
                               'orgs': org_names, 'person_types': p_types})
            else:
                print 'Not Good %s' % (form.errors)
        else:
            search_id = request.GET.get('id')
            if search_id and search_id.isdigit():
                sid = int(search_id)
                account_id, person_type = sid, ''
                results = RegPerson.objects.filter(id=sid)
                try:
                    accounts = AppUser.objects.get(reg_person_id=sid)
                    account_id = 'U%s' % (accounts.id)
                except Exception:
                    pass
                # person types
                person_types = RegPersonsTypes.objects.filter(
                    person_id=sid, is_void=False, date_ended=None)
                for ptype in person_types:
                    person_type = ptype.person_type_id
                # Other
                appuser = {sid: account_id}
                ids = [int(search_id)]
                geo_names = names_from_ids(ids, registry='persons')
                org_names = names_from_ids(ids, registry='person_orgs')
                p_types = names_from_ids(ids, registry='person_types')
                return render(request, 'registry/person_search.html',
                              {'form': form, 'results': results, 'vals': vals,
                               'app_user': appuser, 'person_type': person_type,
                               'geos': geo_names, 'orgs': org_names,
                               'person_types': p_types})
        return render(request, 'registry/person_search.html',
                      {'form': form, 'result': result,
                       'person_type': person_type})
    except Exception, e:
        raise e


@login_required
@is_allowed_groups(['RGM', 'RGU', 'DSU', 'STD'])
def view_person(request, id):
    """Page for viewing person details in full."""
    try:
        # All my filters
        check_fields = ['sex_id', 'cadre_type_id', 'person_type_id',
                        'relationship_type_id', 'identifier_type_id',
                        'tribe_category_id', 'religion_type_id',
                        'contact_detail_type_id']
        vals = get_dict(field_name=check_fields)
        person = RegPerson.objects.get(pk=id)
        person_types = RegPersonsTypes.objects.filter(
            person=person, is_void=False, date_ended=None)
        person_geos = RegPersonsGeo.objects.select_related().filter(
            person=person, is_void=False, date_delinked=None)
        person_orgs = RegPersonsOrgUnits.objects.select_related().filter(
            person=person, is_void=False, date_delinked=None)
        person_extids = RegPersonsExternalIds.objects.filter(
            person=person, is_void=False)
        person_appuser = get_user_details(person)
        # This will be used for children and Guardians ONLY
        guardians = RegPersonsGuardians.objects.select_related().filter(
            child_person=person, is_void=False, date_delinked=None)
        # Household - Introduced in V2
        child_index, members = get_household(person.id)
        print 'HH', child_index, members
        child_id = child_index if child_index else person.id
        siblings = RegPersonsSiblings.objects.select_related().filter(
            child_person_id=child_id, is_void=False,
            date_delinked=None).exclude(sibling_person_id=id)
        # Reverse relationship
        osiblings = RegPersonsSiblings.objects.select_related().filter(
            sibling_person_id=id, is_void=False,
            date_delinked=None)
        # .exclude(sibling_person_id=id)
        child_ids = [gd.child_person_id for gd in osiblings]
        oguardians = RegPersonsGuardians.objects.select_related().filter(
            child_person_id__in=child_ids, is_void=False, date_delinked=None)
        # HH members
        hhs = RegPerson.objects.filter(
            id__in=members, is_void=False).exclude(id=id)

        # Check if has an account
        workforce_id = None
        for pextids in person_extids:
            identity_id = pextids.identifier_type_id
            if identity_id == 'IWKF':
                workforce_id = pextids.identifier
            if identity_id == 'ICOU':
                country_id = pextids.identifier
                if country_id in COUNTRIES:
                    vals[country_id] = COUNTRIES[country_id]
        user_id, orgs, geos = None, None, None
        geo_county, geo_wards = None, None
        try:
            users = AppUser.objects.get(reg_person=person)
            user_id = users.pk
        except Exception:
            pass

        person.ptypes = person_types
        person.porgs = person_orgs
        person.pextids = person_extids
        all_ptypes, all_geos, all_orgs = [], [], []
        person_type_names = []
        all_geos_county, all_geos_wards = [], []
        pers_types, person_type_name = '', ''

        # This is for handling person types
        for person_type in person_types:
            type_id = person_type.person_type_id
            all_ptypes.append(type_id)
            if type_id in vals:
                person_type_names.append(vals[type_id])
        if all_ptypes:
            pers_types = ', '.join(all_ptypes)
        if person_type_names:
            person_type_name = ', '.join(person_type_names)

        for person_geo in person_geos:
            geo_name = person_geo.area.area_name
            geo_type = person_geo.area.area_type_id
            if geo_type == 'GPRV':
                all_geos_county.append(geo_name)
            elif geo_type == 'GDIS':
                all_geos.append(geo_name)
            else:
                all_geos_wards.append(geo_name)
        if all_geos:
            geos = ', '.join(all_geos)
        if all_geos_wards:
            geo_wards = ', '.join(all_geos_wards)
        if all_geos_county:
            geo_county = ', '.join(all_geos_county)

        for person_org in person_orgs:
            org_name = person_org.org_unit.org_unit_name
            all_orgs.append(org_name)
        if all_orgs:
            orgs = ', '.join(all_orgs)
        person.pgeos = geos
        person.geo_wards = geo_wards
        person.geo_county = geo_county
        person.porgs = orgs
        person.person_id = user_id
        person.person_types = pers_types
        person.person_type_name = person_type_name
        # Workforce ID
        person.workforce_id = workforce_id
        return render(request, 'registry/view_person.html',
                      {'person_details': person, 'vals': vals,
                       'appuser': person_appuser, 'guardians': guardians,
                       'siblings': siblings, 'osiblings': osiblings,
                       'oguardians': oguardians, 'hhs': hhs})
    except Exception, e:
        # raise e
        msg = 'Persons error - %s' % (str(e))
        messages.add_message(request, messages.ERROR, msg)
        return HttpResponseRedirect(reverse(persons_search))


@login_required
@is_allowed_groups(['RGM', 'RGU', 'DSU'])
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def edit_person(request, id):
    """
    For editing persons details.

    The page implements modal for creating / removing siblings and
    also caregivers. It has 3 sections edit mode -
    - Normal - editing all information
    - Marking person as dead
    - Marking as void for duplicates or mistakes
    """
    today = datetime.now()
    todate = today.strftime('%d-%b-%Y')
    try:
        ovc = get_ovcdetails(id)
        if request.method == 'POST':
            form = RegistrationForm(request.user, data=request.POST)
            designation = request.POST.get('cadre_type')
            person_type = request.POST.get('person_type')
            first_name = request.POST.get('first_name').strip()
            other_names = request.POST.get('other_names').strip()
            surname = request.POST.get('surname').strip()
            sex_id = request.POST.get('sex_id')
            des_phone_number = request.POST.get('des_phone_number').strip()
            email = request.POST.get('email').strip()
            living_in = request.POST.get('living_in_subcounty')
            working_in_region = request.POST.get('working_in_region')
            working_in_county = request.POST.getlist('working_in_county')
            working_in = request.POST.getlist('working_in_subcounty')

            living_in_ward = request.POST.get('living_in_ward')
            working_in_ward = request.POST.getlist('working_in_ward')

            is_caregiver = request.POST.get('is_caregiver')
            date_of_birth = request.POST.get('date_of_birth')
            child_services = request.POST.get('child_services')
            child_ovc = request.POST.get('child_ovc')

            # org_units = request.POST.getlist('org_unit_id')
            national_id = request.POST.get('national_id')
            staff_id = request.POST.get('staff_id')
            birth_reg_id = request.POST.get('birth_reg_id')
            date_of_birth = request.POST.get('date_of_birth')

            other_phone_no = request.POST.get('other_phone_number').strip()
            physical_address = request.POST.get('physical_address').strip()

            tribe = request.POST.get('tribe')
            religion = request.POST.get('religion')
            country = request.POST.get('country')
            given_name = request.POST.get('given_name')

            audit_date = request.POST.get('audit_date')
            audit_workforce_id = request.POST.get('workforce_id')
            edit_type = int(request.POST.get('edit_person'))
            dob = convert_date(date_of_birth) if str(date_of_birth) else None
            # Update RegPerson
            eperson_id = int(id)
            if edit_type == 1:
                person_types = [str(person_type)]
                if 'TBVC' in person_types:
                    designation = 'COVC' if child_ovc == 'AYES' else 'CGOC'
                if 'TBGR' != person_type and is_caregiver:
                    person_types.append('TBGR')
                phone_number = des_phone_number if des_phone_number else None
                operson = RegPerson.objects.get(pk=id)
                operson.designation = designation
                operson.first_name = first_name
                operson.other_names = other_names
                operson.surname = surname
                operson.sex_id = sex_id
                operson.des_phone_number = phone_number
                operson.email = email
                operson.date_of_birth = dob
                operson.save(update_fields=['first_name', 'other_names',
                                            'surname', 'sex_id', 'email',
                                            'des_phone_number', 'designation',
                                            'date_of_birth'])
                # Update OVC data
                if ovc:
                    cbo_id = request.POST.get('cbo_unit_id')
                    chv_id = request.POST.get('chv_unit_id')
                    ovc.child_cbo_id = cbo_id
                    ovc.child_chv_id = chv_id
                    ovc.save(update_fields=['child_cbo_id', 'child_chv_id'])
                else:
                    if designation == 'COVC':
                        reg_date = '1900-01-01'
                        cbo_id = request.POST.get('cbo_unit_id')
                        chv_id = request.POST.get('chv_unit_id')
                        has_bcert = True if birth_reg_id else False
                        ovc = OVCRegistration(
                            person_id=eperson_id, registration_date=reg_date,
                            has_bcert=has_bcert, is_disabled=False,
                            is_void=False, child_cbo_id=cbo_id,
                            child_chv_id=chv_id,
                            exit_date=None, created_at=now)
                        ovc.save()
                # Update Persons Geography
                person_geos_all = RegPersonsGeo.objects.filter(
                    person_id=eperson_id, is_void=False,
                    date_delinked=None).values(
                        'id', 'area_id', 'area_type')

                area_ids, area_ids_remove = {}, {}
                check_list, new_list = [], {}
                if living_in:
                    area_ids[int(living_in)] = 'GLTL'
                if living_in_ward:
                    area_ids[int(living_in_ward)] = 'GLTL'
                # This is to handle Roles National/County/Sub-county
                reg_role = int(working_in_region) if working_in_region else 0
                if reg_role == 1:
                    create_geo_list(area_ids, working_in_county)
                    scids = geos_from_aids(working_in_county, area_type='GDIS')
                    create_geo_list(area_ids, scids)
                elif reg_role == 2:
                    # Working in values are multi so handle differently
                    create_geo_list(area_ids, working_in)
                    create_geo_list(area_ids, working_in_ward)

                for pgeo in person_geos_all:
                    pgeo_id = pgeo['id']
                    pgeo_aid = pgeo['area_id']
                    pgeo_type = pgeo['area_type']
                    check_list.append(pgeo_aid)
                    if pgeo_aid not in area_ids:
                        area_ids_remove[pgeo_id] = pgeo_type
                for area_new in area_ids:
                    area_type = area_ids[area_new]
                    if area_new not in check_list:
                        new_list[area_new] = area_type
                save_locations(new_list, eperson_id)
                remove_locations(area_ids_remove, eperson_id)

                # Update Person types
                person_type_all = RegPersonsTypes.objects.filter(
                    person_id=eperson_id, is_void=False).values(
                    'id', 'person_type_id')
                new_ptypes, remove_ptypes, type_check_list = [], [], []
                for db_ptype in person_type_all:
                    db_type_id = db_ptype['person_type_id']
                    db_id = db_ptype['id']
                    type_check_list.append(db_type_id)
                    if db_type_id not in person_types:
                        remove_ptypes.append(db_id)
                for new_ptype in person_types:
                    if new_ptype not in type_check_list:
                        new_ptypes.append(new_ptype)
                print 'add', new_ptypes, 'remove', remove_ptypes
                save_person_type(new_ptypes, eperson_id)
                remove_person_type(remove_ptypes, eperson_id)

                # External IDs - factor external ids update on persons
                workforce_id = None
                beneficiary_id = None
                identifier_types = {}
                personids = RegPersonsExternalIds.objects.filter(
                    person_id=eperson_id, is_void=False).values_list(
                        'identifier_type_id', flat=True)

                if child_services and 'IWKF' not in personids:
                    print 'Create WF', child_services
                    if child_services == 'AYES':
                        workforce_id = workforce_id_generator(eperson_id)
                if 'TBGR' in person_types and 'ISCG' not in personids:
                        beneficiary_id = beneficiary_id_generator(eperson_id)
                if national_id:
                    identifier_types['INTL'] = national_id
                if staff_id:
                    identifier_types['IMAN'] = staff_id
                if workforce_id:
                    identifier_types['IWKF'] = workforce_id
                if beneficiary_id:
                    identifier_types['ISCG'] = beneficiary_id
                if birth_reg_id:
                    identifier_types['ISOV'] = birth_reg_id
                if other_phone_no:
                    identifier_types['CPHM'] = other_phone_no
                if physical_address:
                    identifier_types['CPHA'] = physical_address
                if tribe and person_type == 'TBVC':
                    identifier_types['ITRB'] = tribe
                if religion and person_type == 'TBVC':
                    identifier_types['IREL'] = religion
                if country and person_type == 'TBVC':
                    identifier_types['ICOU'] = country
                if given_name and person_type == 'TBVC':
                    identifier_types['IGNM'] = given_name

                save_person_extids(identifier_types, eperson_id)
                # For OVC programming Caregiver and Volunteer add cbo_id
                reg_ovc = request.session.get('reg_ovc', False)
                ovc_cbos = ['TBGR', 'TWVL', 'TBVC']
                ovc_type = str(person_type)
                print 'ptypes', ovc_type
                if reg_ovc and ovc_type in ovc_cbos:
                    cbo_id = request.POST.get('cbo_unit_id')
                    org, created = RegPersonsOrgUnits.objects.update_or_create(
                        person_id=eperson_id, org_unit_id=cbo_id,
                        date_delinked=None,
                        defaults={'person_id': eperson_id,
                                  'date_linked': now, 'date_delinked': None,
                                  'primary_unit': True, 'reg_assistant': False,
                                  'org_unit_id': cbo_id, 'is_void': False},)
                    print 'Delink all the old regions'
                    ops = RegPersonsOrgUnits.objects.filter(
                        person_id=eperson_id, is_void=False).exclude(
                        org_unit_id=cbo_id)
                    for op in ops:
                        print 'delink', op.id
                        op.is_void = True
                        op.date_delinked = now
                        op.save()
                msg = 'Update of Person (%s) was successful.' % first_name
                # For households
                attached_cg = extract_post_params(request, naming='cc_')
                attached_sb = extract_post_params(request, naming='sb_')
                print 'SB', attached_cg, attached_sb
                members = [eperson_id]
                for acg in attached_cg:
                    members.append(acg)
                for asb in attached_sb:
                    members.append(asb)
                # Check if household exits
                index_child, hh_members = get_household(eperson_id)
                if not index_child:
                    index_id = get_index_child(eperson_id)
                    if index_id:
                        umembers = list(set(members))
                        if index_id in members:
                            members.remove(index_id)
                        save_household(index_id, umembers)
            elif edit_type == 2:
                date_of_death = request.POST.get('date_of_death')
                if date_of_death:
                    date_of_death = convert_date(date_of_death)
                    set_person_dead(date_of_death, id)
                msg = 'Update of (%s) to dead was successful.' % (first_name)
            elif edit_type == 3:
                delete_person(id)
                if ovc:
                    ovc.is_void = True
                    ovc.save(update_fields=["is_void"])
                msg = 'Person (%s) deleted successfully.' % (first_name)

            # Perform audit trail here for all
            if edit_type:
                params = {}
                params['transaction_type_id'] = 'UPDS'
                params['interface_id'] = 'INTW'
                params['date_recorded_paper'] = audit_date
                params['paper_person_id'] = audit_workforce_id
                params['person_id'] = eperson_id
                save_audit_trail(request, params)

            messages.add_message(request, messages.INFO, msg)
            url = reverse(persons_search)
            if edit_type == 1:
                url = '%s?id=%d' % (reverse(persons_search), eperson_id)
            return HttpResponseRedirect(url)
        else:
            person, living_in = None, None
            is_workforce = None
            person_type_id = None
            person = RegPerson.objects.get(pk=id)
            if person.date_of_death:
                person_msg = ("This person is dead and not editable.")
                messages.error(request, person_msg)
                return HttpResponseRedirect(reverse(persons_search))
            person_types = RegPersonsTypes.objects.filter(
                person=person, is_void=False, date_ended=None).values_list(
                    'person_type_id', flat=True)
            person_geos = RegPersonsGeo.objects.select_related().filter(
                person=person, is_void=False, date_delinked=None)
            person_orgs = RegPersonsOrgUnits.objects.select_related().filter(
                person=person, is_void=False, date_delinked=None)
            person_extids = RegPersonsExternalIds.objects.filter(
                person=person, is_void=False)
            # These are for children household - Introduced in V2
            child_index, members = get_household(person.id)
            child_id = child_index if child_index else person.id
            print 'HH', child_index, members
            siblings = RegPersonsSiblings.objects.select_related().filter(
                child_person_id=child_id, is_void=False,
                date_delinked=None).exclude(sibling_person_id=id)
            # Reverse relationship
            osiblings = RegPersonsSiblings.objects.select_related().filter(
                sibling_person_id=person.id, is_void=False,
                date_delinked=None)
            guardians = RegPersonsGuardians.objects.select_related().filter(
                child_person_id=person.id, is_void=False, date_delinked=None)
            child_ids = [gd.child_person_id for gd in osiblings]
            gds = RegPersonsGuardians.objects.select_related()
            oguardians = gds.filter(child_person_id__in=child_ids,
                                    is_void=False, date_delinked=None)
            audits = RegPersonsAuditTrail.objects.select_related().filter(
                person=person)[:3]

            # Get person types
            is_ovc = False
            if person.designation == 'COVC' and 'TBVC' in person_types:
                is_ovc = True
            is_caregiver, person_type_id = '', ''
            if len(person_types) == 1:
                is_caregiver = ''
                person_type_id = person_types[0]
            elif len(person_types) == 2:
                is_caregiver = 'on'
                list(person_types).remove('TBGR')
                person_type_id = person_types[0]

            # Get living in and working in details
            working_in_county, living_in_county = [], None
            working_in_subcounty, working_in_ward = [], []
            living_in_subcounty, living_in_ward = '', ''
            area_id = None
            for pgeo in person_geos:
                area_id = pgeo.area_id
                area_type = pgeo.area.area_type_id
                geo_type = pgeo.area_type
                print 'IN', area_id
                if geo_type == 'GLTW':
                    if area_type == 'GPRV' and area_id:
                        working_in_county.append(area_id)
                    elif area_type == 'GDIS' and area_id:
                        working_in_subcounty.append(area_id)
                    else:
                        if area_id:
                            working_in_ward.append(area_id)
                else:
                    if area_type == 'GPRV' and area_id:
                        living_in_county = area_id
                    elif area_type == 'GDIS' and area_id:
                        living_in_subcounty = area_id
                    else:
                        if area_id:
                            living_in_ward = area_id
            # Hack to remove sub_county and ward ids
            print 'LIVIN IN', living_in_county, area_id
            # Get extid values
            id_map = {'INTL': 'national_id', 'IMAN': 'staff_id',
                      'IWKF': 'is_workforce', 'ISCG': 'caregiver_id',
                      'ISOV': 'birth_reg_id', 'CPHM': 'other_phone_number',
                      'CPHA': 'physical_address', 'ITRB': 'tribe',
                      'IREL': 'religion', 'ICOU': 'country',
                      'IGNM': 'given_name'}

            identifiers = {}
            for pextid in person_extids:
                pextid_identifier_type = pextid.identifier_type_id
                pextid_identifier = pextid.identifier
                if pextid_identifier_type in id_map:
                    id_name = id_map[pextid_identifier_type]
                    identifiers[id_name] = pextid_identifier

            # Get org unit values to help with checking primary unit
            pri_unit_id, units_list = '', []
            cbo_id = 0
            for person_org in person_orgs:
                cbo_id = person_org.org_unit_id
                pri_unit = person_org.primary_unit
                unit_names = person_org.org_unit.org_unit_name
                units_list.append(unit_names)
                if pri_unit:
                    pri_unit_id = person_org.org_unit.id
            person_org_names = ', '.join(units_list)
            date_birth = None
            if person.date_of_birth:
                # the_date = convert_date(person.date_of_birth, '%Y-%m-%d')
                date_birth = person.date_of_birth.strftime('%d-%b-%Y')

            # Offer child services
            for pers_ext in person_extids:
                ext_id_name = pers_ext.identifier_type_id
                ext_id_value = pers_ext.identifier
                if ext_id_name == 'IWKF':
                    is_workforce = ext_id_value
            child_service = 'AYES' if is_workforce else 'ANNO'
            child_ovc = 'AYES' if is_ovc else 'ANNO'
            # Cadres and designations
            designation = person.designation
            list_types = ['person_type_id', 'title_type_id',
                          'ngo_title_type_id']
            cadres = get_list_types(list_type=list_types)
            title_id = None
            for cadre in cadres:
                cadre_vals = cadres[cadre]
                for cadre_val in cadre_vals:
                    if designation and cadre_val.startswith(designation):
                        title_id = cadre
            # By inference determine region
            if not working_in_county and not working_in_subcounty:
                work_region = '0'
            elif working_in_county:
                work_region = '1'
            else:
                working_in_county = counties_from_aids(working_in_subcounty)
                print 'CNT', working_in_county, working_in_subcounty
                work_region = '2'
            # Living in county
            list_subcounties = []
            if living_in_subcounty:
                list_subcounties.append(living_in_subcounty)
            living_in_county = counties_from_aids(list_subcounties)
            if len(living_in_county) > 1:
                living_in_county = living_in_county[0]
            initial_vals = {
                'person_type': person_type_id,
                'person_id': person.pk,
                'is_caregiver': is_caregiver,
                'cadre_type': person.designation,
                'first_name': person.first_name,
                'other_names': person.other_names,
                'surname': person.surname, 'child_ovc': child_ovc,
                'des_phone_number': person.des_phone_number,
                'sex_id': person.sex_id, 'date_of_birth': date_birth,
                'email': person.email, 'working_in_county': working_in_county,
                'working_in_subcounty': working_in_subcounty,
                'working_in_ward': working_in_ward,
                'living_in_county': living_in_county,
                'living_in_subcounty': living_in_subcounty,
                'living_in_ward': living_in_ward,
                'org_unit_primary': pri_unit_id,
                'orgs_selected': person_org_names,
                'child_services': child_service,
                'working_in_region': work_region}
            if ovc:
                initial_vals['cbo_unit_id'] = ovc.child_cbo_id
                initial_vals['chv_unit_id'] = ovc.child_chv_id
            # For caregivers and volunteers for OVC Programming
            reg_ovc = request.session.get('reg_ovc', False)
            ovc_cbos = ['TBGR', 'TWVL']
            if reg_ovc and person_type_id in ovc_cbos:
                initial_vals['cbo_unit_id'] = cbo_id

            all_values = merge_two_dicts(initial_vals, identifiers)

            check_fields = ['sex_id', 'relationship_type_id']
            vals = get_dict(field_name=check_fields)
            # This is for titles
            list_types = ['person_type_id', 'title_type_id',
                          'ngo_title_type_id']
            person_titles = get_list_types(list_type=list_types)
            unused_titles = {'TBVC': [], 'TBGR': [], 'TWVL': []}
            titles = merge_two_dicts(person_titles, unused_titles)

            form = RegistrationForm(request.user, data=all_values)
            return render(request, 'registry/person_edit.html',
                          {'form': form, 'pk': person.pk,
                           'person_type': person_type_id, 'titles': titles,
                           'org_units': person_orgs, 'vals': vals,
                           'siblings': siblings, 'person': person,
                           'guardians': guardians, 'audits': audits,
                           'cadre_type': designation, 'title_type': title_id,
                           'todate': todate, 'region_id': work_region,
                           'child_ovc': child_ovc, 'osiblings': osiblings,
                           'oguardians': oguardians})
    except RegPerson.DoesNotExist:
            form = RegistrationSearchForm()
            return render(request, 'registry/person_search.html',
                          {'form': form})
    except Exception, e:
        msg = 'Person update error - %s' % (str(e))
        messages.add_message(request, messages.ERROR, msg)
        return HttpResponseRedirect(reverse(persons_search))
    else:
        return HttpResponseRedirect(reverse(persons_search))


@login_required
@is_allowed_groups(['RGM', 'RGU'])
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def new_user(request, id):
    """
    Page for creating users after registering a person.

    person must be either volunteer, NGO employee or Government
    """
    msg = ''
    password = ''

    try:
        person_id = int(id)
        # Get Name
        user = RegPerson.objects.get(pk=person_id)
        personfname = user.first_name
        personsname = user.surname
        names = user.full_name
        if request.method == 'POST':
            form = NewUser(user, data=request.POST)
            username = request.POST.get('username')
            password1 = request.POST.get('password1')
            password2 = request.POST.get('password2')

            # resolve existing account
            user_exists = AppUser.objects.filter(reg_person=person_id)
            if user_exists:
                msg = 'Person (%s %s) has an existing user account.' % (
                    personfname, personsname)
                messages.add_message(request, messages.INFO, msg)
                return HttpResponseRedirect(reverse(persons_search))

            if password1 == password2:
                password = password1
            else:
                msg = 'Passwords do not match!'
                messages.add_message(request, messages.INFO, msg)
                form = NewUser(user, data=request.POST)
                return render(request, 'registry/new_user.html',
                              {'form': form},)

            # validate username if__exists
            username_exists = AppUser.objects.filter(username__iexact=username)
            if username_exists:
                msg = 'Username (%s) is taken. Pick another one.' % username
                messages.add_message(request, messages.INFO, msg)
                form = NewUser(user, data=request.POST)
                return render(request, 'registry/new_user.html',
                              {'form': form},)
            else:
                # Create User
                user = AppUser.objects.create_user(username=username,
                                                   reg_person=person_id,
                                                   password=password)
                if user:
                    user.groups.add(Group.objects.get(
                        name='Standard logged in'))
                    # Capture msg & op status
                    msg = 'User (%s) save success.' % (username)
                    messages.add_message(request, messages.INFO, msg)
                    return HttpResponseRedirect(
                        '%s?id=%d' % (reverse(persons_search), int(person_id)))
        else:
            form = NewUser(user)
            return render(request, 'registry/new_user.html',
                          {'names': names, 'form': form},)
    except Exception, e:
        msg = 'Error - (%s) ' % (str(e))
        messages.add_message(request, messages.ERROR, msg)
        return HttpResponseRedirect(reverse(persons_search))


@login_required
def registry_look(request):
    """For JSON lookup stuff on registry pages."""
    try:
        msg, selects = 'Registry look up successful', ''
        results = {'message': msg}
        if request.method == 'POST':
            county = request.POST.getlist('county[]')
            sub_county = request.POST.getlist('sub_county[]')
            ward = request.POST.getlist('ward[]')
            action = int(request.POST.get('action'))
            filters = request.POST.get('filter')
            datas = sub_county if action == 1 else county
            extras = ward if action == 1 else sub_county
            print action, datas, extras
            if action == 4:
                extras = request.POST.getlist('ward')
                datas = request.POST.getlist('sub_county')
            if action == 6:
                county = request.POST.get('county')
                datas, extras = [county], []
            su = request.user.is_superuser
            # Check if in National person
            if filters and not su:
                national = RegPersonsGeo.objects.filter(
                    person_id=request.user.id, is_void=False,
                    date_delinked=None).count()
                if national == 0:
                    filters = False
            filter_id = request.user if filters and not su else False
            results = get_geo_selected(results, datas, extras, filter_id)
            res_extras = map(str, extras)
            if res_extras:
                selects = ','.join(res_extras)
            results['selects'] = selects
            print results
        return JsonResponse(results, content_type='application/json',
                            safe=False)
    except Exception, e:
        raise e


@login_required
def person_actions(request):
    """
    Json response on persons update stuff.

    Add / remove Organisational units
    Attach caregivers and siblings
    """
    try:
        results = {'status': 9}
        message = 'Record added successfully.'
        if request.method == 'POST':
            date_now = timezone.now()
            person_id = request.POST.get('person_id')
            edit_type = int(request.POST.get('edit_type'))
            attached_ou = extract_post_params(request, naming='ou_')
            if edit_type == 1:
                message = 'Organisational unit linked successfully.'
                for unid in attached_ou:
                    if len(attached_ou[unid]) > 1:
                        org_unit_id = int(unid)
                        pri_unit = attached_ou[unid]['pri']
                        reg_ass = attached_ou[unid]['reg']
                        pri_check = pri_unit == 'AYES' or pri_unit == 'Yes'
                        reg_check = reg_ass == 'AYES' or reg_ass == 'Yes'
                        is_pri_unit = True if pri_check else False
                        is_reg_ass = True if reg_check else False
                        val, ctd = RegPersonsOrgUnits.objects.update_or_create(
                            person_id=person_id, org_unit_id=org_unit_id,
                            is_void=False,
                            defaults={'person_id': person_id,
                                      'date_linked': date_now,
                                      'org_unit_id': org_unit_id,
                                      'primary_unit': is_pri_unit,
                                      'reg_assistant': is_reg_ass,
                                      'date_delinked': None,
                                      'is_void': False},)
            elif edit_type == 2:
                message = 'Organisational Unit delinked'
                org_unit_id = request.POST.get('org_unit_id')
                org_unit = get_object_or_404(
                    RegPersonsOrgUnits, person_id=person_id,
                    org_unit_id=org_unit_id, is_void=False)
                org_unit.date_delinked = date_now
                org_unit.is_void = True
                org_unit.save(update_fields=["date_delinked", "is_void"])
            elif edit_type == 3 or edit_type == 6:
                # This is for adding caregiver
                extids = {}
                message = 'Caregiver added successfully'
                attached_cg = extract_post_params(request, naming='cc_')
                # This will be a single record - Re-used method
                cpims_id = request.POST.get('caregiver_cpims_id')
                print 'CHK', attached_cg
                for ncg in attached_cg:
                    dob = None
                    if len(attached_cg[ncg]) > 2:
                        cgobj = attached_cg[ncg]
                        cgid = attached_cg[ncg]['cpid']
                        caregiver_id = int(cgid) if cgid.isnumeric() else 0
                        sex_id = attached_cg[ncg]['gender']
                        date_of_birth = attached_cg[ncg]['dob']
                        first_name = attached_cg[ncg]['fname']
                        other_names = attached_cg[ncg]['oname']
                        surname = attached_cg[ncg]['sname']
                        idno = cgobj['idno'] if 'idno' in cgobj else None
                        tel_no = cgobj['tel'] if 'tel' in cgobj else None
                        tel = tel_no if tel_no else None
                        if tel:
                            tel = tel[-9:]
                        print 'obj', cgobj
                        print 'tel', tel
                        if caregiver_id == 0:
                            if date_of_birth:
                                dob = convert_date(date_of_birth)
                            person = RegPerson(
                                designation='CCGV',
                                first_name=first_name.upper(),
                                other_names=other_names.upper(),
                                surname=surname.upper(),
                                sex_id=sex_id, date_of_birth=dob,
                                des_phone_number=tel, email=None,
                                created_by_id=request.user.id,
                                is_void=False)
                            person.save()
                            cpims_id = person.pk
                            results['caregiver_id'] = cpims_id
                            # Save this person type
                            person_types = ['TBGR']
                            save_person_type(person_types, cpims_id)
                            # Copy paste locations from child
                            copy_locations(person_id, cpims_id, request)
                            # Save National ID
                            if idno:
                                extids['INTL'] = idno
                                save_person_extids(extids, cpims_id)
                        # Now save this record to Guardians
                        is_adult = attached_cg[ncg]['adult']
                        relationship = attached_cg[ncg]['ctype']
                        child_headed = True if is_adult == 'No' else False
                        if edit_type == 3:
                            g_count = RegPersonsGuardians.objects.filter(
                                guardian_person_id=cpims_id,
                                child_person_id=person_id, is_void=False,
                                date_delinked=None).count()
                            if g_count == 0:
                                RegPersonsGuardians(
                                    child_person_id=person_id,
                                    guardian_person_id=cpims_id,
                                    relationship=relationship,
                                    date_linked=now,
                                    date_delinked=None,
                                    child_headed=child_headed,
                                    is_void=False).save()

                                # Create beneficiary id
                                pp_id = int(cpims_id)
                                ben_id = beneficiary_id_generator(pp_id)
                                extids['ISCG'] = ben_id
                                save_person_extids(extids, pp_id)
            elif edit_type == 4:
                # This is for adding siblings
                message = 'Sibling added successfully'
                attached_sb = extract_post_params(request, naming='sb_')
                sibling_id = save_sibling(request, attached_sb, person_id)
                if sibling_id:
                    results['sibling_id'] = sibling_id[0]
            elif edit_type == 5:
                # This is for removing guardians
                message = 'Caregiver detached successfully'
                guardian_id = request.POST.get('guardian_id')
                org_unit = get_object_or_404(
                    RegPersonsGuardians, guardian_person_id=guardian_id,
                    child_person_id=person_id, is_void=False,
                    date_delinked=None)
                org_unit.date_delinked = date_now
                org_unit.is_void = True
                org_unit.save(update_fields=["date_delinked", "is_void"])
            elif edit_type == 10:
                # This is for removing siblings
                message = 'Sibling detached successfully'
                sibling_id = request.POST.get('sibling_id')
                sib_details = get_object_or_404(
                    RegPersonsSiblings, sibling_person_id=sibling_id,
                    child_person_id=person_id, is_void=False,
                    date_delinked=None)
                sib_details.date_delinked = date_now
                sib_details.is_void = True
                sib_details.save(update_fields=["date_delinked", "is_void"])
            elif edit_type == 7:
                # Check if child is duplicate if all the following are the same
                # Names, DOB, Gender and Location (Sub-county and ward
                # When adding a new child.
                response = person_duplicate(request)
                results['status'] = response['status']
                message = 'Child duplicate checked successfully.'
            elif edit_type == 8:
                # Check if sibling is duplicate if below are the same
                # Names, DOB, Gender and Location (Sub-county and ward
                # When attaching or creating new siblings.
                response = person_duplicate(request, person='sibling')
                results['status'] = response['status']
                message = ('Sibling duplicate checked successfully.')
            elif edit_type == 9:
                # Got lazy; used this to check if unit exits with same name."""
                response = unit_duplicate(request)
                results['status'] = response['status']
                message = 'Organisation Unit checked successfully.'
            results['message'] = message
        return JsonResponse(results, content_type='application/json',
                            safe=False)
    except Exception, e:
        print 'Error on persons query - %s' % (str(e))
        raise e
