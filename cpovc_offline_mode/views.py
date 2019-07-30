import base64
import json
import logging
import sys
import traceback

from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render

from cpovc_forms.forms import OVCF1AForm, CasePlanTemplate
from cpovc_forms.functions import create_fields, create_form_fields
from cpovc_main.functions import get_dict
from cpovc_offline_mode.helpers import get_ovc_school_details, get_ovc_facility_details, get_ovc_household_members, \
    get_services, save_submitted_form1a, save_submitted_form1b, save_submitted_case_plan_template
from cpovc_ovc.models import OVCRegistration
from cpovc_registry.templatetags.app_filters import gen_value, vals, check_fields

logger = logging.getLogger(__name__)


@login_required(login_url='/')
def templates(request):
    values = get_dict(field_name=check_fields)
    form_1a = OVCF1AForm()
    ffs = create_fields(['form1b_items'])
    domains = create_form_fields(ffs)
    tpls = {
        'ovc_home': render(request, 'ovc/home_offline.html').content,
        'ovc_view': render(request, 'ovc/view_child_offline.html').content,
        'ovc_form1a': render(request, 'forms/form1a_offline.html', {'form': form_1a, 'vals': values}).content,
        'ovc_form1b': render(request, 'forms/form1b_offline.html', {
            'form': form_1a,
            'domains': domains,
            'form1b_allowed': True
        }).content,
        'case_plan_template': render(request, 'forms/case_plan_template_offline.html', {
            'form': CasePlanTemplate(),
            'vals': get_dict(field_name=['sex_id', 'relationship_type_id'])
        }).content
    }
    return JsonResponse({'data': json.dumps(tpls)})


@login_required(login_url='/')
def fetch_data(request):
    user_orgs = request.user.reg_person.regpersonsorgunits_set.values()
    org_units = []

    for org in user_orgs:
        if not org['is_void']:
            org_units.append(org['org_unit_id'])

    ovcs_for_org = OVCRegistration.objects.filter(
        is_void=False,
        is_active=True,
        child_cbo_id__in=org_units).order_by('-id')[:1000]  # limit to 1000

    ovc_data = {}

    for ovc in ovcs_for_org:
        full_name = ovc.person.all_names.replace(' ', '')
        full_name = ''.join([str(ord(i)) for i in full_name])

        key = '{full_name}_{reg_person_id}_{ovc_reg_id}'.format(
            full_name=full_name,
            reg_person_id=ovc.person.id,
            ovc_reg_id=ovc.id).upper()

        def _format_date(date):
            return date.strftime('%d/%m/%Y') if date else ""

        ovc_data[key] = base64.b64encode(json.dumps({
            'id': key,
            'person_id': ovc.person_id,
            'registration_date': _format_date(ovc.registration_date),
            'org_unique_id': ovc.org_unique_id,
            'first_name': ovc.person.first_name,
            'surname': ovc.person.surname,
            'other_names': ovc.person.other_names,
            'sex_id': ovc.person.sex_id,
            'date_of_birth': _format_date(ovc.person.date_of_birth),
            'age': ovc.person.age,
            'registration_date': _format_date(ovc.registration_date),
            'has_bcert': "Yes" if ovc.has_bcert else "No",
            'is_disabled': "Yes" if ovc.is_disabled else "No",
            'child_chv_full_name': ovc.child_chv.full_name if ovc.child_chv else "",
            'chv_id': ovc.child_chv_id,
            'caretake_full_name': ovc.caretaker.full_name if ovc.caretaker else "",
            'caretaker_id': ovc.caretaker_id,
            'org_unit_name': ovc.child_cbo.org_unit_name if ovc.child_cbo else "",
            'is_active': 'Active' if ovc.is_active else 'Exited',
            'immunization_status': gen_value(ovc.immunization_status, vals),
            'school_level': gen_value(ovc.school_level, vals),
            'hiv_status': ovc.hiv_status,
            'suppressed': ovc.hiv_status if ovc.hiv_status == "HSTP" else "N/A",

            # facility details
            'facility': get_ovc_facility_details(ovc),

            # school details
            'school': get_ovc_school_details(ovc),

            # house hold members
            'household_members': get_ovc_household_members(ovc)
        }))

    return JsonResponse({
        'data': ovc_data
    })


@login_required(login_url='/')
def fetch_services(request):
    return JsonResponse({
        'data': base64.b64encode(json.dumps(get_services()))
    })


def submit_form(request):

    logger.info("Submitted data is : {}".format(request.body))

    data = json.loads(request.body)

    payload = data["payload"]
    user_id = data["_userId"]
    ovc_id = payload['person']

    try:
        if payload['form_type'].lower() == 'form1a':
            save_submitted_form1a(
                user_id,
                ovc_id,
                payload['form_data'],
                request.session.get('ou_primary'),
                request.session.get('ou_attached').split(","))

        if payload['form_type'].lower() == 'form1b':
            save_submitted_form1b(user_id, ovc_id, payload['form_data'])
        if payload['form_type'].lower() == 'CasePlanTemplate'.lower():
            save_submitted_case_plan_template(user_id, ovc_id, payload['form_data'])
    except Exception as ex:
        # catch and log, for it to go to logs for manual reviewing
        type_, value_, traceback_ = sys.exc_info()
        formatted_exception = traceback.format_exception(etype=type_, value=value_, tb=traceback_)

        logger.error("Cannot save offline submitted data: {} | Error: {}".format(request.body, formatted_exception))

    return JsonResponse({
        'msg': 'ok'
    })
