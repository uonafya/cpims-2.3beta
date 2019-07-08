import base64
import json

from django.contrib.auth.decorators import login_required
from django.http import JsonResponse

from cpovc_auth.functions import get_attached_units
from cpovc_ovc.models import OVCRegistration
from cpovc_registry.functions import get_attached_ous, get_orgs_child


@login_required(login_url='/')
def fetch_forms(request):
	return JsonResponse({"msg": "ok"})


@login_required(login_url='/')
def fetch_data(request):
	attached_org_units = get_attached_ous(request)
	org_units = get_orgs_child(attached_org_units, 1)

	# access performance for this: upper bound of this: How many ovcs per ancestor org
	ovcs_for_org = OVCRegistration.objects.filter(
		is_void=False,
		is_active=True,
		child_cbo_id__in=org_units)

	ovc_data = {}

	print "Ovcs count: ", len(ovcs_for_org)

	for ovc in ovcs_for_org:
		full_name = ovc.person.all_names.replace(' ', '')
		full_name = ''.join([str(ord(i)) for i in full_name])

		key = '{full_name}_{reg_person_id}_{ovc_reg_id}'.format(
			full_name=full_name,
			reg_person_id=ovc.person.id,
			ovc_reg_id=ovc.id)

		ovc_data[key.upper()] = base64.b64encode(json.dumps({
			'person_id': ovc.person_id,
			'org_unique_id': ovc.org_unique_id,
			'first_name': ovc.person.first_name,
			'surname': ovc.person.surname,
			'other_names': ovc.person.other_names,
			'sex_id': ovc.person.sex_id,
			'date_of_birth': ovc.person.date_of_birth.strftime('%d/%m/%Y'),
			'child_chv_full_name': ovc.child_chv.full_name,
			'caretake_full_name': ovc.caretaker.full_name,
			'org_unt_name': ovc.child_cbo.org_unit_name,
			'is_active': 'Active' if ovc.is_active else 'Exited'

		}))

	return JsonResponse({
		'data': ovc_data
	})


@login_required(login_url='/')
def offline_mode_test(request):
	if request.method == 'GET':
		return JsonResponse(
			{'msg': "ok testing"}, content_type='application/json', safe=True)
	else:
		print request.body
		return JsonResponse(
			{'msg': "submitted"}, content_type='application/json', safe=True)
