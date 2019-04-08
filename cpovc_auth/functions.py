"""Common functions for authentication module."""
from django.utils import timezone

from .models import CPOVCRole, CPOVCUserRoleGeoOrg
from cpovc_main.models import RegTemp
from cpovc_registry.models import (
    RegPersonsGeo, RegPersonsOrgUnits, RegOrgUnit)


def get_allowed_units_county(user_id):
    """
    Return dict with list of allowed group ids mapped to org units.

    and for sub counties do the reverse just list of sub-counties
    """
    try:
        geo_orgs = get_group_geos_org(user_id)
        ex_areas, ex_orgs = [], {}
        for geo_org in geo_orgs:
            if geo_org['area_id']:
                ex_areas.append(geo_org['area_id'])
            if geo_org['org_unit_id']:
                if geo_org['org_unit_id'] in ex_orgs:
                    ex_orgs[geo_org['org_unit_id']].append(geo_org['group_id'])
                else:
                    ex_orgs[geo_org['org_unit_id']] = [geo_org['group_id']]
    except Exception, e:
        error = 'Error getting persons orgs/sub-county groups - %s' % (str(e))
        print error
    else:
        return ex_areas, ex_orgs


def get_groups(grp_prefix='group_'):
    """Return list of ids and CPIMS codes."""
    groups = {}
    disallowed_group = [11]
    try:
        results = CPOVCRole.objects.filter().values(
            'group_ptr_id', 'group_id', 'group_name')
        for group in results:
            group_id = '%s%s' % (grp_prefix, str(group['group_id']))
            if group_id not in disallowed_group:
                groups[group['group_ptr_id']] = group_id

    except Exception, e:
        error = 'Error getting groups - %s' % (str(e))
        print error
    else:
        return groups


def get_group_geos_org(user_id):
    """Get group ids mapping to geos."""
    try:
        result = CPOVCUserRoleGeoOrg.objects.filter(
            user_id=user_id, is_void=False).values(
                'area_id', 'group_id', 'org_unit_id')
    except Exception, e:
        error = 'Error getting geo/orgs by groups - %s' % (str(e))
        print error
    else:
        return result


def remove_group_geo_org(user_id, group_id, area_id, org_unit_id):
    """For removing / revoking this group ids."""
    try:
        geo_orgs = CPOVCUserRoleGeoOrg.objects.get(
            user_id=user_id, group_id=group_id, is_void=False,
            area_id=area_id, org_unit_id=org_unit_id)
        geo_orgs.is_void = True
        geo_orgs.save(update_fields=['is_void'])
    except Exception, e:
        error = 'Error removing org unit -%s' % (str(e))
        print error
        return None
    else:
        return geo_orgs


def save_group_geo_org(user_id, group_id, area_id, org_unit_id):
    """Method for attaching org units and sub-counties."""
    try:
        if org_unit_id:
            geo_org_perm, ctd = CPOVCUserRoleGeoOrg.objects.update_or_create(
                user_id=user_id, group_id=group_id, org_unit_id=org_unit_id,
                is_void=False,
                defaults={'area_id': area_id, 'org_unit_id': org_unit_id,
                          'user_id': user_id, 'group_id': group_id,
                          'is_void': False},)
        geo_org_perm, ctd = CPOVCUserRoleGeoOrg.objects.update_or_create(
            user_id=user_id, group_id=group_id, area_id=area_id, is_void=False,
            defaults={'area_id': area_id, 'org_unit_id': org_unit_id,
                      'user_id': user_id, 'group_id': group_id,
                      'is_void': False},)
    except Exception, e:
        error = 'Error searching org unit -%s' % (str(e))
        print error
        return None
    else:
        return geo_org_perm, ctd


def save_temp_data(user_id, page_id, page_data):
    """"Method to save temp form data for this person and page."""
    try:
        new_tmp, ctd = RegTemp.objects.update_or_create(
            user_id=user_id, page_id=page_id,
            defaults={'data': str(page_data), 'created_at': timezone.now(),
                      'user_id': user_id, 'page_id': page_id},)
    except Exception, e:
        print 'save tmp error - %s' % (str(e))
        pass


def check_national(user):
    """"Method to check if national guy but allow for super user."""
    try:
        if user.is_superuser:
            return False
        person_id = user.reg_person_id
        person_geos = RegPersonsGeo.objects.filter(
            person_id=person_id, is_void=False)
        if person_geos:
            return False
        else:
            return True
    except Exception, e:
        print 'check national error - %s' % (str(e))
        return False


def get_attached_units(user):
    """"Method to check attached units."""
    orgs = []
    try:
        if user.is_superuser:
            return {}
        person_id = user.reg_person_id
        person_orgs = RegPersonsOrgUnits.objects.filter(
            person_id=person_id, is_void=False)
        if person_orgs:
            reg_pri, reg_ovc, reg_pri_name = 0, False, ''
            all_roles, all_ous = [], []
            for p_org in person_orgs:
                p_roles = []
                org_id = p_org.org_unit_id
                org_name = p_org.org_unit.org_unit_name
                reg_assist = p_org.reg_assistant
                if reg_assist:
                    p_roles.append('REGA')
                    all_roles.append('REGA')
                reg_prim = p_org.primary_unit
                if reg_prim:
                    reg_pri = org_id
                    reg_pri_name = org_name
                reg_ovc = p_org.org_unit.handle_ovc
                if reg_ovc:
                    p_roles.append('ROVC')
                    all_roles.append('ROVC')
                    reg_ovc = True
                pvals = {org_id: p_roles}
                orgs.append(pvals)
                all_ous.append(str(org_id))
            allroles = ','.join(list(set(all_roles)))
            allous = ','.join(all_ous)
            vals = {'perms': orgs, 'primary_ou': reg_pri,
                    'attached_ou': allous, 'perms_ou': allroles,
                    'reg_ovc': reg_ovc, 'primary_name': reg_pri_name}
            return vals
        else:
            return {}
    except Exception, e:
        print 'get attached units error - %s' % (str(e))
        return {}


def get_parent_unit(org_ids):
    """Method to do the organisation tree."""
    try:
        # print org_ids
        orgs = RegOrgUnit.objects.filter(
            id__in=org_ids).values_list('parent_org_unit_id', flat=True)
        print 'Check Org Unit level - %s' % (str(orgs))
    except Exception as e:
        print 'No parent unit - %s' % (str(e))
        return []
    else:
        return orgs


def get_orgs_tree(org_id):
    """Method to do the organisation tree."""
    try:
        dcs = [1, 2]
        level = 1
        orgs = {0: dcs, 1: [], 2: [], 3: [], 4: []}
        parent_orgs = get_parent_unit([int(org_id)])
        orgs[1] = parent_orgs
        is_dcs = (i in parent_orgs for i in dcs)
        if not parent_orgs:
            return level, []
        if any(is_dcs):
            level = 0
        else:
            parent_orgs_1 = get_parent_unit(parent_orgs)
            is_dcs = (i in parent_orgs_1 for i in dcs)
            orgs[2] = parent_orgs_1
            if any(is_dcs):
                level = 1
            else:
                parent_orgs_2 = get_parent_unit(parent_orgs_1)
                is_dcs = (i in parent_orgs_2 for i in dcs)
                orgs[3] = parent_orgs_2
                if any(is_dcs):
                    level = 2
                else:
                    parent_orgs_3 = get_parent_unit(parent_orgs_2)
                    is_dcs = (i in parent_orgs_3 for i in dcs)
                    orgs[4] = parent_orgs_3
                    if any(is_dcs):
                        level = 3
    except Exception as e:
        print 'error with tree - %s' % (str(e))
        return 1, {}
    else:
        return level, orgs
