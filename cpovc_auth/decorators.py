"""Decorator to handle permissions."""
from functools import wraps
from django.shortcuts import render, get_object_or_404
from django.utils.decorators import available_attrs
from cpovc_registry.models import (
    RegPersonsAuditTrail, RegOrgUnitsAuditTrail, RegPersonsGeo,
    RegPersonsOrgUnits, RegOrgUnit, RegPerson)
from cpovc_ovc.models import OVCRegistration
from .models import AppUser
from .perms import PERM

ORG_GROUPS = ['DEC', 'DSU', 'DUU', 'RGU']
APPS = {'registry': 1, 'auth': 2, 'forms': 3, 'ovcare': 4, 'reports': 5}
MODULES = {'ou': 1, 'person': 2, 'roles': 3, 'ovc': 6, 'reports': 7}
FORMS = ['crs', 'education', 'school', 'documents']
TRANS = {'search': 0, 'new': 1, 'edit': 2, 'view': 3, 'delete': 4}


def is_allowed_groups(allowed_groups, page=11):
    """Method for checking roles and permissions."""

    def decorator(check_func):
        @wraps(check_func, assigned=available_attrs(check_func))
        def _wrapped_view(request, *args, **kwargs):
            # If active super user lets just proceed
            url_parts = request.path_info.split('/')
            url_len = len(url_parts)
            print 'url', request.path_info, 'Len', len(url_parts), url_parts
            app = url_parts[1] if url_len > 1 and url_parts[1] else None
            module = url_parts[2] if url_len > 2 and url_parts[2] else None
            trans = url_parts[3] if url_len > 3 and url_parts[3] else None
            iid = url_parts[4] if url_len > 4 and url_parts[4] else None
            # print 'pg', page
            mod_id = MODULES[module] if module in MODULES else 1
            trans_id = TRANS[trans] if trans in TRANS else 1
            # Sessions
            reg_ovc = request.session.get('reg_ovc', 0)
            if module and trans:
                page = '%s%s' % (mod_id, trans_id)
            else:
                page = '10'
            page_ids = str(page).zfill(2)
            page_type = page_ids[1:]
            # Get the DCS restricted modules
            if module in FORMS:
                print 'GOK restricted', app, module
                page = '4%s' % (page_type)
                if reg_ovc:
                    page = '5%s' % (page_type)
            page_id = int(page)
            print page_type
            if request.user.is_active and request.user.is_superuser:
                return check_func(request, *args, **kwargs)
            else:
                print 'page id', page_id
                level_perms = PERM[page_id] if page_id in PERM else {}
                print level_perms
                perms_list = level_perms['perms']
                is_ovc, is_dcs, is_nat = False, False, False
                org_id = request.session.get('ou_primary', 0)
                reg_nat = request.session.get('is_national', 0)
                ou_perms = request.session.get('ou_perms', 0)
                ou_attached = request.session.get('ou_attached', 0)
                user_level = request.session.get('user_level', 0)
                print 'oup', ou_perms, ou_attached, user_level, org_id
                if level_perms['ovc'] and reg_ovc:
                    is_ovc = True
                if level_perms['dcs'] and not reg_ovc:
                    is_dcs = True
                if level_perms['ho'] and reg_nat:
                    is_nat = True
                ovc_check = (is_ovc, is_dcs, is_nat)
                user_group = 'ho' if reg_nat else 'dcs'
                user_grp = 'ovc' if reg_ovc else user_group
                print ovc_check
                from .functions import get_groups
                grps = request.user.groups.values_list('id', flat=True)
                # Attached
                ou_parts = ou_attached.split(',') if ou_attached else []
                ous = [int(iou) for iou in ou_parts] if ou_attached else []
                print 'AOU', ous
                cpgrp = get_groups('')
                cpims_grps = [cpgrp[grp] for grp in grps if grp in cpgrp]
                # print cpims_grps
                gen_groups = [x for x in cpims_grps if x not in ORG_GROUPS]
                print ovc_check, gen_groups, cpims_grps
                response = any(value in cpims_grps for value in allowed_groups)
                print 'jr', response
                if response:
                    if any(ovc_check):
                        if perms_list:
                            # Check for the parameters
                            is_perms = check_perm_list(
                                request, perms_list, module, iid, user_grp)
                            if is_perms:
                                return check_func(request, *args, **kwargs)
                        else:
                            return check_func(request, *args, **kwargs)
                # current_url = resolve(request.path_info).url_name
                page_info = 'Permission denied'
                return render(request, 'registry/roles_none.html',
                              {'page': page_info})
        return _wrapped_view
    return decorator


def is_allowed_ous(allowed_groups, page=11):
    return is_allowed_groups(allowed_groups, page)


def check_perm_list(request, perms_list, mod_id, item_id, user_grp=None):
    """Method to check the permission."""
    try:
        if item_id:
            item_check = False
            user_id = int(request.user.reg_person_id)
            wf_id = int(request.user.id)
            print 'Item ID', mod_id, item_id
            for perm_id in perms_list:
                if mod_id == 'person':
                    # Get person type
                    print 'person'
                    creator_id = 0
                    cdetails = get_creator_details(item_id)
                    if cdetails:
                        creator_id = cdetails.created_by_id
                    print 'creator', creator_id, wf_id
                    uid = check_workmate(user_id, item_id, perm_id)
                    if uid or creator_id == wf_id:
                        item_check = True
                    if user_grp == 'dcs' and perm_id == 'GK':
                        item_check = True
                elif mod_id == 'roles':
                    # Get person type
                    print 'roles'
                    person_id, creator_id = get_person(item_id)
                    uid = check_workmate(user_id, person_id, perm_id)
                    if uid or creator_id == wf_id:
                        item_check = True
                elif mod_id == 'ou':
                    # Get org unit
                    print 'org unit'
                    item_check = True
                elif mod_id == 'ovc':
                    print 'Get OVC'
                    item_check = False
                    uid = check_workmate(user_id, item_id, perm_id)
                    if uid:
                        item_check = True
            return item_check
        else:
            return True
    except Exception as e:
        print 'Error checking permission - %s' % (str(e))
        return False


def get_creator_details(item_id, audit_type='Person'):
    """Method to query audit trail for creator."""
    try:
        if audit_type == 'Person':
            record_details = get_object_or_404(
                RegPerson.objects.select_related(), pk=item_id)
        else:
            record_details = get_object_or_404(
                RegOrgUnit.objects.select_related(), pk=item_id)
        return record_details
    except Exception:
        return None


def get_person(item_id):
    """Method to query audit trail for creator."""
    try:
        record_details = get_object_or_404(
            AppUser.objects.select_related(), pk=item_id)
        person_id = record_details.reg_person_id
        creator_id = record_details.reg_person.created_by_id
        return person_id, creator_id
    except Exception:
        return 0, 0


def get_audit_details(item_id, audit_type='Person'):
    """Method to query audit trail for creator."""
    try:
        if audit_type == 'Person':
            record_details = get_object_or_404(
                RegPersonsAuditTrail.objects.select_related(),
                person_id=item_id, transaction_type_id='REGS')
        else:
            record_details = get_object_or_404(
                RegOrgUnitsAuditTrail.objects.select_related(),
                org_unit_id=item_id, transaction_type_id='REGU')
        return record_details
    except Exception:
        return None


def get_child_cbo(child_id):
    """Method to get child cbo."""
    try:
        cbo_ids = []
        cbos = OVCRegistration.objects.select_related().filter(
            person_id=child_id, is_void=False)
        for cbo in cbos:
            cbo_ids.append(cbo.child_cbo_id)
    except Exception as e:
        print 'error getting OVC CBO - %s' % (str(e))
        return []
    else:
        return cbo_ids


def check_workmate(creator_id, person_id, check_type='P'):
    """Method to check if they belong to same org unit."""
    try:
        cur_person_id = int(person_id)
        orgs_dict = {creator_id: [], cur_person_id: []}
        geos_dict = {creator_id: [], cur_person_id: []}
        person_ids = [creator_id, person_id]
        orgs_trees = []
        person_orgs = RegPersonsOrgUnits.objects.select_related().filter(
            person_id__in=person_ids, is_void=False, date_delinked=None)
        if check_type == 'P':
            person_details = RegPersonsGeo.objects.select_related().filter(
                person_id__in=person_ids, is_void=False, date_delinked=None)

            for person_detail in person_details:
                area_id = person_detail.area_id
                geos_dict[person_detail.person_id].append(area_id)

        for person_org in person_orgs:
            orgs_trees.append(person_org.org_unit_id)
            orgs_dict[person_org.person_id].append(person_org.org_unit_id)

        print 'B4 Check', orgs_dict, geos_dict
        creator_org = set(orgs_dict[creator_id])
        user_org = set(orgs_dict[cur_person_id])

        if not user_org:
            child_cbos = get_child_cbo(person_id)
            user_org = set(child_cbos)
        if check_type == 'SL':
            creator_orgs = get_orgs_child(list(creator_org))
        else:
            creator_orgs = creator_org
        print 'OC', creator_orgs, user_org

        same_orgs = set(creator_orgs).intersection(list(user_org))
        if same_orgs:
            return list(same_orgs)
        # Check geo
        creator_geo = set(geos_dict[creator_id])
        user_geo = set(geos_dict[cur_person_id])
        same_geo = creator_geo.intersection(user_geo)
        if same_geo:
            return list(same_geo)
        return []
    except Exception, e:
        print 'error - %s' % (str(e))
        return None


def get_unit_parent(org_ids):
    """Method to do the organisation tree."""
    try:
        print org_ids
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


def get_orgs_child(child_units):
    """Method to do the organisation tree."""
    try:
        # child_units = [int(org_id)]
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
