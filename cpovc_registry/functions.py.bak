"""Registry common functions."""
import uuid
import json
from datetime import datetime, timedelta
from django.utils import timezone
from django.db import connection
from django.shortcuts import get_object_or_404
from cpovc_main.models import SetupGeography, SetupList, RegTemp
from cpovc_main.functions import convert_date, get_dict
from django.db.models import Q, Count
from .models import (
    RegOrgUnitContact, RegOrgUnit, RegOrgUnitExternalID, RegOrgUnitGeography,
    RegPersonsOrgUnits, RegPersonsExternalIds, RegPerson, RegPersonsGeo,
    RegPersonsTypes, RegPersonsSiblings, RegPersonsAuditTrail, AppUser,
    RegOrgUnitsAuditTrail, OVCHouseHold, PersonsMaster)

from cpovc_ovc.models import OVCRegistration, OVCHHMembers, OVCEligibility

from cpovc_auth.models import CPOVCUserRoleGeoOrg
from cpovc_forms.models import (
    OVCCaseRecord, OVCCaseCategory, OVCCaseGeo, OVCCareServices)

from django.db import connection

organisation_id_prefix = 'U'
benficiary_id_prefix = 'B'
workforce_id_prefix = 'W'

def get_ovc_hiv_status():
    hiv_status={}
    hiv_status_list_envelop=[]
    ovc_reg=OVCRegistration.objects.all()
    ovc_reg_all_count=ovc_reg.count()
    ovc_reg_known_count = ovc_reg.filter(Q(hiv_status__iexact = "HSTP") | Q(hiv_status__iexact = "HSTN"))
    ovc_HSTP=ovc_reg.filter(Q(hiv_status__iexact = "HSTP")).count()

    ovc_unknown_count=ovc_reg_all_count-ovc_reg_known_count.count()
    hiv_status['ovc_unknown_count'] = ovc_unknown_count
    hiv_status['ovc_HSTP']=ovc_reg.filter(Q(hiv_status__iexact = "HSTP")).count()
    hiv_status['ovc_HSTN']=ovc_reg.filter(Q(hiv_status__iexact = "HSTN")).count()

    _on_art=ovc_reg.filter(Q(art_status = "ARAR"))
    on_art=_on_art.count()
    not_on_art=ovc_HSTP-on_art
    hiv_status['on_art']=on_art
    hiv_status['not_on_art']=not_on_art
    suppresed=0
    not_suppresed=0
    #get suppresion stats
    with connection.cursor() as cursor:
        try:
            cursor.execute(
                "SELECT count(*) FROM ovc_viral_load ovl inner join ovc_registration ovc on CAST (ovl.person_id  AS Varchar) = CAST (ovc.id  AS Varchar) "
                "where CAST (ovl.viral_load  AS Varchar) != 'lds' or ovl.viral_load < 1000"
                " and ovc.art_status = 'ARAR'"
            )
            _suppresed = cursor.fetchall()
            suppresed=_suppresed[0][0]


            cursor.execute(
                "SELECT count(*) FROM ovc_viral_load ovl inner join ovc_registration ovc on CAST (ovl.person_id  AS Varchar) = CAST (ovc.id  AS Varchar) "
                "where CAST (ovl.viral_load  AS Varchar) = 'lds' or ovl.viral_load > 1000"
                " and ovc.art_status = 'ARAR'"
            )
            _not_suppresed = cursor.fetchall()
            not_suppresed=_not_suppresed[0][0]

        except Exception, e:
            print 'error with dashs - %s' % (str(e))

    hiv_status['suppresed']=suppresed
    hiv_status['not_suppresed']=not_suppresed

    hiv_status_list_envelop.append(hiv_status)
    return hiv_status_list_envelop

def dashboard():
    """Method to get dashboard totals."""
    try:
        dash = {}
        vals = {'TBVC': 0, 'TBGR': 0, 'TWGE': 0, 'TWNE': 0}
        person_types = RegPersonsTypes.objects.filter(
            is_void=False, date_ended=None).values(
                'person_type_id').annotate(dc=Count('person_type_id'))
        for person_type in person_types:
            vals[person_type['person_type_id']] = person_type['dc']
        dash['children'] = vals['TBVC']
        dash['guardian'] = vals['TBGR']
        dash['government'] = vals['TWGE']
        dash['ngo'] = vals['TWNE']
        # Get org units
        org_units = RegOrgUnit.objects.filter(is_void=False).count()
        dash['org_units'] = org_units
        # Case records counts
        case_records = OVCCaseRecord.objects.filter(is_void=False)
        case_counts = case_records.count()
        dash['case_records'] = case_counts
        # Workforce members
        workforce_members = RegPersonsExternalIds.objects.filter(
            identifier_type_id='IWKF', is_void=False).count()
        dash['workforce_members'] = workforce_members
        # Case categories to find pending cases
        pending_cases = OVCCaseCategory.objects.filter(
            is_void=False)
        pending_count = pending_cases.exclude(
            case_id__summon_status=True).count()
        dash['pending_cases'] = pending_count
        dash['hiv_status']=get_ovc_hiv_status()
        # Child registrations
        case_regs = {}
        # Case Records
        ovc_regs = case_records.values(
            'date_case_opened').annotate(unit_count=Count('date_case_opened'))
        for ovc_reg in ovc_regs:
            the_date = ovc_reg['date_case_opened']
            # cdate = '1900-01-01'
            cdate = the_date.strftime('%d-%b-%y')
            case_regs[str(cdate)] = ovc_reg['unit_count']
        # Case categories Top 5
        case_categories = pending_cases.values(
            'case_category').annotate(unit_count=Count(
                'case_category')).order_by('-unit_count')
        dash['case_regs'] = case_regs
        dash['case_cats'] = case_categories
    except Exception, e:
        print 'error with dash - %s' % (str(e))
        dash = {}
        dash['children'] = 0
        dash['guardian'] = 0
        dash['government'] = 0
        dash['ngo'] = 0
        dash['org_units'] = 0
        dash['case_records'] = 0
        dash['workforce_members'] = 0
        dash['pending_cases'] = 0
        dash['case_regs'] = []
        dash['case_cats'] = 0
        return dash
    else:
        return dash


def ovc_dashboard(request):
    """Method to get dashboard totals."""
    try:
        dash = {}
        today = datetime.now()
        start_date = today - timedelta(days=30)
        vals = {'TBVC': 0, 'TBGR': 0, 'TWGE': 0, 'TWNE': 0}
        person_types = RegPersonsTypes.objects.filter(
            is_void=False, date_ended=None).values(
                'person_type_id').annotate(dc=Count('person_type_id'))
        for person_type in person_types:
            vals[person_type['person_type_id']] = person_type['dc']
        dash['children'] = vals['TBVC']
        dash['guardian'] = vals['TBGR']
        dash['government'] = vals['TWGE']
        dash['ngo'] = vals['TWNE']
        # OVC Filters
        cbo_id = request.session.get('ou_primary', 0)
        cbo_ids = request.session.get('ou_attached', [])
        reg_ovc = request.session.get('reg_ovc', 0)
        # Case records
        case_records = OVCCaseRecord.objects.filter(
            date_case_opened__gte=start_date, is_void=False)
        case_counts = case_records.count()
        dash['case_records'] = case_counts
        # Case categories to find pending cases
        pending_cases = OVCCaseCategory.objects.filter(
            date_of_event__gte=start_date, is_void=False)
        pending_count = pending_cases.exclude(
            case_id__summon_status=True).count()
        dash['pending_cases'] = pending_count
        # Child registrations
        ptypes = RegPersonsTypes.objects.filter(
            person_type_id='TBVC', is_void=False,
            date_ended=None).values_list('person_id', flat=True)
        # All linked CBOS
        org_id = int(cbo_id)
        org_ids = get_orgs_child(org_id)
        print 'dash orgs', org_ids
        # Get org units
        orgs_count = len(org_ids) - 1 if len(org_ids) > 1 else 1
        dash['org_units'] = orgs_count
        # Case records counts
        person_orgs = RegPersonsOrgUnits.objects.select_related().filter(
            org_unit_id__in=org_ids, is_void=False,
            date_delinked=None).values_list('person_id', flat=True)
        users_count = AppUser.objects.filter(
            reg_person_id__in=person_orgs).count()
        dash['workforce_members'] = users_count
        # For OVC
        child_regs, case_regs, ovc_regs = {}, {}, {}
        if request.user.is_superuser:
            regs = OVCRegistration.objects.filter(is_void=False)
        else:
            regs = OVCRegistration.objects.filter(
                is_void=False, child_cbo_id__in=org_ids)
        # Default values for IP summary
        am, af, em, ef, sm, sf, gm, gf = 0, 0, 0, 0, 0, 0, 0, 0
        # Get guardians
        guardian_genders = regs.values('caretaker__sex_id').annotate(
            total=Count('caretaker_id', distinct=True)).order_by('total')
        for gs in guardian_genders:
            g_gender = gs['caretaker__sex_id']
            g_count = gs['total']
            if g_gender:
                gg = str(g_gender)
                if gg == 'SMAL':
                    gm = g_count
                else:
                    gf = g_count
        guardian_count = regs.values('caretaker_id').distinct().count()
        dash['guardian'] = guardian_count
        # Get households
        child_ids = regs.values_list('person_id', flat=True)
        hh_count = OVCHHMembers.objects.filter(
            person_id__in=child_ids).values(
            'house_hold_id').distinct().count()
        if cbo_ids:
            cbos_list = [int(cbo_str) for cbo_str in cbo_ids.split(',')]
            org_ids = org_ids + cbos_list
        if request.user.is_superuser:
            oregs = OVCRegistration.objects.filter(
                registration_date__gte=start_date).values(
                'registration_date').annotate(
                unit_count=Count('registration_date'))
            cregs = RegPerson.objects.filter(
                created_at__gte=start_date, id__in=ptypes).values(
                'created_at').annotate(unit_count=Count('created_at'))
        else:
            oregs = OVCRegistration.objects.filter(
                child_cbo_id__in=org_ids,
                registration_date__gte=start_date).values(
                'registration_date').annotate(
                unit_count=Count('registration_date'))
            # Child registrations
            cregs = RegPerson.objects.filter(
                created_at__gte=start_date, id__in=ptypes)
            if reg_ovc:
                cregs = cregs.filter(id__in=child_ids)
            cregs = cregs.values('created_at').annotate(
                unit_count=Count('created_at'))
        dash['household'] = hh_count
        sqs = regs.values('is_active').annotate(
            total=Count('is_active')).order_by('total')
        # Get breakdown by Genders
        ovc_cls = regs.values(
            'is_active', 'person__sex_id').annotate(
            total=Count('person__sex_id')).order_by('total')
        ovc_schs = regs.filter(is_active=True).exclude(
            school_level='SLNS').values(
            'person__sex_id').annotate(
            total=Count('person__sex_id')).order_by('total')
        for ovc_sch in ovc_schs:
            child = ovc_sch['total']
            ovc_sex = str(ovc_sch['person__sex_id'])
            if ovc_sex == 'SMAL':
                sm = child
            else:
                sf = child
        for ovc_cl in ovc_cls:
            child = ovc_cl['total']
            status = ovc_cl['is_active']
            ovc_sex = str(ovc_cl['person__sex_id'])
            if status:
                if ovc_sex == 'SMAL':
                    am = child
                else:
                    af = child
            else:
                if ovc_sex == 'SMAL':
                    em = child
                else:
                    ef = child
        ovc_summ = {'m0': em + am, 'm1': am, 'm2': sm, 'm3': 0,
                    'm4': gm, 'f0': ef + af, 'f1': af,
                    'f2': sf, 'f3': 0, 'f4': gf}
        # Person types
        exited_ovc, active_child = 0, 0
        for sq in sqs:
            child = sq['total']
            status = sq['is_active']
            if status:
                active_child = child
            else:
                exited_ovc = child
        dash['children'] = active_child
        dash['children_all'] = exited_ovc + active_child
        for creg in cregs:
            the_date = creg['created_at']
            cdate = the_date.strftime('%d-%b-%y')
            child_regs[str(cdate)] = creg['unit_count']
        for oreg in oregs:
            the_date = oreg['registration_date']
            cdate = the_date.strftime('%d-%b-%y')
            ovc_regs[str(cdate)] = oreg['unit_count']
        # Case Records / OVC Services
        svm, svf = 0, 0
        if reg_ovc or request.user.is_superuser:
            ovc_serv_all = OVCCareServices.objects.filter(
                event__event_type_id='FSAM', is_void=False,
                event__date_of_event__gte=start_date,
                event__person_id__in=child_ids)
            ovc_servs = ovc_serv_all.values(
                'event__date_of_event').annotate(
                unit_count=Count('event__date_of_event'))
            # Served by gender
            ovc_servgs = ovc_serv_all.values(
                'event__person__sex_id').annotate(
                gender_count=Count('event__person_id', distinct=True))
            for oserv in ovc_servgs:
                sgender = str(oserv['event__person__sex_id'])
                child = oserv['gender_count']
                if sgender == 'SMAL':
                    svm = child
                else:
                    svf = child
            for ovc_serv in ovc_servs:
                the_date = ovc_serv['event__date_of_event']
                cdate = the_date.strftime('%d-%b-%y')
                case_regs[str(cdate)] = ovc_serv['unit_count']
        else:
            ovc_case_regs = case_records.values(
                'date_case_opened').annotate(
                unit_count=Count('date_case_opened'))
            for ovc_reg in ovc_case_regs:
                the_date = ovc_reg['date_case_opened']
                cdate = the_date.strftime('%d-%b-%y')
                case_regs[str(cdate)] = ovc_reg['unit_count']
        ovc_summ['m3'] = svm
        ovc_summ['f3'] = svf
        dash['ovc_summary'] = ovc_summ
        # Case categories Top 5
        cases = OVCEligibility.objects.filter(
            person_id__in=child_ids)
        case_criteria = cases.values(
            'criteria').annotate(unit_count=Count(
                'criteria')).order_by('-unit_count')
        dash['child_regs'] = child_regs
        dash['ovc_regs'] = ovc_regs
        dash['case_regs'] = case_regs
        dash['case_cats'] = {}
        dash['criteria'] = case_criteria
    except Exception, e:
        print 'error - %s' % (str(e))
        dash = {}
        dash['children'] = 0
        dash['children_all'] = 0
        dash['guardian'] = 0
        dash['government'] = 0
        dash['ngo'] = 0
        dash['org_units'] = 0
        dash['case_records'] = 0
        dash['workforce_members'] = 0
        dash['pending_cases'] = 0
        dash['child_regs'] = []
        dash['ovc_regs'] = []
        dash['case_regs'] = []
        dash['case_cats'] = 0
        dash['household'] = 0
        dash['criteria'] = {}
        dash['ovc_summary'] = {}
        return dash
    else:
        return dash


def get_unit_parent(org_ids):
    """Method to do the organisation tree."""
    try:
        orgs = []
        orgs_qs = RegOrgUnit.objects.filter(
            is_void=False,
            parent_org_unit_id__in=org_ids).values_list('id', flat=True)
        print 'Check Org Unit level - %s' % (str(orgs))
        if orgs_qs:
            orgs = [org for org in orgs_qs]
    except Exception as e:
        print 'No parent unit - %s' % (str(e))
        return []
    else:
        return orgs


def get_orgs_child(org_id, m=0):
    """Method to do the organisation tree."""
    try:
        if m:
            child_units = org_id
        else:
            child_units = [int(org_id)]
        p_orgs_3, p_orgs_2, p_orgs_1 = [], [], []
        parent_orgs = get_unit_parent(child_units)
        print 'c1', child_units, parent_orgs
        if parent_orgs:
            p_orgs_1 = get_unit_parent(parent_orgs)
            print 'c2', child_units
            if p_orgs_1:
                p_orgs_2 = get_unit_parent(p_orgs_1)
                print 'c3'
                if p_orgs_2:
                    p_orgs_3 = get_unit_parent(p_orgs_2)
                    print 'c4'
        all_units = child_units + parent_orgs + p_orgs_1 + p_orgs_2 + p_orgs_3
    except Exception as e:
        print 'error with tree - %s' % (str(e))
        return []
    else:
        return all_units


def save_household(index_child, members):
    """Method to create households."""
    try:
        hh_m = [str(m) for m in members]
        hh_ms = ','.join(hh_m)
        hh_members = '%s,%s,' % (index_child, hh_ms)
        OVCHouseHold(index_child_id=index_child,
                     members=hh_members).save()
    except Exception as e:
        print 'error creating household - %s ' % (str(e))
        pass


def get_ovc_lists(ovc_ids):
    """Method to get child chv details from ids."""
    try:
        ovc_details = OVCRegistration.objects.filter(
            person_id__in=ovc_ids, is_void=False)
    except Exception, e:
        print 'error getting ovc lists - %s' % (str(e))
        return {}
    else:
        return ovc_details


def get_index_child(child_id):
    """Method to get the index child."""
    try:
        index_id = 0
        siblings = RegPersonsSiblings.objects.select_related().filter(
            child_person_id=child_id, is_void=False, date_delinked=None)
        # Reverse relationship
        if not siblings:
            siblings = RegPersonsSiblings.objects.select_related().filter(
                sibling_person_id=child_id, is_void=False,
                date_delinked=None)
        for sibling in siblings:
            index_id = sibling.child_person_id
    except Exception as e:
        print 'error getting index child - %s' % (str(e))
        return 0
    else:
        return index_id


def get_household(chid):
    """Method to create households."""
    try:
        child_id = ',%s,' % (chid)
        child_index, cids = 0, []
        child_ids = []
        members = OVCHouseHold.objects.filter(
            index_child_id=chid)
        if not members:
            print 'no mm'
            members = OVCHouseHold.objects.filter(
                members__contains=child_id)
        for member in members:
            cids = member.members.split(',')
            child_index = member.index_child_id
        print 'NN', cids, child_index
        for cid in cids:
            if cid:
                child_ids.append(int(cid))
    except Exception as e:
        print 'error getting household - %s ' % (str(e))
        return 0, []
    else:
        return child_index, child_ids


def get_chvs(person_id):
    """Method to get CHV."""
    try:
        cbo_detail = {'': "Select CHV"}
        # Get my organisation unit / CBO
        org_units = RegPersonsOrgUnits.objects.filter(
            is_void=False, person_id=person_id).values_list(
            'org_unit_id', flat=True)
        org_list = [org for org in org_units]
        org_child = get_unit_parent(org_list)
        org_units = org_list + org_child
        # Get all chvs attached to this org unit / CBO
        person_ids = RegPersonsOrgUnits.objects.filter(
            is_void=False, org_unit_id__in=org_units).values_list(
            'person_id', flat=True)
        # Filter by types
        persons = RegPersonsTypes.objects.filter(
            is_void=False, person_type_id='TWVL', person_id__in=person_ids)
        for person in persons:
            cbo_detail[person.person_id] = person.person.full_name
        chvs = cbo_detail.items()
    except Exception, e:
        print "error getting CHV - %s" % (str(e))
        return ()
    else:
        return chvs


def get_temp(request):
    """Method to get last temp data only less than 15 minutes old."""
    try:
        user_id = request.user.id
        page_id = request.get_full_path()
        print "CHECK TMP", user_id, page_id
        time_threshold = timezone.now() - timedelta(minutes=15)
        tmps = RegTemp.objects.get(user_id=user_id, page_id=page_id,
                                   created_at__gt=time_threshold)
        if tmps:
            return eval(tmps.data)
        return {}
    except Exception:
        return {}


def unit_duplicate(request):
    """Method to check if same unit exists with same name."""
    resp = {'status': 0}
    try:
        print 'DUP org check', request.POST
        unit_name = request.POST.get('org_unit_name').strip()
        existing_units = RegOrgUnit.objects.filter(
            org_unit_name__iexact=unit_name, is_void=False).count()
        resp['status'] = existing_units
        return resp
    except Exception, e:
        print "Error checking unit duplicate - %s" % (str(e))
        return {'status': 9}


def person_duplicate(request, person='child'):
    """Method to check if child already exists."""
    resp = {'status': 0}
    try:
        print 'DUP Check', request.POST
        if person == 'sibling':
            first_name = request.POST.get('sibling_firstname').strip()
            surname = request.POST.get('sibling_surname').strip()
            other_names = request.POST.get('sibling_othernames').strip()
            date_of_birth = request.POST.get('sibling_dob')
            gender = request.POST.get('sibling_gender')
        else:
            first_name = request.POST.get('first_name').strip()
            surname = request.POST.get('surname').strip()
            other_names = request.POST.get('other_names').strip()
            date_of_birth = request.POST.get('date_of_birth')
            gender = request.POST.get('sex_id')
        sub_county = request.POST.get('living_in_subcounty')
        ward = request.POST.get('living_in_ward')
        if not date_of_birth or len(str(date_of_birth)) != 10:
            date_of_birth = None
        else:
            date_of_birth = convert_date(date_of_birth)
        children_qs = RegPerson.objects.filter(
            first_name__iexact=first_name, surname__iexact=surname,
            date_of_birth=date_of_birth, sex_id=gender, is_void=False)
        if other_names:
            children_qs = children_qs.filter(
                other_names__iexact=other_names)
        # Check in Geo locations
        pers_geo = RegPersonsGeo.objects.filter(
            area_id=sub_county, is_void=False)
        pers_geo = pers_geo.values_list("person__id")
        children_qs = children_qs.filter(id__in=pers_geo)
        if ward:
            ward_geo = RegPersonsGeo.objects.filter(
                area_id=ward, is_void=False)
            ward_geo = ward_geo.values_list("person__id")
            children_qs = children_qs.filter(id__in=ward_geo)
        if children_qs:
            resp['status'] = children_qs.count()
            resp['child'] = children_qs
        return resp
    except Exception, e:
        print 'Error checking child duplicate - %s' % (str(e))
        return {'status': 99}


def get_list_types(list_type=['organisation_type_id']):
    """Method to get all organisation types for js."""
    try:
        org_units = SetupList.objects.filter(is_void=False)
        vals = []
        orgs = {}
        orgs_dict = {}
        cnt = 0
        for org_unit in org_units:
            field_name = org_unit.field_name
            item_sub_cat = org_unit.item_sub_category
            res = {'id': org_unit.item_id, 'name': org_unit.item_description,
                   'cat': item_sub_cat, 'field_name': field_name}
            vals.append(res)
            if org_unit.field_name in list_type:
                cnt += 1
                blks = 'BLK_%s' % (str(cnt))
                item_scat = item_sub_cat if item_sub_cat else blks
                orgs[item_scat] = org_unit.item_id
        for val in vals:
            val_field = val['field_name']
            if val_field in orgs:
                type_id = str(orgs[val_field])
                type_id_name = '%s,%s' % (str(val['id']), str(val['name']))
                if type_id not in orgs_dict:
                    orgs_dict[type_id] = [type_id_name]
                else:
                    orgs_dict[type_id].append(type_id_name)
        for org in orgs:
            if org.startswith('BLK_'):
                org_id = orgs[org]
                orgs_dict[org_id] = []
        return orgs_dict
    except Exception, e:
        print 'error - %s' % (str(e))
        pass


def get_user_geos(user):
    """Get attached user Geos."""
    try:
        user_id = user.id
        sub_counties = []
        results = {'sub_counties': [], 'counties': [], 'wards': []}
        user_geos = CPOVCUserRoleGeoOrg.objects.select_related().filter(
            is_void=False, user_id=user_id, area_id__isnull=False)
        print "CHECK", user_geos, user_id
        for user_geo in user_geos:
            geo_id = user_geo.area_id
            sub_counties.append(geo_id)
        if sub_counties:
            # Get all counties if in this list of sub-counties
            wards = []
            counties = counties_from_aids(sub_counties)
            results['sub_counties'] = sub_counties
            results['counties'] = counties
            # Get all counties if in this list of sub-counties
            if counties:
                wards = geos_from_aids(sub_counties, area_type='GWRD')
            results['wards'] = wards
        return results
    except Exception:
        pass


def get_user_details(person):
    """Method to get account user details."""
    try:
        person_appuser = AppUser.objects.get(
            reg_person=person, is_active=True)
        return person_appuser
    except Exception, e:
        print "Get user details error - %s" % (str(e))
        return None


def counties_from_aids(area_list, area_type='GDIS'):
    """Method to get counties for display from area ids."""
    try:
        geos = []
        if area_list:
            geos = SetupGeography.objects.filter(
                area_id__in=area_list, area_type_id=area_type,
                is_void=False).values_list('parent_area_id', flat=True)
    except Exception, e:
        print 'Error getting county list from area ids - %s' % (str(e))
        return []
    else:
        return geos


def geos_from_aids(area_list, area_type='GWRD'):
    """Method to get wards from sub-counties for display from area ids."""
    try:
        geos = SetupGeography.objects.filter(
            parent_area_id__in=area_list, area_type_id=area_type,
            is_void=False).values_list('area_id', flat=True)
    except Exception, e:
        print 'Error getting geo list from area ids - %s' % (str(e))
        return []
    else:
        return geos


def create_geo_list(geo_dict, form_items, geo_type='GLTW'):
    """Method to create a big dict for saving all geo locations."""
    try:
        if form_items:
            for geo_item in form_items:
                if geo_item:
                    geo_dict[int(geo_item)] = geo_type
    except Exception, e:
        print 'Error creating persons geos - %s' % (str(e))
        return geo_dict
    else:
        return geo_dict


def save_audit_trail(request, params, audit_type='Person'):
    """Method to save audit trail depending on transaction."""
    try:
        user_id = request.user.id
        ip_address = get_client_ip(request)
        transaction_type_id = params['transaction_type_id']
        interface_id = params['interface_id']
        meta_data = get_meta_data(request)
        paper_date = None
        print 'Audit Trail', params
        if len(params) >= 3 and audit_type == 'Person':
            date_recorded_paper = params['date_recorded_paper']
            paper_person_id = params['paper_person_id']
            if not paper_person_id:
                paper_person_id = user_id
            person_id = params['person_id']
            if date_recorded_paper:
                paper_date = convert_date(date_recorded_paper)
            RegPersonsAuditTrail(
                transaction_type_id=transaction_type_id,
                interface_id=interface_id,
                date_recorded_paper=paper_date,
                person_recorded_paper_id=paper_person_id,
                timestamp_modified=None,
                app_user_id=user_id,
                ip_address=ip_address,
                meta_data=meta_data,
                person_id=person_id).save()
        elif audit_type == 'Unit':
            org_unit_id = params['org_unit_id']
            RegOrgUnitsAuditTrail(
                transaction_type_id=transaction_type_id,
                interface_id=interface_id,
                timestamp_modified=None,
                org_unit_id=org_unit_id,
                ip_address=ip_address,
                meta_data=meta_data,
                app_user_id=user_id).save()
    except Exception, e:
        print 'Error saving audit - %s' % (str(e))
        pass
    else:
        pass


def save_sibling(request, attached_sb, person_id):
    """Method to save siblings in some weird manner."""
    try:
        new_sib_ids = []
        designation = 'CGSI'
        for sib_id in attached_sb:
            if len(attached_sb[sib_id]) > 4:
                sibling_fdob = attached_sb[sib_id]['dob']
                sibling_names = attached_sb[sib_id]['names'].split('|')
                sibling_rmk = attached_sb[sib_id]['rmk']
                sibling_sex = attached_sb[sib_id]['sex']
                sibling_first_name = sibling_names[0].upper()
                sibling_surname = sibling_names[1].upper()
                sibling_othernames = sibling_names[2].upper()
                sibling_cpid = attached_sb[sib_id]['sbid']
                # To be used by the education background form
                # sibling_class = attached_sb[sib_id]['slevel']
                # Convert date to db one here
                is_dob = None if len(str(sibling_fdob)) != 11 else True
                sibling_dob = convert_date(sibling_fdob) if is_dob else None
                if sibling_cpid:
                    sibling_id = int(sibling_cpid)
                else:
                    child_ovc = request.POST.get('child_ovc')
                    is_ovc = True if child_ovc == 'AYES' else False
                    designation = 'COSI' if is_ovc else 'CGSI'
                    # Save as a person if has no sibling id
                    person = RegPerson(
                        designation=designation,
                        first_name=sibling_first_name.upper(),
                        other_names=sibling_othernames.upper(),
                        surname=sibling_surname.upper(),
                        sex_id=sibling_sex, date_of_birth=sibling_dob,
                        des_phone_number=None, email='',
                        created_by_id=request.user.id,
                        is_void=False)
                    person.save()
                    sibling_id = person.pk
                    # Save this person type
                    person_types = ['TBVC']
                    save_person_type(person_types, sibling_id)
                todate = timezone.now()
                # Save child as OVC
                if designation == 'COSI':
                    reg_date = '1900-01-01'
                    cbo_id = request.POST.get('cbo_unit_id')
                    chv_id = request.POST.get('chv_unit_id')
                    ovc = OVCRegistration(
                        person_id=sibling_id, registration_date=reg_date,
                        has_bcert=False, is_disabled=False, is_void=False,
                        child_cbo_id=cbo_id, child_chv_id=chv_id,
                        exit_date=None, created_at=todate)
                    ovc.save()

                nsib, created = RegPersonsSiblings.objects.update_or_create(
                    child_person_id=person_id, is_void=False,
                    sibling_person_id=sibling_id,
                    defaults={'child_person_id': person_id,
                              'sibling_person_id': sibling_id,
                              'date_linked': todate, 'remarks': sibling_rmk,
                              'is_void': False},)
                # Use Owners location details to create/update sibling details
                copy_locations(person_id, sibling_id, request)
                new_sib_ids.append(sibling_id)
                # Audit trail required here for tracking creators
                params = {}
                params['transaction_type_id'] = 'REGS'
                params['interface_id'] = 'INTW'
                params['date_recorded_paper'] = None
                params['paper_person_id'] = None
                params['person_id'] = int(sibling_id)
                save_audit_trail(request, params)
    except Exception, e:
        print 'Error attaching sibling - ', str(e)
        pass
    else:
        return new_sib_ids


def copy_locations(person_id, relative_id, request):
    """Method to copy owners locations to sibling / guardian."""
    try:
        todate = timezone.now()
        owner_locations = RegPersonsGeo.objects.filter(
            is_void=False, date_delinked=None, person_id=person_id)
        if owner_locations:
            for oloc in owner_locations:
                area_id = oloc.area_id
                area_type = oloc.area_type
                nloc, created = RegPersonsGeo.objects.update_or_create(
                    person_id=relative_id, area_id=area_id, is_void=False,
                    defaults={'area_id': area_id,
                              'person_id': relative_id,
                              'area_type': area_type,
                              'date_linked': todate,
                              'is_void': False},)
        else:
            print 'Child does not exist but create CG'
            area_id = request.POST.get('living_in_subcounty')
            nloc, created = RegPersonsGeo.objects.update_or_create(
                person_id=relative_id, area_id=area_id, is_void=False,
                defaults={'area_id': area_id,
                          'person_id': relative_id,
                          'area_type': 'GLTL',
                          'date_linked': todate,
                          'is_void': False},)
    except Exception, e:
        raise e


def save_person_extids(identifier_types, person_id):
    """Save Person external ids details - Create or update."""
    try:
        for identifier_type in identifier_types:
            identifier = identifier_types[identifier_type]
            location, created = RegPersonsExternalIds.objects.update_or_create(
                person_id=person_id, identifier_type_id=identifier_type,
                is_void=False,
                defaults={'person_id': person_id, 'identifier': identifier,
                          'identifier_type_id': identifier_type,
                          'is_void': False},)
    except Exception, e:
        raise e
    else:
        pass


def save_person_type(person_types, person_id):
    """Method to save all person types."""
    try:
        now = timezone.now()
        for i, p_type in enumerate(person_types):
            RegPersonsTypes(
                person_id=person_id,
                person_type_id=p_type,
                date_began=now,
                date_ended=None,
                is_void=False).save()
    except Exception, e:
        raise e
    else:
        pass


def remove_person_type(person_types, person_id):
    """To mark as removed all person types - date_ended."""
    try:
        now = timezone.now()
        for i, type_id in enumerate(person_types):
            person_area = get_object_or_404(
                RegPersonsTypes, pk=type_id,
                person_id=person_id, is_void=False)
            person_area.date_ended = now
            person_area.save(update_fields=["date_ended"])
    except Exception, e:
        raise e
    else:
        pass


def save_locations(area_ids, person_id):
    """Save locations details."""
    try:
        now = timezone.now()
        for area_id in area_ids:
            area_type = area_ids[area_id]
            RegPersonsGeo(
                person_id=person_id,
                area_id=area_id,
                area_type=area_type,
                date_linked=now,
                date_delinked=None,
                is_void=False).save()
    except Exception, e:
        raise e
    else:
        pass


def remove_locations(area_ids, person_id):
    """Save locations details."""
    try:
        now = timezone.now()
        for area_id in area_ids:
            person_area = get_object_or_404(
                RegPersonsGeo, pk=area_id, person_id=person_id, is_void=False)
            person_area.date_delinked = now
            person_area.is_void = True
            person_area.save(update_fields=["date_delinked", "is_void"])
    except Exception, e:
        raise e
    else:
        pass


def names_from_ids(ids, registry='orgs'):
    """Method to return geo names from list of ids."""
    try:
        orgs = get_specific_geos(ids, registry, reg_type=['GDIS', 'GWRD'])
        orgs_name = {}
        # For getting all area names comma separated
        for geo in ids:
            if geo in orgs:
                gname = orgs[geo]
                gname = list(set(gname))
                orgs_name[geo] = ', '.join(gname)
            else:
                orgs_name[geo] = None
    except Exception, e:
        print 'Error getting list - %s' % (str(e))
        return None
    else:
        return orgs_name


def merge_two_dicts(dict_x, dict_y):
    """
    Given two dicts, merge them into a new dict.

    Uses a shallow copy.
    """
    new_dict = dict_x.copy()
    new_dict.update(dict_y)
    return new_dict


def get_attached_ous(request):
    """method to get attached ous"""
    try:
        ous = []
        if 'ou_attached' in request.session:
            attached_ous = request.session['ou_attached']
            if attached_ous:
                ous = [int(ou) for ou in attached_ous.split(',')]
    except Exception as e:
        print 'error getting attached ous - %s' % (str(e))
        return []
    else:
        return ous


def auto_suggest_person(request, query, qid=0):
    """
    Auto suggest method using jquery auto-suggest.

    Return values are json with extra
    parameters for siblings and caregivers
    """
    try:
        results = []
        person_type = 'TBGR'
        query_id = int(request.GET.get('id'))
        reg_ovc = request.session.get('reg_ovc', 0)
        cbo_id = request.session.get('ou_primary', 0)
        cbo_ids = request.session.get('ou_attached', [])
        # All linked CBOS
        org_id = int(cbo_id)
        org_ids = get_orgs_child(org_id)
        if cbo_ids:
            cbos_list = [int(cbo_str) for cbo_str in cbo_ids.split(',')]
            org_ids = org_ids + cbos_list
        # Get the filter ids
        query_ids = {0: 'TBGR', 1: 'TBVC', 2: 'IWKF'}
        detail_list = [0, 1]
        if query_id in query_ids:
            person_type = query_ids[query_id]
        # Filter by same org units
        # ous = get_attached_ous(request)
        # print 'ou', ous
        tstring = str(query)
        qstring = unicode(tstring)
        psearch = tstring if qstring.isnumeric() else False
        print 'ID search', psearch
        # Get IDS
        ext_ids = {}
        if psearch:
            pids = RegPersonsExternalIds.objects.filter(
                identifier=psearch, identifier_type_id='INTL',
                is_void=False)
            person_list = pids.values_list('person_id', flat=True)
            persons = RegPerson.objects.filter(
                id__in=person_list, is_void=False)
        else:
            porgs = RegPersonsOrgUnits.objects.filter(
                org_unit_id__in=org_ids).values_list('person_id', flat=True)
            # Filters for external ids
            if query_id in detail_list:
                if reg_ovc:
                    person_ids = RegPersonsTypes.objects.filter(
                        person_type_id=person_type, person_id__in=porgs,
                        is_void=False).values_list(
                            'person_id', flat=True)
                else:
                    person_ids = RegPersonsTypes.objects.filter(
                        person_type_id=person_type,
                        is_void=False).values_list(
                            'person_id', flat=True)
            else:
                wf_ids = ['TWNE', 'TWGE', 'TWVL']
                person_ids = RegPersonsTypes.objects.filter(
                    person_type_id__in=wf_ids, person_id__in=porgs,
                    is_void=False).values_list(
                        'person_id', flat=True)
            queryset = RegPerson.objects.filter(
                id__in=person_ids, is_void=False)
            field_names = ['surname', 'email', 'first_name', 'other_names']
            q_filter = Q()
            for field in field_names:
                q_filter |= Q(**{"%s__icontains" % field: query})
            persons = queryset.filter(q_filter)
            pids = RegPersonsExternalIds.objects.filter(
                person_id__in=person_ids, identifier_type_id='INTL')
        for pid in pids:
            ext_ids[pid.person_id] = pid.identifier
        for person in persons:
            person_id = person.pk
            onames = person.other_names if person.other_names else ''
            names = '%s %s %s' % (person.first_name, person.surname,
                                  onames)
            idno = ext_ids[person_id] if person_id in ext_ids else None
            id_ext = ' - %s' % (idno) if idno else ''
            name = '%s%s' % (names.strip(), id_ext)
            val = {'id': person.pk, 'label': name, 'value': name}
            if query_id in detail_list:
                person_dob = person.date_of_birth
                if person_dob:
                    dob_dateobj = convert_date(str(person_dob), '%Y-%m-%d')
                    person_dob = dob_dateobj.strftime('%d-%b-%Y')
                val['gender'] = person.sex_id
                val['dob'] = person_dob
                val['fname'] = person.first_name
                val['sname'] = person.surname
                val['onames'] = person.other_names
                val['tel'] = person.des_phone_number
                val['idno'] = idno
            if query_id == 1:
                # Get case records belonging to this child
                cases, case_ids, allowed_cases = [], [], []
                all_cases = OVCCaseRecord.objects.filter(
                    is_void=False, person_id=person_id)
                for case in all_cases:
                    case_date = case.date_case_opened.strftime('%d-%b-%Y')
                    cd = {'id': case.case_id, 'serial': str(case.case_serial),
                          'case_date': case_date}
                    cases.append(cd)
                    case_ids.append(case.case_id)
                if case_ids:
                    # Now filter only cases handled by this org unit
                    my_org_id = request.session.get('ou_primary')
                    print 'PERMS', my_org_id, case_ids
                    all_cids = OVCCaseGeo.objects.filter(
                        is_void=False, case_id_id__in=case_ids,
                        report_orgunit_id=my_org_id)
                    for ac in all_cids:
                        allowed_cases.append(ac.case_id_id)
                if cases:
                    new_case = []
                    for case in cases:
                        if case['id'] in allowed_cases:
                            new_case.append(case)
                    if new_case:
                        val['cases'] = new_case
                    if request.user.is_superuser:
                        val['cases'] = cases
                val['label'] = '%s (%s)' % (name, len(cases))
            results.append(val)
    except Exception, e:
        print 'error checking persons - %s' % (str(e))
        return []
    else:
        return results


def extract_post_params(request, naming='cc_'):
    """Extract from POST params values starting with some naming."""
    try:
        reqs = request.POST
        req_vals = {}
        for req in reqs:
            val = request.POST.get(req).strip()
            if req.startswith(naming):
                vals = req.split('_')
                if len(vals) > 2:
                    cid, cvalue = vals[1], vals[2]
                    if cid not in req_vals:
                        req_vals[cid] = {}
                    if len(req_vals) > 0:
                        req_vals[cid][cvalue] = val
                    else:
                        req_vals[cid] = {cvalue: val}
                else:
                    cid = vals[1]
                    req_vals[cid] = val.split(',')
        return req_vals
    except Exception, e:
        raise e


def create_olists(org_lists, org_detail, org_ids, ltype=0, i_type=0):
    """Method to create org list of units, sub-units and sub-sub-units."""
    inst_types = ['TNRH', 'TNRB', 'TNRR', 'TNRS', 'TNAP', 'TNRC']
    try:
        if ltype == 0:
            for org_list in org_lists:
                unit_id = org_list.org_unit.id
                unit_vis = org_list.org_unit.org_unit_id_vis
                unit_name = org_list.org_unit.org_unit_name
                unit_type = org_list.org_unit.org_unit_type_id
                unit_names = '%s - %s' % (unit_vis, unit_name)
                org_detail[unit_id] = unit_names
                if i_type == 1:
                    if unit_type in inst_types:
                        org_ids.append(unit_id)
                else:
                    org_ids.append(unit_id)
        else:
            for org_list in org_lists:
                unit_id = org_list.id
                unit_vis = org_list.org_unit_id_vis
                unit_name = org_list.org_unit_name
                unit_type = org_list.org_unit_type_id
                unit_names = '%s - %s' % (unit_vis, unit_name)
                org_detail[unit_id] = unit_names
                if i_type == 1:
                    if unit_type in inst_types:
                        org_ids.append(unit_id)
                else:
                    org_ids.append(unit_id)
    except Exception, e:
        raise e
    else:
        return org_detail, org_ids


def get_specific_orgs(user_id, i_type=0):
    """Get specific Organisational units based on user id."""
    org_detail, result = {'': 'Select Parent Unit'}, ()
    try:
        org_ids = []
        org_lists = RegPersonsOrgUnits.objects.select_related().filter(
            person_id=user_id, is_void=False)
        if org_lists:
            org_detail, org_ids = create_olists(
                org_lists, org_detail, org_ids, 0, i_type)
            # Get sub units
            sub_results = RegOrgUnit.objects.select_related().filter(
                parent_org_unit_id__in=org_ids, is_void=False)
            if sub_results:
                org_detail, sub_org_ids = create_olists(
                    sub_results, org_detail, org_ids, 1, i_type)
                # Get sub sub units
                ssub_results = RegOrgUnit.objects.select_related().filter(
                    parent_org_unit_id__in=sub_org_ids, is_void=False)
                if ssub_results:
                    org_detail, ssub_org_ids = create_olists(
                        ssub_results, org_detail, org_ids, 2, i_type)
        result = org_detail.items()
    except Exception, e:
        error = 'Error getting specific orgs - %s' % (str(e))
        print error
        return result
    else:
        return result


def get_specific_geos(list_ids, registry='orgs', reg_type=[]):
    """Get specific Geography based on user id."""
    try:
        orgs = {}
        if registry == 'persons':
            geos = RegPersonsGeo.objects.select_related().filter(
                person_id__in=list_ids, is_void=False, date_delinked=None)
            # For getting all area ids for geo-locations
            for geo in geos:
                person_id = geo.person_id
                area_name = geo.area.area_name
                area_type = geo.area.area_type_id
                if area_type in reg_type:
                    if person_id not in orgs:
                        orgs[person_id] = [area_name]
                    else:
                        orgs[person_id].append(area_name)
        elif registry == 'person_orgs':
            print 'pps', list_ids
            geos = RegPersonsOrgUnits.objects.select_related().filter(
                person_id__in=list_ids, is_void=False)
            # For getting all geo ids for org units
            for geo in geos:
                person_id = geo.person_id
                org_name = geo.org_unit.org_unit_name

                if person_id not in orgs:
                    orgs[person_id] = [org_name]
                else:
                    orgs[person_id].append(org_name)
            # This is for OVC
            ovcs = get_ovc_lists(list_ids)
            for ovc in ovcs:
                person_id = ovc.person_id
                org_name = ovc.child_cbo.org_unit_name

                if person_id not in orgs:
                    orgs[person_id] = [org_name]
                else:
                    orgs[person_id].append(org_name)
        elif registry == 'person_types':
            person_types = get_dict(field_name=['person_type_id'])
            geos = RegPersonsTypes.objects.select_related().filter(
                person_id__in=list_ids, is_void=False, date_ended=None)
            # For getting all person type ids for persons
            for geo in geos:
                person_id = geo.person_id
                type_id = geo.person_type_id
                if type_id in person_types:
                    type_name = person_types[type_id]
                    if person_id not in orgs:
                        orgs[person_id] = [type_name]
                    else:
                        orgs[person_id].append(type_name)
        else:
            geos = RegOrgUnitGeography.objects.select_related().filter(
                org_unit_id__in=list_ids, is_void=False, date_delinked=None)
            # For getting all area ids for geo-locations
            for geo in geos:
                org_id = geo.org_unit_id
                area_name = geo.area.area_name
                area_type = geo.area.area_type_id
                if area_type in reg_type:
                    if org_id not in orgs:
                        orgs[org_id] = [area_name]
                    else:
                        orgs[org_id].append(area_name)
    except Exception, e:
        error = 'Error getting geos - %s' % (str(e))
        print error
    else:
        return orgs


def get_specific_units(org_ids):
    """Get specific Organisational units based on lit of units."""
    try:
        result = RegOrgUnitGeography.objects.select_related().filter(
            org_unit_id__in=org_ids, is_void=False)
    except Exception, e:
        error = 'Error getting geos - %s' % (str(e))
        print error
    else:
        return result


def get_geo_selected(results, datas, extras, filters=False):
    """Get specific Geography based on existing ids."""
    wards = []
    all_list = get_all_geo_list(filters)
    results['wards'] = datas
    area_ids = map(int, datas)
    selected_ids = map(int, extras)
    # compare
    for geo_list in all_list:
        parent_area_id = geo_list['parent_area_id']
        area_id = geo_list['area_id']
        area_name = geo_list['area_name']
        if parent_area_id in area_ids:
            final_list = '%s,%s' % (area_id, area_name)
            wards.append(final_list)
        # attach already selected
        if area_id in selected_ids:
            extra_list = '%s,%s' % (area_id, area_name)
            wards.append(extra_list)
    unique_wards = list(set(wards))
    results['wards'] = unique_wards
    return results


def get_all_geo_list(filters=False):
    """Get all Geo Locations."""
    try:
        geo_lists = SetupGeography.objects.all()
        geo_lists = geo_lists.filter(is_void=False)
        if filters:
            all_geos = get_user_geos(filters)
            if all_geos:
                subcounty_list = list(all_geos['sub_counties'])
                all_ids = subcounty_list + list(all_geos['wards'])
                geo_lists = geo_lists.filter(area_id__in=all_ids)
        geo_lists = geo_lists.values(
            'area_id', 'area_type_id', 'area_name', 'parent_area_id')
        # .exclude(area_type_id='GPRV')
    except Exception, e:
        raise e
    else:
        return geo_lists


def get_geo_list(geo_lists, geo_filter, add_select=False, user_filter=[]):
    """Get specific Organisational units based on filter and list."""
    area_detail, result = {}, ()
    if add_select:
        area_detail[''] = 'Please Select'
    try:
        if geo_lists:
            for i, geo_list in enumerate(geo_lists):
                area_id = geo_list['area_id']
                area_name = geo_list['area_name']
                area_type = geo_list['area_type_id']
                if geo_filter == area_type:
                    if user_filter:
                        if area_id in user_filter:
                            area_detail[area_id] = area_name
                    else:
                        area_detail[area_id] = area_name
            result = area_detail.items()
    except Exception, e:
        raise e
    else:
        return result


def org_unit_type_filter(queryset, passed_in_org_types):
    """Get specific Organisational units based on a filter."""
    for passed_in_org_type in passed_in_org_types:
        queryset = queryset.filter(org_unit_type_id=passed_in_org_type)
    return queryset


def search_org_units(unit_types, is_closed):
    """Search function for all Organisational units - no filters."""
    try:
        org_units = RegOrgUnit.objects.all()
        org_units = org_units.filter(is_void=False)
        if not is_closed:
            org_units = org_units.filter(date_closed__isnull=True)
        if unit_types:
            # org_units = org_unit_type_filter(org_units, unit_types)
            org_units = org_units.filter(org_unit_type_id__in=unit_types)
    except Exception, e:
        error = "Error searching org units - %s" % (str(e))
        print error
        return {}
    else:
        return org_units


def get_all_org_units():
    """Get all Organisational units."""
    try:
        org_units = RegOrgUnit.objects.all().values(
            'id', 'org_unit_id_vis', 'org_unit_name')
    except Exception, e:
        error = "Error getting org units - %s" % (str(e))
        print error
        return None
    else:
        return org_units


def get_org_units(initial="Select unit"):
    """Get all Organisational units for drop down."""
    try:
        unit_detail = {'': initial} if initial else {}
        org_units = get_all_org_units()
        for unit in org_units:
            unit_vis = unit['org_unit_id_vis']
            unit_name = unit['org_unit_name']
            unit_detail[unit['id']] = '%s %s' % (unit_vis, unit_name)
    except Exception, e:
        print "error - %s" % (str(e))
        return {}
    else:
        return unit_detail.items()


def save_contacts(contact_id, contact_value, org_unit):
    """Save contacts for Organisational units."""
    try:
        contact, created = RegOrgUnitContact.objects.update_or_create(
            contact_detail_type_id=contact_id, org_unit_id=org_unit,
            defaults={'contact_detail_type_id': contact_id,
                      'contact_detail': contact_value,
                      'org_unit_id': org_unit, 'is_void': False},)
    except Exception, e:
        error = 'Error searching org unit -%s' % (str(e))
        print error
        return None
    else:
        return contact, created


def get_contacts(org_id):
    """Get specific Organisational units contacts from org id."""
    try:
        contact_dict = {}
        contacts = RegOrgUnitContact.objects.filter(
            org_unit_id=org_id, is_void=False).values(
            'contact_detail_type_id', 'contact_detail')
        for contact in contacts:
            contact_type = 'contact_%s' % (contact['contact_detail_type_id'])
            contact_dict[contact_type] = contact['contact_detail']
    except Exception, e:
        error = 'Error searching org unit -%s' % (str(e))
        print error
        return None
    else:
        return contact_dict


def save_external_ids(identifier_id, identifier_value, org_unit):
    """Save Organisational units external ids."""
    try:
        contact, created = RegOrgUnitExternalID.objects.update_or_create(
            identifier_type_id=identifier_id, org_unit_id=org_unit,
            defaults={'identifier_type_id': identifier_id,
                      'identifier_value': identifier_value,
                      'org_unit_id': org_unit, 'is_void': False},)
    except Exception, e:
        error = 'Error searching org unit -%s' % (str(e))
        print error
        return None
    else:
        return contact, created


def get_external_ids(org_id):
    """Get Organisational units ids for specific org id."""
    try:
        ext_ids = RegOrgUnitExternalID.objects.filter(
            org_unit_id=org_id, is_void=False).values(
            'identifier_type_id', 'identifier_value')
    except Exception, e:
        raise e
    else:
        return ext_ids


def perform_audit_persons(org_id):
    """TO DO."""
    try:
        ext_ids = RegOrgUnitExternalID.objects.filter(
            org_unit_id=org_id, is_void=False).values(
            'identifier_type_id', 'identifier_value')
    except Exception, e:
        raise e
    else:
        return ext_ids


def save_geo_location(area_ids, org_unit, existing_ids=[]):
    """Save Organisational units geo locations."""
    try:
        date_linked = datetime.now().strftime("%Y-%m-%d")
        # Delink those unselected by user
        area_ids = map(int, area_ids)
        delink_list = [x for x in existing_ids if x not in area_ids]
        for i, area_id in enumerate(area_ids):
            if area_id not in delink_list:
                geo, created = RegOrgUnitGeography.objects.update_or_create(
                    area_id=area_id, org_unit_id=org_unit,
                    defaults={'date_linked': date_linked, 'is_void': False},)
        if delink_list:
            for i, area_id in enumerate(delink_list):
                geo, created = RegOrgUnitGeography.objects.update_or_create(
                    area_id=area_id, org_unit_id=org_unit,
                    defaults={'date_delinked': date_linked, 'is_void': True},)
    except Exception, e:
        error = 'Error linking area to org unit -%s' % (str(e))
        print error
        return None
    else:
        return True


def get_geo_location(org_id):
    """Get specific Organisational units location based on org id."""
    try:
        ext_ids = RegOrgUnitGeography.objects.filter(
            org_unit_id=org_id, is_void=False).values('area_id')
    except Exception, e:
        raise e
    else:
        return ext_ids


def close_org_unit(close_date, org_unit_id):
    """Close Organisational units based on org id."""
    try:
        if not close_date:
            close_date = datetime.now().strftime("%Y-%m-%d")
        org_unit = get_object_or_404(RegOrgUnit, pk=org_unit_id)
        org_unit.date_closed = close_date
        org_unit.save(update_fields=["date_closed"])
    except Exception, e:
        raise e
    else:
        pass


def set_person_dead(date_of_death, person_id):
    """Mark person as dead based on person id."""
    try:
        if not date_of_death:
            date_of_death = datetime.now().strftime("%Y-%m-%d")
        person_detail = get_object_or_404(RegPerson, pk=person_id)
        person_detail.date_of_death = date_of_death
        person_detail.save(update_fields=["date_of_death"])
    except Exception, e:
        raise e


def delete_org_unit(org_unit_id):
    """Mark as void an Organisational unit."""
    try:
        org_unit = get_object_or_404(RegOrgUnit, pk=org_unit_id)
        org_unit.is_void = True
        org_unit.save(update_fields=["is_void"])
    except Exception, e:
        raise e


def delete_person(person_id):
    """Mark as void a person."""
    try:
        person_detail = get_object_or_404(RegPerson, pk=person_id)
        person_detail.is_void = True
        person_detail.save(update_fields=["is_void"])
    except Exception, e:
        raise e


def new_guid_32():
    """Method to generate guid with dashes removed."""
    return str(uuid.uuid1()).replace('-', '')


def org_id_generator(modelid):
    """Method for generating org unit id."""
    uniqueid = '%05d' % modelid
    checkdigit = calculate_luhn(str(uniqueid))
    return organisation_id_prefix + str(uniqueid) + str(checkdigit)


def luhn_checksum(check_number):
    """http://en.wikipedia.org/wiki/Luhn_algorithm ."""
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
    """http://en.wikipedia.org/wiki/Luhn_algorithm ."""
    return luhn_checksum(check_number) == 0


def calculate_luhn(partial_check_number):
    """http://en.wikipedia.org/wiki/Luhn_algorithm ."""
    check_digit = luhn_checksum(int(partial_check_number) * 10)
    return check_digit if check_digit == 0 else 10 - check_digit


def get_client_ip(request):
    """Get IP address for both ajax and normal requests."""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def get_meta_data(request):
    """Method to get meta data."""
    try:
        meta_info = {}
        user_agent = request.META.get('HTTP_USER_AGENT', '')
        meta_info['browser'] = user_agent
        # Compress this text
        content = json.dumps(meta_info, separators=(',', ':'))
        return str(content)
    except Exception:
        return None


def check_duplicate(person_uid):
    """Method to check duplicates."""
    try:
        person = PersonsMaster(id=person_uid)
        person.save()
    except Exception as e:
        print 'error in duplicate page check - %s' % (str(e))
        return None
    else:
        return person


def search_person_ft(request, search_string, ptype, incl_dead):
    """Method to search for persons."""
    try:
        cids = []
        reg_ovc = request.session.get('reg_ovc', 0)
        names = search_string.split()
        person_type = str(ptype)
        p_type = person_type
        other_filter = ''
        if person_type == 'TBVC':
            person_type = 'COVC'
            other_filter = "OR designation = 'TBVC'"
        if p_type == 'TBVC':
            query = ("SELECT id FROM reg_person WHERE to_tsvector"
                     "(first_name || ' ' || surname || ' '"
                     " || COALESCE(other_names,''))"
                     " @@ to_tsquery('english', '%s') AND (designation = '%s'%s)"
                     " ORDER BY date_of_birth DESC")
            vals = ' & '.join(names)
            sql = query % (vals, person_type, other_filter)
        else:
            # Other than OVC
            query = ("SELECT reg_person.id as id FROM reg_person INNER JOIN reg_persons_types "
                     " ON reg_person.id=person_id AND person_type_id = '%s' WHERE to_tsvector"
                     "(first_name || ' ' || surname || ' '"
                     " || COALESCE(other_names,''))"
                     " @@ to_tsquery('english', '%s') "
                     " ORDER BY date_of_birth DESC")
            vals = ' & '.join(names)
            sql = query % (p_type, vals)
        print sql
        with connection.cursor() as cursor:
            cursor.execute(sql)
            rows = cursor.fetchall()
            cids = [r[0] for r in rows]
        qs = RegPerson.objects.filter(is_void=False, id__in=cids)
        if reg_ovc and person_type == 'COVC':
            cbo_ovcs = get_org_ovcs(request)
            qs = qs.filter(id__in=cbo_ovcs)
    except Exception as e:
        print 'error doing fts search - %s' % (str(e))
        return []
    else:
        return qs


def get_org_ovcs(request):
    """Get children for the Org unit."""
    try:
        # OVC Filters
        cbo_id = request.session.get('ou_primary', 0)
        cbo_ids = request.session.get('ou_attached', [])
        # All linked CBOS
        org_id = int(cbo_id)
        org_ids = get_orgs_child(org_id)
        if cbo_ids:
            cbos_list = [int(cbo_str) for cbo_str in cbo_ids.split(',')]
            org_ids = org_ids + cbos_list
        if request.user.is_superuser:
            regs = OVCRegistration.objects.filter(is_void=False)
        else:
            regs = OVCRegistration.objects.filter(
                is_void=False, child_cbo_id__in=org_ids)
        # Get OVC ids
        child_ids = regs.values_list('person_id', flat=True)
    except Exception as e:
        print 'Get getting Org OVCs - %s' % (str(e))
        return []
    else:
        return child_ids
