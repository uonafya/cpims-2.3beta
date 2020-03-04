from cpovc_registry.models import RegPersonsOrgUnits
from cpovc_auth.models import AppUser
from notifications.signals import notify


def send_notification(request, type_id, receipient, message):
    """Method to send out notifications."""
    try:
        if type_id == 2:
            # Get users from this Organization unit
            title = "Child tranfer IN"
            org_ids = [receipient]
            person_ids = get_organization_persons(org_ids)
            users = get_users(person_ids)
            for user in users:
                notify.send(user, recipient=user, verb=title,
                            description=message)
    except Exception as e:
        print ('Error sending notifications - %s' % (str(e)))
        pass


def get_organization_persons(org_ids):
    """Method to get organizations."""
    try:
        person_ids = []
        org_persons = RegPersonsOrgUnits.objects.select_related().filter(
            org_unit_id__in=org_ids, is_void=False, date_delinked=None)
        for org_person in org_persons:
            person_ids.append(org_person.person_id)
    except Exception as e:
        print ('Error getting person ids - %s' % (str(e)))
        return []
    else:
        return person_ids


def get_users(person_ids):
    """Method to get organizations."""
    try:
        users = AppUser.objects.filter(
            reg_person_id__in=person_ids, is_active=True)
    except Exception as e:
        print ('Error getting users - %s' % (str(e)))
        return []
    else:
        return users
