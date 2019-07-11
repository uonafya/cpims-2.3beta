from cpovc_main.models import SetupList
from cpovc_ovc.models import OVCEducation, OVCHealth, OVCHHMembers


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
        'type': member_types.get(member.member_type, 'Parent/Guardian'),
        'phone_number': member.person.des_phone_number,
        'alive': 'Yes' if member.member_alive == 'AYES' else 'No',
        'hiv_status': member.hiv_status,
        'household_head': _is_household_head(member)
    } for member in household_members]


def get_services():
    services = SetupList.objects.filter(is_void=False)
    data = {}

    for service in services:
        service_data = {
            'field_name': service.field_name,
            'item_sub_category': service.item_description,
            'status': 1 if service.item_sub_category else 0,
            'item_sub_category_id': service.item_id
        }

        if service.item_id in data:
            data[service.item_id].append(service_data)
        else:
            data[service.item_id] = [service_data]

    return data
