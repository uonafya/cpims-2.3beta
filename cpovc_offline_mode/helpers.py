import base64
import json

from django.core.cache import cache

from cpovc_forms.models import OVCCareEvents, OVCCareAssessment, OVCCareEAV, OVCCarePriority, OVCCareServices
from cpovc_main.functions import new_guid_32, convert_date
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


def save_submitted_form1a(user_id, ovc_id, form_data, org_unit_primary, org_unit_attached):
    assessment = form_data.get('assessment', {'assessments': []})
    priority = form_data.get('priority', {'priorities': []})
    service = form_data.get('service', {'services': []})

    _handle_assessment(
        user_id,
        ovc_id,
        assessment['assessments'],
        assessment.get("date_of_assessment", None))

    _handle_critical_event(user_id, ovc_id, form_data.get('event', None))

    _handle_priority(
        user_id,
        ovc_id,
        priority['priorities'],
        priority.get("date_of_priority", None))

    _handle_services(
        user_id,
        ovc_id,
        service['services'],
        service.get("date_of_service", None),
        org_unit_primary,
        org_unit_attached)


def _create_ovc_care_event(user_id, ovc_id, event_date):
    event_type_id = 'FSAM'
    person = RegPerson.objects.get(pk=int(ovc_id))
    event_counter = OVCCareEvents.objects.filter(event_type_id=event_type_id, person=person, is_void=False).count()
    ovc_care_event = OVCCareEvents(
        event_type_id=event_type_id,
        event_counter=event_counter,
        event_score=0,
        date_of_event=convert_date(event_date),
        created_by=user_id,
        person=person
    )
    ovc_care_event.save()
    return ovc_care_event.pk


def _get_decoded_list_from_cache(cache_key):
    cache_items = cache.get(cache_key, None)

    if cache_items:
        return json.loads(base64.b64decode(cache_items))
    return []


def _add_list_items_to_cache(cache_key, items):
    cache_timeout = 86400  # 1Day
    cache.set(cache_key, base64.b64encode(json.dumps(items)), cache_timeout)


def _handle_critical_event(user_id, ovc_id, critical_event):
    if not critical_event:
        return

    cache_key = "critical_event_offline_{}".format(ovc_id)
    events_list = critical_event.get("olmis_critical_event", None)
    event_date = critical_event.get("date_of_event", None)

    if not events_list or not event_date:
        return

    events = events_list.split(",")
    events_per_date = []

    for event in events:
        events_per_date.append(base64.b64encode("{}#{}".format(event, event_date)))

    events_to_add = []
    cached_events = _get_decoded_list_from_cache(cache_key)

    for event in events_per_date:
        if event not in cached_events:
            cached_events.append(event)
            events_to_add.append(event)

    _add_list_items_to_cache(cache_key, cached_events)

    if events_to_add:
        ovc_care_event_id = _create_ovc_care_event(user_id, ovc_id, event_date)

        for item in events_to_add:
            events = base64.b64decode(item).split("#")
            OVCCareEAV(
                entity='CEVT',
                attribute='FSAM',
                value=events[0],
                event=OVCCareEvents.objects.get(pk=ovc_care_event_id)).save()


def _handle_assessment(user_id, ovc_id, assessments, date_of_assessment):
    if not assessments or not date_of_assessment:
        return

    cache_key = "assessment_offline_{}".format(ovc_id)

    assessments_to_add = []

    for assessment in assessments:
        not_added = _add_assessments_to_cache(
            cache_key,
            assessment['olmis_assessment_domain'],
            assessment['olmis_assessment_coreservice'],
            assessment['olmis_assessment_coreservice_status'],
            date_of_assessment)

        for item in not_added:
            assessments_to_add.append(item)

    if assessments_to_add:
        service_grouping_id = new_guid_32()
        ovc_care_event_id = _create_ovc_care_event(user_id, ovc_id, date_of_assessment)
        for item in assessments_to_add:
            events = item.split("#")

            OVCCareAssessment(
                domain=events[0],
                service=events[1],
                service_status=events[2],
                event=OVCCareEvents.objects.get(pk=ovc_care_event_id),
                service_grouping_id=service_grouping_id
            ).save()


def _add_assessments_to_cache(cache_key, domain, service, status, date_of_assessment):
    statuses = status.split(",")
    statuses_per_domain_service = []

    for status in statuses:
        statuses_per_domain_service.append("{}#{}#{}#{}".format(domain, service, status, date_of_assessment))

    assessments_to_add = []
    assessments_from_cache = _get_decoded_list_from_cache(cache_key)

    for assessment in statuses_per_domain_service:
        if assessment not in assessments_from_cache:
            assessments_from_cache.append(assessment)
            assessments_to_add.append(assessment)

    _add_list_items_to_cache(cache_key, assessments_from_cache)

    return assessments_to_add


def _handle_priority(user_id, ovc_id, priorities, date_of_priority):
    if not priorities or not date_of_priority:
        return

    cache_key = "priority_offline_{}".format(ovc_id)

    priority_to_add = []

    for priority in priorities:
        not_added = _add_priority_to_cache(
            cache_key,
            priority['olmis_priority_domain'],
            priority['olmis_priority_service'],
            date_of_priority)

        for item in not_added:
            priority_to_add.append(item)

    if priority_to_add:
        service_grouping_id = new_guid_32()
        ovc_care_event_id = _create_ovc_care_event(user_id, ovc_id, date_of_priority)
        for item in priority_to_add:
            events = item.split("#")

            OVCCarePriority(
                domain=events[0],
                service=events[1],
                event=OVCCareEvents.objects.get(pk=ovc_care_event_id),
                service_grouping_id=service_grouping_id
            ).save()


def _add_priority_to_cache(cache_key, domain, service, date_of_priority):
    services = service.split(",")
    service_per_domain = []

    for service in services:
        service_per_domain.append("{}#{}#{}".format(domain, service, date_of_priority))

    priorities_to_to_add = []
    priorities_from_cache = _get_decoded_list_from_cache(cache_key)

    for priority in service_per_domain:
        if priority not in priorities_from_cache:
            priorities_from_cache.append(priority)
            priorities_to_to_add.append(priority)

    _add_list_items_to_cache(cache_key, priorities_from_cache)

    return priorities_to_to_add


def _handle_services(user_id, ovc_id, services, date_of_service, org_unit_primary, org_unit_attached):
    if not services or not date_of_service:
        return

    cache_key = "service_offline_{}".format(ovc_id)

    services_to_add = []

    for service in services:
        not_added = _add_service_to_cache(
            cache_key,
            service['olmis_domain'],
            service['olmis_service'],
            service['olmis_service_date'],
            date_of_service)

        for item in not_added:
            services_to_add.append(item)

    if services_to_add:
        service_grouping_id = new_guid_32()
        ovc_care_event_id = _create_ovc_care_event(user_id, ovc_id, date_of_service)
        org_unit = org_unit_primary if org_unit_primary else org_unit_attached[0]
        for item in services_to_add:
            events = item.split("#")

            OVCCareServices(
                domain=events[0],
                service_provided=events[1],
                date_of_encounter_event=convert_date(events[2]) if not events[2] or events[2] != 'None' or events[2] != '' else None,
                service_provider=org_unit,
                event=OVCCareEvents.objects.get(pk=ovc_care_event_id),
                service_grouping_id=service_grouping_id
            ).save()


def _add_service_to_cache(cache_key, domain, service_list, service_date, date_of_priority):
    services = service_list.split(",")
    service_per_domain = []

    for service in services:
        service_per_domain.append("{}#{}#{}#{}".format(domain, service, service_date, date_of_priority))

    services_to_to_add = []
    services_from_cache = _get_decoded_list_from_cache(cache_key)

    for service in service_per_domain:
        if service not in services_from_cache:
            services_from_cache.append(service)
            services_to_to_add.append(service)

    _add_list_items_to_cache(cache_key, services_from_cache)

    return services_to_to_add
