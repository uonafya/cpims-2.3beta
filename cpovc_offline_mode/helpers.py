import base64
import json

from django.core.cache import cache

from cpovc_forms.models import OVCCareEvents, OVCCareAssessment
from cpovc_main.functions import new_guid_32
from cpovc_main.models import SetupList
from cpovc_ovc.models import OVCEducation, OVCHealth, OVCHHMembers
from cpovc_registry.models import RegPerson


def get_ovc_school_details(ovc):
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


def get_ovc_facility_details(ovc):
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


def get_ovc_household_members(ovc):
    ovc_reg_id = ovc.person.id
    ovc_household = OVCHHMembers.objects.get(is_void=False, person_id=ovc_reg_id)

    if not ovc_household:
        return []

    member_types = {
        'TBVC': 'Sibling',
        'TOVC': 'Enrolled OVC'
    }

    def _is_household_head(hh_member):
        if not hh_member.hh_head:
            if hh_member.member_type == 'TBVC' or hh_member.member_type == 'TOVC':
                return "N/A"
            else:
                return "No"
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
        'type': member_types.get(member.member_type, 'Parent/Guardian'),
        'phone_number': member.person.des_phone_number,
        'alive': 'Yes' if member.member_alive == 'AYES' else 'No',
        'hiv_status': member.hiv_status,
        'household_head': _is_household_head(member)
    } for member in household_members]


def get_services():
    olmis_domain_id = 'olmis_domain_id'
    olmis_assessment_domain_id = 'olmis_assessment_domain_id'
    olmis = 'olmis'
    olmis_priority_service = 'olmis_priority_service'
    data = {
        olmis_domain_id: {},
        olmis_assessment_domain_id: {},
        olmis: {},
        olmis_priority_service: {}
    }

    field_names = [olmis_domain_id, olmis_assessment_domain_id, olmis, olmis_priority_service]

    def append_domain_data(domain, field, items):
        for elem in items:
            if domain in data[field]:
                data[field][domain].append(elem)
            else:
                data[field][domain] = [elem]

    def service_to_dict(service_obj):
        return {
            'field_name': service_obj.field_name,
            'item_sub_category': service_obj.item_description,
            'status': 1 if service_obj.item_sub_category else 0,
            'item_sub_category_id': service_obj.item_id
        }

    for field_name in field_names:
        services = []
        if field_name in [olmis_domain_id, olmis_assessment_domain_id, olmis, olmis_priority_service]:
            services = SetupList.objects.filter(field_name=field_name, is_void=False)

        if field_name == olmis:
            services = SetupList.objects.filter(field_name__icontains='olmis', is_void=False)

        for service in services:
            service_sub_category = service.item_sub_category

            if not service_sub_category:
                append_domain_data(service.item_id, field_name, [service_to_dict(service)])
            else:
                sub_categories = SetupList.objects.filter(field_name=service_sub_category, is_void=False)
                sub_categories_as_dict = [service_to_dict(item) for item in sub_categories]
                append_domain_data(service.item_id, field_name, sub_categories_as_dict)
    return data


def save_submitted_form1a(user_id, ovc_id, form_data):
    cache_timeout = 86400 # 1Day
    # handle assessment
    assessment = form_data.get("assessment", {'assessments': []})

    _handle_assessment(
        user_id,
        ovc_id,
        assessment['assessments'],
        form_data.get("date_of_assessment", None),
        cache_timeout)


def _handle_assessment(user_id, ovc_id, assessments, date_of_assessment, cache_timeout):
    if not assessments or not date_of_assessment:
        return

    cache_key = "assessment_offline_{}".format(ovc_id)

    added_assessments = cache.get(cache_key)

    if added_assessments:
        assessments_from_cache = json.loads(base64.b64decode(added_assessments))
    else:
        assessments_from_cache = []

    assessments_to_add = []

    for assessment in assessments:
        encoded_assessment = base64.b64decode(assessment)

        #  dedup to avoid duplication
        if encoded_assessment not in assessments_from_cache:
            assessments_from_cache.append(encoded_assessment)
            assessments_to_add.append(assessment)

    if assessments_to_add:
        cache.set(
            cache_key,
            base64.b64encode(json.dumps(assessments_to_add)),
            timeout=cache_timeout)
        # save assessment
        event_type_id = 'FSAM'
        person = RegPerson.objects.get(pk=int(ovc_id))
        event_counter = OVCCareEvents.objects.filter(event_type_id=event_type_id, person=person, is_void=False).count()
        ovc_care_event = OVCCareEvents(
            event_type_id=event_type_id,
            event_counter=event_counter,
            event_score=0,
            date_of_event=date_of_assessment,
            created_by=user_id,
            person=person
        )
        ovc_care_event.save()
        ovc_care_event_id = ovc_care_event.pk

        for assessment in assessments_to_add:
            olmis_assessment_domain = assessment['olmis_assessment_domain']
            olmis_assessment_service = assessment['olmis_assessment_coreservice']
            olmis_assessment_service_status = assessment['olmis_assessment_coreservice_status']
            service_grouping_id = new_guid_32()

            for service_status in olmis_assessment_service_status.split(","):
                OVCCareAssessment(
                    domain=olmis_assessment_domain,
                    service=olmis_assessment_service,
                    service_status=service_status,
                    event=OVCCareEvents.objects.get(pk=ovc_care_event_id),
                    service_grouping_id=service_grouping_id
                ).save()




