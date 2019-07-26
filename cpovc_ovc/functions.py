"""OVC common methods."""
import requests
import json
import schedule
import time
from datetime import datetime
from django.utils import timezone
from django.conf import settings
from django.shortcuts import get_object_or_404
from django.shortcuts import get_list_or_404
from django.db.models import Q
from django.db import connection
from django.db import IntegrityError, transaction
from .models import (
    OVCRegistration, OVCHouseHold, OVCHHMembers, OVCHealth, OVCEligibility,
    OVCFacility, OVCSchool, OVCEducation, OVCExit, OVCViralload)
from cpovc_registry.models import (
    RegPerson, RegOrgUnit, RegPersonsTypes, OVCCheckin)
from cpovc_main.functions import convert_date
from cpovc_registry.functions import (
    extract_post_params, save_person_extids, get_attached_ous,
    get_orgs_child)


def get_checkins(user_id):
    """Method to get all checkins."""
    try:
        chs, cnt = '', 0
        checkins = OVCCheckin.objects.filter(
            user_id=user_id).order_by("-timestamp_created")
        cins = []
        for checkin in checkins:
            cnt += 1
            time_diff = get_timediff(checkin.timestamp_created)
            t_diff = '%s ago' % (time_diff)
            chs = '<a href="/ovcare/ovc/view/%s/">' % (checkin.person_id)
            chs += '<button type="button" class="btn btn-primary">'
            chs += ' View OVC</button></a>'
            chs += ' <button type="button" class="btn btn-danger'
            chs += ' removecheckin" id="%s">' % (checkin.person_id)
            chs += ' Remove</button></a>'
            chd = {'ovc_id': checkin.person_id, 'ctime': t_diff,
                   'ovc_name': checkin.person.full_name, 'caction': chs}
            cins.append(chd)
    except Exception as e:
        print 'error getting checkins - %s' % (str(e))
        return "", 0
    else:
        return cins, cnt


def get_school(ovc_id):
    """Method to get school details."""
    try:
        school = OVCEducation.objects.get(person_id=ovc_id, is_void=False)
    except Exception as e:
        print 'No school details - %s' % (str(e))
        return None
    else:
        return school


def get_health(ovc_id):
    """Method to get health details."""
    try:
        health = OVCHealth.objects.get(person_id=ovc_id)
    except Exception as e:
        print 'No health details - %s' % (str(e))
        return None
    else:
        return health


def search_ovc(request):
    """Method to search OVC as per USG."""
    try:
        ous = []
        name = request.POST.get('search_name')
        criteria = request.POST.get('search_criteria')
        exited = request.POST.get('person_exited')
        is_exited = True if exited else False
        # Limit permissions
        aous = get_attached_ous(request)
        ous = get_orgs_child(aous, 1)
        cid = int(criteria)
        cbos, pids, chvs = [], [], []
        designs = ['COVC', 'CGOC']
        if cid in [2, 3, 4]:
            queryset = None
        else:
            queryset = RegPerson.objects.filter(
                is_void=False, designation__in=designs)
        field_names = ['surname', 'first_name', 'other_names']
        q_filter = Q()
        # 1: Names, 2: HH, 3: CHV, 4: CBO
        names = name.split()
        cids = []
        if cid == 0:
            for nm in names:
                for field in field_names:
                    q_filter |= Q(**{"%s__icontains" % field: name})
                pids = queryset.filter(q_filter).values_list(
                    'id', flat=True)
        elif cid == 1:
            pids = []
            query = ("SELECT id FROM reg_person WHERE to_tsvector"
                     "(first_name || ' ' || surname || ' '"
                     " || COALESCE(other_names,''))"
                     " @@ to_tsquery('english', '%s') AND is_void=False"
                     " ORDER BY date_of_birth DESC")
            # " OFFSET 10 LIMIT 10")
            vals = ' & '.join(names)
            sql = query % (vals)
            print sql
            with connection.cursor() as cursor:
                cursor.execute(sql)
                row = cursor.fetchall()
                pids = [r[0] for r in row]
            # print 'cids', pids
        elif cid == 2:
            pids = OVCHHMembers.objects.filter(
                is_void=False,
                house_hold__head_identifier__iexact=name).values_list(
                'person_id', flat=True)
        elif cid == 3:
            chv_ids = RegPersonsTypes.objects.filter(
                is_void=False, person_type_id='TWVL').values_list(
                'person_id', flat=True)
            queryset = RegPerson.objects.filter(
                is_void=False, id__in=chv_ids)
            for nm in names:
                for field in field_names:
                    q_filter |= Q(**{"%s__icontains" % field: nm})
            chvs = queryset.filter(q_filter).values_list(
                'id', flat=True)
        elif cid == 4:
            cbos = RegOrgUnit.objects.filter(
                is_void=False, org_unit_name__icontains=name).values_list(
                'id', flat=True)
        elif cid == 5:
            query = ("SELECT id FROM reg_person WHERE to_tsvector"
                     "(first_name || ' ' || surname || ' ' || other_names)"
                     " @@ to_tsquery('english', '%s') AND designation = 'CCGV'"
                     " ORDER BY date_of_birth DESC")
            vals = ' & '.join(names)
            sql = query % (vals)
            with connection.cursor() as cursor:
                cursor.execute(sql)
                row = cursor.fetchall()
                cids = [r[0] for r in row]
        else:
            for nm in names:
                for field in field_names:
                    q_filter |= Q(**{"%s__icontains" % field: name})
                pids = queryset.filter(q_filter).values_list(
                    'id', flat=True)
        # Query ovc table
        if is_exited:
            qs = OVCRegistration.objects.filter(is_void=False)
        else:
            qs = OVCRegistration.objects.filter(
                is_void=False, is_active=True)
        if not request.user.is_superuser:
            qs = qs.filter(child_cbo_id__in=ous)
        pst, plen = 0, 1000
        if cbos:
            ovcs = qs.filter(child_cbo_id__in=cbos)[pst:plen]
        elif chvs:
            ovcs = qs.filter(child_chv_id__in=chvs)[pst:plen]
        elif cids:
            ovcs = qs.filter(caretaker_id__in=cids)[pst:plen]
        else:
            ovcs = qs.filter(person_id__in=pids)[pst:plen]
    except Exception, e:
        print 'Error searching for OVC - %s' % (str(e))
        return {}
    else:
        return ovcs


def search_master(request):
    """Method to query existing customers."""
    try:
        results = []
        query_id = int(request.GET.get('id'))
        query = request.GET.get('q')
        school_level = request.GET.get('level')
        # Filters for external ids
        if query_id == 1:
            agents = OVCFacility.objects.filter(
                facility_name__icontains=query)
            for agent in agents:
                name = agent.facility_name
                agent_id = agent.id
                val = {'id': agent_id, 'label': name,
                       'value': name}
                results.append(val)
        elif query_id == 2:
            agents = OVCSchool.objects.filter(
                school_name__icontains=query,
                school_level=school_level)
            for agent in agents:
                name = agent.school_name
                agent_id = agent.id
                val = {'id': agent_id, 'label': name,
                       'value': name}
                results.append(val)
    except Exception, e:
        print 'error searching master list - %s' % (str(e))
        return []
    else:
        return results


def get_hh_members(ovc_id):
    """Method to get child chv details."""
    try:
        ovc_detail = get_object_or_404(
            OVCHHMembers, person_id=ovc_id, is_void=False)
    except Exception, e:
        print 'error getting ovc hh members - %s' % (str(e))
        return {}
    else:
        return ovc_detail


def get_ovcdetails(ovc_id):
    """Method to get child chv details."""
    try:
        ovc_detail = get_object_or_404(
            OVCRegistration, person_id=ovc_id, is_void=False)
    except Exception, e:
        print 'error getting ovc details - %s' % (str(e))
        return {}
    else:
        return ovc_detail


def ovc_registration(request, ovc_id, edit=0):
    """Method to complete ovc registration."""
    try:
        min_date = convert_date('01-Jan-1900')
        reg_date = request.POST.get('reg_date')
        reg_date = convert_date(reg_date)
        if reg_date < min_date:
            reg_date = min_date
        bcert = request.POST.get('has_bcert')
        disabled = request.POST.get('disb')
        hh_members = request.POST.getlist('hh_member')
        cbo_id = request.POST.get('cbo_id')
        has_bcert = True if bcert else False
        is_disabled = True if disabled else False

        bcert_no = request.POST.get('bcert_no')
        ncpwd_no = request.POST.get('ncpwd_no')
        ext_ids = {}
        if bcert_no:
            ext_ids['ISOV'] = bcert_no
        if ncpwd_no:
            ext_ids['IPWD'] = ncpwd_no
        if ext_ids:
            save_person_extids(ext_ids, ovc_id)

        hiv_status = request.POST.get('hiv_status')
        immmune = request.POST.get('immunization')
        org_uid = request.POST.get('cbo_uid')
        org_uid_check = request.POST.get('cbo_uid_check')
        caretaker = request.POST.get('caretaker')
        school_level = request.POST.get('school_level')
        is_exited = request.POST.get('is_exited')
        exit_reason = request.POST.get('exit_reason')
        criterias = request.POST.getlist('eligibility')
        exit_date = datetime.now().strftime("%Y-%m-%d")
        ovc_detail = get_object_or_404(OVCRegistration, person_id=ovc_id)
        # HIV status update only if unknown
        if edit == 0:
            edit_hiv = True
            cbo_uid = gen_cbo_id(cbo_id, ovc_id)
            org_cid = cbo_uid if org_uid == org_uid_check else org_uid
            ovc_detail.hiv_status = str(hiv_status)
        else:
            org_cid = org_uid
            nhiv_status = str(hiv_status)
            edit_hiv = False
            if ovc_detail.hiv_status == 'HSKN':
                edit_hiv = True
                ovc_detail.hiv_status = nhiv_status
            elif ovc_detail.hiv_status == 'HSTN' and nhiv_status == 'HSTP':
                edit_hiv = True
                ovc_detail.hiv_status = nhiv_status
            elif ovc_detail.hiv_status == 'HSTP' and nhiv_status == 'HSTN':
                if request.user.is_staff:
                    edit_hiv = True
                    ovc_detail.hiv_status = nhiv_status
            elif ovc_detail.hiv_status == 'HSTP' and nhiv_status == 'HSTP':
                edit_hiv = True
                ovc_detail.hiv_status = nhiv_status
            elif ovc_detail.hiv_status == 'XXXX' or not ovc_detail.hiv_status:
                edit_hiv = True
                ovc_detail.hiv_status = nhiv_status
        is_active = False if is_exited else True
        ovc_detail.registration_date = reg_date
        ovc_detail.has_bcert = has_bcert
        ovc_detail.is_disabled = is_disabled
        ovc_detail.immunization_status = str(immmune)
        ovc_detail.org_unique_id = org_cid
        ovc_detail.caretaker_id = caretaker
        ovc_detail.school_level = school_level
        ovc_detail.is_active = is_active
        ovc_detail.exit_reason = exit_reason
        if exit_reason:
            ovc_detail.exit_date = exit_date
        ovc_detail.save(
            update_fields=["registration_date", "has_bcert", "is_disabled",
                           "immunization_status", "org_unique_id",
                           "caretaker_id", "school_level", "hiv_status",
                           "is_active", "exit_reason", "exit_date"])
        # Update eligibility
        OVCEligibility.objects.filter(person_id=ovc_id).update(is_void=True)
        for criteria_id in criterias:
            eligibility, created = OVCEligibility.objects.update_or_create(
                person_id=ovc_id, criteria=criteria_id, is_void=False,
                defaults={'person_id': ovc_id, 'criteria': criteria_id},)
        # Update Health status
        if hiv_status == 'HSTP' and edit_hiv:
            facility = request.POST.get('facility_id')
            art_status = request.POST.get('art_status')
            link_date = request.POST.get('link_date')
            date_linked = convert_date(link_date)
            ccc_no = request.POST.get('ccc_number')
            if facility and art_status and date_linked and ccc_no:
                health, created = OVCHealth.objects.update_or_create(
                    person_id=ovc_id,
                    defaults={'person_id': ovc_id,
                              'facility_id': facility,
                              'art_status': art_status,
                              'date_linked': date_linked, 'ccc_number': ccc_no,
                              'is_void': False},)
        # Update School details
        if school_level != 'SLNS':
            school_id = request.POST.get('school_id')
            school_class = request.POST.get('school_class')
            school_adm = request.POST.get('admission_type')
            if school_id and school_class and school_adm:
                OVCEducation.objects.filter(person_id=ovc_id).update(is_void=True)
                health, created = OVCEducation.objects.update_or_create(
                    person_id=ovc_id, school_class=school_class,
                    defaults={'person_id': ovc_id,
                              'school_id': school_id,
                              'school_level': school_level,
                              'school_class': school_class,
                              'admission_type': school_adm,
                              'is_void': False},)
        cgs = extract_post_params(request, naming='cg_')
        hhrs = extract_post_params(request, naming='hhr_')
        # Alive status, HIV status and Death cause for Guardian
        ast = extract_post_params(request, naming='astatus_')
        hst = extract_post_params(request, naming='gstatus_')
        cst = extract_post_params(request, naming='cstatus_')
        # Alive status, HIV status and Death cause for Sibling
        sast = extract_post_params(request, naming='sastatus_')
        shst = extract_post_params(request, naming='sgstatus_')
        todate = timezone.now()
        if edit == 0:
            # Create House Hold and populate members
        
            # caretaker_id = int(cgs[caretaker][0])
            # hhid=get_house_hold(caretaker_id)
            caretaker_id = int(caretaker)
            hhid = get_first_household(caretaker_id)

            print("CareTaker ID--->", caretaker_id)
            print("HouseHold ID-->", hhid)
            if not hhid:
                print("I don't have household ID.")
                new_hh=OVCHouseHold(
                    head_person_id=caretaker,
                    head_identifier=caretaker_id
                )
                new_hh.save()
                hh_id=new_hh.pk
                # Duplicate Fix
                # new_hh = OVCHouseHold(
                # head_person_id=caretaker,
                # head_identifier=caretaker_id),
                # new_hh.save()
                # hh_id = new_hh.pk

            else:
                print("I do have household ID.")
                hh_id=hhid.id
                print(hh_id)
            # Add members to HH
            hh_members.append(ovc_id)
            for hh_m in hh_members:
                oid = int(ovc_id)
                hh_head = True if int(hh_m) == caretaker_id else False
                m_type = hhrs[hh_m][0] if hh_m in hhrs else 'TBVC'
                member_type = 'TOVC' if oid == int(hh_m) else m_type
                if member_type == 'TBVC' or member_type == 'TOVC':
                    hh_hiv = shst[hh_m][0] if hh_m in shst else None
                    hh_alive = sast[hh_m][0] if hh_m in sast else 'AYES'
                    hh_death = None
                else:
                    hh_hiv = hst[hh_m][0] if hh_m in hst else None
                    hh_alive = ast[hh_m][0] if hh_m in ast else 'AYES'
                    hh_death = cst[hh_m][0] if hh_m in cst else None
                if oid == hh_m:
                    hh_hiv, hh_alive, hh_death = hiv_status, 'AYES', None

                membership=get_hh_members(hh_m)
                print 'membership', membership
                if not membership:
                    OVCHHMembers(
                        house_hold_id=hh_id, person_id=hh_m,
                        hh_head=hh_head, member_type=member_type,
                        death_cause=hh_death, member_alive=hh_alive,
                        hiv_status=hh_hiv, date_linked=todate).save()
        else:
            # Update HH details
            hhid = request.POST.get('hh_id')
            # caretaker_id = cgs[caretaker][0]
            caretaker_id = int(caretaker) # Fix
            hh_detail = get_object_or_404(OVCHouseHold, id=hhid)
            hh_detail.head_person_id = caretaker
            hh_detail.head_identifier = caretaker_id
            hh_detail.save(update_fields=["head_identifier", "head_person"])
            # Update HH Members
            for hh_m in hhrs:
                oid = int(ovc_id)
                hh_head = True if hh_m == caretaker else False
                member_type = hhrs[hh_m][0]
                if member_type == 'TBVC' or member_type == 'TOVC':
                    hh_hiv = shst[hh_m][0] if hh_m in shst else None
                    hh_alive = sast[hh_m][0] if hh_m in sast else 'AYES'
                    hh_death = None
                else:
                    hh_hiv = hst[hh_m][0] if hh_m in hst else None
                    hh_alive = ast[hh_m][0] if hh_m in ast else 'AYES'
                    hh_death = cst[hh_m][0] if hh_m in cst else None
                if oid == hh_m:
                    hh_hiv, hh_alive, hh_death = hiv_status, 'AYES', None
                hhm, created = OVCHHMembers.objects.update_or_create(
                    person_id=hh_m, house_hold_id=hhid,
                    defaults={'person_id': hh_m, 'hh_head': hh_head,
                              'member_type': member_type, 'is_void': False,
                              'death_cause': hh_death,
                              'member_alive': hh_alive,
                              'date_linked': todate, 'hiv_status': hh_hiv},)
    except Exception, e:
        print 'Error updating OVCID:%s - %s' % (ovc_id, str(e))
        pass
    else:
        pass


def get_timediff(create_time):
    """Get time differences."""
    tnow = timezone.now()

    td = tnow - create_time
    days = td.days
    hours = td.seconds // 3600
    minutes = (td.seconds // 60) % 60
    if days > 0:
        return '%s days' % (days)
    elif hours > 0:
        return '%s hours' % (hours)
    else:
        return '%s minutes' % (minutes)


def gen_cbo_id(cbo_id, ovc_id):
    """Invoice validations."""
    try:
        last_id = OVCRegistration.objects.filter(
            child_cbo_id=cbo_id).exclude(org_unique_id__isnull=True).order_by(
                'org_unique_id').last()
        if not last_id:
            return '00001'
        lid = last_id.org_unique_id
        if lid and lid.isnumeric():
            new_id = str(int(lid) + 1).zfill(5)
        else:
            if lid:
                new_id = '%sX' % (lid[:-1])
            else:
                '0000X'
        return new_id
    except Exception, e:
        raise e
    else:
        pass


def get_house_hold(person_id):
    """Method to get household id."""
    try:
        hh_detail = get_object_or_404(
            OVCHouseHold, head_person_id=person_id)
        print("Get HouseHold Function Detail->",hh_detail);
    except Exception as e:
        print 'error getting hh - %s' % (str(e))
        return None
    else:
        print("Return GetHouseHold Func", hh_detail)
        return hh_detail

def get_first_household(person_id):
    """A fix for duplication-Method to get household list and return just one """
    try:
        hh_details = get_list_or_404(
            OVCHouseHold, head_person_id=person_id)
        hh_detail = hh_details[-1]  # Gets the last item in the list  (First household)
    except Exception as e:
        print 'error getting hh - %s' % (str(e))
        return None
    else:
        return hh_detail  # Return only one household

def get_hh_membership(person_id):
    try:
        member=get_object_or_404(OVCHHMembers, person_id=person_id)

    except Exception as e:
        return None

    else:
        return member

def manage_checkins(request, gid=0):
    """Method to handle checkins."""
    try:
        chs, ovc_ids = '', []
        org_unit_id = None
        ovcid = request.POST.get('ovc_id')
        aid = request.POST.get('id')
        ovcids = request.POST.getlist('ovc_id[]')
        act_id = int(aid) if aid else 0
        action_id = gid if gid else act_id
        user_id = request.user.id
        if ovcid:
            ovc_ids = [ovcid]
        elif ovcids:
            ovc_ids = ovcids
        if action_id == 1:
            if 'ou_primary' in request.session:
                ou_id = request.session['ou_primary']
                org_unit_id = int(ou_id) if ou_id else None
            cnt = 0
            for ovc_id in ovc_ids:
                cnt += 1
                checkin, created = OVCCheckin.objects.update_or_create(
                    person_id=ovc_id, user_id=user_id,
                    defaults={'person_id': ovc_id, 'user_id': user_id,
                              'org_unit_id': org_unit_id},)
            msg = 'OVC (%s) checked in successfully.' % (str(cnt))
        elif action_id == 2:
            chs, cnt = get_checkins(user_id)
            msg = 'OVC checked in returned %s results.' % (cnt)
        elif action_id == 3:
            ovcid = request.POST.get('ovc_out_id')
            # chs, cnt = get_checkins(user_id)
            ovcs = OVCCheckin.objects.filter(person_id=ovcid)
            for ovc in ovcs:
                ovc.delete()
            msg = 'OVC checked out successfully.'
    except Exception as e:
        print 'error handling checkins - %s' % (str(e))
        return msg, 0
    else:
        return msg, chs


def ovc_management(request):
    try:
        action_id = int(request.POST.get('action'))
        if action_id == 2:
            perform_exit(request)
        elif action_id == 3:
            save_viral_load(request)
    except Exception as e:
        raise e
    else:
        pass


def perform_exit(request):
    try:
        ovcid = request.POST.get('ovc_id')
        exit_date = convert_date(request.POST.get('exit_date'))
        exit_reason = request.POST.get('exit_reason')
        exit_org_name = request.POST.get('exit_org_name')
        #
        ovc_details = OVCRegistration.objects.get(person_id=ovcid)
        ovc_details.exit_date = exit_date
        ovc_details.exit_reason = exit_reason
        if exit_org_name:
            # ovc_details.exit_org_name = exit_org_name
            org, created = OVCExit.objects.update_or_create(
                person_id=ovcid,
                defaults={'person_id': ovcid, 'org_unit_name': exit_org_name},)
        ovc_details.is_active = False
        ovc_details.save(
            update_fields=["exit_date", "exit_reason", "is_active"])
    except Exception as e:
        print 'error exiting - %s' % (str(e))
        raise e
    else:
        pass


def get_exit_org(ovc_id):
    """Method to get exit organization."""
    try:
        org = OVCExit.objects.get(is_void=False, person_id=ovc_id)
    except Exception as e:
        print 'No org details - %s' % (str(e))
        return ''
    else:
        return org.org_unit_name


def save_viral_load(request):
    try:
        ovcid = request.POST.get('ovc_id')
        viral_date = convert_date(request.POST.get('viral_date'))
        ldl = request.POST.get('ldl')
        viral_value = request.POST.get('viral_value')
        viral_load = None if ldl == 'true' else viral_value
        # OVC Viral load
        org, created = OVCViralload.objects.update_or_create(
            person_id=ovcid, viral_date=viral_date,
            defaults={'person_id': ovcid, 'viral_load': viral_load},)
    except Exception as e:
        print 'error exiting - %s' % (str(e))
        raise e
    else:
        pass


def method_once(method):
    "A decorator that runs a method only once."
    attrname = "_%s_once_result" % id(method)
    def decorated(self, *args, **kwargs):
        try:
            return getattr(self, attrname)
        except AttributeError:
            setattr(self, attrname, method(self, *args, **kwargs))
            return getattr(self, attrname)
    return decorated


class UpdateViralLoad(object):
	"""docstring for UpdateViralLoad"""
	def __init__(self):
		self.api_url_base = settings.NASCOP_API_BASE_URL
		self.login_url = settings.NASCOP_LOGIN_URL
		self.email = settings.NASCOP_EMAIL
		self.password = settings.NASCOP_PASSWORD
		self.empty_viral_loads_list = self.query_ccc_number_facility()
		self.api_token = self.generate_token()  # Holds the api token

		# def check_for_viral_load():
		# # filter empty viral loads
		# empty_viral_loads = OVCViralload.objects.filter(viral_load__isnull=True).count()
		# viral_load_record = 
		# pass


	def get_date_n_patient_id(self):
		# get date n patient_id(ccc_number)
		empty_viral_loads = OVCViralload.objects.values("viral_date","person_id").filter(viral_load__isnull=True)
		for record in empty_viral_loads:
			viral_date = record["viral_date"]
			person_id = record["person_id"]
			personid_vldate = (person_id, viral_date)
			empty_viral_loads_list.append(personid_vldate)

			# return empty_viral_loads_list


	def query_ccc_number_facility(self):
		cursor = connection.cursor()
		cursor.execute("SELECT ccc_number, facility_code, ovc_viral_load.person_id FROM eid, ovc_viral_load WHERE eid.person_id = ovc_viral_load.person_id AND ovc_viral_load.viral_load IS NULL;")
		empty_viral_load_list = cursor.fetchall()

		return empty_viral_load_list

    @method_once
	def generate_token(self):
		headers = {'Content-Type': 'application/x-www-form-urlencoded'}
		credentials = { "email": self.email, "password": self.password }
		response = requests.post(self.login_url, headers=headers, data=credentials)

		if response.status_code == 200:
			json_token = json.loads(response.content)
			print(json.loads(response.content.decode('utf-8')))
			api_token = json_token.get('token')
			return api_token
		else:
			print(response)


	def get_viral_load(self, facility, patientID):
		headers = {'Authorization': 'Bearer {0}'.format(self.api_token)}
		api_url = '{0}{1}/{2}'.format(self.api_url_base, facility, patientID)
		response = requests.get(api_url, headers=headers)

		if response.status_code == 200:
			json_object = json.loads(response.content)
			data_list = []
			for test in json_object:
				patient = test.get('PatientID')
				date_tested = test.get('DateTested')
				result = test.get('Result')
				data = (patient, date_tested, result)
				print("The details are: {0}, {1}, {2}".format(patient, date_tested, result))
				data_list.append(data)
			print(data_list)
			return data_list
		elif response.status_code == 404:
			print('[!] [{0}] URL not found: [{1}]'.format(response.status_code,api_url))
			return None
		elif response.status_code == 401:
			print('[!] [{0}] Authentication Failed'.format(response.status_code), response.content)
			return None
		elif response.status_code == 400:
			print('[!] [{0}] Bad Request'.format(response.status_code), response.content)
			return None
		elif response.status_code >= 300:
			print('[!] [{0}] Unexpected Redirect'.format(response.status_code), response.content)
			return None
		elif response.status_code >= 500:
			print('[!] [{0}] Server Error'.format(response.status_code), response.content)
			return None
		else:
			print('[?] Unexpected Error: [HTTP {0}]: Content: {1}'.format(response.status_code, response.content))
			return None

	def loop_through_data(self):
		try:
			data=self.empty_viral_loads_list
			for row in data:
				facility_code = row[1]
				ccc_number = row[0]
				person_id = row[2]
				facility_code_ccc = (facility_code, ccc_number)
				print(facility_code_ccc)
				viral_load_records = self.get_viral_load(facility_code, ccc_number)
				if viral_load_records:
					for record in viral_load_records:
						date_tested = record[1]
						result = record[2]
						person_id_date_tested = str(person_id) + '-' + str(date_tested)
						# if person_id_date_tested == concat_personid_date(person_id):
						# 	update
						self.update_table(result, person_id_date_tested)

					# viral_load_list.append(viral_load_records)
					# return viral_load_list
		except Exception as e:
			print 'error exiting - %s' % (str(e))
			raise e
		else:
			pass

	# def concat_personid_date(self, person_id):
	# 	from django.db.models import CharField, Value as V
	# 	from django.db.models.functions import Concat
	# 	person_date = OVCViralload.objects.annotate(personid_date=Concat('person_id', V('-'), 'viral_date',output_field=CharField())).get(person_id=410373)
	# 	return person_date.personid_date

	def update_table(self, new_viral_load, id_n_date):
	    try:
	        cursor = connection.cursor()
	        print("Table Before updating record ")
	        sql_select_query = """SELECT * FROM ovc_viral_load_view WHERE id_n_date = %s"""
	        cursor.execute(sql_select_query, (id_n_date, ))
	        record = cursor.fetchone()
	        print(record)
	        # Update single record now
	        sql_update_query = """UPDATE ovc_viral_load_view SET viral_load_2 = %s WHERE id_n_date = %s"""
	        cursor.execute(sql_update_query, (new_viral_load, id_n_date))
	        connection.commit()
	        count = cursor.rowcount
	        print(count, "Record Updated successfully ")
	        print("Table After updating record ")
	        sql_select_query = """SELECT * FROM ovc_viral_load_view WHERE id_n_date = %s"""
	        cursor.execute(sql_select_query, (id_n_date,))
	        record = cursor.fetchone()
	        print(record)
	    except (Exception, psycopg2.Error) as error:
	        print("Error in update operation", error)


class KMHFLFacilities(object):
    '''
        Auto-update the list of facilities from KMHFL
    '''

    def __init__(self):
        self.username = settings.KMHFL_USERNAME
        self.password = settings.KMHFL_PASSWORD
        self.scope = settings.KMHFL_SCOPE
        self.grant_type = settings.KMHFL_GRANT_TYPE
        self.client_id = settings.KMHFL_CLIENTID
        self.client_secret = settings.KMHFL_CLIENT_SECRET
        self.api_base_url = settings.KMHFL_API_BASE_URL
        self.facility_base_url = settings.KMHFL_FACILITY_BASE_URL
        self.login_url = settings.KMHFL_LOGIN_URL
        self.api_token = self.generate_token()
        self.latest_facility = self.latest_facility()

    @method_once
    def latest_facility(self):
        # query latest facility from db
        latest_mfl_code = OVCFacility.objects.values("facility_code").exclude(facility_code__regex=r'[^0-9]').order_by('facility_code').last()
        return latest_mfl_code["facility_code"]

    @method_once
    def generate_token(self):
        # generate token.
        login_url = self.login_url
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        auth = (self.client_id, self.client_secret)
        credentials = { "grant_type": self.grant_type, 
                        "username": self.username, 
                        "password": self.password, 
                        "scope": self.scope }
        response = requests.post(login_url, headers=headers, data=credentials, auth=auth)
        if response.status_code == 200:
            json_token = json.loads(response.content)
            api_token = json_token.get('access_token')
            return api_token
        else:
            print(response.content)
    

    def get_facilities(self):
        # request for facilities
        headers = {'Authorization': 'Bearer {0}'.format(self.api_token)}
        api_url = '{0}facilities/facilities/?format=json'.format(self.api_base_url)
        response = requests.get(api_url, headers=headers)
        
        if response.status_code == 200:
            json_object = json.loads(response.content)
            return json_object
        else:
            print(response.content, api_url)


    def get_subcounty_id(self, facility_id):
        # request facility and get sub-county id.
        headers = {'Authorization': 'Bearer {0}'.format(self.api_token)}
        payload = {'format': 'json'}
        api_url = '{0}{1}'.format(self.facility_base_url, facility_id)
        response = requests.get(api_url, headers=headers, params=payload)
        if response.status_code == 200:
            json_object = json.loads(response.content)
            cpims_subcounty_id = json_object["constituency_code"]
            return cpims_subcounty_id
        else:
            print(response, api_url)

    @transaction.atomic
    def get_newest_facilities(self):
        # loop for new facilities.
        try:
            data = self.get_facilities()
            results = data["results"]
            for facility in results:
                facility_code = facility["code"]
                if facility_code > self.latest_facility:
                    facility_id = facility["id"]
                    cpims_subcounty_id = self.get_subcounty_id(facility_id)
                    facility_name = facility["official_name"]
                    sub_county_id = facility["sub_county_id"]
                    new_facility = OVCFacility(facility_code=facility_code, 
                        facility_name=facility_name, 
                        sub_county_id=cpims_subcounty_id)
                    
                    new_facility.save()
        
        except Exception as e:
            raise e
        else:
            pass

    def schedule_update(self):
        # Update facilities every tuesday at 00:15 am
        schedule.every().tuesday.at("00:15").do(self.get_newest_facilities)

        # # Check for pending schedules
        # while True:
        #     schedule.run_pending()
        #     time.sleep(1)


KMHFLFacilities().schedule_update()