import base64
import json

from django.contrib.auth.decorators import login_required
from django.http import JsonResponse

from cpovc_ovc.models import OVCRegistration, OVCHHMembers, OVCHealth, OVCEducation
from cpovc_registry.templatetags.app_filters import gen_value, vals


@login_required(login_url='/')
def fetch_forms(request):
	return JsonResponse({"msg": "ok"})


@login_required(login_url='/')
def fetch_data(request):
	user_orgs = request.user.reg_person.regpersonsorgunits_set.values()
	org_units = []

	for org in user_orgs:
		if not org['is_void']:
			org_units.append(org['org_unit_id'])

	# access performance for this: upper bound of this: How many ovcs per ancestor org
	ovcs_for_org = OVCRegistration.objects.filter(
		is_void=False,
		is_active=True,
		child_cbo_id__in=org_units).order_by('-id')[:1000]  # limit to 1000

	ovc_data = {}

	print "Ovcs count: ", len(ovcs_for_org)

	for ovc in ovcs_for_org:
		full_name = ovc.person.all_names.replace(' ', '')
		full_name = ''.join([str(ord(i)) for i in full_name])


		key = '{full_name}_{reg_person_id}_{ovc_reg_id}'.format(
			full_name=full_name,
			reg_person_id=ovc.person.id,
			ovc_reg_id=ovc.id).upper()

		ovc_data[key] = base64.b64encode(json.dumps({
			'id': key,
			'person_id': ovc.person_id,
			'registration_date': ovc.registration_date.strftime('%d/%m/%Y'),
			'org_unique_id': ovc.org_unique_id,
			'first_name': ovc.person.first_name,
			'surname': ovc.person.surname,
			'other_names': ovc.person.other_names,
			'sex_id': ovc.person.sex_id,
			'date_of_birth': ovc.person.date_of_birth.strftime('%d/%m/%Y'),
			'age': ovc.person.age,
			'registration_date': ovc.registration_date.strftime('%d/%m/%Y'),
			'has_bcert': "Yes" if ovc.has_bcert else "No",
			'is_disabled': "Yes" if ovc.is_disabled else "No",
			'child_chv_full_name': ovc.child_chv.full_name,
			'caretake_full_name': ovc.caretaker.full_name,
			'org_unit_name': ovc.child_cbo.org_unit_name,
			'is_active': 'Active' if ovc.is_active else 'Exited',
			'immunization_status': gen_value(ovc.immunization_status, vals),
			'school_level': gen_value(ovc.school_level, vals),
			'hiv_status': ovc.hiv_status,
			'suppressed': ovc.hiv_status if ovc.hiv_status == "HSTP" else "N/A",

			# facility details
			'facility': _get_ovc_facility_details(ovc),

			# school details

			'school': _get_ovc_school_details(ovc),

			# house hold members
			'household_members': _get_ovc_household_members(ovc)
		}))

	return JsonResponse({
		'data': ovc_data
	})


def _get_ovc_school_details(ovc):
	if ovc.school_level == "SLNS":
		return {}

	try:
		school = OVCEducation.objects.get(person_id=ovc.person.id, is_void=False)
		return {
			'school_name': school.school.school_name,
			'school_class': school.school_class,
			'admission_type': school.admission_type
		}
	except OVCEducation.DoesNotExist as e:
		return {}


def _get_ovc_facility_details(ovc):
	if ovc.hiv_status != 'HSTP':
		return {}

	try:
		health = OVCHealth.objects.get(person_id=ovc.person.id)
		return {
			'name': health.facility.facility_name,
			'art_status': health.art_status,
			'date_linked': health.date_linked.strftime('%d/%m/%Y'),
			'ccc_number': health.ccc_number
		}
	except OVCHealth.DoesNotExist as e:
		return {}


def _get_ovc_household_members(ovc):
	ovc_reg_id = ovc.person.id
	ovc_household = OVCHHMembers.objects.get(is_void=False, person_id=ovc_reg_id)

	if not ovc_household:
		return []

	member_types = {
		'TBVC': 'Sibling',
		'TOVC': 'Enrolled OVC'
	}

	def _is_household_head(member):
		if not member.hh_head:
			if member.member_type == 'TBVC' or member.member_type == 'TOVC':
				return "N/A"
			else:
				"No"
		else:
			return "Yes({})".format(ovc_household.house_hold.head_identifier)

	# Get HH members
	household_id = ovc_household.house_hold.id
	household_members = OVCHHMembers.objects.filter(
		is_void=False, house_hold_id=household_id).order_by("-hh_head")
	household_members = household_members.exclude(person_id=ovc_reg_id)[:10]  # limit 10

	return [{
		'first_name': member.person.first_name,
		'surname': member.person.surname,
		'age': member.person.age,
		'type': member_types.get(member.member_type, 'Parent/Guardian') ,
		'phone_number': member.person.des_phone_number,
		'alive': 'Yes' if member.member_alive == 'AYES' else 'No',
		'hiv_status': member.hiv_status,
		'household_head': _is_household_head(member)
	} for member in household_members]


@login_required(login_url='/')
def offline_mode_test(request):
	if request.method == 'GET':
		return JsonResponse(
			{'msg': "ok testing"}, content_type='application/json', safe=True)
	else:
		print request.body
		return JsonResponse(
			{'msg': "submitted"}, content_type='application/json', safe=True)
