"""CPIMS authentication views."""
import urlparse
from django.shortcuts import render
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, JsonResponse
from django.contrib.auth import authenticate, login, logout
from cpovc_auth.forms import LoginForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.forms import formset_factory
from django.contrib.auth.models import Group

from .functions import (
    save_group_geo_org, remove_group_geo_org, get_allowed_units_county,
    get_groups, save_temp_data, check_national, get_attached_units,
    get_orgs_tree)
from .models import AppUser, CPOVCPermission
from cpovc_registry.models import (
    RegPerson, RegPersonsExternalIds, RegPersonsOrgUnits, RegPersonsGeo)
from cpovc_main.models import SetupGeography

from .forms import RolesOrgUnits, RolesGeoArea, RolesForm, PasswordResetForm
from .decorators import is_allowed_groups

from django.contrib.auth.models import Permission
from cpims.views import home as cpims_home
from cpovc_registry.views import persons_search
from cpovc_access.decorators import watch_login
from cpovc_access.forms import StrictAuthenticationForm

from django.contrib.auth.views import password_reset_confirm
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from django.contrib.auth.tokens import default_token_generator
from django.template.response import TemplateResponse
from django.utils.translation import ugettext as _
from django.shortcuts import resolve_url


def home(request):
    """Some default page for the home page / Dashboard."""
    try:
        return render(request, 'base.html', {'status': 200})
    except Exception, e:
        raise e


@watch_login
def log_in(request):
    """Method to handle log in to system."""
    try:
        authentication_form = StrictAuthenticationForm
        if request.method == 'POST':
            # form = LoginForm(data=request.POST)
            form = authentication_form(request, data=request.POST)
            if form.is_valid():
                username = form.data['username'].strip()
                password = form.data['password'].strip()
                user = authenticate(username=username, password=password)
                if user is not None:
                    if user.is_active:
                        login(request, user)
                        # grps = user.groups.all()
                        perms = user.get_all_permissions()
                        """
                        group_ids = Group.objects.all().values_list(
                            'id', flat=True)
                        """
                        group_ids = request.user.groups.values_list(
                            'id', flat=True)
                        # ------------------------------
                        perms = CPOVCPermission.objects.filter(
                            group__id__in=group_ids)
                        print 'perms', perms.count()
                        pperms = Permission.objects.values('id', 'codename')
                        all_perms = {}
                        for pm in pperms:
                            all_perms[pm['codename']] = pm['id']
                        # print all_perms
                        person_id = user.reg_person_id
                        names = RegPerson.objects.get(pk=person_id)
                        user_names = '%s %s' % (
                            names.first_name, names.surname)
                        request.session['names'] = user_names
                        is_national = check_national(user)
                        request.session['is_national'] = is_national
                        ou_vars = get_attached_units(user)
                        # print ou_vars
                        primary_ou, reg_ovc, primary_name = 0, False, ''
                        attached_ou, perms_ou = '', ''
                        if ou_vars:
                            primary_ou = ou_vars['primary_ou']
                            primary_name = ou_vars['primary_name']
                            attached_ou = ou_vars['attached_ou']
                            perms_ou = ou_vars['perms_ou']
                            reg_ovc = ou_vars['reg_ovc']
                        level, pous = get_orgs_tree(primary_ou)
                        print level, pous
                        request.session['ou_primary'] = primary_ou
                        request.session['ou_primary_name'] = primary_name
                        request.session['ou_attached'] = attached_ou
                        request.session['ou_perms'] = perms_ou
                        request.session['reg_ovc'] = reg_ovc
                        request.session['user_level'] = level
                        next_param = request.GET
                        if 'next' in next_param:
                            next_page = next_param['next']
                            print 'NEXT PAGE', next_page
                            if '/login' not in next_page:
                                return HttpResponseRedirect(next_page)
                        return HttpResponseRedirect(reverse(cpims_home))
                    else:
                        msg = "Login Account is currently disabled."
                        messages.add_message(request, messages.ERROR, msg)
                        return render(request, 'login.html', {'form': form})
                else:
                    msg = "Incorrect username and / or password."
                    messages.add_message(request, messages.ERROR, msg)
                    return render(request, 'login.html', {'form': form})
        else:
            form = LoginForm()
            logout(request)
        return render(request, 'login.html', {'form': form, 'status': 200})
    except Exception, e:
        print 'Error login - %s' % (str(e))
        raise e


def log_out(request):
    """Method to handle log out to system."""
    try:
        get_params = request.GET
        user_id = request.user.id
        next_page = '/'
        # Check this value before logout
        just_logged_out = request.session.get('password_change_relogin', False)
        # print 'PC', just_logged_out
        print "User [%s] successfully logged out." % (request.user.username)
        logout(request)
        msg = 'You have successfully logged out.'
        if 'timeout' in get_params:
            msg = ('You have been logged out due to inactivity. '
                   'Please log in again.')
            messages.add_message(request, messages.ERROR, msg)
        elif just_logged_out:
            msg = 'Please log in afresh after password change.'
            messages.add_message(request, messages.INFO, msg)
        else:
            messages.add_message(request, messages.INFO, msg)
        url = reverse(log_in)
        if 'next' in get_params:
            next_page = get_params['next']
            url = '%s?next=%s' % (url, next_page)
        if 'd' in get_params:
            form_data = get_params['d']
            form_params = dict(urlparse.parse_qsl(form_data))
            # Save this to temp table
            save_temp_data(user_id, next_page, form_params)
            print user_id, next_page, form_params
        return HttpResponseRedirect(url)
    except Exception, e:
        print 'Error logout - %s' % (str(e))
        raise e


def register(request):
    """Some default page for the register page."""
    try:
        return render(request, 'register.html', {'status': 200})
    except Exception, e:
        raise e


@login_required
@is_allowed_groups(['ACM', 'DSU'])
def roles_home(request):
    """Default page for Roles home."""
    try:
        return render(request, 'registry/roles_index.html')
    except Exception, e:
        raise e


@login_required
@is_allowed_groups(['ACM', 'DSU'])
def roles_edit(request, user_id):
    """Create / Edit page for the roles."""
    try:
        login_id = request.user.id
        print "Track users, Editing|Logged in", user_id, login_id
        if int(user_id) == login_id:
            page_info = (' - You can not manage your own Rights. '
                         'Contact your supervisor.')
            return render(request, 'registry/roles_none.html',
                          {'page': page_info})
        group_ids = []
        # All groups by details as per CPIMS
        cpims_groups = get_groups()
        groups_cpims = dict(zip(cpims_groups.values(), cpims_groups.keys()))
        # Current geo orgs
        user = AppUser.objects.get(pk=user_id)
        # Test groups
        mygrp = user.groups.values_list('id', flat=True)
        person_id = user.reg_person_id
        ex_areas, ex_orgs = get_allowed_units_county(user_id)
        user_data = {'user_id': user_id}
        vals = {'SMAL': 'Male', 'SFEM': 'Female'}
        person = RegPerson.objects.get(pk=person_id)
        person_extids = RegPersonsExternalIds.objects.filter(
            person_id=person_id)
        # Get org units
        person_orgs = RegPersonsOrgUnits.objects.select_related(
            'org_unit').filter(person_id=person_id, is_void=False)
        units_count = person_orgs.count()
        # Permissions at org level
        ous = []
        if 'ou_attached' in request.session:
            attached_ous = request.session['ou_attached']
            if attached_ous:
                ous = [int(ou) for ou in attached_ous.split(',')]
        a_orgs, user_ous = [], []
        for p_orgs in person_orgs:
            p_org_id = p_orgs.org_unit_id
            user_ous.append(p_org_id)
            if p_org_id in ous:
                a_orgs.append(p_org_id)
        # Get geo locations
        person_geos = RegPersonsGeo.objects.select_related(
            'area').filter(person_id=person_id, area_type='GLTW',
                           area__area_type_id='GDIS',
                           date_delinked=None, is_void=False)
        county_count = person_geos.count()
        for row in person_extids:
            id_type = row.identifier_type_id
            if id_type == "INTL":
                person.national_id = row.identifier
            if id_type == "IWKF":
                person.workforce_id = row.identifier
        # Forms details
        data = {'orgs-TOTAL_FORMS': units_count,
                'orgs-INITIAL_FORMS': '0',
                'orgs-MAX_NUM_FORMS': ''}
        cnt = 0
        # ex_areas, ex_orgs
        for org_unit in person_orgs:
            org_unit_id = org_unit.org_unit.org_unit_id_vis
            org_unit_name = org_unit.org_unit.org_unit_name
            primary_unit = org_unit.primary_unit
            unit_name = '%s %s' % (org_unit_id, org_unit_name)
            unit_id = org_unit.org_unit.id
            field_prefix = 'orgs-%s' % (cnt)
            data['%s-org_unit_id' % (field_prefix)] = unit_id
            data['%s-org_unit_name' % (field_prefix)] = unit_name
            data['%s-org_unit_primary' % (field_prefix)] = primary_unit
            if unit_id in ex_orgs:
                all_fields = ex_orgs[unit_id]
                for all_field in all_fields:
                    f_name = cpims_groups[all_field]
                    data['%s-%s' % (field_prefix, f_name)] = True
            cnt += 1
        org_form_set = formset_factory(RolesOrgUnits)
        formset = org_form_set(data, prefix='orgs')
        # Geo form set
        gdata = {'areas-TOTAL_FORMS': county_count,
                 'areas-INITIAL_FORMS': '0',
                 'areas-MAX_NUM_FORMS': ''}
        cnts = 0
        # Roles check
        for person_geo in person_geos:
            geo_type_id = person_geo.area.area_type_id
            county_id = person_geo.area.area_id
            county_name = person_geo.area.area_name
            if geo_type_id == 'GDIS':
                field_prefix = 'areas-%s' % (cnts)
                gdata['%s-area_id' % (field_prefix)] = county_id
                if county_id in ex_areas:
                    gdata['%s-area_welfare' % (field_prefix)] = True
                gdata['%s-sub_county' % (field_prefix)] = county_name
                cnts += 1
        if not person_geos:
            existing_areas = SetupGeography.objects.filter(
                area_id__in=ex_areas, area_type_id='GDIS', is_void=False)
            county_count = existing_areas.count()
            gdata['areas-TOTAL_FORMS'] = county_count
            for existing_area in existing_areas:
                geo_type_id = existing_area.area_type_id
                county_id = existing_area.area_id
                county_name = existing_area.area_name
                field_prefix = 'areas-%s' % (cnts)
                gdata['%s-area_id' % (field_prefix)] = county_id
                gdata['%s-area_welfare' % (field_prefix)] = True
                gdata['%s-sub_county' % (field_prefix)] = county_name
                cnts += 1
        # print 'RCHECK', person_geos, ex_areas, gdata
        geo_form_set = formset_factory(RolesGeoArea)
        gformset = geo_form_set(gdata, prefix='areas')
        # Get all groups
        for cpims_grp in cpims_groups:
            cur_group = cpims_groups[cpims_grp]
            if cpims_grp in mygrp:
                user_data[cur_group] = True
        if user.is_active:
            user_data['activate_choice'] = 'activate'
        if not user.password_changed_timestamp:
            user_data['reset_password'] = True
        form = RolesForm(data=user_data)
        # Lets do the processing down here - Makes sense
        if request.method == 'POST':
            reqs = request.POST
            req_params, sreq_params = {}, {}

            for cntr in range(0, units_count):
                req_params[cntr] = {}
                for req in reqs:
                    val = request.POST.get(req)

                    if req.startswith('orgs-'):
                        fpam = 'orgs-%s-' % (cntr)
                        fvar = str(req.replace(fpam, ''))
                        req_params[cntr][fvar] = val
            # Save org units
            new_units_org = {}
            for oval in range(0, (units_count)):
                org_details = req_params[oval]
                for org_group in groups_cpims:
                    unit_id = int(org_details['org_unit_id'])
                    if org_group in org_details:
                        group_id = groups_cpims[org_group]
                        if unit_id not in new_units_org:
                            new_units_org[unit_id] = []
                        if group_id not in new_units_org[unit_id]:
                            new_units_org[unit_id].append(group_id)
                        save_group_geo_org(user_id, group_id, None, unit_id)
                        if group_id not in group_ids:
                            group_ids.append(group_id)
            # Remove existing and have been removed
            for f_unit in new_units_org:
                new_orgs = new_units_org[f_unit]
                if f_unit in ex_orgs:
                    to_dels = ex_orgs[f_unit]
                    for to_del in to_dels:
                        if to_del not in new_orgs:
                            remove_group_geo_org(user_id, to_del, None, f_unit)
            # Sub county data
            for sntr in range(0, cnts):
                sreq_params[sntr] = {}
                for req in reqs:
                    val = request.POST.get(req)
                    if req.startswith('areas-'):
                        fpam = 'areas-%s-' % (sntr)
                        fvar = str(req.replace(fpam, ''))
                        sreq_params[sntr][fvar] = val
            new_counties = []
            county_grp = groups_cpims['group_SWA']
            for sval in range(0, len(sreq_params)):
                area_details = sreq_params[sval]
                if 'area_welfare' in area_details:
                    area_id = int(area_details['area_id'])
                    new_counties.append(area_id)
                    save_group_geo_org(user_id, county_grp, area_id, None)
                    if county_grp not in group_ids:
                        group_ids.append(county_grp)
            # Delete area id groups
            for ex_area in ex_areas:
                if ex_area not in new_counties:
                    remove_group_geo_org(user_id, county_grp, ex_area, None)

            user_id = request.POST.get('user_id')
            sys_config = request.POST.get('group_SCM')
            reg_manager = request.POST.get('group_RGM')
            access_manager = request.POST.get('group_ACM')
            national_welfare = request.POST.get('group_SWM')
            standard_log = request.POST.get('group_STD')
            # Accounts specific
            reset_password = request.POST.get('reset_password')
            activate_choice = request.POST.get('activate_choice')
            if sys_config:
                group_ids.append(groups_cpims['group_SCM'])
            if reg_manager:
                group_ids.append(groups_cpims['group_RGM'])
            if access_manager:
                group_ids.append(groups_cpims['group_ACM'])
            if national_welfare:
                group_ids.append(groups_cpims['group_SWM'])
            if standard_log:
                group_ids.append(groups_cpims['group_STD'])
            # Check if any group is being removed
            removed_groups = list(set(mygrp) - set(group_ids))
            print 'New groups', group_ids
            print 'Remove groups', removed_groups
            for group_id in group_ids:
                group = Group.objects.get(id=group_id)
                user.groups.add(group)
            # Lets remove this groups
            for grp_id in removed_groups:
                group = Group.objects.get(id=grp_id)
                user.groups.remove(group)
            # Lets save password change and activate/deactivate
            if reset_password:
                user.password_changed_timestamp = None
                user.save(update_fields=["password_changed_timestamp"])
            if activate_choice:
                a_choice = True if activate_choice == 'activate' else False
                user.is_active = a_choice
                user.save(update_fields=["is_active"])
            # Redirect will be safe for now
            msg = "Roles modified successfully"
            messages.add_message(request, messages.INFO, msg)
            return HttpResponseRedirect(
                '%s?id=%d' % (reverse(persons_search), int(person_id)))

        return render(request, 'registry/roles_edit.html',
                      {'form': form, 'formset': formset,
                       'gformset': gformset, 'person': person,
                       'vals': vals})
    except AppUser.DoesNotExist:
        msg = 'Account must exist to attach a Role / Permission'
        messages.add_message(request, messages.ERROR, msg)
        return render(request, 'registry/roles_index.html')
    except RegPerson.DoesNotExist:
        msg = 'Person must exist to attach a Role / Permission'
        messages.add_message(request, messages.ERROR, msg)
        return render(request, 'registry/roles_index.html')
    except Exception, e:
        print 'error - %s' % (str(e))
        raise e


def reset_confirm(request, uidb36=None, token=None):
    """Method for confirm password reset."""
    return password_reset_confirm(
        request, template_name='registration/password_reset_confirm.html',
        uidb36=uidb36, token=token, post_reset_redirect=reverse(log_in))


def reset(request):
    """Method to do the actual password reset."""
    return password_reset(
        request, template_name='registration/password_reset.html',
        email_template_name='registration/password_reset_email.html',
        subject_template_name='registration/password_reset_subject.txt',
        post_reset_redirect=reverse(log_in))


@csrf_protect
def password_reset(
        request, is_admin_site=False,
        template_name='registration/password_reset_form.html',
        email_template_name='registration/password_reset_email.html',
        subject_template_name='registration/password_reset_subject.txt',
        password_reset_form=PasswordResetForm,
        token_generator=default_token_generator,
        post_reset_redirect=None,
        from_email=None,
        current_app=None,
        extra_context=None,
        html_email_template_name=None):
    """Method to reset password."""
    if post_reset_redirect is None:
        post_reset_redirect = reverse('password_reset_done')
    else:
        post_reset_redirect = resolve_url(post_reset_redirect)
    if request.method == "POST":
        form = password_reset_form(request.POST)
        if form.is_valid():
            opts = {
                'use_https': request.is_secure(),
                'token_generator': token_generator,
                'from_email': from_email,
                'email_template_name': email_template_name,
                'subject_template_name': subject_template_name,
                'request': request,
                'html_email_template_name': html_email_template_name,
            }
            if is_admin_site:
                opts = dict(opts, domain_override=request.get_host())
            form.save(**opts)
            return HttpResponseRedirect(post_reset_redirect)
    else:
        form = password_reset_form()
    context = {
        'form': form,
        'title': _('Password reset'),
    }
    if extra_context is not None:
        context.update(extra_context)
    return TemplateResponse(request, template_name, context,
                            current_app=current_app)


@csrf_exempt
def user_ping(request):
    """Method for checking if user is still logged in with ping."""
    response = {'status': False}
    try:
        if request.user.is_authenticated():
            status = True
    except Exception:
        pass
    else:
        response['status'] = status
        return JsonResponse(response, content_type='application/json')
