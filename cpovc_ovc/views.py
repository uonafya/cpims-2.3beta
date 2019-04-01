"""OVC Care views."""
from django.shortcuts import render
from django.http import HttpResponseRedirect, JsonResponse
from django.core.urlresolvers import reverse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Q
from datetime import date
from .forms import OVCSearchForm, OVCRegistrationForm
from cpovc_registry.models import (
    RegPerson, RegPersonsGuardians, RegPersonsSiblings, RegPersonsExternalIds)
from cpovc_main.functions import get_dict
from .models import (
    OVCRegistration, OVCHHMembers, OVCEligibility, OVCViralload)
from .functions import (
    ovc_registration, get_hh_members, get_ovcdetails, gen_cbo_id, search_ovc,
    search_master, get_school, get_health, manage_checkins, ovc_management,
    get_exit_org)
from cpovc_auth.decorators import is_allowed_ous
from cpovc_forms.models import OVCCareEvents


@login_required(login_url='/')
def ovc_home(request):
    """Some default page for Server Errors."""
    try:
        rid = 0
        reqid = request.GET.get('id', '')
        offset = request.GET.get('offset', '')
        limit = request.GET.get('limit', '')
        if reqid and offset and limit:
            rid = 2
        if request.method == 'POST' or rid:
            aid = request.POST.get('id')
            act_id = int(aid) if aid else 0
            action_id = rid if rid else act_id
            if action_id in [1, 2, 3]:
                msg, chs = manage_checkins(request, rid)
                results = {'status': 0, 'message': msg, 'checkins': chs}
                if rid == 2:
                    results = chs
                return JsonResponse(results, content_type='application/json',
                                    safe=False)
            elif action_id in [4]:
                msg = 'Record deleted successfully.'
                cid = request.POST.get('cid')
                ovc = OVCRegistration.objects.filter(id=cid).delete()
                results = {'status': 0, 'message': 'Record deleted successfully.'}
                return JsonResponse(results, content_type='application/json',
                                    safe=False)
            form = OVCSearchForm(data=request.POST)
            ovcs = search_ovc(request)

            check_fields = ['sex_id']
            vals = get_dict(field_name=check_fields)

            return render(request, 'ovc/home.html',
                          {'form': form, 'ovcs': ovcs,
                           'vals': vals})
        form = OVCSearchForm()
        return render(request, 'ovc/home.html', {'form': form, 'status': 200})
    except Exception, e:
        raise e


def ovc_search(request):
    """Method to do ovc search."""
    try:
        results = search_master(request)
    except Exception, e:
        print 'error with search - %s' % (str(e))
        return JsonResponse(results, content_type='application/json',
                            safe=False)
    else:
        return JsonResponse(results, content_type='application/json',
                            safe=False)


@login_required(login_url='/')
@is_allowed_ous(['RGM', 'RGU', 'DSU', 'STD'])
def ovc_register(request, id):
    """Some default page for Server Errors."""
    try:
        ovc_id = int(id)
        ovc = get_ovcdetails(ovc_id)
        params, gparams = {}, {}
        initial = {}
        # Details
        child = RegPerson.objects.get(is_void=False, id=id)
        # Get guardians
        guardians = RegPersonsGuardians.objects.filter(
            is_void=False, child_person_id=child.id)
        # Get siblings
        siblings = RegPersonsSiblings.objects.filter(
            is_void=False, child_person_id=child.id)
        print 'p', params, 'gp', gparams
        guids, chids = [], []
        for guardian in guardians:
            guids.append(guardian.guardian_person_id)
        guids.append(child.id)
        for sibling in siblings:
            chids.append(sibling.sibling_person_id)
        pids = {'guids': guids, 'chids': chids}
        print pids
        # Existing
        extids = RegPersonsExternalIds.objects.filter(
            person_id__in=guids)
        for extid in extids:
            if extid.person_id == child.id:
                params[extid.identifier_type_id] = extid.identifier
            else:
                gkey = '%s_%s' % (extid.person_id, extid.identifier_type_id)
                gparams[gkey] = extid.identifier
        if request.method == 'POST':
            form = OVCRegistrationForm(guids=pids, data=request.POST)
            print request.POST
            ovc_registration(request, ovc_id)
            msg = "OVC Registration completed successfully"
            messages.info(request, msg)
            url = reverse('ovc_view', kwargs={'id': ovc_id})
            return HttpResponseRedirect(url)
        else:
            cbo_id = ovc.child_cbo_id
            cbo_uid = gen_cbo_id(cbo_id, ovc_id)
            initial['cbo_uid'] = cbo_uid
            initial['cbo_id'] = cbo_id
            initial['cbo_uid_check'] = cbo_uid
            if 'ISOV' in params:
                initial['bcert_no'] = params['ISOV']
                initial['has_bcert'] = 'on'
            form = OVCRegistrationForm(
                guids=pids, initial=initial)
        # Check users changing ids in urls
        ovc_detail = get_hh_members(ovc_id)
        if ovc_detail:
            msg = "OVC already registered. Visit edit page."
            messages.error(request, msg)
            url = reverse('ovc_view', kwargs={'id': ovc_id})
            return HttpResponseRedirect(url)
        # Class levels
        levels = {}
        levels["SLNS"] = []
        levels["SLEC"] = ["BABY,Baby Class", "MIDC,Middle Class",
                          "PREU,Pre-Unit"]
        levels["SLPR"] = ["CLS1,Class 1", "CLS2,Class 2", "CLS3,Class 3",
                          "CLS4,Class 4", "CLS5,Class 5", "CLS6,Class 6",
                          "CLS7,Class 7", "CLS8,Class 8"]
        levels["SLSE"] = ["FOM1,Form 1", "FOM2,Form 2", "FOM3,Form 3",
                          "FOM4,Form 4", "FOM5,Form 5", "FOM6,Form 6"]
        levels["SLUN"] = ["YER1,Year 1", "YER2,Year 2", "YER3,Year 3",
                          "YER4,Year 4", "YER5,Year 5", "YER6,Year 6"]
        levels["SLTV"] = ["TVC1,Year 1", "TVC2,Year 2", "TVC3,Year 3",
                          "TVC4,Year 4", "TVC5,Year 5"]
        # Re-usable values
        check_fields = ['relationship_type_id']
        vals = get_dict(field_name=check_fields)
        return render(request, 'ovc/register_child.html',
                      {'form': form, 'status': 200, 'child': child,
                       'guardians': guardians, 'siblings': siblings,
                       'vals': vals, 'extids': gparams, 'ovc': ovc,
                       'levels': levels})
    except Exception, e:
        print "error with OVC registration - %s" % (str(e))
        raise e


@login_required(login_url='/')
@is_allowed_ous(['RGM', 'RGU', 'DSU', 'STD'])
def ovc_edit(request, id):
    """Some default page for Server Errors."""
    try:
        ovc_id = int(id)
        date_reg = None
        if request.method == 'POST':
            ovc_registration(request, ovc_id, 1)
            # Save external ids from here
            msg = "OVC Registration details edited successfully"
            messages.info(request, msg)
            url = reverse('ovc_view', kwargs={'id': ovc_id})
            return HttpResponseRedirect(url)
        child = RegPerson.objects.get(is_void=False, id=ovc_id)
        creg = OVCRegistration.objects.get(is_void=False, person_id=ovc_id)
        exit_org_name = get_exit_org(ovc_id)
        bcert = 'on' if creg.has_bcert else ''
        disb = 'on' if creg.is_disabled else ''
        exited = '' if creg.is_active else 'on'
        reg_date = creg.registration_date
        child.caretaker = creg.caretaker_id
        child.cbo = creg.child_cbo.org_unit_name
        child.chv_name = creg.child_chv.full_name
        params = {}
        gparams = {}
        siblings = 0
        # Get house hold
        hhold = OVCHHMembers.objects.get(
            is_void=False, person_id=child.id)
        hhid = hhold.house_hold_id
        hhmqs = OVCHHMembers.objects.filter(
            is_void=False, house_hold_id=hhid).order_by("-hh_head")
        # Viral Load
        vloads = OVCViralload.objects.filter(
            is_void=False, person_id=ovc_id).order_by("-viral_date")
        # add caregivers hiv status
        hhmembers = hhmqs.exclude(person_id=child.id)
        # Get guardians and siblings ids
        guids, chids = [], []
        ctaker = 0
        for hh_member in hhmembers:
            member_type = hh_member.member_type
            member_head = hh_member.hh_head
            if member_head:
                ctaker = hh_member.person_id
            if member_type == 'TBVC' or member_type == 'TOVC':
                chids.append(hh_member.person_id)
                siblings += 1
            else:
                guids.append(hh_member.person_id)
        guids.append(child.id)
        pids = {'guids': guids, 'chids': chids}
        extids = RegPersonsExternalIds.objects.filter(
            person_id__in=guids)
        for extid in extids:
            if extid.person_id == child.id:
                params[extid.identifier_type_id] = extid.identifier
            else:
                gkey = '%s_%s' % (extid.person_id, extid.identifier_type_id)
                gparams[gkey] = extid.identifier
        # Get health information
        ccc_no, date_linked, art_status = '', '', ''
        facility_id, facility = '', ''
        if creg.hiv_status == 'HSTP':
            health = get_health(ovc_id)
            if health:
                ccc_no = health.ccc_number
                date_linked = health.date_linked.strftime('%d-%b-%Y')
                art_status = health.art_status
                facility_id = health.facility_id
                facility = health.facility.facility_name
        # Get School information
        sch_class, sch_adm_type = '', ''
        school_id, school = '', ''
        if creg.school_level != 'SLNS':
            school = get_school(ovc_id)
            if school:
                sch_class = school.school_class
                sch_adm_type = school.admission_type
                school_id = school.school_id
                school = school.school.school_name
        bcert_no = params['ISOV'] if 'ISOV' in params else ''
        ncpwd_no = params['IPWD'] if 'IPWD' in params else ''
        # Eligibility
        criterias = OVCEligibility.objects.filter(
            is_void=False, person_id=child.id).values_list(
            'criteria', flat=True)
        if reg_date:
            date_reg = reg_date.strftime('%d-%b-%Y')
        exit_date = None
        if creg.exit_date:
            exit_date = creg.exit_date.strftime('%d-%b-%Y')
        all_values = {'reg_date': date_reg, 'cbo_uid': creg.org_unique_id,
                      'cbo_uid_check': creg.org_unique_id,
                      'has_bcert': bcert, 'disb': disb,
                      'bcert_no': bcert_no, 'ncpwd_no': ncpwd_no,
                      'immunization': creg.immunization_status,
                      'school_level': creg.school_level, 'facility': facility,
                      'facility_id': facility_id, 'school_class': sch_class,
                      'school_name': school, 'school_id': school_id,
                      'admission_type': sch_adm_type,
                      'hiv_status': creg.hiv_status, 'link_date': date_linked,
                      'ccc_number': ccc_no, 'art_status': art_status,
                      'eligibility': criterias, 'is_exited': exited,
                      'exit_reason': creg.exit_reason,
                      'ovc_exit_reason': creg.exit_reason,
                      'exit_date': exit_date,
                      'exit_org_name': exit_org_name}
        form = OVCRegistrationForm(guids=pids, data=all_values)
        for hhm in hhmembers:
            status_id = 'status_%s' % (hhm.person_id)
            all_values['a%s' % (status_id)] = hhm.member_alive
            all_values['g%s' % (status_id)] = hhm.hiv_status
            all_values['sg%s' % (status_id)] = hhm.hiv_status
        # Class levels
        levels = {}
        levels["SLNS"] = []
        levels["SLEC"] = ["BABY,Baby Class", "MIDC,Middle Class",
                          "PREU,Pre-Unit"]
        levels["SLPR"] = ["CLS1,Class 1", "CLS2,Class 2", "CLS3,Class 3",
                          "CLS4,Class 4", "CLS5,Class 5", "CLS6,Class 6",
                          "CLS7,Class 7", "CLS8,Class 8"]
        levels["SLSE"] = ["FOM1,Form 1", "FOM2,Form 2", "FOM3,Form 3",
                          "FOM4,Form 4", "FOM5,Form 5", "FOM6,Form 6"]
        levels["SLUN"] = ["YER1,Year 1", "YER2,Year 2", "YER3,Year 3",
                          "YER4,Year 4", "YER5,Year 5", "YER6,Year 6"]
        levels["SLTV"] = ["TVC1,Year 1", "TVC2,Year 2", "TVC3,Year 3",
                          "TVC4,Year 4", "TVC5,Year 5"]
        # Re-usable values

        check_fields = ['relationship_type_id']
        vals = get_dict(field_name=check_fields)
        return render(request, 'ovc/edit_child.html',
                      {'form': form, 'status': 200, 'child': child,
                       'vals': vals, 'hhold': hhold, 'extids': gparams,
                       'hhmembers': hhmembers, 'levels': levels,
                       'sch_class': sch_class, 'siblings': siblings,
                       'ctaker': ctaker, 'vloads': vloads})
    except Exception, e:
        print "error with OVC editing - %s" % (str(e))
        raise e


@login_required(login_url='/')
@is_allowed_ous(['RGM', 'RGU', 'DSU', 'STD'])
def ovc_view(request, id):
    """Some default page for Server Errors."""
    try:
        aid = 0
        reqid = request.GET.get('id', '')
        offset = request.GET.get('offset', '')
        limit = request.GET.get('limit', '')
        if reqid and offset and limit:
            aid = 2
        if request.method == 'POST' or aid:
            msg, chs = manage_checkins(request, aid)
            results = {'status': 0, 'message': msg, 'checkins': chs}
            if aid == 2:
                results = chs
            return JsonResponse(results, content_type='application/json',
                                safe=False)
        ovc_id = int(id)
        child = RegPerson.objects.get(is_void=False, id=ovc_id)
        creg = OVCRegistration.objects.get(is_void=False, person_id=ovc_id)
        days = 0
        if not creg.is_active and creg.exit_date:
            edate = creg.exit_date
            tdate = date.today()
            days = (tdate - edate).days
        print 'exit days', days
        allow_edit = False if days > 90 else True
        params = {}
        gparams = {}
        # Get guardians
        guardians = RegPersonsGuardians.objects.filter(
            is_void=False, child_person_id=child.id)
        guids = []
        for guardian in guardians:
            guids.append(guardian.guardian_person_id)
        guids.append(child.id)
        extids = RegPersonsExternalIds.objects.filter(
            person_id__in=guids)
        for extid in extids:
            if extid.person_id == child.id:
                params[extid.identifier_type_id] = extid.identifier
            else:
                gkey = '%s_%s' % (extid.person_id, extid.identifier_type_id)
                gparams[gkey] = extid.identifier
        # Health details
        health = {}
        if creg.hiv_status == 'HSTP':
            health = get_health(ovc_id)
        # School details
        school = {}
        if creg.school_level != 'SLNS':
            school = get_school(ovc_id)
        # Get house hold
        hhold = OVCHHMembers.objects.get(
            is_void=False, person_id=child.id)
        # Get HH members
        hhid = hhold.house_hold_id
        hhmqs = OVCHHMembers.objects.filter(
            is_void=False, house_hold_id=hhid).order_by("-hh_head")
        hhmembers = hhmqs.exclude(person_id=child.id)
        # Viral load
        vload = OVCViralload.objects.filter(
            is_void=False, person_id=ovc_id).order_by("-viral_date")[:1]
        vl_sup, v_val, v_dt = 'Missing', None, None
        if vload:
            for vl in vload:
                v_val = vl.viral_load
                v_dt = vl.viral_date
            vl_sup = 'YES' if not v_val or v_val < 1000 else 'NO'
        # Get siblings
        siblings = RegPersonsSiblings.objects.filter(
            is_void=False, child_person_id=child.id)
        # Get services
        servs = {'FSAM': 'f1a', 'FCSI': 'fcsi', 'FHSA': 'fhva'}
        services = {'f1a': 0, 'fcsi': 0, 'fhva': 0}
        sqs = OVCCareEvents.objects.filter(
            Q(person_id=child.id) | Q(house_hold_id=hhid))
        sqs = sqs.filter(is_void=False).values(
            'event_type_id').annotate(
                total=Count('event_type_id')).order_by('total')
        for serv in sqs:
            item = serv['event_type_id']
            item_count = serv['total']
            if item in servs:
                item_key = servs[item]
                services[item_key] = item_count
        # Re-usable values
        check_fields = ['relationship_type_id', 'school_level_id',
                        'hiv_status_id', 'immunization_status_id',
                        'art_status_id', 'school_type_id',
                        'class_level_id']
        vals = get_dict(field_name=check_fields)
        return render(request, 'ovc/view_child.html',
                      {'status': 200, 'child': child, 'params': params,
                       'guardians': guardians, 'siblings': siblings,
                       'vals': vals, 'hhold': hhold, 'creg': creg,
                       'extids': gparams, 'health': health,
                       'hhmembers': hhmembers, 'school': school,
                       'services': services, 'allow_edit': allow_edit,
                       'suppression': vl_sup})
    except Exception, e:
        print "error with OVC viewing - %s" % (str(e))
        raise e


@login_required(login_url='/')
def hh_manage(request, hhid):
    """Some default page for Server Errors."""
    try:
        check_fields = ['hiv_status_id', 'immunization_status_id']
        vals = get_dict(field_name=check_fields)
        hhmembers = OVCHHMembers.objects.filter(
            is_void=False, house_hold_id=hhid).order_by("-hh_head")
        return render(request, 'ovc/household.html',
                      {'status': 200, 'hhmembers': hhmembers,
                       'vals': vals})
    except Exception, e:
        print "error getting hh members - %s" % (str(e))
        raise e


@login_required(login_url='/')
def ovc_manage(request):
    """Some default page for Server Errors."""
    try:
        ovc_management(request)
        results = {'message': 'Successful'}
        return JsonResponse(results, content_type='application/json',
                            safe=False)
    except Exception, e:
        msg = "error updating OVC details - %s" % (str(e))
        results = {'message': msg}
        return JsonResponse(results, content_type='application/json',
                            safe=False)
